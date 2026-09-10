import bpy,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'review');S=bpy.context.scene
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
for d in pref.devices:d.use=d.type=='OPTIX'
S.render.engine='CYCLES';S.cycles.device='GPU';S.render.use_persistent_data=True;S.cycles.use_denoising=True;S.cycles.denoiser='OPENIMAGEDENOISE';S.cycles.denoising_use_gpu=True;S.cycles.samples=192;S.cycles.adaptive_threshold=.025
S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];S.frame_set(1);S.render.resolution_x=2400;S.render.resolution_y=1800;S.render.resolution_percentage=100;S.render.filepath=os.path.join(ROOT,'output','Casa_de_Campo_Atardecer_Revision.png');bpy.ops.render.render(write_still=True)
# The principal review image is identical to the final-size proof.
import shutil
shutil.copy2(S.render.filepath,os.path.join(OUT,'iter2_exterior.png'))
S.cycles.samples=128;S.render.resolution_x=1600;S.render.resolution_y=1066
for name,label in [('REV | Dormitorio completo','dormitorio'),('REV | Dormitorio acceso','dormitorio_acceso'),('REV | Baño completo','bano'),('REV | Baño desde acceso','bano_acceso'),('REV | Cocina comedor','cocina'),('REV | Quincho y extracción','quincho'),('REV | Estudio y cubierta','estudio'),('REV | Vestidor circulación','vestidor'),('REV | Cubierta escalonada','cubierta'),('REV | Portón y riel','porton'),('REV | Escalera y desembarco','escalera')]:
 cam=bpy.data.objects[name];S.camera=cam;S.frame_set(cam['presentation_frame']);S.render.filepath=os.path.join(OUT,'iter2_'+label+'.png');bpy.ops.render.render(write_still=True)
# Independent still checks at shot midpoints; this does not render the video.
route=json.load(open(os.path.join(ROOT,'output','tour_route.json'),encoding='utf8'))['shots'];S.camera=bpy.data.objects['TOUR | Recorrido virtual'];S.render.resolution_x=960;S.render.resolution_y=540;S.cycles.samples=48;S.cycles.denoiser='OPTIX';S.cycles.adaptive_threshold=.06
for i,shot in enumerate(route):
 S.frame_set((shot['start']+shot['end'])//2);S.render.filepath=os.path.join(OUT,'iter2_recorrido_%02d.png'%(i+1));bpy.ops.render.render(write_still=True)
print('REVIEW_ITERATION2_COMPLETE_NO_VIDEO_RENDERED',flush=True)

for i in [3,5,6,9,10]:
 shot=route[i]
 for u,label in [(.15,'antes'),(.85,'despues')]:
  S.frame_set(round(shot['start']+(shot['end']-shot['start'])*u));S.render.filepath=os.path.join(OUT,'iter2_recorrido_%02d_%s.png'%(i+1,label));bpy.ops.render.render(write_still=True)
print('ITER2_ALL_STILL_EVIDENCE_READY',flush=True)
