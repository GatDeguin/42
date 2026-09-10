"""Apply photographic CC0 oak to the loaded scene without modifying any vertex or transform.
Run on a saved candidate, optionally -- --save distinct_output.blend --export-proof.
The parent can exec this script without --save, then save its own coordinated candidate.
"""
import bpy,os,sys,json,hashlib,numpy as np,time
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..'));OUT=os.path.dirname(__file__);ASSET=os.path.join(ROOT,'docs','preview95','assets','oak-veneer-01');S=bpy.context.scene
source=bpy.data.filepath;started=time.perf_counter();derived=json.load(open(os.path.join(ASSET,'derived-provenance.json')))
materials={};images={}
def image(file,linear=False):
 if file not in images:
  im=bpy.data.images.load(os.path.join(ASSET,file),check_existing=True);im.colorspace_settings.name='Non-Color' if linear else 'sRGB';images[file]=im
 return images[file]
def photographic_material(dark,floor,uv_name):
 key=(dark,floor,uv_name)
 if key in materials:return materials[key]
 mat=bpy.data.materials.new('PHOTO95 | oak_veneer_01 | '+('dark' if dark else 'light')+(' parquet' if floor else '')+' | '+uv_name);mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;n.clear()
 out=n.new('ShaderNodeOutputMaterial');bs=n.new('ShaderNodeBsdfPrincipled');l.new(bs.outputs['BSDF'],out.inputs['Surface'])
 bs.inputs['Coat Weight'].default_value=.13;bs.inputs['Coat Roughness'].default_value=.38
 uv=n.new('ShaderNodeUVMap');uv.uv_map=uv_name
 filenames=['oak-parquet-diffuse-2k.jpg','oak-parquet-roughness-2k.png','oak-parquet-normalGL-2k.png'] if floor else ['oak-calibrated-diffuse-2k.jpg','oak_veneer_01_rough_2k.png','oak_veneer_01_nor_gl_2k.png']
 tint=derived['darkBaseFactor' if dark else 'clearBaseFactor']
 for index,file in enumerate(filenames):
  tex=n.new('ShaderNodeTexImage');tex.image=image(file,index>0);tex.extension='REPEAT';l.new(uv.outputs['UV'],tex.inputs['Vector'])
  if index==0:
   mul=n.new('ShaderNodeMix');mul.data_type='RGBA';mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[7].default_value=tint;l.new(tex.outputs['Color'],mul.inputs[6]);l.new(mul.outputs[2],bs.inputs['Base Color'])
  elif index==1:l.new(tex.outputs['Color'],bs.inputs['Roughness'])
  else:
   normal=n.new('ShaderNodeNormalMap');normal.uv_map=uv_name;normal.inputs['Strength'].default_value=.55;l.new(tex.outputs['Color'],normal.inputs['Color']);l.new(normal.outputs['Normal'],bs.inputs['Normal'])
 mat.diffuse_color=tint;mat['photographic_wood']=True;mat['asset_source']='https://polyhaven.com/a/oak_veneer_01';mat['asset_author']='Jenelle van Heerden';mat['asset_license']='CC0';mat['wood_tone']='dark' if dark else 'light';mat['wood_floor']=floor;mat['texture_size_metres']=json.dumps([1.44,2.8] if floor else [1.830000043]*2);mat['source_material_key']='woodDarkPhoto' if dark else 'woodPhoto';materials[key]=mat;return mat

def shape_hash(o):
 h=hashlib.sha256();a=np.empty(len(o.data.vertices)*3,np.float32);o.data.vertices.foreach_get('co',a);h.update(a.tobytes());a=np.empty(len(o.data.loops),np.int32);o.data.loops.foreach_get('vertex_index',a);h.update(a.tobytes());h.update(np.array(o.matrix_world,dtype=np.float64).tobytes());return h.hexdigest()
def uv_hash(layer):
 a=np.empty(len(layer.data)*2,np.float32);layer.data.foreach_get('uv',a);return hashlib.sha256(a.tobytes()).hexdigest()
