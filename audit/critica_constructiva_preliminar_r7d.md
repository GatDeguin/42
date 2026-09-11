# R7D — revisión constructiva preliminar independiente

**Hay progreso geométrico comprobable, pero la mecánica de los herrajes sanitarios todavía tiene interferencias reales.** La maniobra de mantenimiento de D08 está completando su evidencia documental. Esta revisión preliminar no asigna puntaje global ni aprueba el umbral de 9,9/10; quedan por revisar las imágenes, los planos completos y el visor final coherente.

Fuente examinada, abierta sin guardar: `output/Casa_de_Campo_99_R7D.blend`, SHA256 **9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e**. No se usó GPU ni se renderizó vídeo.

## Hallazgos que requieren acción

### P1 — SAN99: pedestal/eje fijo invaden los herrajes móviles

**Confirmado de forma independiente por Boolean EXACT sobre geometría evaluada y por muestras de giro.** En los tres WC se repite la misma construcción de bisagra. El barrido interno propio ensayó 92 pares candidatos; 63 resultaron con volumen positivo. Se distinguieron **30 pares fijo–móvil** de las 33 uniones entre componentes solidarios o fijos. No se califican automáticamente las 63 intersecciones como 63 defectos independientes.

Por cada bisagra:

| Interfaz | Intersección aproximada |
|---|---:|
| Pedestal fijo ↔ manguito móvil del asiento | 347 mm³ |
| Pedestal fijo ↔ brazo móvil del asiento | 247 mm³ |
| Pedestal fijo ↔ manguito móvil de tapa | 49 mm³ |
| Pasador fijo ↔ brazo móvil del asiento | 114 mm³ |
| Pasador fijo ↔ brazo móvil de tapa | 104 mm³ |

En el WC mono, la intersección manguito–pedestal persiste en 0°, 30°, 60° y 90°. También persiste brazo–pasador. No son un mero contacto tangente ni una interferencia sólo en una pose intermedia.

**Cierre solicitado:** representar una unión en la que pedestal y pasador fijos no ocupen el espacio de los elementos que giran; definir alojamientos/holguras y partes solidarias. Comprobar por separado grupos móviles de asiento y tapa contra las partes fijas, incluyendo brazos, manguitos y pasadores. No basta volver a ensayar solamente asiento/cuerpo/cisterna/tapa: el control sanitario actual omite estas relaciones internas.

No se pide rehacer la implantación ni cambiar la huella de los artefactos. Los solapes de un brazo insertado en su propio asiento, manguito unido a su propio brazo o tornillo unido a pedestal pueden ser relaciones constructivas deliberadas; deben distinguirse de los cruces fijo–móvil.

Prueba adicional de tapa del WC mono: no intersecta la cisterna en 0°, 45° ni 90°; a 100° entra aproximadamente 0,000890 m³. **100° no se establece como requisito de diseño.** Se pide declarar y representar un tope/ángulo operativo compatible si se pretende superar los 90° o justificar la retención en su pose abierta. Una tapa estática a 90° no demuestra por sí sola el mecanismo de retención.

Evidencia: `audit/r7d_preliminary/geometry_probe.json`, `sanitary_joint_classification.json`, `mechanical_probe.json`.

### P2 — D08: completar el medio de acceso y la transferencia de piezas

La propuesta física ahora existe y es mucho más precisa que una reserva dibujada: equipos, soportes, conductos, registro y terminales están modelados; la cota mínima nueva es +6,453, equivalente a 3,203 m sobre el piso del estudio.

Las ocho envolventes del constructor comprueban aproximación y descenso inicial de filtros/silenciadores/ventiladores con listas explícitas de partes retiradas. **El descenso hasta H5,40 aún necesita enlazarse con una maniobra de recepción y traslado al piso**, además del medio para que el operario alcance el registro.

Se pidió al autor de planos una propuesta P con posición/nivel de plataforma, cuerpo/alcance, pieza retirada, equipo retenido y transferencia simultáneos. La primera idea de tablero H4,85 fue descartada: un cuerpo de 1,72 m terminaría en H6,57, por encima del cielorraso H6,45. El autor está probando otro emplazamiento a H4,65. No se aprueba ese mecanismo por intención; incorporar únicamente la maniobra que pase el ensayo real y dejar selección/capacidad/estabilidad del medio auxiliar como pendientes profesionales.

Esto no invalida publicar una candidata parcial que lo declare; impide presentar el mantenimiento como completamente resuelto antes de aportar la maniobra.

### P3 — Cota útil de nueva puerta y tablas de sanitarios

El autor de planos entregó la medición R7D al frame 150: cierre por galce/junta X16,6045036; hoja abierta X17,4525013; extremo interior de manija X17,4105015. Informa **848,0 mm en la garganta Z8,93…9,07 y 806,0 mm conservadores** proyectando también la manija sobre toda la profundidad de hoja. A03b/A12 incorporarán esas cotas con método, separadas de los 923 mm entre jambas y del vano de 1,00 m. **Los 813 mm de la versión anterior no son la cota R7D.** Es una medición del autor contrastada con el cambio de herrajes, pendiente de leer en las láminas; no es ancho universal de circulación junto a la cama ni una certificación de accesibilidad.

A09 debe distinguir cuerpo, asiento y envolvente total. La tapa abierta eleva el conjunto hasta 923 mm sobre NPT; no conservar 770 mm como altura total. El autor de planos confirmó que actualiza la proyección y tabla desde R7D.

### Menor — topología de capas húmedas PB

