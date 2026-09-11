import bpy,bmesh,json,runpy,ast,hashlib,os,numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=r'D:\2026\42';OUT=Path(ROOT)/'review99/sanitary_floor';OUT.mkdir(exist_ok=True)
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
source=bpy.data.filepath;sourceSHA=hashlib.sha256(Path(source).read_bytes()).hexdigest();assert sourceSHA=='af722a146b820356cf52c4658952405ea084e083444f5c24d01f4951ac735f95'
for file,names in [('integrate99_r7c.py',['snapshot']),('planos95_juntas_check.py',['bounds','overlap','vol'])]:
 for n in ast.parse((Path(ROOT)/'scripts'/file).read_text('utf8')).body:
  if isinstance(n,ast.FunctionDef) and n.name in names:exec(compile(ast.Module(body=[n],type_ignores=[]),'<independent helper>','exec'),globals())
patch=runpy.run_path(str(Path(ROOT)/'scripts/correcciones99_sanitarios_pavimento.py'));names=patch['BODY']+patch['SEAT']+patch['TANK'];bb=patch['bounds']
tile_users=[o.name for o in S.objects if o.type=='MESH' and not o.hide_render and any(m and m.get('source_material_key')=='tile' for m in o.data.materials)]
allowed=set(names+tile_users+[patch['CAM'],'Zócalo columna cocina']);before=snapshot(True)
old_boxes={}
for i,label in enumerate(['mono','quincho','suite']):
 boxes=[bb(bpy.data.objects[q[i]]) for q in [patch['BODY'],patch['SEAT'],patch['TANK']]]
 old_boxes[label]=[[min(b[k][0] for b in boxes),max(b[k][1] for b in boxes)] for k in range(3)]
result=patch['apply']();after=snapshot(True);outside=[n for n in before if n not in allowed and before[n]!=after.get(n)];new=set(after)-set(before)
assert not outside,outside;assert all(n.startswith('SAN99 |') for n in new);assert set(before)-set(after)=={'Zócalo columna cocina'}
first=snapshot(True);patch['apply']();second=snapshot(True);assert first==second
objects=[bpy.data.objects[n] for n in names]+[bpy.data.objects[n] for n in new if bpy.data.objects[n].type=='MESH']
normals=[]
for o in objects:
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();bm=bmesh.new();bm.from_mesh(me)
 normals.append({'name':o.name,'signed_volume_local':bm.calc_volume(signed=True),'non_manifold_edges':sum(not e.is_manifold for e in bm.edges),'world_determinant':o.matrix_world.determinant()});bm.free();ev.to_mesh_clear()
bad=[r for r in normals if r['signed_volume_local']<=0 or r['non_manifold_edges'] or r['world_determinant']<=0];assert not bad,bad
global_boxes={}
for i,label in enumerate(['mono','quincho','suite']):
 family=[bpy.data.objects[q[i]] for q in [patch['BODY'],patch['SEAT'],patch['TANK']]]+[o for o in objects if o.name.startswith('SAN99 | '+label+' ')]
 boxes=[bb(o) for o in family];newbox=[[min(b[k][0] for b in boxes),max(b[k][1] for b in boxes)] for k in range(3)]
 deltas=[[newbox[k][j]-old_boxes[label][k][j] for j in range(2)] for k in range(2)]
 assert max(abs(v) for row in deltas for v in row)<.00002,(label,deltas)
 global_boxes[label]={'before':old_boxes[label],'after_open_lid':newbox,'max_plan_delta_m':max(abs(v) for row in deltas for v in row)}
def tree(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();t=BVHTree.FromPolygons([ev.matrix_world@v.co for v in me.vertices],[list(p.vertices) for p in me.polygons],epsilon=1e-7);ev.to_mesh_clear();return t
def contains(a,b):return all(a[0][i]<=b[0][i]+1e-6 and a[1][i]>=b[1][i]-1e-6 for i in range(3))
moving={o.name for o in objects}
interfaces=[o.name for o in S.objects if o.name.startswith('BTH95 |') and any(k in o.name for k in ['reserva salida WC','sello salida WC'])]
external=[o for o in S.objects if o.type=='MESH' and not o.hide_render and o.name not in moving and o.name not in interfaces]
cache={o.name:bounds(o) for o in external};trees={};hits=[];pairs=0
for a in objects:
 ab=bounds(a);at=None
 for b in external:
  bv=cache[b.name]
  if not overlap(ab,bv):continue
  if at is None:at=tree(a)
  if b.name not in trees:trees[b.name]=tree(b)
  if not contains(ab,bv) and not contains(bv,ab) and not at.overlap(trees[b.name]):continue
  v=vol(a,b);pairs+=1
  if v>1e-8:hits.append({'a':a.name,'b':b.name,'volume_m3':v})
 if a.name in names:print('SAN99_EXTERNAL',a.name,flush=True)
internal=[]
for i in range(3):
 a=bpy.data.objects[patch['SEAT'][i]];t=bpy.data.objects[patch['TANK'][i]];b=bpy.data.objects[patch['BODY'][i]];lid=bpy.data.objects[result['details'][patch['BODY'][i]]['lid']]
 for x,y in [(a,t),(a,b),(lid,t),(lid,a),(t,b)]:
  v=vol(x,y) if overlap(bounds(x),bounds(y)) else 0;internal.append({'a':x.name,'b':y.name,'volume_m3':v})
report={'source':source,'sourceSHA256':sourceSHA,'patch':result,'scriptSHA256':hashlib.sha256((Path(ROOT)/'scripts/correcciones99_sanitarios_pavimento.py').read_bytes()).hexdigest(),'removed_objects':sorted(set(before)-set(after)),'outside_scope_changes':outside,'new_objects':sorted(new),'idempotence':True,'global_plan_boxes':global_boxes,'interfaces_retained':interfaces,'external_boolean_pairs':pairs,'external_hits':hits,'assembly_contact_checks':internal,'normals':normals,'pass':not hits and all(r['volume_m3']<1e-8 for r in internal)}
(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf8');assert report['pass'],{'external':hits,'internal':[r for r in internal if r['volume_m3']>=1e-8]}
dest=Path(ROOT)/'output/Casa_de_Campo_99_SanitaryFloor_preview.blend';bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest),compress=True)
report.update(output=str(dest),outputSHA256=hashlib.sha256(dest.read_bytes()).hexdigest());(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf8')
assert hashlib.sha256(Path(source).read_bytes()).hexdigest()==sourceSHA
print('SAN99_VALIDATED',json.dumps({'pass':report['pass'],'sha256':report['outputSHA256'],'new_objects':len(new),'external_pairs':pairs,'outside':outside,'internal':internal},ensure_ascii=True),flush=True)
