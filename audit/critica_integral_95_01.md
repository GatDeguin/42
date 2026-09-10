# Auditoría integral independiente · Criterio 9,5 · Iteración 01

Fecha: 10 de septiembre de 2026.

**Puntaje global: 6,9/10. NO APROBADO con el nuevo criterio de 9,5/10.**

**El realismo fotográfico es una condición imprescindible y actualmente no se cumple.** Una buena nota en geometría o controles no puede compensarlo. También quedan discontinuidades y detalles constructivos sin resolver o sin evidencia suficiente.

La nota anterior de 8 correspondía a una reconstrucción y un visor funcionales, con límites expresamente declarados. Esta revisión agrega una exigencia fotográfica y constructiva mucho mayor. La reducción de nota no significa que el archivo haya empeorado o cambiado: se evalúa la misma entrega con un alcance más estricto.

## 1. Objeto y método

Se auditó el sitio público https://gatdeguin.github.io/42/, el archivo editable output/Casa_de_Campo_Final.blend, el render Cycles principal, vistas interiores, planos/cortes/detalles de review, auditorías anteriores y la referencia visual extraída del HTML: source/reference_0.png. Las cotas del HTML y las decisiones posteriores del usuario prevalecen sobre las libertades de la imagen de referencia.

La versión pública fue identificada por el constructor con el commit b96165967d88fff4ea171025e732dde8595150dc. Mi prueba independiente registró:

- Respuesta HTTP 200; trece vistas de escritorio y dos capturas móviles nuevas.
- GLB público: 10.021.880 bytes; SHA256 3ee11de28d53a4e215c6ebb8d8e895478b2ca5bc18c213c6b007cd8dacc4e394.
- JavaScript público SHA256 15b47ce9a1e8f639b38936405e82c7eeea46ce44ad50d0bab92012240609e20d.
- CSS público SHA256 de4cd2f6569ab659b312252ec8cbac1267537d82a8332d3ee9dcfa99e385a4ad.
- Archivo Blender reabierto independientemente: SHA256 58223d78f71dc0c1d4f33034aaaf0be96a1bd420f72f2231468003e942c2bbfe.

Las capturas públicas propias tienen nombres audit/integral95_public_*.png. Los resultados están en integral95_public_checks.json. Reabrí Blender sin guardar cambios y repetí pruebas geométricas propias; también medí específicamente la escalera, el acceso y las piezas pluviales.

El constructor aportó inventarios nuevos de materiales, luces, cámaras y mallas. Los contrasté con las imágenes y con pruebas propias dirigidas. Esos inventarios son evidencia complementaria, no sustituyen la inspección.

No se modificó producción ni el modelo. No se renderizó vídeo.

## 2. Puntajes por áreas

Los puntajes son un juicio crítico sobre la evidencia disponible, no resultados de una certificación. Los pesos hacen explícita la composición de la nota global.

| Área | Peso | Nota | Motivo principal |
|---|---:|---:|---|
| Fidelidad de implantación, dimensiones y alturas | 15 % | 9,2 | Fuente bien conservada y alturas autorizadas verificadas. |
| Circulación, puertas, escalera y accesos | 10 % | 8,0 | Interferencias corregidas; faltan comprobaciones completas de uso y resolución del arranque/umbral. |
| Estructura y apoyos representados | 10 % | 7,0 | Elementos principales plausibles; uniones, apoyos y camino de cargas insuficientemente documentados. |
| Envolvente, cubierta y agua de lluvia | 10 % | 6,0 | Detalle parcial; canaletas cerradas y bajadas sin continuidad hasta descarga. |
| Instalaciones y acústica | 10 % | 5,5 | Extracción coordinada geométricamente; redes y desempeño funcional sin desarrollo suficiente. |
| Documentación arquitectónica verificable | 10 % | 6,0 | Cortes reales útiles, pero escasas cotas y especificaciones de construcción. |
| Realismo de materiales, muebles y equipos | 10 % | 6,5 | Mejor en Cycles; formas y superficies todavía esquemáticas, especialmente en web. |
| Luz, vidrio, agua y atmósfera fotográfica | 10 % | 5,5 | La adaptación pública pierde propiedades ópticas y la atmósfera del referente. |
| Paisaje y relación con el terreno | 5 % | 5,5 | Repetición botánica, siluetas artificiales y transiciones de suelo débiles. |
| Cámaras y composición | 5 % | 7,5 | Ambientes legibles; varias vistas siguen demasiado amplias, recortadas o poco naturales. |
| Visor de escritorio/móvil | 5 % | 8,5 | Funcional y accesible en dimensiones probadas; esto no equivale a calidad fotográfica. |

