# Revisión documental parcial — juego R6G de 33 láminas A2

Fecha: 10 de septiembre de 2026. Crítico independiente: agente de auditoría arquitectónica.

**Nota documental: 8,8/10.** El juego resulta legible y útil para revisar el proyecto; todavía necesita corregir referencias y distinguir algunas cotas de fuente de la piel exterior medida. Esta nota califica la documentación de prueba examinada. **No constituye la aprobación integral de 9,5/10**, ni una evaluación nueva del realismo fotográfico, ni autorización para construir.

## Objeto y trazabilidad

- PDF: planos95/r6g_preview/Casa_de_Campo_Planos_Completos_95_A2.pdf.
- SHA256 del PDF examinado: 322729c5c5b25451d9b36ef6415dab8362d938a294d5f6c8d3931f029bef3c40.
- Modelo declarado: Casa_de_Campo_95_R6G_juntas.blend, SHA256 5ef3e83507a18a80fae342fdf700274397237667b89f38e310198857326849e0.
- Se revisaron las 33 páginas mediante extracción de texto y rasterización propia de Poppler; todas en láminas de contacto y A10b, D03 y D11 ampliadas. Se inspeccionaron cajas de texto y tamaños tipográficos con pdfplumber.
- El ZIP editable contiene 33 SVG y 33 DXF entre 82 miembros y pasa la comprobación de integridad ZIP. Conteo independiente: **192 entidades DXF DIMENSION**. Este conteo confirma editabilidad de las cotas; no sustituye una comprobación numérica individual de las 192.

La geometría R6G precede a las correcciones de consola, apoyos y narices de escalera, banco, taburetes, agua y otros ajustes ya encargados. Su ausencia aquí no se interpreta como regresión. La emisión final deberá regenerarse desde el mismo SHA que el modelo y el visor entregados.

## Resultado por aspecto

| Aspecto | Nota | Evidencia y límite |
|---|---:|---|
| Composición y legibilidad | 9,3 | Las 33 páginas son A2 horizontal, aproximadamente 594 × 420 mm. No hay imágenes raster incrustadas, palabras fuera de página ni textos a menos de 20 pt del borde. Fuente mínima observada: 7,087 pt, aproximadamente 2,50 mm. No se observaron recortes u obstrucciones relevantes en las imágenes revisadas. |
| Identificación de fuente, geometría y propuesta | 9,0 | Las leyendas F/G/P y las limitaciones se reiteran de forma clara. Falta corregir la presentación de dos niveles de cubierta como si fueran la terminación medida. |
| Navegación, referencias y localización | 8,0 | Índice completo y trazas de cortes utilizables. Persisten condicionales heredados, códigos de detalle duplicados entre juego general y suplemento y una identificación territorial incompleta. |
| Contenido de las nuevas láminas | 8,8 | A10b, D03 y D11 aportan cotas y montaje de valor para revisión; las propuestas no se presentan como prestaciones ensayadas. No prueban por sí solas la totalidad de contactos o funcionamiento físico. |
| Paquete vectorial y trazabilidad | 9,1 | PDF, SVG, DXF y SHA identificados. La futura regeneración del modelo exige renovar todos los soportes conjuntamente. |

La nota total es una valoración crítica del conjunto, no una certificación estadística.

## Correcciones exigibles para la emisión

1. **A05a y A05b, niveles de cubierta.** Los rótulos +8,10 de cumbrera y +7,00 de estudio requieren identificación expresa como referencias F. La piel exterior G del estado medido alcanza aproximadamente +8,170 y +7,037 m. Usar los niveles medidos para coronamiento y terminación, conservando las referencias de fuente cuando ayuden a explicar el proyecto. La diferencia no procede de las correcciones posteriores de mobiliario o escalera.

2. **A00 y A03, texto condicional heredado.** El índice dice «Uso PA / recorridos (si P11 existe)» y A03 dice que P11 vincula baño/comedor «cuando figura en el modelo». P11 ya está incorporada en el juego revisado. Describir el estado representado de manera inequívoca.

