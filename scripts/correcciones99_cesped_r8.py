"""R8 lawn: replace only the 73 existing grass meshes and the lawn-surface material only. No save or render in apply()."""
import bpy,json,math,hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1];ASSET=ROOT/'source/assets/grass_bermuda_01'
TAG='photographic_grass_r8_v2';PFX='GRASS8 | '
TREES=np.array([[2,11.7],[4.3,16.8],[8.2,13.55],[9.85,17.85],[9.2,4.4],[1.95,17.2]])
NAMES=['small_'+x for x in 'abcdef']+['medium_'+x for x in 'abcdef']+['dead_a','dead_b','flattened_a','seedling_c']
WEIGHTS=np.array([.12,.16,.01,.16,.13,.10,.015,.12,.015,.10,.005,.015,.005,.005,.03,.01])
def bbox(o):
 p=[o.matrix_world@Vector(v) for v in o.bound_box]
 return [[min(v[k] for v in p),max(v[k] for v in p)] for k in range(3)]
def ground_tree():
 vv=[];ff=[]
 for name in ['Césped del lote','Entorno exterior','Entorno | terreno continuo']:
  o=bpy.data.objects[name];e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();base=len(vv)
  vv.extend([o.matrix_world@v.co for v in m.vertices]);ff.extend([[base+i for i in p.vertices] for p in m.polygons]);e.to_mesh_clear()
 return BVHTree.FromPolygons(vv,ff,all_triangles=False)
def ground_at(tree,x,y):
 p,n,i,d=tree.ray_cast(Vector((float(x),float(y),10)),Vector((0,0,-1)),20)
 if p is None:raise ValueError('No source ground under grass '+str((x,y)))
 return p.z
def exclusion_boxes():
 return [bbox(o) for o in bpy.context.scene.objects if o.name.startswith('Banco huerta | loseta hormigón P')]
def permitted(x,z,r,kind,pads):
 inside=0<x<22 and 0<z<20
 if kind=='lawn' or inside:
  if not (.2+r<x<21.8-r and .2+r<z<19.8-r):return False
  if x>12.8-r and z<13.15+r:return False
  if 11.96-r<x<21.04+r and 13.96-r<z<19.04+r:return False
  if 1.8-r<x<8.7+r and 3.48-r<z<8.02+r:return False
  if any((x-tx)**2+(z-tz)**2<(.47+r)**2 for tx,tz in TREES):return False
  if kind=='meadow' and (x>10.8-r or z<1.2+r or (x<3.5+r and z>12-r)):return False
 else:
  if not (-18+r<x<37-r and -7+r<z<35-r):return False
  if -3-r<z<0+r or (10.6-r<x<14.3+r and z<12.5+r):return False
 for bb in pads:
  if bb[0][0]-.007-r<x<bb[0][1]+.007+r and bb[1][0]-.007-r<-z<bb[1][1]+.007+r:return False
 return True
