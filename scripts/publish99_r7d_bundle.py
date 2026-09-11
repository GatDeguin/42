"""Connect the 25 stills and 33 plans to their already-published R7D source."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'docs';O=R/'review99/r7d_bundle';O.mkdir(parents=True,exist_ok=True)
SHA='9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e'
def read(p):return p.read_text(encoding='utf-8-sig')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
g=json.loads(read(D/'renders99/manifest.json'));p=json.loads(read(D/'planos99/manifest.json'));v=json.loads(read(D/'planos99/publication_validation.json'));q=json.loads(read(R/'review99/r7d_deliverables_qa/report.json'))
assert g['sourceSHA256']==p['model_sha256']==v['model_sha256']==q['sourceSHA256']==SHA
assert len(g['images'])==25 and v['pages']==33 and v['status']=='PASS' and q['passed']
for x in g['images']:assert digest(D/'renders99'/x['file'])==x['sha256']
assert digest(D/'planos99'/p['pdf'])==v['pdf_sha256'];assert digest(D/'planos99'/p['zip'])==v['zip_sha256']
for name in ['index.html','preview99/index.html']:
 f=D/name;s=read(f).replace('../planos/','../planos99/').replace('../renders/','../renders99/').replace('Planos R6K ↗','Planos R7D ↗').replace('Renders R6K ↗','Imágenes R7D ↗')
 s=s.replace('Las galerías de 19 imágenes y 33 planos enlazadas aún corresponden a R6K.','Las 25 imágenes y los 33 planos enlazados provienen de esta misma fuente R7D.');f.write_text(s,encoding='utf8')
f=D/'preview99/controles.html';s=read(f).replace('../planos/','../planos99/').replace('Consultar los planos R6K','Consultar los planos R7D');f.write_text(s,encoding='utf8')
f=D/'preview99/README.md';s=read(f).replace('y paquete completo de25imágenes/33planos pendiente. Los enlaces actuales a planos y galería se rotulanR6K.','y coordinación de mantenimiento. [25 imágenes](../renders99/) y [33 planos](../planos99/) ya disponibles desde esta fuente R7D.');f.write_text(s,encoding='utf8')
f=D/'avance-r7/index.html';s=read(f);s=s.replace('Juego completo de25imágenes y33planos R7D en elaboración.','Auditoría integral del conjunto y cierre de los problemas detectados.');s=s.replace('<h2>Primeras imágenes de esta misma fuente</h2>','<h2>25 imágenes y 33 planos de la misma fuente</h2><p><a class="button" href="../renders99/">Ver las25imágenes ↗</a> · <a class="button" href="../planos99/">Abrir los33planos ↗</a></p><p>Las cuatro vistas siguientes son una selección de la galería completa.</p>');s=s.replace('Las galerías anteriores siguen identificadas como R6K.','Archivo de la revisión anterior R6K.');f.write_text(s,encoding='utf8')
f=R/'README.md';s=read(f);s=s.replace('**[Estado e imágenes R7D](https://gatdeguin.github.io/42/avance-r7/)**','**[25 imágenes R7D](https://gatdeguin.github.io/42/renders99/)** · **[33 planos R7D](https://gatdeguin.github.io/42/planos99/)** · [Estado de revisión](https://gatdeguin.github.io/42/avance-r7/)');s=s.replace('La iluminación web por ambiente y el juego completo de25stills/33planos se están terminando desde el mismo SHA. El visor principal ahora muestraR7D; las [19imágenes anteriores](https://gatdeguin.github.io/42/renders/) y [33planos anteriores](https://gatdeguin.github.io/42/planos/) continúan rotuladosR6K.','La iluminación web por ambiente sigue pendiente. Ya están publicados el visor,25imágenes y33planos de R7D desde el mismo SHA. El PDF es vectorial y el ZIP incluye SVG/DXF con209cotas nativas. Las [19imágenes anteriores](https://gatdeguin.github.io/42/renders/) y [33planos anteriores](https://gatdeguin.github.io/42/planos/) se conservan como archivoR6K.');f.write_text(s,encoding='utf8')
infofile=D/'preview99/assets/model-info.json';info=json.loads(read(infofile));info['publication']['deliverables']={'images':25,'imagesURL':'../renders99/','sheets':33,'plansURL':'../planos99/','sourceSHA256':SHA};info['publication']['knownOpenItems']=['Photographic vegetation and textiles','Sanitary fixed/moving hinge interfaces','Mirror shading normals','MIDI controller height and supports','Comfort at the PB island','Final source-matched room lighting and progressive validation'];infofile.write_text(json.dumps(info,indent=2,ensure_ascii=False),encoding='utf8')
report=dict(revision='R7D',sourceSHA256=SHA,status='COMPLETE_DRAWINGS_AND_STILLS_IN_REVIEW_NOT_APPROVED',targetGlobalScore=9.9,globalScore=None,stills=dict(count=25,manifest='docs/renders99/manifest.json',sha256=digest(D/'renders99/manifest.json')),plans=dict(count=33,pdf='docs/planos99/'+p['pdf'],pdfSHA256=v['pdf_sha256'],zip='docs/planos99/'+p['zip'],zipSHA256=v['zip_sha256'],nativeDimensions=209),staticUI='review99/r7d_deliverables_qa/report.json',videoRendered=False)
audit_file=R/'audit/critica_integral_r7d_99_summary.json'
if audit_file.exists():
 audit=json.loads(read(audit_file));assert audit['sourceSHA256']==SHA
 report.update(globalScore=audit['globalScore'],approved=audit['approved'],audit='audit/critica_integral_r7d_99_summary.json',status='COMPLETE_DRAWINGS_AND_STILLS_REVIEWED_8_5_NOT_APPROVED')
(O/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print('R7D_FULL_DELIVERABLES_CONNECTED',SHA)