**Resultado ponderado: 6,905, redondeado a 6,9/10.** Aunque la media fuese superior, el incumplimiento de la condición fotográfica impediría aprobar con 9,5.

## 3. Qué está verificado, inferido y no comprobado

### Verificado en la entrega

- Implantación nominal de lote 22 × 20 m, edificio 8 × 12 m con referencia X=14/Z=0 y dos módulos de 6 m; pileta nominal 7 × 3 m y organización general concordantes con fuente y verificaciones dimensionales conservadas.
- Piso del estudio a +3,25 y cara inferior del cielorraso a +6,45: 3,20 m libres. Vivienda +3,25/+5,85 y baño +3,30/+5,90: 2,60 m libres. La cubierta del estudio está 0,60 m por encima del módulo de vivienda.
- Dieciocho piezas de peldaños; encuentro superior con descanso a +3,20. Sin escalera interior.
- Doce mecanismos de puertas. La repetición independiente de los barridos anteriores no encontró cruces entre las mallas móviles y cerramientos incluidos, ni con el equipamiento seleccionado.
- Conductos de extracción sin cruces con las piezas constructivas incluidas en la prueba. Siete módulos acústicos sin intersección con el cielorraso. Se conservan 152 vértices en el cielorraso recortado.
- El sitio público carga y ofrece trece vistas sin errores JavaScript o respuestas HTTP fallidas registradas. Capturas en 1440 × 1000 y 390 × 844; sin desbordamiento horizontal.
- El GLB sigue siendo el mismo archivo ya revisado; la adaptación de materiales no constituye una reconstrucción alternativa del edificio.

Las pruebas de intersección son muestreadas y tienen filtros/tolerancias explícitos en sus scripts. “Cero cruces” no equivale a circulación humana completa, estanqueidad, capacidad portante ni funcionamiento de una instalación.

### Inferido y necesitado de justificación

- Secciones, uniones, composición de cubierta, patinillo y recorridos de extracción añadidos donde el HTML no aportaba proyecto constructivo.
- Adecuación de aislamientos, ventilación, carpinterías y soluciones de humedad al clima real.
- Comodidad de uso, mantenimiento y durabilidad de los detalles.
- Prestaciones acústicas de una sala con ladrillo y vidrio expuestos, tratamiento superficial y pasos de instalaciones.

### No comprobable con la evidencia disponible

Capacidad de suelo/fundaciones, resistencia y deformaciones estructurales, viento, comportamiento térmico/higrotérmico, cálculo de pluviales/sanitarias, seguridad y tiro de combustión, aislamiento acústico, tiempo de reverberación, evacuación y cumplimiento normativo local.

No se conoce municipio/provincia ni jurisdicción aplicable. “Cedro Misionero” no permite inferirla. No declaro incumplimientos normativos ni certifico esas prestaciones. La ausencia de cálculo profesional no invalida por sí misma una imagen; sí impide presentar la escena como un proyecto ejecutivo resuelto.

## 4. Bloqueos constructivos y documentación exigible

### C1. El sistema pluvial no está resuelto — bloqueo confirmado

**Ubicación:** canaletas frontal y posterior; bajadas junto a X≈21,72.

