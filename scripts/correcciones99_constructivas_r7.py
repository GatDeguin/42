"""R7A: confine optical pool-water volume to measured basin solids.
Run Blender CPU: blender -b output/Casa_de_Campo_95_R6K.blend --python scripts/correcciones99_constructivas_r7.py
The source file is immutable. Only Agua de pileta changes. No rendering or hydraulics sizing.
"""
import bpy,bmesh,hashlib,json,sys
from pathlib import Path
from array import array
from mathutils import Matrix,Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parent.parent
EXPECTED='a3663a5081dac391303f25b8e9994b1a412a008e971642af29fc2cbee849aa90'
SOURCE=Path(bpy.data.filepath).resolve();source_sha=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
assert source_sha==EXPECTED,'Requires the immutable R6K input'
OUT=ROOT/'output/Casa_de_Campo_99_R7A.blend';REPORT=ROOT/'review99/constructivas_r7a.json';REPORT.parent.mkdir(exist_ok=True)
S=bpy.context.scene;original_frame=S.frame_current;S.frame_set(1);bpy.context.view_layer.update()

def eval_mesh(o):
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=bpy.data.meshes.new_from_object(e,preserve_all_data_layers=True,depsgraph=bpy.context.evaluated_depsgraph_get());m.transform(e.matrix_world);return m

def bounds(o):
 m=eval_mesh(o);vs=[v.co for v in m.vertices];b={k:[min(p[i]*sgn for p in vs),max(p[i]*sgn for p in vs)] for k,i,sgn in [('x',0,1),('y',2,1),('z',1,-1)]};bpy.data.meshes.remove(m);return b

def signature(o):
 h=hashlib.sha256(repr((o.type,tuple(v for r in o.matrix_world for v in r),o.hide_render,tuple(c.name for c in o.users_collection))).encode())
 if o.type=='MESH':
  for seq,prop,typ,width in [(o.data.vertices,'co','f',3),(o.data.loops,'vertex_index','i',1)]:
   a=array(typ,[0])*(len(seq)*width);seq.foreach_get(prop,a);h.update(a.tobytes())
  for uv in o.data.uv_layers:
   a=array('f',[0])*(len(uv.data)*2);uv.data.foreach_get('uv',a);h.update(a.tobytes())
  h.update(repr(tuple(m.name if m else None for m in o.data.materials)).encode())
 return h.hexdigest()

def mesh_metrics(o):
 m=eval_mesh(o);bm=bmesh.new();bm.from_mesh(m);result={'vertices':len(bm.verts),'faces':len(bm.faces),'edges':len(bm.edges),'volume_m3':bm.calc_volume(signed=True),'non_manifold_edges':sum(not e.is_manifold for e in bm.edges),'loose_vertices':sum(not v.link_edges for v in bm.verts)}
 unseen=set(bm.verts);count=0;component_volumes=[]
 while unseen:
  stack=[unseen.pop()];count+=1;component=set(stack)
  while stack:
   v=stack.pop()
   for e in v.link_edges:
    n=e.other_vert(v)
    if n in unseen:unseen.remove(n);stack.append(n);component.add(n)
   faces={f for v in component for f in v.link_faces};cv=0.0
  for f in faces:
   v=[p.co for p in f.verts]
   for j in range(1,len(v)-1):cv+=v[0].dot(v[j].cross(v[j+1]))/6
  component_volumes.append(cv)
 result['connected_components']=count;result['component_signed_volumes_m3']=component_volumes;bm.free();bpy.data.meshes.remove(m);return result

def temporary(o,seal_joint=False):
 m=eval_mesh(o)
 if seal_joint and o.name=='Playa húmeda pileta':
  # The shelf ends 2 micrometres before the east wall: a numerical optical slit.
  # Extend only the hidden cutter end 1mm into that existing wall, not the shelf.
  x0=min(v.co.x for v in m.vertices);x1=max(v.co.x for v in m.vertices)
  for v in m.vertices:
   if v.co.x>x1-.003:v.co.x+=.001001
  m.update()
 c=bpy.data.objects.new('TEMP_R7_'+o.name,m);S.collection.objects.link(c);return c

def remove(o):
 m=o.data;bpy.data.objects.remove(o,do_unlink=True)
 if m.users==0:bpy.data.meshes.remove(m)

