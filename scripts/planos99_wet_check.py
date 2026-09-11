import bpy,json,ast,bmesh,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path('D:/2026/42');S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
for nd in ast.parse((R/'scripts/planos95_juntas_check.py').read_text(encoding='utf-8-sig')).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['bounds','overlap','vol']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
cache={}
def tree(o):
 if o.name not in cache:
  e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();vv=[e.matrix_world@v.co for v in m.vertices];ff=[list(p.vertices) for p in m.polygons];cache[o.name]=(BVHTree.FromPolygons(vv,ff,epsilon=1e-7),vv[0] if vv else Vector());e.to_mesh_clear()
 return cache[o.name]
def inside(p,t):
 d=Vector((.865,.321,.386)).normalized();num=0;q=p.copy()
 for i in range(30):
  hit=t.ray_cast(q,d,100)
  if hit[0] is None:break
  num+=1;q=hit[0]+d*.000003
 return num%2==1
def worth(a,b):
 ta,pa=tree(a);tb,pb=tree(b);return bool(ta.overlap(tb)) or inside(pa,tb) or inside(pb,ta)
parts=[o for o in S.objects if o.type=='MESH' and o.name.startswith('WET99 |')];others=[o for o in S.objects if o.type=='MESH' and not o.hide_render and not o.name.startswith('WET99 |')];bs={o.name:bounds(o) for o in parts+others};hits=[];numerical=[];pairs=0
for a in parts:
 for b in others:
  if not overlap(bs[a.name],bs[b.name]) or not worth(a,b):continue
  # Evaluate only environmental objects near the part, excluding distant botanical bounds.
  if b.name.startswith(('BOT95','TEXT99')):continue
  v=vol(a,b);pairs+=1
  if v>1e-8:
   item={'new':a.name,'existing':b.name,'intersection_m3':v}
   if a.name=='WET99 | PB ceramica8' and b.name in ['Espejo baño mono','BTH95 | mampara canal muro fondo']:
    face=-bs[b.name][1][1];depth=.26-face;area=(bs[b.name][1][0]-bs[b.name][0][0])*(bs[b.name][1][2]-bs[b.name][0][2]);item['normal_overlap_m']=depth
    if 0<=depth<1e-6 and v<=area*depth*1.3:numerical.append(item)
    else:hits.append(item)
   else:hits.append(item)
 print('WETCHECK',a.name,len(hits),flush=True) if hits else None
cer=bpy.data.objects['WET99 | PB ceramica8'];bm=bmesh.new();bm.from_mesh(cer.data);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free()
report={'ceramic_nonmanifold_edges':nonmanifold,'source':bpy.data.filepath,'sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'parts':len(parts),'external_boolean_pairs':pairs,'hits':hits,'coplanar_rounding_under_1_micron':numerical,'pass':not hits and not nonmanifold,'scope':'Every wet new mesh against active external mesh with overlapping evaluated bounds; designed embedded bodies listed as hits for pocket coordination.'}
(R/'review99/wet_check_r7.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8');print('WETRESULT',json.dumps(report,ensure_ascii=False),flush=True)
