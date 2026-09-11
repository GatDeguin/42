"""Publish a validated 33/35-sheet emission; --preview stays outside docs.
Checks actual source, PDF, ZIP inventory, SVG sizes and every native CAD dimension
before writing. No approval or architectural score is inferred from document QA.
"""
from pathlib import Path
import argparse, csv, hashlib, html, json, re, shutil, sys, zipfile
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'planos95/_vendor'))
import pymupdf, ezdxf

p=argparse.ArgumentParser()
p.add_argument('--source',required=True);p.add_argument('--dest',default='docs/planos')
p.add_argument('--expected-sha',required=True);p.add_argument('--revision')
p.add_argument('--review-threshold',default='9.9');p.add_argument('--viewer-url')
p.add_argument('--gallery-url');p.add_argument('--no-viewer',action='store_true');p.add_argument('--back-url');p.add_argument('--preview',action='store_true')
a=p.parse_args();src=(ROOT/a.source).resolve();dst=(ROOT/a.dest).resolve()
assert ROOT in src.parents and ROOT in dst.parents and src!=dst,'Source/destination must be distinct workspace directories'
assert not a.preview or not (dst==ROOT/'docs' or ROOT/'docs' in dst.parents),'Preview publication cannot write docs'
expected=a.expected_sha.lower();assert re.fullmatch('[0-9a-f]{64}',expected),'Invalid expected SHA256'
read=lambda path:json.loads(path.read_text('utf8'))
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()

def write(name,data):
 path=dst/name;path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n','utf8')

def local_target(base,name):
 assert not name.startswith(('http:','https:','//')),'Use local project navigation'
 q=(base/name.split('#')[0].split('?')[0]).resolve()
 assert q==ROOT or ROOT in q.parents,'Path outside workspace'
 return q

def emission_path(sheet,kind):
 name=sheet[kind];assert Path(name).name==name and name.endswith('.'+kind),'Unexpected sheet filename'
 return src/('details' if sheet['id'].startswith('D') else '')/name

general=read(src/'manifest.json');details=read(src/'details/manifest.json')
checks=read(src/'package_validation.json');package=read(src/'package_manifest.json')
geometry=read(src/'geometry.json');meta=geometry.get('scene_metadata',{})
r7=bool(meta.get('r7_constructive_corrections'));r8=bool(meta.get('r8_uso_details'))
model=Path(general['model']);model_name=model.name
match=re.search(r'_(R[0-9]+[A-Za-z0-9]*)',model_name)
revision=a.revision or (match.group(1) if match else 'EN REVISION')
source_preview='preview' in model_name.lower() or 'PREVIEW' in general.get('status','').upper()
assert not source_preview or a.preview,'Preview emission requires --preview'
threshold=a.review_threshold.replace('.',',')
status=('PREVIEW LOCAL / ' if a.preview else '')+'EN REVISION / SIN APROBACION '+threshold
sheets=general['sheets']+details['sheets'];count=len(sheets);ids=[s['id'] for s in sheets]
assert count in (33,35) and len(set(ids))==count,'Supported coherent sets have 33 or35 unique sheets'
assert count==(35 if r8 else 33),'R8 metadata and sheet count disagree'
assert not r8 or ids[-2:]==['D13','D14'],'R8 use sheets missing or misplaced'
assert general['model_sha256']==details['model_sha256']==geometry['sha256']==package['model_sha256']==expected,'Emission source SHA mismatch'
assert sha(model)==expected,'Blender source SHA mismatch'
assert checks==package['checks'],'Package validation differs from manifest'
assert checks['pages']==checks['svg_files']==checks['dxf_files']==count
assert checks['general_pages']==len(general['sheets']) and checks['detail_pages']==len(details['sheets'])
for key in ['consistent_model_sha','general_validation_pass','detail_validation_pass','vector_only','a2_all_pages','anchor_evidence_matches']:
 assert checks[key],key
assert checks['minimum_font_mm']>=2.5,'Minimum font below2.5mm'

