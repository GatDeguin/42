import bpy, math, json, os, sys, re, time, random
from mathutils import Vector, Matrix
import numpy as np
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(ROOT,'scripts'))
OUT=os.path.join(ROOT,'output')
os.makedirs(OUT,exist_ok=True)
DATA=json.load(open(os.path.join(ROOT,'source','scene.json'),encoding='utf8'))
bpy.ops.wm.read_factory_settings(use_empty=True)
S=bpy.context.scene
S.name='CASA DE CAMPO | Atardecer'
S.unit_settings.system='METRIC';S.unit_settings.length_unit='METERS';S.unit_settings.scale_length=1
COL={}
for n in ['SITE','GROUND_FLOOR','UPPER_FLOOR','ROOF','STAIR','POOL','QUINCHO','STUDIO','INTERIORS','FURNITURE','LANDSCAPE','LIGHTS','CAMERAS','DOORS','REFERENCE']:
 c=bpy.data.collections.new(n);S.collection.children.link(c);COL[n]=c
C=Matrix(((1,0,0,0),(0,0,-1,0),(0,1,0,0),(0,0,0,1)))
def cv(p):return Vector((p[0],-p[2],p[1]))
def mat_from(a):return Matrix(np.array(a).reshape(4,4).T.tolist())
def put(obj,col):COL[col].objects.link(obj);return obj
def empty(name,pos,col='REFERENCE'):
 o=bpy.data.objects.new(name,None);o.location=cv(pos);o.empty_display_size=.15;put(o,col);return o
anchor=empty('Material coordinates | metres / world',[0,0,0])
from materials import create_materials
MATS=create_materials(DATA,ROOT,anchor)
def classify(m):
 n=m['name'].lower();p=m['position'];layer=m['layer']
 if layer=='roof':return 'ROOF'
 if layer=='stair':return 'STAIR'
 if any(w in n for w in ['pileta','losetas','playa húmeda']):return 'POOL'
 if m['instances'] or any(w in n for w in ['árbol','huerta','hortaliza','vegetación','césped','arbusto']):return 'LANDSCAPE'
 if 'balcón' in n or 'baranda' in n or 'descanso' in n:return 'UPPER_FLOOR'
 if any(w in n for w in ['estudio','consola','monitor ','woofer','tweeter','fader','perilla','carril fader','medidor consola']):return 'STUDIO'
 if any(w in n for w in ['quincho','parrilla','horno de barro','cúpula horno','boca horno','base horno','bacha doble','mueble bacha','mesada bacha','chimenea horno','brasero','ceniza']):return 'QUINCHO'
 if layer in ('upperDetail','lowerDetail'):return 'INTERIORS'
 if layer=='upper':return 'UPPER_FLOOR'
 if layer=='lower':return 'GROUND_FLOOR'
 return 'SITE'
def mesh_from(name,p,n,uv,idx):
 p=np.asarray(p,dtype=np.float32).reshape(-1,3);n=np.asarray(n,dtype=np.float32).reshape(-1,3);uv=np.asarray(uv,dtype=np.float32).reshape(-1,2);idx=np.asarray(idx,dtype=np.int32).reshape(-1,3).copy()
 # Winding in some source grids differs from explicit normals. Correct it.
 cross=np.cross(p[idx[:,1]]-p[idx[:,0]],p[idx[:,2]]-p[idx[:,0]])
 flip=np.einsum('ij,ij->i',cross,n[idx].mean(axis=1))<0
 idx[flip]=idx[flip][:,[0,2,1]]
 me=bpy.data.meshes.new(name)
 me.vertices.add(len(p));me.vertices.foreach_set('co',p.reshape(-1))
 me.loops.add(idx.size);me.loops.foreach_set('vertex_index',idx.reshape(-1))
 me.polygons.add(len(idx));me.polygons.foreach_set('loop_start',np.arange(len(idx),dtype=np.int32)*3);me.polygons.foreach_set('loop_total',np.full(len(idx),3,dtype=np.int32));me.polygons.foreach_set('use_smooth',np.ones(len(idx),dtype=np.bool_))
 me.update()
 layer=me.uv_layers.new(name='SourceUV');layer.uv.foreach_set('vector',uv[idx.reshape(-1)].reshape(-1))
 try:me.normals_split_custom_set_from_vertices(n.tolist())
 except Exception:pass
 return me
