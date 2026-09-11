"""CPU-only R8 affected geometry, contact and declared use scenarios; read-only source."""
import bpy,bmesh,json,math,hashlib,ast,sys,argparse
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(r'D:/2026/42');S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();model=Path(bpy.data.filepath);SHA=hashlib.sha256(model.read_bytes()).hexdigest();meta=json.loads(S['r8_uso_details'])
ap=argparse.ArgumentParser();ap.add_argument('--out',default='review99/r8_uso');ap.add_argument('--expected-sha');ar=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
if ar.expected_sha and SHA!=ar.expected_sha.lower():raise RuntimeError('Use evidence source SHA mismatch')
out=(R/ar.out).resolve()
if R not in out.parents or R/'docs' in out.parents:raise ValueError('Use QA output must be local, outside docs')
out.mkdir(parents=True,exist_ok=True)
for node in ast.parse((R/'scripts/planos95_juntas_check.py').read_text('utf8')).body:
 if isinstance(node,ast.FunctionDef) and node.name in ['bounds','overlap','vol']:exec(compile(ast.Module(body=[node],type_ignores=[]),'<helper>','exec'),globals())

def sb(o):
 p=[o.matrix_world@Vector(v) for v in o.bound_box];return {'x':[min(q.x for q in p),max(q.x for q in p)],'h':[min(q.z for q in p),max(q.z for q in p)],'z':[min(-q.y for q in p),max(-q.y for q in p)]}
allsource=[o for o in S.objects if o.type=='MESH' and not o.hide_render]
# Copy evaluated world-space geometry to a small CPU collision scene. Broad phase
# includes every active source object overlapping either complete use envelope.
regions_source=[{'x':[15.0,18.5],'h':[.20,2.0],'z':[1.75,4.10]}, {'x':[17.45,19.75],'h':[3.24,4.75],'z':[1.30,4.70]}]
def near(o):
 b=sb(o)
 return any(all(min(b[k][1],r[k][1])-max(b[k][0],r[k][0])>=0 for k in ['x','h','z']) for r in regions_source)
selected=[o for o in allsource if near(o) or o.name in meta['created_objects'] or o.name in meta['changed_objects']]
original_scene=S;collision=bpy.data.scenes.new('R8 isolated evaluated QA');dg=bpy.context.evaluated_depsgraph_get();allob=[]
for o in selected:
 n=o.name;eo=o.evaluated_get(dg);me=bpy.data.meshes.new_from_object(eo);me.transform(eo.matrix_world);o.name='R8 source retained | '+n;q=bpy.data.objects.new(n,me);collision.collection.objects.link(q);allob.append(q)
S=collision;bpy.context.window.scene=S;bpy.context.view_layer.update();bb={o.name:bounds(o) for o in allob};probes=[];rows=[];tests=[]
broadphase={'active_source_meshes':len(allsource),'evaluated_candidates':len(allob),'complete_use_regions_source':regions_source,'scope':'Every active evaluated mesh overlapping the union; omitted boxes are disjoint from complete affected object and body travel envelopes.'}
print('USE_SCOPE',broadphase,flush=True)
def mesh(n,v,f):
 m=bpy.data.meshes.new(n);m.from_pydata([(x,-z,h) for x,h,z in v],[],f);bm=bmesh.new();bm.from_mesh(m);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-8);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(m);bm.free();o=bpy.data.objects.new(n,m);S.collection.objects.link(o);probes.append(o);return o

def box(n,x,h,z):return mesh('USE PROBE '+n,[(xx,hh,zz) for hh in h for zz in z for xx in x],[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)])
def ellipsoid(n,p,rad):
 bm=bmesh.new();bmesh.ops.create_uvsphere(bm,u_segments=24,v_segments=12,radius=1);m=bpy.data.meshes.new(n)
 for v in bm.verts:v.co=Vector((p[0]+v.co.x*rad[0],-p[2]+v.co.y*rad[2],p[1]+v.co.z*rad[1]))
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(m);bm.free();o=bpy.data.objects.new('USE PROBE '+n,m);S.collection.objects.link(o);probes.append(o);return o

