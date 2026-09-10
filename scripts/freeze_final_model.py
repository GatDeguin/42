import bpy,os,json
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene
S['review_iteration']='3 / final coordinated model';S['video_render_requires_explicit_approval']=True
for tx in bpy.data.texts:
 if tx.name.startswith('LEEME'):
  s=tx.as_string().replace('Modelo vigente: Casa_de_Campo_Revision.blend.','Modelo vigente: Casa_de_Campo_Final.blend.');tx.clear();tx.write(s)
S.frame_set(1);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_Final.blend'),compress=True)
print('FINAL_MODEL_SAVED',bpy.data.filepath,flush=True)
