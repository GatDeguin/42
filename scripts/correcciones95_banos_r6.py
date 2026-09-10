"""R6D bathrooms: proposed coordinated fixtures, real floor layers and level-entry shower.
Uses loaded model. --preview writes R6D_preview; optional --out overrides.
"""
import bpy,json,sys,argparse,ast,hashlib,math,bmesh
from pathlib import Path
from mathutils import Vector,Matrix
root=Path(__file__).resolve().parent.parent;S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();source=Path(bpy.data.filepath)
ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--out');args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
if any(o.name.startswith('BTH95 |') for o in S.objects):raise RuntimeError('BTH95 already exists')
COL=bpy.data.collections.new('95 | Baños PB R6D');S.collection.children.link(COL);M={m.get('source_material_key'):m for m in bpy.data.materials if m.get('source_material_key')}
for m in bpy.data.materials:
 if m.name.startswith(('MAT95 | ','SL95 | ')):M[m.name.split(' | ',1)[1]]=m
for node in ast.parse((root/'scripts/correcciones95_corredizas_r5.py').read_text(encoding='utf8')).body:
 if isinstance(node,ast.FunctionDef):exec(compile(ast.Module(body=[node],type_ignores=[]),'<helper>','exec'))
for node in ast.parse((root/'scripts/correcciones95_corredizas_r5_drain_sweep.py').read_text(encoding='utf8')).body:
 if isinstance(node,ast.FunctionDef) and node.name=='sweep':exec(compile(ast.Module(body=[node],type_ignores=[]),'<sweep>','exec'))
operations=[];changes=[]
def bb(n,x,h,z,key='blackMetal'):return box('BTH95 | '+n,{'x':x,'y':h,'z':z},key)
def erase(name):
 o=bpy.data.objects.get(name)
 if o:bpy.data.objects.remove(o,do_unlink=True)
def transform(o,fn):
 mw=o.matrix_world.copy();inv=mw.inverted()
 for v in o.data.vertices:v.co=inv@cv(fn(Vector(src(mw@v.co))))
 o.data.update()
def move_group(prefix,target,angle=0):
 body=bpy.data.objects[prefix];b=bounds(body);c=Vector(tuple(sum(b[k])/2 for k in 'xyz'));t=Vector((target[0],c.y,target[1]));co=math.cos(angle);si=math.sin(angle)
 for o in list(S.objects):
  if o.name==prefix or o.name.startswith(prefix+' |'):
   old=bounds(o)
   def fn(p):
    q=p-c;return t+Vector((co*q.x-si*q.z,q.y,si*q.x+co*q.z))
   transform(o,fn);changes.append({'object':o.name,'before':old,'after':bounds(o)})
def fit(n,target):
 o=bpy.data.objects[n];old=bounds(o)
 def fn(p):return Vector(tuple(target[k][0]+(p[i]-old[k][0])*(target[k][1]-target[k][0])/(old[k][1]-old[k][0]) for i,k in enumerate('xyz')))
 transform(o,fn);changes.append({'object':n,'before':old,'after':bounds(o)});return o
def rigid_turn_fit(n,target):
 o=bpy.data.objects[n];old=bounds(o);cx=sum(old['x'])/2;cz=sum(old['z'])/2
 transform(o,lambda p:Vector((cx-(p.z-cz),p.y,cz+(p.x-cx))));return fit(n,target)
def hollow(n,a,b,outer,inner,key='stainless'):return cylinder('BTH95 | '+n,a,b,outer,key,inner=inner)
def plate_region(n,outer,inner,topfun,thickness,key):
 # Four trapezoids around the drain, each a real watertight layer with flat planar top.
 x0,z0,x1,z1=outer;ix0,iz0,ix1,iz1=inner
 polys=[[(x0,z0),(x1,z0),(ix1,iz0),(ix0,iz0)],[(x1,z0),(x1,z1),(ix1,iz1),(ix1,iz0)],[(x1,z1),(x0,z1),(ix0,iz1),(ix1,iz1)],[(x0,z1),(x0,z0),(ix0,iz0),(ix0,iz1)]];out=[]
 for k,poly in enumerate(polys):
  high=[(x,topfun(x,z),z) for x,z in poly];low=[(x,(topfun(x,z)-thickness if isinstance(thickness,(int,float)) else thickness(x,z)),z) for x,z in poly];v=[cv(p) for p in low+high];f=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)];me=bpy.data.meshes.new(n);me.from_pydata(v,[],f);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();o=bpy.data.objects.new('BTH95 | '+n+f' paño{k+1}',me);COL.objects.link(o);me.materials.append(mat(key));o['detail_status']='P / capa coordinada sin especificación de producto';out.append(o)
 return out
