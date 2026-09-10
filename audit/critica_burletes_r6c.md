# Revisión acotada R6C: burletes heredados posteriores

**Dictamen: incompatibles con la carpintería R5B3; retirar ocho piezas heredadas de la configuración activa.** No es compresión de un sello. Esta revisión no emite nueva nota integral ni reaudita las bisagras.

Fuente reabierta: `output/Casa_de_Campo_95_R6C.blend`, SHA256 `65246b84757806a5d298a42362663fe1387b9870a8a13a9cf546e0f1558aab0b`.

Los ocho objetos `Corrediza posterior A/B Burlete superior/inferior/izquierdo/derecho` son barras macizas estáticas, sin parent de hoja, con material **Metal negro**. Su sección es 26 × 35 mm. Los horizontales cubren 2,55 m en A y 3,35 m en B; los laterales, 2,54 m de altura.

En A ocupan Z 11,9675–12,0025; en B, 11,9645–11,9995. Es exactamente la envolvente transversal de los dos cristales móviles de 9 mm y su cámara de 17 mm. Por tanto, estas barras llenan todo el espesor del vidrio en sus franjas de 26 mm. Los horizontales permanecen atravesados durante las 41 posiciones. Los laterales interceptan las hojas al inicio o final del recorrido. También colisionan con los retornos metálicos nuevos. No puede describirse como una pequeña deformación normal de EPDM.

Los cristales fijos están en otra pista, separada 20 mm de estas barras: conservar las barras no aporta su junta de acristalamiento. Ya están representadas en la familia SL95 las juntas móviles y fijas de 2 mm, los espaciadores/selladores del DVH, las felpas de pista y encuentro, y el burlete de cierre de jamba. Se deben conservar estas piezas nuevas.

La prueba independiente reprodujo los 62 pares únicos / 892 incidencias de los seis objetos señalados por el constructor. Al incluir también ambos **Burlete superior**, encontró 82 pares / 1708 incidencias. El aumento identifica dos piezas omitidas del alcance inicial; no es una regresión entre archivos.

**Corrección exacta:** retirar de escena activa los cuatro nombres indicados de A y los cuatro de B, manteniendo vidrios, perfiles, rigs y toda la familia SL95. No basta con cambiar el material o excluir «burletes» del test. Cierre: reabrir el consolidado, confirmar ausencia de estos ocho sólidos activos y repetir el barrido completo con las juntas restantes clasificadas por función. La geometría propuesta de las juntas no acredita estanqueidad ni prestaciones de una carpintería comercial.

Evidencia reproducible: `audit/integral95_02_r6c_legacy_seals.py`, JSON y log homónimos. Coordenadas en el JSON: X / Y altura / Z profundidad de la fuente.