3. **A13/A13b y suplemento, referencias duplicadas.** Los detalles locales D01–D07 se confunden con las hojas D01–D11. Por ejemplo, D06 designa DVH en A13b y acústica en el suplemento. Cambiar los identificadores locales a 01/A13, 06/A13b, etc., y reservar D01–D11 para las hojas suplementarias.

4. **A12, lenguaje de emisión.** Reemplazar «No modificar pilares silenciosamente» por la descripción geométrica correspondiente: hoja nominal de portón y paso entre caras de pilares son magnitudes diferentes. La instrucción de proceso no pertenece al plano emitido.

5. **Localización.** Incluir Partido de La Matanza, además de Virrey del Pino, Buenos Aires, al menos en índice/trazabilidad y preferentemente en cartelas. El norte está correctamente declarado como orientación aportada por el propietario; no debe convertirse en azimut topográfico comprobado.

El autor de los planos comunicó que estos cinco puntos ya se corrigieron en el generador. **Esta auditoría aún no ha verificado el PDF regenerado**, por lo que se registran como correcciones anunciadas, no como cierres comprobados.

## Comprobación de las tres láminas nuevas

**A10b — Monoambiente.** Distingue correctamente las alturas de tapa, asiento y mesada respecto del piso: 750, 460 y 900 mm. La cota de trabajo de 1,076 m está identificada hasta el tirador. La retirada de silla de 450 mm, la apertura de heladera y la envolvente de usuario de 600 mm son propuestas P; no se presentan como ensayo ergonómico o normativa. La diferencia respecto a los 350 mm utilizados en A03b corresponde a otro ambiente y no constituye una contradicción automática.

**D03 — DVH.** Se leen la composición 9/17/9 mm, galce de 39 mm, juntas de 2 mm y tacos de 6 mm. La conexión del marco a obra está diferenciada como P. El dibujo ayuda a revisar el montaje, pero no acredita estanqueidad, acústica, resistencia ni compatibilidad con un sistema comercial. La revisión documental no sustituye la comprobación física del asiento del marco sobre el alféizar, tratada en una prueba geométrica separada.

**D11 — Ducha.** Representa 900 × 1450 mm, sumidero de 100 × 100 mm, desnivel de 14,5 mm y pendientes diferenciadas por distancia al sumidero. El acceso de 944 mm y la altura de rociador de 2,10 m se leen sin confusión con cotas absolutas. Los estratos y conexiones son comprensibles; no equivalen a ensayo de impermeabilización o dimensionamiento hidráulico.

## Alcance que está bien declarado

Las plantas identifican cortes, pisos y alturas; A01 conserva lote de 22 × 20 m y norte orientativo; A16 diferencia superficies de piezas geométricas de superficies catastrales y advierte sobre sumas duplicadas. Las instalaciones son esquemas funcionales P, con conexiones, caudales y cálculo pendientes. Los detalles estructurales no atribuyen capacidad a placas, anclajes o perfiles por estar dibujados.

No encontré una afirmación de certificación normativa, estructural, acústica o hidráulica que el paquete no pudiera sostener con su alcance declarado. Tampoco encontré una afirmación de que la bañera compacta sirva para inmersión completa de un adulto. La denominación y dimensiones finales del artefacto deberán seguir explícitas en la regeneración.

Para cerrar esta revisión documental basta comprobar los cinco ajustes sobre la nueva emisión, su identidad con el modelo final y las láminas afectadas por la integración. La calidad fotográfica y la aprobación arquitectónica integral requieren sus propias evidencias.

## Evidencias propias

- audit/documental_r6g/metadata.json: huella del PDF, tamaño de las 33 páginas, imágenes y archivo ZIP.
- audit/documental_r6g/text_geometry.json: tamaños tipográficos y cajas de texto.
- audit/documental_r6g/dxf_dimension_count.json: conteo de las 192 cotas nativas por archivo.
- audit/documental_r6g/page_01.txt a page_33.txt: texto examinado.
- audit/documental_r6g/page-01.png a page-33.png: renders propios usados para inspección.

La fuente examinada permanece sin modificar.
