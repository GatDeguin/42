import bpy,json
from mathutils import Vector
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();rows=[]
for o in S.objects:
 if o.type=='MESH':
  v=[o.matrix_world@Vector(q) for q in o.bound_box];a=[min(p[i] for p in v) for i in range(3)];b=[max(p[i] for p in v) for i in range(3)]
  if ((a[0]<17.65 and b[0]>14.2 and a[1]<-6.05 and b[1]>-6.25 and b[2]>4.6) or 'pared' in o.name.lower() or 'Cocina' in o.name or 'Heladera' in o.name):
   rows.append({'name':o.name,'mats':[(s.material.name,s.material.get('source_material_key')) for s in o.material_slots if s.material],'bounds':[a,b]})
print(json.dumps(rows,ensure_ascii=False));json.dump(rows,open('review95/wall_material_probe.json','w',encoding='utf8'),ensure_ascii=False,indent=2)
