import bpy,json
from mathutils import Vector
rows=[];bpy.context.scene.frame_set(1);bpy.context.view_layer.update()
for o in bpy.context.scene.objects:
 if any(k in o.name for k in ['Horno empotrado','Horno cocina','Anafe cocina','Inductor cocina','Heladera','Bacha cocina','Grifería cocina','Consola estudio','Toallero baño suite']):
  v=[o.matrix_world@Vector(q) for q in o.bound_box] if o.type=='MESH' else [o.matrix_world.translation]
  rows.append({'name':o.name,'xyz':[[round(min(p[i] for p in v),5),round(max(p[i] for p in v),5)] for i in [0,2,1]],'material':[s.material.name if s.material else None for s in o.material_slots]})
print(json.dumps(rows,ensure_ascii=False));json.dump(rows,open('review95/appliance_probe.json','w',encoding='utf8'),ensure_ascii=False,indent=2)
