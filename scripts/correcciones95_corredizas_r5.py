"""R5B slider details. Run on loaded copy -- --out PATH --report JSON.
P: dimensional proposal; no structural, hardware or weather certification.
"""
import bpy,json,sys,argparse,hashlib,math,bmesh
from pathlib import Path
from mathutils import Vector
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--report',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
S=bpy.context.scene;source=Path(bpy.data.filepath);source_sha=hashlib.sha256(source.read_bytes()).hexdigest()
if any(o.name.startswith('SL95 |') for o in S.objects):raise RuntimeError('SL95 already present')
S.frame_set(1);bpy.context.view_layer.update()
COL=bpy.data.collections.new('95 | Corredizas propuestas');S.collection.children.link(COL)
M={m.get('source_material_key'):m for m in bpy.data.materials if m.get('source_material_key')}
for m in bpy.data.materials:
 if m.name.startswith('MAT95 | '):M[m.name.split(' | ',1)[1]]=m

def mat(key):
 if key not in M:
  m=bpy.data.materials.new('SL95 | '+key);m.diffuse_color={'rubber95':(.025,.03,.03,1),'stainless':(.38,.4,.42,1),'grout':(.24,.25,.25,1),'polymer':(.16,.17,.17,1)}.get(key,(.025,.028,.032,1));M[key]=m
 return M[key]
def cv(p):return Vector((p[0],-p[2],p[1]))
def src(p):return (p.x,p.z,-p.y)
def bounds(o):
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());p=[src(e.matrix_world@Vector(v)) for v in e.bound_box]
 return {k:[min(q[i] for q in p),max(q[i] for q in p)] for i,k in enumerate('xyz')}
def overlap(a,b,tol=1e-6):return all(min(a[k][1],b[k][1])-max(a[k][0],b[k][0])>tol for k in 'xyz')
def child(o,r):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=r;o.matrix_world=mw;return o
def box(n,b,key='blackMetal',parent=None):
 x,y,z=(b[k] for k in 'xyz');v=[cv(p) for p in [(x[0],y[0],z[0]),(x[1],y[0],z[0]),(x[1],y[1],z[0]),(x[0],y[1],z[0]),(x[0],y[0],z[1]),(x[1],y[0],z[1]),(x[1],y[1],z[1]),(x[0],y[1],z[1])]]
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 o=bpy.data.objects.new(n,me);COL.objects.link(o);o.data.materials.append(mat(key));o['detail_status']='P / propuesta dimensional sin cálculo'
 if parent:child(o,parent)
 return o
def boolean(o,c,operation='DIFFERENCE'):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;m=o.modifiers.new('SL95 alojamiento','BOOLEAN');m.operation=operation;m.solver='EXACT';m.object=c;bpy.ops.object.modifier_apply(modifier=m.name)
def cylinder(n,a,b,r,key='stainless',parent=None,inner=None):
 va,vb=cv(a),cv(b);d=vb-va;bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=r,depth=d.length,location=(va+vb)/2);o=bpy.context.object;o.name=n;o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
 for c in list(o.users_collection):c.objects.unlink(o)
 COL.objects.link(o);o.data.materials.append(mat(key));o['detail_status']='P / propuesta dimensional sin cálculo'
 if inner:
  u=d.normalized();c=cylinder('TMP bore',src(va-u*.002),src(vb+u*.002),inner);boolean(o,c);bpy.data.objects.remove(c,do_unlink=True)
 if parent:child(o,parent)
 return o
operations=[]
def reserve(names,b,label):
 c=box('TMP '+label,b);done=[]
 for name in dict.fromkeys(names):
  o=bpy.data.objects.get(name)
  if o and o.type=='MESH' and overlap(bounds(o),b):boolean(o,c);done.append(name)
 bpy.data.objects.remove(c,do_unlink=True);operations.append({'reservation':label,'source_bounds':b,'objects':done});return done
