"""Verify the published Pages bytes and full LFS downloads against the R7D manifest."""
from pathlib import Path
import argparse,json,hashlib,subprocess,time,urllib.request,concurrent.futures
R=Path(__file__).resolve().parents[1];P=argparse.ArgumentParser();P.add_argument('--commit',required=True);A=P.parse_args();COMMIT=A.commit;BASE='https://gatdeguin.github.io/42/'
manifest=json.loads((R/'review99/github_r7d_progress/manifest.json').read_text(encoding='utf8'));package=json.loads((R/'docs/preview99/assets/web-package.json').read_text(encoding='utf8'))
report=dict(commit=COMMIT,sourceSHA256=manifest['sourceSHA256'],checkedAt=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),pages=[],resources=[],downloads=[],videoRendered=False)
def remote(url,sha,size):
 h=hashlib.sha256();count=0
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'R7D-publication-verification'}),timeout=120) as response:
  for chunk in iter(lambda:response.read(1024*1024),b''):h.update(chunk);count+=len(chunk)
  status=response.status
 row=dict(url=url,status=status,bytes=count,sha256=h.hexdigest(),passed=count==size and h.hexdigest()==sha);assert row['passed'],row;return row
for rel,url in [('docs/index.html',BASE),('docs/preview99/index.html',BASE+'preview99/'),('docs/avance-r7/index.html',BASE+'avance-r7/'),('docs/preview99/assets/model-info.json',BASE+'preview99/assets/model-info.json')]+[('docs/'+x['publicFile'],BASE+x['publicFile']) for x in manifest['images']]:
 data=subprocess.check_output(['git','show',COMMIT+':'+rel],cwd=R);report['pages'].append(remote(url,hashlib.sha256(data).hexdigest(),len(data)))
print('PUBLIC_PAGES_MATCH',len(report['pages']),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 futures=[pool.submit(remote,BASE+'preview99/assets/'+f['uri'],f['sha256'],f['bytes']) for f in package['files']]
 for f in futures:report['resources'].append(f.result())
print('PUBLIC_WEB_RESOURCES_MATCH',len(report['resources']),flush=True)
for path,sha,size in [(manifest['source'],manifest['sourceSHA256'],manifest['sourceBytes']),(manifest['glb'],manifest['glbSHA256'],manifest['glbBytes'])]:
 url='https://media.githubusercontent.com/media/GatDeguin/42/'+COMMIT+'/'+path;report['downloads'].append(remote(url,sha,size));print('PUBLIC_DOWNLOAD_MATCH',path,size,flush=True)
report['passed']=True
out=R/'review99/github_r7d_progress'/('live_verification_'+COMMIT[:7]+'.json');out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print('R7D_PUBLICATION_VERIFIED',out,flush=True)
