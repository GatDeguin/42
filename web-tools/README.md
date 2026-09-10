# Visor web de Casa de Campo

Sitio público: https://gatdeguin.github.io/42/

El directorio docs es el sitio estático completo: HTML, CSS, Three.js, modelo GLB y texturas locales. GitHub Pages publica main:/docs después de cada push. No requiere servidor de aplicación, claves ni CDN.

## Uso

- Arrastrar para orbitar; rueda o pellizco para acercar; botón derecho o dos dedos para desplazar.
- Botones de plantas y diez ambientes para cambiar de cámara.
- Ocultar cubiertas/vegetación y regular el corte horizontal.
- Seleccionar piezas para consultar su nombre y dimensiones envolventes.
- Abrir las doce puertas juntas o seleccionar una y moverla por separado.
- Inicio recupera el encuadre exterior, adaptado a la orientación de pantalla.

Las vistas de planta son perspectivas seccionadas. Las dimensiones seleccionadas son envolventes del objeto visible, no cotas de un plano ejecutivo.

## Desarrollo local

Desde la raíz del repositorio, con Node.js y Python instalados:

    npm ci --prefix web-tools
    python -m http.server 8420 --bind 127.0.0.1 --directory docs

Abrir http://127.0.0.1:8420/. No abrir index.html mediante file://, ya que el navegador necesita servir módulos y GLB por HTTP.

## Regenerar los recursos del modelo

Con Git LFS y Blender 5.2:

    git lfs pull
    node web-tools/sync-assets.mjs
    blender -b output/Casa_de_Campo_Final.blend --python scripts/export_web_model.py
    node web-tools/optimize.mjs
    blender -b output/Casa_de_Campo_Final.blend --python scripts/bake_web_wood.py

El exportador trabaja en memoria y no guarda cambios en el archivo Blender. Mantiene geometría arquitectónica y metadatos de las doce puertas; reduce solo paisaje. El optimizador aplica Meshopt y cuantización. La preparación de maderas hornea color del material original y conserva un mapa de direcciones por objeto. No genera vídeo.

El GLB vigente ocupa 10.021.880 bytes. El visor combina mallas estáticas por material/categoría para reducir llamadas de dibujo y mantiene las piezas originales para selección. Las geometrías comprimidas se expanden antes de transformar sus vértices.

## Verificación

Con Chrome instalado y el servidor local activo:

    node web-tools/qa.mjs
    node web-tools/interactions.mjs
    node web-tools/revision-checks.mjs

VIEWER_URL permite ejecutar las pruebas contra otra URL, incluida la pública. Los informes y capturas se guardan en review/. Se comprueban carga, vistas, errores, destinos de puertas, selección real, órbita, estados de corte, maderas y orientación de pantalla. Las auditorías independientes están en audit/critica_visor_web_*.md.

## Publicar actualizaciones

Modificar docs, verificar, incorporar los cambios a main y subirlos a origin. GitHub Pages vuelve a desplegar automáticamente. Los cambios de geometría requieren repetir exportación y optimización; los de materiales procedurales requieren hornear las texturas.

La animación de puertas es interacción en tiempo real. El renderizado de vídeo permanece pausado hasta aprobación explícita del propietario.
