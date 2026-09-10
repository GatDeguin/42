import bpy,json
from mathutils import Vector
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();rows=[]
for o in S.objects:
 if o.type=='MESH' and any(t in o.name for t in ['puerta estudio','Puerta acceso estudio','Estudio lateral','División estudio vivienda','Toallero baño suite','Premarco baño suite','Zócalo vestidor frente','Aplique descanso','Aplique exterior | carcasa','Puerta acceso vestidor marco']):
  v=[o.matrix_world@Vector(q) for q in o.bound_box];rows.append({'name':o.name,'xyz':[[round(min(p[i] for p in v),5),round(max(p[i] for p in v),5)] for i in [0,2,1]]})
print(json.dumps(rows,ensure_ascii=False));json.dump(rows,open('review95/door_context_bounds.json','w',encoding='utf8'),ensure_ascii=False,indent=2)