def photographic_material():
 m=bpy.data.materials.new(PFX+'Bermuda CC0 alpha mask');m.use_nodes=True
 n=m.node_tree.nodes;l=m.node_tree.links;bs=next(q for q in n if q.type=='BSDF_PRINCIPLED')
 bs.inputs['Roughness'].default_value=.76;bs.inputs['Metallic'].default_value=0
 m.use_backface_culling=False;m['photographic99']=True;m['grass8']=True
 m['asset']='grass_bermuda_01';m['license']='CC0';m['asset_url']='https://polyhaven.com/a/grass_bermuda_01';m['author']='Rico Cilliers';m['uv_space']='Photographic asset atlas, preserved UV0';m['alpha_mode']='MASK';m['alpha_cutoff']=.5
 paths={'diff':'grass_bermuda_01_diff_2k.jpg','alpha':'grass_bermuda_01_alpha_2k.png','normal':'bermuda_source_normal_2k.png','rough':'bermuda_source_rough_2k.png'}
 uv=n.new('ShaderNodeUVMap');uv.uv_map='UVMap'
 for key,fn in paths.items():
  path=(ROOT/'source/photographic99_grass_r8'/fn) if key in ['normal','rough'] else ASSET/'textures'/fn
  im=bpy.data.images.load(str(path),check_existing=True);im.colorspace_settings.name='sRGB' if key=='diff' else 'Non-Color';im.pack()
  t=n.new('ShaderNodeTexImage');t.image=im;t.interpolation='Linear';l.new(uv.outputs['UV'],t.inputs['Vector'])
  if key=='diff':l.new(t.outputs['Color'],bs.inputs['Base Color'])
  elif key=='rough':l.new(t.outputs['Color'],bs.inputs['Roughness'])
  elif key=='normal':
   normal=n.new('ShaderNodeNormalMap');normal.uv_map='UVMap';normal.inputs['Strength'].default_value=.65;l.new(t.outputs['Color'],normal.inputs['Color']);l.new(normal.outputs['Normal'],bs.inputs['Normal'])
  else:
   clip=n.new('ShaderNodeMath');clip.operation='ROUND';l.new(t.outputs['Color'],clip.inputs[0]);l.new(clip.outputs[0],bs.inputs['Alpha'])
 return m
def ground_material():
 manifest=json.loads((ROOT/'source/photographic99_grass_r8/atlas_manifest.json').read_text(encoding='utf-8'))
 for name,info in manifest['files'].items():
  assert hashlib.sha256((ROOT/'source/photographic99_grass_r8'/name).read_bytes()).hexdigest()==info['sha256'],name
 o=bpy.data.objects['Césped del lote'];me=o.data
 # Preserve source point colors in the derivative atlas; no double tint in glTF.
 for a in list(me.color_attributes):me.color_attributes.remove(a)
 uv=me.uv_layers.active or me.uv_layers.new(name='UVMap');uv.name='UVMap';uv.active_render=True
 for p in me.polygons:
  for li in p.loop_indices:
   v=o.matrix_world@me.vertices[me.loops[li].vertex_index].co
   uv.data[li].uv=(v.x/22,1+v.y/20)
 m=bpy.data.materials.new(PFX+'Lote césped y tierra CC0');m.use_nodes=True
 n=m.node_tree.nodes;l=m.node_tree.links;bs=next(q for q in n if q.type=='BSDF_PRINCIPLED')
 m['photographic99']=True;m['grass8']=True;m['license']='CC0';m['asset_url']='https://polyhaven.com/a/grass_bermuda_01'
 m['uv_space']='Unique lot atlas: U=world X/22 m, V=1+world Y/20 m. Original source mask; grass texture repeat 2 m.'
 m['source_substrate']='Original Poly Haven leafy_grass, Charlotte Baglioni, CC0; retained outside grass mask.'
 u=n.new('ShaderNodeUVMap');u.uv_map='UVMap'
 for kind,fn in [('color','lot_color.jpg'),('normal','lot_normal.png'),('rough','lot_rough.png')]:
  im=bpy.data.images.load(str(ROOT/'source/photographic99_grass_r8'/fn),check_existing=True);im.colorspace_settings.name='sRGB' if kind=='color' else 'Non-Color';im.pack()
  t=n.new('ShaderNodeTexImage');t.image=im;t.interpolation='Linear';t.extension='EXTEND';l.new(u.outputs['UV'],t.inputs['Vector'])
  if kind=='normal':
   nm=n.new('ShaderNodeNormalMap');nm.uv_map='UVMap';nm.inputs['Strength'].default_value=.65;l.new(t.outputs['Color'],nm.inputs['Color']);l.new(nm.outputs['Normal'],bs.inputs['Normal'])
  else:l.new(t.outputs['Color'],bs.inputs['Base Color' if kind=='color' else 'Roughness'])
 me.materials.clear();me.materials.append(m);o['grass8_ground_atlas']=True
 return manifest

