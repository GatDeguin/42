# Auditoría arquitectónica integral independiente — R6K

10 de septiembre de 2026. Segunda evaluación integral; criterio de 9,5/10 elevado a 9,9/10 por el propietario al cierre.

**Dictamen: 8,3/10. Hay progreso verificable, pero R6K no alcanza la aprobación de 9,5 ni el realismo fotográfico exigido.** La publicación como candidato en revisión está correctamente identificada y no constituye aprobación. La geometría, el mobiliario y la documentación mejoraron de forma importante respecto del dictamen integral anterior de 6,9. Persisten una interferencia real en la piscina, detalles de coordinación pendientes y una apariencia claramente sintética en partes significativas de las imágenes y del visor.

Durante esta evaluación rigió el umbral de 9,5; al cierre, el propietario elevó la exigencia a **9,9/10 e hiperrealismo fotográfico**. La nota de R6K permanece en 8,3 y no satisface ninguno de esos umbrales. El apartado de aceptación siguiente establece el nuevo criterio para la próxima entrega. El realismo fotográfico es una condición imprescindible. Las buenas notas de documentación, medidas o controles de software no compensan imágenes que todavía no parezcan fotografías. El umbral anterior de 8 y las notas parciales posteriores no equivalen a una aprobación global de 9,5.

## Objeto, trazabilidad y alcance

Se revisaron la geometría evaluada del modelo congelado, el inventario dimensional completo y 54 familias funcionales, encuentros DVH, las 33 láminas A2 y sus editables, las 19 imágenes Cycles de la misma fuente y el visor en escritorio y formatos móviles. Se contrastó la apariencia con la referencia original extraída del HTML. Las cotas expresas y decisiones posteriores del propietario prevalecen sobre libertades de esa imagen de referencia.

| Entrega | Identificación |
|---|---|
| Modelo | output/Casa_de_Campo_95_R6K.blend |
| SHA256 del modelo | a3663a5081dac391303f25b8e9994b1a412a008e971642af29fc2cbee849aa90 |
| GLB local examinado | docs/preview95/assets/house.glb |
| SHA256 del GLB | 7144f32e811e53511c5ca0d706ae4a96dbe98d83e00ea8a07ed723a2e894be03 |
| PDF de 33 A2 | docs/planos/Casa_de_Campo_Planos_A2.pdf |
| SHA256 del PDF | 022d777fc96771d43fd5f2813b187c0057beb7de9e89445daacab8779909798a |
| Imágenes fuente / galería | review95/r6k_stills/manifest.json / docs/renders/manifest.json |
| Publicación informada por el constructor | commit 0d52b52 |
| Visor local y público inspeccionados | http://127.0.0.1:8420/ y https://gatdeguin.github.io/42/ |
| Confirmación pública propia | 2026-09-10, 23:06:16–23:06:47 UTC |

Los hashes de los 19 PNG y sus JPG coinciden con los manifiestos examinados. En la prueba pública, el runtime declara la misma fuente R6K; JavaScript, CSS, módulo fotográfico, metadata y manifiesto de galería coinciden byte a byte con los archivos locales. El hash completo del GLB fue comprobado localmente; no se atribuye a esta prueba una segunda descarga pública íntegra con hash del GLB.

La auditoría no guardó ni modificó el modelo y no renderizó vídeo. Se usa la convención del proyecto X horizontal / Y altura / Z profundidad, convertida en Blender a X / −Z / Y. Las comprobaciones propias se distinguen de los barridos del constructor expresamente citados como evidencia complementaria.

## Puntaje por áreas

Las notas son juicio técnico y visual sobre el alcance digital examinado, no probabilidades ni certificaciones. La ponderación hace transparente el total; no anula la condición fotográfica obligatoria.

