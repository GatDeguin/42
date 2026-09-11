"""Read-only sanitary assembly checks on the frozen integrated source. No save or render."""
import bpy,bmesh,json,runpy,ast,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(r'D:\2026\42');S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
for filename,keys in [('planos95_juntas_check.py',['bounds','overlap','vol']),('preview99_sanitarios_pavimento.py',['tree','contains'])]:
 for f in ast.parse((R/'scripts'/filename).read_text(encoding='utf-8-sig')).body:
  if isinstance(f,ast.FunctionDef) and f.name in keys:exec(compile(ast.Module(body=[f],type_ignores=[]),'<sanitary measurement>','exec'))
patch=runpy.run_path(str(R/'scripts/correcciones99_sanitarios_pavimento.py'));names=patch['BODY']+patch['SEAT']+patch['TANK'];result=json.loads(S[patch['TAG']])
objects=[bpy.data.objects[n] for n in names]+[o for o in S.objects if o.type=='MESH' and o.name.startswith('SAN99 |')]
assert len(objects)==78 and 'Zócalo columna cocina' not in bpy.data.objects
normals=[]
for o in objects:
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();bm=bmesh.new();bm.from_mesh(me)
 normals.append(dict(name=o.name,volume=bm.calc_volume(signed=True),nonmanifold=sum(not e.is_manifold for e in bm.edges),determinant=o.matrix_world.determinant()));bm.free();ev.to_mesh_clear()
interfaces=[o.name for o in S.objects if o.name.startswith('BTH95 |') and any(k in o.name for k in ['reserva salida WC','sello salida WC'])]
external=[o for o in S.objects if o.type=='MESH' and not o.hide_render and o not in objects and o.name not in interfaces]
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
  if v>1e-8:hits.append(dict(a=a.name,b=b.name,volume_m3=v))
internal=[]
for i in range(3):
 a=bpy.data.objects[patch['SEAT'][i]];t=bpy.data.objects[patch['TANK'][i]];b=bpy.data.objects[patch['BODY'][i]];lid=bpy.data.objects[result['details'][patch['BODY'][i]]['lid']]
 for x,y in [(a,t),(a,b),(lid,t),(lid,a),(t,b)]:
  v=vol(x,y) if overlap(bounds(x),bounds(y)) else 0;internal.append(dict(a=x.name,b=y.name,volume_m3=v))
prior=json.loads((R/'review99/sanitary_floor/validation.json').read_text(encoding='utf8'));footprints=[]
for i,label in enumerate(['mono','quincho','suite']):
 family=[bpy.data.objects[q[i]] for q in [patch['BODY'],patch['SEAT'],patch['TANK']]]+[o for o in objects if o.name.startswith('SAN99 | '+label+' ')]
 boxes=[patch['bounds'](o) for o in family];current=[[min(b[k][0] for b in boxes),max(b[k][1] for b in boxes)] for k in range(3)];original=prior['global_plan_boxes'][label]['before']
 delta=max(abs(current[k][j]-original[k][j]) for k in range(2) for j in range(2));footprints.append(dict(label=label,current=current,original=original,maxPlanDelta=delta))
passed=not hits and all(q['volume_m3']<1e-8 for q in internal) and all(q['volume']>0 and q['nonmanifold']==0 and q['determinant']>0 for q in normals) and all(q['maxPlanDelta']<.00002 for q in footprints)
report=dict(source=bpy.data.filepath,sourceSHA256=hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),pass_=passed,externalPairs=pairs,externalHits=hits,internal=internal,normals=normals,footprints=footprints,retainedInterfaces=interfaces,orphanPlinthRemoved=True,videoRendered=False,scope='Geometric contacts and envelopes; generic fixture with simplified internal ceramic, no manufacturer hydraulic performance claim.')
report['pass']=report.pop('pass_');(R/'review99/r7d_integrated/sanitary_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print('R7_SANITARY_FROZEN',passed,pairs,flush=True);assert passed