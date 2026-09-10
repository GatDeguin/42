"""Replace only the two island stool blocks and the garden bench in the loaded scene; optional distinct --save.
All coordinates here use Blender Z-up. No source model or root web files are overwritten.
"""
import bpy,os,sys,json,hashlib,math,numpy as np
from mathutils import Vector
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..'));OUT=os.path.dirname(__file__);S=bpy.context.scene
source=bpy.data.filepath;names=['Taburete isla mono A','Taburete isla mono B','Banco huerta'];support_names=['Apoyo banco huerta','Banco huerta soporte']
assert all(n in S.objects and S.objects[n].type=='MESH' for n in names),'Expected exactly the three original seating blocks'
bpy.context.view_layer.update()
def bounds(o):
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());v=np.array([e.matrix_world@Vector(p) for p in e.bound_box]);return v.min(0),v.max(0)
def geometry_hash(mesh):
 h=hashlib.sha256();v=np.empty(len(mesh.vertices)*3,np.float32);mesh.vertices.foreach_get('co',v);h.update(v.tobytes());l=np.empty(len(mesh.loops),np.int32);mesh.loops.foreach_get('vertex_index',l);h.update(l.tobytes());return h.hexdigest()
def untouched_snapshot():
 result={};meshes={}
 for o in S.objects:
  if o.name in support_names or any(o.name==n or o.name.startswith(n+' | ') for n in names):continue
  if o.type=='MESH' and o.data.as_pointer() not in meshes:meshes[o.data.as_pointer()]=geometry_hash(o.data)
  result[o.name]=dict(type=o.type,matrix=[list(r) for r in o.matrix_world],meshHash=meshes.get(o.data.as_pointer()) if o.type=='MESH' else None,materials=[s.material.name if s.material else None for s in o.material_slots])
 return result
unchanged=untouched_snapshot();rows=[];created=[];removed_supports=[]
for support_name in support_names:
 support=S.objects.get(support_name)
 if support:
  a,b=bounds(support);ba,bb=bounds(S.objects['Banco huerta']);assert np.all(a>=ba-1e-5) and np.all(b<=bb+1e-5),'Extra support is not contained inside the bench block'
  removed_supports.append(dict(name=support_name,bounds=[a.tolist(),b.tolist()]));bpy.data.objects.remove(support,do_unlink=True)
