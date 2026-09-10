import bpy,json,sys,ast,hashlib
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parent.parent;S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
for nd in ast.parse((root/'scripts/planos95_corredizas_check.py').read_text(encoding='utf8')).body:
 if isinstance(nd,ast.FunctionDef):exec(compile(ast.Module(body=[nd],type_ignores=[]),'<collision>','exec'))
import bmesh
checks=[];hits=[];counts={}
def sb(o):
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());p=[e.matrix_world@Vector(v) for v in e.bound_box];return {'x':[min(v.x for v in p),max(v.x for v in p)],'y':[min(v.z for v in p),max(v.z for v in p)],'z':[min(-v.y for v in p),max(-v.y for v in p)]}
def check(name,passed,value=None):checks.append({'name':name,'pass':bool(passed),'value':value})
def pairtest(a,b,label):
 if not bbinter(bounds(a),bounds(b)):return
 v=volume_intersection(a,b);counts[label]=counts.get(label,0)+1
 if v>1e-8:hits.append({'stage':label,'a':a.name,'b':b.name,'volume_m3':v})
for n,top,bottom in [('Piso monoambiente',.21,.20),('Piso quincho',.18,.17),('Piso baño mono',.21,.20),('Piso baño quincho',.21,.20)]:
 b=sb(bpy.data.objects[n]);check(n+' correct level',abs(b['y'][1]-top)<2e-6 and abs(b['y'][0]-bottom)<2e-6,b['y'])
for n,x,z,w,d in [('Lavatorio mono',20.54,4.52,.62,.32),('Lavatorio quincho',20.995,10.37,.46,.38),('Inodoro mono',19.85,5.44,.42,.62),('Inodoro quincho',21.53,10.58,.42,.62)]:
 b=sb(bpy.data.objects[n]);expected=[x-w/2,x+w/2,z-d/2,z+d/2];actual=b['x']+b['z'];check(n+' coordinated bounds',max(abs(a-e) for a,e in zip(actual,expected))<2e-5,actual)
slab=bpy.data.objects['Losa planta baja'];floors=[o for o in S.objects if o.type=='MESH' and (o.name in ['Piso monoambiente','Piso quincho','Piso baño mono','Piso baño quincho'] or o.name.startswith('BTH95 |')) and any(w in o.name.lower() for w in ['piso','base30','mortero','membrana','adhesivo','baldosa']) and 'puente' not in o.name and 'remonte' not in o.name]
for i,a in enumerate(floors):
 pairtest(a,slab,'floor vs slab')
 for b in floors[i+1:]:pairtest(a,b,'floor layers')
fixed=[o for o in S.objects if o.type=='MESH' and (o.name.startswith(('Baño mono muro','Baño mono frente','Baño quincho muro','Baño quincho frente','Separación mono quincho','BTH95 | cierre')) or o==slab or o in floors)]
fixtures=[o for o in S.objects if o.type=='MESH' and o.name.startswith(('Inodoro mono','Inodoro quincho','Lavatorio mono','Lavatorio quincho','Espejo baño mono','Espejo baño pileta','BTH95 | mampara fija'))]
for a in fixtures:
 for b in fixed:pairtest(a,b,'fixture vs architecture')
for i,a in enumerate(fixtures):
 for b in fixtures[i+1:]:
  if a.name.startswith('Inodoro mono') and b.name.startswith('Inodoro mono'):continue
  if a.name.startswith('Inodoro quincho') and b.name.startswith('Inodoro quincho'):continue
  pairtest(a,b,'fixtures')
# Both bathroom doors through five controlled opening states.
rigs=[bpy.data.objects[n] for n in ['DOOR | bathroomMono','DOOR | poolBath']]
for r in rigs:
 if r.animation_data:r.animation_data.action=None
moving=[o for r in rigs for o in r.children_recursive if o.type=='MESH'];move_names={o.name for o in moving};static=[o for o in S.objects if o.type=='MESH' and o.name not in move_names and (o in fixed or o in fixtures or o.name.startswith('BTH95 |'))]
for t in [0,.25,.5,.75,1]:
 for r in rigs:r['open']=t;r.update_tag()
 bpy.context.view_layer.update()
 for a in moving:
  if 'burlete' in a.name.lower():continue
  for b in static:
   if any(w in b.name.lower() for w in ['membrana','junta','sello']):continue
   pairtest(a,b,'door '+str(t))
 print('BATH_DOOR_POSE',t,flush=True)
# Four tray surfaces and central recess carry the specified elevations.
tile=[o for o in S.objects if o.name.startswith('BTH95 | ducha baldosa10')]
check('Four shower planes',len(tile)==4,len(tile))
check('Shower perimeter and drain elevations',all(abs(sb(o)['y'][1]-.21)<2e-6 and abs(sb(o)['y'][0]-.1855)<2e-6 for o in tile),[sb(o)['y'] for o in tile])
check('13 door rigs retained',len([o for o in S.objects if o.name.startswith('DOOR |')])==13)
check('No positive hard intersections in tested sets',not hits,len(hits))
result={'model':bpy.data.filepath,'sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'pass':all(c['pass'] for c in checks),'checks':checks,'hard_intersections':hits,'boolean_pair_counts':counts,'scope':'Geometry/circulation/floor layers; not product performance, normative accessibility, hydraulic or structural calculations'}
(root/'review95/banos_r6d_checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8');print(json.dumps(result,indent=2,ensure_ascii=False))
