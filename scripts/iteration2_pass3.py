import bpy,os,json,math,random,numpy as np
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1)
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};rng=random.Random(21609)
anchor=bpy.data.objects['Material coordinates | metres / world']
# Fine nonperiodic oak pores, measured in metres. Separate board joints for floors.
def oak(key,axis,floor=False):
 mat=bpy.data.materials.new(('Roble aceitado | ' if key=='wood' else 'Nogal mate | ')+str(axis)+(' parquet' if floor else ' veta'));mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;n.clear()
 out=n.new('ShaderNodeOutputMaterial');bs=n.new('ShaderNodeBsdfPrincipled');l.new(bs.outputs[0],out.inputs[0]);bs.inputs['Roughness'].default_value=.43;bs.inputs['Coat Weight'].default_value=.13;bs.inputs['Coat Roughness'].default_value=.38
 tc=n.new('ShaderNodeTexCoord');tc.object=anchor
 mul=n.new('ShaderNodeVectorMath');mul.operation='MULTIPLY';scale=[105,105,105];scale[axis]=1.6;mul.inputs[1].default_value=scale;l.new(tc.outputs['Object'],mul.inputs[0])
 ns=n.new('ShaderNodeTexNoise');ns.inputs['Scale'].default_value=1;ns.inputs['Detail'].default_value=2.3;ns.inputs['Roughness'].default_value=.6;l.new(mul.outputs[0],ns.inputs[0])
 ramp=n.new('ShaderNodeValToRGB');a,b=((.245,.131,.058,1),(.345,.217,.116,1)) if key=='wood' else ((.090,.046,.021,1),(.145,.080,.040,1));ramp.color_ramp.elements[0].color=a;ramp.color_ramp.elements[1].color=b;l.new(ns.outputs['Fac'],ramp.inputs[0]);col=ramp.outputs[0]
 obj=n.new('ShaderNodeObjectInfo');rand=n.new('ShaderNodeMapRange');rand.inputs['To Min'].default_value=.87;rand.inputs['To Max'].default_value=1.08;l.new(obj.outputs['Random'],rand.inputs[0])
 mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;l.new(col,mix.inputs[1]);l.new(rand.outputs[0],mix.inputs[2]);col=mix.outputs[0]
 if floor:
  brick=n.new('ShaderNodeTexBrick');l.new(tc.outputs['Object'],brick.inputs['Vector']);brick.inputs['Scale'].default_value=1;brick.inputs['Mortar Size'].default_value=.0015;brick.inputs['Mortar Smooth'].default_value=.001;brick.inputs['Brick Width'].default_value=1.40;brick.inputs['Row Height'].default_value=.18;brick.offset=.5;brick.offset_frequency=2
  brick.inputs['Color1'].default_value=(.76,.70,.61,1);brick.inputs['Color2'].default_value=(.99,.97,.92,1);brick.inputs['Mortar'].default_value=(.19,.13,.08,1)
  blend=n.new('ShaderNodeMixRGB');blend.blend_type='MULTIPLY';blend.inputs[0].default_value=1;l.new(col,blend.inputs[1]);l.new(brick.outputs['Color'],blend.inputs[2]);col=blend.outputs[0]
 l.new(col,bs.inputs['Base Color'])
 bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.15;bump.inputs['Distance'].default_value=.00020;l.new(ns.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],bs.inputs['Normal'])
 mat['construction_material']='Fine longitudinal grain; no repeating wave albedo; oiled oak/walnut';return mat
woods={(key,axis,floor):oak(key,axis,floor) for key in ['wood','woodDark'] for axis in range(3) for floor in [False,True]}
for o in list(bpy.data.objects):
 if o.type!='MESH' or any(k in o.name.lower() for k in ['árbol','rama','tronco','hojas','huerta','alcorque']):continue
 for slot in o.material_slots:
  key=slot.material.get('source_material_key') if slot.material else None
  if key in ['wood','woodDark']:
   floor='piso' in o.name.lower();dims=o.dimensions;axis=0 if floor else (2 if dims.z>.6 and dims.z>min(dims.x,dims.y)*1.5 else int(np.argmax(dims)))
   slot.link='OBJECT';slot.material=woods[key,axis,floor]
