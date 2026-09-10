# Crítica independiente del visor web · Iteración 02

**Nota: 8/10. Alcanza el umbral solicitado para esta entrega interactiva.**

Las tres pasadas resolvieron los problemas que impedían aprobar la primera versión. La representación conserva la arquitectura auditada, las vistas permiten entender el proyecto y los controles ya informan correctamente sus estados. Existe progreso comprobable respecto del 7 anterior. Esta nota aprueba el visor revisado; no significa fotorealismo máximo ni certificación técnica de la construcción.

## Estado auditado

Estado congelado del 10 de septiembre de 2026:

- viewer.js SHA256: 5EBED471FEF9383AFCA3F544585EA42289E391371162F1E8E6CE563DCAA64AFF
- viewer.css SHA256: E1023D5302E0FCF849ABBE7EE2AA1AF1819DD52A5B01EB19D2D42EDFF19C7D78
- house.glb SHA256: 3EE11DE28D53A4E215C6EBB8D8E895478B2CA5BC18C213C6B007CD8DACC4E394

El GLB permanece idéntico al de la primera auditoría web. El origen declarado sigue siendo Casa_de_Campo_Final.blend, SHA256 58223D78F71DC0C1D4F33034AAAF0BE96A1BD420F72F2231468003E942C2BBFE.

Revisé el código actualizado, el proceso reproducible de horneado de materiales desde Blender y las imágenes nuevas. Ejecuté tres scripts propios en sesiones independientes de Chrome headless, sin modificar visor ni modelo. Los resultados están en audit/web_independent_02.json, audit/web_detail_checks_02.json y audit/web_final_checks_02.json. Las capturas propias conservan el sufijo 02.

## Cierre de los hallazgos anteriores

| Hallazgo de la primera auditoría | Evidencia independiente de esta revisión | Dictamen |
|---|---|---|
| Cota anunciada distinta del corte | Con corte a 4,50 m, título, control y plano real indican 4,50. Al desactivar, el título queda «Planta baja» y hay cero planos de recorte. | Resuelto |
| Vestidor oculto por puertas | Cámara en [18.55, 4.85, 8.75], puertas cerradas y placard completo visible. Se leen ambos accesos y el piso de circulación. | Resuelto |
| Exterior móvil recortado | En 390 × 844 se leen la casa completa, su cubierta escalonada, escalera, pileta y parte del jardín. Inicio reproduce exactamente la posición inicial. El cambio a horizontal y el regreso a vertical recuperan los encuadres correspondientes. | Resuelto para las dimensiones ensayadas |
| Rótulos ilegibles sobre fondos oscuros | Fondo claro estable; «Estudio de grabación» y «Vestidor pasante» se leen sobre acústicos y madera. | Resuelto |
| Maderas principales sin veta ni parquet | 193 mallas usan materiales restaurados con mapas. Se ven veta en puertas y placares, y juntas de parquet en el piso. El proceso toma el color de los materiales del archivo final. | Resuelto en las superficies principales |

La imagen audit/web_vestidor_independent_02.png demuestra particularmente bien el avance: desaparecen las dos grandes obstrucciones de la versión anterior y la madera recupera dirección y escala. audit/web_mobile_independent_02.png y audit/web_home_mobile_02.png documentan el nuevo encuadre del teléfono. audit/web_studio_mobile_independent_02.png verifica el contraste del rótulo.

## Fidelidad e interacción

La comparación propia de las 2.349 cajas de geometría antes y después no encontró cambios de nombre ni de límites mayores que 0,00000001 m: audit/web_geometry_compare_02.json. En conjunto con el hash idéntico del GLB y la lectura del código, esto confirma que las correcciones web no desplazaron la arquitectura. La comparación de cajas por sí sola no demostraría igualdad de todas las caras; aquí se acompaña de la identidad binaria del archivo.

Se conservan las 12 puertas. Hice clic real sobre el portón: el visor seleccionó «Portón negro», abrió solamente gate y mantuvo los otros once destinos cerrados. El estado general pasó a «Personalizadas». La apertura individual alcanzó 0,99999287. La evidencia está en audit/web_final_checks_02.json.

Ocultar cubiertas y vegetación dejó cero mallas visibles de esas categorías. El corte horizontal respondió al control. No hubo errores de JavaScript ni respuestas HTTP fallidas en las comprobaciones propias. No apareció desbordamiento horizontal en 1440, 390 ni 844 px. El menú móvil abre completamente y se cierra al elegir una vista.

No detecté un bloqueo nuevo en la arquitectura, el vestidor, las vistas generales, las superficies modificadas o la combinación de controles ensayada.

## Rendimiento y límites medidos

La carga local hasta estado listo fue de 2,13 s. El GLB sigue pesando 10.021.880 bytes. El exterior mostró 789.066 triángulos y 196 llamadas de dibujo: el material restaurado añadió dos llamadas respecto de la versión anterior.

En el primer muestreo después de cambiar opciones apareció un cuadro de aproximadamente 600 ms. No lo oculto ni lo describo como una experiencia siempre fluida. En un segundo muestreo independiente, después de estabilizar la vista y los materiales, 120 cuadros promediaron 16,65 ms, con máximo 16,80 ms y ninguno mayor de 50 ms. Esto respalda una interacción estable cercana a 60 fps en esta máquina; no garantiza ese rendimiento en un teléfono físico de menor capacidad.

## Mejoras que siguen abiertas, sin impedir esta aprobación

- La luz en tiempo real y los blancos interiores siguen siendo más uniformes que en Cycles. Sombras de contacto y mayor diferenciación de tejidos podrían enriquecer futuras versiones.
- El material secundario «Madera oscura | woodDark» aún carece de mapa. La recuperación comprobada alcanza roble, nogal y parquet principales.
- En el teléfono horizontal de 844 px aparece la interfaz de escritorio y su ayuda menciona rueda y botón derecho. Conviene ajustar esa ayuda también a la capacidad táctil del dispositivo.
- El encuadre móvil ahora prioriza entender el conjunto y deja aire alrededor de la casa. Hay margen para afinar su composición, pero ya no exige corregir el zoom para reconocer el proyecto.
- La pausa inicial observada al cambiar opciones merece seguimiento en dispositivos reales. Una optimización futura puede precalentar las variantes de material usadas por el corte.

## Alcance de la aprobación

**Aprobado con 8/10 para publicar el visor interactivo revisado.** Las vistas PB y PA son perspectivas con corte horizontal; no sustituyen las plantas y secciones documentadas del proyecto.

Esta auditoría comprobó http://127.0.0.1:8420/. La carga pública de GitHub Pages, sus rutas de recursos y sus respuestas HTTP deben verificarse después del despliegue antes de afirmar que el sitio está publicado correctamente. No se requirió ni se revisó un vídeo nuevo, que continúa fuera de este encargo.
