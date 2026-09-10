import bpy,json
from mathutils import Vector
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
rows=[]
for o in S.objects:
 if any(t.lower() in o.name.lower() for t in ['puerta estudio','acceso estudio','burlete','tapajunta','zócalo vestidor','frente vestidor','Aplique','toallero','mesa mono','silla mono','Panel acústico trasero','umbral estudio','Luz exterior']):
  v=[o.matrix_world@Vector(q) for q in o.bound_box] if o.type=='MESH' else [o.matrix_world.translation]
  rows.append({'name':o.name,'type':o.type,'parent':o.parent.name if o.parent else None,'bounds':[[round(min(p[i] for p in v),5),round(max(p[i] for p in v),5)] for i in [0,2,1]],'collection':[c.name for c in o.users_collection]})
json.dump(rows,open('review95/r5a_context.json','w',encoding='utf8'),ensure_ascii=False,indent=2)
print(json.dumps(rows,ensure_ascii=False))
