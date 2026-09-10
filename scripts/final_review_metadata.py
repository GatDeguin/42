import bpy,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene
notes=json.loads(S['corrections'])
notes=[t.replace('3.00m clear opening','3.00m leaf (source pillar clear gap2.75m)').replace('maintaining3m opening','maintaining3m leaf (source clear gap2.75m)') for t in notes]
S['corrections']=json.dumps(notes,ensure_ascii=False)
S['source_gate_leaf_width_m']=3.0;S['source_gate_pillar_clear_width_m']=2.75;S['video_render_requires_explicit_approval']=True
text=bpy.data.texts.get('LEEME | Proyecto y decisiones') or bpy.data.texts.new('LEEME | Proyecto y decisiones')
text.clear();text.write('''CASA DE CAMPO · revisión arquitectónica
Fuente: source/original.html. Se importaron1233objetos de la escenaHTML, sus materiales y16cámaras.
Ejes HTML(X,Y,Z)→Blender(X,-Z,Y); todas las unidades en metros.
Alturas autorizadas: estudio3.20m libres sobre piso+3.25, vivienda2.60m sobre+3.25, baño2.60m sobre+3.30.
Cubierta del estudio0.60m más alta que la vivienda; salto y remates modelados.
Lote22×20; edificio8×12; pileta7×3; escalera18peldaños; descanso1×1.
Portón: hoja3.00m, luz entre pilares de fuente2.75m. No confundir ambas medidas.
Colecciones: componentes normales editables. Texturas y referencia empaquetadas.
Puertas: DOOR | nombre, propiedad open0..1; frames1/30cerradas,105abiertas. Controla hojas, herrajes y guías.
Cámaras CAM | conservan la fuente; REV | vistas de inspección; TOUR | Recorrido virtual es la cámara de montaje corregida.
RECORRIDO | Continuo conserva la alternativa de recorrido continuo anterior como material de trabajo.
Materiales y detalles constructivos añadidos se identifican por nombres y propiedadcorrections; no son cálculos estructurales.
VIDEO: PAUSADO POR EL PROPIETARIO. Requiere aprobación explícita antes de renderizar o codificar.
Pruebas: output/validation.json,review/coordinated_mesh_checks.json; auditorías independientes en audit/.
Modelo vigente: Casa_de_Campo_Revision.blend.
''')
S.frame_set(1);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_Revision.blend'),compress=True)
# Re-render only stills affected by restored acoustic dry joints.
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
for d in pref.devices:d.use=d.type=='OPTIX'
S.render.engine='CYCLES';S.cycles.device='GPU';S.cycles.use_denoising=True;S.render.use_persistent_data=True
S.camera=bpy.data.objects['REV | Estudio y cubierta'];S.frame_set(150);S.render.resolution_x=1600;S.render.resolution_y=1066;S.cycles.samples=128;S.cycles.denoiser='OPENIMAGEDENOISE';S.render.filepath=os.path.join(ROOT,'review','iter2_estudio.png');bpy.ops.render.render(write_still=True)
route=json.load(open(os.path.join(ROOT,'output','tour_route.json'),encoding='utf8'))['shots'][6];S.camera=bpy.data.objects['TOUR | Recorrido virtual'];S.render.resolution_x=960;S.render.resolution_y=540;S.cycles.samples=48;S.cycles.denoiser='OPTIX'
for u,suffix in [(.15,'_antes'),(.5,''),(.85,'_despues')]:
 S.frame_set(round(route['start']+(route['end']-route['start'])*u));S.render.filepath=os.path.join(ROOT,'review','iter2_recorrido_07'+suffix+'.png');bpy.ops.render.render(write_still=True)
print('FINAL_ACOUSTIC_STILLS_REPLACED_NO_VIDEO',flush=True)
