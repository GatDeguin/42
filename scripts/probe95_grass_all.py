import bpy,json
from mathutils import Vector
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
def bound(o):
 e=o.evaluated_get(dg);p=[e.matrix_world@Vector(v) for v in e.bound_box]
 return [[min(v[i] for v in p) for i in range(3)],[max(v[i] for v in p) for i in range(3)]]
pads=[bound(o) for o in S.objects if o.name.startswith('Banco huerta | loseta')]
r=[]
for o in S.objects:
 if o.type!='MESH' or o.hide_render or o.name.startswith('Banco huerta'):continue
 a,b=bound(o)
 if not (a[2]<.17 and b[2]>.01):continue
 if any(all(min(b[k],d[k])-max(a[k],c[k])>0 for k in range(3)) for c,d in pads):r.append({'name':o.name,'bounds':[a,b],'collections':[c.name for c in o.users_collection],'vertices':len(o.data.vertices)})
json.dump(r,open('D:/2026/42/review95/grass_pad_all.json','w'),ensure_ascii=False,indent=2)
