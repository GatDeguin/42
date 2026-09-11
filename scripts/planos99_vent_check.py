"""D08 read-only environmental intersections and tangible service extraction envelopes."""
import bpy,bmesh,json,ast,hashlib
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
parts=[o for o in S.objects if o.type=='MESH' and o.name.startswith('VENT99 |')];others=[o for o in S.objects if o.type=='MESH' and not o.hide_render and not o.name.startswith(('VENT99 |','BOT95','TEXT99'))];bb={o.name:bounds(o) for o in parts+others};hits=[];designed=[];count=0
for a in parts:
 for b in others:
  if not overlap(bb[a.name],bb[b.name]) or not worth(a,b):continue
  v=vol(a,b);count+=1
  if v>1e-8:
   h={'new':a.name,'existing':b.name,'volume_m3':v}
   (designed if 'tornillo cabio P' in a.name and b.name.startswith('Estudio | cabio') else hits).append(h)
 print('VENTCHECK',a.name,'hits',len(hits),flush=True) if len(hits)>0 else None
# Service path solids are temporary test geometry, not invisible substitute equipment.
def cube(n,x,y,z):
 v=[(xx,-zz,yy) for yy in y for zz in z for xx in x];m=bpy.data.meshes.new(n);m.from_pydata(v,[],[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]);m.update();o=bpy.data.objects.new(n,m);S.collection.objects.link(o);return o
rig=bpy.data.objects.get('DOOR | studio')
if rig:
 if rig.animation_data:rig.animation_data.action=None
 rig['open']=1;rig.update_tag();bpy.context.view_layer.update();bb.update({o.name:bounds(o) for o in others});cache.clear()
service=[]
names={o.name:o for o in parts}
hatch=[o.name for o in parts if o.name.startswith(('VENT99 | panel registro desmontable','VENT99 | cierre cuarto vuelta panel'))]
assert len(hatch)==26,hatch

def pref(prefix):return [n for n in names if n.startswith('VENT99 | '+prefix)]

def remove_for(key,kind):
 rem=list(hatch)
 if kind=='filter':
  rem+=pref(key+' filtro tapa inferior desmontable')+pref(key+' cartucho ')
 elif kind=='silencer':
  rem+=pref(key+' silenciador ')+pref(key+' camisa perforada interna')+pref(key+' abrazadera silenciador')+pref(key+' flexible salida')+pref(key+' acople salida silenciador50')+pref(key+' manta acople salida silenciador50')
  z=4.68 if key=='impulsion' else 5.10
  for o in parts:
   lo,hi=bb[o.name];x=(lo[0]+hi[0])/2;zz=-(lo[1]+hi[1])/2
   if o.name.startswith(('VENT99 | varilla equipo M6','VENT99 | tuerca equipo')) and abs(zz-z)<1e-4 and min(abs(x-19.30),abs(x-19.70))<1e-4:rem.append(o.name)
 elif kind=='fan':
  rem+=pref(key+' ventilador ')+pref(key+' flexible entrada')+pref(key+' flexible salida')
 else:raise ValueError(kind)
 assert len(set(rem))==len(rem),(key,kind,rem)
 return sorted(rem)
paths=[('service platform',[18.95,19.55],[3.251,6.0],[4.48,5.68],[],'Access with all new parts installed.'),('rear approach',[14.30,19.55],[3.251,5.25],[5.0,5.60],[],'Approach with all new parts installed; studio door fully open.')]
for key,label,z in [('impulsion','supply',4.68),('extraccion','extract',5.10)]:
 paths.append(('filter '+label+' lower',[18.783,18.805],[5.4,6.999],[z-.110,z+.110],remove_for(key,'filter'),'Isolate unit. Remove both hatch panels and their quarter-turn closures. Release own filter bottom cover, then lower cassette; other unit and all supports remain.'))
 paths.append(('silencer '+label+' lower',[19.199,19.801],[5.4,7.018],[z-.128,z+.128],remove_for(key,'silencer'),'Isolate unit. Remove hatch panels and their closures, both adjacent flexible couplings including detachable exit insulation, own two clamp bands and two rods/nuts; lower own silencer. Other unit, fan, rigid ducts and rails remain.'))
 paths.append(('fan '+label+' lower',[18.949,19.151],[5.4,6.969],[z-.079,z+.079],remove_for(key,'fan'),'Isolate unit. Remove hatch panels and their closures, inlet and outlet flexible couplings; lower fan module. Both filter cases, silencers and structural hangers remain.'))
for n,x,y,z,removed,sequence in paths:
 a=cube(n,x,y,z);bpy.context.view_layer.update();ab=bounds(a);sh=[];pairs=0
 retained=[o for o in parts if o.name not in removed]
 for b in others+retained:
  if not overlap(ab,bb[b.name]) or not worth(a,b):continue
  v=vol(a,b);count+=1;pairs+=1
  if v>1e-8:sh.append({'object':b.name,'family':'VENT99 retained' if b in retained else 'existing','volume_m3':v})
 service.append({'id':n,'source_bounds':{'x':x,'y':y,'z':z},'removed_objects':removed,'retained_vent_objects':len(retained),'removal_sequence':sequence,'boolean_pairs':pairs,'hits':sh,'pass':not sh});cache.pop(a.name,None);bpy.data.objects.remove(a,do_unlink=True)
r={'source':bpy.data.filepath,'sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'boolean_pairs':count,'hard_environment_hits':hits,'designed_screws_embedded_into_rafters':designed,'service_paths':service,'minimum_new_fixed_height_m':min(bb[o.name][0][2] for o in parts),'minimum_height_pass':min(bb[o.name][0][2] for o in parts)>=6.452,'rectangular_air_area_m2':.300*.080,'pass':not hits and all(q['pass'] for q in service) and min(bb[o.name][0][2] for o in parts)>=6.452,'service_entry_door':'studio open=1 for approach check', 'scope':'New environmental contacts; service swept envelopes checked against all active original environment plus all VENT99 except exact per-path removed_objects. Temporary boxes are full conservative swept volumes. This does not validate airflow, acoustics or resistance.'}
(R/'review99/vent_check_r7.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),'utf-8');print('VENTRESULT',json.dumps(r,ensure_ascii=False),flush=True)
