import bpy,bmesh,os,json,math,numpy as np
from mathutils import Vector,Matrix
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'output')
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m}
COL={c.name:c for c in bpy.data.collections}
for name in ['CONSTRUCTION','VENTILATION']:
 c=bpy.data.collections.new(name)
 for sc in bpy.data.scenes:sc.collection.children.link(c)
 COL[name]=c
def cv(p):return Vector((p[0],-p[2],p[1]))
def put(o,col):
 for c in list(o.users_collection):c.objects.unlink(o)
 COL[col].objects.link(o);return o
def box(name,p,size,mat='blackMetal',col='CONSTRUCTION',bev=.002):
 bpy.ops.mesh.primitive_cube_add(size=1,location=cv(p));o=bpy.context.object;o.name=name;o.dimensions=(size[0],size[2],size[1]);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(M[mat]);put(o,col)
 if bev:md=o.modifiers.new('Arista constructiva','BEVEL');md.width=bev;md.segments=2
 return o
def cyl(name,a,b,r,mat='blackMetal',col='CONSTRUCTION'):
 a,b=cv(a),cv(b);bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=r,depth=(b-a).length,location=(a+b)/2);o=bpy.context.object;o.name=name;o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();o.data.materials.append(M[mat]);put(o,col)
 for p in o.data.polygons:p.use_smooth=True
 return o
def remove(name):
 o=bpy.data.objects.get(name)
 if o:bpy.data.objects.remove(o,do_unlink=True)
def cut(o,c):
 bpy.context.view_layer.objects.active=o;md=o.modifiers.new('Hueco constructivo','BOOLEAN');md.operation='DIFFERENCE';md.solver='EXACT';md.object=c;bpy.ops.object.modifier_apply(modifier=md.name)
def bounds(o):
 p=np.array([o.matrix_world@Vector(v) for v in o.bound_box]);return p.min(0),p.max(0)
notes=json.loads(S['corrections'])
# 1. Gate runs on a physically separate interior track.
gate=bpy.data.objects['DOOR | gate'];gate.location.y-=.22;gate.location.z+=.085
gate['construction_note']='Track shifted 0.22m into lot, leaf lifted 0.085m above original datum; 3.00m clear opening retained. Travel remains 3.05m.'
box('Portón | riel interior paralelo',[10.95,.073,.25],[6.65,.018,.025],col='DOORS')
for x in [11.22,13.75]:
 roller=cyl('Portón | rueda de acero',[x,.13,.195],[x,.13,.255],.048,'stainless','DOORS');bpy.context.view_layer.update();mw=roller.matrix_world.copy();roller.parent=gate;roller.matrix_parent_inverse=gate.matrix_world.inverted();roller.matrix_world=mw
for x in [10.88,14.10]:
 box('Portón | guía de retención',[x,1.90,.25],[.065,.12,.13],col='DOORS')
# 2. Complement fine vertical railing infill, preserving the source rail height and position.
for key,a,b in [('lateral',[13.02,5],[13.02,12.98]),('posterior',[13.02,12.98],[21.98,12.98])]:
 d=Vector(b)-Vector(a);N=math.ceil(d.length/.10)
 for j in range(1,N):
  q=Vector(a)+d*j/N;box('Baranda '+key+' | barrotes de protección %03d'%j,[q.x,3.744,q.y],[.012,.928,.012],col='UPPER_FLOOR',bev=.001)
for o in list(S.objects):
 if o.name.startswith(('Baranda lateral poste','Baranda posterior poste')):
  x,y,z=o.location.x,o.location.z,-o.location.y
  box(o.name+' | placa base',[x,3.21,z],[.105,.012,.105],col='UPPER_FLOOR')
  for dx,dz in [(-.033,-.033),(.033,-.033),(-.033,.033),(.033,.033)]:cyl(o.name+' | anclaje',[x+dx,3.215,z+dz],[x+dx,3.233,z+dz],.005,'stainless','UPPER_FLOOR')
for x in [13.02,13.98]:
 for j in range(1,38):
  z=1.20+j*3.8/38;floor=3.2-(5-z)*(3.14/3.8)
  box('Escalera | protección vertical %s %02d'%(x,j),[x,floor+.57,z],[.012,.94,.012],col='STAIR',bev=.001)
for o in [o for o in S.objects if o.name.startswith('Peldaño exterior ') and o.type=='MESH']:
 lo,hi=bounds(o);box(o.name+' | banda antideslizante',[(lo[0]+hi[0])/2,hi[2]+.0025,-hi[1]+.026],[.90,.005,.022],'blackMetal','STAIR',.0007)