# Preserve all door meshes and13 rig definitions.
rigs=[o.name for o in S.objects if o.name.startswith('DOOR |')];door_meshes={o.name:hashlib.sha256(str([(tuple(v.co)) for v in o.data.vertices]).encode()).hexdigest() for rn in ['DOOR | bathroomMono','DOOR | poolBath'] for o in bpy.data.objects[rn].children_recursive if o.type=='MESH'}
# Continuous PB slab ends at+.16. Existing finish volumes are replaced, not stacked.
for name in ['Piso monoambiente','Piso quincho','Piso baño mono','Piso baño quincho']:erase(name)
floors={}
floors['mono']=[bb('mono base30',[14.2,21.8],[.16,.19],[.2,5.9],'grout'),bb('mono adhesivo10',[14.2,21.8],[.19,.20],[.2,5.9],'cement'),box('Piso monoambiente',{'x':[14.2,21.8],'y':[.20,.21],'z':[.2,5.9]},'tile')]
floors['quincho']=[bb('quincho adhesivo10',[14,22],[.16,.17],[6,12],'cement'),box('Piso quincho',{'x':[14,22],'y':[.17,.18],'z':[6,12]},'tile')]
rooms={'mono':{'x':[19.39,21.8],'z':[4.35,5.9]},'quincho':{'x':[20.7,21.8],'z':[10.17,11.83]}}
for key,p in rooms.items():
 cut={'x':p['x'],'z':p['z'],'y':[.15,.22]};reserve([o.name for o in floors[key]],cut,'exclusión piso general bajo baño '+key)
 floors[key+'_bath']=[bb(key+' baño mortero30',p['x'],[.16,.19],p['z'],'grout'),bb(key+' baño membrana2',p['x'],[.19,.192],p['z'],'rubber95'),bb(key+' baño adhesivo8',p['x'],[.192,.20],p['z'],'cement'),box('Piso baño '+key,{'x':p['x'],'z':p['z'],'y':[.20,.21]},'tile')]
# Trim dry floor layers beneath the existing PB bathroom partitions, retaining their coordinates.
for o in list(S.objects):
 if o.type!='MESH' or not o.name.startswith(('Baño mono muro','Baño mono frente |','Baño quincho muro','Baño quincho frente cerrado')):continue
 b=bounds(o)
 if b['y'][0]>.22:continue
 b['y']=[.15,.22];key='mono' if 'mono' in o.name else 'quincho';reserve([p.name for p in floors[key]],b,'encuentro piso-tabique '+o.name)
# Seal the existing100mm privacy gap without moving either wall line or door.
bb('cierre junta muro mono100',[19.25,19.39],[.0,2.60],[5.8,5.9],'whitePlaster')
reserve([p.name for p in floors['mono']],{'x':[19.25,19.39],'y':[.15,.22],'z':[5.8,5.9]},'piso bajo cierre100')
# Flush bath doorway, without duplicating the general layer below it.
qdoor={'x':[20.805,21.635],'z':[11.83,11.975],'y':[.15,.22]};reserve([o.name for o in floors['quincho']],qdoor,'umbral baño quincho')
for label,hh,key in [('mortero',[.16,.19],'grout'),('membrana',[.19,.192],'rubber95'),('adhesivo',[.192,.20],'cement'),('baldosa',[.20,.21],'tile')]:bb('umbral quincho '+label,qdoor['x'],hh,qdoor['z'],key)
# Relocate complete ceramic WC assemblies; the proprietary internal trap is not invented.
move_group('Inodoro mono',[19.85,5.44]);move_group('Inodoro quincho',[21.53,10.58],math.pi)
for label,cx,cz in [('mono',19.85,5.44),('quincho',21.53,10.58)]:
 c=cylinder('TMP WC slab reserve',[cx,-.13,cz],[cx,.22,cz],.060)
 for o in [bpy.data.objects['Losa planta baja']]+floors[label+'_bath']:
  if overlap(bounds(o),bounds(c)):boolean(o,c)
 bpy.data.objects.remove(c,do_unlink=True);hollow('reserva salida WC '+label,[cx,-.12,cz],[cx,.21,cz],.055,.050);hollow('sello salida WC '+label,[cx,.19,cz],[cx,.21,cz],.060,.055,'rubber95')