| Área | Peso | Nota / 10 | Fundamento principal |
|---|---:|---:|---|
| Fidelidad geométrica, escala y alturas | 15 % | 9,2 | Inventario completo y cotas principales coherentes; dimensiones de productos genéricos siguen siendo propuesta. |
| Uso, distribución y circulación | 10 % | 8,8 | Barra, cama, cocinas y baños mejor coordinados; pasos y escenarios de uso requieren conservar las reservas documentadas. |
| Estructura representada y apoyos | 10 % | 8,7 | Cierre de apoyos reales de escalera, muebles y DVH; geometría no demuestra capacidad resistente. |
| Envolvente, encuentros y agua | 10 % | 8,1 | Encuentros DVH corregidos; agua solapa el fondo y falta cerrar la especificación del acabado vertical húmedo. |
| Instalaciones y acústica | 10 % | 7,7 | Mejor detalle y estrategia P explícita; falta coordinación física completa de ventilación, terminales y mantenimiento. |
| Documentación | 10 % | 9,2 | 33 A2 legibles, cotas editables y distinción G/P; pendientes expuestos con honestidad. |
| Realismo de interiores, objetos y textiles | 15 % | 7,5 | Manta, prendas, ciertos sanitarios y equipamiento aún tienen lectura de modelos genéricos. |
| Realismo exterior y paisaje | 10 % | 7,3 | Arbolado mejorado en Cycles, pero huerta repetitiva, suelo/horizonte poco integrados y pérdida de follaje web. |
| Luz y composición de cámaras | 5 % | 7,7 | Más legibilidad; exposición desigual, encuadres cercanos repetidos y composición vertical débil. |
| Visor, correspondencia y experiencia | 5 % | 7,8 | Controles funcionan; carga pesada, divergencia visual y trazado todavía ruidoso en la prueba realizada. |
| **Total ponderado** | **100 %** | **8,3** | **8,26 antes de redondear. Sin aprobación 9,5.** |

## Qué queda verificado

**Medidas y escala.** Se midieron 5.304 objetos geométricos, 4.851 activos para render, más 93 envolventes evaluadas de instancias; 68 contenedores se registraron aparte. Sistema METRIC, escala de unidad 1,0. Los 297 objetos con escala local distinta de uno fueron medidos con su transformación mundial: no son, por ese dato aislado, errores de tamaño. No se detectaron determinantes mundiales negativos ni geometría no finita. Las ocho superficies de dimensión prácticamente nula están identificadas para interpretación contextual.

Se encontraron las 54 familias previstas. La tabla completa está en [el dictamen dimensional R6K](critica_dimensional_r6k.md), con dimensiones, cotas funcionales y límites de medición. Inventariar todos los objetos no significa atribuir dimensiones homologadas a equipos comerciales no identificados ni simular todos sus usos posibles.

Se comprobaron lote de 22 × 20 m y huella principal de 8 × 12 m; estudio con 3,20 m libres, vivienda y baño alto con 2,60 m, y diferencia de 0,60 m entre referencias exteriores correspondientes de las cubiertas. Se mantienen los cambios de distribución pedidos por el propietario: barra paralela a parrilla, mesa del quincho hacia el jardín, orientación coherente de cama y ventana, conexión baño–comedor y cocina reorganizada.

**Escalera y apoyos.** Hay 18 peldaños de madera de 1,00 m de ancho. Las contrahuellas resultan aproximadamente 177,22 mm desde el pavimento real de arranque a +0,06 hasta +3,25. El avance entre peldaños es aproximadamente 211,11 mm; no debe confundirse con la profundidad de cada tabla. Se verifican los 18 apoyos bajo madera, narices de 2 mm y áreas positivas en 36 interfaces tubo–cartela y 36 cartela–zanca. Esto cierra la discontinuidad geométrica examinada, sin demostrar soldaduras, resistencia, vibración o conformidad normativa de la escalera.

**Mobiliario y sanitarios.** Consola con al menos 700 mm de espacio de rodillas en los 12 puntos examinados del vacío central; frente de trabajo aproximadamente a 750 mm. Taburetes con asiento de 650 mm y banco de huerta a 450 mm sobre su apoyo. Las cuatro patas del banco sí tienen contacto positivo con dos tablones cada una: se descartó el falso aviso de separación obtenido inicialmente por un rayo sobre un canto redondeado. El paso medido entre mesa de comedor y tabique de vestidor es 805 mm, superior al objetivo de proyecto de 800 mm; no es una afirmación normativa.

Rociador del monoambiente de Ø200 × 12 mm, cara inferior a 2,10 m sobre piso. La bañera alta de 1,25 × 0,74 × 0,54 m está correctamente descrita como compacta/asiento; no se presenta como una bañera para inmersión adulta extendida. Los apoyos, alturas y huellas mejoraron; la apariencia de los artefactos sigue siendo objeto de crítica visual separada.

