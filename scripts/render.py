import bpy,sys,os,json,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'output')
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
S=bpy.context.scene
S.render.engine='CYCLES';S.cycles.device='GPU'
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='OPTIX';p.get_devices()
for d in p.devices:d.use=d.type=='OPTIX'
S.render.use_persistent_data=True;S.cycles.use_denoising=True;S.render.image_settings.file_format='PNG';S.render.image_settings.color_mode='RGB';S.render.image_settings.color_depth='8'
mode=args[0] if args else 'hero'
if mode=='hero':
 S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];S.frame_set(1)
 S.render.resolution_x=2400;S.render.resolution_y=1800;S.cycles.samples=192;S.cycles.adaptive_threshold=.025
 S.render.filepath=os.path.join(OUT,'Casa_de_Campo_Atardecer.png');bpy.ops.render.render(write_still=True)
elif mode=='test':
 S.render.resolution_x=960;S.render.resolution_y=540;S.cycles.samples=24;S.cycles.adaptive_threshold=.06
 for camera,label in [('CAM | Estudio de grabación','Estudio'),('CAM | Cocina','Cocina'),('CAM | Vestidor pasante','Vestidor'),('CAM | Quincho','Quincho'),('CAM | Dormitorio','Dormitorio'),('CAM | Baño suite','Bano')]:
  S.frame_set(150);S.camera=bpy.data.objects[camera];S.render.filepath=os.path.join(OUT,'control_'+label+'.png');bpy.ops.render.render(write_still=True)
elif mode in ('tour','bench'):
 S.camera=bpy.data.objects['TOUR | Recorrido virtual']
 S.render.resolution_x=1280;S.render.resolution_y=720;S.cycles.samples=24;S.cycles.adaptive_threshold=.065
 S.cycles.denoiser='OPTIX';S.cycles.denoising_use_gpu=True;S.cycles.max_bounces=10;S.cycles.diffuse_bounces=3;S.cycles.glossy_bounces=3;S.cycles.transmission_bounces=10;S.cycles.sample_clamp_indirect=3
 frames=os.path.join(OUT,'tour_frames');os.makedirs(frames,exist_ok=True)
 if mode=='bench':
  for fr in [70,260,760,1120]:
   start=time.time();S.frame_set(fr);S.render.filepath=os.path.join(OUT,'bench_%04d.png'%fr);bpy.ops.render.render(write_still=True);print('BENCH',fr,round(time.time()-start,2),flush=True)
 else:
  a=int(args[1]) if len(args)>1 else 1;b=int(args[2]) if len(args)>2 else S.frame_end
  for fr in range(a,b+1):
   fp=os.path.join(frames,'%05d.png'%fr)
   if os.path.exists(fp):continue
   S.frame_set(fr);S.render.filepath=fp;bpy.ops.render.render(write_still=True)
   if fr%24==0:print('PROGRESS',fr,b,flush=True)
