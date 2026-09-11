import bpy,runpy,json,hashlib
from pathlib import Path
R=Path(r'D:/2026/42');p=Path(bpy.data.filepath);sha=hashlib.sha256(p.read_bytes()).hexdigest();m=runpy.run_path(str(R/'scripts/correcciones99_camara_pileta_r8.py'));r=m['apply']();before=list(bpy.data.objects);r2=m['apply']();assert r==r2 and before==list(bpy.data.objects);r['sourceSHA256']=sha;(R/'review99/r8_visual/pool_camera.json').write_text(json.dumps(r,indent=2,ensure_ascii=False),'utf8');assert hashlib.sha256(p.read_bytes()).hexdigest()==sha;print('R8_POOL_CAMERA_PASS',r,flush=True)
