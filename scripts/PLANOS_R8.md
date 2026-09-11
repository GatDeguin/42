# Planos R8: emisión y publicación reproducibles

Preparación del juego de 35 A2: se conservan las 33 hojas anteriores y se añaden D13 (MIDI, operador y apoyos) y D14 (isla, dos comensales y salida). Se mantienen G/F/P, escalas físicas, texto mínimo de2,50 mm y cotas CAD en metros. Este flujo no asigna una nota crítica ni declara aprobación9,9.

## Emisión local desde una fuente congelada

```powershell
& 'C:/Users/Gaston/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' scripts/planos99_emit_r8.py --model output/MODELO_FINAL.blend --expected-sha SHA256_COMPLETA --out planos95/r8_final_candidate
```

La SHA es obligatoria. Se comprueba antes de crear la salida y al terminar. La emisión ejecuta ensayos CPU de uso y acceso D08 sobre el mismo modelo, extrae su geometría sin guardarlo, genera los35 PDF/SVG/DXF y verifica226 cotas nativas. Un modelo cuyo nombre contiene preview exige `--preview`. No se permite emitir en docs. `--use-evidence` permite reutilizar pruebas sólo si su geometría y JSON contienen la misma SHA. `--reuse-geometry` conserva la comprobación de SHA.

La evidencia D08 se vuelve a ejecutar con `planos99_service_access_probe.py`; su texto procede de `planos99_service_access.md` y conserva límites de medio auxiliar/estabilidad/capacidad no seleccionados. No se cambia la fuente por el ensayo.

Tras revisar visualmente las35 hojas, registrar `visual_review.json` con `status: PASS_DOCUMENT_COMPOSITION`, `model_sha256` exacto y `overview_sheets` completo, además de `REVISION_VISUAL.md`. Este registro es revisión documental, sin aprobación arquitectónica. Rehacer el paquete para incluir esos registros:

```powershell
& 'C:/Users/Gaston/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' scripts/planos95_package.py --out planos95/r8_final_candidate --details planos95/r8_final_candidate/details
```

## Publicación del manifiesto validado

```powershell
& 'C:/Users/Gaston/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' scripts/planos95_publish.py --source planos95/r8_final_candidate --dest docs/planos99 --expected-sha SHA256_COMPLETA --revision R8 --viewer-url ../ --gallery-url ../renders99/
```

El comando admite33 o35 hojas según el manifiesto y la metadata. Antes de escribir verifica los bytes de todos los archivos del paquete fuente y del ZIP, SHA del modelo, PDF vectorial A2, mínimo tipográfico, dimensiones físicas SVG y cada cota DXF contra el CSV. También exige evidencia visual/D08 y de uso R8 de la misma fuente, incluida en el manifiesto. Resuelve el `<base>` del visor y verifica `assets/web-package.json`; la galería también debe tener la misma SHA. No enlaza una galería todavía inexistente.

Produce PDF,35SVG,35DXF,35miniaturas PNG a1000px derivadas del mismo PDF, índice, manifiestos, registros y ZIP. Se compara cada byte del ZIP publicado y cada SHA del manifiesto. El registro `publication_validation.json` queda junto a ellos, fuera del ZIP para evitar autorreferencia de hash. Los nombres públicos siguen siendo `Casa_de_Campo_Planos_A2.pdf` y `Casa_de_Campo_Planos_Editables.zip`.

La preparación se probó exclusivamente fuera de docs. Una prueba aislada usa `--preview --dest planos95/r8_publication_preview`; permite evidencia visual pendiente, la expone en manifiesto y no enlaza visor/galería. Ese modo no puede escribir en docs.

## Comprobación del índice

```powershell
& 'C:/Program Files/nodejs/node.exe' web-tools/planos99-publisher-qa.mjs --publication planos95/r8_publication_preview --out review99/r8_publisher/browser
```

Chrome sin GPU: escritorio1440 y móvil390, número de tarjetas según manifiesto, carga de todas las miniaturas, enlaces HTTP, ausencia de desborde y de errores JavaScript. Esta comprobación no equivale a aprobación crítica.

Las pruebas de preparación pasan para35hojas/226cotas y para33hojas/209cotas. La copia de ensayo no es la entrega final R8. La entrega final exige volver a ejecutar la emisión sobre la SHA integrada definitiva.

## Avance R8 sin visor publicado

La publicación autorizada de avance se prepara en su carpeta separada, conservando R7D:

```powershell
& 'C:/Users/Gaston/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' scripts/planos95_publish.py --source planos95/r8_final --dest docs/avance-r8/planos --expected-sha SHA256_COMPLETA --revision R8 --no-viewer --back-url ../
```

`--no-viewer` deja el visor en preparación y no crea un enlace ficticio. `--back-url` exige que la página de regreso exista. El estado sigue en revisión, sin aprobación9,9. Emisión: Blender CPU secuencial con `-t4`; OMP/MKL/OpenBLAS limitados a4.
