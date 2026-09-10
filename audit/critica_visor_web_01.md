# Crítica independiente del visor web · Iteración 01

**Nota: 7/10. No alcanza todavía el umbral de 8 solicitado.**

La base del visor funciona y conserva la lectura general del proyecto. La carga, la interacción y la reducción de geometría son un avance real. La presentación todavía falla en una vista interior importante, en el encuadre inicial del teléfono y en la correspondencia entre cota anunciada y corte mostrado. Además, la madera perdió el acabado que se había trabajado en el modelo auditado. No corresponde transferir automáticamente el 8 del archivo Blender a esta representación web.

## Estado auditado

Estado congelado entregado por el constructor el 10 de septiembre de 2026:

- index.html SHA256: 164F7CCF93E32B863591EA4DA3EF12210B4050010C5D6F06AB9973A34F9239EF
- viewer.js SHA256: 0E276C1170278504550C0782B06BC98C0BEBD6D5516BA8623150129A087BDA00
- viewer.css SHA256: 3E4869367FBA91824147E2EF35D922ADA4F5231B4FBFD67DD6CBDA54A65E6E94
- house.glb SHA256: 3EE11DE28D53A4E215C6EBB8D8E895478B2CA5BC18C213C6B007CD8DACC4E394

El GLB declara como origen Casa_de_Campo_Final.blend, SHA256 58223D78F71DC0C1D4F33034AAAF0BE96A1BD420F72F2231468003E942C2BBFE. Es el archivo aprobado en la tercera crítica arquitectónica.

Revisé código de visor y exportación, metadatos, las capturas web actuales y ejecuté dos pruebas propias en Chrome headless, en una sesión independiente. No modifiqué el visor, el modelo ni otras sesiones. Los scripts y resultados están en audit/web_independent_01.mjs/.json y audit/web_detail_checks_01.mjs/.json. Esta revisión cubre el visor local; la disponibilidad final de GitHub Pages requiere su propia comprobación después del despliegue.

## Comprobaciones satisfactorias

- Carga local hasta estado listo: 1,77 s en esta máquina. Descarga del GLB: 10.021.880 bytes.
- 2.349 mallas originales y 12 mecanismos de puertas reconocidos; exterior observado: 789.066 triángulos y 194 llamadas de dibujo.
- Muestreo propio de 90 cuadros: media de 16,50 ms, sin cuadros superiores a 50 ms. Es una medición de esta máquina, no una garantía para teléfonos físicos.
- Ocultar cubiertas y vegetación dejó cero mallas visibles pertenecientes a esas categorías. El plano de corte real responde a su control.
- Cero errores JavaScript en la prueba propia. Sin desbordamiento horizontal en 1440 px ni 390 px.
- El menú móvil funciona y termina en x=0, ancho 285 px. La captura anterior con un fragmento de menú correspondía a una transición incompleta; no es un defecto permanente.
- La interfaz permite recorrer las dos plantas y los ambientes, con controles comprensibles. Se verificaron también los nuevos accesos a monoambiente y fachada.
- El informe de interacción del constructor registra clic real sobre el portón, apertura individual y arrastre orbital. Sus doce comprobaciones de apertura conservan los destinos publicados en los metadatos.
- No detecté una regresión de distribución, alturas, cubierta escalonada o elementos principales en las vistas y cajas de geometría examinadas. El exportador conserva la arquitectura y limita la simplificación a paisaje. Esta afirmación no equivale a una comparación vértice por vértice de todo el GLB contra Blender.

## Problemas que impiden aprobar esta versión

### 1. La cota del título puede contradecir el plano real — prioridad alta

Reproducción: seleccionar Planta baja y mover el corte a 4,50 m.

Resultado comprobado:

- Título: «Planta baja · corte a 2,80 m».
- Control: «4,50 m».
- Plano efectivo de Three.js: 4.5.

Una representación arquitectónica no puede anunciar una sección distinta de la que muestra. También debe actualizar el estado al desactivar el corte. Evidencia: audit/web_detail_checks_01.json y audit/web_cut_label_01.png.

Corrección: derivar la etiqueta de la cota y del estado actuales, o separar el nombre de la vista de una etiqueta de corte siempre sincronizada.

### 2. La vista Vestidor queda obstruida por sus propias puertas — prioridad alta

