"""CPU-only measured SAN8 validation; never saves frozen input."""
import bpy,bmesh,runpy,json,hashlib,math,sys,time
from pathlib import Path
from mathutils import Matrix,Vector
R=Path(r'D:\2026\42');OUT=R/'review99/r8_san';OUT.mkdir(exist_ok=True,parents=True)
SHA='9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e'
S=bpy.context.scene;S.frame_set(1);DG=bpy.context.evaluated_depsgraph_get()
assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==SHA
PATCH=R/'scripts/correcciones99_san_mecanica_r8.py'
PATCH_SHA=hashlib.sha256(PATCH.read_bytes()).hexdigest()
import numpy as np
mesh_hash_cache={}
def signature(o):
 h=hashlib.sha256(np.asarray(o.matrix_world,dtype=np.float32).tobytes())
 if o.type=='MESH':
  key=o.data.as_pointer()
  if key not in mesh_hash_cache:
   mh=hashlib.sha256()
   vs=np.empty(len(o.data.vertices)*3,dtype=np.float32);o.data.vertices.foreach_get('co',vs);mh.update(vs.tobytes())
   ls=np.empty(len(o.data.loops),dtype=np.int32);o.data.loops.foreach_get('vertex_index',ls);mh.update(ls.tobytes())
   mh.update(str([m.name if m else None for m in o.data.materials]).encode())
   for uv in o.data.uv_layers:
    arr=np.empty(len(uv.data)*2,dtype=np.float32);uv.data.foreach_get('uv',arr);mh.update(uv.name.encode());mh.update(arr.tobytes())
   mesh_hash_cache[key]=mh.digest()
  h.update(mesh_hash_cache[key])
 return h.hexdigest()
print('CAPTURE_BEFORE',flush=True)
before={o.name:signature(o) for o in bpy.data.objects}
print('BEFORE_CAPTURED',len(before),flush=True)
A=runpy.run_path(str(PATCH));rep=A['apply']();bpy.context.view_layer.update()
print('APPLY_FINISHED',flush=True)
mesh_hash_cache.clear();after={o.name:signature(o) for o in bpy.data.objects}
scope={'removed':sorted(set(before)-set(after)),'added':sorted(set(after)-set(before)),
 'changed_existing_geometry':[n for n in before.keys()&after.keys() if before[n]!=after[n]]}
print('APPLIED',len(scope['added']),scope['changed_existing_geometry'],flush=True)
idemp0=after.copy();A['apply']();mesh_hash_cache.clear();idemp={o.name:signature(o) for o in bpy.data.objects}==idemp0
main_names=rep['main_geometry_unchanged']
topology=[]
for n in rep['new_objects']:
 o=bpy.data.objects[n];bm=bmesh.new();bm.from_mesh(o.data)
 topology.append({'name':n,'nonmanifold':sum(not e.is_manifold for e in bm.edges),'volume_m3':bm.calc_volume(signed=True),'determinant':o.matrix_world.determinant()});bm.free()
def meshdata(o,origin):
 e=o.evaluated_get(DG);m=e.to_mesh();M=Matrix.Translation(-Vector(origin))@e.matrix_world
 v=[M@p.co for p in m.vertices];f=[list(q.vertices) for q in m.polygons];e.to_mesh_clear()
 return v,f
def bbox(v):return [[min(p[k] for p in v),max(p[k] for p in v)] for k in range(3)]
def overlap(a,b):return [min(a[k][1],b[k][1])-max(a[k][0],b[k][0]) for k in range(3)]
def intersection(da,db):
 made=[]
 try:
  for i,(v,f) in enumerate([da,db]):
   m=bpy.data.meshes.new('TEMP_SAN8');m.from_pydata(v,[],f);m.update();o=bpy.data.objects.new('TEMP_SAN8',m);S.collection.objects.link(o);made.append(o)
  mod=made[0].modifiers.new('Exact measured intersection','BOOLEAN');mod.operation='INTERSECT';mod.solver='EXACT';mod.object=made[1];DG.update()
  e=made[0].evaluated_get(DG);m=e.to_mesh();bm=bmesh.new();bm.from_mesh(m);vol=abs(bm.calc_volume(signed=True));bm.free();e.to_mesh_clear()
  return vol
 finally:
  for o in made:m=o.data;bpy.data.objects.remove(o,do_unlink=True);bpy.data.meshes.remove(m)
