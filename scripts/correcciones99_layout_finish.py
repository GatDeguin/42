"""Local completion of R7 layout; callable on loaded layout candidate, no implicit save."""
import bpy,json,ast,bmesh
from pathlib import Path
from mathutils import Vector

def apply():
 global S,COL,M
 S=bpy.context.scene;COL=bpy.data.collections['99 | Layout R7'];M={m.get('source_material_key'):m for m in bpy.data.materials if m.get('source_material_key')}
 for m in bpy.data.materials:
  if m.name.startswith(('SL95 | ','MAT95 | ')):M[m.name.split(' | ',1)[1]]=m
 for nd in ast.parse((Path(__file__).parent/'correcciones95_corredizas_r5.py').read_text(encoding='utf-8-sig')).body:
  if isinstance(nd,ast.FunctionDef) and nd.name in ['mat','cv','src','child','box','boolean','cylinder']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'),globals())
 c=box('TEMP membrane corner',{'x':[20.9,21.8],'y':[.19,.36],'z':[.256,.26]});boolean(bpy.data.objects['Pilar esquina frontal derecha'],c);bpy.data.objects.remove(c,do_unlink=True)
 c=cylinder('TEMP shower pipe reserve',(21.384,.135,.985),(21.606,.131,.985),.024);boolean(bpy.data.objects['Losa planta baja'],c);bpy.data.objects.remove(c,do_unlink=True)
 s=bpy.context.scene;o=bpy.data.objects['Alfombra comedor'];s.frame_set(1);bpy.context.view_layer.update()
 pts=[o.matrix_world@Vector(v) for v in o.bound_box];lo=min(p.z for p in pts);hi=max(p.z for p in pts)
 # A flatwoven8mm rug bears directly on the unchanged+3.25 finish.
 inv=o.matrix_world.inverted()
 for v in o.data.vertices:
  p=o.matrix_world@v.co;p.z=3.25+(p.z-lo)*.008/(hi-lo);v.co=inv@p
 o.data.update();o['detail_status']='P / alfombra tejida plana8mm apoyada sobre piso'
 s['r7_layout_rug_correction']=json.dumps({'object':o.name,'previous_bottom':lo,'previous_top':hi,'bottom':3.25,'top':3.258,'plan_preserved':True,'reason':'2mm geometric clearance below the new bedroom leaf; no certified product.'})
 bpy.context.view_layer.update()
 return json.loads(s['r7_layout_rug_correction'])