# Both vessel basins retain their hollow geometry, coordinated at rim+1.06.
BASINS=[('mono','Lavatorio mono',20.54,4.52,.62,.32,4.35),('quincho','Lavatorio quincho',20.995,10.37,.46,.38,10.17)]
for label,name,cx,cz,w,d,wall in BASINS:
 basin=fit(name,{'x':[cx-w/2,cx+w/2],'y':[.88,1.06],'z':[cz-d/2,cz+d/2]});cw=w-.02;rear=cz-d/2;front=cz+d/2-.02
 # Carcass18mm, legs100mm and removable fronts; the basin sits on its support deck.
 boards=[]
 for side,x in [('i',[cx-cw/2,cx-cw/2+.018]),('d',[cx+cw/2-.018,cx+cw/2])]:boards.append(bb('vanitory '+label+' lateral '+side,x,[.31,.862],[rear,front-.018],'wood'))
 boards.append(bb('vanitory '+label+' base',[cx-cw/2+.018,cx+cw/2-.018],[.31,.328],[rear,front],'wood'))
 boards.append(bb('vanitory '+label+' apoyo bacha',[cx-cw/2,cx+cw/2],[.862,.88],[rear,front],'wood'))
 boards.append(bb('vanitory '+label+' trasera',[cx-cw/2+.018,cx+cw/2-.018],[.328,.862],[rear,rear+.012],'wood'))
 for a,b in [(cx-cw/2,cx-.002),(cx+.002,cx+cw/2)]:bb('vanitory '+label+' frente',[a,b],[.328,.84],[front-.018,front],'woodDark')
 for x in [cx-cw/2+.04,cx+cw/2-.04]:
  for z in [rear+.04,front-.04]:bb('vanitory '+label+' pata',[x-.0125,x+.0125],[.21,.31],[z-.0125,z+.0125],'blackMetal')
  # Shelf brackets physically bridge the10mm wall gap.
  bb('vanitory '+label+' ménsula',[x-.015,x+.015],[.83,.836],[wall,front-.02]);bb('vanitory '+label+' placa muro',[x-.015,x+.015],[.75,.86],[wall,wall+.004])
  for h in [.77,.845]:cylinder('BTH95 | anclaje ménsula '+label,[x,h,wall-.05],[x,h,wall+.004],.003,'stainless')
 # Real waste opening in ceramic and support deck.
 c=cylinder('TMP basin waste',[cx,.85,cz],[cx,.94,cz],.016)
 for o in [basin,boards[3]]:boolean(o,c)
 bpy.data.objects.remove(c,do_unlink=True);hollow('válvula lavatorio '+label,[cx,.913,cz],[cx,.918,cz],.020,.014)
 hollow('bajada lavatorio '+label,[cx,.695,cz],[cx,.916,cz],.016,.014)
 bottle=hollow('sifón botella '+label,[cx,.662,cz],[cx,.80,cz],.035,.031)
 cylinder('BTH95 | tapa inferior sifón '+label,[cx,.658,cz],[cx,.662,cz],.035,'stainless');hollow('tapa superior sifón '+label,[cx,.80,cz],[cx,.806,cz],.035,.016)
 outlet=[cx,.76,cz-.031];wallend=[cx,.76,wall-.04];c=cylinder('TMP waste bore',[cx,.76,cz-.025],[cx,.76,wall-.045],.014);boolean(bottle,c)
 for o in boards:
  if overlap(bounds(o),bounds(c)):boolean(o,c)
 bpy.data.objects.remove(c,do_unlink=True);hollow('ramal lavatorio '+label,outlet,wallend,.016,.014)
 # Wall-mounted mixer/spout, entirely directed into the relocated bowl.
 cylinder('BTH95 | grifo '+label+' cuerpo',[cx,1.18,wall],[cx,1.18,wall+.07],.024,'stainless')
 cs=[];ts=[];a=Vector((cx,1.18,wall+.07));b=Vector((cx,1.18,cz));c=Vector((cx,1.10,cz))
 for i in range(17):
  t=i/16;cs.append((1-t)**2*a+2*t*(1-t)*b+t*t*c);ts.append((2*(1-t)*(b-a)+2*t*(c-b)).normalized())
 sp=sweep('BTH95 | grifo '+label+' caño hueco',cs,ts,Vector((1,0,0)),.008,.006)
 cylinder('BTH95 | grifo '+label+' mando',[cx,1.20,wall+.03],[cx+.035,1.235,wall+.05],.004,'stainless')
 for x in [cx-.05,cx+.05]:
  cylinder('BTH95 | grifo '+label+' toma',[x,1.18,wall-.04],[x,1.18,wall+.022],.006,'stainless');cylinder('BTH95 | grifo '+label+' embellecedor',[x,1.18,wall],[x,1.18,wall+.006],.015,'stainless');cylinder('BTH95 | grifo '+label+' puente',[x,1.18,wall+.018],[cx,1.18,wall+.018],.008,'stainless')
 # Local recesses for plumbing stop inside the wall; network route remains P.
 for o in list(S.objects):
  if o.type=='MESH' and ((label=='mono' and o.name.startswith('Baño mono frente |')) or (label=='quincho' and o.name=='Baño quincho frente cerrado')):
   c=cylinder('TMP wall sleeve',outlet,wallend,.020)
   if overlap(bounds(o),bounds(c)):boolean(o,c)
   bpy.data.objects.remove(c,do_unlink=True)
