"""Read-only CPU comparison: integrated grass against its verified source component."""
import bpy,hashlib,json,sys,runpy,numpy as np,time
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'review99/r8_integrated';O.mkdir(parents=True,exist_ok=True)
FINAL=R/'output/Casa_de_Campo_99_R8.blend';EXPECTED='60810e1945f53b339c070c6e77635f408b99c244fc07f43a5084ebeecdde5329'
REF=R/'output/Casa_de_Campo_99_R8_cesped_preview.blend';REF_SHA='ff504115cb562a1031865cef8cd0e93f2ecf737b8a5d75571cb51170bef28452'
TAG='photographic_grass_r8_v2';A=runpy.run_path(str(R/'scripts/correcciones99_cesped_r8.py'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert Path(bpy.data.filepath)==FINAL and sha(FINAL)==EXPECTED
t=time.time()
def digest(arr):return hashlib.sha256(arr.tobytes()).hexdigest()
def prop_array(items,key,size,dtype):
 a=np.empty(len(items)*size,dtype);items.foreach_get(key,a);return a
def value(x):
 if isinstance(x,(str,int,float,bool)) or x is None:return x
 try:return list(x)
 except:return str(x)
def material(m):
 nodes=[]
 for n in m.node_tree.nodes:
  d={'name':n.name,'type':n.bl_idname,'inputs':{i.identifier:value(i.default_value) for i in n.inputs if hasattr(i,'default_value')}}
  for key in ['operation','uv_map','interpolation','extension','blend_type']:
   if hasattr(n,key):d[key]=getattr(n,key)
  if n.type=='TEX_IMAGE' and n.image:
   im=n.image;p=Path(bpy.path.abspath(im.filepath));packed=bytes(im.packed_file.data) if im.packed_file else None
   d['image']={'file':p.name,'colorspace':im.colorspace_settings.name,'packed_sha256':hashlib.sha256(packed).hexdigest() if packed else None,'file_sha256':sha(p) if p.exists() else None,'size':list(im.size)}
  nodes.append(d)
 return {'name':m.name,'nodes':nodes,'links':sorted((l.from_node.name,l.from_socket.identifier,l.to_node.name,l.to_socket.identifier) for l in m.node_tree.links),'double_sided':not m.use_backface_culling}
def mesh(o):
 m=o.data
 return {'name':o.name,'vertices':len(m.vertices),'polygons':len(m.polygons),'triangles':sum(len(p.vertices)-2 for p in m.polygons),'positions_sha':digest(prop_array(m.vertices,'co',3,np.float32)),'indices_sha':digest(prop_array(m.loops,'vertex_index',1,np.int32)),'polygon_counts_sha':digest(prop_array(m.polygons,'loop_total',1,np.int32)),'smooth_sha':digest(prop_array(m.polygons,'use_smooth',1,np.bool_)),'world_matrix_sha':digest(np.array(o.matrix_world,dtype=np.float32)),'uv':[{'name':u.name,'sha':digest(prop_array(u.data,'uv',2,np.float32)),'active_render':u.active_render,'finite':bool(np.isfinite(prop_array(u.data,'uv',2,np.float32)).all())} for u in m.uv_layers],'material_names':[m.name if m else None for m in m.materials],'hide_render':o.hide_render,'anchor_sha':hashlib.sha256(o.get('grass8_anchors','').encode()).hexdigest(),'export_preserve':bool(o.get('grass8_preserve_faces_on_export')),'colors':[(c.name,c.domain,c.data_type) for c in m.color_attributes]}
def capture():
 grass=sorted([o for o in bpy.data.objects if o.type=='MESH' and o.get(TAG)],key=lambda o:o.name)
 surfaces=[bpy.data.objects[n] for n in ['Césped del lote','Entorno exterior','Entorno | terreno continuo']]
 mats={m.name:m for o in grass+[surfaces[0]] for m in o.data.materials if m}
 result={'grass':{o.name:mesh(o) for o in grass},'surfaces':{o.name:mesh(o) for o in surfaces},'materials':{n:material(m) for n,m in mats.items()},'scenes':{},'resource_manifest':json.loads((R/'source/photographic99_grass_r8/atlas_manifest.json').read_text(encoding='utf-8'))}
 for s in bpy.data.scenes:
  p=json.loads(s.get(TAG,'{}'))
  result['scenes'][s.name]={'grass_present':sum(o.name in s.objects for o in grass),'ground_present':'Césped del lote' in s.objects,'marked':bool(s.get(TAG)),'atlas':p.get('ground_atlas',{}).get('files',{})}
 return result
final=capture()
tree=A['ground_tree']();pads=A['exclusion_boxes']();root_errors=[];roots=0
for name in final['grass']:
 o=bpy.data.objects[name];kind='meadow' if name=='Paisaje | pradera de transición' else 'lawn'
 for x,y,h,r,scale,var in json.loads(o['grass8_anchors']):
  roots+=1;actual=A['ground_at'](tree,x,y)
  if abs(actual-h)>1e-6 or not A['permitted'](x,-y,r,kind,pads):root_errors.append({'name':name,'anchor':[x,y,h,r],'ground_now':actual})
assert sha(REF)==REF_SHA
bpy.ops.wm.open_mainfile(filepath=str(REF),use_scripts=False)
ref=capture()
def differences(a,b,path=''):
 z=[]
 if type(a)!=type(b):return [path]
 if isinstance(a,dict):
  for k in a.keys()|b.keys():
   if k not in a or k not in b:z.append(path+'/'+str(k))
   else:z+=differences(a[k],b[k],path+'/'+str(k))
 elif isinstance(a,list):
  if len(a)!=len(b):z.append(path+'/length')
  for i,(x,y) in enumerate(zip(a,b)):z+=differences(x,y,path+'/'+str(i))
 elif a!=b:z.append(path)
 return z
delta=differences(final,ref)
resource_errors=[]
for name,m in final['materials'].items():
 for n in m['nodes']:
  im=n.get('image')
  if im and (not im['packed_sha256'] or im['packed_sha256']!=im['file_sha256']):resource_errors.append([name,im])
report={'source':str(FINAL),'source_sha256':EXPECTED,'reference':str(REF),'reference_sha256':REF_SHA,'source_unchanged':sha(FINAL)==EXPECTED,'reference_unchanged':sha(REF)==REF_SHA,'mode':'read-only CPU; no apply(), no save(), no render, no GPU','max_threads':4,'grass_objects':len(final['grass']),'vertices':sum(q['vertices'] for q in final['grass'].values()),'triangles':sum(q['triangles'] for q in final['grass'].values()),'component_differences':delta,'anchors_checked':roots,'root_errors':root_errors,'resource_errors':resource_errors,'scenes':final['scenes'],'material_names':list(final['materials']),'ground':final['surfaces']['Césped del lote'],'seconds':time.time()-t,'details':final}
report['pass']=not delta and not root_errors and not resource_errors and len(final['grass'])==73 and len(final['scenes'])==4 and report['source_unchanged'] and report['reference_unchanged']
(O/'grass_final_check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('GRASS_FINAL_READONLY',json.dumps({k:v for k,v in report.items() if k not in ['details','ground','scenes']},ensure_ascii=False),flush=True)
assert report['pass']
