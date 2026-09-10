import bpy,bmesh,os,json,math,random,numpy as np
from mathutils import Vector,Matrix
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'output');S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
D=json.load(open(os.path.join(ROOT,'source','scene.json'),encoding='utf8'));M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};rng=np.random.default_rng(5908)
def cv(p):return Vector((p[0],-p[2],p[1]))
def box(name,p,size,mat='blackMetal',col='INTERIORS',bevel=.003):
 x,y,z=[v/2 for v in size];vs=[cv([a*x,b*y,c*z]) for a,b,c in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
 f=[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)];me=bpy.data.meshes.new(name);me.from_pydata(vs,[],f);me.materials.append(M[mat]);o=bpy.data.objects.new(name,me);o.location=cv(p);bpy.data.collections[col].objects.link(o)
 if bevel:md=o.modifiers.new('Canto suave','BEVEL');md.width=bevel;md.segments=3
 return o
def cylinder(name,a,b,r,mat='stainless',col='INTERIORS'):
 A,B=cv(a),cv(b);t=(B-A).normalized();axis=Vector((1,0,0)) if abs(t.z)>.9 else Vector((0,0,1));u=t.cross(axis).normalized();v=t.cross(u);N=24
 vs=[p+r*(u*math.cos(j*math.tau/N)+v*math.sin(j*math.tau/N)) for p in [A,B] for j in range(N)];f=[tuple(range(N-1,-1,-1)),tuple(range(N,N*2))]
 for j in range(N):k=(j+1)%N;f.append((j,k,N+k,N+j))
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],f);me.materials.append(M[mat])
 for q in me.polygons:q.use_smooth=True
 o=bpy.data.objects.new(name,me);bpy.data.collections[col].objects.link(o);return o
def cut(o,c):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;md=o.modifiers.new('Rebaje coordinado','BOOLEAN');md.operation='DIFFERENCE';md.object=c;bpy.ops.object.modifier_apply(modifier=md.name)
# Source late-patch shower finish was intersecting the bathtub. Place finishes against the real wall.
tile=bpy.data.objects['Revestimiento ducha suite'];tile.location.y=-6.135;tile.location.x=21.23
tile['construction_note']='Wall finish corrected from source Z6.80 inside bathtub to Z6.135 at real bathroom front wall. Bath location retained.'
niche=bpy.data.objects['Nicho ducha suite'];bpy.data.objects.remove(niche,do_unlink=True)
cutter=box('Temporal hueco nicho',[21.30,4.85,6.095],[.18,.42,.20],col='REFERENCE',bevel=0)
for ob in [tile,bpy.data.objects['División estudio vivienda']]:cut(ob,cutter)
bpy.data.objects.remove(cutter,do_unlink=True)
box('Nicho ducha | fondo',[21.30,4.85,6.018],[.16,.40,.012],'tile')
for x,z,w,h in [(21.205,4.85,.015,.42),(21.395,4.85,.015,.42),(21.30,4.63,.20,.015),(21.30,5.07,.20,.015)]:box('Nicho ducha | cerco',[x,z,6.07],[w,h,.12],'tile')
glass=bpy.data.objects['Mampara ducha suite'];glass.location=cv([20.444,4.575,6.82]);glass.dimensions=(.012,.70,1.55)
glass['construction_note']='Shower screen sits beside the bathtub rim, outside ceramic; +3.80..5.35, clear of basin.'
bpy.data.objects['Bañera vivienda'].location.z+=.04
drain=bpy.data.objects['Rejilla ducha suite'];drain.location=cv([21.02,3.338,6.60]);drain.dimensions=(.12,.04,.008)
cylinder('Ducha | montante mural',[21.35,4.02,6.23],[21.35,5.40,6.23],.012)
cylinder('Ducha | brazo',[21.35,5.40,6.23],[21.35,5.40,6.78],.012)
cylinder('Ducha | rociador',[21.35,5.37,6.78],[21.35,5.405,6.78],.11)
cylinder('Bañera | caño de llenado',[21.10,4.03,6.20],[21.10,4.03,6.58],.014)
cylinder('Bañera | boca',[21.10,4.03,6.58],[21.10,3.98,6.58],.014)
for x in [21.17,21.53]:cylinder('Ducha | mando',[x,4.05,6.20],[x,4.05,6.25],.026)
# Recognisable toilet seats and compact cisterns add missing sanitary detailing.
def seat(name,x,z,w,d,h):
 N=64;vs=[];f=[]
 for y,ratio in [(h,1),(h+.025,1),(h+.025,.75),(h,.75)]:
  for j in range(N):
   a=j*math.tau/N;vs.append(cv([x+math.cos(a)*w*.49*ratio,y,z+math.sin(a)*d*.49*ratio]))
 for k in range(3):
  for j in range(N):q=(j+1)%N;f.append((k*N+j,k*N+q,(k+1)*N+q,(k+1)*N+j))
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],f);me.materials.append(M['ceramic'])
 for p in me.polygons:p.use_smooth=True
 o=bpy.data.objects.new(name,me);bpy.data.collections['INTERIORS'].objects.link(o)
