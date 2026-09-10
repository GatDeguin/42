"""Owner layout correction: coherent furnishings and true finished-floor heights.
Reads frozen Pass3d. Architectural openings/geometry are unchanged by this pass.
"""
import bpy,os,math,json,ast,numpy as np
from mathutils import Vector,Matrix
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
for m in bpy.data.materials:
 if m.name.startswith('MAT95 | '):M[m.name.split(' | ',1)[1]]=m
def cv(p):return Vector((p[0],-p[2],p[1]))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_materialidad.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['box','cyl','curve','mesh']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<fast>','exec'))
def bounds(o):
 a=np.array([o.matrix_world@Vector(v) for v in o.bound_box]);return a.min(0),a.max(0)
def deform(o,fn):
 if o.type!='MESH':return
 o.data=o.data.copy();inv=o.matrix_world.inverted()
 for v in o.data.vertices:v.co=inv@fn(o.matrix_world@v.co)
 o.data.update()
def move_to(o,x,h,z):
 a,b=bounds(o);o.location+=cv([x,h,z])-(Vector(a)+Vector(b))/2
def map_h(o,a,b,c,d):
 deform(o,lambda p:Vector((p.x,p.y,c+(p.z-a)*(d-c)/(b-a))))
def erase(prefixes):
 for o in list(S.objects):
  if o.name.startswith(tuple(prefixes)):bpy.data.objects.remove(o,do_unlink=True)
def affine(o,old,new,angle=0):
 o.matrix_world=Matrix.Translation(cv(new))@Matrix.Rotation(-angle,4,'Z')@Matrix.Translation(-cv(old))@o.matrix_world
records=[]
# QUINCHO: service bar along the existing eastern cooking line, 1.13m work aisle.
barprefix=('Mueble parrilla bajo ','Mesada apoyo quincho','Alzada quincho','Bacha quincho','Grifería quincho')
for o in [o for o in S.objects if o.name.startswith(barprefix)]:
 affine(o,[19.46,0,7.54],[18.65,.02,8.69],math.pi/2)
 o['layout_revision']='Owner: free-standing service bar parallel to the grill'
# The high source splashback was a detached wall; replace with 100mm supported splash.
alzada=bpy.data.objects.get('Alzada quincho')
if alzada:
 a,b=bounds(alzada);map_h(alzada,a[2],b[2],1.08,1.18)
for o in [o for o in S.objects if o.name.startswith('Mueble parrilla bajo ')]:
 a,b=bounds(o);map_h(o,a[2],b[2],.28,1.04)
box('MOB95 | zócalo barra quincho',[18.65,.23,8.69],[.44,.10,2.18],'blackMetal','QUINCHO',.002)
# Wall-mounted shelf is returned to masonry over the fixed washing station.
o=bpy.data.objects.get('Estante quincho')
if o:
 affine(o,[20.70,1.82,7.18],[21.70,1.82,8.15],math.pi/2)
 for zz in [7.70,8.60]:
  box('MOB95 | ménsula estante lavado',[21.71,1.765,zz],[.21,.025,.025],'blackMetal','QUINCHO')
  box('MOB95 | anclaje estante lavado',[21.802,1.79,zz],[.02,.13,.04],'blackMetal','QUINCHO')
# Dining group by garden: route to lawn runs along west side, outside chair use.
erase(['Mesa quincho ','Silla quincho ','Mesa baja quincho'])
tx,tz=16.45,10.30;floor=.18;tabletop=.93
# Five separate 40mm timber boards with 2mm joints.
for k in range(5):
 box('Mesa quincho tapa tabla %d'%k,[tx,tabletop-.02,tz-.46+(k+.5)*.184],[2.15,.04,.182],'wood','QUINCHO',.004)
for xx in [tx-.89,tx+.89]:
 for zz in [tz-.34,tz+.34]:
  box('Mesa quincho pata',[xx,(floor+.89)/2,zz],[.055,.89-floor,.055],'blackMetal','QUINCHO',.002)
  box('MOB95 | apoyo pata mesa',[xx,floor+.0025,zz],[.056,.005,.056],'rubber95','QUINCHO',.001)
