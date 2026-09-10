import bpy,os,json,ast,numpy as np
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_textiles.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['bounds','deform']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
pivots={'suiteEntry':(1,-8.9775),'bedroomLink':(0,17.5975),'bathLink':(0,19.3975),'poolBath':(1,-11.9425)}
records=[]
for key,(axis,val) in pivots.items():
 r=bpy.data.objects['DOOR | '+key];saved={o:o.matrix_world.copy() for o in r.children};before=list(r.location);r.location[axis]=val
 for fc in r.animation_data.drivers:
  if fc.data_path=='rotation_euler':fc.driver.expression='opening * 1.5707963267948966'
 bpy.context.view_layer.update()
 for o,mw in saved.items():o.matrix_world=mw
 bpy.context.view_layer.update();records.append({'rig':r.name,'before':before,'after':list(r.location),'max_closed_matrix_error':max(max(abs(o.matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4)) for o,m in saved.items())})
for name,lo,hi in [('Premarco baño suite lateral A',7.975,8.025),('Premarco baño suite lateral B',7.095,7.145)]:
 o=bpy.data.objects[name];a,b=bounds(o)
 deform(o,lambda p:Vector((p.x,-(lo+(-p.y+b[1])*(hi-lo)/(b[1]-a[1])),p.z)))
S['hinge_axes_r5']=json.dumps(records);S['review_iteration']='95 / R5A2 four additional hinged doors'
S.frame_set(1);bpy.context.view_layer.update();bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_95_R5A2.blend'),compress=True)
print('HINGES_SAVED',json.dumps(records),flush=True)