# Verify both on-disk package and zipped bytes, not only a reported PASS.
source_pdf=src/package['complete_pdf'];source_zip=src/'Casa_de_Campo_Planos_Completos_95_Editables.zip'
source_entries={f['path']:f for f in package['files']}
assert len(source_entries)==len(package['files']),'Duplicate package paths'
with zipfile.ZipFile(source_zip) as z:
 assert z.testzip() is None,'Corrupt source ZIP'
 assert len(z.namelist())==len(set(z.namelist())),'Duplicate ZIP members'
 assert set(z.namelist())==set(source_entries)|{'package_manifest.json'},'ZIP inventory mismatch'
 assert z.read('package_manifest.json')==(src/'package_manifest.json').read_bytes()
 for name,f in source_entries.items():
  q=(src/name).resolve();assert src in q.parents and q.is_file(),'Invalid source asset '+name
  raw=q.read_bytes();assert len(raw)==f['bytes'] and hashlib.sha256(raw).hexdigest()==f['sha256'],'Changed source asset '+name
  assert z.read(name)==raw,'ZIP bytes differ: '+name
 assert len([n for n in z.namelist() if n.endswith('.svg')])==count
 assert len([n for n in z.namelist() if n.endswith('.dxf')])==count

audit=read(src/'dimensional_audit.json')
assert audit['status']=='PASS' and audit['model_sha256']==expected
assert all(c['pass'] for c in audit['checks']) and all(c['pass'] for c in audit['measured_items'])
with (src/'dimension_register.csv').open(encoding='utf-8-sig',newline='') as f:register=list(csv.DictReader(f))
assert len(register)==checks['native_dxf_dimensions']==audit['all_dimension_count']
assert set(row['sheet'] for row in register)<=set(ids)
cad_records=[]
for sheet in sheets:
 svg=emission_path(sheet,'svg');dxf=emission_path(sheet,'dxf')
 for q in [svg,dxf]:assert q.relative_to(src).as_posix() in source_entries,'Unregistered drawing'
 el=ET.parse(svg).getroot()
 assert el.attrib.get('width')=='594mm' and el.attrib.get('height')=='420mm','SVG is not physical A2'
 cad=ezdxf.readfile(dxf);assert not cad.audit().errors,'DXF audit failed: '+sheet['id']
 assert cad.header['$INSUNITS']==6,'DXF must use metres'
 dims=list(cad.modelspace().query('DIMENSION'));rows=[r for r in register if r['sheet']==sheet['id']]
 assert len(dims)==len(rows),'CAD/register count mismatch '+sheet['id']
 for index,(dim,row) in enumerate(zip(dims,rows)):
  value=abs(float(row['value_m']));actual=abs(float(dim.get_measurement()))
  assert abs(abs(float(row['to_m'])-float(row['from_m']))-value)<1e-6,'Register arithmetic'
  assert abs(actual-value)<1e-6,'CAD value mismatch '+sheet['id']
  cad_records.append({'sheet':sheet['id'],'index':index,'cad_m':actual,'register_m':value})

with pymupdf.open(source_pdf) as book:
 assert len(book)==count and not any(pg.get_images() for pg in book),'PDF pages/vector check'
 assert all(abs(pg.rect.width*25.4/72-594)<.01 and abs(pg.rect.height*25.4/72-420)<.01 for pg in book)
 fonts=[sp['size']*25.4/72 for pg in book for bl in pg.get_text('dict')['blocks'] for ln in bl.get('lines',[]) for sp in ln['spans']]
 assert min(fonts)>=2.499,'PDF type below physical minimum'
 text='\n'.join(pg.get_text() for pg in book)
 for bad in ('si P11','cuando figura','silenciosamente'):assert bad not in text,bad
 assert 'Partido de La Matanza' in text
 pooltext=' '.join(book[ids.index('A08')].get_text().split());assert '50 mm' in pooltext
 assert ('114 mm' not in pooltext) if r7 else ('114 mm' in pooltext)
 assert '2100 G libre' in text and '200 G' in text and ('12 G cuerpo' in text or 'Cuerpo12 G' in text)
 if r7:
  assert all(meta.get(k) for k in ['r7_wet_details','r7_vent_details','door_hands99_v1']),'Incomplete construction metadata'
  assert '3,203m G' in text and ('DETALLES R8' if r8 else 'DETALLES R7') in text
 if r8:assert 'D13' in text and 'D14' in text

