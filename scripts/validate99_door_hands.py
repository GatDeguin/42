"""Independent read-only door and person-clearance validation; no render or source save."""
import bpy,bmesh,json,math,ast,hashlib,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parent.parent;S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
for nd in ast.parse((ROOT/'scripts/planos95_juntas_check.py').read_text('utf-8-sig')).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['bounds','overlap','vol']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<boolean helpers>','exec'))
def tree(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
 t=BVHTree.FromPolygons([ev.matrix_world@v.co for v in me.vertices],[list(p.vertices) for p in me.polygons],epsilon=1e-7);ev.to_mesh_clear();return t
def contains(a,b):return all(a[0][i]<=b[0][i]+1e-6 and a[1][i]>=b[1][i]-1e-6 for i in range(3))
def force(r,v):r['open']=v;r.update_tag();bpy.context.view_layer.update()
def bsource(b):return {'x':[b[0][0],b[1][0]],'z':[-b[1][1],-b[0][1]],'h':[b[0][2],b[1][2]]}
rigs=[bpy.data.objects['DOOR | '+k] for k in ['bedroomLink','bedroomDining']]
actions={r:r.animation_data.action for r in rigs}
for r in rigs:r.animation_data.action=None;force(r,0)
moving={r:[o for o in r.children_recursive if o.type=='MESH' and not o.hide_render] for r in rigs}
movnames={o.name for v in moving.values() for o in v}
region=([16.25,-10.05,3.24],[18.40,-6.90,5.55])
static=[o for o in S.objects if o.type=='MESH' and not o.hide_render and o.name not in movnames and overlap(bounds(o),region)]
static_cache={o.name:(bounds(o),tree(o)) for o in static}
records=[];hits=[];pairs=0;start=time.time()
for r in rigs:
 record={'rig':r.name,'moving':[o.name for o in moving[r]],'poses':[]}
 for i in range(41):
  force(r,i/40);n=0
  for a in moving[r]:
   ab=bounds(a);at=None
   for b in static:
    bb,bt=static_cache[b.name]
    if not overlap(ab,bb):continue
    if at is None:at=tree(a)
    if not contains(ab,bb) and not contains(bb,ab) and not at.overlap(bt):continue
    v=vol(a,b);pairs+=1
    if v>1e-8:
     row={'rig':r.name,'pose':i,'open':i/40,'moving':a.name,'static':b.name,'volume_m3':v};hits.append(row);n+=1
  record['poses'].append({'open':i/40,'hard_hits':n})
  if i%10==0:print('HANDS_POSE',r.name,i,'hits',n,flush=True)
 force(r,0);records.append(record)
# Exact continuous sourceZ extrema for every evaluated vertex under the -pi/2 driver.
# If these swept intervals are separated, all41x41 combinations are also separated.
intervals={}
for r in rigs:
 force(r,0);base=-r.location.y;values=[]
 for o in moving[r]:
  ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
  for v in me.vertices:
   p=ev.matrix_world@v.co;a=-p.y-base;b=p.x-r.location.x
   vals=[base+a,base+b]
   angle=math.atan2(b,a)
   for t in [angle,angle+math.pi,angle-math.pi]:
    if 0<t<math.pi/2:vals.append(base+a*math.cos(t)+b*math.sin(t))
   values.extend(vals)
  ev.to_mesh_clear()
 intervals[r.name]=[min(values),max(values)]
separation=intervals[rigs[1].name][0]-intervals[rigs[0].name][1]
combined={'exact_continuous_z_intervals':intervals,'minimum_separation_m':separation,'all_41_by_41_combinations_separated':separation>0,'proof':'Analytic extrema of each evaluated vertex under both -pi/2 rotations; a positive separating sourceZ plane proves disjoint sweeps.'}
# Person represented conservatively as a450mm-diameter1720mm-height vertical cylinder.
for r in rigs:force(r,1)
person_obstacles=[o for o in S.objects if o.type=='MESH' and not o.hide_render and overlap(bounds(o),region)]
pcache={o.name:(bounds(o),tree(o)) for o in person_obstacles}
bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.225,depth=1.72,location=(17,-9,4.125))
body=bpy.context.object;body.name='TEST person clearance'
waypoints=[(16.90,9.40),(16.97,9.00),(17.08,8.45),(17.10,7.72),(17.70,7.68),(18.12,7.68)]
samples=[]
for a,b in zip(waypoints,waypoints[1:]):
 length=math.dist(a,b);steps=max(1,math.ceil(length/.04))
 for j in range(steps):
  t=j/steps;samples.append((a[0]*(1-t)+b[0]*t,a[1]*(1-t)+b[1]*t))
