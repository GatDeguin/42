import bpy,os,json,math,hashlib,numpy as np
from mathutils import Vector,Matrix
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;OUT=os.path.join(ROOT,'docs','assets');os.makedirs(OUT,exist_ok=True)
C=Matrix(((1,0,0,0),(0,0,1,0),(0,-1,0,0),(0,0,0,1)))
def pose(o):
 p,q,s=(C@o.matrix_local@C.inverted()).decompose();return {'position':list(p),'quaternion':list(q)[1:]+[q.w],'scale':list(s)}
rigs=[o for o in S.objects if o.name.startswith('DOOR | ')]
doors=[]
for o in rigs:
 S.frame_set(1);bpy.context.view_layer.update();a=pose(o)
 S.frame_set(150);bpy.context.view_layer.update();b=pose(o)
 doors.append({'name':o.name,'key':o.name.split(' | ')[1],'motion':o.get('motion'),'closed':a,'open':b})
S.frame_set(1);bpy.context.view_layer.update()
cameras=[]
for o in S.objects:
 if o.type=='CAMERA' and o.name.startswith(('CAM | ','REV | ')):
  p=C@o.matrix_world.translation;direction=o.matrix_world.to_quaternion()@Vector((0,0,-1));t=p+(C.to_3x3()@direction)*4
  cameras.append({'name':o.name,'position':list(p),'target':list(t),'fov':math.degrees(2*math.atan(36/(2*o.data.lens)))})
# Build an export-only material adaptation. Never save these changes to the audited .blend.
cache={}
def material(old):
 if old.name in cache:return cache[old.name]
 key=old.get('source_material_key','');m=bpy.data.materials.new('WEB | '+old.name);m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF');src=next((n for n in old.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None) if old.use_nodes else None
 color=tuple(src.inputs['Base Color'].default_value) if src else tuple(old.diffuse_color)
 rough=float(src.inputs['Roughness'].default_value) if src else .65;metal=float(src.inputs['Metallic'].default_value) if src else 0
 if old.name.startswith('Roble'):color=(.34,.20,.10,1)
 elif old.name.startswith('Nogal'):color=(.13,.068,.030,1)
 elif old.name.startswith('Corteza'):color=(.10,.078,.046,1)
 elif 'Follaje' in old.name or key in ['leaf','blade']:color=(.085,.19,.04,1)
 elif key in ['grass','outerGrass']:color=(.09,.145,.055,1)
 elif key=='roof':color=(.06,.069,.079,1)
 elif key=='whitePlaster':color=(.68,.64,.57,1)
 elif key=='blackMetal':color=(.028,.032,.034,1)
 elif key in ['glass','glassInner']:color=(.72,.86,.89,.20);metal=.1;rough=.13
 elif key=='water':color=(.035,.30,.39,.63);metal=.15;rough=.16
 bs.inputs['Base Color'].default_value=color;bs.inputs['Roughness'].default_value=max(.15,rough);bs.inputs['Metallic'].default_value=metal
 bs.inputs['Alpha'].default_value=color[3]
 if color[3]<1:m.surface_render_method='DITHERED';m.use_backface_culling=True
 if key in ['warmLight','embers'] or old.name.startswith('meter'):
  bs.inputs['Emission Color'].default_value=color;bs.inputs['Emission Strength'].default_value=.6
 if key in ['brick','brickDark','concrete','concreteDark','tile','poolTile','paving','cement','soil','acoustic']:
  image=next((n.image for n in old.node_tree.nodes if n.type=='TEX_IMAGE' and n.image and 'albedo' in n.image.name),None)
  if image:
   tex=m.node_tree.nodes.new('ShaderNodeTexImage');tex.image=image;m.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color'])
 cache[old.name]=m;return m
selected=[];stats={'source_model':'Casa_de_Campo_Final.blend','source_sha256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),'geometry':'Architecture retained; landscape tessellation reduced for browser; materials adapted for real-time PBR.','objects':0,'vertices_before':0,'vertices_after':0}
bpy.ops.object.select_all(action='DESELECT')
for o in list(S.objects):
 if o.type not in ['MESH','EMPTY'] or o.hide_render:continue
 if o.type=='EMPTY':
  if not o.name.startswith('DOOR | '):continue
 else:
  if any(c.name in ['REFERENCE'] for c in o.users_collection):continue
  if any(w in o.name for w in ['Entorno | terreno continuo','Paisaje | pradera de transición']):continue
  stats['vertices_before']+=len(o.data.vertices)
  o.data=o.data.copy()
  # Give mapped masonry and floors world-scaled box UVs, with independent seams per face.
  if not o.data.uv_layers:o.data.uv_layers.new(name='WebUV')
  uv=o.data.uv_layers.active.data
  for poly in o.data.polygons:
   normal=o.matrix_world.to_3x3()@poly.normal;axis=max(range(3),key=lambda i:abs(normal[i]));axes=[i for i in range(3) if i!=axis]
   for li in poly.loop_indices:
    w=o.matrix_world@o.data.vertices[o.data.loops[li].vertex_index].co;uv[li].uv=(w[axes[0]]*.70,w[axes[1]]*.70)
  mats=[slot.material for slot in o.material_slots]
  for i,old in enumerate(mats):
   if old:o.material_slots[i].link='DATA';o.material_slots[i].material=material(old)
  if o.name.startswith('Árbol lote') and 'hojas' in o.name:
   md=o.modifiers.new('Web foliage LOD','DECIMATE');md.ratio=.16
   bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=md.name)
  elif len(o.data.vertices)>50000 and any(c.name=='LANDSCAPE' for c in o.users_collection):
   md=o.modifiers.new('Web grass LOD','DECIMATE');md.ratio=.20;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=md.name)
  stats['vertices_after']+=len(o.data.vertices)
 # Only compact user-facing metadata; original source parameters remain in .blend.
 label=o.name;collection=next((c.name for c in o.users_collection if c.name in ['ROOF','CONSTRUCTION','VENTILATION','STUDIO','STAIR','POOL','LANDSCAPE','GROUND_FLOOR','UPPER_FLOOR','QUINCHO','INTERIORS','SITE','DOORS']), 'OTHER')
 for k in list(o.keys()):del o[k]
 o['label']=label;o['category']=collection
 if o.type=='MESH':
  heights=[(o.matrix_world@Vector(p)).z for p in o.bound_box];o['minHeight']=min(heights);o['maxHeight']=max(heights)
  o['roofPart']=collection=='ROOF' or (min(heights)>5.7 and collection in ['CONSTRUCTION','STUDIO','INTERIORS'])
 if o in rigs:o['doorKey']=label.split(' | ')[1]
 o.select_set(True);selected.append(o)
stats['objects']=len(selected)
os.makedirs(os.path.join(ROOT,'web-tools','.cache'),exist_ok=True)
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT,'web-tools','.cache','house-raw.glb'),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_animations=False,export_cameras=False,export_lights=False,export_extras=True,export_materials='EXPORT',export_image_format='AUTO',export_texcoords=True,export_normals=True)
json.dump({'doors':doors,'cameras':cameras,'stats':stats,'heights':{'studio':3.2,'dwelling':2.6},'video':'paused'},open(os.path.join(OUT,'model-info.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
print('WEB_EXPORT_COMPLETE',json.dumps(stats),flush=True)
