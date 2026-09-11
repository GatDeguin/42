"""Independent file/print validation of a planos95 emission; does not certify design."""
import json,sys,argparse,hashlib,zipfile,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'planos95/_vendor'))
import pymupdf,ezdxf
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ar=ap.parse_args();out=(ROOT/ar.out).resolve();m=json.loads((out/'manifest.json').read_text(encoding='utf8'));measure=json.loads((out/'measurements.json').read_text(encoding='utf8'));geo=json.loads((out/'geometry.json').read_text(encoding='utf8'));pdf=pymupdf.open(out/m['pdf']);MM=72/25.4
checks=[]
def check(name,passed,evidence):checks.append({'name':name,'pass':bool(passed),'evidence':evidence})
check('Model hash matches frozen input',hashlib.sha256(Path(m['model']).read_bytes()).hexdigest()==m['model_sha256']==geo['sha256'],m['model_sha256'])
check('PDF page count matches manifest',len(pdf)==len(m['sheets']),len(pdf))
check('All PDF sheets are physical A2',all(abs(p.rect.width/MM-594)<.01 and abs(p.rect.height/MM-420)<.01 for p in pdf),[594,420])
check('PDF graphics fully vector',sum(len(p.get_images()) for p in pdf)==0,{'images':sum(len(p.get_images()) for p in pdf),'paths':sum(len(p.get_drawings()) for p in pdf)})
outside=[];small=[]
for i,page in enumerate(pdf):
 for block in page.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   for s in line['spans']:
    x0,y0,x1,y1=s['bbox']
    if x0<9*MM or x1>585*MM or y0<9*MM or y1>411*MM:outside.append([m['sheets'][i]['id'],s['text']])
    if s['size']/MM<2.39:small.append([m['sheets'][i]['id'],s['text'],s['size']/MM])
check('All text inside print frame',not outside,outside);check('Printed text at least 2.4 mm',not small,small)
dimcount=0;dxerrors=[];svgerrors=[]
for sh in m['sheets']:
 d=ezdxf.readfile(out/sh['dxf']);au=d.audit();dimcount+=len(d.modelspace().query('DIMENSION'))
 if d.units!=6 or au.errors:dxerrors.append([sh['id'],d.units,len(au.errors)])
 r=ET.parse(out/sh['svg']).getroot()
 if r.attrib.get('width')!='594mm' or r.attrib.get('height')!='420mm':svgerrors.append(sh['id'])
check('DXF opens with metre units and no audit errors',not dxerrors,dxerrors);check('Native CAD dimensions match drawing register',dimcount==len(measure['dimensions']),dimcount);check('SVG sheets physically sized A2',not svgerrors,svgerrors)
by={o['name']:o for o in geo['objects']};floor=by['Losa planta baja'];check('House footprint preserves 8 x 12 m',abs(floor['hi'][0]-floor['lo'][0]-8)<.001 and abs(floor['hi'][1]-floor['lo'][1]-12)<.001,[floor['hi'][0]-floor['lo'][0],floor['hi'][1]-floor['lo'][1]])
steps=[o for o in geo['objects'] if o['name'].startswith('Peldaño exterior ') and o['name'].split(' ')[-1].isdigit()];check('18 source treads retained',len(steps)==18,len(steps))
report={'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','model':m['model'],'model_sha256':m['model_sha256'],'checks':checks,'not_checked':['Municipal approval or code compliance','Engineering capacity or system performance','Independent 9.9 photographic approval'],'visual_review':'All sheets rendered; representative full-size sheets and complete contact sheet reviewed by author'}
(out/'print_validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
zipname=out/'Casa_de_Campo_Planos_Editables.zip'
with zipfile.ZipFile(zipname,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
 for p in out.iterdir():
  if p.suffix.lower() in ['.pdf','.svg','.dxf','.json','.md'] and p.name!='geometry.json':z.write(p,p.name)
print(json.dumps({'status':report['status'],'checks':len(checks),'failed':[c for c in checks if not c['pass']],'zip_bytes':zipname.stat().st_size},indent=2))
if report['status']!='PASS':sys.exit(1)
