import bpy,os,sys,json,math,random,time
from mathutils import Vector,Matrix
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'output');S=bpy.context.scene;S.frame_set(1)
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m}
def cv(p):return Vector((p[0],-p[2],p[1]))
def box(name,p,d,mat,col):
 bpy.ops.mesh.primitive_cube_add(size=1,location=cv(p));o=bpy.context.object;o.name=name;o.dimensions=(d[0],d[2],d[1]);o.data.materials.append(M[mat])
 for c in list(o.users_collection):c.objects.unlink(o)
 bpy.data.collections[col].objects.link(o)
 return o
# Black housing with small diffuser, instead of an entirely emissive solid fixture at eye level.
o=bpy.data.objects.get('Aplique descanso')
if o:
 o.data.materials.clear();o.data.materials.append(M['blackMetal'])
 box('Aplique descanso | difusor inferior',[13.996,4.65,5.45],[.008,.045,.14],'warmLight','LIGHTS')
 box('Aplique descanso | difusor superior',[13.996,4.87,5.45],[.008,.032,.14],'warmLight','LIGHTS')
# Richer lawn at the source lawn positions, using linked repeated geometry.
rng=random.Random(554)
for o in [o for o in S.objects if o.name.startswith('Césped volumétrico')]:
 for j in range(5):
  d=o.copy();d.data=o.data;d.name='Césped complemento | '+o.name+' '+str(j);bpy.data.collections['LANDSCAPE'].objects.link(d)
  d.location.x+=rng.uniform(-.055,.055);d.location.y+=rng.uniform(-.055,.055);d.scale.z*=rng.uniform(.76,1.13)
# Populate a layered grove strictly outside the plot and outside the source camera locations.
for o in list(bpy.data.objects):
 if o.name.startswith('Entorno arbolado'):bpy.data.objects.remove(o,do_unlink=True)
parts=[o for o in S.objects if o.name.startswith('Árbol lote 2')]
poses=[(-7+i*3.1,29+rng.uniform(0,3)) for i in range(14)]+[(27+rng.uniform(0,3),3+i*3.1) for i in range(9)]+[(-7+rng.uniform(-2,0),5+i*4) for i in range(5)]
for i,(x,z) in enumerate(poses):
 factor=rng.uniform(1.6,2.55);rot=Matrix.Rotation(rng.uniform(0,math.tau),4,'Z')
 T=Matrix.Translation(cv([x,0,z]))@rot@Matrix.Diagonal((factor,factor,factor,1))@Matrix.Translation(-cv([4.3,0,16.8]))
 for p in parts:
  o=p.copy();o.data=p.data;o.name='Arboleda exterior %02d | %s'%(i,p.name);bpy.data.collections['LANDSCAPE'].objects.link(o);o.matrix_world=T@p.matrix_world
# Softer practical illumination, keeping the two bedside lamps readable.
for o in S.objects:
 if o.type=='LIGHT' and o.name.startswith('LED |') and ('cocina' in o.name.lower() or 'vivienda' in o.name.lower()):
  o.data.energy*=.68
# Preserve the physically based sky, expose a slightly brighter late-afternoon presentation.
S.view_settings.exposure=.35
bpy.context.preferences.filepaths.save_version=0
S.camera=bpy.data.objects['CAM | Presentación verticales corregidas']
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Casa_de_Campo.blend'))
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
for d in pref.devices:d.use=d.type=='OPTIX'
S.render.resolution_x=1200;S.render.resolution_y=900;S.cycles.samples=48;S.cycles.use_denoising=True;S.render.filepath=os.path.join(OUT,'preview_v4.png');bpy.ops.render.render(write_still=True)
# Explicit A/B performance check for animation denoising on this GPU.
print('DENOISER_PROPS',[p for p in S.cycles.bl_rna.properties.keys() if 'denois' in p],flush=True)
S.camera=bpy.data.objects['TOUR | Recorrido virtual'];S.render.resolution_x=1280;S.render.resolution_y=720;S.cycles.samples=24;S.cycles.adaptive_threshold=.065
S.cycles.denoiser='OPTIX';S.cycles.denoising_use_gpu=True
for fr in [760,761,1120]:
 t=time.time();S.frame_set(fr);S.render.filepath=os.path.join(OUT,'fastbench_%04d.png'%fr);bpy.ops.render.render(write_still=True);print('FAST_BENCH',fr,time.time()-t,flush=True)
