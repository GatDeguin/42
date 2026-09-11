"""Read-only verification of the published R7D stills and plans bundle."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,subprocess,urllib.request,datetime
R=Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser();a.add_argument('--commit',required=True);args=a.parse_args()
base='https://gatdeguin.github.io/42/'
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',args.commit,'docs/planos99','docs/renders99'],cwd=R).decode().splitlines()
paths+=['docs/index.html','docs/preview99/index.html','docs/preview99/assets/model-info.json','docs/avance-r7/index.html']
def verify(name):
 expected=subprocess.check_output(['git','show',args.commit+':'+name],cwd=R)
 url=base+name.removeprefix('docs/')+'?revision='+args.commit
 req=urllib.request.Request(url,headers={'Cache-Control':'no-cache','User-Agent':'R7D-Deliverables-Verification'})
 with urllib.request.urlopen(req,timeout=60) as response:actual=response.read();status=response.status
 assert actual==expected,name
 return dict(path=name,status=status,bytes=len(actual),sha256=hashlib.sha256(actual).hexdigest())
rows=list(ThreadPoolExecutor(max_workers=4).map(verify,paths))
meta=json.loads(subprocess.check_output(['git','show',args.commit+':docs/preview99/assets/model-info.json'],cwd=R));assert meta['publication']['globalScore']==8.5
report=dict(status='PASS',commit=args.commit,url=base,verifiedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Exact public bytes of all gallery and plan files plus current entry pages and metadata; source Blender/GLB unchanged and previously verified.',files=rows,count=len(rows),bytes=sum(x['bytes'] for x in rows),score=8.5,approved=False,videoRendered=False)
out=R/'review99/r7d_bundle/public_verification.json';out.write_text(json.dumps(report,indent=2),encoding='utf-8')
print('PUBLIC_BUNDLE_PASS',len(rows),'files',round(report['bytes']/1024**2,2),'MiB',args.commit)