Las dos canaletas tienen aproximadamente 0,1695 m³ de volumen, el 99,9845 % de su caja envolvente. Un rayo vertical en el centro impacta la cara superior. Son prácticamente bloques macizos cerrados, sin sección receptora representada.

Las bajadas frontal y posterior terminan a +3,28 m. No se representa su continuidad hasta un punto de descarga. **Sí existe** una prolongación frontal entre +6,33 y +6,95 después de elevar el estudio; no sostengo que falte toda esa extensión. La captación, conexión lateral, registros y evacuación completa siguen sin demostrarse.

**Evidencia:** integral95_rainwater_meshes.json/.py/.log y integral95_geometry_reopen.json.

**Cierre exigible:** plano de cubierta con sentido de pendientes, sección abierta de canaleta, embudo/codo de conexión, continuidad hasta descarga identificada y detalle de fijaciones. Mostrar en corte y en una vista cercana que el agua dispone de un recorrido materialmente continuo. Diámetros y pendientes deben identificarse como propuestas pendientes de cálculo cuando corresponda.

### C2. Acceso del estudio y escalera necesitan un detalle de uso completo

**Ubicación:** descanso exterior X=13…14, Z fuente=5…6; umbral del estudio.

Descanso: +3,20. Umbral y piso del estudio: +3,25. Existe un **resalto de 50 mm**, que no debe quedar oculto detrás de una afirmación general de “desembarco libre”. Puede responder a una decisión de estanqueidad; requiere una resolución y una cota explícitas.

En la escalera medí contrahuellas internas de 174,444 mm, avance entre peldaños de 211,111 mm y pendiente de 39,57°. Cada tabla tiene una profundidad mayor por solape; esa profundidad no debe confundirse con la huella de avance. La tabla inferior está a +0,23444 y la superior a +3,20. La cota acabada de arranque y su apoyo no están suficientemente documentados: no asumo suelo a cero ni declaro por ese dato una primera contrahuella irregular.

**Evidencia:** integral95_geometry_reopen.json; corte_escalera, elevacion_escalera y vistas de acceso.

**Cierre exigible:** sección completa con pavimento inicial, todas las contrahuellas, huellas de avance, ancho útil entre elementos, altura de pasamanos, descanso, umbral y hoja abierta; detalle de anclaje inferior/superior y protección del borde. Comprobación de uso con una envolvente humana y de alcance de manija. Conservar las dimensiones fuente o documentar cualquier cambio autorizado; no ampliar la escalera silenciosamente.

### C3. Cubierta, carpinterías y bordes de losa tienen dibujo geométrico, pero no una definición suficiente

Las láminas de alero y cubierta escalonada muestran intersecciones reales. No identifican de manera completa capas, espesores, solapes, continuidad de membranas, fijaciones ni gestión del agua en el cambio de altura. Tampoco desarrollan los encuentros de DVH, umbrales exteriores y borde de balcón.

La aislación de 80 mm y chapa de 0,8 mm añadidas son decisiones representadas; su mera presencia no demuestra control de condensaciones o puentes térmicos. El detalle visible de una membrana no acredita su continuidad.

**Cierre exigible:** detalles 1:5 o equivalentes legibles del alero, escalón entre cubiertas, paso de conductos, encuentro DVH/muro, umbral exterior y losa/baranda. Cada capa debe tener nombre, espesor y función; las pendientes, sellos y vías de drenaje deben dibujarse. Indicar expresamente qué decisión es inferida y qué verificación queda pendiente.

### C4. Estructura y anclajes no tienen trazabilidad suficiente para una auditoría integral

La escena contiene losas, apoyos, zancas, cabios/correas y anclajes visibles. Las correcciones de extracción evitan las vigas ensayadas. Esto es positivo.

No se aportó un esquema completo de apoyos y transmisión de cargas, fundaciones, uniones de balcón ni dimensionamiento de anclajes. No concluyo que la estructura sea inviable; concluyo que su resolución completa no puede verificarse.

