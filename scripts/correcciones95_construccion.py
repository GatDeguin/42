import bpy,bmesh,os,json,math,ast,numpy as np
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
for nd in ast.parse(open(os.path.join(ROOT,'scripts','iteration1_pass1.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['cv','put','box','cyl','cut','bounds']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
def newmesh(name,vertices,faces,mat='blackMetal',col='CONSTRUCTION',bevel=0):
 me=bpy.data.meshes.new(name);me.from_pydata([cv(p) for p in vertices],[],faces);me.materials.append(M[mat]);bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
 o=bpy.data.objects.new(name,me);COL[col].objects.link(o)
 if bevel:md=o.modifiers.new('Borde de fabricación','BEVEL');md.width=bevel;md.segments=2
 return o
def erase(names):
 for name in names:
  o=bpy.data.objects.get(name)
  if o:bpy.data.objects.remove(o,do_unlink=True)
for o in list(S.objects):
 if o.name.startswith('PL95 |') or o.name.startswith('AC95 |'):bpy.data.objects.remove(o,do_unlink=True)
erase(['Canaleta frontal','Canaleta posterior','Bajada pluvial frontal','Bajada pluvial posterior','Bajada frontal | prolongación por estudio elevado'])
def smoothpath(points,r=.14):
 p=[Vector(a) for a in points];out=[p[0]]
 for a,b,c in zip(p,p[1:],p[2:]):
  v=b-a;w=c-b;rr=min(r,v.length*.24,w.length*.24);start=b-v.normalized()*rr;end=b+w.normalized()*rr;out.append(start)
  for k in range(1,9):
   t=k/8;out.append((1-t)**2*start+2*(1-t)*t*b+t*t*end)
 out.append(p[-1]);return out
def tube(name,points,outer=.055,inner=.052,mat='blackMetal'):
 ps=smoothpath(points);vs=[];n=24;prev=None
 for i,p in enumerate(ps):
  tangent=(ps[min(i+1,len(ps)-1)]-ps[max(0,i-1)]).normalized()
  if prev is None:
   ref=Vector((0,1,0)) if abs(tangent.y)<.9 else Vector((1,0,0));u=tangent.cross(ref).normalized()
  else:u=(prev-tangent*prev.dot(tangent)).normalized()
  v=tangent.cross(u).normalized();prev=u
  for rad in [outer,inner]:
   vs += [list(p+rad*(u*math.cos(k*math.tau/n)+v*math.sin(k*math.tau/n))) for k in range(n)]
 fs=[]
 for i in range(len(ps)-1):
  for k in range(n):
   j=(k+1)%n;a=i*2*n;b=(i+1)*2*n
   fs.append((a+k,a+j,b+j,b+k));fs.append((a+n+j,a+n+k,b+n+k,b+n+j))
 for k in range(n):
  j=(k+1)%n;fs.append((j,k,n+k,n+j));a=(len(ps)-1)*2*n;fs.append((a+k,a+j,a+n+j,a+n+k))
 ob=newmesh(name,vs,fs,mat)
 for p in ob.data.polygons:p.use_smooth=True
 ob['system']='pluvial';ob['outside_diameter']=outer*2;ob['inside_diameter']=inner*2;ob['centreline_source']=json.dumps(points);return ob
def gutter(name,z,low,outlet):
 xmin,xmax=13.675,22.325;xs=[xmin,outlet,xmax];th=.0012;w=.16;h=.14;profile=[(-w/2,0),(w/2,0),(w/2,h),(w/2-th,h),(w/2-th,th),(-w/2+th,th),(-w/2+th,h),(-w/2,h)]
 vs=[(x,low+abs(x-outlet)*.005+v,z+u) for x in xs for u,v in profile];fs=[]
 for i in range(2):
  for k in range(8):fs.append((i*8+k,i*8+(k+1)%8,(i+1)*8+(k+1)%8,(i+1)*8+k))
 fs.extend([tuple(range(7,-1,-1)),tuple(range(16,24))]);o=newmesh(name,vs,fs)
 cutter=cyl('Temporal salida pluvial',[outlet,low-.1,z],[outlet,low+.1,z],.0555,col='REFERENCE');cut(o,cutter);bpy.data.objects.remove(cutter,do_unlink=True)
 o['fall_percent']=.5;o['wall_thickness']=th;o['outlet_source']=json.dumps([outlet,low,z])
 for x in [14,15.2,16.4,17.6,18.8,20,21.2,22.15]:
  # Brackets cradle underside and return toward eave; do not bridge the receiving opening.
  box(name+' | soporte',[x,low+abs(x-outlet)*.005-.008,z],[.024,.008,.18],bev=.001)
 return o
front=gutter('PL95 | canaleta frontal abierta',-.08,6.895,13.80)
rear=gutter('PL95 | canaleta posterior abierta',12.08,6.295,21.78)
frontpath=[[13.8,6.897,-.08],[13.8,6.75,-.08],[13.62,6.58,-.08],[13.62,6.40,.50],[13.62,.20,.50],[13.62,-.20,.70]]
rearpath=[[21.78,6.297,12.08],[21.78,6.16,12.08],[21.78,6.03,12.24],[21.78,.16,12.24],[21.78,-.30,12.42],[21.65,-.35,13.50]]
tube('PL95 | bajada frontal continua',frontpath)
tube('PL95 | bajada posterior continua',rearpath)
# Sleeved passage through the balcony, coordinated away from corner supports.
balcony=bpy.data.objects['Balcón posterior']
c=cyl('Temporal paso pluvial balcón',[21.78,2.95,12.24],[21.78,3.40,12.24],.079,col='REFERENCE');cut(balcony,c);bpy.data.objects.remove(c,do_unlink=True)
tube('PL95 | manguito balcón',[ [21.78,3.00,12.24],[21.78,3.29,12.24]],.077,.072,'stainless')
for side,x,z,ys in [('frontal',13.62,.50,[.55,1.8,3.3,4.7,6.0]),('posterior',21.78,12.24,[.55,1.8,3.4,4.6,5.8])]:
 for h in ys:
  # Two independent straps and a masonry bracket outside the tube bore.
  for dx in [-.061,.061]:box('PL95 | abrazadera '+side,[x+dx,h,z],[.009,.024,.12],bev=.001)
  anchorx=13.98 if side=='frontal' else x
  if side=='frontal':box('PL95 | ménsula '+side,[(x+.061+anchorx)/2,h,z],[(anchorx-x-.061),.02,.02],bev=.001)
  else:box('PL95 | ménsula '+side,[x,h,12.09],[.022,.022,.19],bev=.001)
def chamber(name,x,z,top=.06):
 low=-.52;outer=.48;th=.035
 for xx in [x-outer/2+th/2,x+outer/2-th/2]:box(name+' | pared',[xx,(top+low)/2,z],[th,top-low,outer],'concrete',bev=.002)
 for zz in [z-outer/2+th/2,z+outer/2-th/2]:box(name+' | pared',[x,(top+low)/2,zz],[outer-th*2,top-low,th],'concrete',bev=.002)
 box(name+' | fondo',[x,low-.015,z],[outer,.03,outer],'concrete',bev=.001)
 for xx in [x-.22,x+.22]:box(name+' | marco',[xx,top-.012,z],[.025,.024,.46],bev=.001)
 for zz in [z-.22,z+.22]:box(name+' | marco',[x,top-.012,zz],[.46,.024,.025],bev=.001)
 for i in range(14):
  xx=x-.20+i*.4/13
  # Front inlet tube enters the rear-right half; leave an actual receiving throat.
  for a,b in [(z-.20,z+.20)]:
   if 'frontal' in name and abs(xx-13.62)<.07:
    for aa,bb in [(a,.62),(.78,b)]:
     if bb>aa:box(name+' | rejilla',[xx,top-.004,(aa+bb)/2],[.012,.008,bb-aa],'stainless',bev=.001)
   else:box(name+' | rejilla',[xx,top-.004,z],[.012,.008,.40],'stainless',bev=.001)
chamber('PL95 | cámara frontal registrable',13.62,.70)
chamber('PL95 | cámara posterior registrable',21.65,13.50)
# Buried collector avoids the building footprint and stairs by following garden edges.
collector=[[21.65,-.40,13.5],[12.60,-.45,13.5],[12.60,-.55,.70],[12.60,-.57,.10]]
main_tube=tube('PL95 | colector enterrado de jardín',collector,.080,.074,'concreteDark')
branch_tube=tube('PL95 | enlace cámara frontal',[[13.62,-.39,.7],[12.60,-.55,.7]],.065,.060,'concreteDark')
# Open the branch/main tee: each shell must leave the communicating bore unobstructed.
c=cyl('Temporal boca ramal T',[13.62,-.39,.7],[12.60,-.55,.7],.060,col='REFERENCE');cut(main_tube,c);bpy.data.objects.remove(c,do_unlink=True)
c=cyl('Temporal continuidad colector T',[12.60,-.5484,.9],[12.60,-.5567,.5],.074,col='REFERENCE');cut(branch_tube,c);bpy.data.objects.remove(c,do_unlink=True)
main_tube['tee_open_bore']=True;branch_tube['tee_open_bore']=True
# Cut real openings in chamber walls at crossing points.
for name in ['PL95 | cámara posterior registrable | pared','PL95 | cámara frontal registrable | pared']:
 for o in [v for v in S.objects if v.name.startswith(name)]:
  for pts,rad in [(collector,.081),(frontpath,.056),(rearpath,.056),([[13.62,-.39,.7],[12.60,-.55,.7]],.066)]:
   for a,b in zip(pts,pts[1:]):
    va,vb=cv(a),cv(b);pmin,pmax=bounds(o)
    if all(max(min(va[i],vb[i])-rad,pmin[i])<min(max(va[i],vb[i])+rad,pmax[i]) for i in range(3)):
     c=cyl('Temporal boca cámara',a,b,rad,col='REFERENCE');cut(o,c);bpy.data.objects.remove(c,do_unlink=True)
# Stair finish:18 equal risers from +0.06 to+3.25, source run and width unchanged.
treads=sorted([o for o in S.objects if o.name.startswith('Peldaño exterior ') and '|' not in o.name],key=lambda o:o.location.z)
for j,o in enumerate(treads):
 dz=.05*(j+1)/18;o.location.z+=dz
 for child in [v for v in S.objects if v.name.startswith(o.name+' |')]:child.location.z+=dz
 o['finished_top']=.06+(j+1)*(3.25-.06)/18
# Raise ends of steel stringers and stair protection progressively to the new finish.
for o in list(S.objects):
 if o.type!='MESH':continue
 if o.name.startswith(('Zanca ','Escalera | protección vertical','Pasamanos escalera','Poste escalera','Placa unión escalera descanso','Perfil encuentro descanso escalera')):
  o.data=o.data.copy();inv=o.matrix_world.inverted()
  for v in o.data.vertices:
   w=o.matrix_world@v.co;factor=max(0,min(1,(-w.y-1.2)/3.8));w.z+=.05*factor;v.co=inv@w
 if o.name.startswith(('Baranda lateral','Baranda posterior')):o.location.z+=.05
box('AC95 | pavimento de arranque cota 0.06',[13.5,0, .68],[1.14,.12,1.0],'concrete',bev=.008)
def finish(name,corners,base):
 # corners[(x,z,top)] counterclockwise in source plan; bottom remains on structural slab.
 verts=[(x,base,z) for x,z,h in corners]+[(x,h,z) for x,z,h in corners];n=len(corners)
 faces=[tuple(range(n-1,-1,-1))]
 if n==4:faces += [(n,n+1,n+3),(n+1,n+2,n+3)]
 else:faces.append(tuple(range(n,n*2)))
 faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return newmesh(name,verts,faces,'paver','UPPER_FLOOR',.001)
landing=finish('AC95 | acabado descanso al umbral',[(13,5,3.25),(14,5,3.25),(14,6,3.25),(13,6,3.235)],3.20)
landing['level_at_stair_and_door']=3.25;landing['low_corner_level']=3.235
sidefinish=finish('AC95 | acabado balcón lateral',[(13,6,3.235),(14,6,3.25),(14,12,3.25),(13,12,3.235)],3.21)
rearfinish=finish('AC95 | acabado balcón posterior',[(14,12,3.25),(22,12,3.25),(22,13,3.235),(14,13,3.235)],3.21)
finish('AC95 | acabado esquina de balcón',[(13,12,3.235),(14,12,3.25),(14,13,3.235),(13,13,3.235)],3.21)
c=cyl('Temporal acabado sleeve',[21.78,3.19,12.24],[21.78,3.36,12.24],.079,col='REFERENCE');cut(rearfinish,c);bpy.data.objects.remove(c,do_unlink=True)
# Reserve the complete fixed and moving sill envelopes, including the side leaf's open position.
c=box('Temporal reserva guía lateral',[13.91,3.26,10.36],[.29,.14,2.66],col='REFERENCE',bev=0);cut(sidefinish,c);bpy.data.objects.remove(c,do_unlink=True)
c=box('Temporal reserva guía posterior',[18,3.26,12.05],[8.02,.14,.13],col='REFERENCE',bev=0);cut(rearfinish,c);bpy.data.objects.remove(c,do_unlink=True)
sidefinish['sill_clearance']='Finish stops at X13.765 beside the complete sliding-track sweep; retain 7.5mm minimum geometric clearance.'
rearfinish['sill_clearance']='Finish starts at Z12.115 beyond sills; 15mm elastic perimeter joint.'
# Seal the finish perimeter without filling the track drainage or leaf space.
box('AC95 | junta perimetral riel lateral',[13.761,3.242,10.36],[.006,.005,2.66],'blackMetal',col='UPPER_FLOOR',bev=.0005)
box('AC95 | junta perimetral riel posterior',[18,3.243,12.108],[8,.005,.012],'blackMetal',col='UPPER_FLOOR',bev=.0005)
# Finished edge joint and waterproofing upstand stop below the actual door opening.
for zz in [5.10,5.75]:box('AC95 | junta elástica umbral',[13.97,3.247,zz],[.055,.006,.012],'blackMetal',bev=.001)
# Sub-sill tray follows the full studio opening with end dams.
box('AC95 | bandeja bajo umbral',[14.01,3.203,5.30],[.35,.002,.96],'stainless',bev=0)
for zz in [4.825,5.775]:box('AC95 | retorno bandeja umbral',[14.01,3.222,zz],[.35,.04,.002],'stainless',bev=0)
# Open-railed balconies shed toward a continuous folded drip edge.
# No closed scupper below finish: exposed overflow edge discharges to the garden strip.
def drip(name,points,axis):
 profile=[(.06,3.234),(-.035,3.231),(-.035,3.199),(-.033,3.199),(-.033,3.229),(.06,3.232)]
 verts=[]
 for q in points:
  for u,h in profile:
   verts.append((13+u,h,q) if axis=='x' else (q,h,13-u))
 n=len(profile);faces=[tuple(range(n-1,-1,-1)),tuple(range(n,n*2))]
 for i in range(n):j=(i+1)%n;faces.append((i,j,n+j,n+i))
 o=newmesh(name,verts,faces,'stainless');o['drainage']='Pendiente a borde abierto y goterón; descarga sobre franja exterior de jardín.'
drip('AC95 | goterón continuo lateral',[6,13],'x')
drip('AC95 | goterón continuo posterior',[13,22],'z')
# Small waterproof collars around roof penetrations, and clear access labels in metadata.
for o in S.objects:
 if o.name.startswith(('Horno |','Parrilla |','Cocina |')) and 'babeta' in o.name:o['detail_note']='Babeta con collar sellado y solape bajo chapa; verificar montaje en plano de detalle.'
notes=json.loads(S.get('corrections','[]'));notes.append('95 pass1: open fall gutters, hollow connected downpipes, accessible collection chambers and buried garden collector. Stair18/run3.80 preserved; finished rise0.177222m and landing+3.25 coordinated with sill, balcony finishes with1.5%falls. Services and north updated from owner; capacities are not certified.')
S['corrections']=json.dumps(notes,ensure_ascii=False);S['review_iteration']='95 / pass1 construction candidate';S['video_render_requires_explicit_approval']=True
S['site_location']='Virrey del Pino, La Matanza, Buenos Aires';S['north_source_direction']=json.dumps([-1,0,1]);S['services']='Redes disponibles según propietario; puntos exactos por confirmar'
bpy.context.view_layer.update()
os.makedirs(os.path.join(ROOT,'review95'),exist_ok=True)
details={'status':'EN REVISION','model':'Casa_de_Campo_95_Pass1c.blend','source_axes':'X, heightY, depthZ','rainwater':{'front_path':frontpath,'rear_path':rearpath,'collector':collector,'pipe_diameters_proposed_m':[.11,.16],'note':'Captación y continuidad geométrica; dimensionamiento y empalme exterior a verificar'},'stair':{'treads':18,'run':3.8,'start_finish':.06,'landing_finish':3.25,'riser':(3.25-.06)/18,'going':3.8/18,'balcony_drainage':'Borde abierto con goterón continuo a jardín; sin gárgolas obturadas'},'finish_levels':{'studio':3.25,'dwelling':3.25,'landing_at_door':3.25,'landing_low_corner':3.235},'location':'Virrey del Pino, Buenos Aires','north_plan_xy':[-1,1],'services':'Redes disponibles; posiciones de acometida por confirmar'}
json.dump(details,open(os.path.join(ROOT,'review95','construction_details.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
S.frame_set(1);bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_95_Pass1c.blend'),compress=True)
print('CONSTRUCTION95_PASS1_SAVED',len(S.objects),flush=True)
