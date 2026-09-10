# Auditoría crítica independiente · Iteración 2
Fecha: 10/09/2026. Modelo inspeccionado: output/Casa_de_Campo_Revision.blend.
Puntaje global: **7,0 / 10**. Estado: **todavía requiere mejoras antes de alcanzar 8**.

Se verificaron las tres pasadas documentadas, el modelo reabierto en otro proceso Blender, la imagen principal de revisión, 11 vistas suplementarias, 12 muestras fijas de la cámara animada, plantas, barridos, extracción y detalles de cubierta. No se exige un MP4: el video permanece correctamente pausado por instrucción del usuario.

## Avances confirmados
- El modelo distingue vivienda con 2,60 m libres y estudio con 3,20 m; la cubierta del estudio sube 0,60 m. Se han incorporado cielorrasos, estructura secundaria, aislamiento y el encuentro escalonado.
- Los acústicos ahora se recortan alrededor de los bafles; se cerró la superposición principal señalada en la primera auditoría.
- El portón se desplaza por una vía paralela al muro y se añadieron ruedas/guías.
- La línea de fuego tiene recorridos independientes y salidas, sin prolongar tubos a través de la bañera o los muebles superiores.
- Las nuevas vistas de baño, cocina, estudio y dormitorio son considerablemente más legibles.
- Barandas, fijaciones, antideslizantes, chapa, canaletas y remates mejoran la lectura constructiva.
- Mejoró la exposición interior y la presencia de la piscina; las cámaras originales se conservan.

Estos cambios explican la subida de 6 a 7. No basta para aprobar la revisión, porque siguen existiendo interferencias geométricas comprobadas y la cámara animada aún presenta varios encuadres obstruidos.

## P1 · La corredera derecha del monoambiente invade el baño
Mi prueba independiente evalúa todas las piezas móviles con su malla evaluada y sus modificadores. No se limita a un punto del driver.
En apertura, Puerta doble mono derecha vidrio ocupa:
- X 18,830–19,970
- Y Blender −5,7715..−5,7625
- cota 0,270–2,570

Baño mono muro izquierdo ocupa:
- X 19,250–19,390
- Y Blender −5,800..−4,200
- cota 0,000–2,600

La hoja cruza 14 cm de espesor del muro. También hay intersecciones de marcos/burletes. Se reproduce en frames 78, 90 y 105, y los perfiles tienen interferencias incluso cerrados. El desplazamiento de pista hacia el monoambiente liberó una separación pero generó otra con el baño lateral.

Corrección requerida: resolver la vía completa de ambas hojas respecto de TODA la tabiquería. Considerar la cara hacia quincho u otra disposición paralela que conserve el vano original. No borrar un trozo de pared funcional para hacer desaparecer la colisión.

## P1 · La puerta del baño PB roza/atraviesa el paño de su propia entrada
Baño mono puerta intersecta Baño mono frente | paño en apertura desde el frame 78. En pose abierta el paño ocupa X 19,390–19,440 / Y Blender −4,350..−4,210; la hoja pasa por X 19,410–19,487 / Y −4,281..−3,559.
Corregir eje/holgura y ángulo final, verificando hoja, herrajes y muro. La posición aproximada de la abertura de fuente puede mantenerse.

## P1 · Los conductos aún atraviesan cerramientos y elementos de soporte
La prueba independiente detectó intersección de triángulos reales en estos pares:

| Conducto | Objeto interferido |
|---|---|
| Horno | Estudio · canal de cielorraso 12 |
| Parrilla | Medianera constructiva baja |
| Parrilla | Separación mono quincho derecha |
| Parrilla | Estudio · correa secundaria.007 |
| Parrilla | Estudio · viga de apoyo.001 |
| Parrilla | Estudio · canal de cielorraso 12 |
| Cocina | Vivienda · correa secundaria.005 |
| Cocina | Vivienda · canal de cielorraso 12 |

La subida de parrilla en Z fuente 5,72, radio exterior 0,16, alcanza Z 5,88; la viga ocupa Z 5,83–5,97. Es una interferencia de aproximadamente 5 cm en planta, no una mera línea coincidente.
La medianera interior empieza en X 21,80; el tramo horizontal de parrilla llega a X 21,81. El pasamuros abierto en Separación mono quincho derecha no cubre completamente el trazado actual.

