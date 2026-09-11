# R7D · Revisión visual del constructor sobre 25 vistas

La serie conserva defectos visibles de vegetación, textiles y un espejo, además de comprobaciones ergonómicas pendientes. Este documento entrega evidencia al crítico independiente; no asigna puntuación ni aprueba el umbral 9,9.

Fuente única: `D:\2026\42\output\Casa_de_Campo_99_R7D.blend` · SHA256 `9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e`. Hash comprobado después del render, sin modificar el archivo. No se renderizó vídeo.

Se generaron 19 vistas equivalentes, 4 retratos, un detalle de bañera y una vista del acceso directo dormitorio–estar. Parámetros comunes: Cycles OptiX, 256 muestras, denoise OIDN, umbral adaptativo 0,009, AgX Medium High Contrast y exposición +0,35 EV. Paisajes 2000×1500, exterior principal 2400×1800 y retratos 1800×2400. Dos pausas controladas cedieron GPU para verificar el visor y las siguientes ejecuciones retomaron por hash los archivos existentes.

## Puntos prioritarios para la siguiente revisión

- **Huerta:** rosetas con hojas angulosas y repetidas, lectura de origami; cultivos de hoja ancha aún simplificados. Evidencia `huerta.png` y recorte 1:1.

- **Textiles:** dobladillo del cobertor con tiras finas y pliegues rígidos; bandas regulares en cabecero/sillas; prendas del vestidor demasiado planas. Evidencia `dormitorio.png`, `dormitorio_retrato.png`, `cocina.png` y `vestidor.png`.

- **Espejo del baño del quincho:** reflexión del ladrillo en diagonales/chevrones estirados, anómala para un espejo plano. Identificar primero si procede de normales del espejo o geometría/UV reflejada. Evidencia `bano_quincho.png`.

- **Ergonomía por medir:** vuelo de isla frente a taburetes; altura de teclado respecto a asiento y hueco de rodillas de consola. Son sospechas visuales señaladas para contraste dimensional, no cotas inferidas de perspectiva.

- **Encuadres y contexto:** medianera domina la vista de pileta; varias tomas de baño recortan aparatos y requieren verse juntas; terreno exterior/horizonte siguen poco naturales. Se conservaron los encuadres del candidato durante esta entrega.

La imagen del WC mejora contorno y separación de sus piezas grandes. Los solapes entre piezas pequeñas de bisagras identificados por la auditoría geométrica deben clasificarse y corregirse aparte; estas fotografías no constituyen aprobación mecánica.

## Observaciones por imagen

### Casa y paisaje — exterior

[exterior.png](stills/exterior.png) · 1200×900 vista general; original 2400×1800 · cámara `CAM | Presentación verticales corregidas`, frame 1.

- La envolvente, balcón, escalera, quincho y cubiertas escalonadas se leen sin oclusiones importantes.

- El agua refleja cielo y entorno; el jardín mantiene transición con zonas de paso.

- El terreno exterior al lote conserva una extensión muy uniforme y gris parda; es un límite visible de naturalidad a escala de la imagen.

### Pileta y playa húmeda — pileta

[pileta.png](stills/pileta.png) · 1200×900 vista general; original 2000×1500 · cámara `CAM | Pileta & playa húmeda`, frame 1.

- El agua, playa húmeda y escalera se leen con continuidad; reflejos y refracción visibles.

- El gran paño blanco de medianera ocupa buena parte del primer plano y oculta el lateral próximo de pileta. Una toma complementaria interior al lote permitiría revisar el borde completo.

### Huerta y jardín — huerta

[huerta.png](stills/huerta.png) · 1200×900 vista general; original 2000×1500 · cámara `CAM | Huerta`, frame 1.

- Los cultivos del cantero próximo muestran rosetas de hojas angulosas con pliegues rígidos: apariencia de origami, claramente visible a escala de imagen.

- El cantero derecho tiene hojas anchas oscuras con escasa variación orgánica; todavía se leen como geometría simplificada.

- El césped presenta distribución de briznas y densidad visual bastante uniformes; falta naturalidad local.

### Estudio de grabación — estudio

[estudio.png](stills/estudio.png) · 1200×900 vista general; original 2000×1500 · cámara `LUZ99 | Estudio amplitud`, frame 150.

- La altura libre, paneles suspendidos, ventana, mesa y equipo se leen; la pantalla DAW contiene detalle y no queda sobreexpuesta.

