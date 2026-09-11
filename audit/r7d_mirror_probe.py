"""Read-only mirror optical face and material diagnosis on frozen R7D."""
import bpy,json,hashlib,math
from pathlib import Path
from mathutils import Vector
R=Path(r'D:\2026\42');S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();DG=bpy.context.evaluated_depsgraph_get()
EXPECTED='9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e'
assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==EXPECTED
items=[]
for o in S.objects:
 if o.type!='MESH' or 'espejo' not in o.name.lower():continue
 e=o.evaluated_get(DG);m=e.to_mesh();nm=e.matrix_world.to_3x3().inverted().transposed();v=[e.matrix_world@p.co for p in m.vertices]
 faces=[]
 for p in m.polygons:
  if p.area<.025:continue
  normal=(nm@p.normal).normalized();corners=[(nm@m.corner_normals[i].vector).normalized() for i in p.loop_indices]
  faces.append(dict(index=p.index,area=p.area,vertexCount=len(p.vertices),geometric_normal=list(normal),corners=[list(n) for n in corners],cornerDeviationDegrees=[math.degrees(normal.angle(n)) for n in corners],smooth=p.use_smooth,vertices=[list(v[i]) for i in p.vertices]))
 mats=[]
 for mat in o.data.materials:
  if not mat:continue
  nodes=[]
  if mat.use_nodes:
   for n in mat.node_tree.nodes:
    ins={}
    for i in n.inputs:
     if i.is_linked:ins[i.name]=[f'{l.from_node.name}.{l.from_socket.name}' for l in i.links]
     elif hasattr(i,'default_value'):
      val=i.default_value
      try:ins[i.name]=list(val)
      except:ins[i.name]=val
    nodes.append(dict(name=n.name,type=n.type,inputs=ins))
  mats.append(dict(name=mat.name,nodes=nodes))
 mods=[]
 for mod in o.modifiers:
  d={'name':mod.name,'type':mod.type,'render':mod.show_render,'viewport':mod.show_viewport}
  for attr in ['width','segments','harden_normals','limit_method','angle_limit','keep_sharp','mode','weight']:
   if hasattr(mod,attr):d[attr]=getattr(mod,attr)
  mods.append(d)
 items.append(dict(name=o.name,modifiers=mods,evaluated_faces=faces,materials=mats,hasCustomNormals=m.has_custom_normals,dimensions=list(o.dimensions),scale=list(o.scale)))
 e.to_mesh_clear()
report=dict(sha256=EXPECTED,mirrors=items,cameras=[dict(name=o.name,location=list(o.matrix_world.translation),lens=o.data.lens) for o in S.objects if o.type=='CAMERA' and any(k in o.name.lower() for k in ['baño','bano','quincho'])])
(R/'audit/r7d_preliminary/mirror_probe.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
for q in items:
 print(q['name'],'MODS',q['modifiers'],'CUSTOM',q['hasCustomNormals'])
 for f in q['evaluated_faces']:print('FACE',f['index'],'N',f['geometric_normal'],'DEVIATION',f['cornerDeviationDegrees'],'SMOOTH',f['smooth'])
 print('MATERIAL',json.dumps(q['materials'],ensure_ascii=False))
print('MIRROR_PROBE_DONE',flush=True)
