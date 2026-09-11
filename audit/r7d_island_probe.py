"""Independent R7D island/stool dimensional audit. Read-only source; CPU, no renders."""
import bpy,bmesh,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(r'D:\2026\42'); OUT=R/'audit/r7d_preliminary'
EXPECTED='9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e'
assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==EXPECTED
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();DG=bpy.context.evaluated_depsgraph_get()
cache={}
def geometry(o):
 if o.name not in cache:
  e=o.evaluated_get(DG);m=e.to_mesh();v=[e.matrix_world@q.co for q in m.vertices];f=[list(p.vertices) for p in m.polygons];e.to_mesh_clear()
  cache[o.name]=(v,f)
 return cache[o.name]
def bounds(o):
 v,f=geometry(o);return {'x':[min(q.x for q in v),max(q.x for q in v)],'h':[min(q.z for q in v),max(q.z for q in v)],'z':[min(-q.y for q in v),max(-q.y for q in v)]}
def entry(o):return dict(name=o.name,bounds=bounds(o),hidden=o.hide_render,materials=[m.name if m else None for m in o.data.materials])
parts=[o for o in S.objects if o.type=='MESH' and o.name.startswith(('Isla cocina mono','Taburete isla mono'))]
others=[o for o in S.objects if o.type=='MESH' and o.name.startswith(('Piso mono','Piso planta baja','Mesada cocina mono','Bajos cocina mono','Mesa mono','Silla mono','Sofá mono','Sofa mono'))]
island=[o for o in parts if o.name.startswith('Isla')]
trees={o.name:BVHTree.FromPolygons(*geometry(o),all_triangles=False) for o in island}
top=next(o for o in island if o.name=='Isla cocina mono tapa');tb=bounds(top); seats=[o for o in parts if 'asiento' in o.name.lower()]
if not seats:seats=[o for o in parts if o.name in ['Taburete isla mono A','Taburete isla mono B']]
probes=[]
for seat in seats:
 sb=bounds(seat);xc=sum(sb['x'])/2;zc=sum(sb['z'])/2
 for dx in [-.25,-.12,0,.12,.25]:
  for h in [.75,.86,.92,1.00,1.065]:
   origin=Vector((xc+dx,-2.8,h));direction=Vector((0,-1,0));hits=[]
   for name,tree in trees.items():
    hit=tree.ray_cast(origin,direction,2)
    if hit[0] is not None:hits.append({'name':name,'z':-hit[0].y,'distance':hit[3]})
   hits.sort(key=lambda q:q['distance'])
   probes.append(dict(seat=seat.name,x=xc+dx,h=h,first=hits[0] if hits else None))
report=dict(sha256=EXPECTED,frame=1,axes='source X,H,Z = Blender X,Z,-Y',floorH=.21,
parts=[entry(o) for o in parts],context=[entry(o) for o in others],rayStations=probes,
sourceReference={'url':'https://kb.nkba.org/uploads/2022/05/Kitchen-Planning-Guidelines.pdf','guideline':9,'counter_height_mm':914,'knee_width_mm':610,'knee_depth_mm':381,'status':'design recommendation; not Argentine legal requirement'})
(OUT/'island_probe.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('ISLAND_PROBE_DONE',len(parts),len(seats),len(probes),flush=True)
for o in parts:print(o.name,json.dumps(bounds(o)))
