"""Experimental photo masonry only. Never auto-integrate; compare same-camera stills first.
Execute against a loaded source; optional --save distinct_copy.blend. Geometry and secondary UV remain exact.
"""
import bpy,os,sys,json,hashlib,numpy as np
from mathutils import Vector
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..'));OUT=os.path.dirname(__file__);ASSET=os.path.join(ROOT,'docs','preview95','assets','red-bricks-04');S=bpy.context.scene;source=bpy.data.filepath
images={};materials={};rows=[];tile=np.array(json.load(open(ASSET+'/info.json'))['dimensions'],float)/1000
assert np.max(np.abs(tile-2.5))<1e-8

def image(file,linear):
 if file not in images:
  im=bpy.data.images.load(ASSET+'/'+file,check_existing=True);im.colorspace_settings.name='Non-Color' if linear else 'sRGB';images[file]=im
 return images[file]
def photographic_material(dark,uv_name):
 key=(dark,uv_name)
 if key in materials:return materials[key]
 mat=bpy.data.materials.new('PHOTO95 | red_bricks_04 | '+('brickDarkPhoto' if dark else 'brickPhoto')+' | '+uv_name);mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;n.clear();out=n.new('ShaderNodeOutputMaterial');bs=n.new('ShaderNodeBsdfPrincipled');l.new(bs.outputs['BSDF'],out.inputs['Surface']);bs.inputs['Metallic'].default_value=0;bs.inputs['Coat Weight'].default_value=0
 uv=n.new('ShaderNodeUVMap');uv.uv_map=uv_name;tint=(.8,.78,.73,1) if dark else (1,1,1,1)
 for role,file,target in [('diff','red_bricks_04_diff_2k.png','Base Color'),('rough','red_bricks_04_rough_2k.png','Roughness'),('normal','red_bricks_04_nor_gl_2k.png','Normal')]:
  tex=n.new('ShaderNodeTexImage');tex.image=image(file,role!='diff');tex.extension='REPEAT';l.new(uv.outputs['UV'],tex.inputs['Vector'])
  if role=='normal':
   node=n.new('ShaderNodeNormalMap');node.uv_map=uv_name;node.inputs['Strength'].default_value=.65;l.new(tex.outputs['Color'],node.inputs['Color']);l.new(node.outputs['Normal'],bs.inputs['Normal'])
  elif role=='diff':
   node=n.new('ShaderNodeMix');node.data_type='RGBA';node.blend_type='MULTIPLY';node.inputs[0].default_value=1;node.inputs[7].default_value=tint;l.new(tex.outputs['Color'],node.inputs[6]);l.new(node.outputs[2],bs.inputs['Base Color'])
  else:l.new(tex.outputs['Color'],bs.inputs[target])
 mat.diffuse_color=tint;mat['photographic_masonry']=True;mat['source_material_key']='brickDarkPhoto' if dark else 'brickPhoto';mat['asset_source']='https://polyhaven.com/a/red_bricks_04';mat['asset_author']='Rob Tuytel';mat['asset_license']='CC0';mat['tile_metres']=2.5;mat['review_status']='EXPERIMENTAL';materials[key]=mat;return mat

def shape_hash(o):
 h=hashlib.sha256();a=np.empty(len(o.data.vertices)*3,np.float32);o.data.vertices.foreach_get('co',a);h.update(a.tobytes());a=np.empty(len(o.data.loops),np.int32);o.data.loops.foreach_get('vertex_index',a);h.update(a.tobytes());h.update(np.array(o.matrix_world,dtype=np.float64).tobytes());return h.hexdigest()
def uv_hash(layer):
 a=np.empty(len(layer.data)*2,np.float32);layer.data.foreach_get('uv',a);return hashlib.sha256(a.tobytes()).hexdigest()