El preset abre todas las puertas. En la captura estable, una hoja ocupa casi todo el lado izquierdo y otra gran parte del derecho; el placard queda reducido a una franja central. Esto impide leer el espacio que el botón promete mostrar. La geometría puede ser correcta y la cámara seguir siendo inadecuada.

Evidencia propia: audit/web_vestidor_independent.png.

Corrección: definir un estado de puertas específico para esta vista y ajustar el punto de cámara dentro del espacio disponible. Deben verse el placard, la zona de paso y la relación con sus accesos sin ocultar la mayor parte del cuadro. No mover muros ni alterar los pivotes auditados para resolver una decisión de cámara.

### 3. El exterior inicial del teléfono pierde la composición del conjunto — prioridad media

En 390 × 844, la misma cámara de escritorio recorta el extremo derecho de la casa y muestra solamente una fracción de la pileta. La vista se denomina «Casa y paisaje», pero exige que el visitante corrija el zoom antes de entender el conjunto. En escritorio, PB y PA funcionan como perspectivas cortadas, no como plantas ortográficas; esa distinción debe mantenerse clara.

Evidencia propia: audit/web_mobile_independent.png.

Corrección: adaptar el encuadre inicial al aspecto disponible, mediante distancia/objetivo específicos o ajuste a una caja de interés. Verificar entrada inicial, botón Inicio y cambio de orientación. No basta con ampliar el FOV indiscriminadamente dentro de los ambientes.

### 4. Las etiquetas pierden contraste sobre el modelo — prioridad media

El rótulo oscuro del estudio móvil queda sobre el tratamiento acústico negro y apenas se lee. También sucede en el vestidor sobre la hoja oscura. El texto depende del fondo que casualmente quede detrás de la cámara.

Evidencia: audit/web_studio_mobile_independent.png y audit/web_vestidor_independent.png.

Corrección: dar al rótulo un fondo y contraste estables, con dimensiones que respeten los controles y el ancho del teléfono.

### 5. Las maderas se redujeron a colores planos — prioridad media

La exportación adapta correctamente varios materiales, pero Roble aceitado, Nogal mate y Madera oscura carecen de mapa de color, normales y rugosidad. La prueba propia confirma esos campos vacíos. Mesas, puertas, placares y los pisos de vivienda/monoambiente aparecen como superficies uniformes. Se pierde tanto la veta como la lectura del parquet, un retroceso frente al trabajo del archivo final.

Evidencia: audit/web_detail_checks_01.json; capturas de quincho, dormitorio, monoambiente y vestidor. El inventario propio identifica Roble aceitado como material de Piso vivienda y Piso monoambiente.

Corrección: trasladar a texturas ligeras la madera y el parquet del modelo fuente, conservando dirección, escala y diferencias entre piezas. No hace falta reconstruir todo Cycles ni multiplicar la geometría para resolverlo. Conviene equilibrar también blancos y luz ambiental: baño y textiles siguen demasiado homogéneos, aunque los volúmenes se distinguen.

## Tres pasadas propuestas antes de la segunda nota

1. **Exactitud de los estados:** sincronizar título, corte activo y cota real; revisar que la indicación general de puertas no induzca a error tras una apertura individual; comprobar selección y ocultación combinadas.
2. **Cámaras y lectura:** resolver Vestidor, adaptar el encuadre móvil y proteger el contraste de rótulos. Capturar el estado estable en escritorio y teléfono, incluido Inicio después de cambiar de ambiente.
3. **Acabado visual:** recuperar madera y parquet con texturas de escala coherente, equilibrar los blancos y volver a comprobar carga y fluidez para que la mejora visual no degrade la interacción.

Después de esas pasadas, la segunda auditoría debe revisar el nuevo estado congelado y las vistas afectadas. No se solicita renderizar vídeo ni cambiar la arquitectura auditada.

## Alcance del dictamen

La nota 7 reconoce una aplicación funcional y una exportación útil, pero los defectos anteriores afectan directamente a cómo se entiende y se presenta la arquitectura. El objetivo de la siguiente revisión es un visor fiel, legible y bien encuadrado. El umbral 8 no implicará fotorealismo máximo, cálculo estructural aprobado ni documentación ejecutiva de obra.
