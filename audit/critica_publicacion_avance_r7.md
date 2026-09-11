# Revisión independiente de publicación — avance R7

**Resultado: sin bloqueos de exactitud o alcance en la publicación local examinada.** Puede presentarse como un avance editable en revisión. **Esto no es una auditoría arquitectónica integral, no asigna nota R7 y no acredita hiperrealismo ni aprobación de 9,9/10.** R6K conserva su última nota global de **8,3/10**.

Se examinaron el README principal, la página `docs/avance-r7/index.html`, su imagen, el README técnico de `review99/github_progress/`, los manifiestos y controles vinculados. Esta revisión cubre la coherencia de sus afirmaciones con la evidencia disponible. La descarga y el despliegue públicos posteriores quedan a comprobar después de publicar.

## Archivo y trazabilidad

El crítico leyó el archivo guardado y calculó independientemente su SHA256:

- Modelo: `output/Casa_de_Campo_99_R7_avance.blend`.
- Tamaño: **361.458.601 bytes**, coincidente con el manifiesto.
- SHA256: `2fb66250a3634a3b956244220d0f52f587623c1d0b0179c9ee0a5fd0d9b2bf46`.
- Fuente de puertas: `Casa_de_Campo_99_R7C_hands_preview.blend`, SHA256 `c747143332f00b7888512caad1be7ee7accfd30cb1a57f2703f63bfb6e39f3b9`.

El manifiesto identifica R7 como `IN_REVIEW_NOT_APPROVED`, nota nula y objetivo 9,9. Se leyeron los scripts de creación del checkpoint, sincronización de escenas y cámara de acceso. Su alcance corresponde a añadir cámara, preparar recorrido, metadatos y compartir las colecciones vigentes entre variantes; no incorporan silenciosamente C2/C3.

El constructor aporta `reopen_checks.json` sobre el archivo exacto guardado: 5.611 mallas comparadas con la fuente, sin altas, bajas ni cambios en la comprobación declarada de vértices/topología, matrices al frame 1, asignaciones de material, nombres/tipos de modificadores y visibilidad de render. Declara 82 imágenes empaquetadas, 13 rigs de puertas y cuatro escenas con los mismos 5.890 objetos. Esta revisión comprobó el enlace y alcance del informe; no repitió íntegramente esa comparación geométrica ni la convierte en validación global de todos los parámetros posibles.

## Afirmaciones examinadas

| Afirmación de publicación | Evaluación acotada |
|---|---|
| R7 sin nota; objetivo 9,9; última global R6K 8,3 | Correctamente expresado en las tres superficies de publicación. Ningún texto examinado concede aprobación global. |
| Vestidor sólo dormitorio/baño; nueva puerta dormitorio–estar; baño PB junto a fachada y medianera | Coherente con la versión de distribución y puertas identificada. El README técnico conserva expresamente baño PA–comedor. No se presenta como plano ejecutivo. |
| Aperturas y recorrido comprobados | Se vincula evidencia con su alcance: 41 poses por cada una de las dos puertas, 886 pares exactos, cuerpo de diámetro 450 mm en 73 muestras y separación analítica mínima de barridos de 10,953 mm. El recorrido reabierto declara 9.000 rayos en 12 tomas sin impacto ni errores de posición. Son controles del constructor; no certifican accesibilidad ni todos los movimientos humanos. |
| Escenas de día, noche e inspección comparten distribución | Respaldado por sincronización de colecciones y reporte de reapertura con igualdad de objetos. No implica igualdad de iluminación entre variantes ni aprobación de sus renders. |
| Corrección del agua, avances textiles, huerta y luz incluidos | Coherente con la cadena de fuente declarada y las pruebas parciales anteriores. La publicación no los califica de resultado fotográfico final. |
| C2/C3 y refinamientos pendientes | Correctamente explícito: no se afirma que este checkpoint incluya cierre húmedo, ventilación/mantenimiento o refinamiento posterior de sanitarios/pavimentos. |
| Visor principal, 19 imágenes y 33 planos todavía R6K | Advertencia visible y coherente. El usuario no recibe el juego R6K presentado como documentación de la distribución R7. |
| Vídeo pausado | Declarado en README, página, texto interno y metadatos. No se afirma entregar un vídeo renderizado. |

## Imagen y página

La imagen publicada de acceso es idéntica byte a byte a `review99/door_hands/access_camera/preview.png`: **1.200 × 900 píxeles**, SHA256 `4dd116053ac8688c6b70255244aec9053e0596d6d16255615c774840718465a9`. El crítico comprobó identidad, tamaño y existencia de todos los enlaces locales de la página. El pie la identifica como render previo del modelo de puertas, con la misma geometría de la zona, y expresamente no final. El informe de reapertura respalda la equivalencia declarada; no se atribuye falsamente la imagen al nuevo SHA.

El README técnico vincula los informes de guardado, reapertura, recorrido e imagen. La prueba de página del constructor identifica Chrome local con escritorio y viewport táctil emulado, imagen cargada, sin desbordamiento horizontal y sin errores registrados. No se atribuye una prueba en teléfono físico ni una evaluación del visor R7 final.

## Condiciones que conserva esta publicación

- Mantener los rótulos de avance, nota R7 pendiente y distinción respecto de R6K.
- Mantener C2/C3, sanitarios/pavimentos y los derivados finales como pendientes de integración.
- Publicar los archivos y controles vinculados, incluido el Blender mediante LFS, y comprobar la descarga/página pública después del despliegue.
- Someter la siguiente fuente integral y todos sus derivados al crítico antes de afirmar aprobación arquitectónica/fotográfica.

**Dictamen de este alcance:** publicación de avance descrita con honestidad y trazabilidad suficiente; **sin nota R7 ni aprobación integral**. La auditoría completa sigue pendiente.