rows=[]
for o in list(S.objects):
 if o.type!='MESH' or o.hide_render:continue
 slot_specs={};used_material_indices={p.material_index for p in o.data.polygons}
 for i,slot in enumerate(o.material_slots):
  mat=slot.material
  if i not in used_material_indices or not mat or mat.get('photographic_wood'):continue
  if mat.name.startswith(('Roble aceitado','Nogal mate')) or mat.get('source_material_key') in ['wood','woodDark']:
   slot_specs[i]={'old':mat.name,'dark':mat.name.startswith('Nogal') or mat.get('source_material_key')=='woodDark','floor':'parquet' in mat.name or 'piso' in o.name.lower()}
 if not slot_specs:continue
 before=shape_hash(o);previous_uv={u.name:uv_hash(u) for u in list(o.data.uv_layers)[1:]}
 o.data=o.data.copy()
 if not o.data.uv_layers:o.data.uv_layers.new(name='WoodUV')
 uv=o.data.uv_layers[0];uv.active_render=True;o.data.uv_layers.active_index=0
 coords=np.array([v.co[:] for v in o.data.vertices]);scale=np.array([o.matrix_world.to_3x3().col[i].length for i in range(3)]);coords*=scale
 extents=np.ptp(coords,axis=0);long_axis=int(np.argmax(extents));seed=hashlib.sha256(o.name.encode('utf8')).digest();offset=np.array([int.from_bytes(seed[:4],'little')/2**32,int.from_bytes(seed[4:8],'little')/2**32])
 for poly in o.data.polygons:
  spec=slot_specs.get(poly.material_index)
  if not spec:continue
  axis=0 if spec['floor'] else long_axis;other=[i for i in range(3) if i!=axis]
  if abs(poly.normal[axis])>.85:cross,along=other
  else:cross=min(other,key=lambda i:abs(poly.normal[i]));along=axis
  tile=[1.44,2.8] if spec['floor'] else [1.830000043]*2
  off=np.floor(offset*np.array([8,2]))/np.array([8,2]) if spec['floor'] else offset
  for li in poly.loop_indices:
   p=coords[o.data.loops[li].vertex_index];uv.data[li].uv=(p[cross]/tile[0]+off[0],p[along]/tile[1]+off[1])
 for i,spec in slot_specs.items():o.material_slots[i].link='DATA';o.material_slots[i].material=photographic_material(spec['dark'],spec['floor'],uv.name)
 assert shape_hash(o)==before,'Geometry/transform changed: '+o.name
 assert all(uv_hash(o.data.uv_layers[name])==h for name,h in previous_uv.items()),'Secondary UV modified: '+o.name
 o['photographic_wood_uv0']=True;o['wood_longitudinal_axis_local']=long_axis;o['wood_uv_offset']=offset.tolist()
 rows.append({'name':o.name,'vertices':len(o.data.vertices),'geometrySHA256':before,'geometryUnchanged':True,'secondaryUVUnchanged':True,'uv0':uv.name,'longitudinalAxisLocal':long_axis,'offset':offset.tolist(),'oldMaterials':list(slot_specs.values())})
assert rows,'No timber found'
S['photographic_wood_asset']='https://polyhaven.com/a/oak_veneer_01';S['photographic_wood_license']='CC0';S['photographic_wood_geometry_changed']=False
report={'source':source,'sourceSHA256':hashlib.sha256(open(source,'rb').read()).hexdigest(),'objects':rows,'objectCount':len(rows),'materialCount':len(materials),'imageCount':len(images),'seconds':time.perf_counter()-started,'geometryUnchanged':True,'secondaryUVUnchanged':True,'assetProvenance':os.path.join(ASSET,'provenance.json'),'derivedProvenance':os.path.join(ASSET,'derived-provenance.json')}
if '--save' in sys.argv:
 target=os.path.abspath(sys.argv[sys.argv.index('--save')+1]);assert target!=os.path.abspath(source),'Never overwrite the source'
 bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=target,compress=True);report['output']=target;report['outputSHA256']=hashlib.sha256(open(target,'rb').read()).hexdigest()
if '--export-proof' in sys.argv:
 for o in S.objects:o.select_set(False)
 for row in rows:bpy.data.objects[row['name']].select_set(True)
 bpy.context.view_layer.objects.active=bpy.data.objects[rows[0]['name']]
 bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,'wood-proof.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_apply=True,export_yup=True,export_animations=False,export_cameras=False,export_lights=False,export_extras=True,export_materials='EXPORT',export_image_format='AUTO',export_texcoords=True,export_normals=True)
with open(os.path.join(OUT,'application-report.json'),'w',encoding='utf8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
print('PHOTO95_WOOD_APPLIED',len(rows),len(materials),report.get('output'),flush=True)