**Cierre exigible de plausibilidad visual:** planta estructural con ejes, luces, apoyos y secciones propuestas; cortes que enlacen cubierta, losas y soporte inferior; detalles de unión de escalera, baranda y balcón. Las dimensiones inferidas deben estar identificadas. Para afirmar aptitud para construir, hará falta validación profesional y datos del emplazamiento; no debe simularse esa aprobación con una nota del crítico.

### C5. La extracción está coordinada, pero las instalaciones siguen incompletas

Se verificó la separación geométrica de horno, parrilla y cocina. En particular, el conducto de parrilla recorre varios metros bajo losa antes de subir por el patinillo. La lámina informa diámetros representados de 0,21/0,32 m para horno/parrilla, pero no justifica prestaciones.

Faltan longitud desarrollada, radios/cambios de dirección, acceso de limpieza, condensados, aislamiento térmico, distancias a materiales combustibles y relación entre campana, caudal, reposición de aire y terminal. No afirmo que el trazado no funcione: no hay evidencia para garantizarlo.

Tampoco se aportan redes completas de alimentación/desagüe de baños y cocinas, circuito técnico de pileta, ventilación de locales, electricidad ni acondicionamiento del estudio.

**Cierre exigible:** esquemas coordinados con puntos reales de consumo, descarga y registro; detalle del patinillo y pasos de losa/cubierta; criterios de funcionamiento y mantenimiento. Cálculos o prestaciones que no puedan derivarse de la fuente deben figurar como pendientes y con los datos necesarios identificados.

### C6. El estudio no tiene una estrategia acústica demostrada

La altura y la coordinación geométrica de los paneles están verificadas. El tratamiento representado puede controlar ciertas reflexiones, pero no se aportan objetivos ni prestaciones.

Faltan composición y separación de cerramientos, sellado de puertas/DVH, encuentros del cielorraso, transmisión por losa, ruido de instalaciones y ventilación silenciosa. El patinillo de combustión próximo a la sala requiere una explicación de aislamiento térmico, vibratorio y acústico.

**Cierre exigible:** planta y secciones acústicas con orientación de escucha, posiciones de monitores, puntos de primeras reflexiones, composición y montaje de absorbentes/difusores, sellos y penetraciones; objetivos de aislamiento/reverberación y método de verificación. No asignar valores de dB o RT60 sin cálculo o medición.

### C7. El juego de planos no alcanza la profundidad solicitada

PB/PA tienen dimensiones exteriores y nombres de ambientes, pero faltan cadenas de cotas interiores, vanos, ejes, niveles terminados, secciones de cerramientos y superficies útiles. Las perspectivas cortadas del visor no sustituyen esas plantas.

**Entrega documental exigible:** implantación acotada y niveles del terreno; PB/PA con vanos y circulación; cuatro fachadas; dos cortes generales con ambas alturas; cubierta/pluviales; escalera/acceso; estructura conceptual; carpinterías/barandas; baños y pasos de instalaciones; acústica; cuadro de decisiones fuente/inferidas/pendientes. Las escalas propuestas pueden adaptarse, pero cada detalle debe leerse y comprobarse sin recurrir a una adivinación del modelo.

## 5. Bloqueos fotográficos por vista

### V1. Exterior público: iluminación y óptica de una visualización simplificada

**Evidencia:** integral95_public_exterior.png, integral95_public_pileta.png.

El terreno y el cielo forman campos casi uniformes. Los blancos y la luz de interiores tienen escasa diferenciación; se pierde el contacto y la profundidad de muchos muebles. El agua aparece como una lámina cian transparente sin la riqueza de reflexión/refracción del referente.

El inventario público registra 37 materiales: 16 con mapa de color, cero normal maps, cero mapas de rugosidad, cero AO/light maps y tres bump maps de madera. No se puntúa por cantidad de mapas; las pérdidas visibles y los parámetros explican el problema. El agua web usa opacidad 0,63 y metalness 0,15, con transmisión física cero; el DVH usa opacidad 0,20 y metalness 0,10, también sin transmisión. El Blender sí dispone de agua con transmisión, IOR 1,333 y normal conectado.

