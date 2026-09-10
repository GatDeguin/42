"""Independent frozen-model dimensional audit. Read-only: no save/render/model edits.
Blender --background --factory-startup MODEL --python THIS -- --expected-sha SHA --label r6k
Outputs full evaluated JSON/CSV, 54 furniture families and targeted geometry evidence.
The script supplies measurements and explicit project checks, never a global score/certification.
"""
import bpy,json,hashlib,numpy as np,os,sys,re,ast,csv,contextlib,io
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--expected-sha',required=True);ap.add_argument('--label',default='r6k');args=ap.parse_args(argv)
assert re.fullmatch(r'[a-z0-9_]+',args.label),'Unsafe audit label'
source=Path(bpy.data.filepath)
assert source.is_file(),'Open the frozen model first'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
digest=sha(source)
assert digest.lower()==args.expected_sha.lower(),('SHA mismatch',digest,args.expected_sha)
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
prefix=ROOT/'audit'/('integral95_02_'+args.label)
def save(suffix,data):
 p=Path(str(prefix)+'_'+suffix+'.json');p.write_text(json.dumps(data,ensure_ascii=False,indent=2,default=float),encoding='utf8');return str(p)
# Reuse our own complete evaluated inventory implementation without mutating its source.
inv_code=(ROOT/'audit/integral95_dimension_inventory.py').read_text(encoding='utf8')
env={'__name__':'independent_inventory','__file__':str(ROOT/'audit/integral95_dimension_inventory.py')}
with contextlib.redirect_stdout(io.StringIO()):exec(compile(inv_code,env['__file__'],'exec'),env)
inventory=env['out'];assert inventory['sha256']==digest
objects={o['name']:o for o in inventory['objects'] if o['render_enabled_by_collection']}
scale=float(S.unit_settings.scale_length)
assert abs(scale-1)<1e-9,'Targeted source-space geometric probes require metric scale_length 1; full inventory already records actual scale.'
def b(n):
 q=objects[n]['world_bounds_source_m'];return np.array(q['min']),np.array(q['max'])
def members(pat):
 return [n for n in objects if re.search(pat,n)]
def group_bounds(names):
 return np.min([b(n)[0] for n in names],0),np.max([b(n)[1] for n in names],0)
checks=[]
def check(name,value,target=None,tol=0.0001,minimum=None,explanation='Project geometry criterion, not regulation or product certification'):
 passed=(abs(float(value)-target)<=tol) if target is not None else (float(value)>=minimum-tol)
 checks.append(dict(name=name,measured=value,target=target,minimum=minimum,tolerance_m=tol,pass_geometry=bool(passed),scope=explanation))
def floor_name(title,floor):
 if title=='Banco huerta':return None
 if 'quincho' in title.lower():return 'Piso baño quincho' if title.startswith(('Inodoro','Lavatorio')) else 'Piso quincho'
 if abs(floor-.18)<1e-8:return 'Piso quincho'
 if floor<1:return 'Piso baño mono' if title.startswith(('Inodoro','Lavatorio','Ducha')) else 'Piso monoambiente'
 if title in ['Consola estudio','Silla estudio','Monitor izquierdo','Monitor derecho','Pantalla DAW','Sofá estudio','Rack estudio']:return 'Piso estudio'
 if title in ['Vanitory PA mesada','Bacha apoyo PA','Bañera PA','Inodoro PA','Bidet PA']:return 'Piso baño vivienda'
 return 'Piso vivienda'
