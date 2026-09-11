# Auditoría acotada — puesto de trabajo del estudio R7D

**Resultado:** se descarta que el puesto central de consola carezca de hueco para rodillas. Se confirma una altura de teclado distinta de la del frente de consola y un controlador sin apoyo físico resuelto. El puesto requiere coordinación ergonómica y de montaje antes de considerarlo terminado. Sin nota global en este informe.

Fuente: `output/Casa_de_Campo_99_R7D.blend`, SHA-256 `9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e`. Comprobación de sólo lectura, sin render ni guardado.

## Medidas de uso

| Elemento o reserva | Medida real |
|---|---:|
| Piso terminado | H+3,250 m |
| Asiento de silla fija | 470 mm sobre piso |
| Teclas blancas, superficie superior | **859,5 mm** sobre piso |
| Teclas negras, superficie superior | **872 mm** sobre piso |
| Tecla blanca / negra respecto del asiento | **389,5 / 402 mm** |
| Controlador, cara inferior / superior | 795,5 / 850,5 mm sobre piso |
| Hueco central de rodillas | 700 mm de altura; recorte nominal900 mm de ancho y~600 mm de profundidad bajo frente |
| Holgura vertical hueco–asiento | 230 mm |

Se repitieron los doce rayos de la zona central X18,20/18,40/18,60/18,75 y Z2,65/3,00/3,35: todos alcanzan el intradós a H3,950. Cuatro rayos horizontales desde X19,10 a alturas H3,72–3,94 encuentran el fondo en X18,177. La caja envolvente de la base parece maciza, pero la malla tiene una reserva real. Se conserva el resultado geométrico favorable de R6K.

La cota histórica de aproximadamente750 mm del frente de consola **no describe la superficie del teclado MIDI**, que está elevada por el cuerpo del controlador y su posición.

## Altura y postura

La recomendación de [OSHA para colocación de teclados](https://www.osha.gov/etools/computer-workstations/components/keyboards) relaciona la altura de entrada con codos próximos al cuerpo, hombros relajados y muñecas sin flexión forzada. Se usa sólo como criterio general de postura: no es una norma argentina ni una especificación propia de un instrumento musical.

Para hacer explícita la evaluación, un operador de ensayo con codo relajado a280 mm sobre el asiento lo tendría a750 mm del piso. La tecla blanca actual queda109,5 mm por encima de ese codo; con una distancia horizontal ilustrativa de310 mm exige aproximadamente19,5° de ascenso del antebrazo. Ésta es una postura de prueba declarada, no un percentil antropométrico ni la afirmación de que todos los usuarios tengan esa medida. La silla representada es fija y no ofrece un ajuste que resuelva distintos usuarios.

**Pendiente concreto:** corte del operador con pelvis, codo, mano, muslo, rodilla y pie; separar el uso del MIDI de los controles laterales de mezcla. Resolver la altura del teclado y la silla en conjunto, conservando una reserva real para piernas. No bajar indiscriminadamente toda la consola, pues destruiría el hueco de700 mm que sí está comprobado.

## Apoyo del controlador: fallo constructivo confirmado

La cara inferior del controlador está horizontal en H4,0455 sobre una consola inclinada. Quince estaciones de rayos dirigidos a ésta miden separaciones de3,75 mm en X18,20;15,78 mm en X18,35;31,81 mm en X18,55;43,84 mm en X18,70 y49,05 mm en X18,765.

Se amplió el ensayo a56 estaciones contra **toda la escena**, incluyendo posiciones cercanas a ambos extremos del teclado. No aparece contacto de2 mm o menor: el rayo alcanza la consola o sale por su vuelo frontal. El inventario de objetos que atraviesan el volumen entre ambas superficies contiene únicamente `Consola estudio` y `Controlador estudio`; no se identifican patas, cuñas, bandeja o ménsulas que sostengan el equipo.

No basta inclinar una cámara para ocultar esa separación. Diseñar apoyo físico continuo o puntos de apoyo reales y una retención coherente con la pendiente; comprobar contacto y estabilidad geométrica del montaje, además de corregir la altura de uso. La verificación de resistencia y selección de producto permanece como proyecto específico.

## Evidencia reproducible

- `audit/r7d_preliminary/studio_workstation_inventory.json`
- `audit/r7d_preliminary/studio_workstation_functional.json`
- `audit/r7d_preliminary/studio_controller_support.json`
- `audit/r7d_preliminary/studio_controller_all_support.json`
- Scripts de sólo lectura `audit/r7d_studio_probe.py`, `r7d_studio_functional.py`, `r7d_controller_support.py`, `r7d_controller_all_support.py`.
