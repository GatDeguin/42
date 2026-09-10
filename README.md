# Casa de campo · Reconstrucción arquitectónica

Reconstrucción editable en Blender 5.2 del proyecto definido por casa_campo_estudio_interactivo_mejorado_v3.html.

**Estado:** revisión arquitectónica en curso. Primera evaluación independiente provisional: **6/10**. El renderizado del video está pausado por pedido del propietario y requiere su aprobación explícita para reanudarse.

## Proyecto

- Lote: 22 × 20 m; casa: 8 × 12 m; pileta: 7 × 3 m.
- Escalera exterior de 18 peldaños y descanso de 1 × 1 m.
- Estudio con 3,20 m libres, según la decisión del propietario.
- Conversión de ejes: HTML (X, Y, Z) → Blender (X, −Z, Y). Unidades: metros.
- Cámaras originales, puertas con pivotes y drivers, recorrido continuo y tomas para montaje.
- Materiales y referencias empaquetados en el archivo Blender.

## Archivos y carpetas

- output/Casa_de_Campo.blend: escena editable (Git LFS).
- output/Casa_de_Campo_Atardecer.png: render principal.
- output/control_*.png: vistas interiores de revisión.
- output/validation.json: comprobaciones geométricas automáticas.
- review/: plantas y cortes derivados de la geometría real.
- audit/: informes del crítico independiente.
- scripts/: extracción, construcción, mejoras, comprobación y render.
- source/original.html: fuente arquitectónica original.
- source/request.txt: alcance de la reconstrucción.

## Revisión

Por cada evaluación inferior a 8/10 se realizan tres pasadas de corrección antes de volver a presentar la escena al crítico: construcción y encuentros; cámaras y lectura espacial; materiales, vegetación e iluminación. Se conserva la arquitectura explícita de la fuente y se documentan los ajustes.

La revisión visual y geométrica no reemplaza documentación estructural calculada. Los detalles ausentes en el HTML se identifican como desarrollo del modelo.

## Recursos

Mapas de materiales generados por el HTML. Entorno [Belfast Sunset, Poly Haven](https://polyhaven.com/a/belfast_sunset), CC0.
