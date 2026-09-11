"""Integrate independently checked R7 patches and prepare one editable candidate. No render."""
import bpy,runpy,json,os,hashlib,time,sys,numpy as np
ROOT=r'D:\2026\42';OUT=os.path.join(ROOT,'review99','r7d_integrated');os.makedirs(OUT,exist_ok=True)
BASE=os.path.join(ROOT,'output','Casa_de_Campo_99_R7C_preview.blend')
EXPECTED='f2db43178677a0981751e197bf5af7c59739b2b5f5987d44f625cf5ab2c1f842'
DEST=os.path.join(ROOT,'output','Casa_de_Campo_99_R7D.blend')
assert '--checked-patches' in sys.argv,'Use only after constructor checks are complete'
assert os.path.normcase(bpy.data.filepath)==os.path.normcase(BASE)
assert hashlib.sha256(open(BASE,'rb').read()).hexdigest()==EXPECTED
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
def snapshot():
 cache={};rows={}
 for o in S.objects:
  row=dict(type=o.type,matrix=[round(v,7) for r in o.matrix_world for v in r],parent=o.parent.name if o.parent else None,hidden=o.hide_render,collections=sorted(c.name for c in o.users_collection))
  if o.type=='MESH':
   m=o.data
   if m.as_pointer() not in cache:
    v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);f=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',f)
    cache[m.as_pointer()]=hashlib.sha256(v.tobytes()+f.tobytes()).hexdigest()
   row['mesh']=cache[m.as_pointer()];row['materials']=[m.name if m else None for m in o.data.materials]
  rows[o.name]=row
 return rows
before=snapshot()
files=['correcciones99_humedos_r7.py','correcciones99_ventilacion_r7.py','correcciones99_bedroom_link.py','correcciones99_camara_acceso.py','correcciones99_sanitarios_pavimento.py','finish99_metadata.py']
modules={f:runpy.run_path(os.path.join(ROOT,'scripts',f)) for f in files}
reports={f:modules[f]['apply']() for f in files}
bpy.context.view_layer.update();first=snapshot()
for f in files:modules[f]['apply']()
bpy.context.view_layer.update();second=snapshot()
assert first==second,'Integration patches are not idempotent'
tour=runpy.run_path(os.path.join(ROOT,'scripts','correcciones99_recorrido.py'));route=tour['apply']()
scene_sync=runpy.run_path(os.path.join(ROOT,'scripts','sync99_scene_variants.py'))['apply']()
route_check=tour['verify'](route,os.path.join(OUT,'tour_in_memory.json'))
if not route_check['passed']:raise RuntimeError('Camera route failed; no final candidate saved')
S['tour_route_requires_revalidation_after_layout']=False
S['revision99_integrated']='R7: construction/layout, physical textiles/botany, light/web coordination'
S['review99_status']='Independent global 9.9 approval pending'
S['video_render_requires_explicit_approval']=True
S.view_settings.view_transform='AgX';S.view_settings.look='AgX - Medium High Contrast';S.view_settings.exposure=.35
S.frame_set(1);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas']
S.render.resolution_x=2400;S.render.resolution_y=1800
tx=bpy.data.texts.get('00 LEEME | R7 vigente') or bpy.data.texts.new('00 LEEME | R7 vigente');tx.clear()
tx.write('R7 — modelo integrado en revisión. Umbral global solicitado: 9,9; no aprobado todavía.\n'
 'Fuente vigente: Casa_de_Campo_99_R7D.blend. Todas las escenas comparten los objetos de la planta actual.\n'
 'Coordenadas: fuente (X, altura, profundidad) a Blender (X, -profundidad, altura). Metros.\n'
 'Nivel estructural de referencia PA +3,00; piso terminado general +3,25. Alturas libres: vivienda 2,60 y estudio 3,20.\n'
 'Accesos PA: estar-dormitorio-vestidor-baño-estar. El vestidor no comunica directamente con el estar.\n'
 'Baño PB: fachada Cedro Misionero y medianera derecha.\n'
 'Puertas: frame 1 cerrado; frame 150 abierto. Recorrido preparado: TOUR | Recorrido virtual.\n'
 'VIDEO PAUSADO hasta aprobación explícita del propietario; ningún video R7 ha sido renderizado.\n'
 'G: geometría medida; F: dato del propietario/fuente; P: propuesta dimensional sin cálculo resistente/de instalaciones.\n'
 'Ubicación: Virrey del Pino, La Matanza, Buenos Aires. Norte orientativo -X/+Z según propietario. Acometidas por relevar.\n')
after=snapshot()
bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=DEST,compress=True)
sha=hashlib.sha256(open(DEST,'rb').read()).hexdigest()
report=dict(source=BASE,sourceSHA256=EXPECTED,output=DEST,outputSHA256=sha,videoRendered=False,idempotentPatches=True,
 added=sorted(set(after)-set(before)),removed=sorted(set(before)-set(after)),changed=[n for n in set(before)&set(after) if before[n]!=after[n]],
 patchReports=reports,sceneSynchronization=scene_sync,route=route,routeInMemoryPassed=True,
 scripts={f:hashlib.sha256(open(os.path.join(ROOT,'scripts',f),'rb').read()).hexdigest() for f in files+['correcciones99_recorrido.py','sync99_scene_variants.py']})
json.dump(report,open(os.path.join(OUT,'integration_manifest.json'),'w',encoding='utf8'),indent=2,ensure_ascii=False)
print('R7D_INTEGRATED',sha,len(S.objects),flush=True)