# Recover the original 54 categories, update only selectors changed by real component replacement.
tree=ast.parse((ROOT/'audit/integral95_02_r6f_dimension_families.py').read_text(encoding='utf8'))
rules=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='rules' for t in n.targets))
assert len(rules)==54
families=[];family_by={}
for title,pat,datum,func in rules:
 if title.startswith('Taburete isla'):
  letter=title[-1];pat=r'^Taburete isla mono '+letter+r' \| ';func=r'asiento'
 if title=='Banco huerta':pat=r'^Banco huerta \| ';func=r'tablón asiento'
 if title=='Mesa baja vivienda':pat=r'^(Mesa baja vivienda$|MOB95 \| pata mesa baja estar)';func=r'^Mesa baja vivienda$'
 if title=='Cama conjunto':pat=r'^(Cama dormitorio |MOB95 \| pata cama)'
 if title=='Consola estudio':pat=r'^(Consola estudio$|Base consola estudio$|MOB95 \| apoyo consola)'
 names=members(pat)
 if title.startswith('Mesita luz') and names:
  lo,hi=group_bounds(names)
  names+= [n for n in members(r'^MOB95 \| pata mesa de luz') if all(lo[k]-1e-5<=b(n)[0][k] and b(n)[1][k]<=hi[k]+1e-5 for k in [0,2])]
 foundation=[n for n in names if bpy.data.objects[n].get('foundation_P',False)]
 physical=[n for n in names if n not in foundation]
 fn=floor_name(title,datum);measured_floor=float(b(fn)[1][1]) if fn in objects else datum
 if title=='Banco huerta':
  pads=[n for n in foundation if 'loseta' in n];measured_floor=float(max(b(n)[1][1] for n in pads)) if pads else datum
 row={'family':title,'members':physical,'foundation_members_separate':foundation,'query':pat,'floor_reference':fn or 'Top of measured proposed concrete pads','declared_floor_m':datum,'measured_reference_floor_m':measured_floor,'classification':'G measured / P unbranded assembly; no commercial product identity','scope':'Envelope includes listed components only; lowest point alone is not proof of every support.'}
 if not physical:row['missing_query']=True;families.append(row);continue
 lo,hi=group_bounds(physical);row.update(bbox_source_min=lo.tolist(),bbox_source_max=hi.tolist(),envelope_m=(hi-lo).tolist(),lowest_point_above_floor_m=float(lo[1]-measured_floor),highest_point_above_floor_m=float(hi[1]-measured_floor))
 ff=[n for n in physical if func and 'costura' not in n.lower() and re.search(func,n)]
 row['functional_query_missing']=bool(func and not ff)
 row['functional_surface_heights_above_floor_m']={n:float(b(n)[1][1]-measured_floor) for n in ff}
 if title=='Ducha mono rociador':row['lowest_head_clearance_above_floor_m']=float(lo[1]-measured_floor)
 families.append(row);family_by[title]=row
family_path=save('dimension_families',{'source':str(source),'sha256':digest,'families':families,'count':len(families),'missing':[r['family'] for r in families if r.get('missing_query')]})
# Expected seat/table levels are accepted project intentions, not generic regulations.
targets={'Sofá cama mono':.450,'Mesa mono':.750,'Silla mono 1':.460,'Silla mono 2':.460,'Taburete isla A':.650,'Taburete isla B':.650,'Mesa quincho':.750,'Silla quincho 1':.460,'Silla quincho 2':.460,'Silla quincho 3':.460,'Silla quincho 4':.460,'Silla estudio':.470,'Sofá estudio':.450,'Mesa comedor':.750,'Silla comedor norte -0.49':.470,'Silla comedor norte 0.49':.470,'Silla comedor sur -0.49':.470,'Silla comedor sur 0.49':.470,'Sofá vivienda':.450,'Banco huerta':.450,'Inodoro mono':.455,'Inodoro quincho':.455,'Inodoro PA':.455}
for title,target in targets.items():
 row=family_by.get(title,{})
 for n,v in row.get('functional_surface_heights_above_floor_m',{}).items():check('Functional top: '+n,v,target,tol=.002)
# Whole-scene dimensional outliers remain review flags, never automatic failure.
outliers=[{'name':o['name'],'flags':o['flags'],'bounds':o['world_bounds_source_m'],'active':o['render_enabled_by_collection']} for o in inventory['objects'] if o['flags']]
save('dimensional_outliers',{'source':str(source),'sha256':digest,'items':outliers,'note':'Includes surfaces, glazing, instanced meshes and non-unity scales. Each requires context; not a list of errors.'})
# Actual evaluated mesh helpers from our previously reviewed independent contact probe.
helper_tree=ast.parse((ROOT/'audit/integral95_02_r6h_bearing_knees.py').read_text(encoding='utf8'))
for n in helper_tree.body:
 if isinstance(n,ast.FunctionDef):exec(compile(ast.Module(body=[n],type_ignores=[]),'<independent_contact_helper>','exec'),globals())
cache={}
def meshgeo(n):
 if n not in cache:cache[n]=geo(bpy.data.objects[n])
 return cache[n]