def capsule(n,a,b,rad):
 av,bv=Vector(a),Vector(b);axis=(bv-av).normalized();u=axis.cross(Vector((0,1,0)))
 if u.length<.1:u=axis.cross(Vector((1,0,0)))
 u.normalize();v=axis.cross(u).normalized();pts=[];N=20
 # Hemisphere rings include endpoint tips, yielding a closed convex capsule.
 rings=[]
 for k in range(6):
  t=-math.pi/2+k*math.pi/10;r=rad*math.cos(t);c=av+axis*rad*math.sin(t);rings.append((c,r))
 for k in range(6):
  t=k*math.pi/10;r=rad*math.cos(t);c=bv+axis*rad*math.sin(t);rings.append((c,r))
 for c,r in rings:
  pts.extend([tuple(c+r*(u*math.cos(i*math.tau/N)+v*math.sin(i*math.tau/N))) for i in range(N)])
 f=[]
 for j in range(len(rings)-1):
  for i in range(N):q=(i+1)%N;f.append((j*N+i,j*N+q,(j+1)*N+q,(j+1)*N+i))
 f.extend([tuple(reversed(range(N))),tuple((len(rings)-1)*N+i for i in range(N))]);return mesh('USE PROBE '+n,pts,f)
def test(n,objs,targets=allob,exclude=()):
 bpy.context.view_layer.update();pairs=0;hits=[]
 for a in objs:
  ab=bounds(a)
  for b in targets:
   if b.name in exclude or a==b or not overlap(ab,bb[b.name]):continue
   value=vol(a,b);pairs+=1
   if value>1e-8:hits.append({'probe':a.name,'object':b.name,'volume_m3':value})
 row={'scenario':n,'pairs':pairs,'hits':hits,'pass':not hits};rows.append(row);(out/'check_progress.json').write_text(json.dumps({'sha256':SHA,'rows':rows},ensure_ascii=False,indent=2),'utf8');print('USE_CHECK',n,pairs,len(hits),flush=True);return row

def capture(o):
 return {'name':o.name,'bounds':sb(o),'v':[[p.x,p.z,-p.y] for p in [o.matrix_world@v.co for v in o.data.vertices]],'f':[list(p.vertices) for p in o.data.polygons]}
# All new frame/tray parts versus actual retained scene; weld contacts individually labelled.
new=[S.objects[n] for n in meta['created_objects']];targets=[o for o in allob if o.name not in meta['created_objects']];test('new construction versus retained scene',new,targets)
internal=[];intpairs=0;allowed_weld=[]
for i,a in enumerate(new):
 for b in new[i+1:]:
  if not overlap(bounds(a),bounds(b)):continue
  value=vol(a,b);intpairs+=1
  if value>1e-8:
   if 'cordon soldadura' in a.name or 'cordon soldadura' in b.name:allowed_weld.append([a.name,b.name,value])
   else:internal.append([a.name,b.name,value])
rows.append({'scenario':'new construction internal','pairs':intpairs,'hits':internal,'intended_weld_intersections':allowed_weld,'pass':not internal});print('USE_CHECK internal',intpairs,len(internal),flush=True)
# Actual support contacts: ray in both directions at pad/plate interfaces.
dg=bpy.context.evaluated_depsgraph_get();trees={}
def tree(o):
 if o.name not in trees:
  eo=o.evaluated_get(dg);me=eo.to_mesh();trees[o.name]=BVHTree.FromPolygons([eo.matrix_world@v.co for v in me.vertices],[list(p.vertices) for p in me.polygons]);eo.to_mesh_clear()
 return trees[o.name]
contacts=[]
def contact(label,lower,upper,points):
 for x,z,h in points:
  dn=tree(lower).ray_cast(Vector((x,-z,h+.01)),Vector((0,0,-1)),.1)[0];up=tree(upper).ray_cast(Vector((x,-z,h-.01)),Vector((0,0,1)),.1)[0]
  gap=up.z-dn.z if up is not None and dn is not None else None;contacts.append({'label':label,'objects':[lower.name,upper.name],'point_source':[x,h,z],'gap_m':gap,'pass':gap is not None and abs(gap)<.00002})
for n in meta['created_objects']:
 o=S.objects[n];b=sb(o)
 if 'MIDI apoyo elastomerico' in n:
  x=sum(b['x'])/2;z=sum(b['z'])/2;contact('controller-pad',o,S.objects['Controlador estudio'],[(x,z,b['h'][1])]);contact('pad-tray',S.objects['USO99 | MIDI bandeja18'],o,[(x,z,b['h'][0])])
 if 'MIDI placa asiento base' in n:
  for x in [18.25,18.45]:contact('MIDI plate-existing base',S.objects['Base consola estudio'],o,[(x,sum(b['z'])/2,b['h'][0])])
 if 'isla asiento elastomerico tapa' in n:
  for x in [16.0,16.35,16.82,17.29,17.65]:contact('island pad-counter',o,S.objects['Isla cocina mono tapa'],[(x,sum(b['z'])/2,b['h'][1])])