# 3. Remove physical acoustic overlap with dry construction joints.
baffles=[o for o in S.objects if o.name.startswith('Bafle cielorraso estudio')];clouds=[o for o in S.objects if o.name.startswith('Cloud estudio')]
for cloud in clouds:
 for baff in baffles:
  a,b=bounds(cloud);c,d=bounds(baff)
  if np.all(np.minimum(b,d)-np.maximum(a,c)>0):
   cutter=box('Temporal junta acústica',[(c[0]+d[0])/2,(c[2]+d[2])/2,-(c[1]+d[1])/2],[d[0]-c[0]+.008,.40,d[1]-c[1]+.008],col='REFERENCE',bev=0)
   cut(cloud,cutter);bpy.data.objects.remove(cutter,do_unlink=True)
 cloud['construction_note']='Carved around primary baffles with 4mm dry joints; all undersides >=6.45m.'
# 4. User direction: dwelling 2.60m clear; studio3.20m, higher exterior studio roof.
rise=.60
for o in S.objects:
 if o.name=='Cubierta pendiente Cedro Misionero' or o.name.startswith('Chapa | nervadura 0') or o.name in ['Cumbrera','Canaleta frontal']:o.location.z+=rise
# Rebuild gables with a real vertical step at the boundary between modules.
for oldname,x,mat in [('Frontón lateral izquierdo',14.08,'brick'),('Frontón medianera derecha',21.92,'brickDark')]:
 remove(oldname)
 profile=[(0,6.4),(12,6.4),(6,7.5),(6,8.10),(0,7.0)]
 p=[cv([xx,h,z]) for xx in [x-.09,x+.09] for z,h in profile];n=len(profile);f=[tuple(range(n-1,-1,-1)),tuple(range(n,n*2))]
 for i in range(n):j=(i+1)%n;f.append((i,j,n+j,n+i))
 me=bpy.data.meshes.new(oldname+' | escalonado');me.from_pydata(p,[],f);me.materials.append(M[mat]);o=bpy.data.objects.new(oldname,me);COL['ROOF'].objects.link(o)
box('Estudio | recrecido de fachada bajo cubierta',[18,6.70,.10],[8,.60,.20],'brick','ROOF')
box('Encuentro estudio vivienda | cierre alto',[18,7.24,6.0],[7.64,1.68,.16],'brickDark','ROOF')
box('Cubierta escalonada | babeta vertical',[18,7.825,6.105],[8.62,.68,.022],'blackMetal','ROOF')
box('Cubierta vivienda | contrababeta de encuentro',[18,7.535,6.16],[8.62,.025,.32],'blackMetal','ROOF')
# Front downpipe extension and end shoe.
box('Bajada frontal | prolongación por estudio elevado',[21.72,6.64,.08],[.055,.62,.055],'blackMetal','ROOF')
# Lightweight ceiling for the dwelling; bathroom has source finish +3.30m.
ceiling=box('Cielorraso vivienda | 2.60m sobre piso general',[18,5.859,9.0],[7.60,.018,5.60],'whitePlaster','INTERIORS',0)
# Main ceiling is cut above bathroom, where a separate +5.90m ceiling yields2.60m over tiles.
cutter=box('Temporal techo baño',[20.65,5.87,7.3],[2.28,.5,2.37],col='REFERENCE',bev=0);cut(ceiling,cutter);bpy.data.objects.remove(cutter,do_unlink=True)
box('Cielorraso baño | 2.60m sobre porcelanato',[20.65,5.909,7.3],[2.25,.018,2.35],'whitePlaster','INTERIORS',0)
# Rafters, bearing beams and ceiling channels occupy the now available construction depth.
slope=math.atan(1.1/6)
for front,z,center in [(True,3,7.55),(False,9,6.95)]:
 sign=-1 if front else 1
 for i,x in enumerate(np.linspace(14.32,21.28,11)):
  o=box(('Estudio' if front else 'Vivienda')+' | cabio %02d'%i,[float(x),center-.21,z],[.08,.22,6.17],'blackMetal','CONSTRUCTION');o.rotation_euler.x=sign*slope
 for zz in np.linspace(.15,5.85,8) if front else np.linspace(6.15,11.85,8):
  h=(7.0+(zz)*1.1/6) if front else (7.5-(zz-6)*1.1/6)
  o=box(('Estudio' if front else 'Vivienda')+' | correa secundaria',[18,float(h-.067),float(zz)],[7.58,.055,.045],'blackMetal','CONSTRUCTION')
 for zz in ([.10,5.90] if front else [6.10,11.90]):
  h=(7.0+zz*1.1/6) if front else (7.5-(zz-6)*1.1/6)
  box(('Estudio' if front else 'Vivienda')+' | viga de apoyo',[18,float(h-.21),zz],[7.62,.22,.14],'concreteDark','CONSTRUCTION')
 for i,xx in enumerate(np.linspace(14.4,21.6,13)):
  box(('Estudio' if front else 'Vivienda')+' | canal de cielorraso %02d'%i,[float(xx),6.625 if front else 5.98,z],[.035,.04,5.52],'blackMetal','CONSTRUCTION')
 # Insulated lining follows each exterior slope, normal offset below metal.
 roof=bpy.data.objects['Cubierta pendiente Cedro Misionero' if front else 'Cubierta pendiente pileta']
 insulation=roof.copy();insulation.data=roof.data.copy();insulation.name=('Estudio' if front else 'Vivienda')+' | aislación y membrana bajo chapa';COL['CONSTRUCTION'].objects.link(insulation)
 insulation.location.z-=.075;insulation.data.materials.clear();insulation.data.materials.append(M['whitePlaster'])
