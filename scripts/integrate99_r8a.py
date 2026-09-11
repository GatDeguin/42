"""Freeze pass1 mechanical/use integration after checked component delivery; no render."""
import bpy,runpy,hashlib,json,numpy as np
from pathlib import Path
R=Path(r'D:/2026/42');OUT=R/'review99/r8_integrated';OUT.mkdir(parents=True,exist_ok=True);S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
source=Path(bpy.data.filepath);sha=hashlib.sha256(source.read_bytes()).hexdigest();assert sha=='9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e'
files={'correcciones99_san_mecanica_r8.py':'ee0f76d211906a0543af05bd219de168f94eb6a5759c4fd8c24a584887681ab5','correcciones99_uso_r8.py':'ae8baf1028149fa8cacb3001a80e583ee8f88d4e821405b70a8a9299b85b1acd','correcciones99_optica_topologia_r8.py':None}
for f,h in files.items():
 if h:assert hashlib.sha256((R/'scripts'/f).read_bytes()).hexdigest()==h,f
snap=runpy.run_path(str(R/'scripts/correcciones99_textiles_botanica_r8.py'))['fingerprints'];before=snap(S.objects);reports={};modules={}
for name in files:
 m=runpy.run_path(str(R/'scripts'/name));modules[name]=m;reports[name]=m['apply']();bpy.context.view_layer.update();print('R8A_APPLIED',name,flush=True)
first=snap(S.objects)
for name,m in modules.items():m['apply']();bpy.context.view_layer.update()
second=snap(S.objects);assert first==second,'Pass1 idempotence failed'
sync=runpy.run_path(str(R/'scripts/sync99_scene_variants.py'))['apply']();S['revision99_integrated']='R8A construction and use preview; pass2/3 pending';S['review99_status']='R7D formal8.5; R8 pending independent9.9 review';S['video_render_requires_explicit_approval']=True
for sc in bpy.data.scenes:sc['revision99_authoritative_geometry']='R8A shared construction/use preview'
bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();dest=R/'output/Casa_de_Campo_99_R8A_construccion_preview.blend';bpy.ops.wm.save_as_mainfile(filepath=str(dest),compress=True);outsha=hashlib.sha256(dest.read_bytes()).hexdigest();assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
report={'source':str(source),'sourceSHA256':sha,'output':str(dest),'outputSHA256':outsha,'pass':True,'idempotent':True,'videoRendered':False,'scope':{'added':sorted(first.keys()-before.keys()),'removed':sorted(before.keys()-first.keys()),'changed':sorted(n for n in before.keys()&first.keys() if before[n]!=first[n])},'patches':reports,'scriptSHA256':{f:hashlib.sha256((R/'scripts'/f).read_bytes()).hexdigest() for f in files},'sceneSynchronization':sync}
(OUT/'pass1_manifest.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),'utf8');print('R8A_PASS1_FROZEN',outsha,len(S.objects),flush=True)