# Production requires source-specific visual/service evidence. A local preview may
# exercise the package before those reviews, but must expose their absence.
extra_files=['dimensional_audit.json','dimension_register.csv','AUDITORIA_DIMENSIONAL.md']
optional_pairs=[('visual_review.json','REVISION_VISUAL.md'),('service_access_proposal.json','ACCESO_MANTENIMIENTO_D08.md')]
pending=[]
for json_name,md_name in optional_pairs:
 if not (src/json_name).exists() or not (src/md_name).exists():
  assert a.preview,'Required production evidence missing: '+json_name
  pending.append(json_name);continue
 ev=read(src/json_name);assert ev.get('model_sha256',ev.get('sha256'))==expected,'Evidence from another model: '+json_name
 if json_name=='visual_review.json':
  assert ev['status']=='PASS_DOCUMENT_COMPOSITION' and set(ev['overview_sheets'])==set(ids),'Incomplete visual review'
 else:assert ev.get('pass') is True,'Service access evidence failed'
 extra_files.extend([json_name,md_name])
if r8:
 ev=read(src/'use_evidence/use_validation.json');em=read(src/'r8_emission.json')
 assert ev['sha256']==expected and ev['status']=='PASS' and em['source_sha256']==expected
 assert bool(em['preview'])==source_preview,'R8 preview declaration mismatch'
 extra_files.extend(['use_evidence/use_validation.json','r8_emission.json'])

for name in extra_files:assert name in source_entries,'Evidence not covered by package manifest; repackage emission: '+name

assert not (a.no_viewer and a.viewer_url),'Choose --no-viewer or --viewer-url'
viewer_url=None if a.no_viewer else a.viewer_url or (None if a.preview else '../')
back_url=a.back_url;back_source=None
if back_url:
 back_target=local_target(dst,back_url);assert (back_target/'index.html' if back_target.is_dir() else back_target).is_file(),'Return navigation page missing'
 back_manifest=(back_target if back_target.is_dir() else back_target.parent)/'manifest.json'
 if back_manifest.exists():
  bm=read(back_manifest);back_source=bm.get('sourceSHA256',bm.get('model_sha256'))
  assert back_source==expected,'Return page belongs to another source'
gallery_url=a.gallery_url
viewer_source=None
if viewer_url:
 viewer_target=local_target(dst,viewer_url);assert viewer_target.exists(),'Viewer target missing'
 viewer_index=viewer_target/'index.html' if viewer_target.is_dir() else viewer_target
 viewer_base=viewer_index.parent
 base_match=re.search(r'<base\s+href=[\"\']([^\"\']+)',viewer_index.read_text('utf8'),re.I)
 if base_match:viewer_base=local_target(viewer_base,base_match.group(1))
 viewer_package=viewer_base/'assets/web-package.json'
 assert viewer_package.exists(),'Viewer source manifest missing'
 vm=read(viewer_package);viewer_source=vm.get('sourceSHA256',vm.get('model_sha256'))
 assert viewer_source==expected,'Viewer belongs to another source'

if gallery_url:
 gallery_target=local_target(dst,gallery_url);assert gallery_target.exists(),'Gallery target missing'
 gm=read((gallery_target if gallery_target.is_dir() else gallery_target.parent)/'manifest.json')
 assert gm.get('sourceSHA256',gm.get('model_sha256'))==expected,'Gallery belongs to another source'
assert not (a.preview and (viewer_url or gallery_url)),'Local preview has no project navigation; prevents linking an unrelated revision'

# Re-emission may replace the same managed sheet names, but must not leave stale
# managed SVG/DXF assets when changing sets. Report this before writing anything.
expected_drawings={s[k] for s in sheets for k in ('svg','dxf')}
if dst.exists():
 stale=[q.name for q in dst.iterdir() if q.is_file() and re.fullmatch(r'[AD]\d+[a-z]?\.(svg|dxf)',q.name) and q.name not in expected_drawings]
 assert not stale,'Destination contains stale managed sheets; use an isolated destination: '+str(stale)

dst.mkdir(parents=True,exist_ok=True)
pdfname='Casa_de_Campo_Planos_A2.pdf';zipname='Casa_de_Campo_Planos_Editables.zip'
shutil.copy2(source_pdf,dst/pdfname)
for s in sheets:
 for kind in ('svg','dxf'):shutil.copy2(emission_path(s,kind),dst/s[kind])
