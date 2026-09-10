# Visor web de Casa de Campo

Candidata R6K en revisión; aprobación 9,5 pendiente. GitHub Pages publica main:/docs. Sin servidor de aplicación ni CDN. [Documentación y límites](../docs/preview95/README.md).

Fuente actual: output/Casa_de_Campo_95_R6K.blend, SHA-256 a3663a5081dac391303f25b8e9994b1a412a008e971642af29fc2cbee849aa90; GLB 97.1 MiB. El paquete conserva 13 mecanismos de puerta, escala métrica y cámaras de la fuente. La selección muestra dimensiones envolventes; no cotas libres. Vídeo pausado.

## Desarrollo

Desde la raíz: npm ci --prefix web-tools. Servir docs por HTTP, por ejemplo python -m http.server 8420 --bind 127.0.0.1 --directory docs. Abrir http://127.0.0.1:8420/.

## Exportación y QA

Con Git LFS, Blender 5.2 y Node:

    git lfs pull
    blender -b output/Casa_de_Campo_95_R6K.blend --python scripts/web95_optics_export.py -- --candidate
    node web-tools/photographic95-optimize.mjs
    node web-tools/photographic95-assets-verify.mjs
    node web-tools/photographic95-dimensions-verify.mjs
    node web-tools/photographic95-final-qa.mjs

Exportación sólo en memoria: no altera el Blender. Conserva UV0/PBR y reduce botánica por componentes completos. Meshopt con posiciones de 16 bits; el control de escala decodifica atributos normalizados y compara envolventes con Blender.

photographic95-build.mjs reconstruye el prototipo aislado y photographic95-promotion.mjs prepara la portada con base ./preview95/. La promoción a docs/index.html reutiliza el mismo GLB. photographic95-documentation.mjs y photographic95-publication.mjs se ejecutan sólo tras QA final del mismo SHA. La lista publication-files.json evita incorporar ensayos históricos.

photographic95-qa.mjs mide también el trazador optativo; puede bloquear durante su preparación. photographic95-final-qa.mjs verifica la navegación raster predeterminada, 13 puertas, selección, órbita, corte y emulación móvil. PHOTO95_URL permite probar otra URL. No representa una prueba de teléfono físico.

## GI experimental

No se publica GI como parte de esta candidata: el ensayo previo pertenece a otro SHA. Se conserva como prueba histórica fuera del paquete web; GTAO aporta contacto local y no equivale a iluminación global.

Para regenerar: misma fuente con docs/preview95/gi/bake.py, después gi/denoise.py y photographic95-gi-uv.mjs / photographic95-gi-qa.mjs. No se promete GI completa de la vivienda.

Los antiguos optimize.mjs/export_web_model.py y sus reportes pertenecen al visor anterior; no regeneran R6K completo. Ensayos Pass3b (SHA fd477337c188777079fc9fa5f630958edb077f655237074cd189aa3e698266af, 12 puertas) y Pass3d (GI) se conservan como historia identificada, fuera de la lista publicada.