def horizontal_contact(a,bs,height):
 va,fa=raw(bpy.data.objects[a]);aa=[va[t][:,[0,1]] for t in fa if max(abs(va[t][:,2]-height))<.000003]
 total=0.0
 for name in bs:
  vb,fb=raw(bpy.data.objects[name]);bb=[vb[t][:,[0,1]] for t in fb if max(abs(vb[t][:,2]-height))<.000003]
  total+=sum(area(clip(pa,pb)) for pa in aa for pb in bb)
 return total
def vertical_hit(n,x,z,height,direction,distance):
 loc,normal,idx,dist=meshgeo(n)[2].ray_cast(Vector((x,-z,height)),Vector((0,0,direction)),distance)
 return None if loc is None else float(loc.z)
# Architecture with measured datums, no terrain-zero shortcut.
architecture={}
for n in ['Césped del lote','Losa planta baja','Losa entre plantas','Descanso escalera','Piso estudio','Piso vivienda','Piso baño vivienda','Cubierta pendiente Cedro Misionero','Cubierta pendiente pileta','Cielorraso estudio | cota inferior 6.45m','Cielorraso vivienda | 2.60m sobre piso general','Cielorraso baño | 2.60m sobre porcelanato','Portón negro','Ventana DVH estudio vidrio']:
 if n in objects:architecture[n]=objects[n]['world_bounds_source_m']
lot=b('Césped del lote');check('Lot X',lot[1][0]-lot[0][0],22);check('Lot Z',lot[1][2]-lot[0][2],20)
for ceiling,floor,target in [('Cielorraso estudio | cota inferior 6.45m','Piso estudio',3.20),('Cielorraso vivienda | 2.60m sobre piso general','Piso vivienda',2.60),('Cielorraso baño | 2.60m sobre porcelanato','Piso baño vivienda',2.60)]:
 check('Clear height '+floor,b(ceiling)[0][1]-b(floor)[1][1],target)
check('Roof difference corresponding low exterior datums',b('Cubierta pendiente Cedro Misionero')[0][1]-b('Cubierta pendiente pileta')[0][1],.60)
check('Roof difference corresponding high exterior datums',b('Cubierta pendiente Cedro Misionero')[1][1]-b('Cubierta pendiente pileta')[1][1],.60)
# 18 real tread supports/noses, positive coplanar connection areas, actual rise/going.
stairs=[]
for i in range(1,19):
 wn=f'Peldaño exterior {i}';sn=f'Soporte peldaño {i}';nn=f'Nariz antideslizante peldaño {i}'
 a,c=b(wn);sa,sc=b(sn);na,nc=b(nn)
 row={'step':i,'wood_top':float(c[1]),'wood_bottom':float(a[1]),'tread_width':float(c[0]-a[0]),'board_depth':float(c[2]-a[2]),'plan_center_z':float((a[2]+c[2])/2),'support_gap_m':float(a[1]-sc[1]),'nose_projection_m':float(nc[1]-c[1]),'contacts':[]}
 check('Stair support gap '+str(i),row['support_gap_m'],0)
 check('Stair nose projection '+str(i),row['nose_projection_m'],.002)
 check('Stair width '+str(i),row['tread_width'],1)
 for side,stringer,tx,sx in [('exterior','Zanca exterior',13.0685,13.0625),('interior','Zanca lado edificio',13.8915,13.8975)]:
  pn=f'DIM95 | cartela peldaño {i} {side}';c1=contact(bpy.data.objects[sn],bpy.data.objects[pn],tx);c2=contact(bpy.data.objects[pn],bpy.data.objects[stringer],sx)
  row['contacts'].append({'side':side,'tube_plate':c1,'plate_stringer':c2})
  for typ,v in [('tube_plate',c1),('plate_stringer',c2)]:check('Positive contact '+typ+' '+str(i)+' '+side,v['coplanar_overlap_m2'],minimum=1e-7,tol=0,explanation='Positive evaluated contact area m2; does not prove weld, timber connection or load capacity')
 stairs.append(row)
stairs.sort(key=lambda r:r['wood_top'])
start_pavement=float(b('AC95 | pavimento de arranque cota 0.06')[1][1])
for i,row in enumerate(stairs):
 row['rise_from_previous_m']=row['wood_top']-(stairs[i-1]['wood_top'] if i else start_pavement)
 row['going_from_previous_m']=abs(row['plan_center_z']-stairs[i-1]['plan_center_z']) if i else None
 row['starting_pavement_reference_for_first']=start_pavement if i==0 else None