# Isolation mounts suspend studio treatment clear of the ceiling.
for baff in baffles:
 for z in [2.05,3.95]:
  cyl('Acústica | suspensión antivibratoria',[baff.location.x,6.56,z],[baff.location.x,6.635,z],.009,'blackMetal','STUDIO')
light=bpy.data.objects.get('LED | Luz lineal estudio')
if light:light.location.z=6.42;light.data.energy=140
# 5. Independent extraction paths, routed under slab and into rear corner studio service shaft.
def pipe(name,points,r):
 pp=[cv(p) for p in points];N=24;verts=[];faces=[]
 for i,p in enumerate(pp):
  t=(pp[min(i+1,len(pp)-1)]-pp[max(0,i-1)]).normalized();up=Vector((0,0,1))
  if abs(t.dot(up))>.92:up=Vector((1,0,0))
  a=t.cross(up).normalized();b=t.cross(a).normalized()
  for rad in [r,r-.014]:
   for j in range(N):v=p+(a*math.cos(j*math.tau/N)+b*math.sin(j*math.tau/N))*rad;verts.append(v)
 for i in range(len(pp)-1):
  for layer in [0,1]:
   for j in range(N):
    j2=(j+1)%N;f=(i*2*N+layer*N+j,i*2*N+layer*N+j2,(i+1)*2*N+layer*N+j2,(i+1)*2*N+layer*N+j)
    faces.append(f if layer==0 else tuple(reversed(f)))
 for i in [0,len(pp)-1]:
  for j in range(N):j2=(j+1)%N;faces.append((i*2*N+j,i*2*N+j2,i*2*N+N+j2,i*2*N+N+j))
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.materials.append(M['blackMetal']);me.update()
 for f in me.polygons:f.use_smooth=True
 o=bpy.data.objects.new(name,me);COL['VENTILATION'].objects.link(o);o['inferred_detail']='Independent insulated flue. Coordinated geometry; routing is inferred from absent source services.';return o
routes=[
 ('Horno',.105,[[21.25,2.60,6.75],[21.25,2.68,6.75],[21.30,2.70,6.60],[21.30,2.72,5.52],[21.38,2.77,5.32],[21.56,2.86,5.32],[21.56,3.04,5.32],[21.56,8.70,5.32]]),
 ('Parrilla',.16,[[21.65,2.65,9.44],[21.65,2.65,9.10],[21.65,2.69,6.10],[21.65,2.74,5.91],[21.58,2.88,5.72],[21.58,3.08,5.72],[21.58,8.70,5.72]])]
