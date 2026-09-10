import bpy,json,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
def geo(o):
 e=o.evaluated_get(dg);m=e.to_mesh();p=[o.matrix_world@v.co for v in m.vertices];f=[list(f.vertices) for f in m.polygons];e.to_mesh_clear();a=np.array(p)
 return (a.min(0),a.max(0),BVHTree.FromPolygons(p,f))
def hit(a,b):
 if not np.all(np.minimum(a[1],b[1])-np.maximum(a[0],b[0])>.002):return 0
 return len(a[2].overlap(b[2]))
names=['inodoro','bidet','bañera','bacha','lavatorio','cama','placard','mesa','silla','sillón','sofá','cocina lineal','mueble','estante','rack','parlante']
fixed=[o for o in S.objects if o.type=='MESH' and not o.hide_render and not o.parent and any(t in o.name.lower() for t in names)]
g={o.name:geo(o) for o in fixed};rigs=[o for o in S.objects if o.name.startswith('DOOR | ')];out=[]
for fr in [1,50,66,78,90,105]:
 S.frame_set(fr);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
 for rig in rigs:
  for o in rig.children:
   if o.type!='MESH' or any(t in o.name.lower() for t in ['manija','tirador','rueda','bulón','bisagra']):continue
   gg=geo(o)
   for f in fixed:
    n=hit(gg,g[f.name])
    if n:out.append({'frame':fr,'door':rig.name,'part':o.name,'fixture':f.name,'tri_pairs':n})
json.dump(out,open(r'D:\2026\42\audit\door_fixtures_03.json','w',encoding='utf8'),ensure_ascii=False,indent=2);print(json.dumps(out,ensure_ascii=False))
