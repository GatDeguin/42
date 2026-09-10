# Auditoría parcial R6C — distribución y ensamblaje de mobiliario

**Puntaje: 7,2/10. Hay progreso verificable; esta entrega parcial todavía requiere correcciones.**

El alcance es mobiliario nuevo del monoambiente, apoyos restantes, cajones de vestidor, frentes corredizos de TV y duplicados heredados. No se volvieron a auditar bisagras arquitectónicas ni baños PB pendientes de R6D. No se evaluaron fotografías nuevas ni se emite calificación integral de9,5.

Fuente reabierta: `output/Casa_de_Campo_95_R6C_preview.blend`. SHA256 `241eade674c1edae6be5ab543b1eb8f612d0794aaaf405ab67f532927c98bf83`.

## Progreso comprobado

- 37 piezas de sofá, mesa, sillas, faldones y taburetes coinciden con las transformaciones propuestas: error máximo inferior a0,001mm.
- La L tiene frentes hacia el usuario: lateral+X y posterior−Z. Los frentes de isla miran al pasillo de trabajo+Z. Desaparecen la isla atravesando la mesada y la heladera dentro de los bajos.
- Pasos reales:1,100m lateral,1,200m posterior,1,098m hasta hoja de heladera y **1,076m hasta tirador**. Debe cotarse la dimensión más restrictiva.
- Alturas respecto del piso: mesada/isla900mm, mesa750mm, silla460mm y taburete650mm.
- Taburete retirado350mm deja630mm al sofá; silla norte retirada deja660mm a fachada; silla sur retirada queda1,0325m antes de la puerta de baño cerrada. Se conservan las limitaciones ya documentadas de la hoja abierta y de la heladera en uso.
- Cuatro patas del mueble de apoyo del estudio llegan a+3,25 y a la cara inferior+3,43. Zócalos deTV y vestidor unen piso+3,25 con caras inferiores+3,28.
- El cajón0 deja de cortar el estante: las tres cajas de cajón libran la extracción propuesta450mm en21 posiciones. Esto no acredita todavía el montaje de sus guías.

## Correcciones necesarias

### 1. Bacha de cocina mono atravesada por el propio mueble

BVH confirma104 pares de triángulos contra `Bajos cocina mono lateral | lateral.001` y68 contra `travesaño.001`. El tabique está enZ3,82, dentro de la bachaZ3,68..4,28; el travesaño superior está enZ3,79. No es apoyo admisible del borde de la bacha: ambos entran en el vaso.

Solución propuesta: trasladar bacha y grifería+Z155mm, aZ3,835..4,435, dentro del módulo libre entre3,829 y4,441; rehacer la tapa con **un solo hueco nuevo**. No dejar la abertura anterior. Alternativamente, reconstruir la compartimentación y los soportes dejando libre el vaso y el desagüe.

Cierre exigible: bacha/casco/travesaños sin cruce de mallas; apoyo continuo del borde, orificio y conexión de desagüe; foto cercana desde arriba y sección del bajo.

### 2. Duplicado real de espejo en suite

`Espejo baño` y `Espejo baño suite` tienen el mismo material `Espejo con respaldo opaco | mirror` y ocupan casi el mismo volumen:50 pares de triángulos y29,5mm de solape de cajas enX. No son espejo más tablero soporte distinguibles.

Conservar un conjunto coherente con su respaldo y fijación; retirar el espejo genérico duplicado.

### 3. Dos despieces incompatibles de frentes en cocina de vivienda

Los tres `Frente cocina vivienda0/1/2` se cruzan con cuatro `Frente cocina vivienda detalle0..3`, en seis pares. Todos llevan madera y corresponden a hojas superpuestas, no a una junta constructiva.

Reconstruir un único despiece de frentes, coordinado con horno, bacha, particiones y tiradores. Verificar especialmente que no quede una hoja decorativa detrás o delante de otro frente o de un electrodoméstico.

### 4. Corredera deTV derecha corta el cerco en ambos extremos

Barrido propuesto760mm,41 posiciones: la hoja derecha cruza `Mueble TV` en cerrado y al final abierto. El vaciado tiene límitesX14,828..16,372; la hoja alcanza16,375 al cerrar y14,825 al abrir, aproximadamente3mm dentro del cerco lateral.

Reducir ancho790→780mm, conservando centros y carrera, deja2mm nominales a los extremos; verificar geometría con biseles. Los14mm reportados de solape de cajas enBVH **no son** profundidad normal de penetración.

El montaje necesita apoyo/retención de las hojas. El dibujo de barras paralelas no demuestra por sí solo un sistema corredizo funcionando.

### 5. Guías de cajón todavía separadas de sus apoyos

La guía fija izquierda queda4mm apartada del costado; la derecha14mm. Cada guía móvil queda1,5mm apartada de la caja del cajón. Las barras fija/móvil se superponen sin canal de deslizamiento representado.

Añadir calzos y fijaciones con continuidad real, y resolver sección de deslizamiento. La prueba favorable del cajón solo no puede presentarse como aprobación del herraje completo.

## Evidencia

- `integral95_02_r6c_furniture_geometry.json/.py`: inventario geométrico del archivo reabierto.
- `integral95_02_r6c_layout_comparison.json/.py`: transformaciones, alturas, pasos y contactos de apoyo.
- `integral95_02_r6c_drawer_use.json/.py`: extracción de cajas de cajón.
- `integral95_02_r6c_cabinet_checks.json/.py/.log`: bacha, duplicados y41 poses de correderasTV.

Las alturas y pasos recuperados justifican reconocer avance respecto deR5D. La bacha atravesada, las hojas duplicadas y el cerco que bloquea una corredera impiden aprobar el ensamblaje actual. La nota integral y la apariencia fotográfica siguen pendientes de un paquete consolidado.
