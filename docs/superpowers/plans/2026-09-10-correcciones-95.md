# Correcciones para el criterio 9,5 — plan de ejecución

**Objetivo:** cerrar los hallazgos de la auditoría integral, mejorar la apariencia fotográfica del modelo y del visor y entregar los planos de toda la propiedad.
**Base:** audit/critica_integral_95_01.md y docs/ENTREGA_PLANOS.md.
**Estrategia:** candidatos nuevos de Blender, documentos regenerables y prototipo web aislado; integrar tras verificar geometría e interacción. No guardar sobre el modelo auditado anterior.
**Restricciones:** lote22×20, casa8×12, pileta7×3, 18peldaños/3,80m, altura estudio3,20 y vivienda2,60. Vídeo pausado. Inferencias constructivas identificadas.
**Datos del propietario:** Virrey del Pino, Buenos Aires; servicios de red disponibles; norte hacia abajo-izquierda si la calle ocupa el borde superior.

## Pasada 1 — construcción y planos
- [ ] scripts/correcciones95_construccion.py: canaletas abiertas con pendientes y salidas; tubos huecos continuos hasta cámaras accesibles, separadas de sanitarias. Recorridos fuera de muros y pasos coordinados en balcón.
- [ ] Terminar descanso y balcones a la cota de los umbrales, con pendientes y drenaje; ajustar peldaños/zancas/barandas conservando18 y3,80m. Pavimento de arranque+0,06; desembarco interior+3,25.
- [ ] Modelar remates de membranas/carpinterías, registros, fijaciones y esquemas visibles; documentar estructura e instalaciones como propuestas de coordinación sin inventar cálculos.
- [ ] scripts/verificar95_construccion.py: verificar sección abierta, continuidad hidráulica geométrica, alturas, escalera, huecos y barridos; escribir review95/construccion_checks.json.
- [ ] Guardar output/Casa_de_Campo_95_Pass1.blend y emitir geometría/metadatos para el generador de planos.
- [ ] Agente planos95: scripts/planos95_build.py produce PDF/SVG/DXF en planos95/pass1 desde el candidato, con cotas y niveles comprobables.

## Pasada 2 — materiales, piezas y paisaje
- [ ] scripts/correcciones95_materialidad.py: refinar muebles, textiles, consola y vegetación sin cambiar huellas fuente; mantener las piezas móviles y sus pivotes.
- [ ] Texturas a escala real, metal no metálico donde corresponde, vidrio y agua con transmisión física; mapa de origen de cada mejora.
- [ ] Comparar imágenes y cajas de arquitectura antes/después; guardar candidato nuevo.

## Pasada 3 — luz y presentación
- [ ] Agente visor_fotografico: prototipo docs/preview95, iluminación/materiales/PBR o path tracing progresivo con navegación híbrida, datos reales del modelo y pruebas de interacción.
- [ ] scripts/render95_stills.py: imágenes fijas exteriores e interiores Cycles, atardecer, cámaras y recortes de materiales; nunca vídeo.
- [ ] Integrar únicamente mejoras comprobadas; actualizar exportación GLB y planos para el mismo candidato.
- [ ] Crítico independiente: nueva auditoría completa con umbral9,5, sin compensar falta de fotografía con puntuación del software.
- [ ] Si rechaza, listar hallazgos y efectuar las siguientes tres pasadas antes de otra calificación. Publicar avances con su estado real, sin rotularlos aprobados.