# Physical wall sleeves at two independent penetrations; no floor opening over bath/kitchen fixtures.
wall=bpy.data.objects['Separación mono quincho derecha']
for name,r,pts in routes:
 pipe('Extracción '+name+' | conducto continuo aislado',pts,r)
 x,y=(21.30,2.713) if name=='Horno' else (21.65,2.691)
 cutter=cyl('Temporal pasamuros',[x,y,5.75],[x,y,6.25],r+.025,col='REFERENCE');cut(wall,cutter);bpy.data.objects.remove(cutter,do_unlink=True)
 x,z=pts[-1][0],pts[-1][2]
 # Slab, source finish, studio ceiling and roof penetrations.
 for nm in ['Losa entre plantas','Piso estudio','Cielorraso estudio | cota inferior 6.45m','Cubierta pendiente Cedro Misionero','Estudio | aislación y membrana bajo chapa']:
  ob=bpy.data.objects[nm];cutter=cyl('Temporal paso de conducto',[x,2.9,z],[x,8.5,z],r+.028,col='REFERENCE');cut(ob,cutter);bpy.data.objects.remove(cutter,do_unlink=True)
 h=7.0+z*1.1/6
 box(name+' | babeta de cubierta',[x,h+.047,z],[r*2+.19,.022,r*2+.19],'blackMetal','VENTILATION')
 # Raised rain cap on supports, leaving open annular discharge.
 for angle in [0,math.tau/3,2*math.tau/3]:
  xx=x+r*.75*math.cos(angle);zz=z+r*.75*math.sin(angle);cyl(name+' | soporte sombrerete',[xx,8.65,zz],[xx,8.85,zz],.006,col='VENTILATION')
 bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=r+.065,radius2=.025,depth=.07,location=cv([x,8.865,z]));cap=bpy.context.object;cap.name=name+' | sombrerete antilluvia';cap.data.materials.append(M['blackMetal']);put(cap,'VENTILATION')
# Noncombustible service shaft is entirely behind the studio acoustic panel end.
box('Patinillo extracción | frente registrable',[21.315,5.68,5.50],[.025,5.1,.81],'whitePlaster','VENTILATION')
box('Patinillo extracción | lateral anterior',[21.565,5.68,5.085],[.525,5.1,.025],'whitePlaster','VENTILATION')
box('Patinillo extracción | lateral posterior',[21.565,5.68,5.915],[.525,5.1,.025],'whitePlaster','VENTILATION')
box('Patinillo | registro estudio',[21.298,3.82,5.48],[.015,.62,.42],'whitePlaster','VENTILATION')
# Complete kitchen hood exhaust through its own shaft, away from sanitary fixtures.
pipe('Extracción cocina | salida independiente',[[21.54,5.00,10.31],[21.54,7.95,10.31]],.085)
for nm in ['Cielorraso vivienda | 2.60m sobre piso general','Cubierta pendiente pileta','Vivienda | aislación y membrana bajo chapa','Revestimiento interior | Cubierta pendiente pileta']:
 ob=bpy.data.objects.get(nm)
 if ob:
  cutter=cyl('Temporal paso cocina',[21.54,5.5,10.31],[21.54,8,10.31],.11,col='REFERENCE');cut(ob,cutter);bpy.data.objects.remove(cutter,do_unlink=True)
box('Cocina | babeta sobre cubierta',[21.54,6.755,10.31],[.38,.022,.38],'blackMetal','VENTILATION')
cyl('Cocina | remate superior',[21.54,7.97,10.31],[21.54,8.01,10.31],.13,col='VENTILATION')
# Technical facts and distinctions preserved inside project.
notes += [
'User clarified: dwelling approximately2.60m clear, studio3.20m. General dwelling ceiling+5.85 over+3.25; bathroom+5.90 over+3.30. Studio exterior front roof raised0.60m relative to rear module, with stepped gables and flashing; inference ties roof difference to interior height difference.',
'Iteration1 pass1: gate offset0.22m to inner parallel track and lifted0.085m, maintaining3m opening and3.05m slide. Added fine vertical railing infill, post base anchors and stair anti-slip strips.',
'Iteration1 pass1: acoustic clouds cut around baffles with4mm dry joints; retained3.20m minimum clear height.',
'Iteration1 pass1: roof support, insulation, ceiling channels and stepped flashing added within real available roof cavity; these are coordinated detail geometry, not structural calculations.',
'Iteration1 pass1: independent insulated oven/grill ducts run under slab through sleeved partition penetrations into studio rear-right service shaft; no pipe passes through upstairs bath/kitchen fixtures. Independent kitchen exhaust added. Services are inferred because absent in HTML.'
]
S['corrections']=json.dumps(notes,ensure_ascii=False);S['dwelling_clear_height']=2.6;S['studio_clear_height']=3.2;S['studio_roof_step']=.6;S['review_iteration']='1 / pass1 construction';S['video_render_requires_explicit_approval']=True
json.dump({'routes':routes,'shaft_source_bounds':{'x':[21.3025,21.8275],'z':[5.0725,5.9275]},'studio_roof_rise':.6,'studio_clear':3.2,'dwelling_clear':2.6},open(os.path.join(ROOT,'review','construction_details.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
S.frame_set(1);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Casa_de_Campo.blend'),compress=True)
print('PASS1_CONSTRUCTION_SAVED',len(S.objects),flush=True)
