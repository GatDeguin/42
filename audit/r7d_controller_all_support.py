import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(r'D:\2026\42');S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();DG=bpy.context.evaluated_depsgraph_get()
rows=[]
for x in [18.20,18.22,18.35,18.55,18.7,18.765,18.85,18.90]:
 for z in [2.48,2.52,2.6,3.0,3.4,3.48,3.52]:
  hit,p,n,i,o,m=S.ray_cast(DG,Vector((x,-z,4.04539)),Vector((0,0,-1)),distance=.12)
  rows.append(dict(x=x,z=z,object=o.name if hit else None,h=p.z if hit else None,gap=4.045499801635742-p.z if hit else None))
candidates=[]
for o in S.objects:
 if o.type!='MESH':continue
 v=[o.matrix_world@Vector(p) for p in o.bound_box];lo=[min(q[k] for q in v) for k in range(3)];hi=[max(q[k] for q in v) for k in range(3)]
 if lo[0]<18.91 and hi[0]>18.19 and lo[1]<-2.46 and hi[1]>-3.54 and lo[2]<4.046 and hi[2]>3.995:
  candidates.append(dict(name=o.name,bounds=[lo,hi],hidden=o.hide_render))
(R/'audit/r7d_preliminary/studio_controller_all_support.json').write_text(json.dumps({'sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'rays':rows,'candidates':candidates},indent=2,ensure_ascii=False),encoding='utf-8')
print('CONTACTS',[q for q in rows if q['gap'] is not None and q['gap']<.002])
print('TARGETS',set(q['object'] for q in rows))
print('CANDIDATES',[q['name'] for q in candidates])
