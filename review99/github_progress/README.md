# R7 — publicación de avance

Estado: **en desarrollo, sin nota ni aprobación integral R7**. Objetivo global: **9,9/10 e hiperrealismo fotográfico**. La última evaluación integral de R6K fue8,3/10. Esta publicación mantiene disponible el trabajo comprobado mientras se completa el siguiente candidato.

## Archivo editable

- Archivo: [Casa_de_Campo_99_R7_avance.blend](../../output/Casa_de_Campo_99_R7_avance.blend).
- Tamaño: 361,458,601 bytes.
- SHA256: `2fb66250a3634a3b956244220d0f52f587623c1d0b0179c9ee0a5fd0d9b2bf46`.
- Fuente local de puertas comprobadas: `Casa_de_Campo_99_R7C_hands_preview.blend`, SHA256 `c747143332f00b7888512caad1be7ee7accfd30cb1a57f2703f63bfb6e39f3b9`.
- [Manifiesto del guardado](manifest.json) y [comprobación al reabrir](reopen_checks.json).

El Blender es autónomo: conserva las imágenes empaquetadas y objetos editables. Los scripts registran la construcción y los controles locales; los checkpoints intermedios mencionados en sus rutas no se distribuyen en este punto de avance.

## Cambios y evidencia

El vestidor sólo conecta dormitorio y baño; el dormitorio tiene acceso directo al estar; el baño PA conserva su acceso al comedor. El baño del monoambiente PB se ubica junto a la fachada Cedro Misionero y la medianera derecha. Las cuatro escenas comparten la geometría actual.

Se corrigieron las manos de las dos puertas del dormitorio: [descripción, dimensiones y controles](../door_hands/COORDINACION_MANOS_R7.md). En la fuente de esas puertas se ensayaron41posiciones por hoja,886pares geométricos exactos y una envolvente corporal de450mm en73posiciones sin impactos. La separación analítica mínima entre ambos barridos es10,953mm. Estos controles geométricos no son una certificación de accesibilidad o de productos.

El recorrido de cámara se verifica contra la geometría y las puertas en su estado animado: [control previo al guardado](tour_in_memory.json) y [control del archivo reabierto](tour_reopened.json). Son9000rayos de comprobación a lo largo de12tomas preparadas; no se ha renderizado una secuencia de vídeo.

La [imagen del nuevo acceso](../../docs/avance-r7/acceso-dormitorio.png) procede de la fuente de puertas indicada arriba, con la cámara añadida en memoria. Se conserva su archivo original sin retoque. La verificación al reabrir compara los meshes, matrices, asignaciones de material y visibilidad con esa fuente; no se presenta la imagen como render final del nuevo SHA.

Incluye además corrección del volumen de agua de la piscina, textiles físicos, huerta e iluminación de trabajo. No incluye aún el cierre C2 de revestimientos, C3 de ventilación ni el refinamiento posterior de sanitarios y pavimentos.

## Qué sigue pendiente

- Integrar y verificar los encuentros húmedos y equipos/conductos/mantenimiento de ventilación.
- Terminar sanitarios, pavimentos, cámaras y realismo visual.
- Generar todos los renders, visor y33planos desde un único modelo integrado.
- Auditoría independiente completa, con nota global; [matriz exigida](../../audit/r7_review_requirements.md).

**El visor principal,19imágenes y33planos publicados siguen en R6K.** La página [Avance R7](https://gatdeguin.github.io/42/avance-r7/) muestra el alcance de este checkpoint. La prueba de la página cubre escritorio y viewport táctil emulado, sin afirmar una prueba en teléfono físico: [resultado](page-qa.json).

**Video pausado hasta autorización explícita del propietario.** El checkpoint conserva el recorrido editable. La documentación de estudio no constituye documentación ejecutiva habilitada ni cálculo resistente, hidráulico, acústico o reglamentario.

## Verificación pública

Publicado en el commit5920218. Se descargó y comprobó el Blender completo:361.458.601bytes ySHA256 idéntico al checkpoint. Las tres páginas y la imagen coinciden byte a byte con Git. [Registro HTTP yhashes](live_verification_5920218.json) · [Prueba pública de página en Chrome](live-page/page-qa.json).
