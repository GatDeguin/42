import bpy,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;hero=bpy.data.objects['CAM | Presentación verticales corregidas']
# Quick visibility controls only, not a video sequence.
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='OPTIX';p.get_devices()
for d in p.devices:d.use=d.type=='OPTIX'
S.cycles.device='GPU';S.cycles.samples=32;S.cycles.denoiser='OPTIX';S.cycles.denoising_use_gpu=True;S.render.use_persistent_data=True;S.render.resolution_x=1000;S.render.resolution_y=680;S.render.resolution_percentage=100
for n,label in [('REV | Dormitorio completo','dormitorio'),('REV | Baño completo','bano'),('REV | Baño desde acceso','bano_acceso'),('REV | Cocina comedor','cocina'),('REV | Quincho y extracción','quincho')]:
 o=bpy.data.objects[n];S.camera=o;S.frame_set(o['presentation_frame']);S.render.filepath=os.path.join(ROOT,'review','pass2_'+label+'.png');bpy.ops.render.render(write_still=True)
S.frame_set(1);S.camera=hero;S.render.resolution_y=750;S.render.filepath=os.path.join(ROOT,'review','pass2_exterior.png');bpy.ops.render.render(write_still=True)
print('PASS2_VISIBILITY_RENDERED',flush=True)
