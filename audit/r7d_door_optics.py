import bpy,json,hashlib,math
from pathlib import Path
R=Path(r'D:\2026\42');S=bpy.context.scene;S.frame_set(150);bpy.context.view_layer.update();DG=bpy.context.evaluated_depsgraph_get();rows=[]
for o in S.objects:
 if o.type!='MESH' or not ('dormitorio' in o.name.lower() and 'hoja' in o.name.lower()):continue
 e=o.evaluated_get(DG);m=e.to_mesh();nm=e.matrix_world.to_3x3().inverted().transposed();faces=[]
 for p in m.polygons:
  if p.area<.1:continue
  n=(nm@p.normal).normalized();ds=[math.degrees(n.angle((nm@m.corner_normals[i].vector).normalized())) for i in p.loop_indices]
  faces.append(dict(face=p.index,area=p.area,smooth=p.use_smooth,deviations=ds))
 rows.append(dict(name=o.name,custom=m.has_custom_normals,faces=faces,modifiers=[m.type for m in o.modifiers]));e.to_mesh_clear()
report=dict(sha256=hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),frame=150,doors=rows)
(R/'audit/r7d_preliminary/door_optical_normals.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(rows)
