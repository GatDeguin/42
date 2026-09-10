"""R6A: furniture supports and service fixtures after independent dimensional audit."""
import bpy,os,math,json,ast,numpy as np,sys
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
for m in bpy.data.materials:
 if m.name.startswith('MAT95 | '):M[m.name.split(' | ',1)[1]]=m
def cv(p):return Vector((p[0],-p[2],p[1]))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_textiles.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['bounds','deform','map_h']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_materialidad.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['box','cyl','mesh','curve']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<fast>','exec'))
def erase(prefixes):
 for o in list(S.objects):
  if o.name.startswith(tuple(prefixes)):bpy.data.objects.remove(o,do_unlink=True)
def cut(o,c):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;m=o.modifiers.new('Reserva real R6','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=c;bpy.ops.object.modifier_apply(modifier=m.name)
# Sofa has20mm behind its rear envelope. Coffee table retains410mm from front of frame.
for o in S.objects:
 if o.name.startswith('Sofá vivienda'):o.location.y-=.11
 if o.name.startswith(('Mesa baja vivienda','MOB95 | pata mesa baja estar')):o.location.y-=.15
# Toilets have realistic finished-floor bearing and455mm seat height.
for body,prefix,floor in [('Inodoro mono','Inodoro mono',.21),('Inodoro quincho','Inodoro quincho',.21),('Inodoro vivienda','Inodoro suite',3.25)]:
 map_h(bpy.data.objects[body],floor,floor+.430)
 for suffix,lo,hi in [(' | asiento',.430,.455),(' | mochila compacta',.420,.770),(' | pulsador',.772,.784)]:
  ob=bpy.data.objects.get(prefix+suffix)
  if ob:map_h(ob,floor+lo,floor+hi)
map_h(bpy.data.objects['Bidet vivienda'],3.25,3.67)
# One vanity cabinet replaces duplicated bodies; actual wall face isX19.49.
erase(['Vanitory bajo suite','Mesada baño suite'])
cab=bpy.data.objects['Vanitory vivienda'];map_h(cab,3.38,3.98)
counter=box('Mesada baño suite',[19.780,4.000,6.720],[.570,.040,.740],'concrete','INTERIORS',.003)
for x in [19.57,19.99]:
 for z in [6.42,7.02]:box('MOB95 | pata vanitory suite',[x,3.315,z],[.025,.13,.025],'blackMetal','INTERIORS',.002)
for h in [3.535,3.835]:
 box('MOB95 | frente cajón vanitory',[20.050,h,6.72],[.020,.285,.672],'wood','INTERIORS',.003)
 for z in [6.54,6.90]:cyl('MOB95 | soporte tirador vanitory',[20.061,h+.050,z],[20.081,h+.050,z],.003,'blackMetal','INTERIORS')
 cyl('MOB95 | tirador vanitory',[20.081,h+.050,6.54],[20.081,h+.050,6.90],.004,'blackMetal','INTERIORS')
bpy.data.objects['Espejo baño suite'].location.x+=.112
bpy.data.objects['Grifería baño suite'].location+=cv([-.17,-.01,0])
# Drain passes through tabletop; basin remains supported on tabletop at+4.02.
c=cyl('TEMP desagüe vanitory',[19.70,3.94,6.73],[19.70,4.05,6.73],.021,'stainless','REFERENCE');cut(counter,c);bpy.data.objects.remove(c,do_unlink=True)
# Source refinements had two overlapping rack bodies. Keep equipment location, build one enclosure.
erase(['Rack estudio inferior','Rack estudio frente','Rack lateral estudio','Rack superior estudio','Subsuelo rack estudio'])
box('Subsuelo rack estudio',[20.78,3.28,1.55],[.62,.06,.62],'blackMetal','STUDIO',.004)
for z in [1.2425,1.8575]:box('Rack lateral estudio | chapa lateral',[20.78,3.975,z],[.66,1.33,.005],'blackMetal','STUDIO',.001)
for h in [3.315,4.635]:box('Rack estudio inferior | bandeja',[20.78,h,1.55],[.66,.010,.61],'blackMetal','STUDIO',.001)
box('Rack estudio inferior | fondo ventilado',[21.1075,3.975,1.55],[.005,1.32,.60],'blackMetal','STUDIO',.001)
for z in [1.300,1.800]:box('Rack estudio frente | montante19p',[20.481,3.975,z],[.020,1.32,.024],'blackMetal','STUDIO',.001)
for i in range(8):
 h=3.45+i*.105
 # Chassis cases sit behind the existing faceplate with direct rail fasteners.
 box('Rack audio | chasis unidad%02d'%i,[20.674,h,1.55],[.41,.079,.465],'blackMetal','STUDIO',.001)
 for z in [1.313,1.787]:
  for dh in [-.027,.027]:
   cyl('Rack audio | tornillo fijación',[20.438,h+dh,z],[20.490,h+dh,z],.002,'stainless','STUDIO')
# Vent openings through the rear sheet, sufficient topology to read service construction.
rear=bpy.data.objects['Rack estudio inferior | fondo ventilado']
for j in range(8):
 h=3.45+j*.14;c=box('TEMP ventilación rack',[21.1075,h,1.55],[.03,.008,.42],'blackMetal','REFERENCE',0);cut(rear,c);bpy.data.objects.remove(c,do_unlink=True)
S['review_iteration']='95 / R6A coordinated supports and sanitary heights'
S['r6a_furnishing']=json.dumps({'sofa_shift_source_z':.11,'coffee_shift_source_z':.15,'wc_seat_height_m':.455,'bidet_height_m':.42,'vanity_counter_top':4.02,'rack_base_top':3.31,'rack_location_preserved':'existing audio units remain in place; duplicate bodies replaced','status':'Dimensional furnishing proposal; no system capacity certification'})
S.frame_set(1);bpy.context.view_layer.update();bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
name='Casa_de_Campo_95_R6A_preview.blend' if '--preview' in sys.argv else 'Casa_de_Campo_95_R6A.blend'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output',name),compress=True);print('R6A_SAVED',flush=True)
