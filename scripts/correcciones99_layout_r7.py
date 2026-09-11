"""R7 layout: frontage bathroom PB and direct bedroom-to-living door PA.
Applies to R7A or a descendant with its water correction. Saves separate preview/final.
P construction proposal; dimensions verified geometrically, no product/capacity certification.
"""
import bpy,bmesh,json,math,ast,hashlib,sys,argparse
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parent.parent;S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
p=argparse.ArgumentParser();p.add_argument('--out',default='output/Casa_de_Campo_99_R7A_layout_preview.blend');args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
source=Path(bpy.data.filepath);assert 'r7_constructive_corrections' in S,'Requires R7A water correction';assert not bpy.data.collections.get('99 | Layout R7')
COL=bpy.data.collections.new('99 | Layout R7');S.collection.children.link(COL)
M={m.get('source_material_key'):m for m in bpy.data.materials if m.get('source_material_key')}
for m in bpy.data.materials:
 if m.name.startswith(('MAT95 | ','SL95 | ')):M[m.name.split(' | ',1)[1]]=m
for n in ['mat','cv','src','bounds','overlap','child','box','boolean','cylinder']:
 for nd in ast.parse((ROOT/'scripts/correcciones95_corredizas_r5.py').read_text('utf8')).body:
  if isinstance(nd,ast.FunctionDef) and nd.name==n:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
protected_prefix=('Cama dormitorio','Mesita','Sofá vivienda','Mesa comedor','Silla comedor','Mesa baja vivienda','Mueble TV','Vestidor respaldo','Vestidor lateral','Vestidor estante','Vestidor barral','Vestidor cajón','Vestidor zapatero')
from array import array
def geom_sig(o):
 h=hashlib.sha256(repr(tuple(v for r in o.matrix_world for v in r)).encode())
 if o.type=='MESH':
  a=array('f',[0])*(len(o.data.vertices)*3);o.data.vertices.foreach_get('co',a);h.update(a.tobytes())
  for uv in o.data.uv_layers:
   a=array('f',[0])*(len(uv.data)*2);uv.data.foreach_get('uv',a);h.update(a.tobytes())
 return h.hexdigest()