for k,z in enumerate([2.430,3.570]):
 arm=S.objects[f'USO99 | MIDI brazo40x30 {k}'];calce=S.objects[f'USO99 | MIDI calce8 {k}'];plate=S.objects[f'USO99 | MIDI placa asiento base {k}']
 contact('tray-arm',arm,S.objects['USO99 | MIDI bandeja18'],[(x,z,3.915) for x in [18.52,18.72,18.9]])
 contact('arm-spacer',calce,arm,[(x,z,3.875) for x in [18.28,18.45]])
 contact('spacer-rootplate',plate,calce,[(x,z,3.867) for x in [18.28,18.45]])
for k,z in enumerate([2.430,3.570]):
 for side in [-1,1]:
  contact('root weld-existing steel',S.objects['Base consola estudio'],S.objects[f'USO99 | MIDI soldadura base {k} {side}'],[(x,z+side*.031,3.863) for x in [18.28,18.45]])
for k,z in enumerate([3.365,3.940]):
 rail=S.objects[f'USO99 | isla travesano superior {k}'];pad=S.objects[f'USO99 | isla asiento elastomerico tapa {k}']
 contact('island steel-elastomer',rail,pad,[(x,z,1.072) for x in [16.1,16.35,16.82,17.29,17.55]])
rows.append({'scenario':'measured support interfaces','samples':len(contacts),'hits':[r for r in contacts if not r['pass']],'pass':all(r['pass'] for r in contacts)})
test('changed MIDI assembly versus retained console and base',[S.objects[n] for n in meta['midi']['controller_family']], [S.objects[n] for n in ['Consola estudio','Base consola estudio']])
# Declared knee envelopes plus600mm sensitivity to pelvis-front distance.
knees=[]
for i,x in enumerate([16.35,17.29]):
 knees.append(box(f'island seat{i} 610x381 knee reserve',[x-.305,x+.305],[.90,1.02],[3.32,3.701]))
 for side in [-1,1]:knees.append(box(f'island seat{i} long knee{side}',[x+side*.10-.06,x+side*.10+.06],[.90,1.02],[3.24,3.65]))
test('island two knee reserves and600mm sensitivity',knees)
# Seated island body: explicit adult trial, pelvis atseat, feet on front stoolrail.
island_bodies=[]
for k,x in enumerate([16.35,17.29]):
 o=[];o+=[ellipsoid(f'diner{k} pelvis',(x,.940,3.05),(.17,.08,.14)),capsule(f'diner{k} torso',(x,1.00,3.03),(x,1.43,3.03),.115),ellipsoid(f'diner{k} head',(x,1.67,3.03),(.105,.13,.105))]
 for side in [-1,1]:
  xx=x+side*.10;o.append(capsule(f'diner{k} thigh{side}',(xx,.94,3.13),(xx,.94,3.49),.065));o.append(capsule(f'diner{k} calf{side}',(xx,.92,3.49),(xx,.485,3.24),.045));o.append(box(f'diner{k} foot{side}',[xx-.045,xx+.045],[.410,.465],[3.165,3.425]))
  ax=x+side*.19;o.append(capsule(f'diner{k} upperarm{side}',(ax,1.43,3.03),(ax,1.16,3.03),.035));o.append(capsule(f'diner{k} forearm{side}',(ax,1.16,3.10),(ax,1.16,3.42),.030))
 island_bodies+=o;test('seated island diner'+str(k),o)
# Passage behind both occupied seats, cylinder450x1720, whole retained scene + both bodies.
bodybb={o.name:bounds(o) for o in island_bodies};bb.update(bodybb)
passage=[]
for i in range(15):
 x=15.20+i*(18.20-15.20)/14;passage.append(capsule('rear passage'+str(i),(x,.436,2.37),(x,1.704,2.37),.225))
