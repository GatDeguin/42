"""Finish the R8 static pages when the authorised still rendering has completed."""
from pathlib import Path
import json,time,subprocess,sys
R=Path(__file__).resolve().parents[1];m=R/'review99/r8_final/stills/manifest.json';sha='60810e1945f53b339c070c6e77635f408b99c244fc07f43a5084ebeecdde5329'
last=-1
for _ in range(360):
 try:
  d=json.loads(m.read_text('utf8'));assert d['sourceSHA256']==sha;n=len(d['images'])
 except (FileNotFoundError,json.JSONDecodeError):n=0
 if n!=last:print('STILLS',n,'/26',flush=True);last=n
 if n==26:break
 time.sleep(10)
else:raise RuntimeError('Still rendering not completed within60minutes')
def run(script,*args):
 print('BUILD',script,flush=True);subprocess.run([sys.executable,str(R/'scripts'/script),*args],cwd=R,check=True)
run('publish99_gallery.py','--source','review99/r8_final/stills','--out','docs/renders99','--expected-sha',sha,'--revision','R8','--count','26')
run('planos95_publish.py','--source','planos95/r8_final','--dest','docs/avance-r8/planos','--expected-sha',sha,'--revision','R8','--viewer-url','../../','--gallery-url','../../renders99/','--back-url','../')
run('publish99_r8_full.py')
print('COMPLETE_R8_PAGES_BUILT',flush=True)