def boolean(target,solid,operation='DIFFERENCE'):
 cutter=temporary(solid,operation=='DIFFERENCE');bpy.context.view_layer.objects.active=target;target.select_set(True);md=target.modifiers.new('R7 confine '+solid.name,'BOOLEAN');md.operation=operation;md.solver='EXACT';md.object=cutter;bpy.ops.object.modifier_apply(modifier=md.name);remove(cutter);target.select_set(False)

def intersection(a,b):
 probe=temporary(a);boolean(probe,b,'INTERSECT');m=mesh_metrics(probe);remove(probe);return abs(m['volume_m3'])

def tree(o):
 m=eval_mesh(o);t=BVHTree.FromPolygons([v.co for v in m.vertices],[list(p.vertices) for p in m.polygons],epsilon=1e-8);bpy.data.meshes.remove(m);return t

def pair_contacts(water,solids):
 wt=tree(water);st={o.name:tree(o) for o in solids};rows=[]
 # First lower interface of water must touch the first submerged solid surface.
 points=[(x,z) for x in [13.13,13.65,14.2,15.5,17,18.22,18.46,19.2,19.87] for z in [15.13,15.7,16.5,16.9,17.2,17.6,17.86]]
 points.extend([(13.65,17.65),(13.65,17.23),(13.65,16.91),(18.22,16.5),(19.2,16.5)])
 for x,z in points:
  origin=Vector((x,-z,-.04));direction=Vector((0,0,-1));w=wt.ray_cast(origin,direction,3);hits=[(t.ray_cast(origin,direction,3),n) for n,t in st.items()];hits=[(h,n) for h,n in hits if h[0] is not None]
  expected=min(hits,key=lambda row:row[0][3]) if hits else None
  gap=None if w[0] is None or expected is None else abs(w[3]-expected[0][3]);rows.append({'kind':'vertical_first_interface','source_x':x,'source_z':z,'solid':expected[1] if expected else None,'gap_m':gap,'pass':gap is not None and gap<5e-6})
 for origin,direction in [((13.13,-16.5,-.5),(-1,0,0)),((19.87,-16.5,-.05),(1,0,0)),((16.5,-15.13,-.5),(0,1,0)),((16.5,-17.87,-.5),(0,-1,0))]:
  origin=Vector(origin);direction=Vector(direction);w=wt.ray_cast(origin,direction,.1);hits=[(t.ray_cast(origin,direction,.1),n) for n,t in st.items()];hits=[(h,n) for h,n in hits if h[0] is not None];ex=min(hits,key=lambda r:r[0][3]) if hits else None;gap=None if w[0] is None or ex is None else abs(w[3]-ex[0][3]);rows.append({'kind':'wall_contact','solid':ex[1] if ex else None,'gap_m':gap,'pass':gap is not None and gap<5e-6})
 return rows

water=bpy.data.objects['Agua de pileta'];before_sig={o.name:signature(o) for o in S.objects if o!=water};before_names=set(o.name for o in S.objects)
solids=[o for o in S.objects if o.type=='MESH' and o.name.startswith(('Fondo de pileta','Borde pileta','Escalón pileta','Playa húmeda','Nariz playa húmeda','Junta borde pileta','Banda húmeda'))]
assert len(solids)==14,len(solids)
report={'input':str(SOURCE),'input_sha256':source_sha,'scope':'Only evaluated water mesh clipped against 14 existing pool solids. Architecture, finishes, materials, rigs and surrounding objects preserved. No hydraulic calculation or certified system implied.','cause':'Uniform Solidify1.474 m created water through floor, four walls, steps and shelf.','before_water_bounds_source_m':bounds(water),'before_water_mesh':mesh_metrics(water),'before_intersections':[]}
for o in solids:
 v=intersection(water,o);report['before_intersections'].append({'solid':o.name,'volume_m3':v});print('BASELINE',o.name,v,flush=True)
