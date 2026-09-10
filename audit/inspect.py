import bpy,json,os
from mathutils import Vector
root=r'D:\2026\42\audit';os.makedirs(root,exist_ok=True)
S=bpy.context.scene
def bounds(o):
 ps=[o.matrix_world@Vector(p) for p in o.bound_box]
 return {'lo':[min(p[i] for p in ps) for i in range(3)],'hi':[max(p[i] for p in ps) for i in range(3)]}
data={'closed':[],'open':[]}
for fr,key in [(1,'closed'),(150,'open')]:
 S.frame_set(fr);bpy.context.view_layer.update()
 for o in S.objects:
  if o.type!='MESH':continue
  n=o.name.lower()
  if any(t in n for t in ['árbol','arbol','hoja','rama','tronco','césped','cesped','grove','hierba','grass','follaje','surround','exterior grove']):continue
  d={'name':o.name,'hidden':o.hide_render,'collections':[c.name for c in o.users_collection],'verts':len(o.data.vertices),'polys':len(o.data.polygons),'materials':[s.material.name if s.material else '' for s in o.material_slots],**bounds(o)}
  data[key].append(d)
json.dump(data,open(os.path.join(root,'geometry_bounds.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
print('AUDIT_DUMP',len(data['closed']))
