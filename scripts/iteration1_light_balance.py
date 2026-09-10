import bpy,os,math,json
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene
sun=bpy.data.objects['Sol | Atardecer cálido'];sun.location=( -45,-40,25 );target=Vector((17,-8,2));sun.rotation_euler=(sun.location-target).to_track_quat('Z','Y').to_euler();sun.data.energy=2.6;sun.data.color=(1,.72,.46)
nodes=S.world.node_tree.nodes;sky=next(n for n in nodes if n.type=='TEX_SKY');sky.sun_elevation=math.radians(18);next(n for n in nodes if n.type=='BACKGROUND').inputs['Strength'].default_value=.18
S.view_settings.exposure=.25
water=bpy.data.objects['Agua de pileta'];basin=bpy.data.objects['Fondo de pileta']
print('CAUSTICS_PROPS',[(o.name,[p.identifier for p in o.cycles.bl_rna.properties if 'caustic' in p.identifier]) for o in [water,basin]],flush=True)
for o in [water]:
 if hasattr(o.cycles,'is_caustics_caster'):o.cycles.is_caustics_caster=True
for o in [basin]:
 if hasattr(o.cycles,'is_caustics_receiver'):o.cycles.is_caustics_receiver=True
if hasattr(sun.data.cycles,'is_caustics_light'):sun.data.cycles.is_caustics_light=True
for m in bpy.data.materials:
 if m.get('source_material_key')=='water':
  for n in m.node_tree.nodes:
   if n.type=='VOLUME_ABSORPTION':n.inputs['Density'].default_value=.04
S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];S.frame_set(1)
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_Revision.blend'),compress=True)
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='OPTIX';p.get_devices()
for d in p.devices:d.use=d.type=='OPTIX'
S.cycles.device='GPU';S.cycles.samples=96;S.cycles.denoiser='OPENIMAGEDENOISE';S.cycles.denoising_use_gpu=True;S.render.resolution_x=1600;S.render.resolution_y=1200;S.render.filepath=os.path.join(ROOT,'review','iter1_exterior.png');bpy.ops.render.render(write_still=True)
print('SUNSET_LIGHT_REVIEW_READY',flush=True)
