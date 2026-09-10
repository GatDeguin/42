from pathlib import Path
import json,hashlib,subprocess
R=Path.cwd();p=R/'docs/preview95/publication-files.json';m=json.loads(p.read_text(encoding='utf8'));files=[]
for row in m['files']:
 f=(R/row['path']).resolve();assert R in f.parents and f.is_file()
 assert hashlib.sha256(f.read_bytes()).hexdigest()==row['sha256'],str(f)
 assert f.stat().st_size<100*1024**2,str(f)
 files.append(row['path'])
extra=['docs/preview95/publication-files.json','docs/index.html','web-tools/README.md','web-tools/package.json','web-tools/package-lock.json','docs/preview95/camera-optics.py','docs/preview95/source-envelopes.py','docs/preview95/wood/apply.py','docs/preview95/stools/apply.py','docs/preview95/clothes/apply.py','docs/preview95/brick/apply.py','docs/preview95/brick/calibrate.py','docs/preview95/clothes/application-report.json','docs/preview95/stools/application-report.json']
files+=extra;files+=[str(f.relative_to(R)).replace('\\','/') for f in (R/'web-tools').glob('photographic95*.mjs')]
files=list(dict.fromkeys(files));assert all((R/f).is_file() for f in files)
subprocess.run(['git','-c','core.autocrlf=false','add','--',*files],check=True)
print('STAGED_PUBLICATION_FILES',len(files),'verified_runtime_bytes',m['totalBytes'])
