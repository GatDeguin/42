import bpy,os,math,json,sys
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1)
world=bpy.data.worlds.new('95 | atardecer fotográfico Belfast CC0');world.use_nodes=True;n=world.node_tree.nodes;l=world.node_tree.links;n.clear()
out=n.new('ShaderNodeOutputWorld');bg=n.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.55
env=n.new('ShaderNodeTexEnvironment');env.image=bpy.data.images.load(os.path.join(ROOT,'source','belfast_sunset_2k.hdr'),check_existing=True)
tc=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeMapping');mapping.inputs['Rotation'].default_value[2]=math.radians(112);l.new(tc.outputs['Generated'],mapping.inputs['Vector']);l.new(mapping.outputs[0],env.inputs['Vector']);l.new(env.outputs[0],bg.inputs['Color']);l.new(bg.outputs[0],out.inputs[0]);S.world=world
# Photographic sky is the single environment light; avoid an unaligned second sun.
for o in S.objects:
 if o.type=='LIGHT' and o.data.type=='SUN':
  o.data.energy=.75;o.data.color=(1,.73,.48);o.data.angle=math.radians(1.5)
# Reduce visually dominant bedroom sconces while retaining their physical emitting surfaces.
for o in S.objects:
 if o.type=='LIGHT' and ('dormitorio' in o.name.lower() or 'cama' in o.name.lower()):o.data.energy*=.70
S.view_settings.view_transform='AgX';S.view_settings.look='AgX - Medium High Contrast';S.view_settings.exposure=.35
for cam in [o for o in S.objects if o.type=='CAMERA']:cam.data.dof.use_dof=False
S.render.engine='CYCLES';S.cycles.use_denoising=True;S.cycles.denoiser='OPENIMAGEDENOISE';S.cycles.samples=256;S.cycles.adaptive_threshold=.015;S.cycles.max_bounces=12;S.cycles.transmission_bounces=10;S.cycles.transparent_max_bounces=12
S.render.resolution_x=2400;S.render.resolution_y=1800;S.render.resolution_percentage=100
S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];S['review_iteration']='95 / pass3 HDR light and still presentation';S['video_render_requires_explicit_approval']=True;S['environment95']='Belfast Sunset HDRI CC0; illustrative setting, not surveyed surroundings. HDRI with restrained warm sun at source orientation; illustrative lighting, not a solar study.'
bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_95_Pass3.blend'),compress=True)
# Still proofs only; no animation render call.
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
for d in pref.devices:d.use=d.type=='OPTIX'
S.cycles.device='GPU';S.cycles.denoising_use_gpu=True;S.render.use_persistent_data=True
S.cycles.samples=96;S.cycles.adaptive_threshold=.035;S.render.resolution_x=1280;S.render.resolution_y=960
for name,key in [('CAM | Presentación verticales corregidas','exterior'),('REV | Estudio y cubierta','estudio'),('REV | Dormitorio completo','dormitorio')]:
 cam=bpy.data.objects[name];S.camera=cam;S.frame_set(cam.get('presentation_frame',1));S.render.filepath=os.path.join(ROOT,'review95','pass3_'+key+'.png');bpy.ops.render.render(write_still=True);print('STILL95_READY',key,flush=True)
print('PASS3_STILLS_COMPLETE_VIDEO_PAUSED',flush=True)