for label,x,z,w,d,h in [('suite',20.94,8.13,.45,.66,3.83),('mono',21.18,5.42,.42,.62,.705),('quincho',21.53,10.80,.42,.62,.705)]:
 seat('Inodoro '+label+' | asiento',x,z,w,d,h)
 tank=box('Inodoro '+label+' | mochila compacta',[x,h+.16,z+d*.42],[w*.85,.34,.13],'ceramic',bevel=.04)
 cylinder('Inodoro '+label+' | pulsador',[x,h+.332,z+d*.42],[x,h+.344,z+d*.42],.020)
# Tone and physical scale of materials: retain the source PBR maps while moderating variations.
for key in ['wood','woodDark','stainless','fabric','clothWhite','whitePlaster','concrete','concreteDark','ceramic']:
 m=M[key];n=m.node_tree.nodes;l=m.node_tree.links;bs=next(v for v in n if v.type=='BSDF_PRINCIPLED')
 for b in [v for v in n if v.type=='BUMP']:
  b.inputs['Strength'].default_value=.20 if key!='stainless' else .10
  b.inputs['Distance'].default_value=min(b.inputs['Distance'].default_value,.001)
 if key in ['wood','woodDark']:
  link=bs.inputs['Base Color'].links[0];src=link.from_socket;l.remove(link);h=n.new('ShaderNodeHueSaturation');h.inputs['Saturation'].default_value=.73;h.inputs['Value'].default_value=.90;l.new(src,h.inputs['Color']);l.new(h.outputs['Color'],bs.inputs['Base Color'])
 if key=='stainless':
  for inp in ['Base Color','Roughness']:
   for link in list(bs.inputs[inp].links):l.remove(link)
  bs.inputs['Base Color'].default_value=(.56,.59,.61,1);bs.inputs['Roughness'].default_value=.25;bs.inputs['Anisotropic'].default_value=.64
 if key=='clothWhite':
  for link in list(bs.inputs['Base Color'].links):l.remove(link)
  bs.inputs['Base Color'].default_value=(.60,.565,.495,1);bs.inputs['Sheen Weight'].default_value=.3
 if key=='whitePlaster':
  for link in list(bs.inputs['Base Color'].links):l.remove(link)
  bs.inputs['Base Color'].default_value=(.63,.60,.535,1)
# Ground cover with broad, restrained botanical variation; no tiled dark bands.
for key in ['grass','outerGrass']:
 m=M[key];n=m.node_tree.nodes;l=m.node_tree.links;bs=next(v for v in n if v.type=='BSDF_PRINCIPLED')
 for link in list(bs.inputs['Base Color'].links):l.remove(link)
 tc=n.new('ShaderNodeTexCoord');tc.object=bpy.data.objects['Material coordinates | metres / world'];noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=.7;noise.inputs['Detail'].default_value=3;l.new(tc.outputs['Object'],noise.inputs['Vector'])
 ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.025,.047,.013,1);ramp.color_ramp.elements[1].color=(.066,.094,.028,1);l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.88
