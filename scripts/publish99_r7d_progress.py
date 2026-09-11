"""Publish the current integrated candidate honestly, preserving prior releases."""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image
R=Path(__file__).resolve().parents[1];D=R/'docs';A=D/'preview99/assets';O=R/'review99/github_r7d_progress';O.mkdir(parents=True,exist_ok=True)
SHA='9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e';source=R/'output/Casa_de_Campo_99_R7D.blend'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert digest(source)==SHA
checks={}
for name in ['frozen_geometry_checks','component_regressions']:
 p=R/'review99/r7d_integrated'/(name+'.json');r=json.loads(p.read_text(encoding='utf-8-sig'));assert r['sourceSHA256']==SHA and r['passed'];checks[name]=dict(path=p.relative_to(R).as_posix(),sha256=digest(p))
info=json.loads((A/'model-info.json').read_text(encoding='utf-8-sig'));package=json.loads((A/'web-package.json').read_text(encoding='utf-8-sig'));dims=json.loads((D/'preview99/dimension-verification.json').read_text(encoding='utf-8-sig'))
assert info['stats']['source_sha256']==package['sourceSHA256']==SHA
assert not package['geometryValidationPending'];assert dims.get('pass',dims.get('passed'))
blendurl='https://media.githubusercontent.com/media/GatDeguin/42/main/output/'+source.name
glb=R/'output/Casa_de_Campo_99_R7D.glb';shutil.copyfile(A/'house.glb',glb);assert digest(glb)==package['originalGLBSHA256']
glburl='https://media.githubusercontent.com/media/GatDeguin/42/main/output/'+glb.name
info['downloads']={'blender':blendurl,'glb':glburl};info['publication']={'revision':'R7D','status':'CANDIDATE_IN_REVIEW','targetGlobalScore':9.9,'globalScore':None,'lastFormalScore':{'revision':'R6K','score':8.3},'knownOpenItems':['Photographic vegetation and textiles','Sanitary hinge interfaces under independent review','Source-matched room lighting atlases in preparation','Full R7 still and drawing packages in preparation']}
(A/'model-info.json').write_text(json.dumps(info,indent=2,ensure_ascii=False),encoding='utf8')
p=R/'.gitattributes';s=p.read_text(encoding='utf-8-sig');rule='output/Casa_de_Campo_99_*.glb filter=lfs diff=lfs merge=lfs -text';p.write_text(s.rstrip()+'\n'+(rule+'\n' if rule not in s else ''),encoding='utf8')
p=D/'preview99/index.html';s=p.read_text(encoding='utf-8-sig');s=s.replace('R7 · en desarrollo','R7D · en revisión');s=s.replace('Prueba R7 en desarrollo. La auditoría exige 9,9 y realismo fotográfico. Modelo de trabajo sin aprobación final. Los planos y renders publicados corresponden a R6K hasta cerrar esta revisión.','R7D integrada, sin aprobación final. Objetivo 9,9 e hiperrealismo fotográfico. La mecánica sanitaria y el acabado fotográfico siguen bajo revisión. Las galerías de 19 imágenes y 33 planos enlazadas aún corresponden a R6K.');s=s.replace('>Planos ↗','>Planos R6K ↗').replace('>Renders ↗','>Renders R6K ↗');s=s.replace('<a class="source-link" href="./README.md"','<a class="source-link" href="../avance-r7/">Estado de R7D y primeras imágenes ↗</a>\n<a class="source-link" href="./README.md"');p.write_text(s,encoding='utf8')
root=s.replace('<meta charset="utf-8">','<meta charset="utf-8"><base href="./preview99/">',1);(D/'index.html').write_text(root,encoding='utf8')
p=D/'preview99/controles.html';s=p.read_text(encoding='utf-8-sig').replace('aprobación 9,5 pendiente','R7D · aprobación 9,9 pendiente').replace('./assets/house.glb',glburl).replace('Consultar los planos ↗','Consultar los planos R6K ↗');p.write_text(s,encoding='utf8')
readme=f'''# Visor R7D — candidata integrada en revisión

Fuente: `{source.name}`. SHA256: `{SHA}`.

[Blender editable con materiales empaquetados]({blendurl}) · [GLB autónomo]({glburl}).

Puerta directa dormitorio–estar; vestidor sólo comunica baño y dormitorio; baño PB junto a fachada y medianera. Alturas libres: estudio3,20m y vivienda2,60m. Revestimientos, ventilación y sanitarios integrados con controles geométricos, en auditoría independiente.

El visor conserva escala métrica,13puertas, cámaras corregidas y texturas. El paquete de recursos mantiene los píxeles de las imágenes y la geometría decodificada del GLB. La iluminación calculada por ambiente está en preparación; navegación raster y luz progresiva opcional no tienen aprobación fotográfica.

Objetivo global9,9/10. R7D todavía no tiene nota global. Última nota formalR6K:8,3. Reservas actuales: vegetación rígida, acabado fotográfico, interferencias de herrajes sanitarios y paquete completo de25imágenes/33planos pendiente. Los enlaces actuales a planos y galería se rotulanR6K.

Video pausado hasta autorización expresa. Esta revisión digital no es documentación ejecutiva habilitada ni certificación estructural o de instalaciones.
''';(D/'preview99/README.md').write_text(readme,encoding='utf8')
manifest=json.loads((R/'review99/r7_final/stills/manifest.json').read_text(encoding='utf-8-sig'));assert manifest['sourceSHA256']==SHA
shots=[]
for key in ['exterior','pileta','huerta','estudio']:
 row=next(x for x in manifest['images'] if x['key']==key);src=R/'review99/r7_final/stills'/row['file'];assert digest(src)==row['sha256'];dst=D/'avance-r7'/(key+'-r7d.jpg');im=Image.open(src);im.thumbnail((1600,1200));im.convert('RGB').save(dst,quality=91,optimize=True);shots.append(dict(**row,publicFile=dst.relative_to(D).as_posix(),publicSHA256=digest(dst)))
