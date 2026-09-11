# Coordinación de manos R7 — comprobación geométrica

Estado: apta para integrar en el candidato R7 y someter al crítico. Esta comprobación no asigna la nota fotográfica ni aprueba el proyecto completo.

## Fuente y artefactos

- Base intacta: `output/Casa_de_Campo_99_R7C_preview.blend`, SHA256 `f2db43178677a0981751e197bf5af7c59739b2b5f5987d44f625cf5ab2c1f842`.
- Copia de revisión: `output/Casa_de_Campo_99_R7C_hands_preview.blend`, SHA256 `c747143332f00b7888512caad1be7ee7accfd30cb1a57f2703f63bfb6e39f3b9`.
- Patch callable sin guardado ni render: `scripts/correcciones99_bedroom_link.py` → `apply()`.
- Construcción reproducible de copia: `scripts/preview99_door_hands.py`.
- Barrido independiente: `scripts/validate99_door_hands.py`.
- Cámaras: `scripts/check99_door_cameras.py`.
- Evidencia: `proposal_manifest.json`, `validation.json`, `cameras.json` en esta carpeta.

Aplicar una vez después de los parches de distribución/textiles/luz y C2/C3. Un segundo apply sobre el mismo candidato es un no-op. El archivo fuente R6K y la copia R7C no fueron sobrescritos.

## Problema corregido

La mano original de bedroomLink dejaba el extremo de la puerta abierta junto a la cama y obligaba a entrar por un paso residual. La nueva puerta bedroomDining abría hacia el comedor y se enfrentaba a sofá y silla. Una inversión directa de ambas manos tampoco era válida: las hojas se cruzaban durante los primeros grados de apertura. La versión aquí comprobada ajusta la posición del conjunto de galces dentro del espesor existente y aumenta7mm la jamba de cierre de bedroomDining.

Se conservan exactamente ambos vanos de obra, los muros, cama, ropa de cama, mobiliario, cotas de planta y alturas libres. Las coordenadas siguientes son del sistema fuente X/H/Z en metros.

| Elemento | bedroomLink | bedroomDining |
|---|---:|---:|
| Eje X | 17,5975 | 17,4975 |
| Eje Z | 7,2700 | 9,0100 |
| Eje H | 3,2500 | 3,2500 |
| Mano | Bisagra norte; abre hacia dormitorio | Bisagra derecha; abre hacia dormitorio |
| Ancho de hoja | 820mm | 908mm |
| Espesor de hoja | 45mm | 45mm |
| Altura de hoja | 2170mm | 2200mm |
| Holgura inferior | 10mm | 10mm |
| Vano de obra | Z7,23…8,13 | X16,54…17,54 |
| Driver de giro | opening × −π/2 | opening × −π/2 |

La jamba de cierre de bedroomDining pasa de35 a42mm; la de bisagra conserva35mm. El ancho entre jambas resulta923mm. Esta cota de marco no se presenta como ancho útil universal de paso: hojas y herrajes ocupan volumen durante la maniobra.

bedroomLink incorpora tres bisagras con nudillos de12mm, pasadores de5mm, perforación de5,6mm y separación axial2mm; palancas en ambas caras con rosetas, eje y taladro pasante; galces13mm y juntas2mm. Son herrajes genéricos de coordinación dimensional, no una selección de producto con prestaciones certificadas. Los objetos de herraje nuevos llevan prefijo HAND99.

## Verificaciones completadas

- 65 objetos existentes dentro de las dos familias autorizadas y52 piezas nuevas; **0 cambios de otros objetos,0 objetos existentes perdidos**.
- **13 rigs** conservados, mismas acciones/keyframes; solo bedroomLink cambia el signo del driver.
- Reflectado de geometría horneado en vértices, normales recalculadas, determinantes de objetos positivos. **0 volúmenes locales con orientación negativa**.
- Segunda aplicación: snapshot completo idéntico.
- **41 posiciones por puerta**, contra103 objetos estáticos próximos, evaluando las piezas activas y sus modificadores; **886 intersecciones Boolean Exact** resueltas; **0 solapamientos de volumen >10⁻⁸m³**.
- Separación de los barridos combinados: extremos analíticos de cada vértice para todo ángulo entre0° y90°. Intervalos fuenteZ de piezas móviles:
  - bedroomLink:7,228999…8,091049m.
  - bedroomDining:8,102002…9,096999m.
  - **Separación continua mínima10,953mm**. La separación por un plano común demuestra que las dos familias móviles no se cruzan en las1681 combinaciones de la cuadrícula41×41, ni entre esas muestras.
- Aproximación local comedor→dormitorio→vestidor con ambas puertas abiertas90°: cilindro vertical de450mm de diámetro y1720mm de alto, pies15mm sobre NPT, **73 posiciones espaciadas≤40mm,0 impactos**.
- Ruta fuenteXZ comprobada: (16,90;9,40) → (16,97;9,00) → (17,08;8,45) → (17,10;7,72) → (17,70;7,68) → (18,12;7,68).

La prueba de450mm comprueba esta envolvente de paso; no representa una verificación normativa de accesibilidad, transporte de muebles ni todas las dimensiones corporales. El recorrido completo y su timeline se validan en la integración raíz.

## Cámaras en su presentación

Comprobación adicional de165 rayos por cámara, sobre90% del ancho y alto de su encuadre, con el aspect propio. No se movió ninguna cámara.

| Cámara | Frame | Posición fuente X/H/Z | % de rayos cuyo primer impacto es una puerta móvil | Primer impacto central |
|---|---:|---|---:|---|
| REV · Dormitorio acceso | 1 | 14,57 /4,87 /8,60 | 7,88% | Cabecero a3,108m |
| REV · Dormitorio completo | 1 | 17,12 /4,86 /8,54 | 0% | Almohada a2,615m |
| LUZ99 · Dormitorio desde paso | 150 | 18,20 /4,78 /7,72 | 25,45% | Cortina a4,073m |

Ninguna cámara está dentro de una hoja ni tiene impacto a menos de35mm. Las distancias mínimas son1,687m,1,499m y0,698m, respectivamente. La complementaria desde el paso todavía dedica aproximadamente un cuarto de su encuadre periférico a una hoja; conviene revisar su composición antes de la galería final. La nota de hiperrealismo queda pendiente del crítico sobre el candidato único completo.

No se renderizó video ni se publicó esta copia.
