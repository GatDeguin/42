# Respuesta del constructor al visor web 01

La primera revisión recibió 7/10. Se ejecutaron tres pasadas antes de volver a presentarla al crítico.

1. **Estados y cotas.** El rótulo deriva del corte activo y su cota, y elimina la cota al desactivarlo. Una apertura individual deja el control general en «Personalizadas» cuando las hojas tienen estados distintos.
2. **Cámaras y legibilidad.** El vestidor usa una cámara dentro de la circulación y puertas cerradas. El exterior y las perspectivas generales adaptan su distancia al aspecto disponible y al cambio de orientación. Los rótulos tienen fondo de contraste estable.
3. **Materiales.** Se hornearon roble, nogal y parquet desde el material real del archivo Blender final. Se asignan a 193 piezas con UV según la dirección de veta original. El parquet conserva tablas de 1,40 × 0,18 m. El total de sus tres mapas añade aproximadamente 599 KB. La geometría GLB no cambió.

Verificación: review/web_qa.json, review/web_revision_checks.json y review/web_interaction_test.json. Sin errores JavaScript; prueba real de selección/apertura del portón y órbita; destinos de doce puertas con error posicional inferior a 0,000009 m; cotas sincronizadas; 193 piezas con mapa y UV; móvil sin desbordamiento, con ajuste de orientación.

El archivo Blender final conserva SHA256 58223D78F71DC0C1D4F33034AAAF0BE96A1BD420F72F2231468003E942C2BBFE. No se renderizó vídeo.
