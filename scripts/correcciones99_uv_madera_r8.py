"""Restore explicitly referenced, absent photographic timber UV layers with metric mapping."""
import bpy,numpy as np,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def shape(o):
 m=o.data;v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);i=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',i)
 return hashlib.sha256(v.tobytes()+i.tobytes()+np.array(o.matrix_world,dtype=np.float64).tobytes()).hexdigest()
def requests(o):
 out={}
 used={p.material_index for p in o.data.polygons}
 for slot in used:
  mat=o.data.materials[slot] if slot<len(o.data.materials) else None
  if not mat or not mat.use_nodes:continue
  connected=set();stack=[n for n in mat.node_tree.nodes if n.type=='OUTPUT_MATERIAL' and n.is_active_output]
  while stack:
   n=stack.pop()
   if n in connected:continue
   connected.add(n);stack.extend(l.from_node for s in n.inputs for l in s.links)
  for n in connected:
   if n.type in ['UVMAP','NORMAL_MAP'] and n.uv_map and not o.data.uv_layers.get(n.uv_map):out.setdefault(n.uv_map,[]).append((slot,mat))
 return out

def apply():
 rows=[];unhandled=[]
 for o in list(bpy.context.scene.objects):
  if o.type!='MESH' or o.hide_render:continue
  missing=requests(o)
  if not missing:continue
  old=shape(o);m=o.data
  if m.users>1:o.data=m.copy();m=o.data
  coords=np.array([v.co[:] for v in m.vertices]);scale=np.array([o.matrix_world.to_3x3().col[i].length for i in range(3)]);coords*=scale
  extents=np.ptp(coords,axis=0);long_axis=int(np.argmax(extents));seed=hashlib.sha256(o.name.encode('utf-8')).digest();offset=np.array([int.from_bytes(seed[:4],'little')/2**32,int.from_bytes(seed[4:8],'little')/2**32])
  for uvname,specs in missing.items():
   slots={slot:mat for slot,mat in specs}
   if not all(mat.get('photographic_wood') for mat in slots.values()):unhandled.append(dict(object=o.name,uv=uvname,materials=[m.name for m in slots.values()]));continue
   uv=m.uv_layers.new(name=uvname);assert uv.name==uvname
   for poly in m.polygons:
    mat=slots.get(poly.material_index)
    if mat is None:continue
    floor=mat.get('wood_floor',False);axis=0 if floor else long_axis;other=[i for i in range(3) if i!=axis]
    if abs(poly.normal[axis])>.85:cross,along=other
    else:cross=min(other,key=lambda i:abs(poly.normal[i]));along=axis
    tile=json.loads(mat.get('texture_size_metres','[1.830000043,1.830000043]'));off=np.floor(offset*np.array([8,2]))/np.array([8,2]) if floor else offset
    for li in poly.loop_indices:
     p=coords[m.loops[li].vertex_index];uv.data[li].uv=(p[cross]/tile[0]+off[0],p[along]/tile[1]+off[1])
   rows.append(dict(object=o.name,restoredLayer=uvname,materials=[mat.name for mat in slots.values()],tileMetres=tile,longitudinalAxisLocal=long_axis,offset=offset.tolist(),physicalGeometryUnchanged=True))
  m.update();assert shape(o)==old,o.name
  if not requests(o):o['revision99_r8_uv']='Named photographic UV layers restored with physical asset scale'
 bpy.context.view_layer.update()
 report=dict(corrected=rows,unhandledMissingLayers=unhandled,scope='Only absent explicitly referenced timber UV; existing layers/materials and all geometry preserved',videoRendered=False)
 return report
if __name__=='__main__':
 a=apply();second=apply();assert not second['corrected'];out=R/'review99/r8_optics';out.mkdir(exist_ok=True);(out/'wood_uv_checks.json').write_text(json.dumps(a,indent=2,ensure_ascii=False),encoding='utf-8');print('NAMED_UV_REPAIR',json.dumps(a,ensure_ascii=True),flush=True)
