import bpy,json,ast,os,numpy as np
from mathutils import Vector
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
def bd(o):
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());v=np.array([e.matrix_world@Vector(p) for p in e.bound_box])
 a,b=v.min(0),v.max(0);return [[float(a[0]),float(a[2]),float(-b[1])],[float(b[0]),float(b[2]),float(-a[1])]]
names=('Vestidor cajón','Vestidor lateral','Vestidor costado','Vestidor módulo','MOB95 | guía','Cocina lineal','Frente cocina vivienda','Tirador cocina vivienda','Horno cocina','Mueble TV','MOB95 | riel corredero')
r={o.name:bd(o) for o in S.objects if o.type=='MESH' and o.name.startswith(names)}
json.dump(r,open(r'D:\2026\42\review95\r6e_input_bounds.json','w'),indent=2,ensure_ascii=False)
print(json.dumps(r,ensure_ascii=False))
