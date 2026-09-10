import bpy,json
from mathutils import Vector
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();rows=[]
for o in S.objects:
 if any(t.lower() in o.name.lower() for t in ['Campana cocina','extracción cocina','ducto cocina','extractor cocina','manta','almoh','sábana','colch','Cabezal','luz dormitorio','Lámpara mesa suite']):
  v=[o.matrix_world@Vector(q) for q in o.bound_box] if o.type=='MESH' else [o.matrix_world.translation]
  rows.append({'name':o.name,'type':o.type,'xyz':[[round(min(p[i] for p in v),5),round(max(p[i] for p in v),5)] for i in [0,2,1]],'materials':[s.material.name if s.material else '' for s in o.material_slots] if o.type=='MESH' else [],'vertices':len(o.data.vertices) if o.type=='MESH' else 0})
print(json.dumps(rows,ensure_ascii=False));json.dump(rows,open('review95/r5c_fitout_probe.json','w',encoding='utf8'),ensure_ascii=False,indent=2)
