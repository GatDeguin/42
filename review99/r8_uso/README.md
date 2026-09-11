# R8 uso — primera pasada para integrar

Estado: candidato local comprobado. Sin nota formal, sin aprobación 9,9 y sin publicar.

Fuente inmutable: `Casa_de_Campo_99_R7D.blend`, SHA256 `9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e`.
Preview: `Casa_de_Campo_99_R8_uso_preview.blend`, SHA256 `ac0922a881eeea24ad0a7dfd13bf20e710a9b0069039f06711f5755c2dd78d4d`.

## Aplicación

Importar `scripts/correcciones99_uso_r8.py` y llamar `apply()` en la copia integrada que deriva de R7D. El módulo no guarda ni renderiza. Su marcador `r8_uso_details` hace idempotente la aplicación. El builder independiente es `scripts/planos99_uso_r8_preview.py`; el ensayo CPU es `scripts/planos99_uso_r8_check.py`.

Se modifican 126 piezas autorizadas y se añaden 35; permanecen 6237 objetos externos y 13 rigs. Se verificó la segunda aplicación sin diferencias. No se modificaron el archivo R7D, SAN99, C2, D08 ni las puertas.

## Resultado geométrico

- MIDI: cuerpo genérico 1080×400×55 mm, teclas blancas 750/negras 762,5 mm sobre NPT; silla 470 mm. Bandeja 18, cuatro apoyos 3, brazos huecos 40×30×2, placa 4 y calce 8 mm. Filetes propuestos 3 mm unen placas a base metálica existente. Dos reservas inferiores y un recorte frontal local preservan la consola. Altura libre 665 mm en 12 rayos.
- Isla: tapa 1720×680×35 y altura 900 mm conservadas; fondo retranqueado 150 mm para 400 mm de rodillas. Almacenamiento interior 222 mm. Pórticos con postes 25×25×2 y vigas 25×20×2 mm, elastómero 3 mm bajo tapa. Dos bandas de 610 mm; asientos 650 mm, centros X16,350/17,290. Patas de 35 mm separadas para 305 mm libres, dentro del asiento 380 mm.
- Operador MIDI: brazo 283/antebrazo 249/mano 150 mm; codo 280 mm sobre asiento. Pelvis 15 mm por delante del centro del asiento y zapatos 280×100 mm sobre alfombra a +9 mm del NPT. El cuerpo de ensayo no se añade al Blender entregable.

## Evidencia

`use_validation.json`: 15 grupos PASS, 941 pares Boolean Exact, cero intersecciones no previstas; 54 contactos constructivos y 11 contactos de cuerpo/apoyo, 12 rayos de altura libre, 35 mallas nuevas cerradas. Incluye dos comensales sentados, sensibilidad de rodillas 600 mm, paso posterior Ø450×1718 mm, retirada 450 mm en 21 poses por taburete y entrada/salida en 18 posiciones desde el paso posterior. Los cuatro contactos entre cordones y acero se declaran intencionales. `scope_validation.json` y `dimension_validation.json` enlazan el mismo SHA.

`planos95/r8_uso_candidate/R8_Cortes_de_Uso_A3.pdf`:dos A3 vectoriales, cortes 1:10 y planta 1:20, SVG y PNG. `validation.json` comprueba formato físico, barra de escala, fuente mínima 2,5 mm y texto dentro de página. Se inspeccionaron ambas imágenes.

## Límites

Son geometrías de ensayo declaradas, no percentiles ni accesibilidad certificada. La retirada y las trayectorias se verifican por posiciones; no se simulan equilibrio, esfuerzo, carga ni todos los gestos de sentarse. El paso posterior corresponde a asientos en uso; durante la retirada se emplea el acceso central. Las referencias de NKBA y OSHA son criterios de diseño, no normativa argentina. La resistencia, estabilidad, soldadura, vibración y selección de productos requieren dimensionamiento específico.

La escena de prueba contiene todas las mallas evaluadas cuyo volumen envolvente intersecta cualquiera de las dos regiones completas de uso: 5368 mallas activas se reducen a 1052 candidatas. La exclusión es espacial y se registra en el JSON. Boolean Exact usa un umbral de volumen 1e-8 m³ y prefiltro de 0,01 mm. Contactos rígidos: 20 micras; cuerpos blandos de ensayo:0,1 mm. Las formas del cuerpo y la existencia de contacto no acreditan comodidad universal.
