"""Publish a verified frozen plan set into the existing Pages downloads directory."""
from pathlib import Path
import argparse, hashlib, html, json, re, shutil, sys, zipfile
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'planos95/_vendor'))
import pymupdf
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--dest',default='docs/planos');p.add_argument('--expected-sha',required=True);p.add_argument('--revision');p.add_argument('--review-threshold',default='9.9');p.add_argument('--viewer-url',default='../');p.add_argument('--gallery-url');a=p.parse_args()
src=(ROOT/a.source).resolve();dst=(ROOT/a.dest).resolve()
assert ROOT in src.parents and ROOT in dst.parents
read=lambda p:json.loads(p.read_text('utf8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):
 (dst/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n','utf8')
general=read(src/'manifest.json');details=read(src/'details/manifest.json');checks=read(src/'package_validation.json')
geometry=read(src/'geometry.json');meta=geometry.get('scene_metadata',{});r7=bool(meta.get('r7_constructive_corrections'))
model_name=Path(general['model']).name;revision=a.revision or (re.search(r'_(R[0-9]+[A-Za-z0-9]*)',model_name).group(1) if re.search(r'_(R[0-9]+[A-Za-z0-9]*)',model_name) else 'EN REVISION')
threshold=a.review_threshold.replace('.',',')
status='EN REVISION / SIN APROBACION '+threshold
pool_note=('A08: playa humeda -0,080 m y agua -0,030 m, profundidad actual 50 mm. El volumen de agua se recorto contra los acabados reales; fondo de agua -1,390 m.' if r7 else 'A08: playa humeda -0,080 m y agua -0,030 m, profundidad actual 50 mm. El volumen de agua invade 114 mm del fondo de hormigon; coordinacion pendiente.')
coordination=('R7 incorpora distribucion, encuentros humedos y ventilacion propuesta. La presencia de geometria no acredita prestaciones ni capacidad.' if r7 else 'A08: 50 mm actuales sobre playa humeda; volumen de agua invade 114 mm del fondo de hormigon. Correccion pendiente.')

assert general['model_sha256']==details['model_sha256']==a.expected_sha
assert sha(Path(general['model']))==a.expected_sha
assert checks['pages']==33 and checks['svg_files']==33 and checks['dxf_files']==33
assert checks['consistent_model_sha'] and checks['general_validation_pass'] and checks['detail_validation_pass']
assert checks['vector_only'] and checks['a2_all_pages']
pdfname='Casa_de_Campo_Planos_A2.pdf';zipname='Casa_de_Campo_Planos_Editables.zip'
sheets=general['sheets']+details['sheets'];assert len(sheets)==33 and len({s['id'] for s in sheets})==33
assert geometry['sha256']==a.expected_sha
with pymupdf.open(src/'Casa_de_Campo_Planos_Completos_95_A2.pdf') as preflight:
 assert len(preflight)==33 and not any(p.get_images() for p in preflight)
 assert all(abs(p.rect.width*25.4/72-594)<.01 and abs(p.rect.height*25.4/72-420)<.01 for p in preflight)
 if r7:
  assert all(meta.get(k) for k in ['r7_wet_details','r7_vent_details','door_hands99_v1']),'Incomplete R7 integration'
  pretext='\n'.join(p.get_text() for p in preflight)
  assert 'DETALLES R7' in pretext and '3,203m G' in pretext

dst.mkdir(parents=True,exist_ok=True)
css=(ROOT/'scripts/planos95_publication.css').read_text('utf8')
viewer_url=a.viewer_url
assert not viewer_url.startswith(('http:', 'https:')), 'Use a local viewer path'
viewer_target=(dst/viewer_url.split('#')[0].split('?')[0]).resolve()
assert ROOT/'docs' in viewer_target.parents or viewer_target==ROOT/'docs'
assert viewer_target.exists(), 'Viewer target missing'
gallery_url=a.gallery_url
if gallery_url:
 gallery_target=(dst/gallery_url.split('#')[0].split('?')[0]).resolve()
 assert gallery_target.exists(), 'Do not link a gallery before it exists'
 gallery_manifest=read((gallery_target if gallery_target.is_dir() else gallery_target.parent)/'manifest.json')
 assert gallery_manifest.get('sourceSHA256',gallery_manifest.get('model_sha256'))==a.expected_sha, 'Gallery belongs to a different source'
gallery_nav=f'<a href="{html.escape(gallery_url)}">Galeria {html.escape(revision)} &#8599;</a>' if gallery_url else f'<span class="pending">Galeria {html.escape(revision)} en preparacion</span>'
shutil.copy2(src/'Casa_de_Campo_Planos_Completos_95_A2.pdf',dst/pdfname)
for s in sheets:
 folder=src/('details' if s['id'].startswith('D') else '')
 for kind in ('svg','dxf'):shutil.copy2(folder/s[kind],dst/s[kind])
for fname in ('anclajes_medidos.json','fuentes.md'):shutil.copy2(src/'details'/fname,dst/fname)
extra_files=['dimensional_audit.json','dimension_register.csv','AUDITORIA_DIMENSIONAL.md','visual_review.json','REVISION_VISUAL.md','service_access_proposal.json','ACCESO_MANTENIMIENTO_D08.md']
for n in extra_files:
 assert (src/n).exists(), 'Required audit artifact missing: '+n
 shutil.copy2(src/n,dst/n)
shutil.copy2(src/'manifest.json',dst/'emission_manifest.json')
shutil.copy2(src/'details/manifest.json',dst/'details_manifest.json')
extra_files+=['emission_manifest.json','details_manifest.json']
validation={'status':'PASS_DOCUMENTAL','review_status':status,'model':model_name,'model_sha256':a.expected_sha,'pdf':pdfname,'checks':checks,'general':read(src/'print_validation.json'),'details':read(src/'details/validation.json'),'limits':['Documentary checks do not certify structural, hydraulic, acoustic, weather or statutory performance.',f'G records measured geometry; P records proposals. No approval at {a.review_threshold}/10 is claimed.',pool_note]}
write('print_validation.json',validation)
write('package_validation.json',dict(checks,model_sha256=a.expected_sha,review_status=status))
write('verification.json',{'model_sha256':a.expected_sha,'review_status':status,'combined':checks,'general':read(src/'verification.json'),'details':read(src/'details/validation.json')})
measurements=read(src/'measurements.json');measurements.update(model_sha256=a.expected_sha,detail_dimensions=details['dimensions'],detail_measurements=details['measurements'],proposal_register=details['proposal_register'])
write('measurements.json',measurements)
readme=f'''# Casa de Campo - planos {revision}\n\n{status}. Virrey del Pino, Partido de La Matanza, Buenos Aires.\n\n33 laminas A2 (21 generales + 12 de detalles), PDF vectorial, 33 SVG, 33 DXF y {checks['native_dxf_dimensions']} cotas DXF nativas. Imprimir PDF/SVG a 100 %, en A2 de 594 x 420 mm, sin ajustar a pagina. DXF en metros.\n\nG: geometria medida del modelo. F: referencias de fuente. P: propuestas dimensionales sujetas a proyecto y validacion. No es un proyecto ejecutivo aprobado. Norte orientativo segun el propietario; servicios disponibles y acometidas exactas por confirmar.\n\n{pool_note}\n\nModelo: {model_name}\nSHA256: {a.expected_sha}\n\nPDF: {pdfname}\nZIP: {zipname}\n\nVer manifest.json, measurements.json y print_validation.json para trazabilidad, cotas y limites de verificacion.\n'''
(dst/'README.md').write_text(readme,'utf8')
manifest={'project':'Casa de Campo','place':'Virrey del Pino, Partido de La Matanza, Buenos Aires','status':status,'revision':revision,'model':model_name,'model_sha256':a.expected_sha,'source_sha256':general['source_sha256'],'created_utc':general['created_utc'],'pdf':pdfname,'zip':zipname,'paper_mm':[594,420],'dxf_units':'metres','pages':33,'sheets':sheets,'checks':checks,'legend':{'F':'Referencia de fuente','G':'Geometria medida','P':'Propuesta dimensional'},'sources':details['sources'],'coordination_status':coordination,'navigation':{'viewer':viewer_url,'gallery':gallery_url,'gallery_status':'available' if gallery_url else 'in preparation'},'dimensional_audit':{'path':'dimensional_audit.json','critical_measures':len(read(src/'dimensional_audit.json')['measured_items']),'status':read(src/'dimensional_audit.json')['status']}}
assetnames=[pdfname]+[s[k] for s in sheets for k in ('svg','dxf')]+['README.md','measurements.json','verification.json','print_validation.json','package_validation.json','anclajes_medidos.json','fuentes.md']+extra_files
manifest['files']=[{'path':n,'bytes':(dst/n).stat().st_size,'sha256':sha(dst/n)} for n in assetnames]
write('manifest.json',manifest)
def card(s):
 sid=html.escape(s['id']);title=html.escape(s['title']);svg=html.escape(s['svg']);dxf=html.escape(s['dxf'])
 return f'<article><a class="sheet" href="{svg}" target="_blank"><img loading="lazy" src="{svg}" alt="{sid} - {title}"></a><div class="caption"><h2>{sid} - {title}</h2><nav aria-label="Descargas {sid}"><a href="{svg}" download>SVG &#8595;</a><a href="{dxf}" download>DXF &#8595;</a></nav></div></article>'
page=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#183638"><link rel="icon" href="data:,"><title>Planos {revision} - Casa de Campo / 42</title><style>{css}.group-title{{font-size:22px;font-weight:500;margin:40px 0 20px}}code{{overflow-wrap:anywhere;font-size:11px}}</style></head><body><header><strong>42 / CASA DE CAMPO</strong><nav class="site-nav" aria-label="Navegacion del proyecto"><a href="{html.escape(viewer_url)}">Volver al modelo 3D {html.escape(revision)} &#8599;</a>{gallery_nav}</nav></header><main><div class="intro"><span class="eyebrow">Virrey del Pino &middot; Partido de La Matanza &middot; Buenos Aires</span><h1>La propiedad, en planos.</h1><p>33 l&aacute;minas A2 de la revisi&oacute;n {revision}: implantaci&oacute;n, plantas, fachadas, cortes, cocinas, ba&ntilde;os y detalles. Incluyen cotas del modelo, huellas de uso y propuestas de encuentros constructivos, ac&uacute;stica y servicios.</p><div class="downloads"><a class="button primary" href="{pdfname}" target="_blank">Abrir las 33 l&aacute;minas en PDF &#8599;</a><a class="button" href="{zipname}" download>Descargar PDF + 33 SVG + 33 DXF &#8595;</a></div></div><div class="note"><strong>En revisi&oacute;n &middot; {revision} &middot; sin aprobaci&oacute;n de {threshold}/10.</strong> La geometr&iacute;a medida se identifica con G, las referencias de fuente con F y las propuestas con P. Las comprobaciones documentales pasaron; la capacidad resistente, las instalaciones y el desempe&ntilde;o de los sistemas requieren su proyecto y validaci&oacute;n. No es un proyecto ejecutivo aprobado para construcci&oacute;n.<br><strong>Pileta:</strong> {html.escape(pool_note)}</div><h2 class="group-title">Planos generales &middot; 21 l&aacute;minas</h2><div class="grid">{''.join(card(s) for s in general['sheets'])}</div><h2 class="group-title">Detalles &middot; 12 l&aacute;minas</h2><div class="grid">{''.join(card(s) for s in details['sheets'])}</div><footer>PDF y SVG: imprimir en A2 (594 &times; 420 mm), al 100 % y sin ajustar a p&aacute;gina. DXF: unidades en metros; {checks['native_dxf_dimensions']} cotas nativas.<br>Norte orientativo seg&uacute;n el propietario. Servicios disponibles; ubicaci&oacute;n exacta de acometidas por confirmar.<br><a href="manifest.json">Versi&oacute;n y trazabilidad</a> &middot; <a href="print_validation.json">Validaci&oacute;n documental</a> &middot; <a href="dimension_register.csv">Registro de {checks['native_dxf_dimensions']} cotas (CSV)</a> &middot; <a href="dimensional_audit.json">Auditoria dimensional</a> &middot; <a href="visual_review.json">Revision visual</a> &middot; <a href="ACCESO_MANTENIMIENTO_D08.md">Mantenimiento D08</a><br>Modelo {revision} &middot; SHA256 <code>{a.expected_sha}</code></footer></main></body></html>'''
(dst/'index.html').write_text(page,'utf8')
with zipfile.ZipFile(dst/zipname,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in assetnames+['manifest.json']:z.write(dst/n,n)
with pymupdf.open(dst/pdfname) as doc:
 assert len(doc)==33
 assert all(abs(p.rect.width*25.4/72-594)<.01 and abs(p.rect.height*25.4/72-420)<.01 for p in doc)
 assert sum(len(p.get_images()) for p in doc)==0
 text='\n'.join(p.get_text() for p in doc)
 for bad in ('si P11','cuando figura','silenciosamente'):assert bad not in text,bad
 pool_page=next(i for i,s in enumerate(general['sheets']) if s['id']=='A08');pool_text=' '.join(doc[pool_page].get_text().split());assert '50 mm' in pool_text
 assert ('114 mm' not in pool_text) if r7 else ('114 mm' in pool_text)
 assert 'Partido de La Matanza' in text
 assert '2100 G libre' in text and '200 G' in text and ('12 G cuerpo' in text or 'Cuerpo12 G' in text)
 if r7:
  assert meta.get('r7_wet_details') and meta.get('r7_vent_details') and meta.get('door_hands99_v1'),'R7 publication requires completed wet/vent/door metadata'
  assert '3,203m G' in text and 'DETALLES R7' in text
links=re.findall(r'(?:href|src)="([^"]+)"',page)
missing=[n for n in links if not n.startswith(('data:','http:','https:','#')) and not(dst/n.split('?')[0].split('#')[0]).exists()]
assert not missing,missing
with zipfile.ZipFile(dst/zipname) as z:
 assert z.testzip() is None
 assert len([n for n in z.namelist() if n.endswith('.svg')])==33
 assert len([n for n in z.namelist() if n.endswith('.dxf')])==33
 assert z.read(pdfname)==(dst/pdfname).read_bytes()
 assert read(dst/'manifest.json')['model_sha256']==a.expected_sha
 assert json.loads(z.read('manifest.json'))['model_sha256']==a.expected_sha
assert sha(Path(general['model']))==a.expected_sha
report={'status':'PASS','model_sha256':a.expected_sha,'review_status':status,'pages':33,'svg_files':33,'dxf_files':33,'native_dxf_dimensions':checks['native_dxf_dimensions'],'gallery_cards':page.count('<article>'),'unresolved_links':missing,'pdf_identical_to_emission':sha(dst/pdfname)==sha(src/'Casa_de_Campo_Planos_Completos_95_A2.pdf'),'pdf_sha256':sha(dst/pdfname),'zip_sha256':sha(dst/zipname),'zip_bytes':(dst/zipname).stat().st_size,'model_unchanged':True,'source_checks':checks,'navigation':manifest['navigation'],'copied_audits_match':all(sha(dst/n)==sha(src/n) for n in extra_files if n not in ['emission_manifest.json','details_manifest.json']),'manifest_bytes_match':all(sha(dst/f['path'])==f['sha256'] and (dst/f['path']).stat().st_size==f['bytes'] for f in manifest['files'])}
write('publication_validation.json',report)
print(json.dumps(report,indent=2))
