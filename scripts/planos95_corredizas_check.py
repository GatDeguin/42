import bpy,json,sys,math,bmesh
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
S=bpy.context.scene;out=Path(sys.argv[sys.argv.index('--')+1]);rigs=[bpy.data.objects[n] for n in ['DOOR | balconySide','DOOR | balconyRear_A','DOOR | balconyRear_B']]
def bounds(o):
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());p=[e.matrix_world@Vector(v) for v in e.bound_box];return ([min(v[i] for v in p) for i in range(3)],[max(v[i] for v in p) for i in range(3)])
def bbinter(a,b):return all(min(a[1][i],b[1][i])-max(a[0][i],b[0][i])>.0003 for i in range(3))
def volume_intersection(a,b):
 dg=bpy.context.evaluated_depsgraph_get();o=bpy.data.objects.new('TEST intersection',bpy.data.meshes.new_from_object(a.evaluated_get(dg)));S.collection.objects.link(o);o.matrix_world=a.matrix_world.copy();m=o.modifiers.new('intersection','BOOLEAN');m.operation='INTERSECT';m.solver='EXACT';m.object=b
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=e.to_mesh();bm=bmesh.new();bm.from_mesh(me);bm.transform(e.matrix_world);vol=abs(bm.calc_volume(signed=True));bm.free();e.to_mesh_clear();mesh=o.data;bpy.data.objects.remove(o,do_unlink=True);bpy.data.meshes.remove(mesh);return vol
hits=[];poses=[]
for r in rigs:
 if r.animation_data:r.animation_data.action=None
poses_values=[float(v) for v in sys.argv[sys.argv.index('--')+2].split(',')] if len(sys.argv)>sys.argv.index('--')+2 else [0,.1,.25,.5,.75,.9,1]
for frame in poses_values:
 for r in rigs:r['open']=frame;r.update_tag()
 bpy.context.view_layer.update();moving=[o for r in rigs for o in r.children_recursive if o.type=='MESH'];move_names={o.name for o in moving};static=[o for o in S.objects if o.type=='MESH' and o.name not in move_names and not o.name.startswith(('BOT95','Vegetación','Césped'))];cache={o.name:bounds(o) for o in moving+static};count=0
 for a in moving:
  if any(t in a.name.lower() for t in ['burlete','junta','taco','sello']):continue
  for b in static:
   if any(t in b.name.lower() for t in ['burlete','junta','taco','sello']):continue
   if not bbinter(cache[a.name],cache[b.name]):continue
   vol=volume_intersection(a,b);count+=1
   if vol>1e-8:
    hit={'frame':frame,'moving':a.name,'static':b.name,'volume_m3':vol};hits.append(hit);print('HIT',json.dumps(hit,ensure_ascii=False),flush=True)
 poses.append({'frame':frame,'intersections_computed':count});print('POSE_COMPLETE',frame,count,flush=True)
result={'model':bpy.data.filepath,'poses':poses,'hard_collision_hits':hits,'rig_count':len([o for o in S.objects if o.name.startswith('DOOR |')]),'method':'Evaluated mesh boolean INTERSECT; broadphase depth>0.3mm; positive volume>1e-8m3. Rubber/bearing interfaces excluded.'};out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('COLLISION_CHECK_DONE',len(hits),flush=True)