family_cache={}
for label,body,seat,tank,sign in A['FAMILIES']:
 pv=rep['families'][label]['pivot_blender'];g=rep['groups'][label]
 names=set(sum(g.values(),[]))|{body,tank}
 family_cache[label]={n:meshdata(bpy.data.objects[n],pv) for n in names}
ORIGINAL_SCENE=S
S=bpy.data.scenes.new('SAN8_TEMP_TEST');bpy.context.window.scene=S;DG=bpy.context.evaluated_depsgraph_get()
print('GEOMETRY_CACHED',flush=True)
tests=[];clashes=[];numerical_contacts=[];candidates=0;skips=0;start=time.time()
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
quick='--quick' in args
angles=[0,15,30,45,60,75,90] if quick else [2.25*k for k in range(41)]
for label,body,seat,tank,sign in A['FAMILIES']:
 p=rep['families'][label]['pivot_blender'];g=rep['groups'][label]
 names=set(sum(g.values(),[]))|{body,tank}
 cache=family_cache[label]
 # Convert moving default presentation back to closed; retain exact fixed geometry.
 closed={}
 for kind in ['fixed','seat','lid']:
  for n in g[kind]:
   v,f=cache[n];angle=bpy.data.objects[n]['san8_default_angle_deg']
   M=Matrix.Rotation(-sign*math.radians(angle),4,'X')
   closed[n]=([M@x for x in v],f)
 for n in [body,tank]:closed[n]=cache[n]
 fixed=g['fixed']+[body,tank];fb={n:bbox(closed[n][0]) for n in fixed}
 poses=set([(a,90) for a in angles]+[(0,a) for a in angles]+[(a,a) for a in angles])
 if not quick:poses.update((a,b) for a in range(0,91,15) for b in range(a,91,15))
 for sa,la in sorted(poses):
  moving={}
  for kind,ang in [('seat',sa),('lid',la)]:
   M=Matrix.Rotation(sign*math.radians(ang),4,'X')
   for n in g[kind]:v,f=closed[n];moving[n]=([M@x for x in v],f)
  mb={n:bbox(d[0]) for n,d in moving.items()}
  pairs=[(n,k) for n in moving for k in fixed]+[(n,k) for n in g['seat'] for k in g['lid']]
  num=0
  for n,k in pairs:
   dd=moving.get(k,closed.get(k));bb=mb.get(k,fb.get(k))
   if min(overlap(mb[n],bb))<=2e-7:skips+=1;continue
   candidates+=1;num+=1;v=intersection(moving[n],dd)
   if v>1e-11:
    row={'family':label,'seat_deg':sa,'lid_deg':la,'a':n,'b':k,'volume_m3':v,'volume_mm3':v*1e9}
    if n==seat and ' lid buffer ' in k and sa==la and v/(.014*.010)<3e-7:
     row['equivalent_contact_depth_m']=v/(.014*.010);row['classification']='Seat/lid-buffer intended tangent contact, <=0.3um numerical envelope; independently ray-checked.'
     numerical_contacts.append(row)
    else:clashes.append(row)
  tests.append({'family':label,'seat_deg':sa,'lid_deg':la,'exact_candidates':num})
  if len(tests)%10==0:print('POSE',label,sa,la,'tests',len(tests),'clashes',len(clashes),'secs',round(time.time()-start),flush=True)
 print('FAMILY_DONE',label,'clashes',len(clashes),flush=True)