La escena web utiliza Hemisphere, Directional y RoomEnvironment; no reproduce las 28 luces del archivo ni su iluminación indirecta de Cycles.

**Cierre:** vidrio con espesor/reflexiones/transmisión coherentes, agua con profundidad, reflejos y variación de superficie, luz indirecta y contacto legibles, interiores que respondan a sus luminarias. Verificar el resultado desde las cámaras públicas, no únicamente en un render distinto.

### V2. El render Cycles tampoco alcanza aún 9,5

El render principal es más rico que el visor: agua, vidrio, sombras y luz interior mejoran. Sin embargo, el horizonte, los troncos repetidos, las copas de hojas dispersas, el césped y los muebles todavía revelan claramente una escena sintética.

Respecto de source/reference_0.png, falta la atmósfera cálida del sol bajo, gradación de cielo, profundidad del fondo vegetal, contacto natural con el suelo y riqueza de los primeros planos. Deben conservarse las cotas y la cubierta elevada autorizada; no copiar de la imagen una geometría que contradiga esos datos.

**Cierre:** comparación lado a lado a tamaño final entre referente y render, con explicación de las diferencias geométricas autorizadas. Atardecer coherente, sombras naturales, fondo integrado y materialidad observada de cerca, sin compensar con bloom o desenfoque excesivo.

### V3. Interiores y equipamiento demasiado esquemáticos

- **Estudio:** consola, faders, monitores y silla tienen lectura de bloques; faltan interfaces, uniones, rejillas, cables y escala de equipo verificable. Las superficies acústicas no muestran textura/material suficientes en web.
- **Quincho/monoambiente/cocina:** sillas, tableros y frentes muy homogéneos; los encuentros, espesores aparentes y pequeños herrajes requieren refinamiento. La extracción tiene presencia geométrica, pero su remate visual sigue básico.
- **Dormitorio:** manta con ondulación repetitiva, almohadas como volúmenes rígidos y cortinas simplificadas. La vista Cycles tiene fuertes contrastes y luminarias dominantes; la web pierde profundidad.
- **Baño:** sanitarios ahora huecos y distribución legible, pero superficies blancas poco diferenciadas; grifería, mampara y encuentros carecen de la riqueza óptica propia de una fotografía.
- **Vestidor:** la cámara corregida permite leerlo y la veta está restaurada. La ropa sigue representada por cápsulas uniformes; el mobiliario admite más detalle superficial.

**Cierre:** conservar distribución/huellas y refinar las piezas visibles con referencias dimensionales; materiales a escala real, tejidos con caída y espesor, uniones y detalles de fabricación. Verificación del estudio, cocina, quincho, dormitorio, vestidor y baño a resolución final y con recortes al 100 %.

### V4. Paisaje y terreno

**Evidencia:** exterior Cycles, integral95_public_huerta.png y exterior público.

Se repiten bifurcaciones de troncos y estructuras de copa. Las hojas dispersas producen un aspecto de partículas; los bordes de césped y bases de árboles resultan artificiales. La huerta conserva la distribución correcta, pero especies, suelo y crecimiento son demasiado uniformes. El entorno lejano no comparte el nivel de detalle del edificio.

**Cierre:** variación botánica reconocible, jerarquía de ramas y masa foliar, contacto de raíces/suelo, transiciones del césped y densidad según ubicación; mantener centros de árboles y huerta definidos por fuente. Mostrar exterior cercano, jardín y huerta sin ocultar defectos mediante profundidad de campo.

### V5. Cámaras y entrega pública

La lectura espacial mejoró, pero algunos encuadres interiores tienen perspectiva muy amplia y objetos cortados. El exterior móvil cabe, aunque deja bastante aire y reduce el detalle de la casa. La navegación libre permite atravesar muros; funciona como orbitador, no está verificada como recorrido humano con colisión.

