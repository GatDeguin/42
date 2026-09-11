import bpy,bmesh,ast,json,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path('D:/2026/42');S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();cache={}
for path,names in [('scripts/planos95_juntas_check.py',['bounds','overlap','vol']),('scripts/planos99_vent_check.py',['tree','inside','worth'])]:
 for nd in ast.parse((R/path).read_text(encoding='utf-8-sig')).body:
  if isinstance(nd,ast.FunctionDef) and nd.name in names:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
parts=[o for o in S.objects if o.type=='MESH' and o.name.startswith('VENT99 |')];bb={o.name:bounds(o) for o in parts};hits=[];count=0
for i,a in enumerate(parts):
 for b in parts[i+1:]:
  if not overlap(bb[a.name],bb[b.name]) or not worth(a,b):continue
  v=vol(a,b);count+=1
  if v>1e-8:hits.append({'a':a.name,'b':b.name,'volume_m3':v})
 if i%40==0:print('SELF',i,count,len(hits),flush=True)
nonmanifold=[]
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);n=sum(not e.is_manifold for e in bm.edges);bm.free()
 if n:nonmanifold.append({'name':o.name,'edges':n})
r={'nonmanifold':nonmanifold,'pass':not hits and not nonmanifold,'model':bpy.data.filepath,'sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'boolean_pairs':count,'positive_pairs':hits}
(R/'review99/vent_self_check_r7.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),'utf8');print('SELFRESULT',count,len(hits),flush=True)
