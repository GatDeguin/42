"""R4C: bathroom-dining access, flush wet-room floor and coordinated kitchen layout."""
import bpy,os,math,json,ast,numpy as np
from mathutils import Vector,Matrix
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
P=json.load(open(os.path.join(ROOT,'planos95','layout_r4','propuesta_bano_cocina.json'),encoding='utf8'))
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
for m in bpy.data.materials:
 if m.name.startswith('MAT95 | '):M[m.name.split(' | ',1)[1]]=m
def cv(p):return Vector((p[0],-p[2],p[1]))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_textiles.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['bounds','deform','map_h','erase']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_materialidad.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['box','cyl','curve','mesh']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<fast>','exec'))
def cut(o,c):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;m=o.modifiers.new('Reserva coordinada','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=c;bpy.ops.object.modifier_apply(modifier=m.name)
def bx(name,xb,yb,zb,mat='woodDark',col='INTERIORS',bev=.002):
 return box(name,[(xb[0]+xb[1])/2,(yb[0]+yb[1])/2,(zb[0]+zb[1])/2],[xb[1]-xb[0],yb[1]-yb[0],zb[1]-zb[0]],mat,col,bev)
def affine(o,old,new):
 o.matrix_world=Matrix.Translation(cv(new))@Matrix.Rotation(-math.pi/2,4,'Z')@Matrix.Translation(-cv(old))@o.matrix_world
# Proposed external sliding door: actual void through partition and crossing skirting.
c=bx('Temporal vano baño comedor',[19.55,20.52],[3.195,5.51],[8.40,8.88],col='REFERENCE',bev=0)
wall=bpy.data.objects['Baño tabique posterior'];cut(wall,c)
for o in list(S.objects):
 if o.type=='MESH' and 'zócalo' in o.name.lower():
  a,b=bounds(o);ca,cb=bounds(c)
  if np.all(np.minimum(b,cb)-np.maximum(a,ca)>.0001):cut(o,c)
bpy.data.objects.remove(c,do_unlink=True)
for x0,x1 in [(19.55,19.585),(20.485,20.52)]:bx('MOB95 | jamba baño comedor',[x0,x1],[3.25,5.51],[8.55,8.73],'woodDark','DOORS',.002)
bx('MOB95 | cabezal baño comedor',[19.55,20.52],[5.47,5.51],[8.55,8.73],'woodDark','DOORS',.002)
# Rail and five wall connections; leaf extends above clear head for real privacy overlap.
rail=bx('MOB95 | riel corredera baño comedor',[19.48,21.63],[5.555,5.59],[8.756,8.79],'blackMetal','DOORS',.001)
for x in [19.58,20.08,20.58,21.08,21.58]:
 cyl('MOB95 | anclaje riel baño',[x,5.57,8.68],[x,5.57,8.778],.006,'stainless','DOORS')
 bx('MOB95 | ménsula riel baño',[x-.022,x+.022],[5.53,5.61],[8.707,8.765],'blackMetal','DOORS',.001)
leaf=bx('Puerta baño comedor',[19.51,20.56],[3.26,5.50],[8.745,8.785],'woodDark','DOORS',.003)
# Recess handles are genuine recesses within the leaf on both sides; no projecting bar behind worktop.
groove=bx('Temporal ranura guía hoja',[19.509,20.561],[3.259,3.280],[8.759,8.769],col='REFERENCE',bev=0)
cut(leaf,groove);bpy.data.objects.remove(groove,do_unlink=True)
parts=[leaf]
for z in [8.747,8.783]:
 cutter=box('Temporal tirador embutido',[19.57,4.28,z],[.033,.105,.013],col='REFERENCE',bev=.004);cut(leaf,cutter);bpy.data.objects.remove(cutter,do_unlink=True)
 parts.append(box('Puerta baño comedor | fondo tirador',[19.57,4.28,z+(.005 if z<8.76 else -.005)],[.030,.10,.001],'blackMetal','DOORS',.003))
for x in [19.68,20.39]:
 parts.append(bx('Puerta baño comedor | pletina carro',[x-.018,x+.018],[5.465,5.603],[8.786,8.795],'blackMetal','DOORS',.001))
 parts.append(cyl('Puerta baño comedor | rueda carro',[x,5.611,8.765],[x,5.611,8.795],.021,'blackMetal','DOORS'))
bx('MOB95 | tapa desmontable riel baño',[19.45,21.66],[5.535,5.63],[8.807,8.819],'blackMetal','DOORS',.002)
for x in [19.49,21.62]:bx('MOB95 | tope riel baño',[x-.012,x+.012],[5.55,5.62],[8.757,8.805],'rubber95','DOORS',.002)
# Low guide outside the900mm passage, beside east jamb and below the panel.
bx('MOB95 | guía inferior lateral baño base',[20.523,20.551],[3.25,3.257],[8.735,8.777],'blackMetal','DOORS',.001)
bx('MOB95 | guía inferior lateral baño aleta',[20.523,20.551],[3.257,3.276],[8.762,8.766],'blackMetal','DOORS',.0005)
rig=bpy.data.objects.new('DOOR | bathDining',None);COL['DOORS'].objects.link(rig);rig.location=cv([19.51,3.25,8.765]);rig['open']=0.;rig['motion']='slide';rig['translation_source']='[1.02,0,0]';rig['owner_revision']='New bathroom-dining connection;900mm clear passage'
rig.id_properties_ui('open').update(min=0,max=1,description='0 closed /1 open')
bpy.context.view_layer.update()
for o in parts:
 mw=o.matrix_world.copy();o.parent=rig;o.matrix_world=mw
d=rig.driver_add('location',0).driver;d.expression='19.51 + opening * 1.02';v=d.variables.new();v.name='opening';v.type='SINGLE_PROP';v.targets[0].id=rig;v.targets[0].data_path='["open"]'
for fr,value in [(1,0),(30,0),(105,1),(1400,1),(1480,1)]:rig['open']=value;rig.keyframe_insert(data_path='["open"]',frame=fr)
# Reconstruct wet room50mm above actual structural slab, subtract from general finish.
old=bpy.data.objects.get('Piso baño vivienda')
if old:bpy.data.objects.remove(old,do_unlink=True)
main=[19.49,21.80,6.10,8.57];ext=[19.55,20.52,8.57,8.71]
for rect in [main,ext]:
 x0,x1,z0,z1=rect;c=bx('Temporal piso húmedo',[x0,x1],[3.199,3.301],[z0,z1],col='REFERENCE',bev=0);cut(bpy.data.objects['Piso vivienda'],c);bpy.data.objects.remove(c,do_unlink=True)
 for idx,(name,h0,h1,mat) in enumerate([('base30mm',3.20,3.23,'concrete'),('membrana2mm',3.23,3.232,'rubber95'),('adhesivo8mm',3.232,3.24,'concrete'),('baldosa10mm',3.24,3.25,'tile')]):
  nm='Piso baño vivienda' if rect is main and idx==3 else 'MOB95 | piso baño '+name+(' umbral' if rect is ext else '')
  ob=bx(nm,[x0,x1],[h0,h1],[z0,z1],mat,'UPPER_FLOOR',0);ob['layer_status']='P: coordinated geometric thickness; product/system selection to verify'
# Membrane extension150mm under the dry finish. Cut corresponding volume to avoid doubled solids.
c=bx('Temporal banda impermeable lado seco',[19.55,20.52],[3.23,3.232],[8.71,8.86],col='REFERENCE',bev=0);cut(bpy.data.objects['Piso vivienda'],c);bpy.data.objects.remove(c,do_unlink=True)
bx('MOB95 | banda impermeable continua baño',[19.55,20.52],[3.23,3.232],[8.71,8.86],'rubber95','UPPER_FLOOR',0)
# Joint through only the upper10mm, exactly level with both floor finishes.
c=bx('Temporal junta elástica baño',[19.55,20.52],[3.24,3.251],[8.7075,8.7125],col='REFERENCE',bev=0)
for o in [bpy.data.objects['Piso vivienda']]+[o for o in S.objects if o.name.startswith('MOB95 | piso baño baldosa10mm umbral')]:cut(o,c)
bpy.data.objects.remove(c,do_unlink=True)
bx('MOB95 | junta elástica baño comedor',[19.55,20.52],[3.24,3.25],[8.7075,8.7125],'rubber95','UPPER_FLOOR',0)
moved=[]
for row in P['bath_objects_moves']:
 o=bpy.data.objects.get(row['name'])
 if not o or o.name.startswith('Nicho ducha'):continue
 a,b=bounds(o)
 if b[2]<3.20:continue # Excludes accidental ground-floor name matches.
 o.location+=cv(row['source_delta']);moved.append(o.name)
ceil=bpy.data.objects[P['bath_floor']['ceiling_move']['name']];ceil.location.z-=.05;ceil['finished_clear_height']=2.60
# Old peninsula, stools and their skirting are removed from the new route.
erase(P['kitchen']['remove_and_rebuild']+['Zócalo península cocina'])
# L return extends only to the linear top face. Union avoids overlapping coplanar worktops.
counter=bpy.data.objects['Cocina lineal mesada']
extension=bx('Temporal unión mesada L',[20.74,21.30],[4.1025,4.1575],[8.86,9.48],'concrete','INTERIORS',0)
bpy.context.view_layer.update();bpy.context.view_layer.objects.active=counter;md=counter.modifiers.new('Retorno continuo L','BOOLEAN');md.operation='UNION';md.solver='EXACT';md.object=extension;bpy.ops.object.modifier_apply(modifier=md.name);bpy.data.objects.remove(extension,do_unlink=True)
counter['layout_revision']='Continuous L counter; bathroom sliding leaf passes behind independent return'
bx('Península cocina base coordinada',[20.765,21.135],[3.35,4.1025],[8.885,9.455],'woodDark','INTERIORS',.003)
bx('MOB95 | zócalo retorno cocina',[20.805,21.135],[3.25,3.35],[8.925,9.415],'blackMetal','INTERIORS',.002)
bx('Península cocina frente coordinado',[20.757,21.125],[3.37,4.084],[9.449,9.469],'woodDark','INTERIORS',.003)
box('MOB95 | tirador retorno cocina',[20.94,3.975,9.48],[.22,.012,.016],'stainless','INTERIORS',.003)
# Correct hood clearance from actual hob geometry, leave its continuous riser in place.
hob=bpy.data.objects.get('Anafe cocina');hood=bpy.data.objects.get('Campana cocina visera')
hood_raise=0
if hob and hood:
 ha,hb=bounds(hob);a,b=bounds(hood);hood_raise=max(0,.65-(a[2]-hb[2]))
 for name in ['Campana cocina','Campana cocina visera']:
  ob=bpy.data.objects.get(name)
  if ob:ob.location.z+=hood_raise;ob['hob_clearance_proposed_m']=.65
# Upper cupboards stop before the extractor rather than overlapping its body.
erase(['Alacena cocina','Luz bajo alacena cocina'])
bx('Alacena cocina fondo',[21.765,21.785],[4.84,5.55],[9.18,9.96],'woodDark','INTERIORS',.001)
for zz in [9.189,9.57,9.951]:bx('Alacena cocina costado',[21.43,21.78],[4.84,5.55],[zz-.009,zz+.009],'woodDark','INTERIORS',.001)
for h in [4.849,5.20,5.541]:bx('Alacena cocina estante',[21.43,21.78],[h-.009,h+.009],[9.18,9.96],'woodDark','INTERIORS',.001)
for i,z in enumerate([9.375,9.765]):
 bx('Alacena cocina puerta %d'%i,[21.41,21.428],[4.845,5.545],[z-.190,z+.190],'woodDark','INTERIORS',.003)
 box('Alacena cocina tirador %d'%i,[21.402,5.13,z-.12],[.014,.22,.013],'stainless','INTERIORS',.002)
# Extra storage above refrigerator reuses the available vertical void without restricting its door.
bx('Alacena sobre heladera',[21.435,21.78],[5.51,5.80],[10.88,11.60],'woodDark','INTERIORS',.003)
bx('MOB95 | difusor bajo alacena',[21.44,21.46],[4.832,4.836],[9.20,9.94],'warmLight','LIGHTS',.001)
# Final coordinated table positions. Four lateral chairs, no chair at the rear glazing.
oldpivot=[18.15,0,10.48];newpivot=[17.75,0,10.70]
for name in P['dining']['objects']:
 o=bpy.data.objects.get(name)
 if o:affine(o,oldpivot,newpivot)
for o in list(S.objects):
 if o.name in ['Lámpara comedor','Cable lámpara comedor 17.69','Cable lámpara comedor 18.61','Florero comedor'] or o.name=='MOB95 | difusor opal Lámpara comedor':
  affine(o,oldpivot,newpivot)
# Remove stale earlier decorations/cables which belong to a superseded table position.
erase(['Florero comedor curado','Cable lámpara comedor A','Cable lámpara comedor B'])
vase=bpy.data.objects.get('Florero comedor')
if vase:
 a,b=bounds(vase);vase.location.z+=4.0-a[2]
coffee=bpy.data.objects.get('Mesa baja vivienda')
if coffee:
 affine(coffee,[15.60,0,10.47],[15.44,0,10.62]);map_h(coffee,3.59,3.65)
 for x in [15.26,15.62]:
  for z in [10.34,10.90]:box('MOB95 | pata mesa baja estar',[x,3.42,z],[.025,.34,.025],'blackMetal','INTERIORS',.002)
# Align pendant and diffuser with the shorter worktop. Light sources follow physical luminaires.
for o in S.objects:
 if o.name.startswith(('Lámpara lineal cocina','MOB95 | difusor opal Lámpara lineal cocina')):
  o.location.x+=21.18-20.18;o.location.y-=9.17-9.05
 if o.type=='LIGHT' and 'comedor' in o.name.lower():
  o.location.x=17.75;o.location.y=-10.70
# Add light-weight edit metadata; tour remains paused and flagged for route revalidation.
S['review_iteration']='95 / R4C bathroom dining door and coordinated kitchen'
S['video_render_requires_explicit_approval']=True;S['tour_route_requires_revalidation_after_layout']=True
S['bath_dining_layout95']=json.dumps({'clear_door_width_m':.90,'clear_door_height_m':2.22,'leaf_overlap_head_mm':30,'travel_m':1.02,'floor_level':3.25,'bath_clear_height_m':2.60,'bath_objects_moved':moved,'niche':'existing wall opening retained at absolute elevation','table_center_xz':[17.75,10.70],'coffee_center_xz':[15.44,10.62],'fridge_simultaneous_clearance_proposed_m':.824,'oven_simultaneous_clearance_proposed_m':.974,'hood_raise_m':float(hood_raise),'hood_clearance_proposed_m':.65},ensure_ascii=False)
S.frame_set(1);bpy.context.view_layer.update();bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_95_R4C.blend'),compress=True)
json.dump(json.loads(S['bath_dining_layout95']),open(os.path.join(ROOT,'review95','layout_r4c.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
print('R4C_SAVED_NO_VIDEO',len([o for o in S.objects if o.name.startswith('DOOR |')]),flush=True)