La membrana y el adhesivo de PB conservan tres aristas de borde cada uno alrededor del paso del lavatorio, cerca de X20,524 / H0,768. Forman un triángulo casi degenerado de área 1,03 × 10⁻⁹ m² y altura equivalente de **0,583 µm**. Es un detalle de limpieza topológica; **no demuestra filtración, discontinuidad apreciable del encuentro ni un bloqueo de publicación**. Los informes sólo verificaban ausencia de aristas no manifold en cerámica, no en cada capa oculta.

El paño anterior del vestidor también presenta aristas en la malla sin soldar; una prueba temporal de unión de vértices a 1 µm elimina las 120 aristas de borde. Es una costura coincidente de topología, no una abertura física de pared detectada. No se modifica el modelo para este diagnóstico.

## Comprobaciones independientes favorables

| Elemento | Resultado observado |
|---|---|
| Alturas principales | Piso PA +3,25; cielorraso de estudio +6,450; nubes acústicas con cara inferior +6,450. Vivienda/baño alto +5,850. Conservan 3,20 y 2,60 m respectivamente. |
| Distribución | Vestidor cerrado hacia estar; aparecen los rigs dormitorio–estar, dormitorio–vestidor, vestidor–baño y baño–comedor; falta suiteEntry como corresponde. Baño PB en X19,39…21,80 / Z0,26…1,81, junto a fachada y medianera. |
| Escala SAN99 | Cuerpos de WC mono/quincho 420 × 620 × 430 mm; suite 450 × 660 × 430 mm. Asientos 380 × 445 mm, cara superior a 455 mm sobre NPT. Son dimensiones medidas de producto genérico, no homologación. |
| Apoyos de asiento/cisterna | 18 apoyos, cinco estaciones por apoyo y contacto inferior/superior: 180 interfaces por rayos. Sin separación positiva. Una penetración local de unos 0,040 mm en borde curvo de un apoyo de cisterna del quincho. |
| Capas de paño húmedo | 18 estaciones frontales PB/PA: cerámica de 8 mm, adhesivo de 4 mm y membrana de 2 mm, sin separación entre las capas en las estaciones examinadas; PA añade base de 51 mm. No equivale a ensayo de estanqueidad de todo el baño. |
| Llenador y mando PA | Existen cuerpos empotrados, collar y roseta que ocupan la anterior separación de 35 mm; los extremos enlazan con el caño/mando conservado y el terminado frontal Z6,165. Cerrar lectura constructiva con D11. |
| Apoyo de D08 a cabios | Se localizaron 22 placas conformadas. Las 44 estaciones laterales de contacto placa–cabio quedan dentro de aproximadamente 1 µm. Los rayos de centro no se usan como única prueba por taladros y encuentros. Esto acredita contacto geométrico, no resistencia de anclajes. |
| Zócalo huérfano | El objeto Zócalo columna cocina está eliminado del modelo y del inventario de integración; los actuales sanitarios/mesadas no dependen de ese resto. |

## Evidencia del constructor contrastada, no repetida íntegramente

Se leyeron scripts y resultados de `review99/r7d_integrated/`, todos vinculados a la misma fuente en los controles finales:

- Agua: 14 sólidos y 72 estaciones de contacto; un volumen cerrado, fondo −1,390, cresta −0,030 y envolvente nominal del vaso 7 × 3 m. No se conserva el antiguo conflicto de 114 mm como si siguiera vigente.
- Puertas de dormitorio: 41 poses por hoja, 886 pares sin interferencias, separación continua de barridos y cuerpo de 450 mm en 73 estaciones. La corrección de manos elimina el bloqueo anterior de acceso junto a la cama en el ensayo presentado.
- C2: 123 pares con entorno, sin choque duro; contacto coplanar submicrométrico señalado por separado.
- C3: 88 pares de entorno, ocho maniobras con exclusiones por desmontaje nominales; 65 pares internos sin choques y sin aristas no manifold en VENT99. Rutas y apoyos P, sin caudales, ruido o capacidades inventadas.
- SAN99: 167 pares externos y 15 relaciones internas principales sin choques. El hallazgo P1 demuestra el límite del alcance de esos 15 pares; no contradice que los pares concretos ensayados hayan pasado.
- Inventario común de cuatro escenas y pausa de vídeo; unidades métricas y escala 1. El recorrido de integración tiene 9.000 rayos sin impactos en memoria; la entrega debe conservar su enlace al archivo final.

Esta revisión no sustituye cálculo estructural, hidráulico, acústico o reglamentario. Tampoco convierte ausencia de choques en prueba completa de uso, resistencia o desempeño.

## Entrega y siguiente revisión

R7D puede mostrarse **como candidata en revisión con los pendientes anteriores visibles**. No se debe anunciar mecánica sanitaria o mantenimiento D08 íntegramente aprobados, ni mezclar sus planos con R6K sin rótulo.

Antes del dictamen global se necesitan los 25 renders, las 33 láminas y derivados del visor del mismo SHA, comparativas Cycles/web y comprobaciones de interacción/cámaras. Si se corrige la geometría, se congelará una fuente nueva y se regenerarán o demostrarán equivalentes los derivados afectados. No asigno nota por estos controles parciales.

Scripts propios reproducibles: `audit/r7d_geometry_probe.py`, `r7d_contact_probe.py`, `r7d_mechanical_probe.py` y `r7d_envelope_probe.py`. Resultados: `audit/r7d_preliminary/`. Todos abren la fuente para lectura, crean sólo geometría temporal de prueba y salen sin guardar Blender.
