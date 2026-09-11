"""Build the final R8 candidate from checked pass1 and visual components. No render."""
import bpy,runpy,json,hashlib,time,sys
from pathlib import Path
R=Path(r'D:/2026/42');OUT=R/'review99/r8_integrated';OUT.mkdir(exist_ok=True,parents=True)
assert '--checked-components' in sys.argv,'Require completed component evidence before final integration'
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();source=Path(bpy.data.filepath);sha=hashlib.sha256(source.read_bytes()).hexdigest();assert sha=='a4fd1fe3d964d9366fbc4ee7eeb1a7a268d1e3621aa599edc8630a6399c7fcd1'
files=['correcciones99_uv_madera_r8.py','correcciones99_textiles_botanica_r8.py','correcciones99_tapizados_r8.py','correcciones99_cesped_r8.py','correcciones99_camara_pileta_r8.py']
if '--water-checked' in sys.argv:
 assert (R/'review99/r8_visual/pool_water_render.json').exists();files.append('correcciones99_agua_optica_r8.py')
files+=['finish99_metadata_r8.py'];modules={};reports={}
snap=runpy.run_path(str(R/'scripts/correcciones99_textiles_botanica_r8.py'))['fingerprints'];before=snap(S.objects)
for name in files:
 modules[name]=runpy.run_path(str(R/'scripts'/name));reports[name]=modules[name]['apply']();bpy.context.view_layer.update();print('R8_APPLY',name,flush=True)
first=snap(S.objects)
for name in files:modules[name]['apply']();bpy.context.view_layer.update()
second=snap(S.objects);assert first==second,'Visual component application is not idempotent'
tour=runpy.run_path(str(R/'scripts/correcciones99_recorrido.py'));route=tour['apply']();sync=runpy.run_path(str(R/'scripts/sync99_scene_variants.py'))['apply']();proof=tour['verify'](route,str(OUT/'tour_in_memory.json'));assert proof['passed'],'Prepared camera route fails in integrated R8'
S['tour_route_requires_revalidation_after_layout']=False;S['revision99_integrated']='R8: repaired sanitary mechanics, MIDI/island use, textile/optical/grass refinement and source-matched photographic derivatives';S['review99_status']='R8 final digital candidate; independent9.9 approval pending. Last formal review: R7D8.5.'
for sc in bpy.data.scenes:sc['video_render_requires_explicit_approval']=True;sc['revision99_authoritative_geometry']='R8 shared scene membership'
for t in bpy.data.texts:
 if t.name.startswith('00 LEEME | R7 vigente'):t.name='ARCHIVO | LEEME R7D'
t=bpy.data.texts.get('00 LEEME | R8 vigente') or bpy.data.texts.new('00 LEEME | R8 vigente');t.clear();t.write('R8 — candidato digital en revisión. Aprobación integral9,9 pendiente.\nFuente vigente: Casa_de_Campo_99_R8.blend. Vídeo pausado hasta autorización explícita.\nMetros. Fuente(X,altura,profundidad) → Blender(X,-profundidad,altura).\nLote22×20m; volumen8×12m. NPT PA+3,25m; libre vivienda2,60m y estudio3,20m.\nAccesos: estar-dormitorio-vestidor-baño-estar; no hay vestidor-estar.\nBaño PB junto a fachada Cedro y medianera derecha.13puertas animables: frame1 cerrado,150 abierto.\nCámaras originales conservadas,26imágenes de presentación previstas. TOUR | Recorrido virtual preparado y comprobado, sin vídeo.\nSAN8 incluye holguras/topes/retención propuesta; MIDI a750mm con apoyos, isla con400mm de rodillas.\nG=geometría medida; F=fuente/propietario; P=propuesta sin cálculo resistente/de instalaciones.\nVirrey del Pino, La Matanza, Buenos Aires. Norte orientativo−X/+Z y servicios disponibles según propietario; mensura y acometidas por relevar.\nEl estudio digital no constituye cálculo ni aprobación profesional de obra.\n')
S.view_settings.view_transform='AgX';S.view_settings.look='AgX - Medium High Contrast';S.view_settings.exposure=.35;S.frame_set(1);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];S.render.resolution_x=2400;S.render.resolution_y=1800
bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();dest=R/'output/Casa_de_Campo_99_R8.blend';bpy.ops.wm.save_as_mainfile(filepath=str(dest),compress=True);outsha=hashlib.sha256(dest.read_bytes()).hexdigest();assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
report={'source':str(source),'sourceSHA256':sha,'originalR7DSHA256':'9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e','output':str(dest),'outputSHA256':outsha,'objects':len(S.objects),'idempotent':True,'patches':reports,'scripts':{f:hashlib.sha256((R/'scripts'/f).read_bytes()).hexdigest() for f in files},'sceneSynchronization':sync,'tourVerified':True,'videoRendered':False,'changes':{'added':sorted(first.keys()-before.keys()),'removed':sorted(before.keys()-first.keys()),'changed':sorted(n for n in first.keys()&before.keys() if first[n]!=before[n])}}
(OUT/'integration_manifest.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),'utf8');print('R8_FROZEN',outsha,len(S.objects),flush=True)
