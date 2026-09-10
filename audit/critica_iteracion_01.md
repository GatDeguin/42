# Auditoría crítica independiente · Iteración 1
Fecha: 10/09/2026. Estado: REQUIERE MEJORAS. Puntaje global: **6,0 / 10**.

Se inspeccionaron la petición completa, el inventario HTML, el archivo Blender reabierto en un proceso independiente, la imagen principal de 2400 × 1800, seis imágenes interiores actualizadas, y las plantas/cortes derivados de la malla. La extracción independiente queda en audit/geometry_bounds.json. El modelo es una reconstrucción avanzada, pero todavía no alcanza el nivel de una presentación arquitectónica resuelta.

El puntaje evalúa la entrega de visualización y su coherencia espacial/constructiva visible. No equivale a aprobar un proyecto ejecutivo o un cálculo estructural. No se exigen cálculos que no existen en la fuente.

## Evaluación
| Área | Puntaje | Motivo |
|---|---:|---|
| Fidelidad dimensional a HTML | 8,5 | Huella, implantación, pileta, niveles, cámaras y distribución conservados. |
| Espacio y funcionamiento | 6,0 | Puertas animadas, pero portón atraviesa muro; falta revisión de barridos y vistas legibles. |
| Coherencia constructiva | 5,0 | Extracciones sin salida, encuentros incompletos, acústicos superpuestos, protección de barandas insuficientemente detallada. |
| Materiales y modelado de detalle | 6,0 | Buenos materiales base y cavidades nuevas; mobiliario/metal/vegetación todavía esquemáticos. |
| Luz, paisaje y composición | 5,5 | Referencia cálida y rica; entrega con horizonte vacío, iluminación desigual y encuadre que casi elimina pileta. |
| Evidencia de revisión | 7,0 | 33 verificaciones útiles y planos reales, pero no sustituyen comprobar colisiones, visibilidad y encuentros. |

## Hallazgos que impiden aprobar

### P1 · El portón se introduce íntegramente dentro del muro
En pose abierta, Portón negro ocupa X 7,95–10,95 y coordenada Blender Y −0,07..+0,03; Muro frontal izquierdo ocupa X 0–11 y Y −0,10..+0,06. Hay superposición completa. El driver se mueve, pero el mecanismo no funciona constructivamente.
Corrección: añadir un desplazamiento normal al cerramiento/riel paralelo por el interior antes de correr, o establecer la hoja en una vía paralela que mantenga luz de acceso de 3 m. Documentar cualquier ajuste de pocos centímetros a la fuente. Comprobar todo el barrido, no solo extremos.

### P1 · Horno y parrilla no tienen extracción continua
Chimenea horno termina en cota +2,680; campana parrilla en +2,730. Losa PA comienza en +3,000. No se identifica conducto continuo ni salida exterior.
No se puede prolongar el horno verticalmente sin revisar: su eje X 21,25 / Z fuente 6,75 atraviesa la bañera de arriba, que ocupa X 20,455–21,705 / Z 6,45–7,19. La parrilla bajo X 21,17 / Z 9,44 coincide con cocina superior.
Corrección: trazar dos recorridos de extracción plausibles, representados en planta y sección, con patinillo y paso de cubierta. Posible zona a estudiar: rincón posterior-derecho del estudio, X aproximadamente 21,45–21,79 / Z 5,40–5,80, sujeto a revisión de paneles, baño PB, altura del conducto horizontal y mantenimiento. Esta propuesta es una inferencia de detalle, no una orden de cambiar distribución. No dar por resuelto un tubo que atraviese sanitarios o muebles.

### P1 · Acústicos solapados al elevarlos
Se cumple cota inferior +6,45 y altura libre 3,20 sobre piso +3,25. Sin embargo, Bafles 3/4 se intersectan con Clouds 1/2.
Ejemplo: Bafle 3 = X 17,45–18,37, Z fuente 1,70–4,30, altura 6,45–6,57. Cloud 1 = X 17,35–19,45, Z 1,64–2,66, altura 6,45–6,51. La intersección es aproximadamente 0,92 × 0,96 × 0,06 m.
Corrección: recortar o unir los módulos para producir una sola geometría física coherente conservando el tratamiento y la altura autorizada. Evitar caras coplanares duplicadas.

### P1 · Vistas de dormitorio y baño bloqueadas
control_Dormitorio dedica casi media imagen a la cara próxima de un mueble. control_Bano está casi completamente tapada por una hoja. No son pruebas suficientes de calidad interior ni de circulación. Las cámaras HTML deben conservarse, pero se necesitan cámaras de presentación suplementarias, y verificación visual de cada tramo del tour en poses reales de puertas.
Corrección: mostrar dormitorio completo, relación cama–placard–acceso y baño completo con lavabo, inodoro, bidé y bañera, sin esconder elementos para renderizar.

