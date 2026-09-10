import bpy,os,json,hashlib,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=ROOT+'/docs/preview95/brick/calibrate.py';exec(compile(open(p,encoding='utf8').read(),p,'exec'),{'__file__':p,'__name__':'__main__'})
S=bpy.context.scene;OUT=ROOT+'/review95/r6k_camera_proofs';os.makedirs(OUT,exist_ok=True)
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
for d in pref.devices:d.use=d.type=='OPTIX'
S.render.engine='CYCLES';S.cycles.device='GPU';S.cycles.samples=80;S.cycles.use_denoising=True;S.cycles.denoiser='OPENIMAGEDENOISE';S.cycles.denoising_use_gpu=True;S.cycles.adaptive_threshold=.02;S.render.use_persistent_data=True;S.render.resolution_x=1200;S.render.resolution_y=900;S.render.resolution_percentage=100
r={'source':bpy.data.filepath,'source_sha256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),'calibrated_brick_applied_in_memory':True,'video':False,'shots':[]}
for name,key in [('REV | Dormitorio completo','dormitorio'),('REV | Vestidor circulación','vestidor'),('REV | Baño mono','bano_mono'),('REV | Baño mono sanitarios','bano_mono_sanitarios')]:
 S.camera=bpy.data.objects[name];S.frame_set(S.camera.get('presentation_frame',1));S.view_settings.exposure=.35+S.camera.get('photographic_exposure_compensation_ev',0);S.render.filepath=OUT+'/'+key+'.png';t=time.time();bpy.ops.render.render(write_still=True);r['shots'].append({'name':name,'key':key,'seconds':time.time()-t});json.dump(r,open(OUT+'/manifest.json','w'),indent=2);print('CAMERA_PROOF',key,flush=True)
