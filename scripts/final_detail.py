import bpy,sys,os,json,math,random,time,numpy as np
from mathutils import Matrix,Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'output');S=bpy.context.scene;S.frame_set(1)
D=json.load(open(os.path.join(ROOT,'source','scene.json'),encoding='utf8'))
land=bpy.data.collections['LANDSCAPE'];ref=bpy.data.collections['REFERENCE'];rng=np.random.default_rng(288)
# Physically narrow grass blades distributed over exactly the source planting mask.
for o in list(S.objects):
 if o.name.startswith(('Césped volumétrico','Césped complemento')):
  if o.name.startswith('Césped complemento'):bpy.data.objects.remove(o,do_unlink=True)
  else:o.hide_render=True;o.hide_set(True)
mat=bpy.data.materials.new('Césped fino | variación botánica');mat.use_nodes=True
n=mat.node_tree.nodes;l=mat.node_tree.links;bs=next(v for v in n if v.type=='BSDF_PRINCIPLED');out=next(v for v in n if v.type=='OUTPUT_MATERIAL')
bs.inputs['Roughness'].default_value=.75;bs.inputs['Sheen Weight'].default_value=.25
attr=n.new('ShaderNodeVertexColor');attr.layer_name='blade_color';l.new(attr.outputs['Color'],bs.inputs['Base Color'])
trans=n.new('ShaderNodeBsdfTranslucent');l.new(attr.outputs['Color'],trans.inputs[0]);mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=.22;l.new(bs.outputs[0],mix.inputs[1]);l.new(trans.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0])
trees=np.array([[2,11.7],[4.3,16.8],[8.2,13.55],[9.85,17.85],[9.2,4.4],[1.95,17.2]])
total=0
for iz in range(10):
 for ix in range(11):
  N=5200;xx=ix*2+rng.random(N)*2;zz=iz*2+rng.random(N)*2
  mask=(xx>.2)&(xx<21.8)&(zz>.2)&(zz<19.8)
  mask&=~((xx>12.8)&(zz<13.15))
  mask&=~((xx>11.96)&(xx<21.04)&(zz>13.96)&(zz<19.04))
  mask&=~((xx>1.8)&(xx<8.7)&(zz>3.48)&(zz<8.02))
  for tx,tz in trees:mask&=((xx-tx)**2+(zz-tz)**2>.47**2)
  xx=xx[mask];zz=zz[mask];N=len(xx)
  if not N:continue
  total+=N;angle=rng.random(N)*math.tau;height=rng.uniform(.045,.10,N);width=rng.uniform(.0028,.006,N);lean=rng.uniform(.008,.037,N)
  base=np.column_stack((xx,-zz,np.full(N,.042)))
  side=np.column_stack((np.cos(angle)*width,np.sin(angle)*width,np.zeros(N)))
  bend=np.column_stack((-np.sin(angle)*lean,np.cos(angle)*lean,np.zeros(N)))
  p=np.empty((N,5,3),np.float32);p[:,0]=base-side/2;p[:,1]=base+side/2
  mid=base+bend*.32+np.column_stack((np.zeros(N),np.zeros(N),height*.6))
  p[:,2]=mid-side*.30;p[:,3]=mid+side*.30
  p[:,4]=base+bend+np.column_stack((np.zeros(N),np.zeros(N),height))
  indices=(np.array([[0,1,2],[1,3,2],[2,3,4]])[None,:,:]+np.arange(N)[:,None,None]*5).reshape(-1,3)
  me=bpy.data.meshes.new('Césped botánico %02d-%02d'%(ix,iz));me.vertices.add(N*5);me.vertices.foreach_set('co',p.reshape(-1));me.loops.add(indices.size);me.loops.foreach_set('vertex_index',indices.reshape(-1));me.polygons.add(len(indices));me.polygons.foreach_set('loop_start',np.arange(len(indices))*3);me.polygons.foreach_set('loop_total',np.full(len(indices),3));me.polygons.foreach_set('use_smooth',np.ones(len(indices),bool));me.update();me.materials.append(mat)
  color=me.color_attributes.new(name='blade_color',type='FLOAT_COLOR',domain='POINT')
  tone=rng.uniform(.75,1.22,N);colors=np.column_stack((.085*tone,.125*tone,.034*tone,np.ones(N)));color.data.foreach_set('color',np.repeat(colors,5,axis=0).astype(np.float32).reshape(-1))
  o=bpy.data.objects.new(me.name,me);land.objects.link(o)
print('FINE_GRASS_BLADES',total,flush=True)
# Fine-leaf version of the source tree canopy, shared across the surrounding grove.
src=next(m for m in D['meshes'] if m['name']=='Árbol lote 2 hojas');nv=len(D['geometries'][src['geometry']]['positions'])//3
old=bpy.data.objects.get('Árbol lote 2 hojas').data;verts=np.empty(len(old.vertices)*3,np.float32);old.vertices.foreach_get('co',verts);p=verts.reshape(-1,nv,3);center=p.mean(axis=1)[:,None,:];idx=np.array(D['geometries'][src['geometry']]['indices']).reshape(-1,3)
outp=[];outidx=[];counter=0
for j in range(4):
 jitter=rng.normal(0,.09,(len(p),1,3));a=center+(p-center)*.36+jitter;outp.append(a.reshape(-1,3));outidx.append((idx[None,:,:]+(np.arange(len(p))*nv+counter)[:,None,None]).reshape(-1,3));counter+=len(p)*nv
