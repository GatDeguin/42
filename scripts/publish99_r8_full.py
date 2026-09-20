"""Publish the complete R8 site from its existing frozen source; no new audit or model edits."""
from pathlib import Path
import hashlib,json,shutil,subprocess,argparse
R=Path(__file__).resolve().parents[1];SHA='60810e1945f53b339c070c6e77635f408b99c244fc07f43a5084ebeecdde5329'
A=argparse.ArgumentParser();A.add_argument('--prepare-model',action='store_true');a=A.parse_args()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
write=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assets=R/'docs/preview99/assets';info=read(assets/'model-info.json');package=read(assets/'web-package.json');optics=read(assets/'optics.json')
assert all(s==SHA for s in [info['stats']['source_sha256'],package['sourceSHA256'],optics['sourceSHA256']])
assert hashfile(R/'output/Casa_de_Campo_99_R8.blend')==SHA
info['revision']='R8';info['downloads']={'blender':'https://media.githubusercontent.com/media/GatDeguin/42/main/output/Casa_de_Campo_99_R8.blend','glb':'https://media.githubusercontent.com/media/GatDeguin/42/main/output/Casa_de_Campo_99_R8.glb'}
info['publication']={'revision':'R8','sourceSHA256':SHA,'architecturalReview':'No new review: owner requested direct full publication','videoRendered':False}
info['gi']={'enabled':False,'reason':'Raster PBR navigation and optional progressive light transport; static irradiance atlases not included in this runtime.'}
assert len(info['doors'])==13
assert next(v for v in info['viewerViews'] if v['key']=='pileta')['camera']=='LUZ99 | Pileta desde jardin'
write(assets/'model-info.json',info)
optics['water']['bumpDistanceRatio']=.008/.036
optics['water']['surfaceOpticsNote']='R8 source bump distance8mm, strength0.23. Runtime analytical ripple is scaled relative to previous36mm distance; not a geometry deformation.'
write(assets/'optics.json',optics)
shutil.copyfile(assets/'house.glb',R/'output/Casa_de_Campo_99_R8.glb')
if a.prepare_model:print('R8_MODEL_READY',package['totalBytes']);raise SystemExit(0)
gallery=read(R/'docs/renders99/manifest.json');plans=read(R/'docs/avance-r8/planos/manifest.json')
assert gallery['sourceSHA256']==SHA and len(gallery['images'])==26
assert plans['model_sha256']==SHA and plans['pages']==35
assert plans['navigation']['viewer_model_sha256']==SHA
assert plans['navigation']['gallery_status']=='available'
page=R/'docs/avance-r8/index.html';text=page.read_text('utf8')
text=text.replace('Avance R8 · Casa de campo','R8 · Casa de campo').replace('R8 / avance integrado en revisión','R8 / versión publicada').replace('Más detalle, con medidas comprobables.','La propiedad completa, en R8.')
intro=text.index('<p><strong>R8 todavía no tiene una calificación integral.')
intro_end=text.index('</p>',intro)+4
text=text[:intro]+'<p>El modelo interactivo, las imágenes y los planos corresponden a la misma fuente R8. Explora todos los ambientes y descarga los archivos completos.</p>'+text[intro_end:]
start=text.index('<div class="grid">');end=text.index('<h2>Cuatro vistas del modelo R8</h2>',start)
text=text[:start]+'''<div class="details"><strong>El visor interactivo ya utiliza R8.</strong><p>Explora el modelo completo, sus 13 puertas, cubiertas, cortes y ambientes. El Blender, el GLB, las 26 imágenes y los 35 planos corresponden a la misma fuente.</p><p><a class="button" href="../">Abrir el modelo R8 ↗</a> <a class="button" href="../renders99/">Ver las 26 imágenes ↗</a> <a class="button" href="planos/">Abrir los 35 planos ↗</a></p><p>Publicación directa solicitada por el propietario; no incorpora una nueva calificación arquitectónica. Video pausado.</p></div>'''+text[end:]
text=text.replace('Cuatro vistas del modelo R8','Selección de la galería R8').replace('Imagen de avance sin aprobación fotográfica.','Imagen calculada desde el modelo R8.').replace('Estas cuatro imágenes y el Blender descargable corresponden a R8.','Estas imágenes y el modelo descargable corresponden a R8.')
page.write_text(text,'utf8')
p=R/'docs/avance-r8/manifest.json';m=read(p);m.update(status='COMPLETE_R8_SITE_PUBLISHED_WITHOUT_NEW_REVIEW',viewerRevision='R8',galleryImages=26,plans=35,fullGallery='../renders99/',viewer='../');write(p,m)
p=R/'docs/avance-r7/index.html';s=p.read_text('utf8').replace('Abrir el modelo interactivo R7D','Abrir el modelo interactivo actual R8').replace('href="../renders99/"','href="../renders-r7d/"');p.write_text(s,'utf8')
(R/'docs/preview99/README.md').write_text('''# Visor R8

Fuente: `Casa_de_Campo_99_R8.blend`, SHA256 `'''+SHA+'''`.

Modelo métrico completo, 13 puertas y correderas, selección de objetos, cubiertas, cortes y cámaras interiores/exteriores. La nueva cámara de pileta se sitúa en el jardín. Navegación PBR con luz progresiva opcional; no se reutilizan los atlas estáticos de versiones anteriores.

[26 imágenes de R8](../renders99/) · [35 planos R8](../avance-r8/planos/) · [Blender editable](https://media.githubusercontent.com/media/GatDeguin/42/main/output/Casa_de_Campo_99_R8.blend) · [GLB](https://media.githubusercontent.com/media/GatDeguin/42/main/output/Casa_de_Campo_99_R8.glb).

Publicación integral autorizada sin otra revisión arquitectónica. No se asigna una nota nueva. Los planos conservan sus referencias G/F/P y propuestas pendientes de cálculo profesional. Video pausado.
''','utf8')
(R/'README.md').write_text('''# Casa de campo · R8

**[Abrir el modelo interactivo R8](https://gatdeguin.github.io/42/)** · [26 imágenes](https://gatdeguin.github.io/42/renders99/) · [35 planos](https://gatdeguin.github.io/42/avance-r8/planos/).

[Blender editable](https://media.githubusercontent.com/media/GatDeguin/42/main/output/Casa_de_Campo_99_R8.blend) · [GLB](https://media.githubusercontent.com/media/GatDeguin/42/main/output/Casa_de_Campo_99_R8.glb) · [PDF A2](https://gatdeguin.github.io/42/avance-r8/planos/Casa_de_Campo_Planos_A2.pdf) · [PDF +SVG +DXF](https://gatdeguin.github.io/42/avance-r8/planos/Casa_de_Campo_Planos_Editables.zip).

Virrey del Pino, La Matanza, Buenos Aires. Lote 22 × 20 m y edificio 8 × 12 m; estudio con 3,20 m libres y vivienda con 2,60 m. Dormitorio con puerta al estar; vestidor sólo entre baño y dormitorio. Baño del monoambiente junto a la fachada y medianera. Barra del quincho paralela a la parrilla, comedor hacia el jardín y cama orientada según el propietario.

R8 integra herrajes sanitarios corregidos, apoyo del MIDI con teclas a 750 mm, isla con 400 mm para rodillas, espejos, textiles, huerta y césped. El visor carga esta fuente completa, con 13 puertas, cámaras, cortes, cubiertas y selección métrica. Las 26 imágenes Cycles y los 35 planos comparten la misma fuente. 226 cotas CAD nativas y 49 medidas críticas identificadas.

SHA256 del Blender: `'''+SHA+'''`.

La publicación completa fue solicitada sin una nueva revisión. La última calificación independiente, 8,5/10, pertenece a [R7D](audit/critica_integral_r7d_99.md); no se transfiere a R8. Los planos distinguen geometría medida G, referencias F y propuestas P. **Video pausado hasta autorización explícita.**

## Archivos y reproducción

[HTML original](source/original.html) · [Encargo](source/request.txt) · [Notas del visor](docs/preview99/README.md) · [Generación de planos](scripts/PLANOS_R8.md).

Blender 5.2/Cycles; visor Three.js con recursos locales. Los archivos Blender y GLB de salida usan Git LFS: después de clonar, ejecutar `git lfs pull`. Geometría y texturas web se publican como recursos separados; cada versión identifica su fuente.

Recursos CC0 de Poly Haven: Belfast Sunset, Tree Small 02, Oak Veneer 01, Red Bricks 04, Terlenka y Grass Bermuda 01. Procedencia y huellas en source/assets y source/photographic99_grass_r8.

[Galería R7D archivada](https://gatdeguin.github.io/42/renders-r7d/) · [Planos R7D archivados](https://gatdeguin.github.io/42/planos99/) · [Versión R6K](https://gatdeguin.github.io/42/preview95/).
''','utf8')
release={'revision':'R8','sourceSHA256':SHA,'web':package['files'],'standaloneGLB':{'path':'output/Casa_de_Campo_99_R8.glb','bytes':(R/'output/Casa_de_Campo_99_R8.glb').stat().st_size,'sha256':hashfile(R/'output/Casa_de_Campo_99_R8.glb')},'stills':26,'plans':35,'doors':13,'newArchitecturalReview':False,'videoRendered':False}
write(R/'review99/r8_final/release.json',release);print('R8_FULL_SITE_READY',len(package['files']))
