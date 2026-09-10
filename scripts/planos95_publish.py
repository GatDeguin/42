"""Publish a verified frozen plan set into the existing Pages downloads directory."""
from pathlib import Path
import argparse, hashlib, html, json, re, shutil, sys, zipfile
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'planos95/_vendor'))
import pymupdf
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--dest',default='docs/planos');p.add_argument('--expected-sha',required=True);a=p.parse_args()
src=(ROOT/a.source).resolve();dst=(ROOT/a.dest).resolve()
assert ROOT in src.parents and ROOT in dst.parents
read=lambda p:json.loads(p.read_text('utf8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):
 (dst/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n','utf8')
general=read(src/'manifest.json');details=read(src/'details/manifest.json');checks=read(src/'package_validation.json')
assert general['model_sha256']==details['model_sha256']==a.expected_sha
assert sha(Path(general['model']))==a.expected_sha
assert checks['pages']==33 and checks['svg_files']==33 and checks['dxf_files']==33
assert checks['consistent_model_sha'] and checks['general_validation_pass'] and checks['detail_validation_pass']
assert checks['vector_only'] and checks['a2_all_pages']
pdfname='Casa_de_Campo_Planos_A2.pdf';zipname='Casa_de_Campo_Planos_Editables.zip'
sheets=general['sheets']+details['sheets'];assert len(sheets)==33 and len({s['id'] for s in sheets})==33
dst.mkdir(parents=True,exist_ok=True)
oldhtml=(dst/'index.html').read_text('utf8') if (dst/'index.html').exists() else ''
css=re.search(r'<style>(.*?)</style>',oldhtml,re.S).group(1) if '<style>' in oldhtml else ''
shutil.copy2(src/'Casa_de_Campo_Planos_Completos_95_A2.pdf',dst/pdfname)
for s in sheets:
 folder=src/('details' if s['id'].startswith('D') else '')
 for kind in ('svg','dxf'):shutil.copy2(folder/s[kind],dst/s[kind])
for fname in ('anclajes_medidos.json','fuentes.md'):shutil.copy2(src/'details'/fname,dst/fname)
status='EN REVISION / SIN APROBACION 9,5'
validation={'status':'PASS_DOCUMENTAL','review_status':status,'model':'Casa_de_Campo_95_R6K.blend','model_sha256':a.expected_sha,'pdf':pdfname,'checks':checks,'general':read(src/'print_validation.json'),'details':read(src/'details/validation.json'),'limits':['Documentary checks do not certify structural, hydraulic, acoustic, weather or statutory performance.','G records measured geometry; P records proposals. No approval at 9.5/10 is claimed.','A08 records water at -0.030 m, wet shelf at -0.080 m (50 mm water depth), and unresolved 114 mm overlap between the water volume and concrete floor.']}
write('print_validation.json',validation)
write('package_validation.json',dict(checks,model_sha256=a.expected_sha,review_status=status))
write('verification.json',{'model_sha256':a.expected_sha,'review_status':status,'combined':checks,'general':read(src/'verification.json'),'details':read(src/'details/validation.json')})
measurements=read(src/'measurements.json');measurements.update(model_sha256=a.expected_sha,detail_dimensions=details['dimensions'],detail_measurements=details['measurements'],proposal_register=details['proposal_register'])
write('measurements.json',measurements)
readme=f'''# Casa de Campo - planos R6K\n\n{status}. Virrey del Pino, Partido de La Matanza, Buenos Aires.\n\n33 laminas A2 (21 generales + 12 de detalles), PDF vectorial, 33 SVG, 33 DXF y {checks['native_dxf_dimensions']} cotas DXF nativas. Imprimir PDF/SVG a 100 %, en A2 de 594 x 420 mm, sin ajustar a pagina. DXF en metros.\n\nG: geometria medida del modelo. F: referencias de fuente. P: propuestas dimensionales sujetas a proyecto y validacion. No es un proyecto ejecutivo aprobado. Norte orientativo segun el propietario; servicios disponibles y acometidas exactas por confirmar.\n\nA08: playa humeda -0,080 m y agua -0,030 m, profundidad actual 50 mm. El volumen de agua penetra 114 mm en el fondo de hormigon: coordinacion pendiente de la siguiente revision.\n\nModelo: Casa_de_Campo_95_R6K.blend\nSHA256: {a.expected_sha}\n\nPDF: {pdfname}\nZIP: {zipname}\n\nVer manifest.json, measurements.json y print_validation.json para trazabilidad, cotas y limites de verificacion.\n'''
(dst/'README.md').write_text(readme,'utf8')
manifest={'project':'Casa de Campo','place':'Virrey del Pino, Partido de La Matanza, Buenos Aires','status':status,'revision':'R6K','model':'Casa_de_Campo_95_R6K.blend','model_sha256':a.expected_sha,'source_sha256':general['source_sha256'],'created_utc':general['created_utc'],'pdf':pdfname,'zip':zipname,'paper_mm':[594,420],'dxf_units':'metres','pages':33,'sheets':sheets,'checks':checks,'legend':{'F':'Referencia de fuente','G':'Geometria medida','P':'Propuesta dimensional'},'sources':details['sources'],'known_coordination_issue':'A08: 50 mm actuales sobre playa humeda; volumen de agua invade 114 mm del fondo de hormigon. Correccion pendiente.'}
assetnames=[pdfname]+[s[k] for s in sheets for k in ('svg','dxf')]+['README.md','measurements.json','verification.json','print_validation.json','package_validation.json','anclajes_medidos.json','fuentes.md']
manifest['files']=[{'path':n,'bytes':(dst/n).stat().st_size,'sha256':sha(dst/n)} for n in assetnames]
write('manifest.json',manifest)
def card(s):
 sid=html.escape(s['id']);title=html.escape(s['title']);svg=html.escape(s['svg']);dxf=html.escape(s['dxf'])
 return f'<article><a class="sheet" href="{svg}" target="_blank"><img loading="lazy" src="{svg}" alt="{sid} - {title}"></a><div class="caption"><h2>{sid} - {title}</h2><nav aria-label="Descargas {sid}"><a href="{svg}" download>SVG &#8595;</a><a href="{dxf}" download>DXF &#8595;</a></nav></div></article>'
page=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#183638"><link rel="icon" href="data:,"><title>Planos R6K - Casa de Campo / 42</title><style>{css}.group-title{{font-size:22px;font-weight:500;margin:40px 0 20px}}code{{overflow-wrap:anywhere;font-size:11px}}</style></head><body><header><strong>42 / CASA DE CAMPO</strong><a href="../">Volver al modelo 3D &#8599;</a></header><main><div class="intro"><span class="eyebrow">Virrey del Pino &middot; Partido de La Matanza &middot; Buenos Aires</span><h1>La propiedad, en planos.</h1><p>33 l&aacute;minas A2 de la revisi&oacute;n R6K: implantaci&oacute;n, plantas, fachadas, cortes, cocinas, ba&ntilde;os y detalles. Incluyen cotas del modelo, huellas de uso y propuestas de encuentros constructivos, ac&uacute;stica y servicios.</p><div class="downloads"><a class="button primary" href="{pdfname}" target="_blank">Abrir las 33 l&aacute;minas en PDF &#8599;</a><a class="button" href="{zipname}" download>Descargar PDF + 33 SVG + 33 DXF &#8595;</a></div></div><div class="note"><strong>En revisi&oacute;n &middot; R6K &middot; sin aprobaci&oacute;n de 9,5/10.</strong> La geometr&iacute;a medida se identifica con G, las referencias de fuente con F y las propuestas con P. Las comprobaciones documentales pasaron; la capacidad resistente, las instalaciones y el desempe&ntilde;o de los sistemas requieren su proyecto y validaci&oacute;n. No es un proyecto ejecutivo aprobado para construcci&oacute;n.<br><strong>Coordinaci&oacute;n pendiente en pileta:</strong> A08 muestra 50 mm de agua sobre la playa h&uacute;meda. El volumen de agua invade 114 mm del fondo de hormig&oacute;n; se consigna para corregir en la siguiente revisi&oacute;n.</div><h2 class="group-title">Planos generales &middot; 21 l&aacute;minas</h2><div class="grid">{''.join(card(s) for s in general['sheets'])}</div><h2 class="group-title">Detalles &middot; 12 l&aacute;minas</h2><div class="grid">{''.join(card(s) for s in details['sheets'])}</div><footer>PDF y SVG: imprimir en A2 (594 &times; 420 mm), al 100 % y sin ajustar a p&aacute;gina. DXF: unidades en metros; {checks['native_dxf_dimensions']} cotas nativas.<br>Norte orientativo seg&uacute;n el propietario. Servicios disponibles; ubicaci&oacute;n exacta de acometidas por confirmar.<br><a href="manifest.json">Versi&oacute;n y trazabilidad</a> &middot; <a href="print_validation.json">Validaci&oacute;n documental</a> &middot; <a href="measurements.json">Registro de cotas</a><br>Modelo R6K &middot; SHA256 <code>{a.expected_sha}</code></footer></main></body></html>'''
(dst/'index.html').write_text(page,'utf8')
with zipfile.ZipFile(dst/zipname,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in assetnames+['manifest.json']:z.write(dst/n,n)
with pymupdf.open(dst/pdfname) as doc:
 assert len(doc)==33
 assert all(abs(p.rect.width*25.4/72-594)<.01 and abs(p.rect.height*25.4/72-420)<.01 for p in doc)
 assert sum(len(p.get_images()) for p in doc)==0
 text='\n'.join(p.get_text() for p in doc)
 for bad in ('si P11','cuando figura','silenciosamente'):assert bad not in text,bad
 pool_text=' '.join(doc[10].get_text().split());assert '50 mm' in pool_text and '114 mm' in pool_text
 assert 'Partido de La Matanza' in text
 assert '2100 G libre' in text and '200 G' in text and '12 G cuerpo' in text
links=re.findall(r'(?:href|src)="([^"]+)"',page)
missing=[n for n in links if not n.startswith(('data:','http:','https:','../')) and not(dst/n).is_file()]
assert not missing,missing
with zipfile.ZipFile(dst/zipname) as z:
 assert z.testzip() is None
 assert len([n for n in z.namelist() if n.endswith('.svg')])==33
 assert len([n for n in z.namelist() if n.endswith('.dxf')])==33
 assert z.read(pdfname)==(dst/pdfname).read_bytes()
 assert read(dst/'manifest.json')['model_sha256']==a.expected_sha
 assert json.loads(z.read('manifest.json'))['model_sha256']==a.expected_sha
assert sha(Path(general['model']))==a.expected_sha
report={'status':'PASS','model_sha256':a.expected_sha,'review_status':status,'pages':33,'svg_files':33,'dxf_files':33,'native_dxf_dimensions':checks['native_dxf_dimensions'],'gallery_cards':page.count('<article>'),'unresolved_links':missing,'pdf_identical_to_emission':sha(dst/pdfname)==sha(src/'Casa_de_Campo_Planos_Completos_95_A2.pdf'),'pdf_sha256':sha(dst/pdfname),'zip_sha256':sha(dst/zipname),'zip_bytes':(dst/zipname).stat().st_size,'model_unchanged':True,'source_checks':checks}
write('publication_validation.json',report)
print(json.dumps(report,indent=2))
