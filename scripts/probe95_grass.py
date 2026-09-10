import bpy,json
from mathutils import Vector
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();r=[]
for o in S.objects:
 if o.name.startswith('Banco huerta | loseta') or o.name=='Césped botánico 04-03':
  e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());p=[e.matrix_world@Vector(v) for v in e.bound_box]
  r.append({'name':o.name,'type':o.type,'hide_render':o.hide_render,'hide_view':o.hide_get(),'raw_bounds':[[min((o.matrix_world@Vector(v))[i] for v in o.bound_box) for i in range(3)],[max((o.matrix_world@Vector(v))[i] for v in o.bound_box) for i in range(3)]],'eval_bounds':[[min(v[i] for v in p) for i in range(3)],[max(v[i] for v in p) for i in range(3)]],'verts':len(o.data.vertices) if o.type=='MESH' else None})
json.dump(r,open('D:/2026/42/review95/grass_pad_probe.json','w'),ensure_ascii=False,indent=2)
