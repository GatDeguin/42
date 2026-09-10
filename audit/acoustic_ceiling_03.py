import bpy,json,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
def geom(o):
 p=[o.matrix_world@v.co for v in o.data.vertices];q=np.array(p);return q.min(0),q.max(0),BVHTree.FromPolygons(p,[list(x.vertices) for x in o.data.polygons])
c=bpy.data.objects['Cielorraso estudio | cota inferior 6.45m'];a,b,B=geom(c);hits=[]
for o in S.objects:
 if o.name.startswith(('Bafle cielorraso estudio','Cloud estudio')):
  d,e,C=geom(o);inter=B.overlap(C)
  if inter:hits.append({'panel':o.name,'intersection_pairs':len(inter),'box_overlap_m':np.minimum(b,e).__sub__(np.maximum(a,d)).tolist()})
print(json.dumps({'ceiling_vertices':len(c.data.vertices),'panel_ceiling_intersections':hits},ensure_ascii=False))
json.dump({'ceiling_vertices':len(c.data.vertices),'panel_ceiling_intersections':hits},open(r'D:\2026\42\audit\acoustic_ceiling_03.json','w',encoding='utf8'),ensure_ascii=False,indent=2)
