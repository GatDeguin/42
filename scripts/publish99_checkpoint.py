"""Create the reviewed R7 progress checkpoint; no still or video render."""
import bpy, runpy, json, hashlib, os
ROOT=r'D:\2026\42'
BASE=os.path.join(ROOT,'output','Casa_de_Campo_99_R7C_hands_preview.blend')
EXPECTED='c747143332f00b7888512caad1be7ee7accfd30cb1a57f2703f63bfb6e39f3b9'
DEST=os.path.join(ROOT,'output','Casa_de_Campo_99_R7_avance.blend')
OUT=os.path.join(ROOT,'review99','github_progress');os.makedirs(OUT,exist_ok=True)
assert os.path.normcase(bpy.data.filepath)==os.path.normcase(BASE)
assert hashlib.sha256(open(BASE,'rb').read()).hexdigest()==EXPECTED
S=bpy.context.scene;S.frame_set(1)
files=['correcciones99_camara_acceso.py','finish99_metadata.py']
reports={f:runpy.run_path(os.path.join(ROOT,'scripts',f))['apply']() for f in files}
tour=runpy.run_path(os.path.join(ROOT,'scripts','correcciones99_recorrido.py'));route=tour['apply']()
reports['sceneSynchronization']=runpy.run_path(os.path.join(ROOT,'scripts','sync99_scene_variants.py'))['apply']()
qa=tour['verify'](route,os.path.join(OUT,'tour_in_memory.json'))
assert qa['passed'],'Do not publish failed camera route'
S['tour_route_requires_revalidation_after_layout']=False
S['revision99_integrated']='R7 progress: layout, water, textiles, botany, light and door handedness'
S['review99_status']='Work in progress. Global independent target 9.9; R7 not scored.'
S['video_render_requires_explicit_approval']=True
S.view_settings.view_transform='AgX';S.view_settings.look='AgX - Medium High Contrast';S.view_settings.exposure=.35
S.frame_set(1);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas']
S.render.resolution_x=2400;S.render.resolution_y=1800;S.render.resolution_percentage=100
text=bpy.data.texts.get('00 LEEME | R7 vigente') or bpy.data.texts.new('00 LEEME | R7 vigente');text.clear()
text.write('R7 AVANCE — checkpoint editable en revisión, NO aprobado. Umbral global solicitado: 9,9/10.\n'
'Vestidor sólo conecta dormitorio y baño; dormitorio tiene puerta propia al estar. Baño PA conserva conexión al comedor.\n'
'Baño PB junto a fachada Cedro Misionero y medianera derecha.\n'
'Metros. Conversión fuente (X,altura,profundidad) → Blender (X,-profundidad,altura). Piso PA +3,25. Alturas libres vivienda2,60 y estudio3,20.\n'
'Todas las escenas comparten geometría actual. Frame1: puertas cerradas; frame150: abiertas.\n'
'Recorrido preparado: TOUR | Recorrido virtual. VIDEO PAUSADO hasta autorización explícita.\n'
'Pendiente: C2 revestimientos húmedos, C3 ventilación/mantenimiento, refinamiento sanitario/pavimentos, nueva exportación web, planos y renders del mismo SHA, auditoría integral.\n'
'Las imágenes, visor y planos R6K publicados no describen este checkpoint. No es documentación ejecutiva habilitada.\n')
assert all(set(sc.objects)==set(S.objects) for sc in bpy.data.scenes)
assert len([o for o in S.objects if o.name.startswith('DOOR |')])==13
assert all(im.packed_file or im.packed_files for im in bpy.data.images if im.source=='FILE')
bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=DEST,compress=True)
report=dict(revision='R7 avance',status='IN_REVIEW_NOT_APPROVED',targetGlobalScore=9.9,score=None,base=BASE,baseSHA256=EXPECTED,output=DEST,outputSHA256=hashlib.sha256(open(DEST,'rb').read()).hexdigest(),bytes=os.path.getsize(DEST),objects=len(S.objects),scenes=[dict(name=sc.name,objects=len(sc.objects)) for sc in bpy.data.scenes],videoRendered=False,routePassed=True,patchReports=reports,scripts={f:hashlib.sha256(open(os.path.join(ROOT,'scripts',f),'rb').read()).hexdigest() for f in files+['correcciones99_recorrido.py','sync99_scene_variants.py','publish99_checkpoint.py']})
json.dump(report,open(os.path.join(OUT,'manifest.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
print('CHECKPOINT_SAVED',report['outputSHA256'],report['bytes'],flush=True)