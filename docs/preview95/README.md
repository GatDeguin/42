# Casa de campo · candidata R6K

**En revisión · aprobación 9,5 pendiente.** El visor mantiene la arquitectura 3D real y sus controles. No se generó vídeo.

## Fuente y descarga

[Modelo GLB](./assets/house.glb), 97.1 MiB. [Fuente Blender R6K](https://media.githubusercontent.com/media/GatDeguin/42/main/output/Casa_de_Campo_95_R6K.blend). SHA-256 de Blender: a3663a5081dac391303f25b8e9994b1a412a008e971642af29fc2cbee849aa90. [Galería de renders](../renders/) y [planos](../planos/).

El modelo, cámaras, luces y materiales se exportaron juntos desde esa fuente. [Ayuda de controles](./controles.html). El visor inicia en raster; las **13 puertas** se verificaron cerradas y abiertas. La selección informa envolventes de objetos, no dimensiones libres entre terminaciones.

## Imagen y materiales

HDR Belfast Sunset de la fuente, con orientación, intensidad y exposición exportadas. Three 0.180 usa AgX; no se afirma equivalencia exacta con Cycles. Las 33 luces mantienen posición, orientación, tamaño y energía relativa; raster utiliza las ocho áreas más cercanas, las puntuales y el sol. Las áreas raster no proyectan sombras propias, por lo que puede haber fugas de luz.

Roble fotográfico CC0 Oak Veneer 01, de Jenelle van Heerden; ladrillo Red Bricks04, de Rob Tuytel, calibrado en RGB lineal sin emisión; árbol Tree Small02, de Rico Cilliers. Mapas de 2K con albedo sRGB y normales/rugosidad lineales. Madera con UV0 métrica longitudinal y variación por pieza; ladrillo con módulo 2,5 m y fase mundial común. Procedencia y hashes en assets/oak-veneer-01, assets/red-bricks-04 y assets/tree-small-02-provenance.json.

Botánica: 70 posiciones y dos mallas compartidas; hojas completas, UV y alpha originales. Se conservan 20.000 componentes de hoja por árbol cercano y 4.000 en el fondo. El follaje reducido no equivale al render Blender.

Vidrio y agua usan transmisión física, metalicidad cero e IOR 1,52 y 1,333; los reflejos/transmisiones de raster siguen siendo aproximados. GTAO aporta contacto local. El trazado progresivo es optativo y requiere esperar acumulación y reconstrucción al abrir puertas; corte y selección utilizan raster.

## GI

No se publica GI como parte de esta candidata: el ensayo previo pertenece a otro SHA. Se conserva como prueba histórica fuera del paquete web; GTAO aporta contacto local y no equivale a iluminación global.

## Verificación de esta fuente

[QA de navegación](./final-verification.json): Chrome con ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Ti (0x00002489) Direct3D11 vs_5_0 ps_5_0, D3D11), escritorio 1440×1000 y emulación táctil 390×844. Carga inicial 21.29 s y mediana raster 16.7 ms/cuadro. Vistas, órbita, selección, corte, cubiertas, vegetación y 13 puertas verificadas, sin errores JavaScript/HTTP. Esto no mide un teléfono físico.

[QA de dimensiones](./dimension-verification.json): 1 unidad GLB = 1 m; 4707 objetos comparados con vértices evaluados de Blender, 4969 comparaciones incluidas puertas abiertas y cerradas. Error máximo 0.284 mm. La tolerancia individual depende de un paso de cuantización de 16 bits transformado a metros más 0,02 mm de precisión numérica. Vegetación LOD y terreno sustituido se declaran aparte.

[QA de materiales y geometría](./asset-verification.json): fuente SHA, mapas UV0/PBR, botánica compartida y puertas. La geometría normalizada se decodifica antes de calcular envolventes o BVH; una aserción impide la regresión de oclusores gigantes.

## Límites e historial

La calidad fotográfica 9,5 sigue pendiente de crítica independiente. Follaje LOD, repetición superficial, entorno y diferencias entre motores limitan la imagen. No se verificaron Safari ni dispositivos móviles físicos.

Ensayo histórico Pass3b, SHA fd477337c188777079fc9fa5f630958edb077f655237074cd189aa3e698266af: primera activación del trazador bloqueó el hilo principal 24,90 s; cambiar vista llegó a 10,15 s. Su fuente tenía 12 puertas y esas cifras no se atribuyen a R6K. El trazador permanece apagado por defecto. Ensayo GI Pass3d, SHA 49c887fa62ff004910b058b7221b4af5bc8cdee2dbe2a6b40cf3673fa0791d9c: 43 superficies del estudio; el histórico no se confunde con la candidata actual.

## Reproducción y publicación

Exportar la fuente con scripts/web95_optics_export.py --candidate, ejecutar photographic95-optimize.mjs, photographic95-assets-verify.mjs, photographic95-dimensions-verify.mjs y photographic95-final-qa.mjs. Para el ensayo GI se usa la misma fuente, gi/bake.py, gi/denoise.py y los verificadores GI. Los scripts no guardan la fuente.

[Lista exacta de archivos publicables](./publication-files.json). Excluye comparativas históricas y copias Blender de ensayo. Dependencias y licencias en vendor; Three 0.180.0, three-gpu-pathtracer 0.0.24, three-mesh-bvh 0.9.5.

Fuentes primarias: [three-gpu-pathtracer](https://github.com/gkjohnson/three-gpu-pathtracer), [material físico Three](https://threejs.org/docs/pages/MeshPhysicalMaterial.html), [unidades glTF](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#coordinate-system-and-units), [Oak Veneer01](https://polyhaven.com/a/oak_veneer_01), [Red Bricks04](https://polyhaven.com/a/red_bricks_04), [Tree Small02](https://polyhaven.com/a/tree_small_02), [OIDN](https://www.openimagedenoise.org/documentation.html).