for name in ('anclajes_medidos.json','fuentes.md'):shutil.copy2(src/'details'/name,dst/name)
for name in extra_files:
 (dst/name).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src/name,dst/name)
for source_name,dest_name in [('manifest.json','emission_manifest.json'),('details/manifest.json','details_manifest.json'),('package_manifest.json','source_package_manifest.json')]:
 shutil.copy2(src/source_name,dst/dest_name)
extra_files+=['emission_manifest.json','details_manifest.json','source_package_manifest.json']

# All thumbnail pixels come from the exact complete vector PDF, using CPU only.
thumbs=[];(dst/'thumbs').mkdir(exist_ok=True)
with pymupdf.open(source_pdf) as book:
 for i,(pg,s) in enumerate(zip(book,sheets)):
  name='thumbs/'+s['id']+'.png';pix=pg.get_pixmap(matrix=pymupdf.Matrix(1000/pg.rect.width,1000/pg.rect.width),alpha=False)
  pix.save(dst/name);s['thumbnail']=name;s['pdf_page']=i+1
  thumbs.append({'sheet':s['id'],'path':name,'pdf_page':i+1,'width':pix.width,'height':pix.height,'source_pdf_sha256':sha(source_pdf),'sha256':sha(dst/name)})
write('thumbnail_manifest.json',{'model_sha256':expected,'source_pdf_sha256':sha(source_pdf),'renderer':'PyMuPDF CPU from complete PDF','thumbnails':thumbs})
write('cad_publication_check.json',{'status':'PASS','model_sha256':expected,'units':'metres','dimensions':len(cad_records),'tolerance_m':1e-6,'records':cad_records})
pool_note=('A08: playa humeda -0,080 m y agua -0,030 m, profundidad actual 50 mm. Volumen de agua recortado contra los acabados reales; fondo -1,390 m.' if r7 else 'A08: playa humeda -0,080 m y agua -0,030 m, profundidad actual 50 mm. El volumen invade114 mm del fondo de hormigon; coordinacion pendiente.')
coordination=('R8 incorpora apoyo y uso del MIDI y reserva de rodillas de isla. D13/D14 distinguen geometria G y cuerpos de prueba P. ' if r8 else '')+('Encuentros humedos y ventilacion propuestos; su geometria no acredita prestaciones ni capacidad.' if r7 else pool_note)
validation={'status':'PASS_DOCUMENTAL','review_status':status,'model':model_name,'model_sha256':expected,'pdf':pdfname,'checks':checks,'general':read(src/'print_validation.json'),'details':read(src/'details/validation.json'),'pending_preview_evidence':pending,'limits':['Documentary checks do not certify structural, hydraulic, acoustic, weather or statutory performance.',f'No approval at{a.review_threshold}/10 is claimed.',pool_note]}
write('print_validation.json',validation)
write('package_validation.json',dict(checks,model_sha256=expected,review_status=status))
write('verification.json',{'model_sha256':expected,'review_status':status,'combined':checks,'general':read(src/'verification.json'),'details':read(src/'details/validation.json')})
measurements=read(src/'measurements.json');measurements.update(model_sha256=expected,detail_dimensions=details['dimensions'],detail_measurements=details['measurements'],proposal_register=details['proposal_register']);write('measurements.json',measurements)
readme=f'''# Casa de Campo - planos {revision}

{status}. Virrey del Pino, Partido de La Matanza, Buenos Aires.

{count} laminas A2 ({len(general['sheets'])} generales + {len(details['sheets'])} detalles), PDF vectorial, {count} SVG, {count} DXF, {count} miniaturas y {checks['native_dxf_dimensions']} cotas DXF nativas. Imprimir PDF/SVG a100 %, A2 de594 x420 mm, sin ajustar. DXF en metros.

G: geometria medida. F: referencia de fuente. P: propuesta dimensional sujeta a proyecto y validacion. Norte orientativo segun propietario, servicios disponibles y acometidas por confirmar. No es un proyecto ejecutivo aprobado.

{coordination}

{pool_note}

Modelo: {model_name}
SHA256: {expected}
PDF: {pdfname}
ZIP: {zipname}

Validacion real de bytes del paquete de origen, PDF, SVG, ZIP y todas las cotas CAD. Ver manifest.json, dimension_register.csv y cad_publication_check.json.
'''
if pending:readme+='\nPrueba local: evidencia pendiente antes de publicar: '+', '.join(pending)+'.\n'
(dst/'README.md').write_text(readme,'utf8')
css=(ROOT/'scripts/planos95_publication.css').read_text('utf8')
viewer_nav=f'<a href="{html.escape(viewer_url)}">Volver al modelo 3D {html.escape(revision)} &#8599;</a>' if viewer_url else ('<span class="pending">Prueba local de planos</span>' if a.preview else f'<span class="pending">Visor {html.escape(revision)} en preparacion</span>')
if back_url:viewer_nav=f'<a href="{html.escape(back_url)}">Volver al avance {html.escape(revision)} &#8599;</a>'+viewer_nav
gallery_nav=f'<a href="{html.escape(gallery_url)}">Galeria {html.escape(revision)} &#8599;</a>' if gallery_url else '<span class="pending">Galeria en preparacion</span>'

