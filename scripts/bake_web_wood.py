import bpy,os,json
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'docs','assets','textures')
source=bpy.context.scene
assignments={}
for o in source.objects:
 if o.type!='MESH':continue
 for slot in o.material_slots:
  m=slot.material
  if m and m.name.startswith(('Roble aceitado','Nogal mate')):
   tail=m.name.split('|')[1].strip()
   assignments[o.name]={'wood':'oak' if m.name.startswith('Roble') else 'walnut','axis':int(tail[0]),'floor':'parquet' in tail}
json.dump(assignments,open(os.path.join(OUT,'wood-surfaces.json'),'w',encoding='utf8'),ensure_ascii=False)
scene=bpy.data.scenes.new('Web material bake only');bpy.context.window.scene=scene
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=1
anchor=bpy.data.objects['Material coordinates | metres / world'];scene.collection.objects.link(anchor)
for name,source_name,floor in [('oak','Roble aceitado | 2 veta',False),('walnut','Nogal mate | 2 veta',False),('parquet','Roble aceitado | 0 parquet',True)]:
 material=bpy.data.materials[source_name].copy()
 n=material.node_tree.nodes;l=material.node_tree.links
 bs=next(nod for nod in n if nod.type=='BSDF_PRINCIPLED')
 color=bs.inputs['Base Color'].links[0].from_socket
 output=next(nod for nod in n if nod.type=='OUTPUT_MATERIAL')
 for link in list(output.inputs['Surface'].links):l.remove(link)
 emission=n.new('ShaderNodeEmission');l.new(color,emission.inputs['Color']);l.new(emission.outputs[0],output.inputs['Surface'])
 image=bpy.data.images.new('Web bake '+name,width=1024,height=1024,alpha=False);image.colorspace_settings.name='sRGB'
 tex=n.new('ShaderNodeTexImage');tex.image=image
 for nod in n:nod.select=False
 tex.select=True;n.active=tex
 w,h=(2.8,1.44) if floor else (1.4,1.4)
 vertices=[(0,0,0),(w,0,0),(w,h,0),(0,h,0)] if floor else [(0,0,0),(w,0,0),(w,0,h),(0,0,h)]
 mesh=bpy.data.meshes.new('Bake plane');mesh.from_pydata(vertices,[],[(0,1,2,3)]);mesh.materials.append(material)
 uv=mesh.uv_layers.new(name='UVMap')
 for i,co in enumerate([(0,0),(1,0),(1,1),(0,1)]):uv.data[i].uv=co
 obj=bpy.data.objects.new('Material sample '+name,mesh);scene.collection.objects.link(obj)
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 bpy.ops.object.bake(type='EMIT',margin=0,use_clear=True)
 image.filepath_raw=os.path.join(OUT,name+'_albedo.png');image.file_format='PNG';image.save()
 bpy.data.objects.remove(obj,do_unlink=True)
 print('BAKED',name,flush=True)
print('WEB_WOOD_BAKE_COMPLETE',len(assignments),flush=True)
