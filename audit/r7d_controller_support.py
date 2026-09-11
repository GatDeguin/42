import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(r'D:\2026\42');S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();DG=bpy.context.evaluated_depsgraph_get()
o=bpy.data.objects['Consola estudio'];e=o.evaluated_get(DG);m=e.to_mesh();bv=BVHTree.FromPolygons([e.matrix_world@q.co for q in m.vertices],[list(p.vertices) for p in m.polygons]);e.to_mesh_clear()
rows=[]
for x in [18.20,18.35,18.55,18.70,18.765]:
 for z in [2.6,3.0,3.4]:
  p,n,i,d=bv.ray_cast(Vector((x,-z,4.0454)),Vector((0,0,-1)),1)
  rows.append(dict(x=x,z=z,supportH=p.z if p else None,gapFromControllerBottom=4.045499801635742-p.z if p else None))
(R/'audit/r7d_preliminary/studio_controller_support.json').write_text(json.dumps({'sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'probes':rows},indent=2),encoding='utf-8')
print(rows)
