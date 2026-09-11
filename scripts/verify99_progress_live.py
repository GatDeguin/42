from pathlib import Path
import subprocess,hashlib,json,time,urllib.request
ROOT=Path(r'D:\2026\42');COMMIT='59202185bc57176bdc91e53ee2a522839177d208';BASE='https://gatdeguin.github.io/42/'
report=dict(commit=COMMIT,checkedAt=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),pages=[],videoRendered=False)
for rel,url in [('docs/index.html',BASE),('docs/preview95/index.html',BASE+'preview95/'),('docs/avance-r7/index.html',BASE+'avance-r7/'),('docs/avance-r7/acceso-dormitorio.png',BASE+'avance-r7/acceso-dormitorio.png')]:
 expected=subprocess.check_output(['git','show',COMMIT+':'+rel],cwd=ROOT)
 r=urllib.request.urlopen(url,timeout=90);content=r.read();passed=content==expected
 report['pages'].append(dict(url=url,status=r.status,bytes=len(content),sha256=hashlib.sha256(content).hexdigest(),exactGitBytes=passed));assert passed,url
model=ROOT/'output/Casa_de_Campo_99_R7_avance.blend';expected=hashlib.sha256(model.read_bytes()).hexdigest()
url='https://media.githubusercontent.com/media/GatDeguin/42/'+COMMIT+'/output/Casa_de_Campo_99_R7_avance.blend'
h=hashlib.sha256();count=0
with urllib.request.urlopen(url,timeout=90) as r:
 while chunk:=r.read(1024*1024):h.update(chunk);count+=len(chunk)
report['model']=dict(url=url,status=r.status,bytes=count,sha256=h.hexdigest(),exactExpectedHash=h.hexdigest()==expected and count==model.stat().st_size)
assert report['model']['exactExpectedHash'];report['passed']=True
(ROOT/'review99/github_progress/live_verification_5920218.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=True),flush=True)