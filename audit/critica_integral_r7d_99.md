# Auditoría integral independiente — R7D

11 de septiembre de 2026. Fuente congelada R7D y entrega completa de esta iteración.

**Dictamen: 8,5/10. R7D muestra progreso respecto de R6K (8,3), pero NO alcanza el umbral de9,9 ni el hiperrealismo fotográfico solicitado.** El total ponderado sin redondeo es8,465. Persisten errores físicos y ópticos comprobados, además de limitaciones visibles de materiales, vegetación y visor. Se requieren tres pasadas correctivas y una nueva auditoría integral.

Ésta es la evaluación formal de R7D tal como se entrega ahora, autorizada tras reunir25 imágenes y33 planos. La iluminación GI de ocho regiones y la convergencia fotográfica web siguen pendientes; se califican como trabajo no completado. Los anteriores informes preparatorios y acotados conservan su alcance y fecha. Sus frases «sin nota global» no sustituyen este dictamen posterior.

## Entrega y alcance de la revisión

| Elemento | Identificación |
|---|---|
| Fuente Blender | output/Casa_de_Campo_99_R7D.blend |
| SHA256 fuente | 9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e |
| Imágenes examinadas | review99/r7_final/stills/manifest.json;25 PNG, cinco contactos y acercamientos nativos |
| Planos | planos95/r7d_candidate/Casa_de_Campo_Planos_Completos_95_A2.pdf;33 A2 |
| SHA256 PDF | f1237f05ca9438963ec0d8b81edae8df81bdcd5c2b20889ecb57639b5cca3cc1 |
| Editables comprobados |33 DXF,209 cotas DIMENSION nativas;33 SVG en paquete |
| Verificación propia de derivados | audit/r7d_final/evidence_verification.json:88/88 archivos del manifiesto coinciden y25/25 PNG coinciden |
| Visor público | https://gatdeguin.github.io/42/; evidencia pública del constructor f8026c0 en review99/github_r7d_progress |
| Estado de vídeo | Pausado; esta auditoría no renderizó vídeo ni utilizó GPU |

Se inspeccionaron las25 composiciones y los acercamientos de cama, huerta, consola y espejo. Se revisó la composición de las33 hojas mediante sus nueve contactos y se ampliaron A03b, A10b, D08 y D11 para las cuestiones más recientes. Se extrajo el texto del PDF completo, se verificaron tamaño A2 y trazabilidad de sus archivos y se contaron las cotas CAD nativas. Los42 valores críticos recalculados por el autor de planos se usan como evidencia complementaria, contrastando los relativos a nuestros hallazgos con la fuente.

Las mediciones propias abrieron R7D en modo de sólo lectura: geometría evaluada, contactos, intersecciones exactas, normales ópticas, dimensiones de muebles y pruebas de uso declaradas. Los barridos completos de puertas, la maniobra P de mantenimiento y las regresiones globales del constructor se citan con su alcance; no se presentan como una repetición independiente de todos los ensayos.

Para web se examinaron sus capturas públicas de exterior, estudio y acceso, informes de carga/controles y verificación de recursos. La prueba Chrome de cuatro vistas,13 puertas y retrato fue ejecutada por el constructor; esta revisión no hizo una segunda sesión interactiva propia ni una medición nueva de FPS. El intento de lectura independiente por herramienta web no obtuvo la página. La evaluación se apoya en la evidencia identificada y no atribuye a esta auditoría una comprobación pública adicional inexistente. Los nuevos planos/galería R7D están evaluados como archivos entregados; la publicación posterior de esos enlaces requiere la verificación correspondiente.

La nota se refiere al estudio digital. Mensura, resistencia, estabilidad, prestaciones de instalaciones/acústica y aprobación municipal requieren proyecto y comprobaciones profesionales propios. Estas reservas no justifican los errores de geometría, uso o imagen que sí pueden verificarse aquí.

## Puntaje por áreas

Se conservan las diez áreas y ponderaciones de R6K. Son juicios sobre la entrega observable, no certificaciones ni probabilidades.