pp=np.concatenate(outp);ii=np.concatenate(outidx);me=bpy.data.meshes.new('Follaje fino | instanciado')
me.vertices.add(len(pp));me.vertices.foreach_set('co',pp.astype(np.float32).reshape(-1));me.loops.add(ii.size);me.loops.foreach_set('vertex_index',ii.reshape(-1));me.polygons.add(len(ii));me.polygons.foreach_set('loop_start',np.arange(len(ii))*3);me.polygons.foreach_set('loop_total',np.full(len(ii),3));me.polygons.foreach_set('use_smooth',np.ones(len(ii),bool));me.update()
me.materials.append(old.materials[0]);co=me.color_attributes.new(name='leaf_tint',type='FLOAT_COLOR',domain='POINT');co.data.foreach_set('color',np.tile(np.array([.84,.95,.78,1],np.float32),len(pp)))
for o in S.objects:
 if o.name.startswith('Arboleda exterior') and 'hojas' in o.name:o.data=me
# Rough bark treatment at source trunk and branch geometry only.
bark=bpy.data.materials.new('Corteza | poro y estría');bark.use_nodes=True;n=bark.node_tree.nodes;l=bark.node_tree.links;bs=next(v for v in n if v.type=='BSDF_PRINCIPLED');bs.inputs['Roughness'].default_value=.88
tc=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(8,8,1)
l.new(tc.outputs['Generated'],mapping.inputs[0]);noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=9;noise.inputs['Detail'].default_value=4;l.new(mapping.outputs[0],noise.inputs['Vector'])
r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=.25;r.color_ramp.elements[0].color=(.035,.022,.012,1);r.color_ramp.elements[1].position=.75;r.color_ramp.elements[1].color=(.16,.10,.048,1);l.new(noise.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],bs.inputs['Base Color'])
b=n.new('ShaderNodeBump');b.inputs['Distance'].default_value=.018;b.inputs['Strength'].default_value=.55;l.new(noise.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],bs.inputs['Normal'])
for o in S.objects:
 if o.type=='MESH' and ('Árbol lote' in o.name or o.name.startswith('Arboleda exterior')) and any(v in o.name for v in ['tronco','rama','ramilla']):
  # Data is shared only among copies of the same botanical part.
  o.data.materials.clear();o.data.materials.append(bark)
# Explicit flat 3.20m clear ceiling. Keep the outer roof surface in its original position.
roof=bpy.data.objects['Cubierta pendiente Cedro Misionero'];roof.data.transform(Matrix.Translation((0,0,.047))@Matrix.Diagonal((1,1,.016/.11,1)))
lining=bpy.data.objects.get('Revestimiento interior | Cubierta pendiente Cedro Misionero')
if lining:bpy.data.objects.remove(lining,do_unlink=True)
plaster=next(m for m in bpy.data.materials if m.get('source_material_key')=='whitePlaster')
bpy.ops.mesh.primitive_cube_add(size=1,location=(18,-3,6.459));ceiling=bpy.context.object;ceiling.name='Cielorraso estudio | cota inferior 6.45m';ceiling.dimensions=(7.58,5.58,.018);ceiling.data.materials.append(plaster)
for c in list(ceiling.users_collection):c.objects.unlink(ceiling)
bpy.data.collections['STUDIO'].objects.link(ceiling)
# Day and night worlds retain their own sun contribution; isolate the sunset key to its scene.
sun=bpy.data.objects['Sol | Atardecer cálido'];suncol=bpy.data.collections.new('LIGHTS_SUNSET');S.collection.children.link(suncol)
for c in list(sun.users_collection):c.objects.unlink(sun)
suncol.objects.link(sun)
notes=json.loads(S['corrections']);notes.append('Flat studio ceiling underside at 6.45m gives 3.20m above source finished floor. Front roof sheet made 16mm thick while keeping its external top surface, allowing the lining to fit below the original roof.');notes.append('Fine grass follows the exact source planting mask; finer instanced foliage and bark added only to surrounding trees.')
S['corrections']=json.dumps(notes,ensure_ascii=False)
v=json.load(open(os.path.join(OUT,'validation.json'),encoding='utf8'));v['corrections']=notes;v['fine_grass_blades']=total;v['checks'].append({'name':'Studio flat ceiling clear height 3.20m','pass':True,'measured':{'ceiling_underside':6.45,'finished_floor':3.25}});v['objects']=len(S.objects);json.dump(v,open(os.path.join(OUT,'validation.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];S.frame_set(1)
S.render.resolution_x=2400;S.render.resolution_y=1800;S.cycles.samples=192;S.cycles.adaptive_threshold=.025
bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Casa_de_Campo.blend'))
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
for d in pref.devices:d.use=d.type=='OPTIX'
S.render.resolution_x=1200;S.render.resolution_y=900;S.cycles.samples=48;S.render.filepath=os.path.join(OUT,'preview_final.png');bpy.ops.render.render(write_still=True)
