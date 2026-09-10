# Crítica parcial de mobiliario y uso — R5D y comprobaciones R6A

**R5D: 6,0/10 en distribución, apoyos y posibilidad de uso. No aprobado.** Hay avances claros en dormitorio, quincho y comedor, pero la cocina del monoambiente no puede funcionar con los volúmenes actuales. Este puntaje no evalúa fotografías nuevas de R5D, que todavía no estaban disponibles al cerrar la inspección.

**Correcciones puntuales R6A: 8,5/10 en el subconjunto sofá–vanitory–rack–cotas de sanitarios.** Cierran los fallos medidos en ese subconjunto. No equivale a aprobar todo R6A: siguen pendientes la cocina mono, los apoyos restantes, el cajón del vestidor y la nueva distribución de los baños.

El criterio integral permanece en **9,5/10 con apariencia fotográfica imprescindible**. Una comprobación geométrica satisfactoria no puede compensar una imagen insuficiente ni certificar estructuras, instalaciones o cumplimiento normativo.

## Fuentes y método

- R5D: `output/Casa_de_Campo_95_R5D_preview.blend`, SHA256 `614ef565264654054365a57438357a889f1be15028d6ba72075d3dd10dca72fc`.
- R6A: fuente y SHA en `integral95_02_r6a_furniture_geometry.json`.
- Coordenadas de proyecto: X horizontal, Y altura, Z profundidad; metros.
- Mallas evaluadas al reabrir archivos guardados; inventario de596 objetos de mobiliario y apoyos, seguido de inventario geométrico del edificio y pruebas de pares seleccionados.
- BVH de triángulos para confirmar cruces reales. Un solape de cajas no se presenta como profundidad normal exacta; contactos coplanares de apoyo se distinguen de penetraciones.
- Las huellas de operador de600mm, retirada de silla350mm y extracción de cajón450mm son **hipótesis P de estudio de uso**, no requisitos normativos ni mecanismos certificados.
- No se modificó ningún modelo ni se renderizó vídeo.

## Hallazgos prioritarios del estado R5D

| Ambiente / objeto | Hecho comprobado | Corrección o cierre |
|---|---|---|
| Cocina mono | Isla y mesada posterior se cruzan. Base isla terminaZ4,93 y bajo posterior empieza5,02:90mm. Tapas se solapan Z4,86..5,04. BVH confirma cruce. | Rehacer la L y adelantar isla según propuesta acotada adjunta. |
| Heladera mono | Ocupa los bajos lateral y posterior: intersecciones reales con ambos. | Ubicar en paño posterior al oeste del acceso doble. |
| Frentes cocina mono | Laterales orientados hacia−X contra pared; posteriores hacia+Z contra tabique. | Frentes lateral+X, posterior−Z; isla desde+Z. |
| Estar vivienda | Respaldo invade tabique90mm, base70mm. | **Cerrado en R6A:** conjunto+Z110mm; distancia posterior20mm. |
| Vanitory suite | Dos cuerpos superpuestos; cuerpo y mesada penetran tabique hasta120/130mm de caja. | **Cerrado en R6A:** un cuerpo; mesadaX19,495..20,065 con5mm respecto muroX19,49. |
| Rack estudio | Dos cuerpos bajo piso120mm; base3,075..3,125 totalmente dentro de losa3,00..3,20. El volumen contenido ilustra por qué un BVH sin cruces de superficies no basta. | **Cerrado en R6A:** un gabinete, base3,25..3,31 y bandejas/chasis. |
| Sanitarios | WC PB penetran piso55mm; WC suite30mm y bidet40mm. Asientos de WC PB520mm y suite555mm sobre pavimento. | **Cerrado en R6A:** cuerpos desde pavimento, asientos455mm, bidet420mm. Son dimensiones propuestas; falta seleccionar producto real. |
| Mueble apoyo estudio | Fondo inferior3,43 sobre piso3,25:180mm sin pieza de apoyo bajo su huella. | Añadir patas/base o fijación mural real; no hay pared inmediata que justifique un voladizo. |
| Mueble TV | Fondo inferior3,28 sobre piso3,25:30mm sin patas/base identificables. | Incorporar apoyo. Definir frentes: en R6A quedan345mm hasta mesa baja; no cabe un cajón de400mm sin interferir. |
| Armario vestidor | Laterales/respaldo a3,28:30mm sobre piso; zapateros a3,265:15mm. | Zócalo/patas y soporte de módulos. |
| Lavatorios PB | Bordes a0,81 sobre piso0,21:600mm de altura. Lavatorio mono no presenta apoyo inferior ni encuentro con muro. | Reubicar a altura de uso adulto propuesta y representar mueble/ménsulas. |
| Baño quincho | WC original mira al muroZ10,17; frente de tazaZ10,49:320mm disponibles. | Giro180° propuesto hacia acceso; ver condición geométrica siguiente. |
| Baño mono | Taza empiezaZ5,11 frente a plato que termina5,01:100mm entre ambos, dentro de la misma franjaX del WC. | No rotular100mm como circulación. El uso invade la superficie de ducha elevada; redistribuir o declarar y resolver explícitamente el sector húmedo compartido. |

## Uso y cierres comprobados

**Comedor / cocina de vivienda.** Con sillas retiradas350mm, las cajas reales dejan aproximadamente0,981m hasta la envolvente propuesta del operador del horno,0,831m hasta la de heladera y0,814m hasta la mesa baja. El espacio ha mejorado. No se afirma funcionamiento de electrodomésticos: sus hojas no están articuladas en el modelo y las envolventes continúan comoP.

