import bpy,os,json,time,hashlib
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;OUT=os.path.join(ROOT,'review95','r5_visual');os.makedirs(OUT,exist_ok=True)
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
for d in pref.devices:d.use=d.type=='OPTIX'
S.render.engine='CYCLES';S.cycles.device='GPU';S.cycles.samples=96;S.cycles.use_denoising=True;S.cycles.denoiser='OPENIMAGEDENOISE';S.cycles.denoising_use_gpu=True;S.cycles.adaptive_threshold=.018;S.render.use_persistent_data=True;S.render.resolution_x=1440;S.render.resolution_y=1080;S.render.resolution_percentage=100
shots=[('REV | Dormitorio completo','dormitorio',150),('REV | Dormitorio acceso','dormitorio_acceso',150),('REV | Quincho y extracción','quincho',150),('REV | Cocina comedor','cocina',150),('REV | Baño acceso comedor','puerta_bano',150),('REV | Estudio y cubierta','estudio',150),('REV | Baño acceso comedor','puerta_cerrada',1)]
for name,key,frame in shots:
 S.camera=bpy.data.objects[name];S.frame_set(frame);S.render.filepath=os.path.join(OUT,key+'.png');t=time.time();bpy.ops.render.render(write_still=True);print('R5_PROOF',key,round(time.time()-t,1),flush=True)
json.dump({'model':bpy.data.filepath,'sha256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),'shots':shots,'video_rendered':False},open(os.path.join(OUT,'manifest.json'),'w'),indent=2)
print('R5_PROOFS_DONE_NO_VIDEO')