**Cierre:** una cámara arquitectónica por ambiente que muestre espacio y conexiones sin distorsión dominante, más primeros planos pertinentes. Repetir escritorio/móvil y puertas en poses reales. Una galería Cycles puede complementar la exploración, pero no autoriza a llamar fotográfico al visor si la escena interactiva continúa con el aspecto actual.

## 6. Tres pasadas priorizadas

| Pasada | Trabajo concreto | Evidencia que debe entregarse antes de otra nota |
|---|---|---|
| 1 · Coherencia constructiva y documentación | Resolver captación/descarga pluvial; detallar escalera, arranque y umbral; completar encuentros de cubierta/DVH/balcón; esquemas estructural, de instalaciones y acústico con inferencias declaradas. | Modelo congelado nuevo; planos acotados y detalles legibles; secciones que demuestren continuidad; barridos y comprobaciones dirigidas a las modificaciones. |
| 2 · Materialidad, equipamiento y paisaje | Afinar muebles/sanitarios/equipo técnico manteniendo huellas; tejidos, metal, ladrillo y acústicos a escala; vidrio/agua físicamente coherentes; vegetación y suelo sin repetición dominante. | Vistas sin efectos ocultadores y recortes al 100 %; parámetros de materiales/escala; referencias de piezas; comparación de geometría antes/después. |
| 3 · Luz, cámaras y resultado publicado | Recuperar atardecer y profundidad; equilibrar interiores y luminarias; corregir perspectivas; trasladar la mejora al resultado público sin perder interacción. | Exterior principal, pileta, huerta y seis interiores a calidad final; mismas cámaras comparables en visor y Cycles; pruebas públicas escritorio/móvil, carga y controles. |

Después de completar las tres pasadas debe volver a intervenir el crítico independiente sobre un estado congelado. No se presume que tres pasadas bastarán para 9,5.

## 7. Regla de aprobación con 9,5

Deben cumplirse simultáneamente:

1. No quedar discontinuidades constructivas confirmadas sin resolver ni sistemas presentados como completos sin evidencia.
2. Conservar cotas fuente y decisiones autorizadas, con registro explícito de cambios.
3. Entregar la documentación necesaria para revisar los detalles realmente representados, separando propuestas de prestaciones verificadas.
4. Alcanzar una lectura fotográfica consistente en exterior e interiores críticos, sin geometría simbólica dominante, repetición evidente o pérdidas ópticas como las actuales.
5. Mantener esa calidad en el resultado que se presenta al usuario y pasar otra revisión independiente con nota global ≥9,5. Los controles no pueden elevar artificialmente una imagen que no satisface el punto anterior.

**Aprobación visual**, **plausibilidad constructiva** y **certificación ejecutiva** son dictámenes diferentes. La tercera necesita profesionales, datos y responsabilidades que esta auditoría de una escena no puede sustituir.

## 8. Evidencia y decisión final

Pruebas propias nuevas:

- integral95_public_checks.mjs/.json y trece capturas públicas de escritorio, más móvil/exterior/estudio.
- integral95_geometry_reopen.py/.json/.log.
- integral95_independent_checks_03.json: sin cruces en pares ensayados.
- integral95_door_fixtures_03.json: sin choques en equipamiento ensayado.
- integral95_acoustic_ceiling_03.json: sin intersecciones panel/cielorraso.
- integral95_rainwater_meshes.py/.json/.log: canaletas cerradas y límites reales de bajadas.

Evidencia complementaria: integral95_inventory.json, integral95_web_materials.json, output/validation.json, planos de review, renders Cycles vigentes y source/reference_0.png.

**Decisión: 6,9/10, no aprobado para el estándar 9,5.** El sitio está disponible y el trabajo acumulado es útil, pero no está justificado presentarlo como una entrega fotográfica ni como un proyecto constructivo completamente resuelto. Mantener el vídeo pausado y avanzar por las tres pasadas documentadas antes de solicitar otra calificación.
