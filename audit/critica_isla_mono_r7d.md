# Auditoría acotada — isla y taburetes del monoambiente R7D

**Resultado:** existe un vuelo real de **250 mm**, pero la profundidad de uso sigue siendo corta para un puesto cómodo de comedor a esta altura. La imagen exagera visualmente la falta de espacio; el problema no es ausencia de vuelo ni tiradores enfrentados a las rodillas. Es un déficit verificable de reserva que requiere otra pasada de diseño. **Sin nota global ni aprobación integral R7D.**

## Fuente y método

- Fuente abierta en modo de sólo lectura: `output/Casa_de_Campo_99_R7D.blend`.
- SHA-256: `9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e`.
- Frame 1, geometría evaluada con modificadores/normales actuales, coordenadas fuente X/H/Z = Blender X/Z/−Y; piso terminado H+0,210.
- Imagen existente contrastada: `review99/r7_final/stills/mono_cocina.png`.
- 51 piezas inventariadas; 50 rayos a distintas alturas y posiciones delante de la isla; 14 envolventes de uso comprobadas mediante intersecciones Boolean EXACT. No se renderizó ni guardó la fuente.
- Evidencia: `audit/r7d_preliminary/island_probe.json`, `island_use_envelopes.json`; scripts `audit/r7d_island_probe.py` y `r7d_island_use_probe.py`.

## Cotas obtenidas de la malla

| Magnitud | R7D |
|---|---:|
| Tapa, ancho × profundidad × espesor | 1720 × 680 × 35 mm |
| Canto de uso / fondo macizo que limita rodillas | Z3,320 / Z3,570 |
| Vuelo útil hasta la primera obstrucción | **250 mm** |
| Altura de tapa sobre piso terminado | **900 mm** |
| Intradós de tapa sobre piso | 865 mm |
| Asiento sobre piso | **650 mm** |
| Distancia vertical asiento–tapa / asiento–intradós | 250 / **215 mm** |
| Cada asiento | 380 × 380 × 30 mm |
| Centros de asientos A / B | X16,320 / X17,380; ambos Z3,050 |
| Separación entre centros | 1060 mm |
| Canto delantero del asiento / canto de tapa | Z3,240 / Z3,320: 80 mm de separación |
| Frente de puertas de mueble, lado de trabajo | Z3,975 |
| Extremo de tiradores, lado de trabajo | Z3,988; queda 12 mm dentro del canto Z4,000 |
| Reposapiés superior sobre piso / bajo asiento | 200 / 450 mm |

Los tiradores se encuentran en el **lado opuesto** a los taburetes. El fondo que se ve desde ellos es una placa de 18 mm en Z3,570–3,588. Los 50 rayos interceptan primero ese fondo en la zona de uso; su distancia al canto permanece en 250 mm. No aparece una pieza oculta que reduzca adicionalmente ese vuelo.

## Criterio de confort y prueba geométrica

Como referencia de diseño se consultó la [NKBA, Kitchen Planning Guideline 9, PDF público](https://kb.nkba.org/uploads/2022/05/Kitchen-Planning-Guidelines.pdf): para una mesada de 914 mm recomienda por comensal una reserva de 610 mm de ancho y 381 mm de profundidad. Se usa como referencia próxima a los 900 mm del modelo, **no como reglamento argentino ni certificación de accesibilidad**. Frente a ella, la profundidad modelada presenta un déficit de **131 mm**.

Se ensayó esa planta de reserva en una banda vertical declarada H0,900–1,020: ambas plazas intersectan la placa del fondo; algunos extremos también alcanzan costillas del mueble. La altura de la banda es una selección del auditor, no una exigencia atribuida a NKBA.

Una segunda prueba usa dos volúmenes de rodillas por asiento, de 120 mm de ancho, centros separados 200 mm y altura entre 40 y 160 mm sobre el asiento. Comienzan en el canto frontal de éste y terminan a 500, 550 o 600 mm por delante de su centro, que se toma como referencia de pelvis:

| Alcance delantero declarado desde centro de asiento | Resultado en ambas plazas |
|---|---|
| 500 mm, final Z3,550 | Libre; quedan 20 mm hasta el fondo |
| 550 mm, final Z3,600 | Interferencia: cada rodilla atraviesa el fondo de 18 mm |
| 600 mm, final Z3,650 | Misma interferencia con el fondo |

Se verificaron cuatro envolventes libres y diez con cruce, contando las dos reservas generales. La intersección de cada rodilla larga con la placa es aproximadamente 259 cm³. Estos volúmenes son un **ensayo de sensibilidad geométrica**, no percentiles antropométricos ni un cuerpo sentado completo. Demuestran dependencia de la postura; no permiten afirmar que ninguna persona pueda sentarse. Alejar el taburete cambia el alcance a la mesa y debe comprobarse como una postura completa, no darse por solución automática.

El ancho de 610 mm centrado en el taburete B sobrepasa el extremo derecho de la tapa unos **5 mm**. Es un descentrado menor fácilmente corregible; el ancho total disponible permite dos plazas. No debe confundirse con el déficit de profundidad.

## Corrección concreta y evidencia para cerrar

1. Dar a ambas plazas una reserva continua de profundidad próxima a 381 mm, o justificar una solución equivalente con un cuerpo sentado dimensionado y posición de uso explícita. Un cambio de cámara no resuelve este punto.
2. Comparar dos operaciones: retranquear el fondo del mueble conservando el canto actual, o ampliar la tapa hacia los taburetes y reposicionarlos. La primera reduce almacenamiento; la segunda ocupa espacio de circulación. No desplazar la isla completa hacia el frente de cocina sin volver a medir el pasillo y aperturas.
3. Mantener razonados los 900/650 mm y la holgura vertical; al mover muebles comprobar muslos, rodillas, reposapiés, entrada/salida y paso detrás del usuario. Recentralizar los dos puestos dentro de la tapa.
4. Dibujar un corte de uso a escala con piso, asiento, rodillas, fondo, canto, apoyos y material de tapa. Una eventual mayor consola requiere un detalle de soporte coherente con la tapa de 35 mm; esta revisión no valida resistencia.
5. Repetir medidas, envolventes y vista humana desde el mismo SHA corregido. La isla R7D puede publicarse como candidata con esta limitación explícita, pero no doy por resuelta su ergonomía para el objetivo 9,9.