**DVH.** Se ensayaron 71 pares con Boolean EXACT, incluyendo perfiles, vidrios, juntas y cerramientos próximos: sin intersecciones indebidas en los pares comprobados. Dieciocho estaciones verificaron los contactos alféizar–EPDM–marco con errores del orden de micras. Quedan cerrados los conflictos de 8,5 mm y los encuentros adyacentes examinados. No se deriva de ello un ensayo de estanqueidad, aislamiento acústico, durabilidad o resistencia.

**Puertas y recorrido.** Se identifican 13 rigs y el visor mueve los 13 hasta su apertura objetivo. El constructor aporta barridos de 41 estados contra equipamiento activo y comprobaciones del cuerpo de cámara en las 12 tomas. Son evidencia complementaria; esta ejecución no repitió todas las bisagras ni todos los movimientos de cajones y electrodomésticos. El giro orbital del visor tampoco equivale a un recorrido peatonal con colisiones físicas.

El consolidado propio contiene 239 controles geométricos: 238 dentro del criterio y uno pendiente. Ese recuento no sustituye la nota arquitectónica.

## Bloqueos y criterios observables de cierre

### C1 — Interferencia real entre agua y fondo de piscina

**Confirmado por malla, rayos y volumen.** Cresta del agua −0,030 m; coronamiento +0,070 m: resguardo correcto de 100 mm. Nueve rayos sitúan la playa húmeda en −0,080 m, por lo que allí hay 50 mm de agua, no 160 mm.

El fondo del volumen de agua está a −1,504 m y el fondo de hormigón llega a −1,390 m: **114 mm de penetración**. Boolean EXACT mide aproximadamente **2,148717 m³** de solape. La lámina A08 lo declara correctamente, pero declararlo no lo resuelve.

**Cierre exigible:** ajustar el agua al interior real del vaso sin cambiar la cresta autorizada; comprobar fondo, paredes, escalones y playa con pruebas de intersección y una sección acotada. Repetir una imagen a ras de agua para descartar huecos ópticos. La filtración, impulsión, skimmer y desagüe requieren su proyecto hidráulico separado.

### V1 — Textiles y objetos de interior aún no fotográficos

**Observación visual directa:** dormitorio y dormitorio_acceso muestran una manta de espesor y superficie demasiado uniformes, con caída poco convincente; almohadas muy similares, con pliegues regulares. En vestidor, las prendas se leen como láminas repetidas, oscuras y alineadas, aunque su ancho haya sido corregido. En estudio, consola, mandos y ciertos equipos siguen pareciendo modelos esquemáticos. Varios sanitarios carecen del detalle y la variación óptica que permitirían leer cerámica, herrajes y encuentros con naturalidad.

No se cuestiona automáticamente su escala: tamaño plausible y apariencia fotográfica son controles diferentes.

**Cierre exigible:** tejidos con espesor, costuras y caída coherentes con gravedad, apoyos y compresión; prendas con volumen, cuello/mangas y separación física; detalles de fabricación plausibles en los equipos que quedan cerca de cámara. Validar con vistas amplias y acercamientos derivados del mismo modelo, sin retoque que oculte defectos de geometría.

### V2 — Huerta, suelo y paisaje insuficientes; pérdida de follaje en web

**Observación visual directa:** huerta conserva hojas de silueta plana y repetitiva, secuencias muy regulares en trepadoras, sustrato poco volumétrico y escasa variación de crecimiento. En exterior y cubiertas, el plano lejano y el horizonte forman una pradera demasiado uniforme, con integración débil de árboles y suelo.

El arbolado de Cycles mejoró. Sin embargo, en el visor muchas copas visibles en las fotografías pasan a ramas casi desnudas o pequeños puntos oscuros. Es un problema de correspondencia observable. Su causa concreta —exportación, alfa, material, visibilidad o nivel de detalle— todavía requiere diagnóstico; no se atribuye sin prueba a un mecanismo específico.

**Cierre exigible:** curvatura, inserción y variación botánica creíbles, suelo con relieve y transiciones, mejor contacto con el terreno y fondo con profundidad. Comparar cámara equivalente Cycles/web con las mismas copas y una captura próxima de hojas para demostrar que la exportación conserva su cobertura y material. Mantener implantación y centros del proyecto.

### V3 — Materialidad y luz aún divergentes entre imagen y visor