def globox(t,u,h,axis):return {'x':t if axis=='x' else u,'y':h,'z':u if axis=='x' else t}
def xyz(t,u,h,axis):return (t,h,u) if axis=='x' else (u,h,t)
def gb(n,t,u,h,f,key='blackMetal',parent=None):return box('SL95 | '+f['id']+' '+n,globox(t,u,h,f['axis']),key,parent)
def sig(r):return {'drivers':[(d.data_path,d.array_index,d.driver.expression) for d in (r.animation_data.drivers if r.animation_data else [])],'action':r.animation_data.action.name if r.animation_data and r.animation_data.action else None,'rotation_mode':r.rotation_mode,'scale':list(r.scale)}
rigs=[o for o in S.objects if o.name.startswith('DOOR |')];rig_before={r.name:sig(r) for r in rigs}
F=[{'id':'L','rig':'DOOR | balconySide','axis':'z','lower':'Corrediza lateral A marco inferior','upper':'Corrediza lateral A marco superior','static_prefix':['Marco corrediza lateral','Corrediza lateral |'],'fixedprefix':'Corrediza lateral B'}, {'id':'A','rig':'DOOR | balconyRear_A','axis':'x','lower':'Hoja posterior A | perfil móvil.001','upper':'Hoja posterior A | perfil móvil','static_prefix':['Corrediza posterior A marco','Marco corrediza posterior A'],'fixedprefix':'Corrediza posterior A'}, {'id':'B','rig':'DOOR | balconyRear_B','axis':'x','lower':'Hoja posterior B | perfil móvil.001','upper':'Hoja posterior B | perfil móvil','static_prefix':['Corrediza posterior B marco','Marco corrediza posterior B'],'fixedprefix':'Corrediza posterior B'}]
hosts=[o.name for o in S.objects if o.type=='MESH' and any(s in o.name.lower() for s in ['losa entre','balcón lateral','balcón posterior','piso vivienda','umbral','dintel','alféizar','goterón interior balcón','acabado balcón','base adherida balcón'])]
original_bounds={};original_glass={};reports=[];support_pairs=[];handle_changes=[]
# Obsolete continuous120mm 'stops' blocked the complete sill. Replace with local buffers.
for name in ['Tope corrediza lateral','Tope corrediza posterior','Manija corrediza lateral B','Manija corrediza posterior A | paño fijo','Manija corrediza posterior B | paño fijo']:
 o=bpy.data.objects.get(name)
 if o:handle_changes.append({'object':name,'action':'removed obsolete fixed handle/continuous stop'});bpy.data.objects.remove(o,do_unlink=True)

