import bpy,runpy,hashlib,json,time,numpy as np
from pathlib import Path
R=Path(r'D:\2026\42');O=R/'review99/r8_cesped';O.mkdir(parents=True,exist_ok=True)
SHA='9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e'
assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==SHA
source=bpy.data.filepath
cache={}
def sig(o):
 h=hashlib.sha256(np.asarray(o.matrix_world,dtype=np.float32).tobytes());h.update(str(o.hide_render).encode())
 if o.type=='MESH':
  key=o.data.as_pointer()
  if key not in cache:
   g=hashlib.sha256()
   v=np.empty(len(o.data.vertices)*3,np.float32);o.data.vertices.foreach_get('co',v);g.update(v.tobytes())
   l=np.empty(len(o.data.loops),np.int32);o.data.loops.foreach_get('vertex_index',l);g.update(l.tobytes())
   for uv in o.data.uv_layers:
    a=np.empty(len(uv.data)*2,np.float32);uv.data.foreach_get('uv',a);g.update(a.tobytes())
   g.update(str([m.name if m else None for m in o.data.materials]).encode());cache[key]=g.digest()
  h.update(cache[key])
 return h.hexdigest()
ground=bpy.data.objects['Césped del lote'];gv=np.array([list(v.co) for v in ground.data.vertices]);gf=[tuple(p.vertices) for p in ground.data.polygons]
print('GRASS8_CAPTURE',flush=True);before={o.name:sig(o) for o in bpy.data.objects};A=runpy.run_path(str(R/'scripts/correcciones99_cesped_r8.py'));t=time.time();rep=A['apply']();seconds=time.time()-t
cache.clear();after={o.name:sig(o) for o in bpy.data.objects};changed=sorted(n for n in before.keys()&after.keys() if before[n]!=after[n]);new=sorted(set(after)-set(before));removed=sorted(set(before)-set(after))
A['apply']();cache.clear();idempotent=after=={o.name:sig(o) for o in bpy.data.objects}
tree=A['ground_tree']();pads=A['exclusion_boxes']();roots=[];uv=[];errors=[]
for row in rep['objects']:
 o=bpy.data.objects[row['name']];anchors=json.loads(o['grass8_anchors'])
 for x,y,h,r,scale,var in anchors:
  measured=A['ground_at'](tree,x,y)
  if abs(h-measured)>1e-6 or not A['permitted'](x,-y,r,row['kind'],pads):errors.append([o.name,x,y,h,measured])
 roots.append({'object':o.name,'anchors':len(anchors),'excluded_roots':sum(not A['permitted'](x,-y,r,row['kind'],pads) for x,y,h,r,scale,var in anchors)})
 layer=o.data.uv_layers['UVMap'];arr=np.empty(len(layer.data)*2,np.float32);layer.data.foreach_get('uv',arr);uv.append({'object':o.name,'min':float(arr.min()),'max':float(arr.max()),'finite':bool(np.isfinite(arr).all())})
report={'source_sha256':SHA,'source':source,'patch_sha256':hashlib.sha256((R/'scripts/correcciones99_cesped_r8.py').read_bytes()).hexdigest(),'seconds_apply':seconds,'changed':changed,'added_objects':new,'removed_objects':removed,'idempotent':idempotent,'root_errors':errors,'roots':roots,'uv':uv,'totals':{k:v for k,v in rep.items() if k.startswith('total_')},'scenes':rep['scenes']}
report['ground_geometry_unchanged']=bool(np.array_equal(gv,np.array([list(v.co) for v in ground.data.vertices]))) and gf==[tuple(p.vertices) for p in ground.data.polygons]
report['ground_mask_huerta_errors']=rep['ground_atlas']['huerta_nonzero_mask_pixels']
report['pass']=report['ground_geometry_unchanged'] and report['ground_mask_huerta_errors']==0 and set(changed)==set(rep['replaced']+['Césped del lote']) and not new and not removed and idempotent and not errors and all(q['finite'] for q in uv) and len(rep['scenes'])==4
(O/'construction.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2),encoding='utf-8');(O/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
if report['pass']:
 bpy.context.preferences.filepaths.save_version=0
 bpy.ops.wm.save_as_mainfile(filepath=str(R/'output/Casa_de_Campo_99_R8_cesped_preview.blend'),compress=True)
print('GRASS8_RESULT',report['pass'],'clumps',rep['total_clumps'],'vertices',rep['total_vertices_after'],'triangles',rep['total_triangles_after'],'seconds',round(seconds,2),flush=True)
