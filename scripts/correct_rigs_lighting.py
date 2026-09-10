import bpy, math, json, os, sys, ast, numpy as np
from mathutils import Matrix,Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'output');sys.path.insert(0,os.path.join(ROOT,'scripts'))
S=bpy.context.scene;DATA=json.load(open(os.path.join(ROOT,'source','scene.json'),encoding='utf8'))
S.frame_set(1);bpy.context.view_layer.update()
C=Matrix(((1,0,0,0),(0,0,-1,0),(0,1,0,0),(0,0,0,1)))
# Restore source closed transforms before rebuilding the corrected hierarchy.
rigs=[o for o in S.objects if o.name.startswith('DOOR |')]
for o in list(S.objects):
 if '| paño fijo' in o.name:bpy.data.objects.remove(o,do_unlink=True)
for rig in rigs:
 for o in list(rig.children):
  if 'source_id' in o:
   m=DATA['meshes'][o['source_id']];o.parent=None;o.matrix_parent_inverse=Matrix.Identity(4)
   o.matrix_world=C@Matrix(np.array(m['matrix']).reshape(4,4).T.tolist())@C.inverted()
  else:bpy.data.objects.remove(o,do_unlink=True)
 bpy.data.objects.remove(rig,do_unlink=True)
COL={c.name:c for c in bpy.data.collections}
MATS={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m}
MATS.update({m.name:m for m in bpy.data.materials if m.name in ['meterCyan','meterAmber','meterGreen','embers']})
OBJS={o['source_id']:o for o in S.objects if 'source_id' in o}
for o in OBJS.values():
 if o.name=='Baño mono puerta':o.location.z=1.285
corrections=json.loads(S['corrections'])
text=open(os.path.join(ROOT,'scripts','build_scene.py'),encoding='utf8').read()
for node in ast.parse(text).body:
 if isinstance(node,ast.FunctionDef) and node.name in ['cv','mat_from','put','empty','box']:
  exec(ast.get_source_segment(text,node),globals())
from doors_tour import setup_doors
RIGS=setup_doors(globals())
for e in RIGS.values():
 for layer in e.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:
      if k.co.x>=1400:k.co.y=1
# Adjusted presentation camera, retaining every exact source camera.
cam=bpy.data.objects['CAM | Presentación verticales corregidas'];cam.location=cv([7.2,6.8,21.5])
cam.rotation_euler=(cv([17.0,6.8,9.4])-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=29;cam.data.shift_y=-.17
for o in bpy.data.objects:
 if o.type=='CAMERA':o.data.clip_end=10000
# Photographic sunset environment, with the original procedural worlds retained as day/night alternatives.
w=S.world;nodes=w.node_tree.nodes;links=w.node_tree.links
out=next(n for n in nodes if n.type=='OUTPUT_WORLD');bg=next(n for n in nodes if n.type=='BACKGROUND')
env=nodes.new('ShaderNodeTexEnvironment');env.image=bpy.data.images.load(os.path.join(ROOT,'source','belfast_sunset_2k.hdr'));env.image.pack();env.label='Poly Haven / Belfast Sunset / CC0'
tc=nodes.new('ShaderNodeTexCoord');mapping=nodes.new('ShaderNodeMapping');mapping.inputs['Rotation'].default_value[2]=math.radians(45)
links.new(tc.outputs['Generated'],mapping.inputs['Vector']);links.new(mapping.outputs['Vector'],env.inputs['Vector']);links.new(env.outputs['Color'],bg.inputs['Color']);bg.inputs['Strength'].default_value=.45
ld=bpy.data.lights.new('Sol | Atardecer cálido','SUN');ld.energy=1.65;ld.color=(1,.66,.39);ld.angle=math.radians(1.4)
sun=bpy.data.objects.new('Sol | Atardecer cálido',ld);COL['LIGHTS'].objects.link(sun);sun.location=cv([-25,9,25]);sun.rotation_euler=(cv([17,2,8])-sun.location).to_track_quat('-Z','Y').to_euler()
# Bedroom practical lamps were inert source geometry. Light them at their specified locations.
for z in [6.18,8.78]:
 d=bpy.data.lights.new('Suite | lámpara de lectura','POINT');d.energy=20;d.color=(1,.70,.43);d.shadow_soft_size=.12
 o=bpy.data.objects.new(d.name,d);o.location=cv([15.08,4.18,z]);COL['LIGHTS'].objects.link(o)
# Make central listening-area acoustic clearance visible and traceable.
S.view_settings.exposure=.25
S['corrections']=json.dumps(list(dict.fromkeys(corrections)),ensure_ascii=False)
S.frame_set(1);bpy.context.view_layer.update()
door_report=[]
for key in ['studio','suiteEntry','bedroomLink','bathLink','poolBath']:
 idx=DATA['doors'][key][0];o=OBJS[idx];expect=cv(DATA['meshes'][idx]['position'])
 error=(o.matrix_world.translation-expect).length;door_report.append({'door':key,'closed_position_error_m':error})
print('CLOSED_DOOR_CHECK',json.dumps(door_report),flush=True)
assert max(x['closed_position_error_m'] for x in door_report)<.001
v=json.load(open(os.path.join(OUT,'validation.json'),encoding='utf8'));v['checks'].append({'name':'Hinged door closed transforms match source after parenting','pass':True,'measured':door_report})
v['checks'].append({'name':'Rear sliders fit original glazing bays in closed pose','pass':all(abs(OBJS[i].dimensions.x-DATA['meshes'][i]['scale'][0]/2)<.003 for i in DATA['doors']['balconyRear'])})
v['corrections']=list(dict.fromkeys(corrections));json.dump(v,open(os.path.join(OUT,'validation.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Casa_de_Campo.blend'))
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='OPTIX';p.get_devices()
for d in p.devices:d.use=d.type=='OPTIX'
S.camera=cam;S.render.resolution_x=1200;S.render.resolution_y=900;S.cycles.samples=48;S.render.filepath=os.path.join(OUT,'preview_v3.png');bpy.ops.render.render(write_still=True)