- Controles de consola y cajas del equipo todavía se leen como piezas genéricas repetidas; los paneles negros son muy uniformes en el plano próximo.

- La vista es válida para auditar distribución, pero el equipo cercano sigue limitando la credibilidad de fotografía de un estudio real.

### Cocina de la vivienda — cocina

[cocina.png](stills/cocina.png) · 1200×900 vista general; original 2000×1500 · cámara `REV | Cocina comedor`, frame 150.

- Cocina, heladera, campana, mesada reacomodada y mesa se leen; acceso lateral despejado y reflejos del vidrio coherentes.

- En sillas próximas se ven bandas horizontales regulares en la tapicería, con lectura similar a veta; conviene revisar textura/UV antes de reclamar fotografía indistinguible.

- Electrodomésticos y objeto cilíndrico sobre mesa siguen siendo muy simplificados de cerca.

### Quincho y línea de fuego — quincho

[quincho.png](stills/quincho.png) · 1200×900 vista general; original 2000×1500 · cámara `REV | Quincho y extracción`, frame 150.

- Barra y parrilla quedan paralelas; mesa y sillas se ubican hacia el jardín y la circulación lateral se lee.

- La carpintería corrediza y línea de fuego son visibles. Campana y conducto ennegrecen la franja alta, pero conservan volumen.

- Mesadas y mobiliario siguen muy limpios/uniformes; mejora geométrica clara, realismo de materiales aún limitado en primer plano.

### Dormitorio — dormitorio

[dormitorio.png](stills/dormitorio.png) · 1200×900 vista general; original 2000×1500 · cámara `REV | Dormitorio completo`, frame 1.

- La ventana queda junto al lado longitudinal de la cama; cama y mesas de luz no se ven atravesadas por puertas.

- El borde transversal de la ropa de cama presenta pliegues muy agudos y tiras delgadas superpuestas, con lectura de papel más que tejido.

- Cabecero tapizado muestra bandas horizontales regulares similares a las sillas de cocina. Almohadas y superficie principal del cobertor resultan demasiado uniformes.

### Acceso al dormitorio — dormitorio_acceso

[dormitorio_acceso.png](stills/dormitorio_acceso.png) · 1200×900 vista general; original 2000×1500 · cámara `REV | Dormitorio acceso`, frame 1.

- La cámara conserva vista clara de cama y acceso lateral, sin hoja dentro del plano de cámara.

- Esta vista confirma los pliegues rígidos del borde de ropa de cama y las bandas del cabecero; son visibles a escala normal de publicación.

### Vestidor — vestidor

[vestidor.png](stills/vestidor.png) · 1200×900 vista general; original 2000×1500 · cámara `REV | Vestidor circulación`, frame 1.

- La exposición permite leer estantes, cajones y prendas; mejora respecto del vestidor oscuro.

- Encuadre frontal de placard: útil para mobiliario, muestra muy poco de la circulación del vestidor.

- Las prendas se leen como tiras muy planas y repetidas, sin una silueta de ropa convincente. La zona de barra/prendas junto al divisor derecho merece contraste geométrico de apoyos; no afirmo un choque sólo por la imagen.

- La veta se repite con escala y contraste fuertes en paneles próximos.

### Baño de la vivienda — bano

[bano.png](stills/bano.png) · 1200×900 vista general; original 2000×1500 · cámara `REV | Baño completo`, frame 1.

- Lavatorio, bañera, rociador, hornacina y pavimento se leen sin exposición quemada dominante.

- La vista titulada baño completo recorta WC y bidé en el borde derecho/inferior. Debe leerse junto a las tomas de acceso, no como cobertura completa autónoma.

- El revestimiento blanco continuo y la bañera presentan muy poca variación superficial visible; grifería/lavatorio son geométricamente simplificados.

### Baño desde el acceso — bano_acceso

[bano_acceso.png](stills/bano_acceso.png) · 1200×900 vista general; original 2000×1500 · cámara `REV | Baño desde acceso`, frame 150.

- Esta toma complementa la principal: se ven la taza WC, cisterna, tapa y el espacio ante bañera; ya no aparece el zócalo huérfano.

- Bidé y lavatorio quedan parcialmente fuera del encuadre; cobertura de baño requiere la serie completa.

- El vidrio se distingue por bordes/reflexión, y el desagüe de bañera es visible. La fotografía no permite certificar los mecanismos internos de bisagras SAN99.

### Comunicación entre baño y comedor — puerta_bano

