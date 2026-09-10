# Respuesta de construcción · segunda ronda de correcciones

Modelo vigente: output/Casa_de_Campo_Final.blend. La tercera auditoría independiente determina la nota; este documento registra acciones y evidencias, no se asigna una aprobación propia.

## Pasada 1 · Coordinación física
- Ambas hojas correderas PB pasan a una vía paralela por la cara del quincho, Z fuente 6,22. Se conserva el vano; se agregan ménsulas.
- Eje de puerta baño PB desplazado 55 mm hacia la cara exterior manteniendo la pose cerrada.
- Conductos de horno/parrilla reubicados dentro del patinillo. Montantes:X21,50/Z5,20 yX21,50/Z5,57. Cocina:X21,46/Z10,49. No se cortaron vigas para resolverlos.
- Se reconstruyeron las perforaciones anteriores y abrieron los pasos coordinados; el canal de cielorraso se resuelve con bastidor alrededor del patinillo.
- La auditoría posterior detectó la pérdida de recortes acústicos durante esa reconstrucción. Se repusieron juntas perimetrales 4 mm, conservando la cara inferior+6,45.

## Pasada 2 · Recorrido
- Se rehicieron los tramos 04,06,07,10 y 11 de la cámara animada, con tiempos de transición y permanencia que permiten leer los espacios.
- El tramo 04 rodea la esquina del baño antes de mirar su puerta; el recorrido editado tiene 1968 fotogramas a 24 fps.
- Puerta de baño de suite abre hacia vestidor para librar bidet y encuadre; manta recogida dentro del área del colchón para librar la puerta del dormitorio.
- Se corrigió la cara del cartel de calle. La hoja del portón mide 3 m y la luz entre los pilares de fuente es 2,75 m.
- Las 12 cámaras de control de recorrido son muestras fijas. No se renderizó ni codificó video.

## Pasada 3 · Materiales y paisaje
- Madera con veta longitudinal fina, variación por objeto y juntas de parquet 180 mm.
- Fustes y ramas ahusados, corteza, briznas de pradera y arboleda periférica menos regular.
- Se conservaron los seis centros de árboles originales, la implantación, la posición de mobiliario principal y la secuencia funcional.

## Comprobaciones
- output/validation.json:29 comprobaciones de dimensiones, alturas, cámaras, materiales y coordinación.
- review/coordinated_mesh_checks.json: mallas evaluadas de hojas/perfiles frente a muros en 27 poses distintas; conductos frente a cerramientos y estructura.
- review/door_fixtures_final.json: barridos frente a muebles y sanitarios.
- review/saved_route_final.json:reapertura desde disco,36 posiciones de cámara y consistencia de 1968 fotogramas.
- audit/:pruebas independientes y dictamen del crítico.
- review/:plantas, cortes, detalles, barridos y extracción derivados del modelo.
- Se verificó persistencia en un archivo final nuevo después de que un lector simultáneo de Blender impidiera reemplazar la revisión anterior en Windows. Los renders finales salen del archivo nuevo.

Estas comprobaciones documentan el modelo y sus barridos muestreados; no constituyen cálculo estructural ni proyecto ejecutivo de instalaciones.