El visor actual sí tiene materiales PBR: la inspección encontró 66 materiales, 36 mapas de normales y 28 de rugosidad. Agua y vidrio declaran transmisión 1 e índices de refracción coherentes. Por tanto, **no corresponde repetir el antiguo diagnóstico de ausencia general de mapas o transmisión**.

Aun así, el raster presenta luz más plana, agua menos rica, ropa más uniforme y diferencias marcadas de exposición respecto de Cycles. En las fotografías, algunas superficies blancas, telas y piezas de mobiliario siguen demasiado homogéneas. La repetición, la escala de textura, el contacto y los detalles de borde pesan más que la cantidad de mapas.

Hay 33 luces de fuente registradas, pero el tratamiento raster tiene limitaciones y no reproduce automáticamente la iluminación de Cycles. El atlas GI aparece desactivado: no debe presentarse como una iluminación precalculada validada de R6K.

**Cierre exigible:** comparar exterior, estudio, dormitorio, baño y vestidor desde cámaras equivalentes; comprobar exposición, contraste, contacto, color y transmisión. Seleccionar una solución de iluminación viable para el visor y verificarla sobre el SHA final. No basta aumentar mapas o luces sin evaluar el resultado.

### V4 — Composición y modo progresivo aún no cumplen una entrega fotográfica

Varias vistas interiores recortan piezas cercanas o repiten primeros planos sin una toma complementaria suficiente del espacio completo. Vestidor pierde legibilidad en zonas oscuras; los baños son claros para inspección, pero sus vistas elevadas necesitan complemento a altura humana. Los encuadres técnicos de escalera y cubierta son útiles y no se consideran defectos por ser elevados.

En móvil, la arquitectura cabe en pantalla, pero exterior conserva mucho cielo y muro delantero; estudio deja grandes franjas de techo y piso. Ajustar el encuadre al aspecto evita recortes, pero no produce por sí solo una buena composición vertical.

El trazador progresivo funciona. En la prueba propia de estudio, después de **91,3 s desde la activación y 34,67 muestras**, la captura seguía visiblemente granulada. La construcción inicial de escena llevó aproximadamente 30 s. Esto no demuestra que jamás pueda converger; demuestra que el resultado observado todavía no estaba listo para presentación.

**Cierre exigible:** cámaras verticales compuestas para los espacios principales, tomas amplias complementarias y tratamiento consistente de exposición. Para el modo progresivo, declarar un criterio de convergencia observable y tiempo objetivo, comprobarlo con capturas y hardware identificado, y resolver el ruido mediante presupuesto, filtrado o estrategia de iluminación adecuada. Una captura aún ruidosa no acredita fotorealismo.

### C2 — Especificación incompleta del acabado vertical en zona húmeda

En el baño del monoambiente se ve ladrillo directamente expuesto al agua de ducha; también debe coordinarse la protección de los paños afectados en el baño alto. La documentación de pendientes, sumidero y capas de piso no demuestra por sí sola un acabado vertical lavable e impermeable compatible con ese uso.

Es un **punto no demostrado**, no una prueba de filtración ni una declaración de incumplimiento legal. Puede existir una solución compatible con la estética, pero debe estar especificada.

**Cierre exigible:** sección de encuentro piso–muro y perímetro de ducha, continuidad de impermeabilización, tratamiento de penetraciones y juntas, y especificación del acabado expuesto y su mantenimiento. Distinguir lo ya modelado de la propuesta; representar la consecuencia visual si cambia el acabado.

### C3 — La ventilación acústica está propuesta, pero su coordinación física no está cerrada

D08 sí contiene una estrategia y ubicación acotada: cajas P en X18,30…20,50 / Z2,80…4,30 / +6,68…+7,08, silenciadores de 1.500 × 600, espacios de servicio, ductos iniciales Ø200 y circuitos separados de impulsión y retorno. **No es correcto decir que falta toda estrategia o toda localización.**

La propia lámina señala que soportes y accesos deben comprobarse antes de modelar, y que terminales, caudal, presión, ruido y condensados requieren selección y dimensionamiento. La reserva dibujada aún no equivale a un montaje coordinado con cabios, nubes acústicas, extracción de combustión, registros y cubierta.

**Cierre exigible para plausibilidad digital:** esquema 3D y cortes que sitúen cajas, soportes, registros, conductos y terminales; acceso real de mantenimiento y conservación de los 3,20 m libres; separación funcional de tomas/expulsiones y combustión. Toda hipótesis dimensional debe seguir marcada P. La selección y comprobación profesional de caudales, atenuación y seguridad siguen siendo una etapa distinta.