check('Top tread finish datum',stairs[-1]['wood_top'],3.25)
# Real console underside sampled throughout central knee zone and front worktop.
console=[]
for x in [18.19,18.35,18.55,18.72]:
 for z in [2.6,3.0,3.4]:
  hits=[{'object':n,'y':h} for n in ['Consola estudio','Base consola estudio'] if (h:=vertical_hit(n,x,z,3.2501,1,1.5)) is not None]
  nearest=min(hits,key=lambda r:r['y']) if hits else None
  clearance=nearest['y']-b('Piso estudio')[1][1] if nearest else None
  console.append({'x':x,'z':z,'first_surface':nearest,'clearance_m':clearance})
  if clearance is not None:check('Console knee '+str(x)+'/'+str(z),clearance,minimum=.70)
front=vertical_hit('Consola estudio',18.72,3.0,5.5,-1,3)
if front is not None:check('Console front working height',front-b('Piso estudio')[1][1],.75,tol=.01,explanation='Nominal front worktop height; sloped console top varies with X')
# New seats: furniture/support datum and individual contact chains, not a solid envelope only.
seats=[]
for title in ['Taburete isla A','Taburete isla B','Banco huerta']:
 row=family_by[title];names=row['members'];feet=[n for n in names if 'apoyo elastomérico' in n];legs=[n for n in names if ' | pata ' in n];surfaces=[n for n in names if 'asiento' in n]
 chain=[]
 for foot in feet:
  tag=foot.split('apoyo elastomérico ',1)[1];leg=next(n for n in legs if n.endswith(tag));fa,fb=b(foot);la,lb=b(leg);x,z=(fa+fb)[[0,2]]/2
  seat_hits=[{'object':n,'bottom_y':h} for n in surfaces if (h:=vertical_hit(n,x,z,lb[1]-.005,1,.15)) is not None]
  actual_floor=row['measured_reference_floor_m']
  chain.append({'foot':foot,'leg':leg,'foot_to_finish_m':float(fa[1]-actual_floor),'pad_to_leg_gap_m':float(la[1]-fb[1]),'leg_top':float(lb[1]),'seat_underside_hits':seat_hits})
  check('Foot finish '+foot,fa[1]-actual_floor,0)
  check('Pad-leg '+leg,la[1]-fb[1],0)
  bearing_area=horizontal_contact(leg,surfaces,float(lb[1]));chain[-1]['leg_seat_contact_area_m2']=bearing_area
  check('Leg-seat positive contact '+leg,bearing_area,minimum=1e-6,tol=0,explanation='Positive coplanar area m2 over actual leg top; center ray is diagnostic when rounded slat edges leave local gaps. No capacity certification.')
 seats.append({'family':title,'seat_members':surfaces,'seat_thickness_m':{n:float(b(n)[1][1]-b(n)[0][1]) for n in surfaces},'contact_chains':chain,'footrest_heights_m':{n:float(b(n)[1][1]-row['measured_reference_floor_m']) for n in names if 'reposapiés' in n}})
# Water, swimming ledge and showers. Highest ledge AABB is not necessarily its central tread level.
wa,wb=b('Agua de pileta');caps={n:float(b(n)[1][1]) for n in members(r'^Borde pileta (norte|sur|este|oeste)$')}
pool={'water_min':wa.tolist(),'water_max':wb.tolist(),'cap_tops':caps,'freeboards_m':{n:h-float(wb[1]) for n,h in caps.items()},'wet_ledge_samples':[]}
check('Pool crest',wb[1],-.030)
pool['basin_floor_top_y']=float(b('Fondo de pileta')[1][1])
check('Pool water volume above basin floor',wa[1],minimum=pool['basin_floor_top_y'],explanation='Bulk water mesh should not extend below concrete floor top; final exact overlap is reported in separate clarification probe.')
for n,v in pool['freeboards_m'].items():check('Pool freeboard '+n,v,.100)
for x in [18.6,19.0,19.6]:
 for z in [15.5,16.5,17.5]:
  h=vertical_hit('Playa húmeda pileta',x,z,1,-1,3)
  pool['wet_ledge_samples'].append({'x':x,'z':z,'surface_y':h,'water_depth_m':float(wb[1]-h) if h is not None else None})
