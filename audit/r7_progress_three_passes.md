# R7 — tres pasadas posteriores al dictamen de 8,3

Objetivo global vigente: **9,9/10 e hiperrealismo fotográfico**. Este registro enumera trabajo realizado y pendiente; no asigna una nota ni sustituye al crítico independiente. Video pausado hasta autorización expresa.

## Problemas señalados por el crítico

1. Agua atravesando el fondo de la pileta114mm.
2. Textiles y equipos con aspecto sintético.
3. Vegetación poco convincente y pérdida de follaje en el visor.
4. Diferencia de materiales e iluminación entre Cycles y web.
5. Ruido progresivo y encuadres insuficientes.
6. Continuidad de revestimientos húmedos no demostrada.
7. Ventilación D08 sin coordinación física de equipos, conductos y mantenimiento.

Se sumaron las correcciones del propietario: vestidor sin acceso al comedor, puerta directa dormitorio–estar y baño PB junto a fachada y medianera. Las alturas libres siguen siendo3,20m en estudio y2,60m en vivienda.

## Pasada1 — construcción y distribución

- Agua ajustada a los14sólidos del vaso, con72contactos de control. Sin intersecciones significativas, manteniendo la geometría del vaso.
- Distribución PA/PB corregida. Las manos de las puertas se reajustaron al detectar que una hoja obstaculizaba el nuevo acceso; la fuente revisada pasa41posiciones por hoja,886pares, separación continua10,953mm y envolvente corporal450mm en73muestras.
- El recorrido preparado se ajustó a esa distribución y pasó9000rayos sobre el checkpoint reabierto. No se renderizó video.
- C2: baldosas sólidas, juntas2×8mm y capas posteriores continuas;128cuerpos de baldosa. Ensayo final8c:123pares contra el entorno, sin interferencias ni aristas no manifold. El redondeo coplanar de0,248µm queda separado del criterio de choque.
- C3: equipos y ductos con accesos/extracciones explícitos. Un cruce entre impulsión y extracción fue detectado y corregido. Ensayo final7:65pares internos sin choques,88pares de entorno,8recorridos de mantenimiento aprobados y punto fijo mínimo+6,453m.

Las pruebas C2 yC3 se repetirán tras integrarlas con la geometría sanitaria final.

## Pasada2 — geometría y materiales físicos

- Manta simulada, almohadas cerradas y costuras corregidas; cortinas y prendas adultas con apoyos y separaciones medidas.
- Cuatro canteros conservados, con plantas y sustrato diferenciados; no se sustituyeron especies de huerta por ornamentales para obtener una imagen más vistosa.
- Texturas métricas y normales PBR conservadas como datos editables. Se mantiene pendiente el juicio fotográfico sobre las imágenes finales.

## Pasada3 — luz, sanitarios y entrega coherente

- Emisores físicos y luminarias recolocados; luz del vestidor fuera de tableros. Nuevas cámaras a altura de uso, encuadres verticales y vista del acceso real desde el estar.
- Al refinar las superficies sanitarias se detectó un choque heredado entre asiento y cisterna. Se está reconstruyendo el conjunto dentro de su huella global, conservando apoyo y conexión de descarga; se validarán dimensiones adultas, bisagras, topes y tapa.
- Pavimento PBR de300mm con junta3,5mm y relieve moderado, frente a la junta visual previa de aproximadamente11,7mm.
- Visor: follaje completo, compresión sin pérdida verificada por píxeles, terreno original y preservación de UV. Se corrigió el guardado HDR que alteraba los valores lineales de iluminación.
- Pendiente: fuente integrada única,25imágenes definitivas,33planos, exportación GLB, iluminación de8sectores, pruebas de dimensiones/interacción/móvil emulado y comparativas Cycles–web.

## Próxima auditoría formal

Sólo se solicitará cuando las tres pasadas estén integradas y todos los derivados señalen el mismo SHA. El crítico deberá revisar arquitectura, medidas, funcionamiento y apariencia fotográfica del conjunto. Un resultado inferior a9,9 debe conservar su nota real, listar los problemas y abrir otras tres pasadas constructivas.

El avance publicado en GitHub es un checkpoint parcial. No es el paquete final que se someterá a esa auditoría.

## Integración R7D y publicación de candidata

Fuente congelada: `9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e`. Los parches se integraron de forma idempotente. La reapertura pasó controles de agua, alturas, escala, escenas y los cinco ensayos de componentes: SAN99 dentro de su alcance, revestimientos, ventilación, contactos internos de ventilación y manos de puertas. Recorrido preparado: 9.000 rayos, sin video. Visor: 5.588 comparaciones dimensionales; textura y geometría decodificada del paquete verificadas. Chrome comprobó vistas, 13 puertas y retrato sin errores.

Estos ensayos no cierran la auditoría. El crítico amplió el barrido de herrajes SAN99 y encontró interferencias entre pedestales fijos y manguitos/brazos móviles. La tapa necesita un límite operativo explícito de 90°; a 100° alcanza la cisterna. La documentación de acceso y descenso de equipos D08 está ampliándose. Las imágenes de huerta y textiles siguen mostrando rigidez. Estos puntos quedan abiertos para la siguiente corrección.

A pedido del propietario se publica R7D como candidata integrada, con visor y cuatro primeras imágenes de ese SHA. El juego completo de 25 imágenes, 33 planos y los ocho atlas de iluminación siguen en elaboración. No se asigna nota global R7D ni se afirma aprobación.