## Lectura de las 19 imágenes

Todas corresponden al manifiesto R6K verificado. Esta tabla registra el control visual de la entrega, sin convertir cada vista en un dictamen estructural.

| Imagen | Lectura y acción pendiente |
|---|---|
| exterior | Arquitectura y escalonamiento claros; mejorar integración de terreno, horizonte y masas vegetales. |
| pileta | Agua Cycles más convincente; corregir volumen inferior y equilibrar la presencia del muro cercano. |
| huerta | Botánica y sustrato muy repetitivos; es uno de los puntos más débiles de realismo. |
| estudio | Tratamiento y distribución legibles; enriquecer equipos/materiales y complementar el encuadre cercano. |
| cocina | Nueva distribución coherente; mejorar contacto, detalle y variación moderada de superficies. |
| quincho | Barra y mesa responden a la corrección; revisar luz del rincón de servicio y fabricación del equipamiento. |
| dormitorio | Orientación correcta; manta, almohadas y cortina requieren mayor credibilidad física. |
| dormitorio_acceso | Confirma la distribución; repite los defectos textiles y necesita una vista más amplia complementaria. |
| vestidor | Se corrigió la antigua obstrucción de cámara; prendas y exposición siguen siendo débiles. |
| bano | Compacto y legible; completar acabado húmedo y una toma a altura humana. |
| bano_acceso | Útil para disposición; la vista elevada y materiales uniformes limitan su lectura fotográfica. |
| puerta_bano | Explica el vínculo; hoja cercana domina el encuadre y corta la percepción del conjunto. |
| mono_cocina | Alturas y apoyos mejorados; luminarias y acabados aún demasiado genéricos. |
| mono_distribucion | Buena lectura funcional; sofá, tejidos y luz uniforme todavía sintéticos. |
| bano_mono | Rociador y lavabo coherentes; falta demostrar acabado vertical húmedo compatible. |
| bano_mono_sanitarios | Sanitarios de tamaño plausible; detalle y respuesta óptica aún esquemáticos. |
| bano_quincho | Giro del WC y lavabo mejor coordinados; mejorar cerámica y encuentros próximos. |
| escalera | Buena evidencia del ensamblaje; mantener detalle acotado y no atribuirle capacidad calculada. |
| cubiertas | Útil para escalonamiento y remates; completar coordinación de sistemas y calidad del entorno. |

La referencia original tiene mayor profundidad paisajística y una integración más natural de luz, vegetación y materiales. No obliga a reproducir su geometría ni una hora solar específica. Las nuevas cotas, el techo de estudio más alto y las decisiones de distribución deben conservarse al mejorar las imágenes.

## Visor: funcionamiento comprobado y límites

Se probaron 13 vistas, los 13 controles de puertas y el corte de planta, además de escritorio, retrato 390 × 844 y paisaje 844 × 390. No se detectaron errores de página ni desbordamiento horizontal. El corte desactivado elimina sus planos y rótulo correspondiente. El estado público informa «En revisión · aprobación 9,5 pendiente».

La prueba empleó Chrome con GPU real NVIDIA RTX 3060 Ti mediante ANGLE, no un teléfono físico. La carga local inicial fue de 22,7 s y la pública de 30,3 s en estas ejecuciones. La carga móvil de 5,2 s reutilizó el contexto de pruebas y no representa una medición de red y teléfono independientes. El GLB pesa aproximadamente 101,8 MB, por lo que corresponde medir descarga, memoria y respuesta en dispositivos reales antes de afirmar buen rendimiento móvil general.

La escena contabiliza 5.047 mallas en runtime y 1.586 llamadas de dibujo en la medición recogida. Los 11,27 millones de triángulos reportados por el renderer incluyen pasadas de render; no se presentan como cantidad única de triángulos del modelo.

Los controles son utilizables y la publicación está identificada con honestidad. Las pérdidas de follaje, la discrepancia de luz y el ruido progresivo impiden equiparar este visor con las fotografías Cycles o declarar calidad fotográfica general.

## Documentación, inferencias y límites profesionales

Las 33 A2 son vectoriales, sin imágenes raster incrustadas. Fuente mínima observada de aproximadamente 2,50 mm; no se detectaron palabras fuera de página. El ZIP pasa la prueba de integridad y contiene 33 SVG, 33 DXF y 195 entidades DIMENSION nativas contadas independientemente. Se comprobaron las correcciones de referencias locales, P11, La Matanza, cotas reales de cubierta, D03, D11 y la advertencia de piscina en A08.