def card(s):
 sid=html.escape(s['id']);title=html.escape(s['title']);svg=html.escape(s['svg']);dxf=html.escape(s['dxf']);thumb=html.escape(s['thumbnail'])
 return f'<article><a class="sheet" href="{svg}" target="_blank"><img loading="lazy" width="1000" height="708" src="{thumb}" alt="{sid} - {title}"></a><div class="caption"><h2>{sid} - {title}</h2><nav aria-label="Descargas {sid}"><a href="{svg}" download>SVG &#8595;</a><a href="{dxf}" download>DXF &#8595;</a></nav></div></article>'
extra_links=''
for fname,label in [('visual_review.json','Revision visual'),('ACCESO_MANTENIMIENTO_D08.md','Mantenimiento D08'),('use_evidence/use_validation.json','Pruebas de uso R8')]:
 if fname in extra_files:extra_links+=f' &middot; <a href="{fname}">{label}</a>'
preview_note='<br><strong>Prueba local del generador; fuente de ensayo. No es la emision final.</strong>' if a.preview else ''
page=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#183638"><link rel="icon" href="data:,"><title>Planos {revision} - Casa de Campo /42</title><style>{css}</style></head><body><header><strong>42 / CASA DE CAMPO</strong><nav class="site-nav" aria-label="Navegacion del proyecto">{viewer_nav}{gallery_nav}</nav></header><main><div class="intro"><span class="eyebrow">Virrey del Pino &middot; Partido de La Matanza &middot; Buenos Aires</span><h1>La propiedad, en planos.</h1><p>{count} laminas A2 de la revision {revision}: implantacion, plantas, fachadas, cortes, cocinas, banos y detalles. Incluyen cotas del modelo, huellas de uso y propuestas de encuentros constructivos, acustica y servicios.</p><div class="downloads"><a class="button primary" href="{pdfname}" target="_blank">Abrir las {count} laminas en PDF &#8599;</a><a class="button" href="{zipname}" download>Descargar PDF + {count} SVG + {count} DXF &#8595;</a></div></div><div class="note"><strong>En revision &middot; {revision} &middot; sin aprobacion de {threshold}/10.</strong> Geometria medida G, referencias de fuente F y propuestas P. La capacidad resistente, las instalaciones y el desempeno de los sistemas requieren proyecto y validacion. No es un proyecto ejecutivo aprobado para construccion.{preview_note}<br><strong>Pileta:</strong> {html.escape(pool_note)}</div><h2 class="group-title">Planos generales &middot; {len(general['sheets'])} laminas</h2><div class="grid">{''.join(card(s) for s in general['sheets'])}</div><h2 class="group-title">Detalles &middot; {len(details['sheets'])} laminas</h2><div class="grid">{''.join(card(s) for s in details['sheets'])}</div><footer>PDF/SVG: A2 (594 &times;420 mm),100 %, sin ajustar. DXF: metros; {checks['native_dxf_dimensions']} cotas nativas.<br>Norte orientativo segun propietario. Servicios disponibles; acometidas por confirmar.<br><a href="manifest.json">Version y trazabilidad</a> &middot; <a href="print_validation.json">Validacion documental</a> &middot; <a href="dimension_register.csv">Registro de cotas CSV</a> &middot; <a href="dimensional_audit.json">Auditoria dimensional</a>{extra_links}<br>Modelo {revision} &middot; SHA256 <code>{expected}</code></footer></main></body></html>'''
for old,new in {'laminas':'láminas','revision':'revisión','implantacion':'implantación','banos':'baños','acustica':'acústica','aprobacion':'aprobación','Geometria':'Geometría','geometria':'geometría','desempeno':'desempeño','validacion':'validación','Validacion':'Validación','construccion':'construcción','emision':'emisión','humeda':'húmeda','Galeria':'Galería','preparacion':'preparación','Version':'Versión','Auditoria':'Auditoría','Navegacion':'Navegación','segun':'según'}.items():
 page=re.sub(r'\b'+old+r'\b',new,page)