protected={o.name:geom_sig(o) for o in S.objects if o.name.startswith(protected_prefix) or o.name=='Agua de pileta'}
report={'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'coordinate_system':'source X,Yheight,Zdepth; metres','removed':[],'moved':[],'new_doors':[],'changed_hosts':[],'new_materials':[]}
M['r7_door']=bpy.data.objects['Puerta acceso vestidor'].data.materials[0]
M['r7_wall']=bpy.data.objects['Vestidor cierre al estar paño A'].data.materials[0]

def erase(o):
 if isinstance(o,str):o=bpy.data.objects.get(o)
 if o:report['removed'].append(o.name);bpy.data.objects.remove(o,do_unlink=True)

def bb(n,x,h,z,key='r7_wall',parent=None):return box('LAY99 | '+n,{'x':x,'y':h,'z':z},key,parent)

def cut_host(o,c,op='DIFFERENCE'):
 boolean(o,c,op)
 if o.name not in report['changed_hosts']:report['changed_hosts'].append(o.name)

def cut_region(names,reg,label):
 c=box('TEMP R7 '+label,reg)
 for n in names:
  o=bpy.data.objects.get(n)
  if o and o.type=='MESH' and overlap(bounds(o),reg):cut_host(o,c)
 erase(c)

def transform_group(obs,T):
 obs=list(dict.fromkeys(obs));saved={o:o.matrix_world.copy() for o in obs};before={o:bounds(o) for o in obs if o.type=='MESH'}
 def depth(q):
  d=0
  while q.parent:q=q.parent;d+=1
  return d
 for o in sorted(obs,key=depth):o.matrix_world=T@saved[o]
 bpy.context.view_layer.update()
 for o,b in before.items():report['moved'].append({'object':o.name,'before':b,'after':bounds(o)})

def uv_box(o):
 me=o.data
 for name in ['UVMap','WoodUV','MapaUV']:
  uv=me.uv_layers.get(name) or me.uv_layers.new(name=name)
  for poly in me.polygons:
   ax=max(range(3),key=lambda i:abs(poly.normal[i]));ij=[i for i in range(3) if i!=ax]
   for j in poly.loop_indices:
    co=me.vertices[me.loops[j].vertex_index].co;uv.data[j].uv=(co[ij[0]],co[ij[1]])

# Suite entry is explicitly removed; wardrobe stays linked only to bedroom and bath.
r=bpy.data.objects['DOOR | suiteEntry']
for o in list(r.children_recursive):erase(o)
erase(r)
for o in list(S.objects):
 if o.name.startswith(('Puerta acceso vestidor','Premarco acceso vestidor')):erase(o)
fill=bb('cierre vestidor estar',[18.06,18.98],[3.20,5.43],[8.93,9.07])
# Flush existing floor and baseboard interfaces at the infill, with no protrusion into805mm passage.
cut_region([o.name for o in S.objects if o.type=='MESH' and o.name.lower().startswith('piso')],{'x':[18.06,18.98],'y':[3.199,3.251],'z':[8.93,9.07]},'floor under wardrobe infill')
for n,z in [('rodapie vestidor enrasado',[8.93,8.932]),('rodapie estar enrasado',[9.068,9.07])]:
 c=bb('TEMP rodapie',[18.06,18.98],[3.25,3.35],z);cut_host(fill,c);erase(c);bb(n,[18.06,18.98],[3.25,3.35],z,'woodDark')
# Direct bedroom doorway: rough1000, frame35 each side,915x45 leaf.
opening={'x':[16.54,17.54],'y':[3.20,5.50],'z':[8.925,9.075]}
cut_region(['Dormitorio tabique transversal'],opening,'new bedroom opening')
cut_region([o.name for o in S.objects if o.type=='MESH' and ('zócalo' in o.name.lower() or 'rodapi' in o.name.lower())],dict(opening,y=[3.19,3.46]),'skirting terminates at new bedroom opening')
# Finish a level threshold on structural slab, removing any general finish volume in this footprint.
threshold={'x':[16.54,17.54],'y':[3.1999,3.2501],'z':[8.93,9.07]}
cut_region([o.name for o in S.objects if o.type=='MESH' and o.name.lower().startswith('piso')],threshold,'bedroom threshold')
bb('umbral dormitorio base40',[16.54,17.54],[3.20,3.24],[8.93,9.07],'grout');bb('umbral dormitorio baldosa10',[16.54,17.54],[3.24,3.25],[8.93,9.07],'tile')

# Relocate the complete existing bathroom including its built floor/fixture assemblies.
old_bathrig=bpy.data.objects['DOOR | bathroomMono']
for o in list(old_bathrig.children_recursive):erase(o)
erase(old_bathrig)
for o in list(S.objects):
 if o.name.startswith(('Baño mono muro','Baño mono frente |','Baño mono puerta','Baño mono | manija','BTH95 | cierre junta muro mono')):erase(o)
move=[]
for o in S.objects:
 n=o.name
 if n.startswith(('Inodoro mono','Ducha baño mono')) or n in ['Espejo baño mono','Barra toalla baño mono','Lavatorio mono','Piso baño mono']:move.append(o)
 elif n.startswith('BTH95 | ') and ((('mono' in n) and n not in ['BTH95 | mono base30','BTH95 | mono adhesivo10']) or any(t in n for t in ['ducha ','mampara '])):move.append(o)
transform_group(move,Matrix.Translation(cv((0,0,-4.09))))
# Move placard to old bathroom against medianera, front toward-X, bearing on+.21 floor.
pc=bpy.data.objects['Placard mono'];old=bounds(pc);ctr=Vector((sum(old['x'])/2,sum(old['y'])/2,sum(old['z'])/2));target=Vector((21.525,ctr.y+.04,4.90));T=Matrix.Translation(cv(target))@Matrix.Rotation(-math.pi/2,4,'Z')@Matrix.Translation(-cv(ctr));transform_group([pc],T)
# Dining table and both chairs move together; kitchen/fridge/island are preserved.
move=[o for o in S.objects if o.name.startswith(('Mesa mono ','Silla mono ','MOB95 | faldón mesa mono'))]
transform_group(move,Matrix.Translation(cv((.06,0,1.0))))
# Restore former slab and medianera pockets before cutting the new local sanitary reserves.
slab=bpy.data.objects['Losa planta baja']
for x,z in [([19.78,19.92],[5.37,5.51]),([21.28,21.63],[4.99,5.16])]:
 c=bb('TEMP reponer reserva anterior',x,[0,.16],z,'concrete');cut_host(slab,c,'UNION');erase(c)
median=bpy.data.objects['Medianera constructiva baja'];c=bb('TEMP reponer retorno anterior',[21.8,21.805],[.19,.36],[4.35,5.8],'brick');cut_host(median,c,'UNION');erase(c)
for label,cx,cz,radius,low,high in [('WC',19.85,1.35,.060,-.13,.22),('ducha',21.35,.985,.052,.04,.20)]:
 c=cylinder('TEMP sanitary '+label,(cx,low,cz),(cx,high,cz),radius);cut_host(slab,c);erase(c)
c=cylinder('TEMP ramal ducha',(21.384,.135,.985),(21.606,.131,.985),.024);cut_host(slab,c);erase(c)
# Continuous dry floor replaces its former bathroom hole, then excludes new bathroom and walls.
for n in ['Piso monoambiente','BTH95 | mono base30','BTH95 | mono adhesivo10']:erase(n)
dry=[box('BTH95 | mono base30',{'x':[14.2,21.8],'y':[.16,.19],'z':[.2,5.9]},'grout'),box('BTH95 | mono adhesivo10',{'x':[14.2,21.8],'y':[.19,.20],'z':[.2,5.9]},'cement'),box('Piso monoambiente',{'x':[14.2,21.8],'y':[.20,.21],'z':[.2,5.9]},'tile')]
cut_region([o.name for o in dry],{'x':[19.25,21.8],'y':[.15,.22],'z':[.2,1.95]},'new bath footprint')
# Front60mm lining aligns the finished face with the existing260mm corner column.
front=bb('baño mono trasdosado frontal60',[19.39,21.8],[.16,3.0],[.2,.26],'whitePlaster')
cut_host(front,bpy.data.objects['Pilar esquina frontal derecha'])
west_a=bb('baño mono oeste norte',[19.25,19.39],[.16,3.0],[.26,.36],'whitePlaster');west_b=bb('baño mono oeste sur',[19.25,19.39],[.16,3.0],[1.36,1.81],'whitePlaster');west_h=bb('baño mono oeste dintel',[19.25,19.39],[2.46,3.0],[.36,1.36],'whitePlaster');south=bb('baño mono posterior',[19.25,21.8],[.16,3.0],[1.81,1.95],'whitePlaster')
# New entrance membrane is continuous with the bath, all at floor+.21.
for label,hh,k in [('mortero30',[.16,.19],'grout'),('membrana2',[.19,.192],'rubber95'),('adhesivo8',[.192,.20],'cement'),('baldosa10',[.20,.21],'tile')]:bb('umbral baño mono '+label,[19.25,19.39],hh,[.36,1.36],k)
# Recess relocated membrane returns into substrate; finished wall lines are retained.
for reg in [{'x':[20.9,21.8],'y':[.19,.36],'z':[.256,.26]},{'x':[21.8,21.804],'y':[.19,.36],'z':[.26,1.71]}]:cut_region([front.name,median.name,'Pilar esquina frontal derecha'],reg,'new waterproof return reserve')
# Local plumbing sockets, penetrating substrate but not creating arbitrary network routes.
for x,h,z,rad in [(20.54,.76,.26,.020),(20.49,1.18,.26,.007),(20.59,1.18,.26,.007),(21.35,1.31,.26,.011),(21.35,2.23,.26,.011)]:
 c=cylinder('TEMP wall socket',(x,h,z-.045),(x,h,z+.004),rad);cut_host(front,c);cut_host(bpy.data.objects['Fachada ciega de ladrillo'],c);erase(c)
# Old toallero would meet the new west doorway; mount on south wall instead.
towel=[o for o in S.objects if o.name=='Barra toalla baño mono' or o.name.startswith('BTH95 | soporte toallero mono')]
# Existing rail is vertical in plan along Z; rotate90deg onto the new rear wall.
b=bounds(bpy.data.objects['Barra toalla baño mono']);ctr=Vector((sum(b['x'])/2,sum(b['y'])/2,sum(b['z'])/2));tar=Vector((20.47,ctr.y,1.750));transform_group(towel,Matrix.Translation(cv(tar))@Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Translation(-cv(ctr)))

# Generic proposed hinged assembly, local t along closed leaf and d toward opening side.
def door(key,label,axis,raw,wall,floor,head,wood='r7_door'):
 lo,hi=raw;cl,cr=lo+.035,hi-.035;ll,lr=cl+.0075,cr-.0075;D=wall[1]-.0025;bottom=floor+.010;top=head-.005
 def pt(t,h,d):return (t,h,d) if axis=='x' else (-d,h,t)
 def reg(tt,hh,dd):
  return {'x':tt,'y':hh,'z':dd} if axis=='x' else {'x':[-dd[1],-dd[0]],'y':hh,'z':tt}
 def part(n,tt,hh,dd,k='r7_wall',parent=None):return box(label+' | '+n,reg(tt,hh,dd),k,parent)
 rig=bpy.data.objects.new('DOOR | '+key,None);bpy.data.collections['DOORS'].objects.link(rig);rig.location=cv(pt(ll,floor,D));rig['open']=0.0;rig['motion']='hinge';rig['max_angle_degrees']=90.0;rig.id_properties_ui('open').update(min=0,max=1)
 dr=rig.driver_add('rotation_euler',2).driver;dr.expression='opening * -1.5707963267948966';v=dr.variables.new();v.name='opening';v.type='SINGLE_PROP';v.targets[0].id=rig;v.targets[0].data_path='["open"]'
 for fr,val in [(1,0),(30,0),(105,1),(1480,1)]:rig['open']=val;rig.keyframe_insert(data_path='["open"]',frame=fr)
 S.frame_set(1);bpy.context.view_layer.update()
 left=part('jamba bisagra',[lo,cl],[floor,head+.035],wall);right=part('jamba cierre',[cr,hi],[floor,head+.035],wall);header=part('dintel',[lo,hi],[head,head+.035],wall)
 leaf=part('hoja',[ll,lr],[bottom,top],[D-.045,D],wood,rig);uv_box(leaf)
 # Back stops sit behind the closed leaf, with touching2mm EPDM seals.
 for nm,tt in [('bisagra',[cl,cl+.0225]),('cierre',[cr-.0225,cr])]:
  part('galce '+nm,tt,[bottom,top],[D-.060,D-.047],'r7_wall');part('junta '+nm,tt,[bottom,top],[D-.047,D-.045],'rubber95')
 part('galce superior',[cl+.0225,cr-.0225],[top-.0175,head],[D-.060,D-.047],'r7_wall');part('junta superior',[cl+.0225,cr-.0225],[top-.0175,top],[D-.047,D-.045],'rubber95')
 # Three mortised knuckle hinges with real bore/pin and alternating axial ownership.
 for h in [floor+.28,floor+1.05,head-.25]:
  cut=cylinder('TEMP hinge mortise',pt(ll,h-.046,D),pt(ll,h+.046,D),.0062);boolean(leaf,cut);erase(cut)
  part('bisagra placa fija',[ll-.035,ll-.008],[h-.045,h+.045],[D,D+.0025],'stainless')
  part('bisagra placa movil',[ll+.006,ll+.036],[h-.014,h+.014],[D,D+.002],'stainless',rig)
  cylinder(label+' | bisagra eje',pt(ll,h-.046,D),pt(ll,h+.046,D),.0025,'stainless')
  for j,(a,b) in enumerate([(h-.044,h-.016),(h-.014,h+.014),(h+.016,h+.044)]):
   cylinder(label+' | bisagra nudillo '+str(j),pt(ll,a,D),pt(ll,b,D),.006,'stainless',rig if j==1 else None,inner=.0028)
   wing=part('bisagra ala '+str(j),[ll-.008,ll] if j!=1 else [ll,ll+.008],[a,b],[D,D+.002],'stainless',rig if j==1 else None)
   bore=cylinder('TEMP paso eje ala',pt(ll,a-.002,D),pt(ll,b+.002,D),.0028);boolean(wing,bore);erase(bore)
  for dh in [-.032,.032]:cylinder(label+' | tornillo marco',pt(ll-.023,h+dh,D-.016),pt(ll-.023,h+dh,D+.003),.0018,'stainless')
  for tt in [ll+.015,ll+.028]:cylinder(label+' | tornillo hoja',pt(tt,h,D-.014),pt(tt,h,D+.003),.0018,'stainless',rig)
 # Lever on both sides,42mm maximum projection, with rose and continuous spindle.
 ht=floor+1.08;handle_t=lr-.105
 for side,face in [(1,D),(-1,D-.045)]:
  cylinder(label+' | manija roseta',pt(handle_t,ht,face),pt(handle_t,ht,face+side*.003),.025,'stainless',rig)
  cylinder(label+' | manija vástago',pt(handle_t,ht,face+side*.003),pt(handle_t,ht,face+side*.035),.007,'stainless',rig)
  cylinder(label+' | manija palanca',pt(handle_t,ht,face+side*.035),pt(handle_t-.10,ht,face+side*.035),.007,'stainless',rig)
 part('burlete inferior soporte',[ll+.02,lr-.02],[bottom,bottom+.012],[D-.030,D-.015],'blackMetal',rig)
 # 6mm reveal below carrier remains until a selected adjustable sweep is specified.
 spec={'key':key,'label':label,'axis':axis,'raw_opening':raw,'clear_frame_m':cr-cl,'frame35_mm':35,'leaf_width_m':lr-ll,'leaf_thickness_m':.045,'pivot_source':pt(ll,floor,D),'floor_m':floor,'head_underside_m':head,'leaf_bottom_m':bottom,'leaf_top_m':top,'angle_deg':90,'driver':'opening * -pi/2 Blender Z','wall_range_local_d':wall,'clear_min_including_handle_estimate_m':cr-(ll+.045+.042),'moving_objects':[o.name for o in rig.children_recursive]}
 report['new_doors'].append(spec);return rig

door('bedroomDining','Puerta dormitorio comedor','x',[16.54,17.54],[8.93,9.07],3.25,5.465)
door('bathroomMono','Baño mono puerta','z',[.36,1.36],[-19.39,-19.25],.21,2.425)
import runpy
report['rug_correction']=runpy.run_path(str(ROOT/'scripts/correcciones99_layout_finish.py'))['apply']()
# New slabs/walls remain at original datums and water mesh is not touched by this patch.
report['rooms']={'mono_bath_inside':{'x':[19.39,21.8],'z':[.26,1.81],'floor':.21,'slab_soffit':3.0},'shower':{'x':[20.9,21.8],'z':[.26,1.71],'perimeter_y':.21,'drain_y':.1955,'rociador_clear_m':2.0999},'closet_mono':bounds(pc),'table_center_source_xz':[19.26,3.06],'kitchen_preserved':True,'bedroom_furniture_preserved':True,'wardrobe_closed_to_dining':True,'dining_passage_original_m':.805}
report['limits']=['Rigs are new geometrical proposals; hardware, structure and product selection need engineering confirmation.','PB slabs: old local sanitary voids closed and new local ones opened; reinforcement coordination remains required.','Wet wall finish continuity and D08 ventilation are separate patches.','Tour route/camera framing require regeneration for the new layout.']
report['protected_furniture_and_water_unchanged']=all(geom_sig(bpy.data.objects[n])==v for n,v in protected.items());report['protected_object_count']=len(protected);assert report['protected_furniture_and_water_unchanged']
S['r7_layout']=json.dumps(report,ensure_ascii=False);S['review_iteration']='99 / R7A layout';S['tour_route_requires_revalidation_after_layout']=True
S.frame_set(1);bpy.context.view_layer.update();bpy.context.preferences.filepaths.save_version=0
out=(ROOT/args.out).resolve();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True);report['output']=str(out);report['output_sha256']=hashlib.sha256(out.read_bytes()).hexdigest();(ROOT/'review99/layout_r7a_details.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf8');print('LAYOUT_SAVED',str(out),report['output_sha256'],flush=True)
