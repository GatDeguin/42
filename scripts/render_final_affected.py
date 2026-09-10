import bpy,os,json,shutil
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'review');S=bpy.context.scene
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
for d in pref.devices:d.use=d.type=='OPTIX'
S.render.engine='CYCLES';S.cycles.device='GPU';S.cycles.use_denoising=True;S.render.use_persistent_data=True;S.render.resolution_percentage=100;S.cycles.adaptive_threshold=.025
S.frame_set(1);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];S.render.resolution_x=2400;S.render.resolution_y=1800;S.cycles.samples=192;S.cycles.denoiser='OPENIMAGEDENOISE';S.render.filepath=os.path.join(ROOT,'output','Casa_de_Campo_Atardecer_Revision.png');bpy.ops.render.render(write_still=True);shutil.copy2(S.render.filepath,os.path.join(OUT,'iter2_exterior.png'))
S.render.resolution_x=1600;S.render.resolution_y=1066;S.cycles.samples=128
for name,label in [('REV | Baño desde acceso','bano_acceso'),('REV | Baño completo','bano'),('REV | Dormitorio completo','dormitorio'),('REV | Dormitorio acceso','dormitorio_acceso'),('REV | Vestidor circulación','vestidor')]:
 S.camera=bpy.data.objects[name];S.frame_set(S.camera['presentation_frame']);S.render.filepath=os.path.join(OUT,'iter2_'+label+'.png');bpy.ops.render.render(write_still=True)
route=json.load(open(os.path.join(ROOT,'output','tour_route.json'),encoding='utf8'))['shots'];S.camera=bpy.data.objects['TOUR | Recorrido virtual'];S.render.resolution_x=960;S.render.resolution_y=540;S.cycles.samples=48;S.cycles.denoiser='OPTIX';S.cycles.adaptive_threshold=.06
for i in [3,9,10]:
 for u,suffix in [(.15,'_antes'),(.5,''),(.85,'_despues')]:
  shot=route[i];S.frame_set(round(shot['start']+(shot['end']-shot['start'])*u));S.render.filepath=os.path.join(OUT,'iter2_recorrido_%02d%s.png'%(i+1,suffix));bpy.ops.render.render(write_still=True)
print('FINAL_VISUAL_EVIDENCE_READY_NO_VIDEO',flush=True)