# Fine curved leaves, with per-leaf variation; retain original tree positions and canopy centres.
leafmat=bpy.data.materials.new('Follaje | hoja fina translúcida');leafmat.use_nodes=True;n=leafmat.node_tree.nodes;l=leafmat.node_tree.links;bs=next(v for v in n if v.type=='BSDF_PRINCIPLED');out=next(v for v in n if v.type=='OUTPUT_MATERIAL')
attr=n.new('ShaderNodeVertexColor');attr.layer_name='leaf_tint';l.new(attr.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.58;bs.inputs['Sheen Weight'].default_value=.12
tr=n.new('ShaderNodeBsdfTranslucent');l.new(attr.outputs['Color'],tr.inputs[0]);mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=.28;l.new(bs.outputs[0],mix.inputs[1]);l.new(tr.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0])
for tree in range(1,7):
 obj=bpy.data.objects['Árbol lote %d hojas'%tree];src=next(m for m in D['meshes'] if m['name']==obj.name);nv=len(D['geometries'][src['geometry']]['positions'])//3;old=obj.data
 p=np.empty(len(old.vertices)*3,np.float32);old.vertices.foreach_get('co',p);p=p.reshape(-1,nv,3);centers=p.mean(axis=1)[:,None,:];old.calc_loop_triangles();idx=np.array([t.vertices for t in old.loop_triangles])
 vs=[];fs=[];colors=[]
 for j in range(4):
  pp=centers+(p-centers)*rng.uniform(.30,.46,(len(p),1,1))+rng.normal(0,.07,(len(p),1,3))
  pp[:,:,2]+=np.sin(np.linspace(0,math.pi,nv))[None,:]*.018
  vs.append(pp.reshape(-1,3));fs.append(idx+j*len(old.vertices))
  t=rng.uniform(.75,1.35,len(p));c=np.column_stack((.035*t,.085*t,.014*t,np.ones(len(p))));colors.append(np.repeat(c,nv,axis=0))
 pp=np.concatenate(vs);ii=np.concatenate(fs);me=bpy.data.meshes.new(obj.name+' | hoja fina editable');me.vertices.add(len(pp));me.vertices.foreach_set('co',pp.reshape(-1));me.loops.add(ii.size);me.loops.foreach_set('vertex_index',ii.reshape(-1));me.polygons.add(len(ii));me.polygons.foreach_set('loop_start',np.arange(len(ii))*3);me.polygons.foreach_set('loop_total',np.full(len(ii),3));me.polygons.foreach_set('use_smooth',np.ones(len(ii),bool));me.update();me.materials.append(leafmat)
 co=me.color_attributes.new(name='leaf_tint',type='FLOAT_COLOR',domain='POINT');co.data.foreach_set('color',np.concatenate(colors).astype(np.float32).reshape(-1));obj.data=me
# Replace repeated outside assemblies with editable collection instances; remove floating mulch discs.
for o in list(S.objects):
 if o.name.startswith('Arboleda exterior'):bpy.data.objects.remove(o,do_unlink=True)
prototypes={}
roots={2:[4.3,0,16.8],3:[8.2,0,13.55],5:[9.2,0,4.4]}
for number in [2,3,5]:
 c=bpy.data.collections.new('BOTÁNICA | árbol tipo %d'%number)
 for src in [o for o in S.objects if o.name.startswith('Árbol lote %d '%number) and 'alcorque' not in o.name]:
  du=src.copy();du.data=src.data;c.objects.link(du)
 prototypes[number]=c
poses=[(-10+i*3.1,38+rng.uniform(0,4)) for i in range(16)]+[(29+rng.uniform(0,4),-3+i*4) for i in range(10)]+[(-12+rng.uniform(-3,0),-5+i*5) for i in range(8)]+[(-12+i*3.8,-25-rng.uniform(0,6)) for i in range(17)]+[(-10+i*5,-39-rng.uniform(0,7)) for i in range(13)]
for i,(x,z) in enumerate(poses):
 number=[2,3,5][i%3];f=float(rng.uniform(1.65,3.15));rz=float(rng.uniform(0,math.tau));root=cv(roots[number])
 ob=bpy.data.objects.new('Paisaje | árbol exterior %02d'%i,None);ob.instance_type='COLLECTION';ob.instance_collection=prototypes[number];bpy.data.collections['LANDSCAPE'].objects.link(ob)
 ob.matrix_world=Matrix.Translation(cv([float(x),-.045,float(z)]))@Matrix.Rotation(rz,4,'Z')@Matrix.Diagonal((f*.95,f,f*float(rng.uniform(.85,1.2)),1))@Matrix.Translation(-root)
# Soft distant landform only beyond the source property and street context.
old=bpy.data.objects.get('Entorno | terreno continuo')
if old:bpy.data.objects.remove(old,do_unlink=True)
vs=[];fs=[];N=65
for iy in range(N):
 for ix in range(N):
  x=-300+ix*600/(N-1);y=-300+iy*600/(N-1);dist=max(abs(x-11)-20,abs(y+10)-25,0);amp=min(1,dist/55)
  h=-.16+amp*(1.25*math.sin(x*.018+y*.021)+.65*math.sin(x*.035-y*.016))
  vs.append((x,y,h))
