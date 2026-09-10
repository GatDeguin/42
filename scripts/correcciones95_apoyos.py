"""Resolve independently audited bearing gaps, balcony anchorage and inlet grille."""
import bpy,os,math,json,ast,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
def cv(p):return Vector((p[0],-p[2],p[1]))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_materialidad.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['box','cyl']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<fast>','exec'))
def bounds(o):
 a=np.array([o.matrix_world@Vector(v) for v in o.bound_box]);return a.min(0),a.max(0)
def cut(o,c):
 bpy.context.view_layer.objects.active=o;m=o.modifiers.new('Reserva de montaje','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=c;bpy.ops.object.modifier_apply(modifier=m.name)
def geom(o):
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();v=[e.matrix_world@p.co for p in m.vertices];f=[list(p.vertices) for p in m.polygons];e.to_mesh_clear();return BVHTree.FromPolygons(v,f)
# Wall brackets: actual extension to masonry and a continuous fixing shank.
for o in list(S.objects):
 if o.name.startswith('PL95 | ménsula frontal'):
  o.data=o.data.copy();a,b=bounds(o);inv=o.matrix_world.inverted()
  for v in o.data.vertices:
   p=o.matrix_world@v.co
   if p.x>(a[0]+b[0])/2:p.x+=.060
   v.co=inv@p
  h=(a[2]+b[2])/2;z=-(a[1]+b[1])/2
  cyl('FIX95 | fijación ménsula a mampostería',[13.965,h,z],[14.09,h,z],.005,'stainless')
# Cradle joints bear through explicit4mm pads, with return legs tied into the façade.
for o in list(S.objects):
 if 'canaleta' in o.name and ' | soporte' in o.name:
  a,b=bounds(o);x=(a[0]+b[0])/2;z=-(a[1]+b[1])/2;h=b[2]
  newx=max(14.08,min(21.90,x));o.location.x+=newx-x;x=newx
  box('FIX95 | calzo soporte canaleta 4mm',[x,h+.002,z],[.024,.004,.16],'blackMetal',bev=0)
  front='frontal' in o.name;zz=.004 if front else 11.996;top=6.982 if front else 6.382
  box('FIX95 | retorno soporte canaleta',[x,(h+top)/2,zz],[.024,top-h,.006],'blackMetal',bev=.0005)
  zz2=.12 if front else 11.88
  cyl('FIX95 | tornillo soporte canaleta',[x,top-.014,zz],[x,top-.014,zz2],.004,'stainless')
# Grate opening follows the inclined pipe footprint, with a border that supports the cut bars.
c=box('Temporal paso tapa cámara',[13.62,.06,.575],[.142,.16,.152],col='REFERENCE',bev=0);bpy.context.view_layer.update()
for o in list(S.objects):
 if o.name.startswith('PL95 | cámara frontal registrable | rejilla'):cut(o,c)
bpy.data.objects.remove(c,do_unlink=True)
for x in [13.546,13.694]:box('FIX95 | borde reserva rejilla',[x,.049,.575],[.006,.012,.164],'stainless',bev=.001)
for z in [.496,.654]:box('FIX95 | borde reserva rejilla',[13.62,.049,z],[.154,.012,.006],'stainless',bev=.001)
# The old external bolt heads cannot be given a fictitious embedment. Replace their whole fixing.
for o in list(S.objects):
 if o.name.startswith(('Baranda lateral poste','Baranda posterior poste')) and any(t in o.name for t in [' | placa base',' | anclaje']):bpy.data.objects.remove(o,do_unlink=True)
duplicate=bpy.data.objects.get('Baranda posterior poste 0')
if duplicate:bpy.data.objects.remove(duplicate,do_unlink=True)
floors=[geom(o) for o in S.objects if o.name.startswith('AC95 | acabado ') and o.type=='MESH']
def floorh(x,z):
 hits=[b.ray_cast(cv([x,3.31,z]),Vector((0,0,-1)),.2)[0] for b in floors];hs=[p.z for p in hits if p]
 return max(hs) if hs else 3.235
def grout(name,x0,x1,z0,z1,top,bottom):
 vs=[]
 for x,z in [(x0,z0),(x1,z0),(x1,z1),(x0,z1)]:vs.append(cv([x,bottom,z]))
 vs+=[cv([x,top,z]) for x,z in [(x0,z0),(x1,z0),(x1,z1),(x0,z1)]]
 fs=[(0,1,2),(0,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(M['concrete']);me.update();ob=bpy.data.objects.new(name,me);COL['UPPER_FLOOR'].objects.link(ob);return ob
records=[]
posts=[o for o in S.objects if o.type=='MESH' and o.name.startswith(('Baranda lateral poste','Baranda posterior poste')) and '|' not in o.name]
for o in posts:
 a,b=bounds(o);x=(a[0]+b[0])/2;z=-(a[1]+b[1])/2
 side=o.name.startswith('Baranda lateral');substrate=3.20 if side and z<6 else 3.21
 if side:
  x0,x1=13.0,13.21
  if z<5.1:z0,z1=4.978,5.21;zs=[5.09,5.17]
  elif z>12.8:z0,z1=12.79,13.0;zs=[12.83,12.91]
  else:z0,z1=z-.055,z+.055;zs=[z-.033,z+.033]
  xs=[13.09,13.17]
 else:
  z0,z1=12.79,13.0;zs=[12.83,12.91]
  if x>21.8:x0,x1=21.79,22.0;xs=[21.83,21.91]
  else:x0,x1=x-.055,x+.055;xs=[x-.033,x+.033]
 plate=box('FIX95 | placa interior '+o.name,[(x0+x1)/2,3.260,(z0+z1)/2],[x1-x0,.012,z1-z0],'blackMetal','UPPER_FLOOR',.001)
 plate['design_status']='P: conexión geométrica propuesta; verificar cargas, armado y anclaje. No es cálculo resistente.'
 # Remove finish locally: grout bears directly on the structural slab, not on paving.
 cutter=box('Temporal cajeado acabado bajo anclaje',[(x0+x1)/2,3.26,(max(z0,5.0)+z1)/2],[x1-x0,.12,z1-max(z0,5.0)],col='REFERENCE',bev=0);bpy.context.view_layer.update()
 for floor in [v for v in S.objects if v.name.startswith('AC95 | acabado ') and v.type=='MESH']:
  fa,fb=bounds(floor);ca,cb=bounds(cutter)
  if np.all(np.minimum(fb,cb)-np.maximum(fa,ca)>.0001):cut(floor,cutter)
 bpy.data.objects.remove(cutter,do_unlink=True)
 grout('FIX95 | grout hasta sustrato '+o.name,x0+.002,x1-.002,max(z0+.002,5.001),z1-.002,3.254,substrate)
 # Post bears on plate, preserving its top and all railing heights.
 inv=o.matrix_world.inverted();o.data=o.data.copy()
 for v in o.data.vertices:
  w=o.matrix_world@v.co
  if w.z<3.28:w.z=3.266
  v.co=inv@w
 substrate=3.20 if side and z<6 else 3.21
 for xx in xs:
  for zz in zs:
   cyl('FIX95 | vástago M10 continuo',[xx,substrate-.10,zz],[xx,3.284,zz],.005,'stainless','UPPER_FLOOR')
   cyl('FIX95 | arandela M10',[xx,3.266,zz],[xx,3.269,zz],.011,'stainless','UPPER_FLOOR')
   cyl('FIX95 | tuerca M10',[xx,3.269,zz],[xx,3.278,zz],.0085,'stainless','UPPER_FLOOR')
 records.append({'post':o.name,'plate_source_box':[x0,x1,z0,z1,3.254,3.266],'anchor_x':xs,'anchor_z':zs,'embedment_proposed_m':.10,'substrate_top':substrate,'anchor_bottom':substrate-.10,'status':'P / geometry only; engineer must validate load, edge distance, slab reinforcement and selected anchor'})
# Source location and geometry checks do not imply certified anchorage capacity.
records=json.loads(json.dumps(records,default=float))
S['anchors95']=json.dumps(records,ensure_ascii=False);S['review_iteration']='95 / pass3b independent bearing corrections';S['video_render_requires_explicit_approval']=True
bpy.context.view_layer.update();S.camera=bpy.data.objects['CAM | Presentación verticales corregidas']
os.makedirs(os.path.join(ROOT,'review95'),exist_ok=True)
json.dump({'status':'P/PROPOSED','fixes':['Wall bracket terminates inside masonry with shank','4mm gutter cradle pads and façade return fixings','Grille reserve follows inclined pipe','Balcony plates anchor inside concrete and bear through fitted grout'],'balcony_connections':records},open(os.path.join(ROOT,'review95','bearing_details.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_95_Pass3b.blend'),compress=True)
print('PASS3B_SAVED_NO_VIDEO',len(records),flush=True)
