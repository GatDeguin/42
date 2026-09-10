# Auditoría dimensional preliminar R6F

**Nota parcial de coordinación dimensional y uso: 7,5/10. No es la nota integral ni aprobación del umbral 9,5.** Las dimensiones generales y numerosas alturas de mobiliario son coherentes; los encuentros de escalera, sellos, puesto de trabajo y nivel de agua todavía impedían cerrar el candidato examinado. Las correcciones anunciadas después requieren una nueva comprobación del consolidado.

Fuente: `output/Casa_de_Campo_95_R6F_route.blend`, SHA256 `91cdd8b058b68caf6bc1797e13f216bd7bd1d45652dbe37603895cc92b98bfbc`.

El inventario evaluado contiene 4845 objetos geométricos; 4392 están habilitados para render por objeto y colección. Se registraron además 57 envolventes de instancias evaluadas, y 68 contenedores/elementos sin malla propia en una lista explícita. Unidades métricas, factor1. Las 309 transformaciones con escala distinta de1 se registraron, sin confundirlas con dimensiones físicas incorrectas. Ninguna matriz mundial tiene determinante negativo. El JSON/CSV conserva también alternativas ocultas.

Se agrupó una primera tabla de54familias de mobiliario, sanitarios y equipos. Sus miembros y cajas reales están identificados; una caja envolvente no sustituye un claro útil, espesor normal o ficha comercial. La tabla es base de interpretación y no una aprobación automática de cada producto.

Medidas verificadas representativas:

| Elemento | Medida o cota G | Interpretación |
|---|---:|---|
| Lote |22×20m|Huella del terreno de la fuente |
| Losa principal / implantación |8×12m; X14–22/Z0–12|Conservada |
| Losa entre plantas |+3,00 a+3,20m|20cm; el piso terminado está a+3,25 |
| Vivienda / estudio |2,60 /3,20m libres|Cielorrasos+5,85/+6,45 sobre piso+3,25 |
| Desnivel entre cubiertas equivalentes |0,60m|Faldón del módulo estudio elevado |
| Escalera |18peldaños, ancho1m, contrahuella177,22mm|Huella entre frentes211,11mm; tabla223,11mm con vuelo. Verificar adecuación normativa con fuente aplicable; no certificada |
| Desembarco |1×1m estructural|Terminación y enlace al acceso a comprobar como conjunto |
| Vaso de piscina |7×3m exterior|Interior entre muros6,76×2,76m; no confundir exterior con espejo libre |
| Solárium |1m alrededor del vaso|Retiro del vaso2m a límites posterior y derecho |
| Sofás |asiento450mm|Tres ambientes; respaldo total860mm |
| Sillas |460mm mono/quincho;470mm comedor/estudio|Superficies de asiento sobre piso real |
| Mesas principales |750mm|Mono, quincho y comedor |
| Mesa baja |400mm|Vivienda |
| Mesadas/isla |900mm mono y quincho|PA~908mm, medida del conjunto existente |
| WC / bidet |455 /420mm|Alturas de asiento/borde |
| Lavatorios PB |850mm|Borde respecto del piso+0,21 |
| Bacha apoyo suite |870mm|Mesada770mm más cuenco100mm |
| Colchón |~1,727×1,901m; cara superior605mm|Genérico sin fabricante; no denominar medida comercial estándar |
| Bañera |1,25×0,74×0,54m|Compacta/asiento; producto por seleccionar |

Bloqueos y outliers reunidos en esta tanda:

1. **24 barras legacy de acristalamiento** en seis familias llenan la sección9+17+9 de los DVH. La prueba propia confirmó48pares barra–cristal. No son compresión de EPDM. Los ocho posteriores ya se habían retirado; estas piezas permanecían en mono, ventanas y corredizas laterales.
2. **Escalera:** bajo el peldaño superior quedan39,50mm de aire hasta su soporte; los quince primeros presentan separaciones decrecientes, y los tres inferiores penetraciones. Los antideslizantes conservan las alturas antiguas: el superior queda45mm enterrado. Los rayos verticales confirman que no existe calzo oculto en el eje medido.
3. **Consola:** cara inferior frente a+3,723 frente al asiento+3,720: sólo3,4mm de espacio sobre asiento, con base maciza que invade la zona de piernas. La longitud3,35m no es por sí sola imposible; el fallo está en la sección de uso.
4. **Ducha mono:** cara inferior del rociador a1,75m sobre piso; requiere elevarla y conectar el conjunto. **BañoPA:** permanece un segundo cabezal legacy bajo, aparte del rociador nuevo.
5. **Banco huerta:** bloque/asiento a560mm sobre referencia de apoyo; construcción y altura deben resolverse como banco real. Los taburetes650mm mantienen altura coherente, pero su aspecto de bloques requiere el montaje de mobiliario anunciado.
6. **Piscina:** agua a+0,0825 supera12,5mm el coronamiento+0,070, sin rebalse resuelto. Se requiere cota operativa y resguardo o proyecto de rebalse. El constructor propone−0,030; todavía no está en esta fuente.
7. **Bañera compacta:** no atribuir capacidad de inmersión adulta extendida ni medidas comerciales a un objeto genérico de1,25m.

Las cinco correcciones previas R6E se reprodujeron también en R6F: bacha libre de bajos, duplicados retirados, paneles/patines TV sin choques en41posiciones propuestas y canales de guías telescópicas sin choque entre etapas en21posiciones. Estos ensayos geométricos no equivalen a resistencia, vida útil ni funcionamiento certificado de un herraje comercial.

Pendiente para el cierre integral: revisar el consolidado con todos estos cambios, medir claros reales de13rigs y configuraciones de uso de equipos/sofá cama, verificar la concordancia del plano y GLB, y examinar las imágenes finales. Las huellas de usuario son propuestas explícitas, no comprobación antropométrica universal ni accesibilidad normativa. Cálculo estructural, selección de productos, hidráulica, acústica y proyecto ejecutivo siguen diferenciados de la geometría.

Evidencias propias:

- `integral95_dimension_inventory.py`, JSON/CSV `integral95_dimensions_Casa_de_Campo_95_R6F_route.*`.
- `integral95_02_r6f_dimension_families.json`:54familias y cotas, con miembros explícitos.
- `integral95_02_r6f_stair_datums.json`:18encuentros de peldaños.
- `integral95_02_r6f_dimensional_probes.py/.json/.log`:48pares de acristalamiento, rayos de apoyos y secciones de consola.
- `integral95_02_r6f_assemblies.py/.json`:bacha, duplicados, TV y etapas de guías.
- `protocolo_auditoria_dimensional_95.md`:alcance y reglas para la revisión final.