Los datos de Virrey del Pino, La Matanza, orientación norte y redes disponibles proceden del propietario y la documentación: no sustituyen mensura, azimut topográfico, niveles de conexión o confirmación de prestaciones de las redes.

- **Verificado:** mallas, cotas, contactos, hashes, legibilidad y funcionamiento expresamente enumerados; apariencia de las capturas inspeccionadas.
- **Inferido o propuesto:** montaje constructivo donde falta especificación, hipótesis de utilización y mobiliario genérico, detalles P de ventilación y apoyos sin cálculo. Se explicita qué evidencia permitiría cerrarlos.
- **No comprobable con esta entrega:** capacidad de fundaciones, estructura y uniones; suelo, viento y acciones; estanqueidad ensayada; caudales, presiones y seguridad de instalaciones; prestaciones acústicas; cumplimiento integral de normativa y permisos.

La escalera medida requiere comprobación competente de huella, contrahuella, baranda y uso para la jurisdicción y categoría correspondientes. No se inventa una regla aplicable ni se considera que un barrido sin colisiones pruebe cumplimiento.

Para transformar el estudio digital en documentación apta para construir se necesitarán relevamiento y suelo, cálculos estructurales y planos de armado/uniones, proyectos de instalaciones y drenaje, especificaciones completas de envolvente e impermeabilización, selección y prestaciones de carpinterías, y definición acústica con objetivos y verificaciones. Ese trabajo profesional es distinto de la aprobación visual. **La falta de una firma profesional no es la razón por la que se rechaza aquí el 9,5: la entrega digital tiene defectos observables propios.**

## Tres pasadas exigibles antes de la próxima revisión global

1. **Geometría y coordinación.** Corregir el volumen de agua; definir el acabado húmedo y sus encuentros; coordinar físicamente la propuesta de ventilación acústica y acceso de servicio. Mantener cotas, arquitectura y distribución aprobadas. Entregar secciones G/P, ensayos de solape/contacto y reservas de uso del mismo archivo guardado. No reabrir sistemas ya cerrados sin una razón nueva.

2. **Materiales y elementos próximos a cámara.** Rehacer la caída de manta, almohadas y prendas; mejorar botánica de huerta, suelo y transición de paisaje; desarrollar los detalles de equipos y sanitarios que se ven de cerca. Revisar escala, juntas y respuesta material con acercamientos y vistas amplias. Las mejoras deben existir en el modelo exportable, no sólo en un retoque de imagen.

3. **Correspondencia web, luz y composición.** Resolver la pérdida de follaje y divergencias ópticas, componer vistas verticales, dar tomas complementarias de ambientes y alcanzar un resultado progresivo convergido dentro de una estrategia de rendimiento declarada. Entregar nuevo SHA único con las 19 imágenes, planos afectados, GLB, metadata y capturas de escritorio/móvil; repetir sólo los controles pertinentes a los cambios y una comprobación de integridad general.

La siguiente auditoría debe puntuar el resultado real. Completar tres pasadas, aumentar muestras o aportar más documentos no concede automáticamente 9,5. Para aprobar, deberán cerrarse los defectos geométricos relevantes, quedar explícitas y coordinadas las propuestas constructivas del alcance digital y sostenerse el realismo en exterior, interiores y la presentación web elegida.


## Nuevo umbral de 9,9: condiciones de aceptación para la próxima entrega

El aumento solicitado no modifica retrospectivamente la nota de R6K ni concede puntos por intención. Para considerar 9,9, la siguiente versión deberá satisfacer conjuntamente estas condiciones:

