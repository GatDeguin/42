import bpy,json,ast,numpy as np,hashlib,bmesh
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
digest=hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest();assert digest=='a3663a5081dac391303f25b8e9994b1a412a008e971642af29fc2cbee849aa90'
root=Path(r'D:\2026\42\audit')
for n in ast.parse((root/'integral95_02_r6h_bearing_knees.py').read_text(encoding='utf8')).body:
 if isinstance(n,ast.FunctionDef):exec(compile(ast.Module(body=[n],type_ignores=[]),'<own helper>','exec'))
def flat_tris(o,h):
 v,f=raw(o);return [v[t][:,[0,1]] for t in f if max(abs(v[t][:,2]-h))<.000003]
seats=[o for o in S.objects if o.name.startswith('Banco huerta | tablón asiento')]
legs=[o for o in S.objects if o.name.startswith('Banco huerta | pata ')]
rows=[]
for leg in legs:
 v,f=raw(leg);h=v[:,2].max();legfaces=flat_tris(leg,h);areas=[]
 for seat in seats:
  bb=flat_tris(seat,h);a=sum(area(clip(pa,pb)) for pa in legfaces for pb in bb)
  if a>1e-10:areas.append({'seat':seat.name,'coplanar_contact_m2':a})
 rows.append({'leg':leg.name,'top_y':float(h),'contact_areas':areas,'total_contact_m2':sum(r['coplanar_contact_m2'] for r in areas),'pass_geometric_contact':sum(r['coplanar_contact_m2'] for r in areas)>1e-6})
geo_cache={}
for n in ast.parse((root/'integral95_02_r6k_dvh_final.py').read_text(encoding='utf8')).body:
 if isinstance(n,ast.FunctionDef):exec(compile(ast.Module(body=[n],type_ignores=[]),'<own exact helper>','exec'))
a=bpy.data.objects['Agua de pileta'];b=bpy.data.objects['Fondo de pileta']
vol=intersection(a,b)
r={'source':bpy.data.filepath,'sha256':digest,'bench':rows,'bench_classification':'Central ray meets 3mm rounded slat edge; positive contact over actual leg footprint means central-ray gap alone is not a floating leg. Capacity not assessed.','water_base_intersection_m3':vol}
(root/'integral95_02_r6k_bench_pool_clarification.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(r,ensure_ascii=False,indent=2),flush=True)
