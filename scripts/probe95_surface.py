import bpy,json
for name in ['Heladera puerta superior','Horno cocina vidrio','Anafe cocina','División estudio vivienda']:
 o=bpy.data.objects[name];print(name,'custom',o.data.has_custom_normals,'slots',[(s.link,s.material.name) for s in o.material_slots])
 for sl in o.material_slots:
  m=sl.material
  for n in m.node_tree.nodes:
   if n.type in ['BSDF_PRINCIPLED','BUMP']:
    print(n.type,{i.name:list(i.default_value) if hasattr(i.default_value,'__len__') else i.default_value for i in n.inputs if hasattr(i,'default_value') and i.name in ['Base Color','Roughness','Strength','Distance','Anisotropic']})
