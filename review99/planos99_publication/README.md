# Publicación aislada de planos R7D

Destino: docs/planos99/. No se sustituyen los planos R6K de docs/planos/.

Fuente: output/Casa_de_Campo_99_R7D.blend
SHA256: 9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e
Estado: EN REVISIÓN / SIN APROBACIÓN 9,9.

El PDF conserva los bytes de la emisión revisada. El ZIP de publicación se recompone con nombres de descarga estables y sus registros; por eso difiere del ZIP local de trabajo. Contiene un PDF de 33 A2, 33 SVG, 33 DXF y los registros/manifiestos. El PDF es vectorial, con 209 cotas nativas DXF y fuente mínima de 2,5 mm. La auditoría recalcula 42 dimensiones críticas y las operaciones de todas las cotas.

La navegación enlaza ../ al visor principal R7D y ../renders99/ a la galería de 25 fotografías. El publicador exige que el manifiesto de la galería tenga la misma SHA. No se modificaron el visor, los renders ni la fuente Blender.

## Reproducir

```text
python scripts/planos95_emit.py --model output/Casa_de_Campo_99_R7D.blend --out planos95/r7d_candidate --expected-sha 9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e --status "EN REVISION R7 / SIN APROBACION 9,9"
python scripts/planos95_publish.py --source planos95/r7d_candidate --dest docs/planos99 --expected-sha 9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e --revision R7D --review-threshold 9.9 --viewer-url ../ --gallery-url ../renders99/
node web-tools/planos99-publication-qa.mjs
python scripts/planos99_publication_scope.py
```

La primera orden requiere Blender, los paquetes Python y Arial instalados. Antes de publicar una nueva emisión, revisar visualmente las hojas y generar el ensayo de acceso D08 de la fuente elegida; no reutilizar sus informes si cambia el SHA. El ensayo actual está en review99/service_access_r7d.json; las copias públicas documentan sus límites. La prueba del navegador usa Chrome instalado, un servidor HTTP local temporal y no requiere GPU.

## Validación local

publication_validation.json del destino confirma bytes, SHA, dimensiones de página, referencias y CRC ZIP. browser_validation.json verifica escritorio 1440 × 1000 y móvil 390 × 844: 33 vistas cargadas, 76 enlaces HTTP locales correctos, sin desbordamiento ni errores de JavaScript. Se revisaron capturas de cabecera y pie de página. Esto prepara la publicación; no acredita despliegue remoto ni aprobación arquitectónica.