GEO={}
for i,g in enumerate(DATA['geometries']):
 p=np.asarray(g['positions']).reshape(-1,3);n=np.asarray(g['normals']).reshape(-1,3)
 p=p[:,[0,2,1]]*np.array([1,-1,1]);n=n[:,[0,2,1]]*np.array([1,-1,1])
 GEO[i]=mesh_from('Source geometry %03d'%i,p,n,g['uvs'],g['indices'])
print('GEOMETRIES',len(GEO),flush=True)
OBJS={};rng=random.Random(681)
for m in DATA['meshes']:
 if m['layer']=='sky' or m['material']=='contactShadow':continue
 mat=MATS.get(m['material'],MATS['whitePlaster'])
 if m['instances']:
  g=DATA['geometries'][m['geometry']]
  pp=np.asarray(g['positions'],dtype=np.float32).reshape(-1,3);nn=np.asarray(g['normals'],dtype=np.float32).reshape(-1,3)
  ins=np.asarray(m['instances'],dtype=np.float32).reshape(-1,4,4).transpose(0,2,1)
  p=np.einsum('nij,vj->nvi',ins[:,:3,:3],pp)+ins[:,:3,3][:,None,:]
  nm=np.linalg.inv(ins[:,:3,:3]).transpose(0,2,1)
  n=np.einsum('nij,vj->nvi',nm,nn);n/=np.maximum(np.linalg.norm(n,axis=2)[:,:,None],1e-8)
  p=p.reshape(-1,3)[:,[0,2,1]]*np.array([1,-1,1]);n=n.reshape(-1,3)[:,[0,2,1]]*np.array([1,-1,1])
  idx=np.asarray(g['indices']).reshape(-1,3)[None,:,:]+(np.arange(len(ins))*len(pp))[:,None,None]
  uv=np.tile(np.asarray(g['uvs']).reshape(-1,2),(len(ins),1))
  me=mesh_from(m['name']+' | editable source instances',p,n,uv,idx)
  me['source_instance_count']=len(ins)
  attr=me.color_attributes.new(name='leaf_tint',type='FLOAT_COLOR',domain='POINT')
  tones=np.array([[rng.uniform(.75,1.1),rng.uniform(.83,1.1),rng.uniform(.72,1.0),1] for _ in ins],dtype=np.float32)
  attr.data.foreach_set('color',np.repeat(tones,len(pp),axis=0).reshape(-1))
 else:me=GEO[m['geometry']].copy()
 me.materials.clear();me.materials.append(mat)
 obj=bpy.data.objects.new(m['name'],me);put(obj,classify(m))
 obj.matrix_world=C@mat_from(m['matrix'])@C.inverted()
 obj['source_id']=m['id'];obj['source_layer']=m['layer'];obj['source_position_xyz']=m['position'];obj['source_size_xyz']=m['scale'];obj['source_material']=m['material']
 # Source geometry is already bevelled. Preserve explicit custom normals.
 OBJS[m['id']]=obj
 if m['id']%200==0:print('IMPORTED',m['id'],flush=True)
for me in list(bpy.data.meshes):
 if me.users==0:bpy.data.meshes.remove(me)
def box(name,p,size,mat,col,bevel=.003):
 x,y,z=[v/2 for v in size]
 verts=[(a*x,b*y,c*z) for a,b,c in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
 faces=[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)]
 me=bpy.data.meshes.new(name);me.from_pydata([cv(v) for v in verts],[],faces);me.materials.append(MATS[mat]);me.update()
 o=bpy.data.objects.new(name,me);put(o,col);o.location=cv(p)
 if bevel:mod=o.modifiers.new('Soft construction edge','BEVEL');mod.width=bevel;mod.segments=2
 return o
