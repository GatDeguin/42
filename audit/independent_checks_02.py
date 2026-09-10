import bpy,json,os,itertools,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
def geo(o):
 e=o.evaluated_get(dg);m=e.to_mesh();p=[o.matrix_world@v.co for v in m.vertices];f=[list(f.vertices) for f in m.polygons];e.to_mesh_clear();a=np.array(p)
 return (a.min(0),a.max(0),BVHTree.FromPolygons(p,f))
def overlap(a,b):
 return np.all(np.minimum(a[1],b[1])-np.maximum(a[0],b[0])>.002)
def meaningful(a,b):
 if not overlap(a,b):return 0
 return len(a[2].overlap(b[2]))
pipes=[o for o in S.objects if o.type=='MESH' and o.name.startswith('Extracción ')]
targets=[o for o in S.objects if o.type=='MESH' and not o.hide_render and any(t in o.name.lower() for t in ['cabio','correa','cielorraso','aislación','cubierta pendiente','patinillo','losa','piso estudio','tabique','medianera','separación mono','muro','viga de apoyo'])]
g={o.name:geo(o) for o in targets+pipes}
hits=[]
for p in pipes:
 for o in targets:
  n=meaningful(g[p.name],g[o.name])
  if n:hits.append({'pipe':p.name,'other':o.name,'tri_pairs':n})
# Actual moving rear panes, tracks and gate; test all children, not only handles.
walls=[o for o in S.objects if o.type=='MESH' and not o.hide_render and any(t in o.name.lower() for t in ['muro','tabique','separación mono','división estudio','medianera','fachada ciega','paño']) and not o.parent and not any(t in o.name.lower() for t in ['marco','vidrio','paño fijo','frente cocina'])]
wg={o.name:geo(o) for o in walls}
doorhits=[]
rigs=[o for o in S.objects if o.name.startswith('DOOR | ')]
for fr in [1,42,54,66,78,90,105]:
 S.frame_set(fr);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
 for rig in rigs:
  for o in rig.children:
   if o.type!='MESH' or any(t in o.name.lower() for t in ['manija','tirador','rueda','bulón','bisagra']):continue
   gg=geo(o)
   for wall in walls:
    n=meaningful(gg,wg[wall.name])
    if n:doorhits.append({'frame':fr,'rig':rig.name,'leaf':o.name,'other':wall.name,'tri_pairs':n})
result={'file':bpy.data.filepath,'pipe_structure_intersections':hits,'all_door_leaf_wall_intersections':doorhits}
json.dump(result,open(r'D:\2026\42\audit\independent_checks_02.json','w',encoding='utf8'),ensure_ascii=False,indent=2)
print(json.dumps(result,ensure_ascii=False))