# Mirrors now face the basins from the front walls.
rigid_turn_fit('Espejo baño mono',{'x':[20.26,20.82],'y':[1.25,2.15],'z':[4.35,4.38]})
rigid_turn_fit('Espejo baño pileta',{'x':[20.765,21.225],'y':[1.25,2.15],'z':[10.17,10.20]})
# Towel rail away from the WC use envelope, with two actual wall standoffs.
o=bpy.data.objects['Barra toalla baño mono'];transform(o,lambda p:p+Vector((-.12,0,-.43)))
for z in [4.71,5.31]:cylinder('BTH95 | soporte toallero mono',[19.39,1.30,z],[19.45,1.30,z],.006,'stainless')
# Level shower: perimeter+.21, central100x100 at+.1955, four graded planes.
for name in ['Plato ducha baño mono','Mampara baño mono']:erase(name)
outer=[20.9,4.35,21.8,5.8];inner=[21.30,5.025,21.40,5.125];cx,cz=21.35,5.075
reserve([o.name for o in floors['mono_bath']],{'x':[20.9,21.8],'y':[.15,.22],'z':[4.35,5.8]},'ducha enrasada sin piso duplicado')
def top(x,z):return .1955+.0145*max(abs(x-cx)-.05,0)/.40 if abs(x-cx)/.45>=abs(z-cz)/.725 else .1955+.0145*max(abs(z-cz)-.05,0)/.675
# At trapezoid vertices each coordinate is exact; each emitted face is planar.
plate_region('ducha mortero variable',outer,inner,lambda x,z:top(x,z)-.020,lambda x,z:.16,'grout')
plate_region('ducha membrana2',outer,inner,lambda x,z:top(x,z)-.018,.002,'rubber95')
plate_region('ducha adhesivo8',outer,inner,lambda x,z:top(x,z)-.010,.008,'cement')
plate_region('ducha baldosa10',outer,inner,top,.010,'tile')
# Membrane turns on front/east walls, buried behind the removable finish detail.
for x,z,w,d in [(21.35,4.351,.9,.002),(21.799,5.075,.002,1.45)]:bb('ducha remonte membrana150',[x-w/2,x+w/2],[.19,.36],[z-d/2,z+d/2],'rubber95')
# Central trap with accessible grille and a coordinated reserve, no claimed hydraulic capacity.
c=cylinder('TMP shower sanitary reserve',[cx,.04,cz],[cx,.20,cz],.052);boolean(bpy.data.objects['Losa planta baja'],c);bpy.data.objects.remove(c,do_unlink=True)
body=hollow('ducha cuerpo sifón',[cx,.055,cz],[cx,.1875,cz],.045,.040,'stainless');cylinder('BTH95 | ducha fondo sifón',[cx,.045,cz],[cx,.055,cz],.045,'stainless')
hollow('ducha tubo inmersión',[cx,.067,cz],[cx,.188,cz],.020,.016,'stainless');hollow('ducha tapa cierre cuerpo',[cx,.184,cz],[cx,.188,cz],.045,.020,'stainless')
# Outlet inner weir+.117 minus dip+.067 yields a proposed50mm water seal.
outlet=[cx+.040,.135,cz];end=[cx+.25,.131,cz];c=cylinder('TMP shower outlet bore',[cx+.034,.135,cz],end,.020);boolean(body,c);boolean(bpy.data.objects['Losa planta baja'],c);bpy.data.objects.remove(c,do_unlink=True);hollow('ducha ramal P40',outlet,end,.020,.018,'stainless')
# 100mm grate frame and8mm slits; removable from above.
for x in [cx-.048,cx+.048]:bb('ducha marco rejilla',[x-.002,x+.002],[.1915,.1955],[cz-.05,cz+.05],'stainless')
for z in [cz-.048,cz+.048]:bb('ducha marco rejilla',[cx-.046,cx+.046],[.1915,.1955],[z-.002,z+.002],'stainless')
for i in range(7):
 x=cx-.039+i*.013;bb('ducha barra rejilla',[x-.0025,x+.0025],[.1915,.1955],[cz-.046,cz+.046],'stainless')
