import bpy,os,json,time,hashlib
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;OUT=os.path.join(ROOT,'review95','r6f_visual');os.makedirs(OUT,exist_ok=True)
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
for d in pref.devices:d.use=d.type=='OPTIX'
S.render.engine='CYCLES';S.cycles.device='GPU';S.cycles.samples=128;S.cycles.use_denoising=True;S.cycles.denoiser='OPENIMAGEDENOISE';S.cycles.denoising_use_gpu=True;S.cycles.adaptive_threshold=.014;S.render.use_persistent_data=True;S.render.resolution_x=1600;S.render.resolution_y=1200;S.render.resolution_percentage=100
shots=[('REV | Mono cocina e isla','mono_cocina'),('REV | Mono distribución','mono_distribucion'),('REV | Baño mono','bano_mono'),('REV | Baño quincho','bano_quincho'),('REV | Cocina comedor','cocina'),('REV | Vestidor circulación','vestidor'),('REV | Dormitorio completo','dormitorio'),('REV | Baño acceso comedor','puerta_bano'),('REV | Quincho y extracción','quincho')]
r={'model':bpy.data.filepath,'sha256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),'shots':[],'video_rendered':False}
for name,key in shots:
 S.camera=bpy.data.objects[name];S.frame_set(S.camera.get('presentation_frame',150));S.view_settings.exposure=.35+S.camera.get('photographic_exposure_compensation_ev',0)
 S.render.filepath=os.path.join(OUT,key+'.png');t=time.time();bpy.ops.render.render(write_still=True)
 r['shots'].append({'camera':name,'file':key+'.png','frame':S.frame_current,'seconds':round(time.time()-t,1)})
 json.dump(r,open(os.path.join(OUT,'manifest.json'),'w'),indent=2,ensure_ascii=False);print('R6F_PROOF',key,round(time.time()-t,1),flush=True)
