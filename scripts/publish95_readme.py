"""Write publication documentation only after model, photographs and plan evidence exist."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];m=R/'output/Casa_de_Campo_95_R6K.blend';sha=hashlib.sha256(m.read_bytes()).hexdigest()
g=json.loads((R/'docs/renders/manifest.json').read_text(encoding='utf8'));assert g['source_sha256']==sha and len(g['images'])==19
assert (R/'docs/planos/Casa_de_Campo_Planos_A2.pdf').exists()
readme=f"""# Casa de campo · modelo y documentación arquitectónica

**[Explorar el modelo 3D](https://gatdeguin.github.io/42/)** · **[Ver las 19 imágenes](https://gatdeguin.github.io/42/renders/)** · **[Abrir los planos](https://gatdeguin.github.io/42/planos/)**

Reconstrucción editable del proyecto, basada en el HTML/JavaScript original y las correcciones del propietario. Ubicación indicada: **Virrey del Pino, La Matanza, Buenos Aires**.

**Candidato R6K en revisión. La aprobación integral de 9,5/10 y el realismo fotográfico exigidos siguen pendientes del agente crítico independiente.** La última auditoría integral publicada calificó la entrega inicial con6,9/10; las notas parciales posteriores no equivalen a aprobar esta versión. [Auditorías y evidencia](audit/).

**El video permanece pausado hasta autorización explícita.** El archivo conserva las cámaras y el recorrido editable, sin secuencia de video renderizada.

## Entrega del candidato

- [Blender completo R6K — descarga directa](https://media.githubusercontent.com/media/GatDeguin/42/main/output/Casa_de_Campo_95_R6K.blend), con materiales empaquetados, objetos y colecciones editables.
- [19 imágenes Cycles, ambiente por ambiente](https://gatdeguin.github.io/42/renders/), calculadas desde esta misma escena; exterior2400×1800 e interiores1800×1350.
- [Planos A2 en PDF](docs/planos/Casa_de_Campo_Planos_A2.pdf) y [paquete PDF +SVG +DXF](docs/planos/Casa_de_Campo_Planos_Editables.zip): plantas de toda la propiedad, cortes, fachadas, cubiertas y detalles.
- [Criterios, medidas e inferencias](docs/DECISIONES.md).
- [Uso y reproducción del visor](web-tools/README.md).

SHA256 del modelo: `{sha}`.

![Casa y paisaje](docs/renders/exterior.jpg)

## Correcciones incorporadas

Estudio con3,20m libres y vivienda con2,60m; cubierta del estudio0,60m más alta. Barra del quincho paralela a la parrilla y comedor acercado al jardín. Cama orientada con la ventana a la derecha de quien está acostado. Nuevo acceso corredizo entre el baño y el comedor de planta alta, y mesada de cocina reordenada.

Se coordinan alturas de mobiliario, pasos, asientos y apoyos: mesa750mm, barra900mm y taburetes650mm. Los pasos se miden hasta la geometría real —incluidos tiradores— y los planos distinguen cotas del modelo de propuestas pendientes de definición.

Las13 puertas y correderas conservan mecanismos independientes. La revisión incluye barridos con41 estados, encuentros de carpinterías, soportes de18 peldaños, rodillas bajo consola, desagües representados y capas de baños. Cada prueba conserva su alcance; no demuestra por sí sola la totalidad del funcionamiento constructivo.

## Fuente y alcance

Lote22×20m; edificio8×12m; pileta7×3m de envolvente nominal; huerta, jardín, quincho, estudio, vivienda, baños, balcones y escalera exterior. Sin escalera interior. La hoja del portón mide3m y la luz entre pilares de fuente es2,75m.

El norte indicado por el propietario apunta abajo a la izquierda cuando Cedro Misionero queda arriba; es orientativo. Se informó disponibilidad de todos los servicios; las acometidas y el relevamiento del lote siguen pendientes.

[HTML original](source/original.html) · [Encargo](source/request.txt). Conversión métrica: HTML(X,Y,Z) → Blender(X,−Z,Y). Las instrucciones posteriores del propietario prevalecen sobre las contradicciones de la fuente. El archivo original [Casa_de_Campo_Final.blend](output/Casa_de_Campo_Final.blend) se conserva como registro y **no es el candidato R6K**.

Los detalles no definidos en la fuente se identifican como propuestas. La documentación permite revisar arquitectura y geometría; no constituye documentación ejecutiva habilitada ni cálculo estructural, hidráulico, acústico o reglamentario.

## Materiales y reproducción

Blender5.2/Cycles y visorThree.js con recursos locales. Modelos Blender mediante GitLFS: después de clonar, ejecutar `git lfs pull`.

Recursos CC0 de PolyHaven: [Belfast Sunset](https://polyhaven.com/a/belfast_sunset), [Tree Small02](https://polyhaven.com/a/tree_small_02), [Oak Veneer01](https://polyhaven.com/a/oak_veneer_01) y [Red Bricks04](https://polyhaven.com/a/red_bricks_04). Se conservan atribución, escala física y trazabilidad de los archivos; el albedo del ladrillo tiene una calibración documentada.

El visor usa geometría del modelo y materiales PBR. La navegación raster y el trazado progresivo opcional tienen límites distintos de los renders Cycles; sus verificaciones y fuentes se documentan [aquí](docs/preview95/README.md).
"""
readme=readme.replace('## Fuente y alcance','Pendiente geométrico documentado en A08: el volumen de agua se prolonga unos 114 mm dentro del fondo del vaso. La corrección queda para la siguiente revisión; no se presenta R6K como aprobado.\n\n## Fuente y alcance').replace('[Planos A2 en PDF]','[33 láminas A2 en PDF]')
(R/'README.md').write_text(readme,encoding='utf8')
dec="""# Fuente, decisiones y alcance técnico

| Tema | Base conservada o decisión |
|---|---|
| Fuente | HTML/JavaScript original y correcciones posteriores del propietario. |
| Coordenadas | HTML(X,Y,Z)→Blender(X,−Z,Y), metros, factor de unidad1. |
| Ubicación | Virrey del Pino, La Matanza, Buenos Aires, informada por el propietario. |
| Norte | Abajo a la izquierda con Cedro Misionero arriba: vector fuente(-X,+Z). Orientativo, sin levantamiento topográfico. |
| Servicios | Todos disponibles según propietario. Puntos y niveles de conexión no relevados. |
| Implantación | Lote22×20; casa8×12 enX14/Z0, dos módulos de6m; pileta7×3 nominal exterior del vaso. |
| Planta alta | Losa estructural+3,00..+3,20; piso terminado general y baño+3,25. |
| Altura estudio | 3,20m libres; cielorraso y límite inferior de tratamiento acústico+6,45. |
| Altura vivienda | 2,60m libres; cielorraso general y baño+5,85. |
| Cubiertas | Estudio más alto:0,60m de desnivel, derivado de las alturas interiores autorizadas. Pendientes y huella de fuente conservadas. |
| Escalera | Exterior,18 peldaños, ancho nominal1m, recorrido3,80m, descanso1×1. Contrahuellas177,22mm desde arranque+0,06 hasta acabado+3,25. Huella de avance211,11mm. Sin escalera interior. |
| Quincho | Barra paralela a parrilla; mesa/sillas hacia jardín, apoyadas en piso acabado. |
| Dormitorio | Cabecera al muroZ6,10; ventana a la derecha de quien está acostado, dirección−X. Se conserva vestidor y se desactiva armario duplicado del dormitorio. |
| Baño/comedor | Nuevo vano y corredera con luz900mm, altura libre2220mm; baño enrasado y retorno de mesada reordenado. |
| Mobiliario | Medidas desde pisos acabados; apoyos, espacio de rodillas y equipos coordinados. El objetivo de paso de0,80m en comedor es proyectual, no una afirmación normativa. |
| Carpintería | Vanos y doble vidrio conservados. Galces, juntas, perfiles, asientos y herrajes propuestos;13 mecanismos independientes. |
| Portón | Hoja3m, luz entre pilares2,75m, carrera3,05m. |
| Baños | Capas y pendientes modeladas. Bañera1,25×0,74 clasificada compacta/asiento; producto aún por seleccionar. |
| Pileta | Cota máxima modelada del agua−0,030; coronamiento del vaso+0,070, resguardo100mm. Operación/filtrado requieren proyecto específico. |
| Construcción añadida | Apoyos, correas, cielorrasos, aislamiento, fijaciones, juntas y remates son desarrollo de la reconstrucción. |
| Instalaciones | Trazados y reservas propuestos, no dimensionamiento definitivo ni redes de servicio verificadas en sitio. |
| Vegetación | Seis posiciones de árboles del lote conservadas; entorno adicional de ambientación. |
| Video | Pausado hasta autorización explícita. Cámaras/poses y recorrido editado incluidos. |

Las cotas de planos se distinguen según su base: fuente, geometría evaluada o propuesta. No se deben convertir medidas de envolventes ni visualizaciones en tolerancias de fabricación sin el detalle correspondiente.

La documentación permite revisar geometría, circulación, materiales y encuentros. Capacidad de suelo/fundaciones, estructura, estanqueidad, desempeño térmico/acústico, redes y cumplimiento normativo requieren datos de sitio y verificación profesional antes de construir.
"""
(R/'docs/DECISIONES.md').write_text(dec,encoding='utf8')
print('PUBLICATION_DOCUMENTATION_READY',sha)
