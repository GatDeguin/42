"""Freeze R6K from the coordinated geometry and reviewed bounded patches; no video."""
import bpy,runpy,os,json,hashlib
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for relative in ['scripts/correcciones95_apoyos_dvh.py','scripts/correcciones95_rociador_final.py','docs/preview95/clothes/apply.py','docs/preview95/brick/calibrate.py']:
 print('INTEGRATING',relative,flush=True);runpy.run_path(os.path.join(R,relative),run_name='__main__')
S=bpy.context.scene;S.frame_set(1);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas']
S['review_iteration']='95 / R6K coordinated publication candidate';S['architect_review_approval']='PENDING_GLOBAL_9_5';S['video_render_requires_explicit_approval']=True
S['site_location_owner']='Virrey del Pino, La Matanza, Buenos Aires'
S['north_source_xz_owner']='(-X,+Z), orientative, Cedro Misionero above'
S['services_owner']='All services available; connection points not surveyed'
note=bpy.data.texts.get('LEEME | Revisión R6 vigente')
if note:
 note.clear();note.write("""CASA DE CAMPO · CANDIDATO R6K EN REVISIÓN
Fuente: HTML/JavaScript y correcciones posteriores del propietario.
Unidades métricas. Estudio 3,20 m y vivienda/baño 2,60 m libres. Piso PA +3,25.
13 puertas animadas, incluida conexión baño-comedor; cámaras fuente y REV.
Barra paralela a parrilla, mesa del quincho al jardín, ventana a la derecha de quien se acuesta, mesada reordenada.
Mobiliario y apoyos coordinados; reservas y juntas de DVH; rociador plano; prendas a escala adulta.
Recorrido editado 1968 fotogramas/24 fps preparado. Video PAUSADO hasta autorización explícita.
La escena alternativa continua anterior es histórica y no se ha revalidado.
Aprobación integral 9,5 y realismo fotográfico pendientes de auditoría independiente.
Detalles y productos propuestos no constituyen cálculo, selección comercial ni certificación para construir.
""")
bpy.context.view_layer.update();bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
out=os.path.join(R,'output','Casa_de_Campo_95_R6K.blend');bpy.ops.wm.save_as_mainfile(filepath=out,compress=True)
sha=hashlib.sha256(open(out,'rb').read()).hexdigest()
report={'model':out,'sha256':sha,'bytes':os.path.getsize(out),'status':'EN REVISION / GLOBAL9.5 PENDIENTE','doors':len([o for o in S.objects if o.name.startswith('DOOR |')]),'video_rendered':False,'source_geometry':'Casa_de_Campo_95_R6K_geometry.blend','patches':['DVH bearing reserves','flat shower head','adult garments','calibrated brick PBR']}
json.dump(report,open(os.path.join(R,'review95','r6k_release.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2);print('R6K_FROZEN',sha,flush=True)