from mathutils.bvhtree import BVHTree
stops=[];buffer_contacts=[];arm_joins=[]
for label,body,seat,tank,sign in A['FAMILIES']:
 def closed_mesh(n):
  v,f=family_cache[label][n];o=bpy.data.objects[n];angle=o.get('san8_default_angle_deg',0)
  M=Matrix.Rotation(-sign*math.radians(angle),4,'X')
  return [M@x for x in v],f
 sv,sf=closed_mesh(seat);seat_bvh=BVHTree.FromPolygons(sv,sf,all_triangles=False)
 lidname=rep['families'][label]['lid'];lv,lf=closed_mesh(lidname);lid_bvh=BVHTree.FromPolygons(lv,lf,all_triangles=False)
 for i in [1,2]:
  for kind,target in [('seat',seat),('lid',lidname)]:
   prefix='SAN8 | '+label+' H'+str(i)+' '+kind+' '
   v,f=closed_mesh(prefix+'dog')
   for angle,end,expect in [(0,0,False),(-.25,0,True),(90,90,False),(90.25,90,True)]:
    M=Matrix.Rotation(sign*math.radians(angle),4,'X')
    vol=intersection(([M@x for x in v],f),closed_mesh(prefix+'stop'+str(end)))
    stops.append({'family':label,'hinge':i,'group':kind,'angle_deg':angle,'stop_deg':end,'volume_mm3':vol*1e9,'overrun_expected':expect,'pass':(vol>1e-11) if expect else (vol<=1e-11)})
   vol=intersection(closed_mesh(prefix+'arm'),closed_mesh(target))
   arm_joins.append({'family':label,'hinge':i,'group':kind,'solidary_join_volume_mm3':vol*1e9,'pass':vol>1e-11})
 for n in rep['groups'][label]['lid']:
  if 'lid buffer' not in n:continue
  v,f=closed_mesh(n);bb=bbox(v);gaps=[];lidgaps=[]
  for u in [.1,.5,.9]:
   for vfrac in [.1,.5,.9]:
    x=bb[0][0]+u*(bb[0][1]-bb[0][0]);y=bb[1][0]+vfrac*(bb[1][1]-bb[1][0])
    loc,normal,idx,dist=seat_bvh.ray_cast(Vector((x,y,bb[2][0]+.0001)),Vector((0,0,-1)),.01)
    gaps.append(None if loc is None else bb[2][0]-loc.z)
    loc,normal,idx,dist=lid_bvh.ray_cast(Vector((x,y,bb[2][1]-.0001)),Vector((0,0,1)),.01)
    lidgaps.append(None if loc is None else loc.z-bb[2][1])
  buffer_contacts.append({'name':n,'seat_gaps_m':gaps,'lid_gaps_m':lidgaps,'pass':all(g is not None and abs(g)<3e-6 for g in gaps+lidgaps)})

bpy.context.window.scene=ORIGINAL_SCENE;bpy.data.scenes.remove(S);S=ORIGINAL_SCENE
report={'source_sha256':SHA,'patch_sha256':PATCH_SHA,'quick':quick,'positive_stops':stops,'lid_buffer_contacts':buffer_contacts,'solidary_arm_joins':arm_joins,'scope':scope,'idempotent':idemp,'main_geometry_preserved':all(before[n]==after[n] for n in main_names),'topology':topology,'tests':tests,'exact_intersections':candidates,'aabb_separated_or_tangent':skips,'clashes':clashes,'numerical_contacts':numerical_contacts,'seconds':time.time()-start,'threshold_m3':1e-11,'aabb_contact_tolerance_m':2e-7}
report['pass']=all(q['pass'] for q in stops+buffer_contacts+arm_joins) and not clashes and idemp and report['main_geometry_preserved'] and not scope['changed_existing_geometry'] and all(t['nonmanifold']==0 and t['volume_m3']>0 and t['determinant']>0 for t in topology)
(OUT/('validation_quick.json' if quick else 'validation.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
(OUT/'construction.json').write_text(json.dumps(rep,indent=2),encoding='utf-8')
if report['pass'] and not quick:
 for label,*_ in A['FAMILIES']:A['pose'](label,0,90)
 bpy.ops.wm.save_as_mainfile(filepath=str(R/'output/Casa_de_Campo_99_R8_san_preview.blend'))
print('SAN8_RESULT',report['pass'],'clashes',len(clashes),'seconds',report['seconds'],flush=True)