# Glass12mm with sealed U-track, setting blocks and fixed wall channel.
glass=bb('mampara fija12',[20.894,20.906],[.219,2.169],[4.356,4.856],'glass')
bb('mampara base3',[20.889,20.911],[.210,.213],[4.35,4.865],'stainless')
for x in [[20.889,20.892],[20.908,20.911]]:bb('mampara U lateral',x,[.213,.243],[4.35,4.865],'stainless')
for x in [[20.892,20.894],[20.906,20.908]]:bb('mampara junta',x,[.219,.243],[4.356,4.856],'rubber95')
for z in [4.43,4.78]:bb('mampara taco',[20.894,20.906],[.213,.219],[z-.025,z+.025],'rubber95')
bb('mampara canal muro fondo',[20.889,20.911],[.213,2.175],[4.35,4.353],'stainless')
for x in [[20.889,20.892],[20.908,20.911]]:bb('mampara canal muro lateral',x,[.213,2.175],[4.353,4.376],'stainless')
for h in [.40,1.1,1.85]:cylinder('BTH95 | mampara anclaje muro',[20.9,h,4.29],[20.9,h,4.354],.003,'stainless')
for z in [4.43,4.78]:cylinder('BTH95 | mampara anclaje base',[20.9,.15,z],[20.9,.213,z],.003,'stainless')
# Shower head and mixer have continuous pipes and wall supports.
o=bpy.data.objects['Ducha baño mono'];b=bounds(o);center=Vector(tuple(sum(b[k])/2 for k in 'xyz'));transform(o,lambda p:p-center+Vector((21.35,2.02,4.60)))
cylinder('BTH95 | ducha columna',[21.35,1.31,4.40],[21.35,2.02,4.40],.010,'stainless');cylinder('BTH95 | ducha brazo rociador',[21.35,2.02,4.40],[21.35,2.02,4.60],.010,'stainless');cylinder('BTH95 | ducha mezclador',[21.35,1.31,4.35],[21.35,1.31,4.44],.025,'stainless')
for h in [1.31,1.88]:cylinder('BTH95 | ducha ménsula',[21.35,h,4.35],[21.35,h,4.40],.007,'stainless');cylinder('BTH95 | ducha roseta',[21.35,h,4.35],[21.35,h,4.356],.02,'stainless')
# Recess the membrane returns behind a2mm protective finish, preserving finished wall lines.
frontmem=bpy.data.objects['BTH95 | ducha remonte membrana150'];fit(frontmem.name,{'x':[20.9,21.8],'y':[.19,.36],'z':[4.346,4.348]})
sidemem=bpy.data.objects['BTH95 | ducha remonte membrana150.001'];fit(sidemem.name,{'x':[21.802,21.804],'y':[.19,.36],'z':[4.35,5.8]})
frontreserve={'x':[20.9,21.8],'y':[.19,.36],'z':[4.346,4.35]};sidereserve={'x':[21.8,21.804],'y':[.19,.36],'z':[4.35,5.8]}
for reg in [frontreserve,sidereserve]:
 targets=[o.name for o in S.objects if o.type=='MESH' and not o.name.startswith('BTH95') and bounds(o)['y'][0]<.19 and bounds(o)['y'][1]>2.5 and overlap(bounds(o),reg)]
 reserve(targets,reg,'reserva retorno impermeable')
