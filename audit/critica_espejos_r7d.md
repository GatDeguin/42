# Auditoría acotada — óptica de espejos R7D

**Hallazgo confirmado:** las caras ópticas planas de los espejos del quincho y de la suite tienen normales de sombreado que simulan una superficie curva. Es un error del modelo que distorsiona la reflexión; no corresponde a un espejo arquitectónico plano. Debe corregirse antes de dar por logrado el realismo fotográfico. **Sin nota global en este informe.**

Fuente de sólo lectura: `output/Casa_de_Campo_99_R7D.blend`, SHA-256 `9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e`. Se contrastó la imagen existente `review99/r7_final/stills/bano_quincho.png`. No hubo render ni guardado de la fuente.

## Medición

| Objeto | Desviación de normales de esquina respecto de la cara plana | Desviación de dirección reflejada en 14 muestras interiores |
|---|---:|---:|
| Espejo baño pileta, correspondiente al quincho | 27,38°–31,02° | 1,68°–**53,77°** |
| Espejo baño suite | 28,35°–31,59° | 1,72°–**42,37°** |
| Espejo baño mono, control | 0° | 0° |

Las cuatro caras triangulares mayores de cada espejo son planas; se midieron sus vértices, normales geométricas y normales personalizadas de esquina. En quincho y suite estas últimas están inclinadas en distintas direcciones. La interpolación sobre los triángulos crea el aspecto de deformación continua y quiebres diagonales observados.

Los tres objetos no tienen modificadores activos. Por tanto, no hay un Bevel en ejecución que se pueda simplemente desactivar: el problema está incorporado en las normales de la malla evaluada. El material compartido `Espejo con respaldo opaco | mirror` usa Metallic 1, Roughness 0,025 y no tiene Normal/Bump conectado. El espejo del mono utiliza ese mismo material y conserva normales planas, lo que separa el defecto local de geometría del material común.

## Comprobación del reflejo

Se tomaron siete posiciones interiores en cada uno de los dos triángulos visibles de cada espejo. Desde sus cámaras del modelo se comparó la reflexión ideal usando la normal geométrica con la reflexión usando la normal interpolada actual; luego se lanzaron los rayos a la escena. Es una prueba analítica de primer rebote, sin muestreo de rugosidad y sin sustitución del render.

En el quincho cambia el punto alcanzado en las paredes/puerta; en algunas muestras de suite el rayo desviado vuelve a alcanzar el propio espejo. El control del mono coincide exactamente. La prueba confirma una causa suficiente de deformación óptica y no depende de la distribución UV del ladrillo. **No se infiere de ello que todas las UV de las paredes hayan sido auditadas o estén libres de defectos.**

Evidencia: `audit/r7d_preliminary/mirror_probe.json` y `mirror_rays.json`; scripts `audit/r7d_mirror_probe.py` y `r7d_mirror_rays.py`.

## Corrección y cierre exigidos

1. Restaurar normales constantes en cada cara óptica principal de quincho y suite, conservando cantos/biseles y separación de sus normales. No aplanar el volumen físico del respaldo ni deformar la superficie para compensar la imagen.
2. Repetir el control sobre la geometría exportada/evaluada. Para este espejo ideal plano, la cara óptica debe mantener desviaciones numéricas despreciables respecto de su normal; el bisel puede conservar normales propias.
3. Volver a producir las vistas humanas del baño y una toma oblicua desde el SHA corregido. Las hiladas reflejadas deben conservar la geometría proyectiva propia de un plano, sin abombamiento ni cheurones artificiales.
4. Mantener la versión R7D publicada identificada como candidata con este defecto pendiente; no atribuirle cierre fotográfico por el hecho de que el material sea metálico o que el visor cargue correctamente.