p=D/'avance-r7/index.html';old=p.read_text(encoding='utf-8-sig');head=old[:old.index('<body>')];figures=''.join(f'<figure><img src="{x["key"]}-r7d.jpg" alt="{x["title"]}" loading="lazy"><figcaption>{x["title"]} · Cycles, R7D. Imagen en revisión fotográfica.</figcaption></figure>' for x in shots)
p.write_text(head+f'''<body><header><a href="../">42 / CASA DE CAMPO</a><a href="https://github.com/GatDeguin/42">Proyecto en GitHub ↗</a></header><main><p class="label">Virrey del Pino · Cedro Misionero</p><span class="status">R7D / candidata integrada en revisión</span><h1>Recorre la distribución actualizada.</h1><p class="lead">El dormitorio tiene puerta propia al estar. El vestidor comunica sólo baño y dormitorio. El baño del monoambiente está junto a la fachada y la medianera.</p><p><a class="button" href="../">Abrir el modelo interactivo R7D ↗</a></p><p>Objetivo de la auditoría independiente: <strong>9,9/10 e hiperrealismo fotográfico</strong>. R7D aún no tiene nota global ni aprobación. Última evaluación integral de R6K:8,3/10.</p><div class="grid"><section><h2>Ya integrado</h2><ul><li>Distribución, manos de puertas y recorrido de control.</li><li>Agua de pileta ajustada al vaso.</li><li>Revestimientos húmedos y coordinación de ventilación.</li><li>Sanitarios y pavimentos con geometría y materiales revisados.</li><li>Visor métrico, texturas y cámaras exportados desde R7D.</li></ul></section><section><h2>Revisión abierta</h2><ul><li>El crítico detectó interferencias pequeñas en herrajes de sanitarios: se corregirán.</li><li>Vegetación todavía rígida y acabados que requieren mayor realismo.</li><li>Iluminación web calculada de los ocho sectores.</li><li>Juego completo de25imágenes y33planos R7D en elaboración.</li></ul></section></div><p><a class="button" href="{blendurl}">Descargar Blender R7D ↓</a> · <a href="{glburl}">Descargar GLB ↓</a></p><h2>Primeras imágenes de esta misma fuente</h2>{figures}<div class="details"><strong>Las galerías anteriores siguen identificadas como R6K.</strong><p>Consulta el <a href="../preview95/">visor R6K</a>, sus <a href="../renders/">19imágenes</a> y sus <a href="../planos/">33láminas</a> como documentación de esa revisión. No describen las últimas correcciones de R7D.</p><p><a href="https://github.com/GatDeguin/42/blob/main/review99/github_r7d_progress/README.md">Fuente, alcance y comprobaciones de esta publicación ↗</a></p><p><strong>Video pausado hasta autorización explícita.</strong></p></div></main><footer>Estudio arquitectónico en revisión. No constituye documentación ejecutiva habilitada ni cálculo profesional de estructura e instalaciones.</footer></body></html>''',encoding='utf8')
p=R/'README.md';old=p.read_text(encoding='utf-8-sig');tail=old[old.index('## Entrega publicada R6K'):];intro=f'''# Casa de campo · modelo y documentación arquitectónica

**[Explorar R7D en 3D](https://gatdeguin.github.io/42/)** · **[Estado e imágenes R7D](https://gatdeguin.github.io/42/avance-r7/)** · [Descargar Blender R7D]({blendurl}) · [Descargar GLB]({glburl}).

Reconstrucción editable en Virrey del Pino, La Matanza, Buenos Aires. **R7D es una candidata integrada en revisión; no tiene nota global ni aprobación.** El objetivo solicitado es9,9/10 e hiperrealismo fotográfico. Última auditoría formalR6K: **8,3/10**, sin aprobación.

R7D incorpora el baño PB junto a fachada/medianera, elimina la puerta vestidor–comedor y agrega dormitorio–estar. Integra revestimientos húmedos, ventilación y sanitarios revisados. Estudio3,20m libres; vivienda2,60m. Puertas, agua, alturas y encuentros tienen controles geométricos; la auditoría independiente aún debe cerrar el conjunto.

**Reservas conocidas:** el crítico detectó interferencias de herrajes sanitarios y las hojas de huerta siguen rígidas. La iluminación web por ambiente y el juego completo de25stills/33planos se están terminando desde el mismo SHA. El visor principal ahora muestraR7D; las [19imágenes anteriores](https://gatdeguin.github.io/42/renders/) y [33planos anteriores](https://gatdeguin.github.io/42/planos/) continúan rotuladosR6K.

[Controles y huellas de la publicación R7D](review99/github_r7d_progress/README.md) · [Protocolo independiente](audit/r7_review_requirements.md). **Video pausado hasta autorización explícita.**

''';p.write_text(intro+tail,encoding='utf8')
report=dict(revision='R7D',status='CANDIDATE_IN_REVIEW',targetGlobalScore=9.9,globalScore=None,source=source.relative_to(R).as_posix(),sourceSHA256=SHA,sourceBytes=source.stat().st_size,glb=glb.relative_to(R).as_posix(),glbSHA256=digest(glb),glbBytes=glb.stat().st_size,webEntrypoint='docs/preview99/assets/house.gltf',resourceManifestSHA256=digest(A/'web-package.json'),checks=checks,images=shots,videoRendered=False)
(O/'manifest.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8');(O/'README.md').write_text(readme+'\n\n[Manifiesto](manifest.json) · [Controles geométricos](../r7d_integrated/frozen_geometry_checks.json) · [Regresiones de componentes](../r7d_integrated/component_regressions.json).\n',encoding='utf8')
print('R7D_PROGRESS_READY',SHA,len(shots))
