"""Combine coherent general/detail drawing sets, preserving full vector PDF and CAD sources."""
from pathlib import Path
import argparse,sys,json,hashlib,shutil,zipfile
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT/'planos95/_vendor'))
import pymupdf
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--details',default='planos95/details95');ar=ap.parse_args()
out=(ROOT/ar.out).resolve();src=(ROOT/ar.details).resolve();dst=out/'details'
base=json.loads((out/'manifest.json').read_text(encoding='utf8'));det=json.loads((src/'manifest.json').read_text(encoding='utf8'));bv=json.loads((out/'print_validation.json').read_text(encoding='utf8'));dv=json.loads((src/'validation.json').read_text(encoding='utf8'))
assert base['model_sha256']==det['model_sha256']==hashlib.sha256(Path(base['model']).read_bytes()).hexdigest(), 'Mixed model versions'
assert bv['status']=='PASS' and not dv['text_outside_frame'] and not dv['dxf_errors'] and dv['anchor_evidence_matches']
assert src!=out and dst.parent==out
if src!=dst:
 dst.mkdir(exist_ok=True)
 for p in src.iterdir():
  if p.suffix.lower() in ['.pdf','.svg','.dxf','.json','.md','.csv']:shutil.copy2(p,dst/p.name)
 if (src/'qa').exists():shutil.copytree(src/'qa',dst/'qa',dirs_exist_ok=True)
book=pymupdf.open();a=pymupdf.open(out/base['pdf']);d=pymupdf.open(dst/det['pdf']);book.insert_pdf(a);book.insert_pdf(d)
toc=[[1,'Planos generales A00-A16',1]]+[[2,s['id']+' | '+s['title'],i+1] for i,s in enumerate(base['sheets'])]+[[1,'Detalles G/P '+det['sheets'][0]['id']+'-'+det['sheets'][-1]['id'],len(a)+1]]+[[2,s['id']+' | '+s['title'],len(a)+i+1] for i,s in enumerate(det['sheets'])]
book.set_toc(toc);book.set_metadata({'title':'Casa de Campo | Planos generales y detalles G-P','subject':'Modelo '+Path(base['model']).name+' / SHA256 '+base['model_sha256'],'author':'Proyecto Casa de Campo','keywords':'A2, vectorial, G medido, P propuesto, revision'})
name='Casa_de_Campo_Planos_Completos_95_A2.pdf';book.save(out/name,garbage=4,deflate=True)
MM=72/25.4
checks={'consistent_model_sha':True,'general_validation_pass':bv['status']=='PASS','detail_validation_pass':not dv['text_outside_frame'] and not dv['dxf_errors'],'pages':len(book),'general_pages':len(a),'detail_pages':len(d),'vector_only':sum(len(p.get_images()) for p in book)==0,'a2_all_pages':all(abs(p.rect.width/MM-594)<.01 and abs(p.rect.height/MM-420)<.01 for p in book),'native_dxf_dimensions':base['metrics']['dimension_count']+dv['native_dxf_dimensions'],'dxf_files':len(base['sheets'])+len(det['sheets']),'svg_files':len(base['sheets'])+len(det['sheets']),'anchor_evidence_matches':dv['anchor_evidence_matches'],'minimum_font_mm':round(min(sp['size']/MM for pg in book for bl in pg.get_text('dict')['blocks'] for ln in bl.get('lines',[]) for sp in ln['spans']),3)}
assert checks['pages']==len(base['sheets'])+len(det['sheets']) and checks['vector_only'] and checks['a2_all_pages']
files=[p for p in out.rglob('*') if p.is_file() and 'qa' not in p.relative_to(out).parts and p.suffix.lower() in ['.pdf','.svg','.dxf','.json','.md','.csv'] and p.name not in ['geometry.json','package_manifest.json','package_validation.json','handoff_checks.json']]
package={'project':'Casa de Campo','status':base['status'],'model':base['model'],'model_sha256':base['model_sha256'],'complete_pdf':name,'general_pdf':base['pdf'],'details_pdf':'details/'+det['pdf'],'checks':checks,'files':[{ 'path':p.relative_to(out).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
(out/'package_validation.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False),encoding='utf8')
(out/'README_ENTREGA.md').write_text('# Planos generales y detalles\n\nEstado: '+base['status']+'\n\nPDF principal: '+name+'\n\n'+str(checks['pages'])+' laminas A2: '+str(checks['general_pages'])+' generales y '+str(checks['detail_pages'])+' de detalles. '+str(checks['native_dxf_dimensions'])+' cotas nativas DXF; PDF y SVG vectoriales al 100 %. DXF en metros, vistas separadas horizontalmente.\n\nModelo: '+Path(base['model']).name+'\nSHA256: '+base['model_sha256']+'\n\nG identifica geometria medida; P identifica propuestas de coordinacion. Los desarrollos incorporados se muestran como G medido, sin certificar su capacidad o prestaciones. D04 registra placas, grout y 68 vastagos del modelo:100 mm dentro del hormigon es una dimension geometrica propuesta, no capacidad validada.\n\nEl paquete conserva las hojas base por separado y el suplemento en details/. Las referencias de fabricante estan en details/fuentes.md y enlazadas en el PDF.\n\nNo es un proyecto ejecutivo certificado. Se requieren mensura, topografia, suelos y calculos estructurales, de instalaciones y acusticos. El umbral critico 9,9 y el realismo fotografico se evalúan por separado. Video pausado.\n\nGeneradores: scripts/planos95_build.py, scripts/planos95_details_build.py. Validacion: scripts/planos95_verify.py. Paquete: scripts/planos95_package.py.\n',encoding='utf8')
# Refresh file inventory after the delivery index is written.
files=[p for p in out.rglob('*') if p.is_file() and 'qa' not in p.relative_to(out).parts and p.suffix.lower() in ['.pdf','.svg','.dxf','.json','.md','.csv'] and p.name not in ['geometry.json','package_manifest.json','handoff_checks.json']]
package['files']=[{'path':p.relative_to(out).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
(out/'package_manifest.json').write_text(json.dumps(package,indent=2,ensure_ascii=False),encoding='utf8')
zipname=out/'Casa_de_Campo_Planos_Completos_95_Editables.zip'
with zipfile.ZipFile(zipname,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
 for p in files+[out/'package_manifest.json']:z.write(p,p.relative_to(out).as_posix())
print(json.dumps({'pdf':str(out/name),'zip':str(zipname),'zip_bytes':zipname.stat().st_size,'checks':checks,'model_sha256':base['model_sha256']},indent=2))