Corrección requerida: desplazar el recorrido y reconstruir pasos con holguras. Se sugirió estudiar Z 5,64 para la montante de parrilla, comprobando separación respecto del horno en Z 5,32 y de la envolvente del patinillo. No perforar una viga principal para ocultar la incompatibilidad; coordinar canaletas/perfiles secundarios mediante bastidores o desvíos plausibles. Regenerar lámina y prueba tras corregir.

## P1 · La cámara animada no está completamente resuelta
Las cámaras suplementarias mejoraron, pero no modificaron suficientemente la cámara real de recorrido. Las 12 muestras de sus puntos medios muestran:
- 04: muro del baño ocupa gran parte de imagen; la línea de fuego queda cortada.
- 06: predominan cielo y una visual muy ascendente; no se entiende la secuencia de peldaños.
- 07: reversos de altavoces ocultan buena parte de la consola.
- 10: placard de primer plano bloquea casi media vista del dormitorio.
- 11: hoja/mueble próximo domina el encuadre al entrar al baño.

No es necesario renderizar el video para corregir esto. Ajustar puntos de mirada, secuencia y velocidad, conservando la ruta espacial y las cámaras HTML; repetir muestras antes/centro/después de estos tramos. El movimiento puede transitar por espacios estrechos, pero necesita revelar el ambiente al concluir cada transición.

## P2 · Apariencia todavía mejorable
- El texto CEDRO MISIONERO aparece espejado en iter1_porton.png. Corregir orientación de la cara tipográfica.
- El vestidor y varios muebles muestran ondas de madera grandes y repetidas. Ajustar escala/dirección/variación por tabla; evitar que suelo y carpinterías parezcan compartir un patrón ondulado.
- La vegetación secundaria sigue mostrando grupos de troncos cilíndricos y copas repetidas sobre suelo muy uniforme. Mantener los centros principales y añadir variación más natural de fuste, ramificación y masas de follaje.
- En el exterior las bandas de césped y el horizonte todavía se leen artificiales. La composición sí muestra más piscina, pero la calidez y riqueza de paisaje de la referencia aún no están igualadas.
- Refinar estos aspectos después de las interferencias; no sustituir exactitud por decoración.

## Limitaciones detectadas en la verificación anterior
revision_checks.json informa cero colisiones, pero su algoritmo:
1. selecciona una sola pieza por puerta, y para hojas posteriores termina eligiendo manijas;
2. descarta solapes menores de 12 mm en cualquier eje, lo que descarta de entrada vidrios de 9 mm;
3. comprueba vértices dentro de una caja, que puede omitir cruces entre caras.

Por ello 'cero' no es evidencia suficiente de funcionamiento. Mi revisión usó mallas evaluadas, todas las hojas/perfiles móviles y cruces de triángulos después de un filtro espacial de 2 mm. Evidencia reproducible:
- audit/independent_checks_02.py
- audit/independent_checks_02.json
- audit/independent_checks_02.log
- audit/geometry_bounds_02.json

Debe distinguirse un contacto previsto (piezas apoyadas o insertadas) de una interferencia inválida. Los pares P1 aquí listados fueron revisados contra dimensiones y no son simples apoyos.

## Fe de precisión respecto de la primera auditoría
El HTML define una hoja de portón de 3,00 m y pilares de 0,25 m que reducen la luz entre sus caras a aproximadamente 2,75 m. La reconstrucción debe conservar esa distinción. La frase '3,00 m claros' de la primera revisión fue demasiado amplia; no se exige ensanchar el acceso contrariando los pilares de fuente.

## Tres pasadas antes de próxima nota
1. **Coordinación física:** corredera PB, puerta baño, ocho pares conducto/estructura/cerramiento; actualizar pasos y probar todas las piezas a lo largo de sus barridos.
2. **Recorrido y lectura:** reparar los cinco tramos indicados, cartel y coherencia de poses; emitir muestras fijas comparables.
3. **Calidad visual y cierre:** madera, césped, vegetación y balance de luz; revisar nueva imagen principal y regenerar únicamente evidencia afectada.

Para alcanzar 8: cerrar P1 con evidencia reproducible; conservar niveles y geometría autorizados; mostrar mejora concreta de las muestras de cámara y de los materiales más visibles. No hace falta modificar distribución, producir un cálculo estructural inexistente ni renderizar el MP4 todavía.
