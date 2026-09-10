import bpy,json,sys,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parent.parent;data=json.loads((root/'review95/corredizas_r6_drains.json').read_text(encoding='utf8'));dg=bpy.context.evaluated_depsgraph_get();checks=[]
def cv(p):return Vector((p[0],-p[2],p[1]))
for f in data['families']:
 for j,d in enumerate(f['drains'],1):
  name='SL95 | '+f['family']+f' drenaje{j} Ø14 interior10';o=bpy.data.objects[name];e=o.evaluated_get(dg);me=e.to_mesh();verts=[e.matrix_world@v.co for v in me.vertices];faces=[list(p.vertices) for p in me.polygons];tree=BVHTree.FromPolygons(verts,faces,epsilon=1e-7);e.to_mesh_clear();center=cv(d['bend_midpoint'])-cv(d['bend_tangent'])*.0003;end=cv(d['outlet']);out=(end-cv(d['start'])).normalized();normal=cv(d['bend_plane_normal']);tangent=cv(d['bend_tangent']);side=tangent.cross(normal).normalized();rays=[]
  for k in range(32):
   ray=normal*math.cos(2*math.pi*(k+.37)/32)+side*math.sin(2*math.pi*(k+.37)/32);hit=tree.ray_cast(center,ray,.025);rays.append(hit[3])
  top_height=f['rolling_height_m']-.002+.001;top=cv(d['mouth_top']);topopen=tree.ray_cast(top-Vector((0,0,.003)),Vector((0,0,1)),.02)[0] is None;endopen=tree.ray_cast(end-out*.003,out,.02)[0] is None
  checks.append({'object':name,'back_corner_32_rays_have_wall':all(v is not None and .0045<v<.0055 for v in rays),'inner_wall_first_hit_min_m':min(v for v in rays if v is not None),'inner_wall_first_hit_max_m':max(v for v in rays if v is not None),'top_mouth_open':topopen,'outlet_mouth_open':endopen})
result={'model':bpy.data.filepath,'checks':checks,'pass':all(x['back_corner_32_rays_have_wall'] and x['top_mouth_open'] and x['outlet_mouth_open'] for x in checks),'method':'BVH rays from elbow cavity:32 radial directions0.3mm off the mid-ring seam, avoiding ray/edge degeneracy; two free-mouth checks; geometric continuity only, no hydraulic test.'};(root/'review95/corredizas_r6_drain_checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8');print(json.dumps(result,ensure_ascii=False,indent=2))