bb('ducha membrana puente frontal',[20.9,21.8],[.19,.192],[4.348,4.35],'rubber95');bb('ducha membrana puente lateral',[21.8,21.802],[.19,.192],[4.35,5.8],'rubber95')
bb('ducha protección retorno frontal2',[20.9,21.8],[.192,.36],[4.348,4.35],'whitePlaster');bb('ducha protección retorno lateral2',[21.8,21.802],[.192,.36],[4.35,5.8],'whitePlaster')
# Grille bearing ring and bonded membrane collar: no floating gap or open annulus.
for a,b in [([cx-.05,cx-.04],[cz-.05,cz+.05]),([cx+.04,cx+.05],[cz-.05,cz+.05]),([cx-.04,cx+.04],[cz-.05,cz-.04]),([cx-.04,cx+.04],[cz+.04,cz+.05])]:bb('ducha aro apoyo rejilla',a,[.188,.1915],b,'stainless')
reg={'x':[cx-.06,cx+.06],'y':[.1725,.1785],'z':[cz-.06,cz+.06]}
reserve([o.name for o in S.objects if o.name.startswith(('BTH95 | ducha mortero','BTH95 | ducha membrana2','BTH95 | ducha adhesivo8'))],reg,'alojamiento collar desagüe')
for name,hh,rad,key in [('brida desagüe',[.1725,.1745],.045,'stainless'),('collar sellado desagüe',[.1745,.1785],.045,'rubber95')]:
 o=bb('ducha '+name,[cx-.06,cx+.06],hh,[cz-.06,cz+.06],key);c=cylinder('TMP collar bore',[cx,.17,cz],[cx,.18,cz],rad);boolean(o,c);bpy.data.objects.remove(c,do_unlink=True)
# Verify preserved circulation-defining doors and rigs.
assert rigs==[o.name for o in S.objects if o.name.startswith('DOOR |')]
assert all(hashlib.sha256(str([tuple(v.co) for v in bpy.data.objects[n].data.vertices]).encode()).hexdigest()==sha for n,sha in door_meshes.items())
S['bathrooms_r6d']='P: coordinated mono/quincho fixtures, floor layers above+.16 slab, level shower with central drain and50mm proposed trap seal. No hydraulic/structural/product validation.'
S.frame_set(1);bpy.context.view_layer.update();out=Path(args.out) if args.out else root/'output'/('Casa_de_Campo_95_R6D_preview.blend' if args.preview else 'Casa_de_Campo_95_R6D.blend');out=out.resolve();bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
report={'source_model':str(source),'model':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'status':'P solution modelled; no product/load/hydraulic validation','coordinate_convention':'source X,Yheight,Zdepth metres','rig_count':len(rigs),'bath_door_meshes_preserved':True,'changes':changes,'reservations':operations,'shower':{'outer':outer,'drain':inner,'perimeter_y':.21,'drain_y':.1955,'slopes_percent':[.0145/.675*100,.0145/.40*100],'mortar_thickness_mm':[15.5,30],'tile_mm':10,'adhesive_mm':8,'membrane_mm':2,'proposed_trap_seal_mm':50,'glass_entry_clear_m':5.8-4.856},'floors':{'structural_slab_top':.16,'mono_top':.21,'quincho_top':.18,'baths_top':.21},'limitations':['Fixture selection, supports and fasteners require sizing.','Slab sanitary reservations require reinforcement coordination.','Internal WC trap not modelled: sanitary appliance must be selected;110mm outlet is a proposed connection reserve.','Drain stubs stop at local coordination limits; network routes and hydraulic calculations remain pending.','Shower opening is not splash-tested; no watertightness certification.']}
(root/'review95/banos_r6d_details.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8');print('BATHROOMS_R6D_SAVED',report['sha256'],flush=True)
