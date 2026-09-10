# Auditoría dimensional consolidada: ejecución sobre candidato congelado

El script integral95_02_consolidated_dimensions.py es de lectura. Reabre y mide la geometría evaluada; no guarda el .blend ni produce renders. Requiere el SHA256 exacto proporcionado para la entrega y vuelve a comprobarlo al terminar.

Ejemplo PowerShell, reemplazando únicamente archivo y SHA por la entrega congelada:

    & 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --factory-startup 'D:/2026/42/output/Casa_de_Campo_95_R6K.blend' --python 'D:/2026/42/audit/integral95_02_consolidated_dimensions.py' -- --expected-sha SHA256_DE_LA_ENTREGA --label r6k

Produce el inventario completo JSON/CSV cuyo nombre contiene el nombre del modelo; además:

- integral95_02_r6k_dimension_families.json: 54 familias, miembros explícitos, apoyos separados, alturas desde terminaciones medidas.
- integral95_02_r6k_dimensional_outliers.json: alertas de escala/dimensiones de todos los objetos medidos, sin equipararlas automáticamente a fallos.
- integral95_02_r6k_consolidated_dimensions.json: arquitectura, escalera, consola, nuevos asientos, piscina, duchas, comedor y envolventes descriptivas de 13 rigs.
- integral95_02_r6k_dimensional_summary.json: controles geométricos fallidos, consultas ausentes y trazabilidad.

Dependencias de auditoría existentes:
integral95_dimension_inventory.py; la constante rules de integral95_02_r6f_dimension_families.py; funciones de malla y contacto de integral95_02_r6h_bearing_knees.py. Las dependencias se leen, no se modifican.

El número de controles aprobados no genera una nota ni una aprobación. Las envolventes de los rigs no equivalen al claro útil de puerta, y esta ejecución no repite sus barridos. La aptitud de uso, los detalles restantes y el realismo fotográfico se juzgan sobre la entrega completa. No se certifica capacidad estructural, normativa, hidráulica, acústica ni productos comerciales no identificados.

Ejecutado sobre R6K SHA a3663a5081dac391303f25b8e9994b1a412a008e971642af29fc2cbee849aa90: 54 familias, 239 controles, un pendiente geométrico confirmado en el fondo del agua. Véanse critica_dimensional_r6k.md y las evidencias finales; no existe aprobación integral automática.
