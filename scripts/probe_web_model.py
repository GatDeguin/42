import bpy,json,os
S=bpy.context.scene
rows=[]
for c in S.collection.children:
 obs=[o for o in c.all_objects if o.type=='MESH' and not o.hide_render]
 rows.append({'collection':c.name,'objects':len(obs),'vertices':sum(len(o.data.vertices) for o in obs),'polygons':sum(len(o.data.polygons) for o in obs)})
print(json.dumps(rows))
print('EXPORTER',[(p.identifier,p.default if p.type!='ENUM' else str(p.default)) for p in bpy.ops.export_scene.gltf.get_rna_type().properties if p.identifier in ['export_draco_mesh_compression_enable','export_gpu_instances','export_yup','export_apply','export_materials','use_selection','use_visible','export_cameras','export_extras','export_animations']])