wood_before={o.name:(shape_hash(o),[uv_hash(u) for u in o.data.uv_layers],[s.material.name if s.material else None for s in o.material_slots]) for o in S.objects if o.type=='MESH' and any(s.material and s.material.get('photographic_wood') for s in o.material_slots)}
for o in list(S.objects):
 if o.type!='MESH' or o.hide_render:continue
 used={p.material_index for p in o.data.polygons};slots={i:s.material for i,s in enumerate(o.material_slots) if i in used and s.material and s.material.get('source_material_key') in ['brick','brickDark']}
 if not slots:continue
 before=shape_hash(o);secondary={u.name:uv_hash(u) for u in list(o.data.uv_layers)[1:]};o.data=o.data.copy()
 if not o.data.uv_layers:o.data.uv_layers.new(name='MasonryUV')
 uv=o.data.uv_layers[0];uv.active_render=True;o.data.uv_layers.active_index=0;coords=[o.matrix_world@v.co for v in o.data.vertices];normal_matrix=o.matrix_world.to_3x3().inverted().transposed();mapped=[]
 for poly in o.data.polygons:
  if poly.material_index not in slots:continue
  normal=(normal_matrix@poly.normal).normalized();horizontal=abs(normal.z)>.85;tangent=Vector((-normal.y,normal.x,0))
  if tangent.length>1e-8:tangent.normalize()
  if tangent.x<0 or (abs(tangent.x)<1e-8 and tangent.y<0):tangent.negate()
  axis_aligned=max(abs(normal.x),abs(normal.y))>.999
  for li in poly.loop_indices:
   p=coords[o.data.loops[li].vertex_index]
   if horizontal:value=(p.x/tile[0],p.y/tile[1])
   else:value=((p.x+p.y if axis_aligned else p.dot(tangent))/tile[0],p.z/tile[1])
   uv.data[li].uv=value;mapped.append(li)
 for i,old in slots.items():o.material_slots[i].link='DATA';o.material_slots[i].material=photographic_material(old.get('source_material_key')=='brickDark',uv.name)
 assert shape_hash(o)==before,'Geometry changed: '+o.name
 assert all(uv_hash(o.data.uv_layers[k])==v for k,v in secondary.items()),'Secondary UV changed: '+o.name
 o['photographic_masonry_uv0']=True;o['masonry_world_phase']='Vertical walls V=world Z/2.5; cardinal faces U=(world X+world Y)/2.5; diagonal faces metric world tangent. Horizontal surfaces XY/2.5.'
 rows.append(dict(name=o.name,vertices=len(o.data.vertices),geometrySHA256=before,geometryUnchanged=True,secondaryUVUnchanged=True,uv0=uv.name,mappedLoops=len(mapped),originalMaterials=[m.name for m in slots.values()]))
assert rows,'No source brick materials found'
assert wood_before=={o.name:(shape_hash(o),[uv_hash(u) for u in o.data.uv_layers],[s.material.name if s.material else None for s in o.material_slots]) for o in S.objects if o.type=='MESH' and any(s.material and s.material.get('photographic_wood') for s in o.material_slots)},'Photographic wood changed'
report=dict(status='EXPERIMENTAL; requires visual comparison before integration',source=source,sourceSHA256=hashlib.sha256(open(source,'rb').read()).hexdigest(),objects=rows,objectCount=len(rows),materialCount=len(materials),woodObjectsUntouched=len(wood_before),tileMetres=tile.tolist(),normalStrength=.65,darkBaseFactor=[.8,.78,.73,1],provenance=ASSET+'/provenance.json',geometryUnchanged=True,secondaryUVUnchanged=True)
if '--save' in sys.argv:
 target=os.path.abspath(sys.argv[sys.argv.index('--save')+1]);assert target!=os.path.abspath(source);bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=target,compress=True);report['output']=target;report['outputSHA256']=hashlib.sha256(open(target,'rb').read()).hexdigest()
json.dump(report,open(OUT+'/application-report.json','w',encoding='utf8'),ensure_ascii=False,indent=2);print('EXPERIMENTAL_PHOTO_BRICK',len(rows),'objects; wood untouched',len(wood_before),flush=True)