def library():
 path=ASSET/'grass_bermuda_01_2k.blend'
 assert hashlib.sha256(path.read_bytes()).hexdigest()=='3b2ec52390d293b9e810ec4e2a182d725ed2a858eb0912f5bb36909d9c5f5073'
 with bpy.data.libraries.load(str(path),link=False) as (src,dst):dst.objects=['grass_bermuda_01_'+x for x in NAMES]
 data=[]
 for name,o in zip(NAMES,dst.objects):
  assert o and not o.modifiers
  me=o.data;v=np.empty(len(me.vertices)*3,dtype=np.float32);me.vertices.foreach_get('co',v);v=v.reshape(-1,3);v[:,2]-=v[:,2].min()
  loops=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',loops)
  counts=np.empty(len(me.polygons),np.int32);me.polygons.foreach_get('loop_total',counts)
  smooth=np.empty(len(me.polygons),np.bool_);me.polygons.foreach_get('use_smooth',smooth)
  uv=np.empty(len(me.loops)*2,np.float32);me.uv_layers.active.data.foreach_get('uv',uv)
  data.append({'name':name,'v':v,'loops':loops,'counts':counts,'smooth':smooth,'uv':uv.reshape(-1,2),'height':float(v[:,2].max()),'radius':float(np.linalg.norm(v[:,:2],axis=1).max()),'custom_normals':me.has_custom_normals})
  bpy.data.objects.remove(o,do_unlink=True)
  if me.users==0:bpy.data.meshes.remove(me)
 return data