for name in names:
 bench=name=='Banco huerta';FLOOR=.05 if bench else .21;TOP=.50 if bench else .86;SEAT=.04 if bench else .03;LEG=.05 if bench else .035
 original=S.objects[name];a,b=bounds(original);center=(a+b)/2;original_matrix=[list(r) for r in original.matrix_world];footprint=b-a
 assert abs(footprint[0]-(1.25 if bench else .38))<2e-5 and abs(footprint[1]-(.42 if bench else .38))<2e-5,'Unexpected footprint'
 assert abs(a[2]-FLOOR)<2e-5 and abs(b[2]-(.61 if bench else TOP))<2e-5,'Unexpected source support/seat elevation'
 wood=original.material_slots[0].material
 assert wood and wood.get('photographic_wood') and not wood.get('wood_floor'),'Photographic source oak is required'
 uv_name=next(n.uv_map for n in wood.node_tree.nodes if n.type=='UVMAP')
 collection=original.users_collection[0];props=dict(original.items());source_bounds=[a.tolist(),b.tolist()];bpy.data.objects.remove(original,do_unlink=True)
 family=bpy.data.objects.new(name,None);collection.objects.link(family);family.empty_display_type='PLAIN_AXES';family.empty_display_size=.04;family.location=(float(center[0]),float(center[1]),FLOOR)
 for k,v in props.items():family[k]=v
 family['furniture_family']='garden_bench' if bench else 'island_counter_stool';family['height_above_finish_m']=TOP-FLOOR;family['source_footprint_m']=[float(footprint[0]),float(footprint[1])];family['source_position_xyz']=[float(center[0]),(FLOOR+TOP)/2,float(-center[1])];family['source_size_xyz']=[float(footprint[0]),TOP-FLOOR,float(footprint[1])];family['construction']=('40 mm oak slats with 6 mm joints; four 50 mm legs; joined upper frame; four 5 mm elastomer pads' if bench else '30 mm oak seat; four 35 mm legs; joined upper apron; footrest at 200 mm; four 5 mm elastomer pads')
 bpy.context.view_layer.update();parts=[]
 def metric_uv(obj,axis):
  uv=obj.data.uv_layers.new(name=uv_name);uv.active_render=True;seed=hashlib.sha256(obj.name.encode('utf8')).digest();off=[int.from_bytes(seed[:4],'little')/2**32,int.from_bytes(seed[4:8],'little')/2**32]
  for poly in obj.data.polygons:
   other=[i for i in range(3) if i!=axis]
   if abs(poly.normal[axis])>.85:cross,along=other
   else:cross=min(other,key=lambda i:abs(poly.normal[i]));along=axis
   for li in poly.loop_indices:
    p=obj.data.vertices[obj.data.loops[li].vertex_index].co;uv.data[li].uv=(p[cross]/1.830000043+off[0],p[along]/1.830000043+off[1])
  obj['photographic_wood_uv0']=True;obj['wood_longitudinal_axis_local']=axis;obj['wood_uv_offset']=off
 def box(label,pos,size,material,bevel=.001,axis=0):
  x,y,z=[v/2 for v in size];verts=[(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)];faces=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
  mesh=bpy.data.meshes.new(name+' | '+label);mesh.from_pydata(verts,[],faces);mesh.materials.append(material);mesh.update();obj=bpy.data.objects.new(name+' | '+label,mesh);collection.objects.link(obj);obj.parent=family;obj.location=Vector(pos)-family.location
  obj['furniture_family']=name;obj['source_layer']='ground' if bench else 'lower';obj['component']=label
  if material.get('photographic_wood'):metric_uv(obj,axis)
  if bevel:
   mod=obj.modifiers.new('Rounded manufactured edges','BEVEL');mod.width=bevel;mod.segments=4;mod.affect='EDGES';mod.limit_method='ANGLE'
  parts.append(obj);created.append(obj);return obj
 cx,cy=float(center[0]),float(center[1]);w,d=float(footprint[0]),float(footprint[1]);dx=w/2-(.075 if bench else .020)-LEG/2;dy=d/2-.100 if bench else d/2-.020-LEG/2
 if bench:
  gap=.006;slat=(d-3*gap)/4
  for j in range(4):box('tablón asiento '+str(j+1),(cx,cy-d/2+slat/2+j*(slat+gap),TOP-SEAT/2),(w,slat,SEAT),wood,.003,0)
 else:box('asiento 30 mm',(cx,cy,TOP-SEAT/2),(w,d,SEAT),wood,.006,0)
 rubber=bpy.data.materials.get('STOOL95 | elastomer foot')
 if not rubber:
  rubber=bpy.data.materials.new('STOOL95 | elastomer foot');rubber.use_nodes=True;bs=next(n for n in rubber.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(.019,.021,.018,1);bs.inputs['Roughness'].default_value=.88
 for sx in [-1,1]:
  for sy in [-1,1]:
   tag=('izq' if sx<0 else 'der')+' '+('frente' if sy<0 else 'dorso');x=cx+sx*dx;y=cy+sy*dy
   box('pata '+tag,(x,y,(FLOOR+.005+TOP-SEAT)/2),(LEG,LEG,TOP-SEAT-FLOOR-.005),wood,.0012,2)
   box('apoyo elastomérico '+tag,(x,y,FLOOR+.0025),(LEG,LEG,.005),rubber,.0007,0)
 rail_height=.07 if bench else .06;rail_thickness=.025 if bench else .018
 for side in [-1,1]:
  box('faldón unión X '+str(side),(cx,cy+side*dy,TOP-SEAT-rail_height/2),(2*dx-LEG,rail_thickness,rail_height),wood,.001,0)
  box('faldón unión Y '+str(side),(cx+side*dx,cy,TOP-SEAT-rail_height/2),(rail_thickness,2*dy-LEG,rail_height),wood,.001,1)
  if not bench:box('reposapiés X '+str(side),(cx,cy+side*dy,FLOOR+.20-.0125),(2*dx-LEG,LEG,.025),wood,.0015,0)
  if not bench:box('travesaño Y '+str(side),(cx+side*dx,cy,FLOOR+.20-.0125),(LEG,2*dy-LEG,.025),wood,.0015,1)
 if bench:box('travesaño central bajo tablones',(cx,cy,TOP-SEAT-.0175),(.040,2*dy+LEG,.035),wood,.001,1)
 foundation=[]
 if bench:
  concrete=next(m for m in bpy.data.materials if m.get('source_material_key')=='concrete')
  granular=bpy.data.materials.new('STOOL95 | proposed granular bedding');granular.use_nodes=True;gb=next(n for n in granular.node_tree.nodes if n.type=='BSDF_PRINCIPLED');gb.inputs['Base Color'].default_value=(.12,.095,.06,1);gb.inputs['Roughness'].default_value=1
  family['support_design_status']='P';family['support_design_note']='Proposed four 200x200x40 mm concrete pads (+.010 to +.050), on 50 mm granular bedding (-.040 to +.010); seat +.500, 450 mm over pads and 460 mm above existing +.040 grass. No terrain mesh altered.'
  for sx in [-1,1]:
   for sy in [-1,1]:
    x=cx+sx*dx;y=cy+sy*dy
    for label,z,h,mat in [('loseta hormigón P',.030,.040,concrete),('lecho granular P',-.015,.050,granular)]:
     item=box(label+' '+str(sx)+' '+str(sy),(x,y,z),(.200,.200,h),mat,.002 if h==.040 else 0,0);item['classification']='P';item['foundation_P']=True;item['proposal']='Local bench foundation; no global terrain modifications';foundation.append(item)
  assert len(foundation)==8
 bpy.context.view_layer.update();bb=[bounds(o) for o in parts if not o.get('foundation_P')];lo=np.min([q[0] for q in bb],0);hi=np.max([q[1] for q in bb],0)
 assert np.max(np.abs(lo[:2]-a[:2]))<2e-6 and np.max(np.abs(hi[:2]-b[:2]))<2e-6,'Footprint changed'
 assert abs(lo[2]-FLOOR)<2e-6 and abs(hi[2]-TOP)<2e-6,'Support or seat height changed'
 for o in parts:
  if o.get('foundation_P'):
   fa,fb=bounds(o);assert np.all(fa[:2]>=a[:2]-2e-6) and np.all(fb[:2]<=b[:2]+2e-6),'Foundation projects outside retained footprint'
  if 'pata ' in o.name:assert abs(bounds(o)[1][2]-(TOP-SEAT))<2e-6
  if 'apoyo elastomérico' in o.name:assert abs(bounds(o)[0][2]-FLOOR)<2e-6
  if not bench and ('reposapiés' in o.name or 'travesaño' in o.name):assert abs(bounds(o)[1][2]-(FLOOR+.20))<2e-6
 rows.append(dict(name=name,sourceBounds=source_bounds,newBounds=[lo.tolist(),hi.tolist()],centerXY=center[:2].tolist(),footprint=[w,d],parts=[o.name for o in parts],seatThickness=SEAT,seatAboveFloor=TOP-FLOOR,legSection=[LEG,LEG],footrestAboveFloor=None if bench else .20,footPads=4,material=wood.name,uv0=uv_name,sourceMatrix=original_matrix,proposedFoundation=[o.name for o in foundation],foundationStatus='P' if bench else None))
bpy.context.view_layer.update();assert untouched_snapshot()==unchanged,'An object outside the two stool families changed'
report=dict(source=source,sourceSHA256=hashlib.sha256(open(source,'rb').read()).hexdigest(),families=rows,removedDuplicateSupports=removed_supports,newMeshes=len(created),untouchedObjects=len(unchanged),untouchedGeometryTransformsMaterials=True)
if '--save' in sys.argv:
 target=os.path.abspath(sys.argv[sys.argv.index('--save')+1]);assert target!=os.path.abspath(source),'Never overwrite input';bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=target,compress=True);report['output']=target;report['outputSHA256']=hashlib.sha256(open(target,'rb').read()).hexdigest()
json.dump(report,open(os.path.join(OUT,'application-report.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2);print('THREE_SEATS_REPLACED',len(rows),len(created),'OTHER_OBJECTS_UNCHANGED',len(unchanged),flush=True)
