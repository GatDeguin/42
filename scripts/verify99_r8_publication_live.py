"""Verify each published R8 page/artifact byte and optionally the LFS source stream."""
from pathlib import Path
import json,hashlib,urllib.request,concurrent.futures,sys,time
R=Path(__file__).resolve().parents[1];out=R/'review99/github_r8_progress';manifest=json.loads((out/'publication_inventory.json').read_text('utf8'))
base='https://gatdeguin.github.io/42/';rows=[q for q in manifest['files'] if q['path'].startswith('docs/')]
def check(q):
 url=base+q['path'][5:];req=urllib.request.Request(url,headers={'User-Agent':'CasaCampo-PublicationVerifier/1.0','Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=90) as response:data=response.read();status=response.status
 digest=hashlib.sha256(data).hexdigest();assert digest==q['sha256'],(q['path'],digest,q['sha256']);return dict(path=q['path'],bytes=len(data),sha256=digest,status=status)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:public=list(ex.map(check,rows))
report=dict(sourceSHA256=manifest['sourceSHA256'],base=base,files=public,fileCount=len(public),passed=True,videoRendered=False)
if '--source' in sys.argv:
 url='https://media.githubusercontent.com/media/GatDeguin/42/main/output/Casa_de_Campo_99_R8.blend';h=hashlib.sha256();total=0
 req=urllib.request.Request(url,headers={'User-Agent':'CasaCampo-PublicationVerifier/1.0'})
 with urllib.request.urlopen(req,timeout=180) as response:
  while chunk:=response.read(1024*1024):h.update(chunk);total+=len(chunk)
 assert h.hexdigest()==manifest['sourceSHA256'];report['sourceDownload']=dict(url=url,bytes=total,sha256=h.hexdigest(),passed=True)
(out/'public_verification.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),'utf8');print(json.dumps({'passed':True,'files':len(public),'sourceDownloadVerified':'sourceDownload' in report},indent=2))