**Dormitorio.** Cama, cabecero y ventana siguen la orientación corregida. Patas de cama y mesas de luz llegan a piso; lámparas apoyan en las tapas. La nueva manta deja aproximadamente616mm hacia la envolvente de cortina en el tramo útil y810mm hacia el tabique opuesto, fuera de las mesitas en cabecera. No se exige pasar entre cama y mesita: el acceso a las caras laterales ocurre desde los pies.

**Quincho.** Mesa750mm, asientos460mm y patas/regatones apoyados en piso. Barra paralela a parrilla; paso de trabajo nominal mínimo1,13m. La retirada de350mm de sillas posteriores permanece sobre el pavimento. Se distingue esta mejora del problema independiente del baño.

**R6A sanitario.** Reapertura confirma bases de WC exactamente en0,21/3,25 y asiento455mm; bidet420mm. Los triángulos que coinciden con la cara del piso son contacto de apoyo, no penetración.

**R6A estar.** El sofá deja20mm respecto tabique; la mesa baja desplazada+Z150mm conserva410mm hasta frente del sofá. La apertura del muebleTV requiere una solución de frente compatible con los345mm disponibles.

**Cajones de vestidor.** Extracción conceptual+Z450mm,21posiciones por cajón, contra mallas fijas cercanas: cajones1 y2 sin cruces. Cajón0 atraviesa el estante3,64 en12,5mm durante todas las poses. Propuesta: cajaY3,665..3,905, con12,5mm inferior y25mm hasta siguiente cajón; representar las guías y verificar el nuevo conjunto.

**Baño quincho propuesto.** El giro180° con centroX21,53/Z10,58 libera cerca de0,94m al frente de taza. Lavatorio al norte y taza no se cruzan en sus huellas propuestas. La medianera interior está enX21,80: la envolvente inicialmente dibujada hasta21,83 penetraba30mm. Puede ubicarse la envolvente de usuario delante enX21,195..21,795/Z10,89..11,49, con desplazamiento lateral35mm respecto eje de taza. No supone accesibilidad reglamentaria ni uso simultáneo de dos personas. Debe comprobarse tras modelar.

## Propuesta mono acotada

Archivos: `integral95_02_mono_layout_proposal.json`, `.svg` y `.png`. La lámina es un diagrama de coordinación de huellas; la envolvente está simplificada y no reemplaza una planta arquitectónica completa de aberturas.

- L lateral X14,24..14,86/Z3,20..5,82; retorno X14,24..15,78/Z5,20..5,82.
- Heladera X15,84..16,54/Z5,10..5,82, frente−Z.
- Isla tapa X15,96..17,68/Z3,32..4,00; base retrasada aZ3,57 para voladizo250mm al norte.
- Pasos con muebles cerrados:1,10m lateral,1,20m posterior,1,10m frente a heladera; franja al este de isla1,57m hacia acceso doble.
- Sofá completo−Z700mm; taburetes−Z770mm; mesa y sillas+X1150mm/−Z740mm.
- Mesa750mm sobre piso, silla460mm, mesada900mm y taburete650mm.
- Taburete retirado350mm conserva630mm hacia sofá; silla norte retirada conserva660mm a fachada.
- **Puerta de baño real:**41poses frente a mesa/sillas propuestas normales y retiradas350mm, cero intersecciones.
- Con puerta abierta, queda283mm hasta la silla retirada: esa ranura no es un paso. La aproximación se hace por oeste desde la franja al este de isla.
- El uso de heladera ocupa temporalmente el pasillo de trabajo; la circulación general se desvía al este de la isla. No se promete1m detrás del usuario con heladera abierta.
- El sofá cama no tiene mecanismo desplegado modelado: se debe comprobar posición nocturna y almacenamiento de taburetes antes de afirmar su funcionamiento.
- Campana/extracción del mono, conexiones y holguras de equipos requieren coordinación; este esquema no las acredita.

## Puntajes de entregas parciales anteriores

- **Imágenes interiores R5A,7vistas:7,0/10.** Mejora de encuadres, DAW alineado y distribución; siguen subexposición de dormitorio, campana desconectada y materiales/mobiliario de lectura esquemática.
- **Puertas corregidas R5A2/R5C_preview:9,0/10 en geometría de giro/articulación.** Cuatro batientes conservan cierre y libran41poses; estudio18piezas móviles frente186fijas libra41poses sin exclusiones de marcos/herrajes.96rayos verifican holgura radial0,199–0,200mm en bisagras. No es puntaje del edificio ni certificación de herrajes.

## Evidencia reproducible

- `integral95_02_furniture_r5d.json`:inventario de596 objetos.
- `integral95_02_r5d_furniture_geometry.json/.py/.log`:mallas y pares confirmados.
- `integral95_02_r6a_furniture_geometry.json/.py/.log`:reapertura de correcciones.
- `integral95_02_r6a_drawer_use.json/.py/.log`:extracción de cajones.
- `integral95_02_mono_proposal_door.json/.py/.log`:puerta frente a muebles propuestos.
- `integral95_02_mono_layout_proposal.json/.svg/.png/.py`:coordenadas, hipótesis, dibujo y generador.
- `integral95_02_r5_checkpoint.json`:fotografías inspeccionadas y pruebas previas de puertas.

Quedan pendientes el modelo consolidado, los planos concordantes, las nuevas fotografías y el visor correspondiente. La calificación integral se emitirá sobre ese paquete congelado.
