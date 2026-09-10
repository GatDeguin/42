"""Compare licensed photographic tree asset at the original planting centres."""
import bpy,os,math,json
from mathutils import Matrix,Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);col=bpy.data.collections['LANDSCAPE']
asset=os.path.join(ROOT,'source','assets','tree_small_02','tree_small_02_2k.blend')
with bpy.data.libraries.load(asset,link=False) as (src,dst):dst.objects=['tree_small_02_LOD1']
tree=dst.objects[0];tree.name='BOT95 | árbol fotografiado base';data=tree.data
for m in data.materials:
 m['asset_source']='https://polyhaven.com/a/tree_small_02';m['asset_license']='CC0';m['preserve_asset_uv']=True
# Every replacement shares mesh and textures; normal source locations remain unchanged.
poses=[]
for o in S.objects:
 if o.name.startswith('MAT95 | árbol ') and o.name.endswith('ramas'):poses.append((o.name,o.matrix_world.copy()))
for o in S.objects:
 if o.name.startswith('MAT95 | árbol '):o.hide_render=True;o.hide_set(True)
for i,(name,mat) in enumerate(poses):
 o=bpy.data.objects.new('BOT95 | árbol %02d'%i,data);col.objects.link(o);o.matrix_world=mat@Matrix.Diagonal((1.01,.83,.84,1))
 o['asset_source']='https://polyhaven.com/a/tree_small_02';o['asset_license']='CC0';o['tree_source_centre']=list(mat.translation);o['preserve_asset_uv']=True
S['botany95']='TreeSmall02, RicoCilliers / PolyHaven, CC0. Mesh instance at the same planting centres; species illustrative.'
bpy.context.view_layer.update();S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_95_Pass3a.blend'),compress=True)
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
for d in pref.devices:d.use=d.type=='OPTIX'
S.cycles.device='GPU';S.cycles.samples=96;S.cycles.adaptive_threshold=.035;S.cycles.denoising_use_gpu=True;S.render.resolution_x=1600;S.render.resolution_y=1200;S.render.resolution_percentage=100
S.render.filepath=os.path.join(ROOT,'review95','pass3a_exterior.png');bpy.ops.render.render(write_still=True)
print('BOTANICAL_COMPARISON_READY_NO_VIDEO',len(poses),flush=True)
