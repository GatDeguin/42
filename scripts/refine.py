import bpy,sys,os,json,math
from mathutils import Vector,Matrix
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'output');S=bpy.context.scene
for o in S.objects:
 if o.name.startswith('Entorno arbolado'):
  # Move supplementary trees behind the prescribed external cameras, outside the lot.
  i=int(o.name.split()[2]);shift=Vector((0,-8,0)) if i in [2,3,4,5,6] else Vector((-5,0,0)) if i in [0,1,11] else Vector((5,0,0))
  o.location+=shift
# A continuous distant landscape prevents the finite source ground creating a black horizon.
mat=next(m for m in bpy.data.materials if m.get('source_material_key')=='outerGrass')
p=[];f=[]
def quad(x0,y0,x1,y1):
 i=len(p);p.extend([(x0,y0,-.16),(x1,y0,-.16),(x1,y1,-.16),(x0,y1,-.16)]);f.append((i,i+1,i+2,i+3))
quad(-300,-300,300,-20);quad(-300,0,300,300);quad(-300,-20,0,0);quad(22,-20,300,0)
me=bpy.data.meshes.new('Terreno lejano');me.from_pydata(p,[],f);me.materials.append(mat);o=bpy.data.objects.new('Entorno | terreno continuo',me);bpy.data.collections['LANDSCAPE'].objects.link(o)
# Use realistic material swatches in the solid viewport as well.
data=json.load(open(os.path.join(ROOT,'source','scene.json'),encoding='utf8'))
def lin(v):return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
for m in bpy.data.materials:
 key=m.get('source_material_key')
 if key in data['materials']:
  d=data['materials'][key];profile=data['profiles'].get(d.get('texture'))
  if profile:m.diffuse_color=tuple(lin(v/255)*c for v,c in zip(profile['rgb'],d['color']))+(1,)
# Ordinary mesh transforms, linked vegetation remains instanced.
for o in S.objects:
 if o.type=='MESH' and o.data.users==1 and not o.parent and not o.modifiers:
  sc=o.scale.copy();o.data.transform(Matrix.Diagonal((sc.x,sc.y,sc.z,1)));o.scale=(1,1,1)
# Roof-off inspection scene and orthographic plan camera.
inspection=bpy.data.scenes.new('INSPECCIÓN | Planta alta')
for c in S.collection.children:
 if c.name not in ['ROOF','REFERENCE']:inspection.collection.children.link(c)
inspection.world=bpy.data.worlds['Cielo físico | DÍA'];inspection.render.engine='CYCLES';inspection.cycles.device='GPU';inspection.cycles.samples=64;inspection.cycles.use_denoising=True
inspection.unit_settings.system='METRIC';inspection.render.resolution_x=1400;inspection.render.resolution_y=1400;inspection.view_settings.view_transform='AgX';inspection.view_settings.exposure=.3
cd=bpy.data.cameras.new('Planta alta | ortogonal seccionada');co=bpy.data.objects.new('CAM | Planta alta ortogonal',cd);bpy.data.collections['CAMERAS'].objects.link(co);co.location=(18,-6,18);co.rotation_euler=(0,0,0);cd.type='ORTHO';cd.ortho_scale=14;cd.clip_start=13.15;cd.clip_end=100;inspection.camera=co
S.frame_set(1);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas']
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':
  area.spaces.active.shading.color_type='MATERIAL';area.spaces.active.region_3d.view_perspective='CAMERA'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Casa_de_Campo.blend'))
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='OPTIX';p.get_devices()
for d in p.devices:d.use=d.type=='OPTIX'
S.render.resolution_x=1200;S.render.resolution_y=900;S.cycles.samples=48;S.render.filepath=os.path.join(OUT,'preview_v2.png');bpy.ops.render.render(write_still=True)