for f in F:
 print('SL95 FAMILY',f['id'],flush=True);S.frame_set(1);bpy.context.view_layer.update();r=bpy.data.objects[f['rig']];axis=f['axis'];cross='z' if axis=='x' else 'x'
 originals=[o for o in r.children_recursive if o.type=='MESH'];f['originals']=[o.name for o in originals];original_bounds[f['id']]={o.name:bounds(o) for o in originals}
 for o in originals:
  if 'vidrio' in o.name.lower():original_glass[o.name]=[list(v.co) for v in o.data.vertices]
 states=[]
 for frame in [1,45,67,90,105]:
  S.frame_set(frame);bpy.context.view_layer.update();states.extend(bounds(o) for o in originals if 'manija' not in o.name.lower())
 lane={k:[min(b[k][0] for b in states)-.003,max(b[k][1] for b in states)+.003] for k in 'xyz'};S.frame_set(1);bpy.context.view_layer.update()
 if axis=='x':lane[cross][1]+=.008 # rear retention beads extend8mm past original glazing
 low=bounds(bpy.data.objects[f['lower']]);up=bounds(bpy.data.objects[f['upper']]);bf=low['y'][0];wheel_u=sum(low[cross])/2;track=bf-.003;t=lane[axis];u=lane[cross];bed=track-.008;panbottom=track-.005;pantop=track-.002
 # Reposition existing handles onto closing stiles; retain the same rig and travel.
 hn='Manija corrediza lateral A' if f['id']=='L' else 'Manija corrediza posterior '+f['id']
 hand=bpy.data.objects.get(hn)
 if hand:
  hb=bounds(hand);hc=Vector(tuple(sum(hb[k])/2 for k in 'xyz'));ht=low[axis][0]+(.082 if axis=='z' else .0);hu=low[cross][0]-.040
  # The rear lower member starts at the glass edge; lateral82mm includes its projecting end.
  target=Vector(xyz(ht,hu,hc.y,axis));mw=hand.matrix_world.copy();mw.translation+=cv(target-hc);hand.matrix_world=mw;child(hand,r)
  handle_changes.append({'object':hn,'old_bounds':hb,'new_bounds':bounds(hand),'rig':r.name})
  for h in [4.32,4.64]:cylinder('SL95 | '+f['id']+' soporte manija',xyz(ht,hu+.022,h,axis),xyz(ht,low[cross][0]+.006,h,axis),.005,'stainless',r)
 statics=[o.name for o in S.objects if o.type=='MESH' and o.name not in f['originals'] and any(o.name.startswith(p) for p in f['static_prefix'])]
 reserve(statics,lane,f['id']+' vaciado de marcos fijos')
 lr=globox([t[0]-.003,t[1]+.003],[u[0]-.004,u[1]+.004],[bed,3.28],axis);ur=globox([t[0]-.003,t[1]+.003],[u[0]-.004,u[1]+.004],[up['y'][0]-.003,up['y'][1]+.006],axis)
 reserve(hosts+statics,lr,f['id']+' cajeado pista inferior');reserve(hosts+statics,ur,f['id']+' cajeado guía superior')
 gb('lecho continuo3mm',t,[u[0]-.003,u[1]+.003],[bed,panbottom],f,'grout');gb('bandeja base3mm',t,[u[0]-.003,u[1]+.003],[panbottom,pantop],f,'stainless');gb('carril rodadura8x2mm',t,[wheel_u-.004,wheel_u+.004],[pantop,track],f,'stainless')
 for side,uu in [('i',[u[0]-.003,u[0]]),('e',[u[1],u[1]+.003])]:gb('bandeja pared '+side,t,uu,[pantop,3.27],f)
 for q,tt in [('inicio',[t[0]-.003,t[0]]),('fin',[t[1],t[1]+.003])]:gb('bandeja cierre '+q,tt,[u[0]-.003,u[1]+.003],[panbottom,3.27],f)
 top=up['y'][1]+.003;gb('guía superior techo3mm',t,[u[0]-.003,u[1]+.003],[top,top+.003],f)
 for side,uu in [('i',[u[0]-.003,u[0]]),('e',[u[1],u[1]+.003])]:gb('guía superior ala '+side,t,uu,[up['y'][0]-.003,top],f)
 for edge,tt in [('inicio',[t[0]-.018,t[0]-.003]),('fin',[t[1]+.003,t[1]+.018])]:gb('jamba portaguía '+edge,tt,[u[0]-.003,u[1]+.003],[3.27,top+.003],f)
 for j,frac in enumerate([.20,.80],1):
  wt=low[axis][0]+frac*(low[axis][1]-low[axis][0]);reserve([f['lower']],globox([wt-.013,wt+.013],[wheel_u-.007,wheel_u+.007],[bf-.001,bf+.018],axis),f['id']+f' alojamiento rodillo{j}');center=track+.010
  wheel=cylinder('SL95 | '+f['id']+f' rodillo{j} diámetro20',xyz(wt,wheel_u-.004,center,axis),xyz(wt,wheel_u+.004,center,axis),.010,'polymer',r,inner=.0021)
  cylinder('SL95 | '+f['id']+f' eje{j} diámetro4',xyz(wt,wheel_u-.010,center,axis),xyz(wt,wheel_u+.010,center,axis),.002,'stainless',r);fc=wheel.driver_add('delta_rotation_euler',2);var=fc.driver.variables.new();var.name='opening';var.type='SINGLE_PROP';var.targets[0].id=r;var.targets[0].data_path='["open"]';travel=(lane[axis][1]-lane[axis][0])-(low[axis][1]-low[axis][0])-.006;fc.driver.expression=f'opening * {travel/.010*(1 if axis=="z" else -1):.9f}';support_pairs.append({'family':f['id'],'object':wheel.name,'contact_height':track,'rail_top':track,'roller_diameter_mm':20})
 # Local elastomer stops contact the bottom member at closed and fully open positions.
 for label,tt in [('cierre',[t[0]-.003,t[0]+.003]),('abierto',[t[1]-.003,t[1]+.003])]:gb('tope elástico '+label,tt,[wheel_u-.016,wheel_u+.016],[bf+.050,bf+.070],f,'rubber95')
 glasses=[o for o in originals if 'vidrio' in o.name.lower()];frames=[o.name for o in originals if ('marco' in o.name.lower() or 'perfil móvil' in o.name.lower())];glazing=[]
 for gi,g in enumerate(glasses,1):
  b=bounds(g);gt=b[axis];gu=b[cross];bottom=b['y'][0];reserve(frames,globox([gt[0]-.002,gt[1]+.002],[gu[0]-.002,gu[1]+.002],[bottom-.006,b['y'][1]+.002],axis),f['id']+f' galce vidrio{gi}')
  if axis=='x':gb(f'apoyo vidrio{gi} ménsula continua',gt,[low[cross][0]+.010,gu[1]+.002],[bottom-.010,bottom-.006],f,'blackMetal',r)
  for j,frac in enumerate([.25,.75],1):
   ct=gt[0]+frac*(gt[1]-gt[0]);gb(f'taco vidrio{gi}-{j} 100mm',[ct-.05,ct+.05],[gu[0]-.001,gu[1]+.001],[bottom-.006,bottom],f,'rubber95',r)
  for side,uu in [('a',[gu[0]-.002,gu[0]]),('b',[gu[1],gu[1]+.002])]:
   gb(f'junta vidrio{gi} inferior{side}',gt,uu,[bottom,bottom+.012],f,'rubber95',r);gb(f'junta vidrio{gi} superior{side}',gt,uu,[b['y'][1]-.012,b['y'][1]],f,'rubber95',r)
   for edge,tt in [('i',[gt[0],gt[0]+.010]),('f',[gt[1]-.010,gt[1]])]:gb(f'junta vidrio{gi} lateral{side}{edge}',tt,uu,[bottom+.012,b['y'][1]-.012],f,'rubber95',r)
  glazing.append({'glass':g.name,'bottom_m':bottom,'setting_block_height_mm':6,'setting_block_length_mm':100,'positions_fraction':[.25,.75],'pocket_clearance_mm':2})
 # Rear glazing retainers connect the existing front members to both panes.
 if axis=='x':
  glassbs=[bounds(g) for g in glasses];gt=[min(b[axis][0] for b in glassbs),max(b[axis][1] for b in glassbs)];gu=[min(b[cross][0] for b in glassbs),max(b[cross][1] for b in glassbs)];gh=[min(b['y'][0] for b in glassbs),max(b['y'][1] for b in glassbs)]
  for label,uu in [('frente',[low[cross][1],gu[0]-.002]),('dorso',[gu[1]+.002,gu[1]+.008])]:
   for edge,hh in [('base',[gh[0]-.006,gh[0]+.012]),('cabeza',[gh[1]-.012,gh[1]+.002])]:gb('junquillo '+label+' '+edge,[gt[0]-.002,gt[1]+.002],uu,hh,f,'blackMetal',r)
   for edge,tt in [('i',[gt[0]-.002,gt[0]+.010]),('f',[gt[1]-.010,gt[1]+.002])]:gb('junquillo '+label+' '+edge,tt,uu,[gh[0]+.012,gh[1]-.012],f,'blackMetal',r)
  for edge,tt in [('i',[gt[0]-.020,gt[0]-.002]),('f',[gt[1]+.002,gt[1]+.020])]:gb('retorno montante '+edge,tt,[low[cross][0]+.010,gu[1]+.008],gh,f,'blackMetal',r)
  gb('puente superior acristalamiento',gt,[low[cross][0]+.010,gu[1]+.008],[gh[1]+.002,gh[1]+.006],f,'blackMetal',r)
 fixedglasses=[o for o in S.objects if o.type=='MESH' and o.name.startswith(f['fixedprefix']) and 'vidrio' in o.name.lower() and o.name not in f['originals']];fixedframes=[o.name for o in S.objects if o.type=='MESH' and o.name.startswith(f['fixedprefix']) and 'marco' in o.name.lower() and o.name not in f['originals']]
 for gi,g in enumerate(fixedglasses,1):
  b=bounds(g);gt=b[axis];gu=b[cross];bottom=b['y'][0];reserve(fixedframes,globox([gt[0]-.002,gt[1]+.002],[gu[0]-.002,gu[1]+.002],[bottom-.006,b['y'][1]+.002],axis),f['id']+f' galce fijo vidrio{gi}')
  for j,frac in enumerate([.25,.75],1):
   ct=gt[0]+frac*(gt[1]-gt[0]);gb(f'fijo taco vidrio{gi}-{j}',[ct-.05,ct+.05],[gu[0]-.001,gu[1]+.001],[bottom-.006,bottom],f,'rubber95')
  if axis=='x':gb(f'fijo apoyo exterior vidrio{gi}',gt,[u[1],gu[1]+.002],[bottom-.010,bottom-.006],f)
 if axis=='x' and fixedglasses:
  bs=[bounds(g) for g in fixedglasses];ft=[min(b[axis][0] for b in bs),max(b[axis][1] for b in bs)];fu=[min(b[cross][0] for b in bs),max(b[cross][1] for b in bs)];fh=[min(b['y'][0] for b in bs),max(b['y'][1] for b in bs)]
  for label,uu in [('frente',[fu[0]-.008,fu[0]-.002]),('dorso',[fu[1]+.002,fu[1]+.008])]:
   for edge,hh in [('base',[fh[0]-.006,fh[0]+.012]),('cabeza',[fh[1]-.012,fh[1]+.002])]:gb('fijo junquillo '+label+' '+edge,[ft[0]-.002,ft[1]+.002],uu,hh,f)
   for edge,tt in [('i',[ft[0]-.002,ft[0]+.010]),('f',[ft[1]-.010,ft[1]+.002])]:gb('fijo junquillo '+label+' '+edge,tt,uu,[fh[0]+.012,fh[1]-.012],f)
  for edge,tt in [('i',[ft[0]-.020,ft[0]-.002]),('f',[ft[1]+.002,ft[1]+.020])]:gb('fijo retorno '+edge,tt,[u[1],fu[1]+.008],fh,f)
  gb('fijo puente superior',ft,[u[1],fu[1]+.008],[fh[1]+.002,fh[1]+.006],f)
 for name in fixedframes:
  b=bounds(bpy.data.objects[name]);casing={k:[v[0]-.001,v[1]+.001] for k,v in b.items()};reserve(hosts,casing,f['id']+' alojamiento marco fijo '+name)
  if 'inferior' not in name:continue
  b=bounds(bpy.data.objects[name]);seat={k:list(v) for k,v in b.items()};seat['y']=[b['y'][0]-.003,b['y'][0]];reserve(hosts,seat,f['id']+' asiento marco fijo');box('SL95 | '+f['id']+' asiento marco fijo3mm',seat,'grout')
 drains=[]
 for j,dt in enumerate([t[0]+.28,t[1]-.28],1):
  outeru=u[0]+.013 if axis=='z' else u[1]-.013;endu=12.99 if axis=='z' else 13.01;startheight=pantop-.016;length=abs(endu-outeru);endheight=startheight-.02*length
  start=xyz(dt,outeru,startheight,axis);end=xyz(dt,endu,endheight,axis);a=xyz(dt,outeru,pantop+.001,axis);b=xyz(dt,outeru,startheight,axis);segments=[(a,b),(start,end)]
  for label,(p,q) in zip(['vertical','salida'],segments):
   cutter=cylinder('TMP drain',p,q,.008);candidates=hosts+statics+[o.name for o in COL.objects if o.name.startswith('SL95 | '+f['id']) and not o.parent and 'drenaje' not in o.name];done=[]
   for name in dict.fromkeys(candidates):
    ob=bpy.data.objects.get(name)
    if ob and ob!=cutter and ob.type=='MESH' and overlap(bounds(ob),bounds(cutter)):boolean(ob,cutter);done.append(name)
   bpy.data.objects.remove(cutter,do_unlink=True);operations.append({'reservation':f['id']+f' drain{j} '+label,'start':p,'end':q,'diameter_mm':16,'objects':done})
  tube=cylinder('SL95 | '+f['id']+f' drenaje{j} Ø14 interior10',a,b,.007);arm=cylinder('TMP drain arm',start,end,.007);boolean(tube,arm,'UNION');bpy.data.objects.remove(arm,do_unlink=True)
  for p,q in segments:
   pa,pb=cv(p),cv(q);v=(pb-pa).normalized();c=cylinder('TMP bore',src(pa-v*.012),src(pb+v*.012),.005);boolean(tube,c);bpy.data.objects.remove(c,do_unlink=True)
  cylinder('SL95 | '+f['id']+f' sello drenaje{j}',xyz(dt,outeru,pantop-.002,axis),xyz(dt,outeru,pantop,axis),.010,'rubber95',inner=.007)
  drains.append({'start':start,'outlet':end,'slope_percent':2,'outer_diameter_mm':14,'inner_diameter_mm':10,'note':'P reserva por coordinar con armado; descarga a cara libre del balcón'})
 reports.append({'family':f['id'],'rig':f['rig'],'source_lane':lane,'lower_reservation':lr,'upper_reservation':ur,'rolling_height_m':track,'glazing':glazing,'drains':drains,'static_objects':statics})
