"""R8 photographic upholstery, same mean linear colour and unchanged furniture geometry."""
from pathlib import Path
import bpy,numpy as np,hashlib,json
R=Path(__file__).resolve().parents[1];NAME='UPH99 | Tejido tapizado fotográfico';UV='UPH99_UV';TILE=[.2657081476760712,.2662999927997589]
# Mean linear RGB of source fabric_albedo and CC0 Terlenka diffuse, measured without modifying either image.
OLD_MEAN=np.array([.24723730558865356,.21749501909852093,.15854020677115394]);PHOTO_MEAN=np.array([.5622147949416687,.42960513517215204,.32259202417152577]);TINT=OLD_MEAN/PHOTO_MEAN

def shape(o):
 m=o.data;v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);i=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',i)
 return hashlib.sha256(v.tobytes()+i.tobytes()+np.array(o.matrix_world,dtype=np.float64).tobytes()).hexdigest()
def material():
 old=bpy.data.materials.get(NAME)
 if old:return old
 m=bpy.data.materials.new(NAME);m.use_nodes=True;ns=m.node_tree.nodes;ls=m.node_tree.links;ns.clear();out=ns.new('ShaderNodeOutputMaterial');bs=ns.new('ShaderNodeBsdfPrincipled');ls.new(bs.outputs['BSDF'],out.inputs['Surface']);bs.inputs['Roughness'].default_value=.82;bs.inputs['Sheen Weight'].default_value=.30;bs.inputs['Sheen Roughness'].default_value=.65
 uv=ns.new('ShaderNodeUVMap');uv.uv_map=UV
 for channel,file in [('color','terlenka_diff_2k.png'),('normal','terlenka_nor_gl_2k.png'),('rough','terlenka_rough_2k.png')]:
  tex=ns.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(R/'source/assets/terlenka'/file),check_existing=True);tex.image.colorspace_settings.name='sRGB' if channel=='color' else 'Non-Color';ls.new(uv.outputs['UV'],tex.inputs['Vector'])
  if channel=='color':
   mix=ns.new('ShaderNodeMix');mix.data_type='RGBA';mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[7].default_value=(*TINT,1);ls.new(tex.outputs['Color'],mix.inputs[6]);ls.new(mix.outputs[2],bs.inputs['Base Color'])
  elif channel=='normal':
   nm=ns.new('ShaderNodeNormalMap');nm.uv_map=UV;nm.inputs['Strength'].default_value=.18;ls.new(tex.outputs['Color'],nm.inputs['Color']);ls.new(nm.outputs['Normal'],bs.inputs['Normal'])
  else:
   # Preserve the measured photographic roughness directly for matching glTF export.
   ls.new(tex.outputs['Color'],bs.inputs['Roughness'])
 m.diffuse_color=(*OLD_MEAN,1);m['photographic99']=True;m['source_asset']='https://polyhaven.com/a/terlenka';m['asset_license']='CC0';m['texture_module_m']=TILE;m['linear_mean_colour_preserved']=True;m['source_material_key']='fabricPhotographic';return m

def apply():
 rows=[];mat=material()
 for o in list(bpy.context.scene.objects):
  if o.type!='MESH' or o.hide_render:continue
  slots=[i for i,m in enumerate(o.data.materials) if m and m.name=='Textil | fabric']
  if not slots:continue
  old=shape(o)
  if o.data.users>1:o.data=o.data.copy()
  m=o.data;uv=m.uv_layers.get(UV) or m.uv_layers.new(name=UV);coords=np.array([v.co[:] for v in m.vertices]);coords*=np.array([o.matrix_world.to_3x3().col[i].length for i in range(3)])
  for poly in m.polygons:
   if poly.material_index not in slots:continue
   axis=max(range(3),key=lambda i:abs(poly.normal[i]));cross,along=[i for i in range(3) if i!=axis]
   for li in poly.loop_indices:
    p=coords[m.loops[li].vertex_index];uv.data[li].uv=(p[cross]/TILE[0],p[along]/TILE[1])
  for i in slots:m.materials[i]=mat
  m.update();assert shape(o)==old,o.name
  o['revision99_r8_upholstery']='Photographic measured weave; original mean colour and physical geometry preserved'
  rows.append(dict(object=o.name,slots=slots,geometryUnchanged=True,geometrySHA256=old))
 return dict(objects=rows,objectCount=len(rows),textureModuleM=TILE,originalMeanLinearRGB=OLD_MEAN.tolist(),photoMeanLinearRGB=PHOTO_MEAN.tolist(),tintFactor=TINT.tolist(),scope='Visible furniture with original fabric material only; geometry and placements unchanged',videoRendered=False)
if __name__=='__main__':
 report=apply();assert apply()['objectCount']==0
 out=R/'review99/r8_visual';out.mkdir(exist_ok=True);(out/'upholstery_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print('UPHOLSTERY_PASS',report['objectCount'],flush=True)
