import bpy,os,json
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene
o=bpy.data.objects['Entorno | terreno continuo']
bpy.ops.mesh.primitive_cube_add(size=1,location=(11,-10,0));c=bpy.context.object;c.dimensions=(22.02,20.02,5);bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;md=o.modifiers.new('Vacío bajo lote y pileta','BOOLEAN');md.operation='DIFFERENCE';md.object=c;bpy.ops.object.modifier_apply(modifier=md.name);bpy.data.objects.remove(c,do_unlink=True)
water=bpy.data.objects['Agua de pileta'];water.modifiers['Water volume | basin depth'].thickness=1.474
for o in S.objects:
 if o.type=='MESH' and o.name.startswith(('Fondo de pileta','Borde pileta','Escalón pileta','Playa húmeda')):o.cycles.is_caustics_receiver=True
bpy.data.objects['Sol | Atardecer cálido'].data.energy=3.3
S.view_settings.exposure=.28;S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];S.frame_set(1)
note=json.loads(S['corrections']);note.append('Distant terrain excludes the complete source plot, preventing soil from covering the submerged pool volume. Water volume reaches real basin floor; pool caustic receivers enabled.');S['corrections']=json.dumps(note,ensure_ascii=False)
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_Revision.blend'),compress=True)
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='OPTIX';p.get_devices()
for d in p.devices:d.use=d.type=='OPTIX'
S.cycles.device='GPU';S.cycles.samples=96;S.cycles.denoiser='OPENIMAGEDENOISE';S.cycles.denoising_use_gpu=True;S.render.resolution_x=1600;S.render.resolution_y=1200;S.render.filepath=os.path.join(ROOT,'review','iter1_exterior.png');bpy.ops.render.render(write_still=True)
print('POOL_AND_PRESENTATION_CORRECTED',flush=True)