samples.append(waypoints[-1]);person_hits=[]
for i,(x,z) in enumerate(samples):
 body.location=(x,-z,3.265+.86);bpy.context.view_layer.update();ab=bounds(body);at=tree(body)
 for o in person_obstacles:
  bb,bt=pcache[o.name]
  if not overlap(ab,bb):continue
  if not contains(ab,bb) and not contains(bb,ab) and not at.overlap(bt):continue
  v=vol(body,o)
  if v>1e-8:person_hits.append({'sample':i,'position_source':[x,3.265,z],'object':o.name,'volume_m3':v})
me=body.data;bpy.data.objects.remove(body,do_unlink=True);bpy.data.meshes.remove(me)
open_bounds={r.name:{o.name:bsource(bounds(o)) for o in moving[r]} for r in rigs}
for r,action in actions.items():r.animation_data.action=action
S.frame_set(1);bpy.context.view_layer.update()
camera_checks=[]
for name in ['REV | Dormitorio acceso','REV | Dormitorio completo','LUZ99 | Dormitorio desde paso']:
 cam=bpy.data.objects.get(name)
 if not cam:continue
 S.frame_set(cam.get('presentation_frame',1));bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
 corners=cam.data.view_frame(scene=S);xmin=min(p.x for p in corners);xmax=max(p.x for p in corners);ymin=min(p.y for p in corners);ymax=max(p.y for p in corners);zz=corners[0].z
 origin=cam.matrix_world.translation;ray_hits=[];door_hits=[]
 for iy in range(5):
  for ix in range(5):
   u=.1+ix*.2;v=.1+iy*.2;direction=cam.matrix_world.to_quaternion()@Vector((xmin*(1-u)+xmax*u,ymin*(1-v)+ymax*v,zz)).normalized()
   ray_origin=origin.copy();hit=False
   for retry in range(12):
    hit,loc,n,idx,ob,mat=S.ray_cast(dg,ray_origin,direction,distance=100)
    if not hit or not ob.hide_render:break
    ray_origin=loc+direction*.0001
   if hit:
    rec={'sample':[ix,iy],'object':ob.name,'distance_m':float((loc-origin).length)};ray_hits.append(rec)
    if ob.name in movnames:door_hits.append(rec)
 camera_checks.append({'name':name,'source_position':[origin.x,origin.z,-origin.y],'lens_mm':cam.data.lens,'presentation_frame':S.frame_current,'grid_samples':25,'moving_door_first_hits':door_hits,'moving_door_coverage_fraction':len(door_hits)/25,'near_obstruction':any(h['distance_m']<.035 for h in ray_hits),'central_first_hit':next((h for h in ray_hits if h['sample']==[2,2]),None)})
S.frame_set(1);bpy.context.view_layer.update()
report={'source':bpy.data.filepath,'sourceSHA256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'camera_checks':camera_checks,'door_checks':records,'static_objects':[o.name for o in static],'hard_intersections':hits,'boolean_pairs':pairs,'combined_doors':combined,'person':{'diameter_m':.45,'height_m':1.72,'floor_m':3.25,'feet_clearance_m':.015,'waypoints_source_xz':waypoints,'samples':len(samples),'spacing_max_m':.04,'hits':person_hits,'pass':not person_hits},'open90_bounds':open_bounds,'rig_count':len([o for o in S.objects if o.name.startswith('DOOR |')]),'seconds':time.time()-start}
report['pass']=not hits and separation>.005 and not person_hits and report['rig_count']==13
(ROOT/'review99/door_hands/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf8')
print('HANDS_VALIDATION '+json.dumps({k:report[k] for k in ['pass','boolean_pairs','combined_doors','person','hard_intersections','seconds']},ensure_ascii=True),flush=True)