for zz in [tz-.34,tz+.34]:box('MOB95 | larguero mesa',[tx,.85,zz],[1.83,.075,.032],'blackMetal','QUINCHO',.001)
for xx in [tx-.89,tx+.89]:box('MOB95 | travesaño mesa',[xx,.85,tz],[.032,.075,.68],'blackMetal','QUINCHO',.001)
def chair(i,x,z,back):
 # back=-1: chair facing +Z. back=+1: facing -Z.
 pref='Silla quincho %d '%i;seat=floor+.46
 for k in range(3):box(pref+'asiento tabla %d'%k,[x,seat-.014,z-.225+(k+.5)*.15],[.46,.028,.148],'wood','QUINCHO',.004)
 for xx in [x-.181,x+.181]:
  for zz in [z-.18,z+.18]:
   isback=(zz-z)*back>0
   top=floor+.91 if isback else seat-.028
   topz=zz+back*.045 if isback else zz
   ob=cyl(pref+'estructura',[xx,floor+.004,zz],[xx,top,topz],.016,'blackMetal','QUINCHO')
   box(pref+'regatón',[xx,floor+.002,zz],[.035,.004,.035],'rubber95','QUINCHO',.001)
 for k in range(3):
  h=floor+.59+k*.115;zz=z+back*(.193+(h-floor-.46)*.10)
  slat=box(pref+'respaldo listón %d'%k,[x,h,zz],[.405,.097,.024],'wood','QUINCHO',.004)
  slat.rotation_euler[0]=back*math.radians(6)
 for zz in [z-.18,z+.18]:box(pref+'travesaño asiento',[x,seat-.037,zz],[.38,.024,.024],'blackMetal','QUINCHO',.002)
for i,(x,z,back) in enumerate([(15.75,9.54,-1),(17.15,9.54,-1),(15.75,11.06,1),(17.15,11.06,1)],1):chair(i,x,z,back)
records.append({'group':'Quincho','finished_floor':.18,'table_top':.93,'table_height':.75,'seat_top':.64,'seat_height':.46,'table_center_source':[tx,tz],'bar_bounds_xz':[18.34,18.96,7.4,9.98],'work_aisle_min':1.13,'garden_west_path_min':1.19,'rear_chair_pullback_m':.35,'rear_chair_pulled_edge_max_z':11.67,'rear_floor_edge_z':12})
# Move the real luminaire and its light together over the dining group.
for o in S.objects:
 if 'quincho' in o.name.lower() and (o.type=='LIGHT' or o.name=='Luz lineal quincho'):
  o.location.x+=tx-18.1;o.location.y-=tz-8.85
# BEDROOM: source mattress already ran along Z, but headboard and nightstands ran across it.
# Align all components to head at interior wall Z6.10, feet toward Z8.15, window on right in bed.
for o in [o for o in S.objects if o.name.startswith('Cama dormitorio ')]:
 o.location.y+=.325
# Fixed drape now stays within 35mm of the frame so it does not consume the side passage.
o=bpy.data.objects['Cama dormitorio manta']
def drape_limit(p):
 p.x=max(14.895,p.x);p.y=max(-8.18,p.y);return p
deform(o,drape_limit)
o=bpy.data.objects['Cabezal dormitorio']
affine(o,[14.94,4.02,7.48],[15.82,3.975,6.135],math.pi/2)
a,b=bounds(o)
# 70mm headboard fixed to the wall; source 140mm thickness is excessive at this junction.
deform(o,lambda p:Vector((p.x,-(6.10+((-p.y)-(-b[1]))*.07/(b[1]-a[1])),p.z)))
# Ensure exact wall-facing thickness independent of transformed bound ordering.
a,b=bounds(o);center=(a[1]+b[1])/2
deform(o,lambda p:Vector((p.x,-6.135+(p.y-center)*.07/(b[1]-a[1]),p.z)))
# Cabinet and bench were incompatible with the usable bedside and door circulation.
for o in list(S.objects):
 if o.name.startswith(('Placard dormitorio','Banqueta pie cama')):
  o.hide_render=True;o.hide_set(True);o['layout_revision']='Removed from active arrangement: storage in existing walk-through wardrobe; keep clear bedroom circulation'
# Base on four short feet, rather than hovering above the finished floor.
o=bpy.data.objects['Cama dormitorio base'];a,b=bounds(o);map_h(o,a[2],b[2],3.33,3.65)
for x in [15.10,16.54]:
 for z in [6.37,7.97]:box('MOB95 | pata cama',[x,3.29,z],[.065,.08,.065],'blackMetal','INTERIORS',.004)