test('rear passage behind two diners diameter450',passage,allob+island_bodies)
# Withdraw each stool450mm, while the other diner remains seated. Check21positions.
withdraw=[]
for k,prefix in enumerate(['Taburete isla mono A |','Taburete isla mono B |']):
 group=[o for o in allob if o.name.startswith(prefix)];others=[o for o in allob if o not in group];otherbody=[o for o in island_bodies if not o.name.startswith('USE PROBE diner'+str(k))];original=[o.location.copy() for o in group]
 hits=[];pairs=0
 for step in range(21):
  for o,v in zip(group,original):o.location=v+Vector((0,.45*step/20,0))
  bpy.context.view_layer.update()
  if step%5==0:print('STOOL_POSE',k,step,flush=True)
  for a in group:
   ab=bounds(a)
   for b in others+otherbody:
    if not overlap(ab,bb[b.name]):continue
    value=vol(a,b);pairs+=1
    if value>1e-8:hits.append([step,a.name,b.name,value])
 # Standing/side approach via central gap into seat-front pocket after withdrawal.
 stand=[]
 for j in range(7):
  z=2.37+(3.05-2.37)*j/6;stand.append(capsule(f'entry{k}_rear{j}',(16.82,.436,z),(16.82,1.704,z),.225))
 for j in range(11):
  x=16.82+( [16.35,17.29][k]-16.82)*j/10;stand.append(capsule(f'entry{k}_{j}',(x,.436,3.05),(x,1.704,3.05),.225))
 bb.update({o.name:bounds(o) for o in group});test('entry standing to seat'+str(k),stand,others+group+otherbody)
 for o,v in zip(group,original):o.location=v
 bpy.context.view_layer.update();bb.update({o.name:bounds(o) for o in group});withdraw.append({'seat':k,'positions':21,'pairs':pairs,'hits':hits,'pass':not hits})
rows.append({'scenario':'stool withdrawal450mm','seats':withdraw,'hits':[h for r in withdraw for h in r['hits']],'pass':all(r['pass'] for r in withdraw)})
# MIDI operator primary pose, fixed470mm seat; elbow280mm above seat.
operator=[]
operator.append(ellipsoid('MIDI pelvis',(19.085,3.790,3.00),(.14,.07,.16)))
operator.append(capsule('MIDI torso',(19.10,3.86,3),(19.10,4.27,3),.105));operator.append(ellipsoid('MIDI head',(19.10,4.51,3),(.11,.135,.10)))
for side in [-1,1]:
 z=3+side*.115;operator.append(capsule('MIDI thigh'+str(side),(19.06,3.79,z),(18.62,3.79,z),.060));operator.append(capsule('MIDI calf'+str(side),(18.62,3.74,z),(18.64,3.354,z),.045));operator.append(box('MIDI foot'+str(side),[18.40,18.68],[3.259,3.319],[z-.050,z+.050]));zz=3+side*.195
 operator.append(capsule('MIDI upperarm'+str(side),(19.105,4.255,zz),(19.220,4.000,3+side*.235),.033));operator.append(capsule('MIDI forearm'+str(side),(19.220,4.000,3+side*.235),(18.975,4.018,zz),.025));operator.append(mesh('USE PROBE MIDI hand'+str(side),[(x,h,zv) for zv in [zz-.035,zz+.035] for x,h in [(18.81,4.000),(18.96,4.015),(18.96,4.042),(18.81,4.024)]],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]))
test('MIDI primary seated operator',operator)
# Real contacts of the selected trial bodies with seats, footrests and keys.
body_contacts=[]
def body_support(label,body,x,z,h):
 bpy.context.view_layer.update();found=[]
 for o in allob:
  b=bb[o.name]
  if not(b[0][0]-1e-6<=x<=b[1][0]+1e-6 and b[0][1]-1e-6<=-z<=b[1][1]+1e-6 and b[0][2]<=h+.005 and b[1][2]>=h-.1):continue
  q=tree(o).ray_cast(Vector((x,-z,h+.005)),Vector((0,0,-1)),.12)[0]
  if q is not None:found.append((q.z,o.name))
 found.sort(reverse=True);up=tree(body).ray_cast(Vector((x,-z,h-.02)),Vector((0,0,1)),.05)[0]
 gap=up.z-found[0][0] if up is not None and found else None
 body_contacts.append({'label':label,'body':body.name,'point_source':[x,h,z],'support':found[0] if found else None,'gap_m':gap,'contact_tolerance_m':.0001,'pass':gap is not None and abs(gap)<.0001})
for k,x in enumerate([16.35,17.29]):
 body_support('seated pelvis',next(o for o in island_bodies if o.name==f'USE PROBE diner{k} pelvis'),x,3.05,.86)
 for side in [-1,1]:body_support('feet on stool rail',next(o for o in island_bodies if o.name==f'USE PROBE diner{k} foot{side}'),x+side*.1,3.2025,.410)
body_support('MIDI pelvis on seat',next(o for o in operator if o.name=='USE PROBE MIDI pelvis'),19.085,3,3.72)
for side in [-1,1]:
 body_support('MIDI feet on rug actual top',next(o for o in operator if o.name==f'USE PROBE MIDI foot{side}'),18.50,3+side*.115,3.259)
 body_support('MIDI fingertips on white keys',next(o for o in operator if o.name==f'USE PROBE MIDI hand{side}'),18.81001,2.808 if side<0 else 3.192,4.0)