[puerta_bano.png](stills/puerta_bano.png) · 1200×900 vista general; original 2000×1500 · cámara `REV | Baño acceso comedor`, frame 150.

- La comunicación comedor–baño está claramente representada; hoja corrediza retirada, hueco y umbral visibles.

- El paso hacia lavatorio/bañera se lee y no hay cámara atravesando la hoja.

- La madera de la hoja muy próxima presenta un acabado brillante y veta dominante; revisar concordancia con el acabado elegido.

### Cocina e isla del monoambiente — mono_cocina

[mono_cocina.png](stills/mono_cocina.png) · 1200×900 vista general; original 2000×1500 · cámara `REV | Mono cocina e isla`, frame 1.

- Cocina en L, isla y salida al quincho se leen completas.

- Los taburetes se sitúan delante de un frente macizo; el vuelo de mesada parece corto. Verificar con cotas el espacio para rodillas antes de aprobar uso como barra.

- El volumen negro alto y los electrodomésticos carecen de detalles cercanos suficientes para una lectura fotográfica; mesadas muy uniformes.

### Distribución del monoambiente — mono_distribucion

[mono_distribucion.png](stills/mono_distribucion.png) · 1200×900 vista general; original 2000×1500 · cámara `REV | Mono distribución`, frame 1.

- Vista clara del frente operativo de isla, sofá y circulación del monoambiente.

- Se confirma el frente de isla macizo; el vuelo hacia taburetes debe medirse en conjunto con mono_cocina.

- No muestra el acceso al baño reubicado; esa correspondencia requiere plano/recorrido y las dos vistas específicas del baño PB.

- Tapicería del sofá y frentes de cocina muy uniformes de cerca.

### Ducha del monoambiente — bano_mono

[bano_mono.png](stills/bano_mono.png) · 1200×900 vista general; original 2000×1500 · cámara `REV | Baño mono`, frame 150.

- La vista final conserva el encuadre de prueba: rociador, lavatorio, mampara y desagüe incluidos.

- Juntas del piso y revestimiento se leen proporcionadas, sin defecto de escala grueso visible.

- Porcelana, espejo y grifería aún tienen modelado simple; no se observó regresión visual del ajuste sanitario en la integración R7D.

### Sanitarios del monoambiente — bano_mono_sanitarios

[bano_mono_sanitarios.png](stills/bano_mono_sanitarios.png) · 1200×900 vista general; original 2000×1500 · cámara `REV | Baño mono sanitarios`, frame 150.

- Contorno de WC, asiento, tapa y cisterna continuo; la interferencia gruesa anterior entre asiento y depósito ya no aparece visualmente.

- La relación con puerta y piso queda visible, y las juntas mantienen escala coherente con el encuadre.

- Las pequeñas bisagras son visibles, pero esta vista no resuelve ni aprueba los solapes mecánicos señalados por el crítico.

### Baño del quincho — bano_quincho

[bano_quincho.png](stills/bano_quincho.png) · 1200×900 vista general; original 2000×1500 · cámara `REV | Baño quincho`, frame 150.

- WC orientado correctamente y con contorno continuo; lavatorio y relación entre artefactos visibles.

- El espejo muestra una reflexión del ladrillo en grandes diagonales/chevrones estirados, no plausible como espejo plano. Revisar normales/suavizado del espejo y geometría/UV reflejadas.

- Boca de taza simplificada y grifería genérica siguen limitando el realismo cercano.

### Escalera y desembarco — escalera

[escalera.png](stills/escalera.png) · 1200×900 vista general; original 2000×1500 · cámara `REV | Escalera y desembarco`, frame 150.

- Peldaños, zancas, barandas, fijación superior y desembarco se leen con detalle.

- La toma recorta el apoyo inferior de la escalera; para auditar esa unión hace falta el detalle/plano o un encuadre complementario.

- Los reflejos del vidrio y la lectura de ladrillo/metal son coherentes; no aparece una hoja bloqueando el desembarco en esta vista.

### Cubiertas a distinta altura — cubiertas

[cubiertas.png](stills/cubiertas.png) · 1200×900 vista general; original 2000×1500 · cámara `REV | Cubierta escalonada`, frame 1.

- Se ven cubierta alta, tramo bajo adyacente, canaleta, bajada y salidas de conductos.

- El acabado de chapa mantiene ritmo y reflejos coherentes; los elementos quedan legibles.

- El terreno exterior plano y la transición al horizonte HDRI mantienen una separación visual evidente. El entorno no puede tomarse como relevamiento real del emplazamiento.

