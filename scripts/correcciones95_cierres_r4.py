"""Closure of saved R4C: slide path skirtings, supported hanger plates, screen assembly and views."""
import bpy,os,math,json,ast,numpy as np
from mathutils import Vector,Matrix
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
def cv(p):return Vector((p[0],-p[2],p[1]))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_textiles.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['bounds','deform','map_h']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_materialidad.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['box','cyl']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<fast>','exec'))
def cut(o,c):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;m=o.modifiers.new('Reserva al recorrido completo','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=c;bpy.ops.object.modifier_apply(modifier=m.name)
c=box('Temporal recorrido inferior corredera baño',[20.55,3.32,8.767],[2.12,.16,.066],col='REFERENCE',bev=0)
touched=[]
for o in [v for v in S.objects if v.type=='MESH' and 'zócalo' in v.name.lower()]:
 a,b=bounds(o);ca,cb=bounds(c)
 if np.all(np.minimum(b,cb)-np.maximum(a,ca)>.0001):cut(o,c);touched.append(o.name)
bpy.data.objects.remove(c,do_unlink=True)
o=bpy.data.objects['Zócalo cocina lineal']
deform(o,lambda p:Vector((p.x,min(p.y,-8.885),p.z)))
# Keep carriage sideplates beside the rail; steel studs transfer load into the wood leaf.
rig=bpy.data.objects['DOOR | bathDining'];bpy.context.view_layer.update()
for o in [v for v in rig.children if v.name.startswith('Puerta baño comedor | pletina carro')]:
 o.location.y-=.008
for x in [19.68,20.39]:
 for h in [5.474,5.494]:
  o=cyl('Puerta baño comedor | perno carro',[x,h,8.770],[x,h,8.803],.0035,'stainless','DOORS');bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=rig;o.matrix_world=mw
# DAW waveform geometry must remain registered to the screen it represents.
for o in S.objects:
 if o.name.startswith('DAW | '):o.location.z-=.223
# Apply the source-derived fine longitudinal timber shaders also to objects created after R4B.
woods={}
for m in bpy.data.materials:
 if m.name.startswith(('Roble aceitado | ','Nogal mate | ')) and 'parquet' not in m.name:
  axis=int(m.name.split(' | ',1)[1].split()[0]);woods[('wood' if m.name.startswith('Roble') else 'woodDark',axis)]=m
for o in S.objects:
 if o.type!='MESH' or o.hide_render:continue
 for slot in o.material_slots:
  key=slot.material.get('source_material_key') if slot.material else None
  if key in ['wood','woodDark']:
   axis=int(np.argmax(o.dimensions))
   if (key,axis) in woods:slot.link='OBJECT';slot.material=woods[key,axis]
# Views avoid the open bedroom leaf; source cameras remain stored separately.
for name,p,t,lens in [('REV | Dormitorio completo',[17.23,4.87,7.63],[15.50,4.20,6.82],22),('REV | Dormitorio acceso',[14.57,4.87,8.60],[15.90,4.25,6.76],24),('REV | Baño acceso comedor',[19.92,4.92,10.00],[20.10,4.30,7.50],25)]:
 ob=bpy.data.objects.get(name)
 if ob is None:
  data=bpy.data.cameras.new(name);ob=bpy.data.objects.new(name,data);COL['CAMERAS'].objects.link(ob)
 ob.location=cv(p);ob.rotation_euler=(cv(t)-ob.location).to_track_quat('-Z','Y').to_euler();ob.data.lens=lens;ob.data.dof.use_dof=False;ob['presentation_frame']=150
S['review_iteration']='95 / R4D coordinated slide and assembled interiors';S['r4d_closures']=json.dumps({'skirting_cut':touched,'DAW_translation_m':-.223,'carriage_sideplate_rail_clearance_m':.003,'cameras_avoid_open_bedroom_leaf':True})
S.frame_set(1);bpy.context.view_layer.update();bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_95_R4D.blend'),compress=True)
print('R4D_SAVED',touched,flush=True)