for side,x in [('izq',17.09),('der',14.55)]:
 o=bpy.data.objects['Mesa de luz suite '+side];move_to(o,x,3.64,6.49)
 a,b=bounds(o);map_h(o,a[2],b[2],3.50,3.78)
 for xx in [x-.15,x+.15]:
  for zz in [6.34,6.64]:box('MOB95 | pata mesa de luz',[xx,3.375,zz],[.026,.25,.026],'blackMetal','INTERIORS',.002)
 lamp=bpy.data.objects.get('Lámpara mesa suite '+side)
 if lamp:bpy.data.objects.remove(lamp,do_unlink=True)
 cyl('Lámpara mesa suite '+side+' base',[x,3.78,6.49],[x,3.795,6.49],.070,'blackMetal','INTERIORS')
 cyl('Lámpara mesa suite '+side+' pie',[x,3.795,6.49],[x,3.98,6.49],.009,'stainless','INTERIORS')
 # Hollow shade has an actual opening; emitter and bulb are inside.
 N=48;vs=[];fs=[]
 for h,r in [(3.94,.105),(4.12,.077),(4.12,.074),(3.94,.102)]:
  vs.extend([cv([x+r*math.cos(k*math.tau/N),h,6.49+r*math.sin(k*math.tau/N)]) for k in range(N)])
 for j in range(4):
  jj=(j+1)%4
  for k in range(N):q=(k+1)%N;fs.append((j*N+k,j*N+q,jj*N+q,jj*N+k))
 shade=mesh('Lámpara mesa suite '+side+' pantalla',vs,fs,'linen95','INTERIORS')
 for f in shade.data.polygons:f.use_smooth=True
 cyl('Lámpara mesa suite '+side+' bombilla',[x,3.98,6.49],[x,4.035,6.49],.021,'warmLight','INTERIORS')
lights=sorted([o for o in S.objects if o.type=='LIGHT' and o.name.startswith('Suite | lámpara de lectura')],key=lambda o:o.location.y)
for ob,x in zip(lights,[14.55,17.09]):ob.location=cv([x,4.02,6.49]);ob.data.energy=10;ob.data.shadow_soft_size=.04
records.append({'group':'Dormitorio','finished_floor':3.25,'bed_source_box':[14.93,16.71,6.165,8.145],'headboard_source_box':[14.81,16.83,6.10,6.17],'window_wall_x':14.2,'right_in_bed_direction':'-X, window wall','side_clearance_window_m':.615,'side_clearance_wardrobe_side_m':.84,'foot_clearance_frame_m':.755,'foot_clearance_textile_m':.72,'storage':'Existing walk-through wardrobe; bedroom duplicate cabinet and bench removed from active furnishing'})
# Sofas: piecewise section adjustment keeps seat450mm, back860mm and feet on true floor.
for prefix,floor,sourcebase in [('Sofá cama mono',.21,.17),('Sofá estudio',3.25,3.25),('Sofá vivienda',3.25,3.25)]:
 objects=[o for o in S.objects if o.name.startswith(prefix)]
 def f(p):
  h=p.z-sourcebase;p.z=floor+float(np.interp(h,[0,.19,.655,1.125],[0,.11,.45,.86]));return p
 for o in objects:deform(o,f)
 records.append({'group':prefix,'finished_floor':floor,'seat_height_m':.45,'back_height_m':.86,'correction':'Section reshaped from actual finished floor; same plan footprint'})
# Dining and studio chairs: true470mm sitting height and grounded supports.
for prefix in ['Silla comedor ','Silla estudio ']:
 for o in [v for v in S.objects if v.name.startswith(prefix)]:
  map_h(o,3.25,3.765,3.25,3.72)
# Table dining surface750mm with45mm top, grounded legs. Contents follow the top.
for o in [v for v in S.objects if v.name.startswith('Mesa comedor ')]:
 a,b=bounds(o)
 if 'tapa' in o.name:map_h(o,a[2],b[2],3.955,4.0)
 elif 'pata' in o.name:map_h(o,a[2],b[2],3.25,3.955)
# No timeline/video render. All owner-source building geometry remains intact in this file.
S['review_iteration']='95 / R4A owner furnishing coordination'
S['furniture_coordination95']=json.dumps(records,ensure_ascii=False)
S['video_render_requires_explicit_approval']=True
bpy.context.view_layer.update();S.frame_set(1)
json.dump({'model':'Casa_de_Campo_95_R4A.blend','owner_corrections':True,'furniture':records},open(os.path.join(ROOT,'review95','furniture_r4a.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_95_R4A.blend'),compress=True)
print('R4A_FURNISHING_SAVED',flush=True)
