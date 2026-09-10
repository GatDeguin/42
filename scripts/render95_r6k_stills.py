"""Generate still photographs from one SHA-identified frozen candidate. No animation and no scene save."""
import bpy,os,json,hashlib,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'review95','r6k_stills');os.makedirs(OUT,exist_ok=True);S=bpy.context.scene
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
for d in pref.devices:d.use=d.type=='OPTIX'
S.render.engine='CYCLES';S.cycles.device='GPU';S.cycles.use_denoising=True;S.cycles.denoiser='OPENIMAGEDENOISE';S.cycles.denoising_use_gpu=True;S.cycles.adaptive_threshold=.012;S.render.use_persistent_data=True;S.render.resolution_percentage=100
shots=[
('CAM | Presentación verticales corregidas','exterior','Casa y paisaje'),
('CAM | Pileta & playa húmeda','pileta','Pileta y playa húmeda'),
('CAM | Huerta','huerta','Huerta y jardín'),
('REV | Estudio y cubierta','estudio','Estudio de grabación'),
('REV | Cocina comedor','cocina','Cocina de la vivienda'),
('REV | Quincho y extracción','quincho','Quincho y línea de fuego'),
('REV | Dormitorio completo','dormitorio','Dormitorio'),
('REV | Dormitorio acceso','dormitorio_acceso','Acceso al dormitorio'),
('REV | Vestidor circulación','vestidor','Vestidor'),
('REV | Baño completo','bano','Baño de la vivienda'),
('REV | Baño desde acceso','bano_acceso','Baño desde el acceso'),
('REV | Baño acceso comedor','puerta_bano','Comunicación entre baño y comedor'),
('REV | Mono cocina e isla','mono_cocina','Cocina e isla del monoambiente'),
('REV | Mono distribución','mono_distribucion','Distribución del monoambiente'),
('REV | Baño mono','bano_mono','Ducha del monoambiente'),
('REV | Baño mono sanitarios','bano_mono_sanitarios','Sanitarios del monoambiente'),
('REV | Baño quincho','bano_quincho','Baño del quincho'),
('REV | Escalera y desembarco','escalera','Escalera y desembarco'),
('REV | Cubierta escalonada','cubiertas','Cubiertas a distinta altura')]
report={'source_model':os.path.basename(bpy.data.filepath),'source_sha256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),'status':'CANDIDATO EN REVISIÓN · aprobación global9.5 pendiente','video':'PAUSED_PENDING_EXPLICIT_APPROVAL','images':[]}
assert all(name in bpy.data.objects for name,key,title in shots)
for name,key,title in shots:
 camera=bpy.data.objects[name];S.camera=camera;S.frame_set(camera.get('presentation_frame',1));S.cycles.samples=192;S.render.resolution_x=2400 if key=='exterior' else 1800;S.render.resolution_y=1800 if key=='exterior' else 1350
 S.view_settings.exposure=.35+camera.get('photographic_exposure_compensation_ev',0)
 S.render.filepath=os.path.join(OUT,key+'.png');t=time.time();bpy.ops.render.render(write_still=True)
 report['images'].append({'file':key+'.png','title':title,'camera':name,'frame':S.frame_current,'pixels':[S.render.resolution_x,S.render.resolution_y],'samples':S.cycles.samples,'seconds':round(time.time()-t,2)})
 json.dump(report,open(os.path.join(OUT,'manifest.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2);print('STILL_READY',key,round(time.time()-t,1),flush=True)
print('ALL_STILLS_READY_NO_VIDEO',flush=True)