| Área | Peso | Nota /10 | Fundamento |
|---|---:|---:|---|
| Fidelidad geométrica, escala y alturas | 15% | 9,3 | Correcciones del propietario incorporadas y cotas principales coherentes; medidas físicas diferenciadas de productos genéricos. |
| Uso, distribución y circulación | 10% | 8,4 | Accesos y baño PB corregidos; permanecen déficit de reserva en isla y coordinación del puesto MIDI. |
| Estructura representada y apoyos | 10% | 8,7 | Apoyos de edificio/ventilación mejor documentados; montaje sin apoyo del controlador requiere corrección. |
| Envolvente, encuentros y agua | 10% | 9,1 | Interferencia de agua corregida y continuidad húmeda representada; especificación y ensayos de prestaciones pendientes. |
| Instalaciones y acústica | 10% | 8,4 | Ventilación física y maniobra P de mantenimiento coordinadas geométricamente; caudal, acústica y medio auxiliar por resolver. |
| Documentación | 10% | 9,3 | 33 A2 y 209 cotas nativas coherentes; faltan cortes de los usos recién detectados y cierre de propuestas. |
| Realismo de interiores, objetos y textiles | 15% | 7,6 | Mejor separación de sanitarios y legibilidad; espejos deformantes, textiles rígidos, prendas y equipos genéricos. |
| Realismo exterior y paisaje | 10% | 7,6 | Agua y lectura del edificio mejoran; rosetas facetadas, repetición del jardín y transición de horizonte poco natural. |
| Luz y composición de cámaras | 5% | 8,2 | 25 vistas con mejores tomas amplias/retratos; ciertos recortes y respuesta óptica/material siguen limitando credibilidad. |
| Visor, correspondencia y experiencia | 5% | 7,4 | Fuente actual y 13 controles verificados por constructor; raster visible distante de Cycles, GI y convergencia pendientes. |
| **Total** | **100%** | **8,5** | **8,465 sin redondear. Sin aprobación9,9.** |

Los avances documentales o geométricos no compensan por promedio una apariencia claramente sintética en zonas principales ni un mecanismo físicamente imposible.

## Avance comprobable

**Decisiones del propietario.** La distribución y los planos incorporan vestidor conectado sólo con baño y dormitorio, puerta directa dormitorio–estar y conexión baño–comedor conservada. El baño del monoambiente está junto a Cedro y medianera. Cama/ventana, barra paralela a parrilla, mesa hacia jardín y reorganización de cocinas son coherentes con las decisiones registradas. Se conservan lote22×20, huella8×12 y las referencias autorizadas. El norte orientativo y los servicios disponibles están declarados; acometidas y mensura siguen sin relevamiento.

**Alturas y acceso.** NPT superior+3,25; vivienda y baño alto2,60 libres, estudio3,20. Los accesorios nuevos de ventilación comienzan en+6,453, equivalentes a3,203 sobre NPT. La hoja dormitorio–estar tiene848 mm en la garganta y806 mm conservadores incluyendo la proyección de manija; A03b/A12 explican esa diferencia respecto de923 mm entre marco y del antiguo cálculo813 mm. Esa cota no se extiende a todo el trayecto junto a la cama. El constructor aporta41 poses por nueva puerta,886 pares sin choque,73 posiciones del cuerpo de450 mm y separación mínima entre barridos de10,95 mm.

**C1, agua.** La corrección elimina el antiguo solape de114 mm con el fondo. La regresión del SHA integrado conserva14 intersecciones de control y72 estaciones de contacto, cresta−0,030 y fondo interior−1,390. A08 y las imágenes muestran agua dentro del vaso. El circuito hidráulico conserva su proyecto pendiente.

**C2, húmedos.** Las18 estaciones propias confirman capas de8/4/2 mm sin separación física relevante; los retornos, juntas y penetraciones se representan en D11. El llenador/mando de bañera ahora tiene cuerpo y encuentro que salvan el vacío anterior de35 mm. Dos pequeñas anomalías topológicas de membrana/adhesivo PB son aristas de triángulos casi degenerados, del orden submicrométrico; se registran para limpieza de malla, sin atribuirles una filtración no demostrada.