def roots(o):
 p=np.empty(len(o.data.vertices)*3,np.float32);o.data.vertices.foreach_get('co',p);p=p.reshape(-1,3)
 M=np.array(o.matrix_world,dtype=np.float64);p=p@M[:3,:3].T+M[:3,3]
 if o.name.startswith('Césped botánico '):
  assert len(p)%5==0
  # The previous mesh stores each connected blade in five consecutive vertices.
  for f in o.data.polygons:
   assert len({i//5 for i in f.vertices})==1
  return (p.reshape(-1,5,3)[:,0,:]+p.reshape(-1,5,3)[:,1,:])/2,'lawn'
 assert len(p)%3==0
 base=(p.reshape(-1,3,3)[:,0,:]+p.reshape(-1,3,3)[:,1,:])/2
 _,idx=np.unique(np.round(base[:,:2],3),axis=0,return_index=True)
 return base[np.sort(idx)],'meadow'
def apply():
 S=bpy.context.scene
 if S.get(TAG):
  rep=json.loads(S[TAG]);assert all(bpy.data.objects[n].get(TAG) for n in rep['replaced']);return rep
 targets=sorted([o for o in S.objects if o.type=='MESH' and not o.hide_render and (o.name.startswith('Césped botánico ') or o.name=='Paisaje | pradera de transición')],key=lambda o:o.name)
 assert len(targets)==73,len(targets)
 ground_report=ground_material();asset=library();mat=photographic_material();tree=ground_tree();pads=exclusion_boxes();assert len(pads)==4
 rng=np.random.default_rng(820991)
 rep={'version':TAG,'source_file':bpy.data.filepath,'asset_sha256':'3b2ec52390d293b9e810ec4e2a182d725ed2a858eb0912f5bb36909d9c5f5073','asset':'Poly Haven grass_bermuda_01, CC0, Rico Cilliers','replaced':[o.name for o in targets],'objects':[],'root_embedding_m':.0007,'geometry_decimation':False,'alpha':'Physical photographic cutout, Math ROUND -> glTF MASK 0.5; no procedural dither','variants':[{k:v for k,v in a.items() if k in ['name','height','radius','custom_normals']} for a in asset]}
 for oi,o in enumerate(targets):
  old=o.data;base,kind=roots(o);nb=len(base)
  if kind=='lawn':base=base[np.sort(rng.choice(nb,int(nb*.40),replace=False))]
  vs=[];loops=[];counts=[];uvs=[];smooth=[];anchor=[];used={a['name']:0 for a in asset};rejected=0;offset=0;heights=[]
  for p in base:
   a=asset[int(rng.choice(len(asset),p=WEIGHTS))]
   scale=float(rng.uniform(.78,1.16));scale=min(scale,(.09 if kind=='lawn' else .12)/a['height'])
   radius=a['radius']*scale;x,y=p[:2];z=-y
   if not permitted(x,z,radius,kind,pads):rejected+=1;continue
   angle=float(rng.uniform(0,math.tau));ca,sa=math.cos(angle),math.sin(angle)
   v=a['v'].astype(np.float64)*scale
   xy=v[:,:2]@np.array([[ca,sa],[-sa,ca]])+p[:2]
   soil=np.array([ground_at(tree,q[0],q[1]) for q in xy])
   world=np.column_stack((xy,soil+v[:,2]-.0007))
   inv=np.array(o.matrix_world.inverted(),dtype=np.float64);local=world@inv[:3,:3].T+inv[:3,3]
   vs.append(local.astype(np.float32));loops.append(a['loops']+offset);counts.append(a['counts']);uvs.append(a['uv']);smooth.append(a['smooth']);offset+=len(v)
   anchor.append([float(x),float(y),ground_at(tree,x,y),radius,scale,a['name']]);used[a['name']]+=1;heights.append(float(v[:,2].max()))
  me=bpy.data.meshes.new(PFX+o.name);v=np.concatenate(vs);li=np.concatenate(loops);ct=np.concatenate(counts)
  me.vertices.add(len(v));me.vertices.foreach_set('co',v.reshape(-1));me.loops.add(len(li));me.loops.foreach_set('vertex_index',li);me.polygons.add(len(ct));me.polygons.foreach_set('loop_start',np.cumsum(np.r_[0,ct[:-1]]));me.polygons.foreach_set('loop_total',ct);me.polygons.foreach_set('use_smooth',np.concatenate(smooth));me.update()
  uv=me.uv_layers.new(name='UVMap');uv.data.foreach_set('uv',np.concatenate(uvs).reshape(-1));uv.active_render=True;me.materials.append(mat)
  previous=len(old.vertices);o.data=me;o[TAG]=True;o['grass8_source_asset']='grass_bermuda_01';o['grass8_preserve_faces_on_export']=True
  if old.users==0:bpy.data.meshes.remove(old)
  row={'name':o.name,'kind':kind,'original_roots':nb,'candidate_roots':len(base),'accepted_clumps':len(anchor),'rejected_at_exclusions':rejected,'vertices_before':previous,'vertices_after':len(v),'polygons_after':len(ct),'triangles_after':int(np.sum(ct-2)),'height_range_m':[min(heights),max(heights)],'variants':used,'anchors':anchor}
  rep['objects'].append(row)
  if oi%12==0:print('GRASS8_SECTOR',oi+1,'of',len(targets),'vertices',len(v),'clumps',len(anchor),flush=True)
 rep['ground_atlas']=ground_report
 rep['total_vertices_before']=sum(q['vertices_before'] for q in rep['objects']);rep['total_vertices_after']=sum(q['vertices_after'] for q in rep['objects']);rep['total_triangles_after']=sum(q['triangles_after'] for q in rep['objects']);rep['total_clumps']=sum(q['accepted_clumps'] for q in rep['objects'])
 assert rep['total_vertices_after']<2000000
 # Detailed anchors are kept on each replaced mesh object, not multiplied across four scene reports.
 for row in rep['objects']:
  bpy.data.objects[row['name']]['grass8_anchors']=json.dumps(row.pop('anchors'),separators=(',',':'))
 rep['scenes']=[s.name for s in bpy.data.scenes if all(n in s.objects for n in rep['replaced'])]
 for sc in bpy.data.scenes:
  if sc.name in rep['scenes']:sc[TAG]=json.dumps(rep,ensure_ascii=False)
 bpy.context.view_layer.update();return rep