showers={'mono_underside_y':float(b('Ducha baño mono')[0][1]),'mono_floor_y':float(b('Piso baño mono')[1][1]),'legacy_PA_shower_present':'Ducha baño vivienda' in bpy.data.objects,'PA_head_bounds':objects.get('Ducha | rociador',{}).get('world_bounds_source_m'),'compact_tub_bounds':objects['Bañera vivienda']['world_bounds_source_m'],'compact_tub_label':bpy.data.objects['Bañera vivienda'].get('fixture_classification')}
check('Shower mono clear underside',showers['mono_underside_y']-showers['mono_floor_y'],2.10)
checks.append({'name':'Low legacy PA shower removed','pass_geometry':not showers['legacy_PA_shower_present'],'scope':'Presence of replaced duplicate, not sprinkler specification'})
# Dining coherent relocation and actual passage between table and wardrobe rear wall.
ta,tb=b('Mesa comedor tapa');wall=members(r'^Vestidor cierre al estar paño ')
wallmax=max(b(n)[1][2] for n in wall)
dining={'table_min':ta.tolist(),'table_max':tb.tolist(),'center_source':((ta+tb)/2).tolist(),'wardrobe_wall_rear_y_sourceZ':float(wallmax),'table_to_wardrobe_wall_gap_m':float(ta[2]-wallmax),'design_objective_not_regulation_m':.80,'group_members':members(r'^(Mesa comedor |Silla comedor )')}
check('Dining center sourceZ after +10mm',float((ta[2]+tb[2])/2),10.71,tol=.0001)
check('Dining passage to wardrobe wall',dining['table_to_wardrobe_wall_gap_m'],minimum=.80,tol=.0001)
legacy_glazing=[n for n in objects if ' Burlete ' in n and any(m and m=='Metal negro | blackMetal' for m in objects[n]['materials'])]
checks.append({'name':'Legacy solid glazing bars absent','pass_geometry':not legacy_glazing,'remaining':legacy_glazing,'scope':'Named obsolete solid metal seals only; does not certify every glazing assembly.'})
# Closed rig audit is descriptive only. Sweeps are a separately performed test, not repeated here.
rigs=[]
for rig in S.objects:
 if not rig.name.startswith('DOOR |'):continue
 descendants=[]
 for n in objects:
  p=bpy.data.objects[n].parent
  while p:
   if p==rig:descendants.append(n);break
   p=p.parent
 lo,hi=group_bounds(descendants) if descendants else (None,None)
 rigs.append({'rig':rig.name,'active_descendant_meshes':descendants,'closed_group_bounds_source':{'min':lo.tolist(),'max':hi.tolist()} if descendants else None,'note':'Group envelope includes hardware, not useful clear passage. Refer to independent opening/sweep evidence.'})
check('Door rig count',len(rigs),13,tol=0)
missing=[f['family'] for f in families if f.get('missing_query')]
targeted={'source':str(source),'sha256':digest,'architecture':architecture,'stairs':stairs,'console':console,'seats':seats,'pool':pool,'showers':showers,'dining':dining,'rigs':rigs,'checks':checks,'missing_families':missing,'limitations':['Only accepted project dimensions are treated as checks; no regulatory, structural, plumbing, acoustic or commercial-product certification.','Furniture envelopes and 54 functional categories do not prove every possible use scenario. Proposed equipment opening envelopes and live door sweeps remain separate evidence.','Human review and new photographs are indispensable before any overall score; a passing number of checks cannot establish photorealism.']}
target_path=save('consolidated_dimensions',targeted)
end_sha=sha(source);assert end_sha==digest,'File changed during independent audit'
summary={'source':str(source),'sha256':digest,'inventory_summary':inventory['summary'],'families':len(families),'missing_families':missing,'missing_functional_queries':[r['family'] for r in families if r.get('functional_query_missing')],'geometry_checks':len(checks),'failed_geometry_checks':[r for r in checks if not r['pass_geometry']],'outputs':[family_path,target_path],'file_integrity_unchanged':True,'status':'Measurements prepared for independent judgment; no automatic architecture or image approval.'}
save('dimensional_summary',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)
