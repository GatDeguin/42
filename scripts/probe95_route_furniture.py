import bpy,json,numpy as np
from mathutils import Vector
S=bpy.context.scene;S.frame_set(150);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
r={}
for o in S.objects:
 if o.type!='MESH' or not o.name.startswith(('Mueble apoyo estudio','Mesa comedor','Silla comedor','Sofá vivienda','Puerta baño vivienda','Puerta dormitorio','Mesa quincho','Silla quincho')):continue
 e=o.evaluated_get(dg);v=np.array([e.matrix_world@Vector(p) for p in e.bound_box]);a,b=v.min(0),v.max(0)
 r[o.name]={'x':[round(float(a[0]),4),round(float(b[0]),4)],'z':[round(float(-b[1]),4),round(float(-a[1]),4)],'h':[round(float(a[2]),4),round(float(b[2]),4)]}
json.dump(r,open(r'D:\2026\42\review95\r6_route_furniture.json','w'),ensure_ascii=False,indent=2)
print(json.dumps({n:v for n,v in r.items() if any(t in n for t in ['tapa','asiento','Sofá vivienda asiento','Puerta baño vivienda','Mueble apoyo estudio','Puerta dormitorio'])},ensure_ascii=False))
