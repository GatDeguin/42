# SAN8 · Revisión mecánica de bisagras sanitarias

Se corrigieron los 30 cruces fijo–móvil señalados por la auditoría independiente de R7D. Las pruebas del constructor aprueban la geometría del parche. Esta subentrega no sustituye el siguiente dictamen independiente ni asigna una nueva nota global.

## Alcance y construcción

Se sustituyen 36 piezas SAN99 por 192 piezas SAN8: seis mecanismos, dos por sanitario. Se conservan los doce cuerpos principales (taza, asiento, tapa y cisterna de cada baño), sus mallas, UV, materiales, posiciones, huellas, alturas, apoyos cerámicos y conexiones. No hubo cambios geométricos en los objetos existentes que permanecen. La colección nueva aparece completa en las cuatro escenas y la segunda aplicación es idempotente.

- Horquilla con apoyos fuera de los manguitos y travesaño inferior. Los brazos arrancan fuera del pasador y se unen con volumen positivo a sus propios cuerpos solidarios.
- Pasador nominal de 6 mm, cuello doble D alojado en perforaciones compatibles de la horquilla y extremo exterior cilíndrico de rosca M6 nominal. Cabeza y tuerca de 10 mm entre caras, accionables con llaves.
- Casquillo interior de 6,2 mm y alojamiento de 8 mm. Holgura radial nominal 0,10 mm; mínimo conservador facetado durante todo el giro 0,0963 mm.
- Discos de fricción con bloqueo doble D, arandela cónica de precarga y tuerca. La geometría representa una retención por fricción propuesta; no simula un coeficiente de fricción ni acredita una capacidad de retención. Par, materiales, precarga y tolerancias industriales requieren selección y ensayo del herraje. La rosca se representa por diámetros nominales.
- Topes sectoriales físicos a 0° y 90°. Saliente móvil separado 0,400 mm del portatope; alojamiento separado 0,600 mm de los dientes fijos.
- Cuatro apoyos elastoméricos de 14 × 10 × 4 mm por tapa, entre ésta cerrada y el asiento. Se mantienen los apoyos previos de asiento y cisterna.

Horquilla, pasador, tuerca y discos forman el grupo fijo. Cada asiento con brazos, alojamientos, casquillos, salientes y apoyos forma un grupo móvil solidario; la tapa forma otro. Los contactos de unión dentro de un grupo se distinguen de interfaces cinemáticas. La función pose(familia, asiento, tapa) exige 0 ≤ asiento ≤ tapa ≤ 90. Presentación conservada: asiento cerrado y tapa abierta a 90°.

La tipología de retención regulable tiene referencia funcional en [Southco E6](https://southco.com/en_us_int/hinges/positioning-hinges/e6-adjustable-torque-position-control-hinges) y [precarga de resortes de disco de SPIROL](https://my.spirol.com/resources/white-papers/adjustable-bearing-preload-solutions/). No se atribuye el modelo a esos productos ni se copia una capacidad de catálogo.

## Resultados medidos

| Control | Resultado |
|---|---|
| Apertura | 426 poses, malla de 2,25° y combinaciones adicionales |
| Intersecciones exactas fijo–móvil y asiento–tapa | 11,223; 0 penetraciones duras |
| Topes | 48 controles: contacto a 0°/90° y bloqueo al sobrepasar −0,25°/90,25° |
| Unión brazo–cuerpo solidario | 12 conexiones de volumen positivo |
| Apoyos de tapa | 12 apoyos, 216 rayos; desviación máxima 0.384 µm |
| Contactos tangentes numéricos | 172; profundidad equivalente máxima 0.150 µm |
| Topología nueva | 192 sólidos cerrados, volumen y determinante positivos |
| Fuente, alcance, UV, escenas e idempotencia | Aprobados |

El umbral general de intersección es 0,01 mm³. Sólo los contactos asiento–tope elastomérico, con ambos grupos al mismo ángulo, admiten hasta 0,3 µm de profundidad numérica equivalente y se corroboran mediante rayos. No se amplía la tolerancia global para ocultar cruces.

## Verificación continua

Los límites radiales separan eje, casquillos, cuerpos y portatopes durante todo el giro; los intervalos axiales separan los grupos. La tapa permanece sobre el asiento para cualquier diferencia de ángulos entre 0 y 90°, por los signos y mínimos medidos de V y W en la expresión Wrot = V sen(d) + W cos(d).

| Baño | A cisterna (mm) | Asiento–tapa rígida cerrada (mm) | Asiento sobre taza durante giro (mm) |
|---|---:|---:|---:|
| mono | 15.200 | 4.000 | 4.000 |
| quincho | 15.200 | 4.000 | 4.000 |
| suite | 51.601 | 4.000 | 4.000 |

La envolvente continua de los vértices girando entre 0 y 90° se contrastó con todas las mallas visibles ajenas al sanitario. Siete cajas generales fueron candidatas; el recorte de sus triángulos y rayos de pertenencia demostraron cero superficies dentro de la trayectoria y ningún volumen contenedor. Incluye capas del baño PB, terreno y conducto de extracción.

## Archivos y reproducción

- scripts/correcciones99_san_mecanica_r8.py: función apply(), sin guardado ni render.
- scripts/check99_san_mecanica_r8.py: barrido, contactos, topología y conservación.
- scripts/proof99_san_mecanica_r8.py: envolventes, entorno y secciones reales.
- review99/r8_san/validation.json: resultados detallados de prueba.
- review99/r8_san/continuous_and_sections.json: prueba continua y entorno.
- review99/r8_san/construction.json: inventario y grupos.
- review99/r8_san/secciones_mecanismo.svg y .png: cuatro cortes de la malla.
- output/Casa_de_Campo_99_R8_san_preview.blend: copia de revisión.

Fuente R7D inalterada: 9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e

Parche SAN8: ee0f76d211906a0543af05bd219de168f94eb6a5759c4fd8c24a584887681ab5

Copia SAN8: 75737be3802bbd69f99226af444158658e0d1e3b324de9920e399969ff6cb982

No se modificaron parches R7 publicados. No hubo GPU, vídeo, commit ni publicación en esta subentrega.
