"""Render source-identified R7 architectural stills. Does not render animation or save the source."""
import bpy,os,json,hashlib,time,sys,ast
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
def arg(k,default=None):return args[args.index(k)+1] if k in args else default
OUT=os.path.abspath(arg('--out',os.path.join(ROOT,'review99','r7_final','stills')));os.makedirs(OUT,exist_ok=True)
source=bpy.data.filepath;sha=hashlib.sha256(open(source,'rb').read()).hexdigest()
expected=arg('--expected-sha');assert expected and sha==expected,'Explicit frozen source SHA required'
S=bpy.context.scene
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
for d in pref.devices:d.use=d.type=='OPTIX'
S.render.engine='CYCLES';S.cycles.device='GPU';S.cycles.samples=int(arg('--samples','256'));S.cycles.use_denoising=True;S.cycles.denoiser='OPENIMAGEDENOISE';S.cycles.denoising_use_gpu=True;S.cycles.use_adaptive_sampling=True;S.cycles.adaptive_threshold=.009;S.render.use_persistent_data=True
S.render.resolution_percentage=100;S.render.image_settings.file_format='PNG';S.render.image_settings.color_depth='8'
S.view_settings.view_transform='AgX';S.view_settings.look='AgX - Medium High Contrast';S.view_settings.exposure=.35
tree=ast.parse(open(os.path.join(ROOT,'scripts','render95_r6k_stills.py'),encoding='utf-8-sig').read())
shots=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='shots' for t in n.targets))
shots=[('LUZ99 | Estudio amplitud' if key=='estudio' else name,key,title) for name,key,title in shots]
shots+= [
 ('LUZ99 | Estudio retrato','estudio_retrato','Estudio, composición vertical'),
 ('LUZ99 | Dormitorio retrato','dormitorio_retrato','Dormitorio, composición vertical'),
 ('LUZ99 | Vestidor retrato','vestidor_retrato','Vestidor, composición vertical'),
 ('LUZ99 | Exterior jardin retrato','exterior_retrato','Jardín, composición vertical'),
 ('LUZ99 | Bano suite humano','bano_humano','Bañera de la vivienda, detalle a altura de uso'),
 ('LUZ99 | Acceso dormitorio desde estar','dormitorio_puerta','Puerta directa del dormitorio al estar')]
only=set(arg('--only','').split(',')) if arg('--only') else None
if only:shots=[s for s in shots if s[1] in only]
manifest=os.path.join(OUT,'manifest.json')
report=dict(source=source,sourceSHA256=sha,revision='R7',status='CANDIDATO EN REVISIÓN; umbral global 9,9 pendiente',video='PAUSED_PENDING_EXPLICIT_APPROVAL',engine='Cycles OptiX',transform='AgX Medium High Contrast',exposureEV=.35,images=[])
if os.path.exists(manifest):
 prior=json.load(open(manifest,encoding='utf8'))
 assert prior['sourceSHA256']==sha,'Output directory contains a different revision'
 if '--resume' in args:report['images']=prior['images']
paused=False
for name,key,title in shots:
 if os.path.isfile(os.path.join(OUT,'pause_after_current.flag')):
  paused=True;print('R7_STILLS_PAUSED_BY_REQUEST',len(report['images']),flush=True);break
 camera=bpy.data.objects.get(name);assert camera and camera.type=='CAMERA',name
 path=os.path.join(OUT,key+'.png')
 if '--resume' in args and any(r['key']==key and os.path.isfile(path) and r['sha256']==hashlib.sha256(open(path,'rb').read()).hexdigest() for r in report['images']):continue
 S.camera=camera;S.frame_set(camera.get('presentation_frame',1));bpy.context.view_layer.update()
 portrait=key.endswith('_retrato');S.render.resolution_x=1800 if portrait else (2400 if key=='exterior' else 2000);S.render.resolution_y=2400 if portrait else (1800 if key=='exterior' else 1500)
 S.render.filepath=path;t=time.perf_counter();bpy.ops.render.render(write_still=True)
 row=dict(key=key,file=key+'.png',title=title,camera=name,frame=S.frame_current,pixels=[S.render.resolution_x,S.render.resolution_y],samples=S.cycles.samples,adaptiveThreshold=S.cycles.adaptive_threshold,exposureEV=.35,positionBlender=list(camera.matrix_world.translation),quaternionBlender=list(camera.matrix_world.to_quaternion()),lensMM=camera.data.lens,sensorMM=[camera.data.sensor_width,camera.data.sensor_height],shift=[camera.data.shift_x,camera.data.shift_y],seconds=round(time.perf_counter()-t,2),sha256=hashlib.sha256(open(path,'rb').read()).hexdigest())
 report['images']=[r for r in report['images'] if r['key']!=key]+[row]
 json.dump(report,open(manifest,'w',encoding='utf8'),ensure_ascii=False,indent=2);print('R7_STILL_READY',key,row['seconds'],flush=True)
assert hashlib.sha256(open(source,'rb').read()).hexdigest()==sha
print('R7_STILLS_PAUSED_NO_VIDEO' if paused else 'R7_STILLS_DONE_NO_VIDEO',len(report['images']),flush=True)
