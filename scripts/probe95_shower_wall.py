import bpy,json
from mathutils import Vector
S=bpy.context.scene;S.frame_set(150);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
r={'hits':[],'fixtures':[]}
for h in [.4,1.0,1.31,1.7,2.1,2.31]:
 hit,loc,n,index,obj,mat=S.ray_cast(dg,Vector((21.35,-5.10,h)),Vector((0,1,0)),distance=1)
 r['hits'].append({'height':h,'name':obj.name if hit else None,'source_hit':[loc.x,loc.z,-loc.y] if hit else None})
for o in S.objects:
 if o.name.startswith('BTH95 | ducha ') or o.name=='Ducha baño mono':
  e=o.evaluated_get(dg);p=[e.matrix_world@Vector(v) for v in e.bound_box];r['fixtures'].append({'name':o.name,'bounds':[[min(v[i] for v in p) for i in range(3)],[max(v[i] for v in p) for i in range(3)]]})
json.dump(r,open('D:/2026/42/review95/shower_wall_probe.json','w'),ensure_ascii=False,indent=2)
print(r['hits'])