S.frame_set(1);bpy.context.view_layer.update();preserved=[]
for f in F:
 for n,b in original_bounds[f['id']].items():
  now=bounds(bpy.data.objects[n]);err=max(abs(now[k][i]-b[k][i]) for k in 'xyz' for i in [0,1]);preserved.append({'object':n,'envelope_error_m':err})
  if err>2e-5 and 'Manija' not in n:raise RuntimeError('Exterior envelope changed: '+n+' '+str(err))
for n,vertices in original_glass.items():
 if vertices!=[list(v.co) for v in bpy.data.objects[n].data.vertices]:raise RuntimeError('Glass geometry changed: '+n)
assert {r.name:sig(r) for r in rigs}==rig_before,'Rig definition changed'
assert len([o for o in S.objects if o.name.startswith('DOOR |')])==len(rigs),'Rig count changed'
S['sliding_windows_r5']='P: hollow channels, measured glass pockets, Ø20 rollers, EPDM supports and drained pans. Loads, reinforcement and product selection require design.';S['review_iteration']='95 / R5B three balcony sliding assemblies';S.frame_set(1);bpy.context.view_layer.update();bpy.context.preferences.filepaths.save_version=0
out=Path(args.out).resolve();out.parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
report={'source_model':str(source),'source_sha256':source_sha,'model':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'coordinates':'source metres X,Yheight,Zdepth','status':'P geometry proposed; no capacity, lifecycle, waterproofing or regulatory certification','rig_count':len(rigs),'rig_definitions_preserved':True,'original_glass_vertices_preserved':True,'original_exterior_envelopes':preserved,'families':reports,'handle_changes':handle_changes,'bearing_pairs':support_pairs,'reservations':operations,'limitations':['Roller/material selection and capacities require manufacturer verification.','Localized slab and head recesses/drain bores require coordination with structural reinforcement and calculations.','No water test, thermal/acoustic calculation or installation certification is represented.']}
p=Path(args.report).resolve();p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8');print('SLIDING_R5_COMPLETE',str(out),'SHA',report['sha256'],'RIGS',len(rigs),'RESERVATIONS',len(operations),flush=True)
