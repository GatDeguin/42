"""Publish a source-identified R8 progress page without replacing the R7D viewer."""
from pathlib import Path
import json, hashlib, html, shutil
from PIL import Image
R=Path(__file__).resolve().parents[1]
OUT=R/'review99/github_r8_progress';OUT.mkdir(parents=True,exist_ok=True)
PAGE=R/'docs/avance-r8';PAGE.mkdir(parents=True,exist_ok=True)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
integ=read(R/'review99/r8_integrated/integration_manifest.json');model=Path(integ['output']);sourceSHA=sha(model)
assert sourceSHA==integ['outputSHA256'] and integ['idempotent'] and integ['tourVerified']
geometry=read(R/'review99/r8_integrated/frozen_geometry_checks.json')
assert geometry['sourceSHA256']==sourceSHA and geometry['passed']
stills=R/'review99/r8_checkpoint/stills';m=read(stills/'manifest.json')
assert m['sourceSHA256']==sourceSHA and len(m['images'])==4
keys={'estudio','dormitorio','huerta','pileta_jardin'};assert {q['key'] for q in m['images']}==keys
images=[]
for q in m['images']:
 p=stills/q['file'];assert sha(p)==q['sha256'];im=Image.open(p);assert list(im.size)==q['pixels'];dst=PAGE/(q['key']+'.jpg');im.convert('RGB').save(dst,quality=94,subsampling=0,optimize=True)
 images.append(dict(q,publicFile=dst.name,publicSHA256=sha(dst),sourcePNG=str(p.relative_to(R))))
planfile=PAGE/'planos/index.html';plantext=('<a class="button" href="planos/">Ver los 35 planos R8 ↗</a>' if planfile.exists() else '<a href="../planos99/">Consultar los 33 planos publicados de R7D ↗</a>')
if planfile.exists():
 pm=read(PAGE/'planos/manifest.json');assert pm['model_sha256']==sourceSHA
css=(R/'docs/avance-r7/index.html').read_text('utf8').split('<style>',1)[1].split('</style>',1)[0]
figures=''.join('<figure><img src="'+q['publicFile']+'" width="'+str(q['pixels'][0])+'" height="'+str(q['pixels'][1])+'" loading="lazy" alt="'+html.escape(q['title'])+'"><figcaption>'+html.escape(q['title'])+' · Cycles, fuente R8. Imagen de avance sin aprobación fotográfica.</figcaption></figure>' for q in images)
text="""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#213b34"><title>Avance R8 · Casa de campo</title><link rel="icon" href="data:,"><style>{css}</style></head><body><header><a href="../">42 / CASA DE CAMPO</a><a href="https://github.com/GatDeguin/42">Proyecto en GitHub ↗</a></header><main><p class="label">Virrey del Pino · Cedro Misionero</p><span class="status">R8 / avance integrado en revisión</span><h1>Más detalle, con medidas comprobables.</h1><p class="lead">Herrajes sanitarios corregidos, apoyos para el teclado del estudio, espacio para las rodillas en la isla y mejoras de textiles, espejos y jardín.</p><p><strong>R8 todavía no tiene una calificación integral.</strong> El objetivo es 9,9/10 e hiperrealismo fotográfico. La última auditoría independiente corresponde a R7D y dio <strong>8,5/10</strong>.</p><p><a class="button" href="https://media.githubusercontent.com/media/GatDeguin/42/main/output/Casa_de_Campo_99_R8.blend">Descargar Blender R8 ↓</a> · {plantext}</p><div class="grid"><section><h2>Incorporado en R8</h2><ul><li>Sanitarios con ejes, apoyos, retención y topes revisados.</li><li>Teclado MIDI con teclas a 750 mm, apoyos físicos y 665 mm libres inferiores.</li><li>Isla del monoambiente con 400 mm de profundidad libre para rodillas.</li><li>Espejos con normales ópticas corregidas; roble y telas a escala.</li><li>Manta y almohadas con nuevas formas, prendas con volumen y hojas de huerta más suaves.</li><li>Césped de recurso fotográfico, cobertura continua y nueva vista de la pileta desde el jardín.</li></ul></section><section><h2>En revisión</h2><ul><li>Comprobación integral de arquitectura y realismo por el crítico independiente.</li><li>Iluminación de los ocho sectores del visor y comparación con Cycles.</li><li>Rendimiento, navegación y exportación del modelo R8 para la web.</li><li>Selección y cálculo profesional de herrajes, apoyos y soluciones propuestas.</li></ul></section></div><div class="details"><strong>El visor interactivo sigue mostrando R7D.</strong><p>Estas cuatro imágenes y el Blender descargable corresponden a R8. El <a href="../">visor</a>, la <a href="../renders99/">galería de 25 imágenes</a> y los <a href="../planos99/">33 planos R7D</a> conservan su fuente identificada mientras se verifica el nuevo conjunto.</p><p><a href="https://github.com/GatDeguin/42/blob/main/audit/r8_three_passes.md">Estado de las tres pasadas correctivas ↗</a> · <a href="https://github.com/GatDeguin/42/blob/main/audit/critica_integral_r7d_99.md">Auditoría independiente R7D ↗</a></p><p><strong>Video pausado hasta autorización explícita.</strong></p></div><h2>Cuatro vistas del modelo R8</h2>{figures}<div class="details"><strong>Fuente de esta publicación</strong><p>Casa_de_Campo_99_R8.blend<br><code>{sourceSHA}</code></p><p><a href="manifest.json">Identificación y huellas de las imágenes ↗</a> · <a href="https://github.com/GatDeguin/42/blob/main/review99/github_r8_progress/README.md">Alcance y comprobaciones ↗</a></p></div></main><footer>Estudio arquitectónico en revisión. Las propuestas no constituyen cálculo ni documentación ejecutiva habilitada.</footer></body></html>
""".format(css=css,plantext=plantext,figures=figures,sourceSHA=sourceSHA)
(PAGE/'index.html').write_text(text,encoding='utf8')
public=dict(revision='R8',status='ADVANCE_PENDING_GLOBAL_REVIEW',sourceSHA256=sourceSHA,sourceFile=model.name,lastFormalReview=dict(revision='R7D',score=8.5,target=9.9),viewerRevision='R7D',images=images,videoRendered=False)
(PAGE/'manifest.json').write_text(json.dumps(public,ensure_ascii=False,indent=2),encoding='utf8')
for rel in ['docs/index.html','docs/preview99/index.html']:
 p=R/rel;s=p.read_text('utf8');old='<a class="source-link" href="../avance-r7/">Estado de R7D y primeras imágenes ↗</a>';new='<a class="source-link" href="../avance-r8/">Avance R8 · modelo, imágenes y correcciones ↗</a>'
 assert old in s or new in s;s=s.replace(old,new);p.write_text(s,'utf8')