### Estudio, composición vertical — estudio_retrato

[estudio_retrato.png](stills/estudio_retrato.png) · 900×1200 vista general; original 1800×2400 · cámara `LUZ99 | Estudio retrato`, frame 150.

- El retrato aporta buena lectura de techo y paneles respecto a puesto de trabajo; cámara libre de oclusión.

- Comprobar altura de teclado/superficie frente a asiento y espacio de rodillas bajo consola: visualmente teclado alto y frente inferior macizo. Requiere medidas, no inferencia desde perspectiva.

- Controles genéricos, repetición y uniformidad superficial del equipo persisten como límite fotográfico.

### Dormitorio, composición vertical — dormitorio_retrato

[dormitorio_retrato.png](stills/dormitorio_retrato.png) · 900×1200 vista general; original 1800×2400 · cámara `LUZ99 | Dormitorio retrato`, frame 1.

- Ventana, cortina y relación de cama con muro y techo quedan claras en vertical.

- El encuadre destina mucho espacio al muro/cielorraso vacío y recorta parte del pie de cama; puede refinarse para una fotografía editorial.

- Persisten los pliegues rígidos del cobertor y las bandas del cabecero; la vista vertical confirma que no son sólo un efecto de la primera cámara.

### Vestidor, composición vertical — vestidor_retrato

[vestidor_retrato.png](stills/vestidor_retrato.png) · 900×1200 vista general; original 1800×2400 · cámara `LUZ99 | Vestidor retrato`, frame 1.

- La toma vertical permite revisar casi todo el placard y su iluminación interior, sin bloqueo por puertas.

- La ropa continúa leyendo como tiras largas planas, con muy poca variación de caída y detalle textil.

- La relación de la barra y prendas con el divisor derecho debe verificarse geométricamente; posible incongruencia visual de apoyo/ocupación, no choque confirmado por imagen.

- La repetición y escala dominante de veta siguen visibles en la carpintería.

### Jardín, composición vertical — exterior_retrato

[exterior_retrato.png](stills/exterior_retrato.png) · 900×1200 vista general; original 1800×2400 · cámara `LUZ99 | Exterior jardin retrato`, frame 1.

- La composición vertical muestra vivienda, cubierta elevada del estudio, balcón, quincho y pileta con lectura clara.

- Árbol próximo aporta profundidad; no se ve una oclusión que impida entender la envolvente principal.

- Persisten la uniformidad del césped y terreno exterior y el contexto de horizonte genérico. No sustituye vista catastral/levantamiento de la propiedad.

### Bañera de la vivienda, detalle a altura de uso — bano_humano

[bano_humano.png](stills/bano_humano.png) · 1200×900 vista general; original 2000×1500 · cámara `LUZ99 | Bano suite humano`, frame 1.

- Funciona como detalle de bañera a altura de uso, coherente con el título corregido; no se presenta como vista total del baño.

- Mampara, grifería, hornacina y parte de WC/lavatorio visibles; misma lectura material que la prueba sanitaria.

- Los aparatos recortados en bordes requieren los otros encuadres. Superficies blancas y piezas cercanas conservan simplificación perceptible.

### Puerta directa del dormitorio al estar — dormitorio_puerta

[dormitorio_puerta.png](stills/dormitorio_puerta.png) · 1200×900 vista general; original 2000×1500 · cámara `LUZ99 | Acceso dormitorio desde estar`, frame 150.

- El acceso directo estar–dormitorio queda mostrado; se distingue el paso y la cama, sin cámara dentro de una hoja.

- La hoja del paso al vestidor se ve al fondo; su posición reduce vista del interior, pero el recorrido físico fue comprobado por separado.

- En la hoja de madera del fondo aparece una franja especular diagonal muy marcada. Revisar normales/suavizado de caras planas y mapa normal para descartar artefacto de sombreado.

## Integridad y evidencia

Los 25 PNG pasaron hash, dimensión y decodificación. Se generaron 5 contactos en `stills/contacts`; manifiesto `integrity.json`. Los recortes 1:1 de huerta, ropa de cama, equipo y sillas están en `stills/detail_crops`, con cajas de recorte y hashes. Ninguna imagen fue retocada para ocultar geometría.

El índice técnico de cámaras, focales, desplazamientos, poses y tiempos está en `stills/manifest.json`. El listado estructurado de hallazgos está en `constructor_visual_review.json`.