| Condición | Evidencia exigible |
|---|---|
| Geometría coordinada sin defectos mayores conocidos | Cierre de C1 y de todo nuevo solape duro o apoyo discontinuo encontrado; medidas y reservas de uso conservadas, con secciones y pruebas de la fuente final. Una exclusión global de familias en los tests no demuestra cierre. |
| Materiales y objetos próximos a cámara convincentes | Las 19 vistas finales y acercamientos al tamaño de exportación deben sostener escala, espesor, contacto y comportamiento material: sin mantas rígidas, prendas laminares, repeticiones evidentes o artefactos genéricos dominantes. No se exige suciedad artificial para aparentar realismo. |
| Paisaje integrado | Huerta, copas, suelo y fondo con volumen, variación y crecimiento plausibles; sin hojas flotantes, masas que desaparecen en exportación ni horizonte de plano uniforme que delate el montaje. |
| Luz y acabado de imagen | Luz, exposición, reflejos y profundidad coherentes en exterior e interiores; sin ruido visible que distraiga, zonas funcionales ilegibles, reflejos rotos o texturas estiradas. Revisar al tamaño nativo de entrega, además de las miniaturas. |
| Correspondencia Cycles/web | Comparativas desde cámaras equivalentes de exterior, estudio, dormitorio, baño y vestidor. Conservar geometría, materiales, cobertura vegetal y carácter de iluminación. La navegación raster puede identificarse como previsualización; el modo presentado como fotográfico y la galería deben demostrar el resultado final sin sustituir silenciosamente el modelo por una imagen ajena. |
| Presentación móvil y escritorio | Encuadres propios para retrato y paisaje, controles legibles, ausencia de desbordamientos, prueba real de carga y respuesta en al menos un dispositivo móvil representativo y un escritorio identificado. Definir tiempo y criterio de convergencia del modo fotográfico; no presentar una captura todavía ruidosa como objetivo cumplido. |
| Construcción plausible y documentación sincera | C2/C3 coordinados en el alcance digital, propuestas P identificadas y coherentes con planos/modelo. Las prestaciones que requieren cálculo o ensayo deben permanecer explícitamente pendientes, sin convertir la calificación visual en certificación ejecutiva. |
| Una sola versión verificable | Modelo, GLB, fotografías, PDF, editables y metadata de una misma fuente congelada; manifiestos y comparación pública. Cualquier retoque de exposición debe ser declarable y no ocultar geometría incorrecta. |

La crítica deberá revisar tanto imágenes generales como detalles y comprobar una muestra representativa de interiores, exterior, paisaje y móvil. **La condición fotográfica no se satisface con una única imagen excepcional.** Tampoco se otorga 9,9 por promediar notas altas de documentación con un área visual débil.

Las tres pasadas propuestas arriba siguen siendo el orden de trabajo. Tras ellas se emitirá una nueva nota independiente; si el resultado aún muestra defectos relevantes, continuará por debajo de 9,9 aunque todas las tareas previstas se hayan ejecutado.

## Evidencia reproducible

Pruebas propias:

- audit/critica_dimensional_r6k.md — tabla de 54 familias y dictamen parcial.
- audit/integral95_02_consolidated_dimensions.py y audit/integral95_02_r6k_consolidated_dimensions.json — mediciones y 239 controles.
- audit/integral95_dimensions_Casa_de_Campo_95_R6K.json y .csv — inventario completo evaluado.
- audit/integral95_02_r6k_dimension_families.json y audit/integral95_02_r6k_dimensional_outliers.json — familias y señales contextuales.
- audit/integral95_02_r6k_dvh_final.py/.json/.log — 71 pares y contactos.
- audit/integral95_02_r6k_bench_pool_clarification.py/.json/.log — contacto del banco y solape real del agua.
- audit/documental_r6k/metadata.json, checks.json y page_01…33.txt — revisión del PDF y los editables.
- audit/integral95_02_visual/verified_manifest.json y contact_01…03.jpg — integridad y lectura de imágenes.
- audit/integral95_02_web_checks.mjs y audit/integral95_02_web/checks.json — pruebas locales, controles, materiales y rendimiento.
- audit/integral95_02_web/estudio_progressive.png, capturas de ambientes y móvil — resultado visual observado.
- audit/integral95_02_public_confirmation.mjs, audit/integral95_02_web/public_confirmation.json y public_exterior.png — confirmación pública de la entrega.

Evidencia complementaria del constructor, no presentada como repetición independiente completa: review95/r6j_construction_checks.json, review95/r6j_furniture_door_checks.json y review95/r6f_route_body_checks.json, con su fuente declarada y alcance; los nombres históricos no deben confundirse con una nueva prueba propia sobre cada estado de R6K.

**Decisión final: R6K obtiene 8,3/10 y puede permanecer publicada como estudio digital en revisión. No alcanza 9,5 ni el nuevo umbral de 9,9/10; no se afirma hiperrealismo general y no es documentación certificada para ejecutar obra.**