p=R/'docs/avance-r7/index.html';s=p.read_text('utf8');new='<p><a class="button" href="../avance-r8/">Ver el nuevo avance R8 ↗</a></p>'
if new not in s:s=s.replace('<h1>',new+'<h1>',1);p.write_text(s,'utf8')
p=R/'README.md';s=p.read_text('utf8');marker='## Avance integrado R8'
latest='**Último avance: [R8 · modelo, cuatro imágenes y35 planos](https://gatdeguin.github.io/42/avance-r8/)**. Pendiente de auditoría integral.\n\n'
if latest not in s:s=s.replace('\n\n','\n\n'+latest,1)
if marker not in s:
 at=s.index('## Entrega publicada R6K');s=s[:at]+"""## Avance integrado R8

**[Ver las cuatro imágenes nuevas y el estado de R8](https://gatdeguin.github.io/42/avance-r8/)** · [Descargar Blender R8](https://media.githubusercontent.com/media/GatDeguin/42/main/output/Casa_de_Campo_99_R8.blend).

R8 integra las correcciones de herrajes sanitarios, apoyos del MIDI y rodillas bajo la isla, junto con mejoras de espejo, textiles, vegetación y agua. Las imágenes de avance se calculan desde el mismo archivo integrado. **R8 todavía no tiene nota integral; 8,5/10 sigue correspondiendo a R7D.** El visor principal permanece en R7D mientras se comprueba la exportación y la iluminación web de R8.

[Alcance, SHA y controles de R8](review99/github_r8_progress/README.md) · [Tres pasadas correctivas](audit/r8_three_passes.md). Video pausado.

"""+s[at:]
p.write_text(s,'utf8')
(OUT/'README.md').write_text('# Avance integrado R8\n\nFuente: `'+model.name+'`, SHA256 `'+sourceSHA+'`.\n\nCuatro imágenes Cycles se calcularon desde esa fuente, sin guardar ni alterar el modelo. El registro de imágenes conserva cámara, resolución, muestras y SHA del PNG; `docs/avance-r8/manifest.json` identifica también los JPEG públicos.\n\nLa prueba geométrica sobre esta misma fuente comprueba agua, alturas, escalera, accesos, escala, recursos empaquetados y sincronización de escenas. Las pruebas de componente se distinguen de las regresiones integradas y no implican aprobación arquitectónica.\n\nLa auditoría integral vigente es R7D: 8,5/10. R8 no tiene nueva nota; objetivo 9,9. El visor R7D continúa publicado; R8 es una descarga Blender y una página de avance hasta cerrar exportación e iluminación. Video pausado.\n\n- [Integración](../r8_integrated/integration_manifest.json)\n- [Geometría integrada](../r8_integrated/frozen_geometry_checks.json)\n- [Estado de las tres pasadas](../../audit/r8_three_passes.md)\n',encoding='utf8')
print(json.dumps(dict(sourceSHA256=sourceSHA,images=len(images),page=str(PAGE/'index.html')),indent=2))