# Tapered, gently irregular trunks and branches, retaining original axes and canopy anchors.
bark=bpy.data.materials.new('Corteza | fisura fina gris parda');bark.use_nodes=True;n=bark.node_tree.nodes;l=bark.node_tree.links;bs=n.get('Principled BSDF');bs.inputs['Roughness'].default_value=.91
tc=n.new('ShaderNodeTexCoord');mul=n.new('ShaderNodeVectorMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=(18,18,2);l.new(tc.outputs['Object'],mul.inputs[0]);noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=4;noise.inputs['Detail'].default_value=3;l.new(mul.outputs[0],noise.inputs[0]);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.027,.025,.019,1);ramp.color_ramp.elements[1].color=(.105,.090,.069,1);l.new(noise.outputs[0],ramp.inputs[0]);l.new(ramp.outputs[0],bs.inputs['Base Color']);bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.0025;bump.inputs['Strength'].default_value=.45;l.new(noise.outputs[0],bump.inputs['Height']);l.new(bump.outputs[0],bs.inputs['Normal'])
done=set()
for o in list(bpy.data.objects):
 if o.type!='MESH' or not o.name.startswith('Árbol lote') or not any(w in o.name for w in ['tronco','rama']):continue
 old=o.data
 if old.name in done:continue
 done.add(old.name);p=np.array([v.co for v in old.vertices]);lo=p.min(0);hi=p.max(0);cen=(lo+hi)/2;radius=max(hi[0]-lo[0],hi[1]-lo[1])/2;height=hi[2]-lo[2];vs=[];fs=[];trunk='tronco' in o.name;phase=rng.uniform(0,math.tau);N=14;K=10
 for k in range(K):
  t=k/(K-1);rr=radius*((1.22-.68*t)+(.36*math.exp(-t*18) if trunk else 0))
  dx=radius*.45*math.sin(t*math.pi)*math.sin(phase+t*5);dy=radius*.45*math.sin(t*math.pi)*math.cos(phase+t*4)
  for j in range(N):
   a=j*math.tau/N;rad=rr*(1+.075*math.sin(a*5+phase+t*2));vs.append((cen[0]+dx+rad*math.cos(a),cen[1]+dy+rad*math.sin(a),lo[2]+height*t))
 for k in range(K-1):
  for j in range(N):q=(j+1)%N;fs.append((k*N+j,k*N+q,(k+1)*N+q,(k+1)*N+j))
 fs.extend([tuple(range(N-1,-1,-1)),tuple(range((K-1)*N,K*N))]);me=bpy.data.meshes.new(old.name+' | fuste ahusado');me.from_pydata(vs,[],fs);me.materials.append(bark)
 for f in me.polygons:f.use_smooth=True
 for du in list(bpy.data.objects):
  if du.type=='MESH' and du.data==old:du.data=me
# Fine rough ground, plus discrete grass tufts with varied length; property footprints stay unchanged.
for key in ['grass','outerGrass']:
 m=M[key];n=m.node_tree.nodes;l=m.node_tree.links;bs=next(v for v in n if v.type=='BSDF_PRINCIPLED')
 for link in list(bs.inputs['Normal'].links):l.remove(link)
 tc=n.new('ShaderNodeTexCoord');tc.object=anchor;ns=n.new('ShaderNodeTexNoise');ns.inputs['Scale'].default_value=95;ns.inputs['Detail'].default_value=2;l.new(tc.outputs['Object'],ns.inputs[0]);bp=n.new('ShaderNodeBump');bp.inputs['Strength'].default_value=.28;bp.inputs['Distance'].default_value=.007;l.new(ns.outputs[0],bp.inputs['Height']);l.new(bp.outputs[0],bs.inputs['Normal'])
grassmat=bpy.data.materials.new('Pradera | briznas naturales');grassmat.use_nodes=True;n=grassmat.node_tree.nodes;l=grassmat.node_tree.links;bs=n.get('Principled BSDF');bs.inputs['Roughness'].default_value=.87
at=n.new('ShaderNodeVertexColor');at.layer_name='tint';l.new(at.outputs[0],bs.inputs['Base Color'])
vs=[];fs=[];cs=[]
for i in range(9500):
 x=rng.uniform(-18,37);z=rng.uniform(-7,35)
 inside=0<x<22 and 0<z<20
 if inside:
  if x>10.8 or z<1.2 or (x<3.5 and z>12):continue
  h=rng.uniform(.035,.075);ground=0.015
 else:h=rng.uniform(.10,.25);ground=-.145
 # Keep the street, entry strip and paved surroundings clean.
 if -3<z<0 or (10.6<x<14.3 and z<12.5):continue
 col=(rng.uniform(.035,.085),rng.uniform(.065,.115),rng.uniform(.012,.035),1)
 for j in range(3):
  a=rng.uniform(0,math.tau);w=rng.uniform(.006,.014);lean=rng.uniform(.01,.055);n0=len(vs)
  vs.extend([(x-w*math.cos(a),-z-w*math.sin(a),ground),(x+w*math.cos(a),-z+w*math.sin(a),ground),(x+lean*math.sin(a),-z+lean*math.cos(a),ground+h)])
  fs.append((n0,n0+1,n0+2));cs.extend([col]*3)
me=bpy.data.meshes.new('Pradera | malla editable de briznas');me.from_pydata(vs,[],fs);me.materials.append(grassmat);attr=me.color_attributes.new(name='tint',type='FLOAT_COLOR',domain='POINT');attr.data.foreach_set('color',np.array(cs,dtype=np.float32).reshape(-1));ob=bpy.data.objects.new('Paisaje | pradera de transición',me);bpy.data.collections['LANDSCAPE'].objects.link(ob)
# Disturb repeated background rows in depth and width without moving the source six trees.
for ob in S.objects:
 if ob.name.startswith('Paisaje | árbol exterior'):
  ob.location.x+=rng.uniform(-1.8,1.8);ob.location.y+=rng.uniform(-2.5,2.5)
S['review_iteration']='2 / pass3 fine materials and botanical detail';S['video_render_requires_explicit_approval']=True
notes=json.loads(S['corrections']);notes.append('Iteration2 pass3: longitudinal fine-grain oak/walnut with individual object variation and180mm parquet joints; tapered bark branches, meadow tufts and irregular outer grove. Original six tree centres retained.');S['corrections']=json.dumps(notes,ensure_ascii=False)
S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];S.frame_set(1);bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_Revision.blend'),compress=True)
print('PASS2_3_SAVED_NO_VIDEO',flush=True)
