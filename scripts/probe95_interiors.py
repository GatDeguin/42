import bpy,json,os
from mathutils import Vector
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
def b(o):
 v=[o.matrix_world@Vector(x) for x in o.bound_box]
 return [[round(min(p[i] for p in v),5) for i in range(3)],[round(max(p[i] for p in v),5) for i in range(3)]]
objects=[]
for o in S.objects:
 n=o.name.lower()
 if o.type=='MESH' and any(k in n for k in ['quincho','cama dormitorio','cabezal dormitorio','mesa de luz','lámpara mesa','banqueta','placard dormitorio','vestidor tabique','dormitorio transversal']):
  objects.append({'name':o.name,'bounds':b(o),'matrix':[list(r) for r in o.matrix_world],'materials':[m.name if m else None for m in o.data.materials],'mesh_verts':len(o.data.vertices),'modifiers':[(m.name,m.type) for m in o.modifiers]})
mats=[]
for m in bpy.data.materials:
 if m.get('source_material_key') in ['whitePlaster','concrete','cement','wood','darkWood','fabric','linen','acoustic']:
  nodes=[]
  for n in m.node_tree.nodes:
   if n.type in ['TEX_NOISE','BUMP','VALTORGB','MIX_RGB','TEX_IMAGE','BSDF_PRINCIPLED']:
    nodes.append({'type':n.type,'name':n.name,'image':n.image.name if n.type=='TEX_IMAGE' and n.image else None,'inputs':{v.name:list(v.default_value) if hasattr(v.default_value,'__len__') else v.default_value for v in n.inputs if hasattr(v,'default_value') and v.type in ['VALUE','RGBA','VECTOR']},'links':[(l.from_node.name,l.from_socket.name,l.to_socket.name) for l in m.node_tree.links if l.to_node==n]})
  mats.append({'name':m.name,'key':m.get('source_material_key'),'nodes':nodes})
os.makedirs('review95',exist_ok=True)
json.dump({'objects':objects,'materials':mats},open('review95/interior_probe.json','w',encoding='utf8'),ensure_ascii=False,indent=2)
print('PROBE',len(objects),len(mats))