rows.append({'scenario':'trial body support contacts','samples':len(body_contacts),'hits':[r for r in body_contacts if not r['pass']],'pass':all(r['pass'] for r in body_contacts)})
# Vertical knee headroom on actual tray:12 rays.
rayitems=[]
for x in [18.52,18.65,18.8,18.9]:
 for z in [2.65,3,3.35]:
  hits=[]
  for o in allob:
   b=bb[o.name]
   if not(b[0][0]<=x<=b[1][0] and b[0][1]<=-z<=b[1][1]) or b[1][2]<3.85:continue
   q=tree(o).ray_cast(Vector((x,-z,3.860)),Vector((0,0,1)),.3)[0]
   if q is not None:hits.append((q.z,o.name))
  hits.sort();rayitems.append({'x':x,'z':z,'first':hits[0] if hits else None,'above_floor':hits[0][0]-3.25 if hits else None})
rows.append({'scenario':'MIDI headroom665mm all12rays','hits':[r for r in rayitems if not r['first'] or abs(r['above_floor']-.665)>.00002],'pass':all(r['first'] and abs(r['above_floor']-.665)<.00002 for r in rayitems)})
# Mesh manifold check of new fabricated elements.
meshchecks=[]
for o in new:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);v=abs(bm.calc_volume());bm.free();meshchecks.append({'name':o.name,'nonmanifold_edges':bad,'volume_m3':v})
rows.append({'scenario':'new construction closed meshes','hits':[r for r in meshchecks if r['nonmanifold_edges'] or r['volume_m3']<1e-10],'pass':all(not r['nonmanifold_edges'] and r['volume_m3']>1e-10 for r in meshchecks)})
# Focused mesh extraction for the two local use sections.
focus=[o for o in allob if o.name in meta['changed_objects'] or o.name in meta['created_objects'] or o.name.startswith(('Silla estudio','Consola estudio','Base consola estudio','Isla cocina mono','Taburete isla mono'))]
(out/'geometry.json').write_text(json.dumps({'model':str(model),'sha256':SHA,'axes':'X,H,Z','objects':[capture(o) for o in focus],'operator':[capture(o) for o in operator],'diners':[capture(o) for o in island_bodies]},ensure_ascii=False),'utf8')
result={'model':str(model),'sha256':SHA,'broad_phase':broadphase,'status':'PASS' if all(r['pass'] for r in rows) else 'FAIL','rows':rows,'support_contacts':contacts,'body_support_contacts':body_contacts,'midi_headroom_rays':rayitems,'new_meshes':meshchecks,'operator_dimensions':{'MIDI_seat_m':.470,'MIDI_pelvis_offset_forward_from_seat_centre_m':.015,'MIDI_rug_top_above_NPT_m':.009,'MIDI_relaxed_elbow_from_seat_m':.280,'MIDI_forearm_axis_rise_m':.018,'MIDI_forearm_axis_run_m':.245,'MIDI_forearm_axis_lateral_offset_m':.040,'MIDI_upper_arm_axis_length_m':math.sqrt(.115**2+.255**2+.04**2),'MIDI_forearm_axis_length_m':math.sqrt(.245**2+.018**2+.04**2),'MIDI_hand_envelope_mm':[150,70,42],'MIDI_shoe_envelope_mm':[280,100,60],'MIDI_fingertip_bottom_above_floor_m':.750,'MIDI_thigh_radius_m':.06,'MIDI_head_top_above_floor_m':1.395,'diner_seat_m':.650,'diner_knee_length_trial_m':.60,'passage_diameter_m':.450,'passage_height_m':1.718,'stool_withdrawal_m':.45,'entry_positions_each':18,'entry_trajectory_source_xz':{'rear_to_gap':[[16.82,2.37],[16.82,3.05]],'gap_to_seats':[[16.35,3.05],[17.29,3.05]]}},'limits':['Trial body dimensions explicitly selected; not population percentiles or accessibility certification.','Entry checks standing approaches and21stool poses; it does not simulate dynamic balance or full sit-to-stand motion.','Keys are primary neutral input; all auxiliary console controls are not claimed to share that reach/posture.','Weld beads touch connected steel intentionally; capacity and fabrication remain professional selection.']};(out/'use_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf8');print(json.dumps({'status':result['status'],'failed':[(r['scenario'],len(r.get('hits',[]))) for r in rows if not r['pass']],'rows':len(rows),'contacts':len(contacts)}),flush=True)
assert hashlib.sha256(model.read_bytes()).hexdigest()==SHA