(dst/'index.html').write_text(page,'utf8')
assetnames=[pdfname]+[s[k] for s in sheets for k in ('svg','dxf','thumbnail')]+['index.html','README.md','measurements.json','verification.json','print_validation.json','package_validation.json','anclajes_medidos.json','fuentes.md','thumbnail_manifest.json','cad_publication_check.json']+extra_files
assert len(set(assetnames))==len(assetnames)
manifest={'project':'Casa de Campo','place':'Virrey del Pino, Partido de La Matanza, Buenos Aires','status':status,'revision':revision,'preview':a.preview,'model':model_name,'model_sha256':expected,'source_sha256':general['source_sha256'],'created_utc':general['created_utc'],'pdf':pdfname,'zip':zipname,'paper_mm':[594,420],'dxf_units':'metres','pages':count,'sheets':sheets,'checks':checks,'legend':{'F':'Referencia de fuente','G':'Geometria medida','P':'Propuesta dimensional'},'sources':details['sources'],'coordination_status':coordination,'navigation':{'back':back_url,'back_model_sha256':back_source,'viewer':viewer_url,'viewer_model_sha256':viewer_source,'gallery':gallery_url,'gallery_status':'available' if gallery_url else 'in preparation'},'dimensional_audit':{'path':'dimensional_audit.json','critical_measures':len(audit['measured_items']),'status':audit['status']},'source_package':{'manifest_sha256':sha(src/'package_manifest.json'),'zip_sha256':sha(source_zip),'files_checked':len(source_entries)},'pending_preview_evidence':pending,'files':[{'path':name,'bytes':(dst/name).stat().st_size,'sha256':sha(dst/name)} for name in assetnames]}
write('manifest.json',manifest)
with zipfile.ZipFile(dst/zipname,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name in assetnames+['manifest.json']:z.write(dst/name,name)
links=re.findall(r'(?:href|src)="([^"]+)"',page)
missing=[name for name in links if not name.startswith(('data:','http:','https:','#')) and not local_target(dst,html.unescape(name)).exists()]
assert not missing,missing
with zipfile.ZipFile(dst/zipname) as z:
 assert z.testzip() is None
 assert len([n for n in z.namelist() if n.endswith('.svg')])==count
 assert len([n for n in z.namelist() if n.endswith('.dxf')])==count
 assert len([n for n in z.namelist() if n.startswith('thumbs/') and n.endswith('.png')])==count
 for name in assetnames+['manifest.json']:assert z.read(name)==(dst/name).read_bytes(),'Published ZIP mismatch '+name
assert sha(model)==expected,'Source changed during publication'
assert all(sha(dst/f['path'])==f['sha256'] and (dst/f['path']).stat().st_size==f['bytes'] for f in manifest['files'])
report={'status':'PASS','model_sha256':expected,'review_status':status,'preview':a.preview,'pages':count,'svg_files':count,'dxf_files':count,'thumbnail_files':count,'native_dxf_dimensions':len(cad_records),'gallery_cards':page.count('<article>'),'unresolved_links':missing,'pdf_identical_to_emission':sha(dst/pdfname)==sha(source_pdf),'pdf_sha256':sha(dst/pdfname),'zip_sha256':sha(dst/zipname),'zip_bytes':(dst/zipname).stat().st_size,'model_unchanged':True,'source_package_files_checked':len(source_entries),'source_zip_bytes_match':True,'every_cad_value_matches':True,'source_checks':checks,'navigation':manifest['navigation'],'manifest_bytes_match':True,'pending_preview_evidence':pending}
write('publication_validation.json',report)
print(json.dumps(report,ensure_ascii=False,indent=2))