def light(name,p,energy,color=(1,.73,.46),size=.2,target=None,type='AREA'):
 d=bpy.data.lights.new(name,type);d.energy=energy;d.color=color
 if type=='AREA':d.shape='DISK';d.size=size
 elif type=='POINT':d.shadow_soft_size=size
 o=put(bpy.data.objects.new(name,d),'LIGHTS');o.location=cv(p)
 if target is not None:o.rotation_euler=(cv(target)-o.location).to_track_quat('-Z','Y').to_euler()
 o['sunset_watts']=energy;return o
def target_cam(name,p,t,lens):
 d=bpy.data.cameras.new(name);d.lens=lens;d.sensor_width=36;d.clip_start=.035;d.clip_end=250
 o=put(bpy.data.objects.new(name,d),'CAMERAS');o.location=cv(p);o.rotation_euler=(cv(t)-o.location).to_track_quat('-Z','Y').to_euler();d.dof.use_dof=False
 o['source_position_xyz']=p;o['source_target_xyz']=t
 return o
from detailing import enrich
corrections=enrich(globals())
from doors_tour import setup_doors,setup_tour
RIGS=setup_doors(globals())
CAM={}
for key,v in DATA['views'].items():CAM[key]=target_cam('CAM | '+v['label'],v['p'],v['t'],v['f'])
CAM['bathroom']=target_cam('CAM | Baño suite',[20.06,4.88,8.43],[20.9,4.35,6.7],18)
CAM['mono']=target_cam('CAM | Monoambiente',[18.4,1.86,5.36],[16.85,1.25,2.4],22)
# Add an architecturally corrected counterpart; source camera remains exact.
v=DATA['views']['hero'];CAM['presentation']=target_cam('CAM | Presentación verticales corregidas',v['p'],[v['t'][0],v['p'][1],v['t'][2]],26)
CAM['presentation'].data.shift_y=-.16
world=bpy.data.worlds.new('Cielo físico | Atardecer');world.use_nodes=True
nt=world.node_tree;nt.nodes.clear();wo=nt.nodes.new('ShaderNodeOutputWorld');bg=nt.nodes.new('ShaderNodeBackground');sky=nt.nodes.new('ShaderNodeTexSky')
sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(9);sky.sun_rotation=math.radians(140);sky.altitude=.15;sky.air_density=1.0;sky.aerosol_density=2.0;sky.ozone_density=1
sky.sun_disc=True;sky.sun_size=math.radians(.9);sky.sun_intensity=.65
bg.inputs['Strength'].default_value=.35;nt.links.new(sky.outputs['Color'],bg.inputs['Color']);nt.links.new(bg.outputs[0],wo.inputs[0]);S.world=world
# Actual emitting fixtures and area/point light sources complement physically traced indirect light.
for m in DATA['meshes']:
 if m['material']!='warmLight':continue
 p=m['position'].copy();name=m['name'];sz=m['scale']
 if 'subacuática' in name:
  p[0]-=.07;light('LED | '+name,p,25,(.45,.72,1),.13,[p[0]-1,p[1],p[2]])
 elif 'baliza' in name:light('LED | '+name,p,28,(1,.74,.45),.07,type='POINT')
 elif 'Aplique' in name:
  p[0]-=.16;light('LED | '+name,p,55,size=.12,target=[p[0],p[1]-1,p[2]])
 elif 'Vestidor' in name or 'vestidor' in name:light('LED | '+name,p,38,size=.5,target=[p[0],p[1]-1,p[2]])
 elif 'lineal' in name.lower() or 'alacena' in name.lower() or 'Lámpara' in name or 'colgante' in name or 'Luz' in name:
  p[1]-=.055;light('LED | '+name,p,110 if 'lineal' in name.lower() else 28,size=max(.15,min(max(sz),2)),target=[p[0],p[1]-1,p[2]])
