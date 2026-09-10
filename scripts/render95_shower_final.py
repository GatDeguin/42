import bpy,os,time
from mathutils import Vector
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));p=R+'/docs/preview95/brick/calibrate.py';exec(compile(open(p,encoding='utf8').read(),p,'exec'),{'__file__':p,'__name__':'__main__'})
q=R+'/scripts/correcciones95_rociador_final.py';exec(compile(open(q,encoding='utf8').read(),q,'exec'),{'__file__':q,'__name__':'__main__'})
S=bpy.context.scene;pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
for d in pref.devices:d.use=d.type=='OPTIX'
S.render.engine='CYCLES';S.cycles.device='GPU';S.cycles.samples=80;S.cycles.use_denoising=True;S.cycles.denoiser='OPENIMAGEDENOISE';S.cycles.denoising_use_gpu=True;S.render.use_persistent_data=True;S.render.resolution_x=1200;S.render.resolution_y=900;S.render.resolution_percentage=100
c=bpy.data.objects['REV | Baño mono'];S.camera=c;S.frame_set(150);S.view_settings.exposure=.35+c.get('photographic_exposure_compensation_ev',0)
def cv(v):return Vector((v[0],-v[2],v[1]))
for i,p,t,f in [(3,[20.50,1.82,5.65],[21.25,1.44,4.42],19)]:
 c.location=cv(p);c.rotation_euler=(cv(t)-c.location).to_track_quat('-Z','Y').to_euler();c.data.lens=f;S.render.filepath=R+'/review95/r6k_camera_proofs/shower_option'+str(i)+'.png';bpy.ops.render.render(write_still=True)
print('SHOWER_OPTIONS_DONE_NO_SAVE')