for iy in range(N-1):
 for ix in range(N-1):a=iy*N+ix;fs.append((a,a+1,a+N+1,a+N))
me=bpy.data.meshes.new('Terreno lejano | ondulación suave');me.from_pydata(vs,[],fs);me.materials.append(M['outerGrass']);ob=bpy.data.objects.new('Entorno | terreno continuo',me);bpy.data.collections['LANDSCAPE'].objects.link(ob)
# A clear physical sunset sky; retain the packed photographic environment as an optional world.
previous=S.world.copy();previous.name='OPCIÓN | HDRI Belfast Sunset'
world=bpy.data.worlds.new('Atardecer | cielo físico limpio');world.use_nodes=True;n=world.node_tree.nodes;l=world.node_tree.links;n.clear()
out=n.new('ShaderNodeOutputWorld');bg=n.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.22;sky=n.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(11);sky.sun_rotation=math.radians(130);sky.sun_disc=False;sky.air_density=1;sky.aerosol_density=.8;sky.ozone_density=1
l.new(sky.outputs['Color'],bg.inputs['Color']);l.new(bg.outputs[0],out.inputs[0]);S.world=world;bpy.data.scenes['RECORRIDO | Continuo'].world=world
sun=bpy.data.objects['Sol | Atardecer cálido'];sun.data.energy=2.2;sun.data.color=(1,.78,.53);sun.data.angle=math.radians(1.15)
# Less uneven practical light and the new lower dwelling ceiling.
for o in S.objects:
 if o.type=='LIGHT' and o.name.startswith('LED |'):
  if any(w in o.name.lower() for w in ['cocina','alacena','vivienda']):o.data.energy*=.62
  o.data.color=(1,.81,.61)
light=bpy.data.objects.get('Luz lineal vivienda')
if light:light.location.z=5.68
led=bpy.data.objects.get('LED | Luz lineal vivienda')
if led:led.location.z=5.64;led.data.energy=75
S.view_settings.exposure=.1
S['review_iteration']='1 / pass3 materials landscape light'
notes=json.loads(S['corrections']);notes+=['Iteration1 pass3: corrected source shower lining onto actual wall, recessed niche, rim-mounted shower screen, taps/shower and toilet detailing. Bath floor base reconciled by40mm while preserving plan footprint.','Iteration1 pass3: finer leaves preserve source tree centres; outside grove uses varied collection instances with no mulch discs. Grass colour no longer repeats source dark tile bands. Distant terrain/trees fill horizon beyond source site.','Iteration1 pass3: source steel albedo streaks replaced with restrained brushed finish; wood saturation and bump moderated. Physical clear sunset sky and balanced practical lamps; original packed HDRI preserved as optional world.']
S['corrections']=json.dumps(notes,ensure_ascii=False);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];S.frame_set(1)
bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Casa_de_Campo_Revision.blend'),compress=True)
print('PASS3_SAVED',len(S.objects),flush=True)
# Review stills only. User explicitly paused video rendering.
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='OPTIX';p.get_devices()
for d in p.devices:d.use=d.type=='OPTIX'
S.cycles.device='GPU';S.cycles.samples=64;S.cycles.denoiser='OPTIX';S.cycles.denoising_use_gpu=True;S.render.use_persistent_data=True;S.render.resolution_x=1400;S.render.resolution_y=1050;S.render.resolution_percentage=100;S.render.filepath=os.path.join(ROOT,'review','iter1_exterior.png');bpy.ops.render.render(write_still=True)
S.render.resolution_x=1200;S.render.resolution_y=800
for name,label in [('REV | Dormitorio completo','dormitorio'),('REV | Baño completo','bano'),('REV | Baño desde acceso','bano_acceso'),('REV | Cocina comedor','cocina'),('REV | Quincho y extracción','quincho'),('REV | Estudio y cubierta','estudio'),('REV | Vestidor circulación','vestidor'),('REV | Cubierta escalonada','cubierta'),('REV | Portón y riel','porton'),('REV | Escalera y desembarco','escalera')]:
 c=bpy.data.objects[name];S.camera=c;S.frame_set(c['presentation_frame']);S.render.filepath=os.path.join(ROOT,'review','iter1_'+label+'.png');bpy.ops.render.render(write_still=True)
print('PASS3_REVIEW_STILLS_READY',flush=True)
