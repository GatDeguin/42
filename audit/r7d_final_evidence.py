import json,hashlib
from pathlib import Path
from pypdf import PdfReader
import sys
sys.path.insert(0, str(Path(r'D:\2026\42\planos95\_vendor')))
import ezdxf
R=Path(r'D:\2026\42');O=R/'audit/r7d_final';O.mkdir(exist_ok=True)
P=R/'planos95/r7d_candidate';pm=json.loads((P/'package_manifest.json').read_text(encoding='utf-8'))
rows=[]
for r in pm['files']:
 f=P/r['path'];h=hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else None
 rows.append(dict(file=r['path'],exists=f.exists(),match=h==r['sha256'],actual=h))
f=P/pm['complete_pdf'];reader=PdfReader(f);pages=[]
for i,page in enumerate(reader.pages):
 txt=page.extract_text();pages.append(dict(page=i+1,size_mm=[round(float(page.mediabox.width)*25.4/72,3),round(float(page.mediabox.height)*25.4/72,3)],characters=len(txt),firstLines=txt.splitlines()[:6],hasR7='R7' in txt))
(O/'plans_text.txt').write_text('\n\n'.join(f'PAGE {i+1}\n{p.extract_text()}' for i,p in enumerate(reader.pages)),encoding='utf-8')
native=[]
for p in P.rglob('*.dxf'):
 d=ezdxf.readfile(p);native.append(dict(file=str(p.relative_to(P)),dimensions=len(d.modelspace().query('DIMENSION'))))
M=R/'review99/r7_final/stills';sm=json.loads((M/'manifest.json').read_text(encoding='utf-8'));stills=[]
for item in sm['images']:
 f=M/item['file'];h=hashlib.sha256(f.read_bytes()).hexdigest();stills.append(dict(key=item['key'],file=item['file'],match=h==item['sha256'],sha256=h))
report=dict(modelSHA=pm['model_sha256'],stillsSHA=sm['sourceSHA256'],plan_files=rows,pages=pages,pdfSHA=hashlib.sha256(f.read_bytes()).hexdigest(),nativeDXF=native,nativeDimensionCount=sum(p['dimensions'] for p in native),stills=stills,stillsCount=len(stills))
report['pdfSHA']=hashlib.sha256((P/pm['complete_pdf']).read_bytes()).hexdigest()
(O/'evidence_verification.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print('EVIDENCE',len(rows),'file checks',sum(r['match'] for r in rows),'pages',len(pages),'stills',len(stills),sum(r['match'] for r in stills),'DXF',report['nativeDimensionCount'],'PDFSHA',report['pdfSHA'])
print('PUBLICFILES',[(str(p.relative_to(R/'review99/github_r7d_progress')),p.stat().st_size) for p in (R/'review99/github_r7d_progress').rglob('*') if p.is_file()])
