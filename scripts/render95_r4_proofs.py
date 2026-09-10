import bpy,os,json,time
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;OUT=os.path.join(ROOT,'review95','r4_visual');os.makedirs(OUT,exist_ok=True)
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
for d in pref.devices:d.use=d.type=='OPTIX'
S.render.engine='CYCLES';S.cycles.device='GPU';S.cycles.samples=64;S.cycles.use_denoising=True;S.cycles.denoiser='OPENIMAGEDENOISE';S.cycles.denoising_use_gpu=True;S.cycles.adaptive_threshold=.025;S.render.use_persistent_data=True;S.render.resolution_x=1280;S.render.resolution_y=960;S.render.resolution_percentage=100
def cv(p):return Vector((p[0],-p[2],p[1]))
cd=bpy.data.cameras.new('Revisión puerta baño comedor');co=bpy.data.objects.new(cd.name,cd);S.collection.objects.link(co);co.location=cv([19.92,4.92,10.0]);co.rotation_euler=(cv([20.10,4.30,7.50])-co.location).to_track_quat('-Z','Y').to_euler();cd.lens=25
for name,key,frame in [('REV | Dormitorio completo','dormitorio',150),('REV | Quincho y extracción','quincho',150),('REV | Cocina comedor','cocina',150),('Revisión puerta baño comedor','puerta_bano',150),('REV | Estudio y cubierta','estudio',150),('Revisión puerta baño comedor','puerta_cerrada',1)]:
 S.camera=bpy.data.objects[name];S.frame_set(frame);S.render.filepath=os.path.join(OUT,key+'.png');t=time.time();bpy.ops.render.render(write_still=True);print('R4_PROOF',key,round(time.time()-t,1),flush=True)
print('R4_PROOFS_DONE_NO_VIDEO')