**C3, ventilación.** Equipos, dos circuitos, filtros, silenciadores, terminales y apoyos existen en3D. Se comprobaron44 estaciones laterales de contacto de22 placas con cabios; los controles del constructor conservan encuentros y reservas sin impactos indebidos. D08 muestra el acceso propuesto: plataforma1200×600, tablero+4,65, cuerpoØ450×1720, cabeza+6,37 y recepción de módulos+5,40. La prueba incluye desplazar temporalmente el mueble de apoyo y sus cuatro patas y transferir piezas al medio elevador. Queda documentada la reserva geométrica; selección, estabilidad, capacidad, herramientas y alcance del operario siguen como P. Las bocas finales están separadas2,52 m entre centros, coherente con el detalle final.

**Documentación.** Las33 A2, sus capas gráficas G/F/P y209 cotas CAD mantienen buena legibilidad y correspondencia. La escala y huella de los WC están separadas de su altura de asiento455 mm y de la envolvente con tapa abierta. El zócalo huérfano de cocina ha desaparecido. El juego es útil para revisar el proyecto completo; necesita sumar los cortes de uso que revelan los siguientes conflictos.

## Bloqueos confirmados y cierre exigido

### R7D-01 — Bisagras sanitarias que se atraviesan

La auditoría independiente ensayó92 pares internos candidatos. Clasificó30 cruces fijo–móvil y separó otros33 encuentros entre piezas solidarias/fijas. El pedestal invade manguitos y brazos; el pasador atraviesa brazos que deberían girar. En muestras0°,30°,60° y90° persiste la interferencia. Es un defecto mecánico real aunque los componentes pequeños se lean mejor en la fotografía.

**Corregir:** definir alojamientos, holguras, grupos solidarios y tope/retención de apertura. Verificar asiento y tapa contra todas las piezas fijas, incluidos brazos/manguitos/pasadores. No basta ensayar sólo los cuatro grandes volúmenes del WC. Informe: `audit/critica_constructiva_preliminar_r7d.md`.

### R7D-02 — Controlador MIDI sin apoyo y puesto mal coordinado

El hueco central de rodillas sí existe: doce rayos confirman700 mm de altura. La sospecha de base totalmente maciza queda descartada. Sin embargo, la silla fija tiene asiento470 mm y las teclas están a859,5/872 mm, unos390/402 mm por encima del asiento. La antigua cota del frente de consola750 mm no describe la altura del teclado.

Además,56 rayos contra toda la escena no encuentran apoyo entre controlador horizontal y consola inclinada; las separaciones medidas van de3,75 a49,05 mm. El inventario local no identifica patas, cuñas o bandeja.

**Corregir:** montar el equipo sobre apoyos reales y representar un operador dimensionado con alcance, codos, rodillas y pies. Ajustar teclado/asiento conservando reserva física para piernas; no bajar todo el conjunto sin probar la consecuencia. El informe contiene una postura de ensayo explícita, sin presentarla como percentil antropométrico: `audit/critica_puesto_estudio_r7d.md`.

### R7D-03 — Isla: vuelo existente, reserva de rodillas insuficiente para el objetivo de confort

Se midieron250 mm útiles hasta el fondo, tapa900 mm, asiento650 mm y215 mm entre asiento e intradós. Los tiradores están al lado de trabajo y no invaden las rodillas. La falta total de vuelo que sugiere la perspectiva queda descartada.

