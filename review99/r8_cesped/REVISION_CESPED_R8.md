# R8 · Césped fotográfico: entrega del constructor

Se reemplazan las 73 mallas de césped existentes y el acabado/UV de Césped del lote. Se conserva R7D, toda la arquitectura, árboles, canteros, senderos, niveles y terreno exterior de 600 m. No se asigna una nota arquitectónica nueva.

- Fuente R7D: 9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e.
- Copia R8: ff504115cb562a1031865cef8cd0e93f2ecf737b8a5d75571cb51170bef28452.
- Parche scripts/correcciones99_cesped_r8.py: f68d744baaa229545fd481f9ded04d24916a91f009ecec4a0656f0dd87f7504e. Su función apply() es idempotente, no guarda ni renderiza.
- 121.647 manojos, 1.588.465 vértices, 1.567.231 triángulos; 73 objetos, identidades y cuatro escenas conservados.
- 0 objetos añadidos/eliminados, 0 cambios fuera del alcance, 0 errores de raíces/exclusiones.
- Suelo: 16 vértices y 8 caras intactos. Únicamente cambia material/UV; su tinte original queda integrado en el atlas.
- 225,27 m² dentro de la máscara original; 0 píxeles de césped en la máscara de tierra de huerta.
- Raíces sobre las tres superficies existentes, empotramiento 0,7 mm. Alturas máximas de 90 mm dentro del lote y 120 mm en pradera. Exclusiones ampliadas por el radio completo de cada manojo.

El recurso es [Bermuda de Poly Haven](https://polyhaven.com/a/grass_bermuda_01), Rico Cilliers, CC0. Se conservan formas fotográficas, UV y alfa. El sustrato fuera del césped conserva [leafy_grass](https://polyhaven.com/a/leafy_grass), Charlotte Baglioni, CC0, remuestreado al atlas.

La sotocobertura procede de una vista ortogonal de 50.000 manojos reales en 2×2 m: color sin iluminación, normales y rugosidad. No se usan imágenes generadas para ocultar geometría. No hay superficies superpuestas. El prefiltrado por área en espacio lineal evita aliasing durante la reducción. La rugosidad efectiva del sustrato incluye la varianza angular perdida al filtrar las normales, mediante una adaptación aproximada a GGX inspirada en [Toksvig](https://developer.download.nvidia.com/whitepapers/2006/Mipmapping_Normal_Maps.pdf). No se aplica a la tierra descubierta ni a las hojas próximas; las mediciones y fórmula figuran en atlas_manifest.json. El atlas alcanza aproximadamente 5 mm/texel en color y 10 mm/texel en normal/rugosidad. Las hojas próximas conservan geometría y su atlas fotográfico de 2K.

## Comparación visual

Exterior y huerta se comparan con las cámaras y exposición originales, 128 muestras. La primera variante dejaba demasiada tierra visible; la segunda reveló aliasing al remuestrear el suelo. Se incrementó la cobertura y se corrigió el filtrado. Las pruebas intermedias se conservan.

La continuidad y variedad mejoran frente a las púas uniformes y los manojos aislados. La tierra de huerta y los alcorques siguen visibles. Las vistas parten de R7D: todavía muestran plantas de canteros y agua anteriores a los cambios de otras tareas. El césped mantiene un color oscuro/oliva bajo la exposición original de atardecer. No se cambió la iluminación para aparentar mejora. Debe volver a revisarse en la candidata consolidada por el crítico independiente.

## Exportación y coste

El GLB aislado conserva 74 mallas (césped más suelo), 1,567,239 triángulos, UV0, normales y tangentes. Alfa MASK 0,5, doble cara, normales y rugosidad. Persisten 73 marcadores grass8_preserve_faces_on_export. Los anclajes de diagnóstico se retiran sólo de la copia exportada.

Archivo sin compresión geométrica: 118.09 MiB. Imágenes: 35.48 MiB. Primitivos/draw calls potenciales: 74. Texturas RGBA8 estimadas con mipmaps: 192 MiB, antes del resto del proyecto. No se han medido FPS ni carga del visor completo. Optimizar transferencia/compresión debe conservar las hojas.

Evidencia: validation.json, construction.json, export_validation.json, export_source.json, delivery.json, comparacion_cesped.jpg, detalle_cesped_1a1.jpg y stills_verified/. Recursos/recetas: source/photographic99_grass_r8/, derive99_grass_understory.py y build99_grass_lot_atlas.py.

R7D y SAN8 intactos. Sin publicación y sin video.
