import bpy,json
from mathutils import Vector
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();rows=[]
for r in S.objects:
 if r.name.startswith('DOOR | ') and r.get('motion')=='hinge':
  def b(o):
   v=[o.matrix_world@Vector(q) for q in o.bound_box];return [[round(min(p[i] for p in v),4) for i in range(3)],[round(max(p[i] for p in v),4) for i in range(3)]]
  rows.append({'name':r.name,'location':list(r.location),'drivers':[(d.data_path,d.array_index,d.driver.expression) for d in r.animation_data.drivers],'children':[(o.name,b(o)) for o in r.children if o.type=='MESH']})
print(json.dumps(rows,ensure_ascii=False));json.dump(rows,open('review95/hinge_probe.json','w',encoding='utf8'),ensure_ascii=False,indent=2)