assert sum(r['volume_m3'] for r in report['before_intersections'])>2.0
# Bake evaluated water once, keeping the original optical material and surface mesh.
original_water_matrix=water.matrix_world.copy();oldmesh=water.data;newmesh=eval_mesh(water);water.modifiers.clear();water.data=newmesh;water.matrix_world=Matrix.Identity(4)
if oldmesh.users==0:bpy.data.meshes.remove(oldmesh)
for o in solids:
 if next(r['volume_m3'] for r in report['before_intersections'] if r['solid']==o.name)>1e-10:boolean(water,o)
# Exact Boolean keeps nested cavity normals facing out of the fluid. Recalculating
# each disconnected cavity independently would incorrectly fill its optical volume.
# Restore original local coordinates so object-driven optical texture mapping remains.
water.data.transform(original_water_matrix.inverted());water.matrix_world=original_water_matrix;water.data.update();bpy.context.view_layer.update()
water['design_water_crest_y']=-.030;water['freeboard_to_basin_cap_m']=.100;water['r7_confinement']='Evaluated mesh follows existing floor/walls/steps/shelf with exact Boolean contact; hydraulic project remains pending.'
report['after_water_bounds_source_m']=bounds(water);report['after_water_mesh']=mesh_metrics(water);report['after_intersections']=[]
for o in solids:
 v=intersection(water,o);report['after_intersections'].append({'solid':o.name,'volume_m3':v,'pass':v<1e-8});print('FINAL',o.name,v,flush=True)
report['contacts']=pair_contacts(water,solids)
report['unchanged_objects']=all(signature(bpy.data.objects[n])==sig for n,sig in before_sig.items());report['object_names_preserved']=before_names==set(o.name for o in S.objects)
report['rig_count']=len([o for o in S.objects if o.name.startswith('DOOR |')]);report['new_materials']=[];report['changed_objects']=[water.name];report['hidden_joint_closure']={'location':'East end of wet shelf at X19.88 against east basin wall','original_gap_m':0.000001907,'water_only_cutter_extension_into_wall_m':0.001001,'finish_geometry_changed':False}
report['preserved_datums']={'water_crest_m':report['after_water_bounds_source_m']['y'][1],'wet_shelf_top_m':bounds(bpy.data.objects['Playa húmeda pileta'])['y'][1],'basin_cap_m':bounds(bpy.data.objects['Borde pileta norte'])['y'][1],'nominal_basin_width_m':bounds(bpy.data.objects['Fondo de pileta'])['x'][1]-bounds(bpy.data.objects['Fondo de pileta'])['x'][0],'nominal_basin_depth_m':bounds(bpy.data.objects['Fondo de pileta'])['z'][1]-bounds(bpy.data.objects['Fondo de pileta'])['z'][0]}
report['limitations']=['Existing support/finish assemblies are unaltered; no structural proof is claimed.','Water boundary coincides with physical surfaces without an artificial optical air gap.','Filtration, operating level, circulation, drainage and safety require a hydraulic project.','Unmodeled wet-wall finishes and D08 ventilation coordination remain separate tasks.']
metrics=report['after_water_mesh'];report['pass']=all(r['pass'] for r in report['after_intersections']) and all(r['pass'] for r in report['contacts']) and report['unchanged_objects'] and report['object_names_preserved'] and metrics['non_manifold_edges']==0 and sum(v>0 for v in metrics['component_signed_volumes_m3'])==1 and metrics['volume_m3']>0 and report['rig_count']==13
assert abs(report['preserved_datums']['water_crest_m']+.030)<1e-6
assert abs(report['preserved_datums']['wet_shelf_top_m']+.080)<1e-6
assert abs(report['preserved_datums']['basin_cap_m']-.070)<1e-6
assert abs(report['preserved_datums']['nominal_basin_width_m']-7)<1e-6 and abs(report['preserved_datums']['nominal_basin_depth_m']-3)<1e-6
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf8')
assert report['pass'],'R7A proof failed: inspect report, output not saved'
S['r7_constructive_corrections']=json.dumps(report,ensure_ascii=False);S['review_iteration']='99 / R7A pool confinement';S.frame_set(original_frame);bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT),compress=True)
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
report['output']=str(OUT);report['output_sha256']=hashlib.sha256(OUT.read_bytes()).hexdigest();report['input_unchanged']=True;REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf8');print('R7A_READY',json.dumps({k:report[k] for k in ('pass','output','output_sha256','after_water_mesh','preserved_datums')},indent=2),flush=True)
