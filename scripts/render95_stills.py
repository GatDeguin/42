"""Final-size still evidence for frozen candidate. Never renders animation or saves the scene."""
import bpy,os,json,hashlib,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'review95','final_stills');os.makedirs(OUT,exist_ok=True);S=bpy.context.scene
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
for d in pref.devices:d.use=d.type=='OPTIX'
S.render.engine='CYCLES';S.cycles.device='GPU';S.cycles.use_denoising=True;S.cycles.denoiser='OPENIMAGEDENOISE';S.cycles.denoising_use_gpu=True;S.cycles.adaptive_threshold=.018;S.render.use_persistent_data=True;S.render.resolution_percentage=100
shots=[('CAM | Presentación verticales corregidas','exterior'),('CAM | Pileta & playa húmeda','pileta'),('CAM | Huerta','huerta'),('REV | Estudio y cubierta','estudio'),('REV | Cocina comedor','cocina'),('REV | Quincho y extracción','quincho'),('REV | Dormitorio completo','dormitorio'),('REV | Dormitorio acceso','dormitorio_acceso'),('REV | Vestidor circulación','vestidor'),('REV | Baño completo','bano'),('REV | Baño desde acceso','bano_acceso'),('CAM | Monoambiente','monoambiente'),('REV | Escalera y desembarco','escalera'),('REV | Cubierta escalonada','cubiertas')]
report={'source_model':os.path.basename(bpy.data.filepath),'source_sha256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),'video':'PAUSED_PENDING_EXPLICIT_APPROVAL','images':[]}
for name,key in shots:
 camera=bpy.data.objects[name];S.camera=camera;S.frame_set(camera.get('presentation_frame',1));S.cycles.samples=192 if key=='exterior' else 128;S.render.resolution_x=2400 if key=='exterior' else 1800;S.render.resolution_y=1800 if key=='exterior' else 1350
 S.render.filepath=os.path.join(OUT,key+'.png');t=time.time();bpy.ops.render.render(write_still=True)
 report['images'].append({'file':key+'.png','camera':name,'frame':S.frame_current,'pixels':[S.render.resolution_x,S.render.resolution_y],'samples':S.cycles.samples,'seconds':round(time.time()-t,2)})
 json.dump(report,open(os.path.join(OUT,'manifest.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2);print('STILL_READY',key,round(time.time()-t,1),flush=True)
print('ALL_14_STILLS_READY_NO_VIDEO',flush=True)