La referencia de diseño [NKBA Guideline9](https://kb.nkba.org/uploads/2022/05/Kitchen-Planning-Guidelines.pdf), para una altura próxima de914 mm, propone381 mm de profundidad por puesto: diferencia de131 mm. Es una recomendación de diseño, no normativa local. Los ensayos declarados a500 mm por delante del centro de asiento quedan libres20 mm; los de550/600 mm atraviesan la placa.

**Corregir:** coordinar tapa, fondo, taburetes y paso posterior; probar ambas plazas sentadas y sus entradas/salidas. Añadir corte de uso y soporte de la tapa si se amplía su consola. Informe: `audit/critica_isla_mono_r7d.md`.

### R7D-04 — Espejos planos con sombreado curvo

Quincho y suite conservan normales personalizadas desviadas aproximadamente27–32° respecto de sus caras planas. La prueba analítica produce cambios de dirección reflejada de hasta53,77° y42,37°. El espejo del mono es control correcto con0°. Se confirma una causa local del reflejo en chevrones del quincho; no se atribuye sin prueba a UV del ladrillo.

**Corregir:** restaurar normales planas en las caras ópticas, preservar cantos y verificar el resultado exportado y en tomas oblicuas. Informe: `audit/critica_espejos_r7d.md`.

La nueva puerta dormitorio–comedor tiene caras planas con normales correctas (0°), sin modificadores. Su franja diagonal brillante sigue como observación para revisar material/UV/iluminación; no se añade como otro error geométrico confirmado.

### R7D-05 — Textiles, ropa y equipos aún sintéticos

En los acercamientos nativos, el borde de cama presenta tiras estrechas y pliegues de arista demasiado aguda; la superficie central y almohadas conservan uniformidad excesiva. Las prendas del vestidor se leen como láminas estrechas repetidas, aun con mejor luz. Cabecero y sillas muestran bandas regulares; conviene revisar escala/dirección de tejido y relieve. La consola gana detalle de controles pero mantiene grandes piezas genéricas y el apoyo defectuoso descrito.

**Corregir:** continuidad y radios creíbles del dobladillo, compresión/contacto de almohadas y prendas con volumen legible en cuello, hombro y manga. Validar distancia de uso y acercamientos del mismo modelo; la textura añadida no reemplaza una silueta convincente. No hace falta ensuciar arbitrariamente materiales nuevos para conseguir realismo.

### R7D-06 — Huerta y entorno todavía esquemáticos

Las rosetas cercanas muestran hojas facetadas, puntas y pliegues repetidos; su lectura es de origami. Otros cultivos conservan siluetas simplificadas. El césped tiene una distribución demasiado uniforme y la transición del terreno del modelo al horizonte permanece visible. Estos defectos se perciben en la imagen general y en el recorte nativo.

**Corregir:** morfología vegetal por especie propuesta, curvatura/espesor, inserciones y variación de crecimiento coherentes; reducir patrones repetitivos sin alterar ubicación autorizada de canteros. Resolver transición de suelo y fondo con escala y luz consistentes. Comprobar también la silueta de las copas y su alfa en web.

### R7D-07 — Fotografía y visor sin cierre

La serie mejora exposición, lectura del vestidor, estudio amplio y cuatro composiciones verticales. El baño se comprende combinando varias tomas; algunas recortan aparatos. La medianera ocupa mucho primer plano de pileta y falta una toma interior que muestre su borde próximo completo.

En las capturas públicas, el raster sigue mostrando copas punteadas, suelo y agua simplificados y una respuesta de luz/material distinta de Cycles. El constructor registra descarga131,8 MB,13 puertas y cero errores en sus pruebas; eso acredita funcionamiento dentro de ese alcance. No hay nueva prueba de carga fría/FPS comparable ni convergencia fotográfica validada. La GI de ocho regiones sigue ausente. Se acepta detener su horneado en esta fuente que ya requiere corrección; **se puntúa la entrega actual, sin anticipar la calidad del trabajo futuro**.

**Corregir:** después de cerrar geometría/materiales, congelar la siguiente fuente, generar iluminación consistente, validar HDR/color y comparar cámaras equivalentes Cycles/web. Medir carga y fluidez con equipo/red declarados, escritorio y viewport táctil emulado. La ausencia de teléfono físico sólo limita afirmaciones sobre rendimiento móvil real; no exige adquirir uno ni bloquea por sí sola el alcance digital.

## Tres pasadas antes de la próxima presentación

1. **Construcción y uso.** Resolver SAN99, apoyo/altura del MIDI e isla; completar cortes de operador y comensales. Limpiar anomalías de malla pertinentes y conservar accesos, alturas, agua y C2/C3 ya coordinados. Repetir los controles afectados con la geometría final.
2. **Materiales y forma visible.** Corregir espejos, diagnóstico de brillo de puerta, dobladillos/almohadas/prendas, botánica y acabado de equipos cercanos. Evaluar pruebas fijas amplias y de detalle; no producir vídeo.
3. **Luz, derivados y entrega.** Congelar un único SHA, generar las vistas y planos afectados, resolver GI/correspondencia web, probar navegación/carga y revisar la publicación exacta. Presentar un solo paquete con pendientes explícitos para la siguiente auditoría integral.

**Estado final de R7D: 8,5/10, candidata en revisión, NO APROBADA para9,9.** La siguiente nota debe basarse en correcciones y pruebas observables, sin elevar el resultado por el número de archivos, el tiempo de cálculo o la intención del constructor.
