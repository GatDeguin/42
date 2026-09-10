import bpy,os,json,ast
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
import numpy as np
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
tree=ast.parse(open(os.path.join(ROOT,'scripts','iteration1_pass1.py'),encoding='utf8').read())
for nd in tree.body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['cv','put','box','cut','bounds']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helpers>','exec'))
ceiling=bpy.data.objects['Cielorraso estudio | cota inferior 6.45m']
ac=[o for o in S.objects if o.name.startswith(('Bafle cielorraso estudio','Cloud estudio'))]
for panel in ac:
 lo,hi=bounds(panel)
 cutter=box('Temporal junta perimetral acústica',[(lo[0]+hi[0])/2,6.5,-(lo[1]+hi[1])/2],[hi[0]-lo[0]+.008,.5,hi[1]-lo[1]+.008],col='REFERENCE',bev=0)
 cut(ceiling,cutter);bpy.data.objects.remove(cutter,do_unlink=True)
ceiling['construction_note']='18mm lining cut around acoustic panels with4mm dry perimeter joint; all undersides retain+6.45m.'
S['review_iteration']='2 / three passes plus acoustic ceiling regression repair'
S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];S.frame_set(1);bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_Revision.blend'),compress=True)
print('ACOUSTIC_CEILING_JOINTS_RESTORED',len(ac),flush=True)