light('Indirecta | monoambiente',[18.1,2.78,2.7],120,size=2,target=[18.1,.5,2.7])
light('Indirecta | baño suite',[20.55,5.72,7.40],95,size=.8,target=[20.5,3.5,7.4])
light('Indirecta | baño pileta',[21.3,2.48,10.94],60,size=.5,target=[21.3,.5,10.9])
light('Indirecta | baño mono',[20.6,2.48,5.1],60,size=.5,target=[20.6,.5,5.1])
# Cycles production setup.
S.render.engine='CYCLES';S.cycles.device='GPU'
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
for d in pref.devices:d.use=d.type=='OPTIX'
S.cycles.samples=128;S.cycles.use_denoising=True;S.cycles.adaptive_threshold=.035
S.cycles.max_bounces=12;S.cycles.diffuse_bounces=4;S.cycles.glossy_bounces=4;S.cycles.transmission_bounces=12;S.cycles.transparent_max_bounces=12
S.cycles.sample_clamp_indirect=5
S.render.resolution_x=2000;S.render.resolution_y=1500;S.render.resolution_percentage=100
S.render.image_settings.file_format='PNG';S.render.image_settings.color_mode='RGB';S.render.image_settings.color_depth='8'
S.render.fps=24;S.render.film_transparent=False;S.render.use_file_extension=True;S.render.use_persistent_data=True
S.view_settings.view_transform='AgX'
try:S.view_settings.look='AgX - Medium High Contrast'
except:pass
S.view_settings.exposure=.6
TOUR,ROUTE=setup_tour(globals())
S.camera=CAM['presentation'];S.frame_set(1)
# Named lighting variants share model data without duplicating geometry.
for name,elev,strength,exposure in [('DÍA',38,.55,.2),('NOCHE',-7,.012,1.0)]:
 variant=bpy.data.scenes.new('CASA DE CAMPO | '+name)
 for c in COL.values():variant.collection.children.link(c)
 variant.world=world.copy();variant.world.name='Cielo físico | '+name
 sk=next(n for n in variant.world.node_tree.nodes if n.bl_idname=='ShaderNodeTexSky');sk.sun_elevation=math.radians(elev)
 next(n for n in variant.world.node_tree.nodes if n.bl_idname=='ShaderNodeBackground').inputs['Strength'].default_value=strength
 variant.camera=CAM['presentation'];variant.render.engine='CYCLES';variant.cycles.device='GPU';variant.cycles.samples=128;variant.cycles.use_denoising=True
 variant.render.resolution_x=2000;variant.render.resolution_y=1500;variant.view_settings.view_transform='AgX';variant.view_settings.exposure=exposure
 variant.unit_settings.system='METRIC'
# Reference is embedded in the blend for traceability.
bpy.data.images.load(os.path.join(ROOT,'source','reference_0.png')).pack()
readme=bpy.data.texts.new('LEEME | Source, units, doors, tour')
readme.write('CASA DE CAMPO\\nHTML coordinates (X,Y,Z) -> Blender (X,-Z,Y). Metres.\\nSource mesh names and IDs are retained. Frame 1 closed; frames 160+ tour doors open.\\nThe camera TOUR has a baked smooth equivalent rig and an editable Bezier route. Set scene.camera to TOUR to render animation.\\nThe presentation camera has vertical correction; all CAM source cameras are kept verbatim.\\nThe source image is packed. Procedural PBR maps generated by the original HTML are packed.\\nCorrections:\\n'+'\\n'.join(corrections))
S['source_file']='casa_campo_estudio_interactivo_mejorado_v3.html';S['axis_conversion']='(X,Y,Z) => (X,-Z,Y)';S['corrections']=json.dumps(corrections,ensure_ascii=False)
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':
  area.spaces.active.region_3d.view_perspective='CAMERA'
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Casa_de_Campo.blend'))
from validate_scene import validate
report=validate(globals())
json.dump(report,open(os.path.join(OUT,'validation.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
print('SAVED',len(S.objects), 'objects',len(bpy.data.materials),'materials',flush=True)
if '--preview' in sys.argv:
 S.render.resolution_x=1200;S.render.resolution_y=900;S.cycles.samples=32;S.cycles.adaptive_threshold=.07
 S.render.filepath=os.path.join(OUT,'preview.png');bpy.ops.render.render(write_still=True)
print('DONE',flush=True)
