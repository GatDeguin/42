"""Read-only R7D studio workstation inventory."""
import bpy,json,hashlib
from pathlib import Path
R=Path(r'D:\2026\42');S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();DG=bpy.context.evaluated_depsgraph_get()
EXPECTED='9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e';assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==EXPECTED
def entry(o):
 e=o.evaluated_get(DG);m=e.to_mesh();v=[e.matrix_world@p.co for p in m.vertices];e.to_mesh_clear()
 return dict(name=o.name,bounds={'x':[min(p.x for p in v),max(p.x for p in v)],'h':[min(p.z for p in v),max(p.z for p in v)],'z':[min(-p.y for p in v),max(-p.y for p in v)]},hidden=o.hide_render,materials=[m.name if m else None for m in o.data.materials])
parts=[entry(o) for o in S.objects if o.type=='MESH' and any(k in o.name.lower() for k in ['consola','teclado','silla estudio','sillón estudio','sillon estudio','silla operador','butaca estudio','silla ergonom','silla giratoria'])]
(R/'audit/r7d_preliminary/studio_workstation_inventory.json').write_text(json.dumps({'sha256':EXPECTED,'parts':parts},ensure_ascii=False,indent=2),encoding='utf-8')
for p in parts:print(p['name'],p['bounds'])
print('STUDIO_INVENTORY_DONE',len(parts),flush=True)