### P2 · Protección y encuentros de balcones/escalera sin resolver
Baranda lateral tiene un vacío inferior de aproximadamente 0,5425 m y otro de 0,457 m entre sus dos líneas horizontales. No basta indicar altura 1,05 m para representar una protección razonable de borde.
Corrección: completar paños con elementos finos compatibles con la referencia y conservar altura/posición. Mostrar anclajes plausibles, continuidad en esquina y desembarco, y remate de losa/goterón. La fuente ya incluye zancas, placas de unión superiores y bulones: no duplicarlos innecesariamente.

Escalera conserva 18 peldaños, huella efectiva 0,2111 m y contrahuella entre peldaños 0,17444 m. Es compacta y empinada por mandato de la fuente; no ampliar su desarrollo de 3,80 m silenciosamente. Revisar primer escalón contra piso de arranque real (+0,06 de referencia), apoyo inferior, continuidad de pasamanos y antideslizantes. El corte actual por eje no muestra las zancas porque están a los lados; agregar elevación lateral del conjunto.

### P2 · Cubierta y cielorraso requieren un encuentro creíble
El cielorraso está a +6,450..6,468 y el faldón frontal se adelgazó conservando cara exterior. En el borde delantero interior hay muy poco espacio disponible entre ambos. Los cortes muestran envolvente y paneles, pero no un conjunto de correas/soportes, fijaciones o solución de borde que explique cómo se sostiene la cubierta y cómo remata el cielorraso.
Corrección: sección ampliada de borde + sección en zona media, con componentes dimensionados que quepan realmente. No añadir vigas que atraviesen el cielorraso para luego ocultarlas. Se puede inferir detalle constructivo compatible; no se necesita cálculo estructural inexistente en HTML.

### P2 · Paisaje y luz no alcanzan la referencia
La imagen principal deja un gran campo verde plano y un horizonte abrupto. Se ven discos de base de árboles fuera de la medianera; árboles similares repetidos y hojas grandes dan aspecto de maqueta. Césped aparece en franjas discontinuas con cambios de densidad demasiado visibles.
Corrección: continuidad de suelo/vegetación, eliminar bases artificiales visibles, variar escala y orientación de vegetación secundaria, mejorar transición de césped, conservar árboles y elementos principales de fuente.
La luz de cielo es gris y deslavada; las mesadas de cocina aparecen excesivamente blancas y el acero tiene rayado de escala exagerada. Equilibrar potencia/temperatura de prácticas y exposición; ajustar metal y madera a escala física, evitando ruido fuerte.
El encuadre corta casi toda la pileta y dedica bastante espacio al cielo; una cámara adicional más cercana a la composición de referencia debe mostrar jardín y agua sin cambiar las cámaras originales.

## Evidencia requerida en próxima presentación
1. Plantas PB y PA con hojas abiertas/cerradas, barridos y anchos libres; zoom del acceso estudio y secuencia dormitorio–vestidor–baño.
2. Corte de extracción desde horno y parrilla hasta salida exterior, con planta del patinillo, comprobando no interferencia con sanitarios/cocina.
3. Detalle de cubierta/cielorraso a +6,45 y plano de tratamiento acústico sin sólidos solapados.
4. Elevación completa de escalera y detalle de arranque/desembarco; balcón con remates/anclajes.
5. Imagen principal revisada, vistas interiores legibles y contact sheet del tour que cubra cada ambiente y transición.
6. Verificación geométrica de barridos de puertas, en particular portón; la prueba 'driver se mueve' no es una comprobación de funcionamiento.
7. Registrar inferencias separadas de las dimensiones explícitas de HTML.

## Tres pasadas del constructor antes de nueva auditoría
1. Resolver funcionamiento y construcción: portón, extracción, acústicos, barandas, cubierta y encuentros; regenerar evidencia dimensional.
2. Resolver espacio y presentación: cámaras suplementarias, barridos de puertas, trayectorias y encuadres. Revisar muestras del tour antes del render completo.
3. Resolver apariencia: luz, escala de materiales, vegetación, césped, agua y composición. Renderizar nueva imagen principal y controles consistentes.

Criterio para alcanzar 8: hallazgos P1 cerrados con evidencia; detalles P2 resueltos o limitaciones específicas documentadas sin ocultarlos; arquitectura legible en imágenes y recorrido; mejora material/lumínica clara respecto a esta entrega. Mantener la prioridad de exactitud arquitectónica sobre decoración.

## Cambio de alcance comunicado al cerrar la auditoría
El constructor informa una nueva instrucción del usuario: el techo del estudio debe quedar más alto que el de la vivienda. Esta auditoría puntúa el modelo inspeccionado, anterior a ese cambio. La próxima revisión verificará una cubierta escalonada coherente, el remate vertical entre módulos, encuentros impermeables, soporte y aislamiento reales; conservará la altura libre de estudio aprobada de 3,20 m. La elevación definitiva debe constar como decisión explícita/inferencia documentada. Esta modificación puede resolver la estrechez del borde de cubierta, pero requiere nuevos cortes y render.
