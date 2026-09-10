"""Pass2: manufactured equipment, cloth and botanical structure. No video rendering."""
import bpy,bmesh,os,json,math,ast,random,re,numpy as np
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
for nd in ast.parse(open(os.path.join(ROOT,'scripts','iteration1_pass1.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['cv','put','box','cyl','bounds']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
# Direct datablock constructors avoid rebuilding the entire scene for every small control.
def box(name,p,size,mat='blackMetal',col='CONSTRUCTION',bev=.002):
 x,y,z=size[0]/2,size[2]/2,size[1]/2
 vs=[(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)]
 fs=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(M[mat]);me.update();o=bpy.data.objects.new(name,me);o.location=cv(p);COL[col].objects.link(o)
 if bev:md=o.modifiers.new('Arista fabricada','BEVEL');md.width=bev;md.segments=2
 return o
def cyl(name,a,b,r,mat='blackMetal',col='CONSTRUCTION'):
 a,b=cv(a),cv(b);t=(b-a).normalized();u=t.cross(Vector((1,0,0)) if abs(t.x)<.9 else Vector((0,1,0))).normalized();v=t.cross(u);mid=(a+b)/2;N=24;vs=[]
 for p in [a,b]:
  vs.extend([p-mid+r*(u*math.cos(k*math.tau/N)+v*math.sin(k*math.tau/N)) for k in range(N)])
 fs=[tuple(range(N-1,-1,-1)),tuple(range(N,2*N))]
 for k in range(N):q=(k+1)%N;fs.append((k,q,N+q,N+k))
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(M[mat]);me.update();o=bpy.data.objects.new(name,me);o.location=mid;COL[col].objects.link(o)
 for p in me.polygons:p.use_smooth=len(p.vertices)==4
 return o

R=random.Random(9542)
def material(key,color,rough=.5,metal=0):
 m=bpy.data.materials.new('MAT95 | '+key);m.use_nodes=True;bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal;m.diffuse_color=(*color,1);M[key]=m;return m
def mesh(name,vs,fs,mat,col='INTERIORS'):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(M[mat]);me.update()
 o=bpy.data.objects.new(name,me);COL[col].objects.link(o);return o
def curve(name,points,r,mat,col='STUDIO'):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=12;cu.bevel_depth=r;cu.bevel_resolution=3
 sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
 for b,p in zip(sp.bezier_points,points):b.co=cv(p);b.handle_left_type='AUTO';b.handle_right_type='AUTO'
 cu.materials.append(M[mat]);o=bpy.data.objects.new(name,cu);COL[col].objects.link(o);return o
def label(name,text,p,size=.012):
 cu=bpy.data.curves.new(name,'FONT');cu.body=text;cu.size=size;cu.align_x='CENTER';cu.align_y='CENTER';cu.extrude=.00005
 cu.materials.append(M['print']);o=bpy.data.objects.new(name,cu);COL['STUDIO'].objects.link(o);o.location=cv(p);o.rotation_euler[2]=math.pi/2;return o
material('print',(.57,.62,.63),.62)
material('consolePlate',(.018,.023,.026),.34,.6)
material('rubber95',(.012,.014,.016),.76)
material('silver95',(.38,.40,.42),.29,.95)
material('linen95',(.68,.63,.53),.88)
material('cotton95',(.78,.73,.63),.83)
material('leaf95',(.032,.075,.017),.68)
# Woven fibres at submillimetre scale, independent of object bounds.
for key in ['linen95','cotton95']:
 m=M[key];n=m.node_tree.nodes;l=m.node_tree.links;bs=next(q for q in n if q.type=='BSDF_PRINCIPLED');bs.inputs['Sheen Weight'].default_value=.3
 tc=n.new('ShaderNodeTexCoord');wa=n.new('ShaderNodeTexWave');wa.wave_type='BANDS';wa.bands_direction='X';wa.inputs['Scale'].default_value=1150;wa.inputs['Distortion'].default_value=1.6
 wb=n.new('ShaderNodeTexWave');wb.wave_type='BANDS';wb.bands_direction='Y';wb.inputs['Scale'].default_value=1450
 for w in [wa,wb]:l.new(tc.outputs['Object'],w.inputs['Vector'])
 mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';l.new(wa.outputs['Color'],mul.inputs[0]);l.new(wb.outputs['Color'],mul.inputs[1])
 b=n.new('ShaderNodeBump');b.inputs['Distance'].default_value=.00032;b.inputs['Strength'].default_value=.27;l.new(mul.outputs[0],b.inputs['Height']);l.new(b.outputs[0],bs.inputs['Normal'])
# Retain console enclosure dimensions. Replace oversized floating controls by 32 mounted channels.
for o in list(S.objects):
 if o.name.startswith(('Fader consola ','Carril fader ','Perilla consola ')):bpy.data.objects.remove(o,do_unlink=True)
desk=bpy.data.objects['Consola estudio'];dep=bpy.context.evaluated_depsgraph_get();ed=desk.evaluated_get(dep);me=ed.to_mesh()
bv=BVHTree.FromPolygons([ed.matrix_world@v.co for v in me.vertices],[list(f.vertices) for f in me.polygons]);ed.to_mesh_clear()
def top(x,z):
 hit=bv.ray_cast(cv([x,5,z]),Vector((0,0,-1)),2)[0];return hit.z if hit else 4.20
def cbox(name,x,z,sx,sz,h,mat='consolePlate',extra=.003):
 return box('MAT95 | '+name,[x,top(x,z)+extra+h/2,z],[sx,h,sz],mat,'STUDIO',min(.001,h*.2))
for i in range(32):
 if i%8==0:print('CONSOLE_CHANNEL',i,flush=True)
 z=1.62+i*.088
 central=2.4<z<3.6
 cbox('tira canal %02d'%(i+1),17.96 if central else 18.18,z,.38 if central else .91,.082,.003)
 # 100mm fader; aluminium cap 18x26mm, channel pitch88mm.
 if not central:
  cbox('ranura fader %02d'%i,18.44,z,.10,.003,.002,'rubber95',.007)
  x=18.40+R.random()*.075;cbox('capuchón fader %02d'%i,x,z,.018,.026,.012,'silver95',.009)
  for k in range(7):cbox('escala canal',18.39+k*.016,z+.015,.001,.006,.0005,'print',.008)
 for j in range(5):
  x=17.83+j*.086;y=top(x,z)+.009
  cyl('MAT95 | encoder canal %02d %02d'%(i,j),[x,y,z],[x,y+.018,z],.009,'rubber95','STUDIO')
  box('MAT95 | índice encoder',[x+.003,y+.0185,z],[.004,.001,.0015],'print','STUDIO',0)
 if not central:
  for j in range(2):cbox('tecla canal',18.27+j*.041,z,.022,.019,.006,'rubber95',.008)
  cbox('etiqueta OLED canal',18.20,z,.031,.055,.002,'screen',.008)
 for j in range(7):
  col='meterGreen' if j<5 else 'meterAmber'
  if col not in M:M[col]=bpy.data.materials.get(col)
  cbox('segmento vúmetro',17.745+j*.005,z,.0025,.018,.001,col,.008)
 xx=17.78 if central else 18.535;label('MAT95 | número canal',str(i+1),[xx,top(xx,z)+.010,z],.010)
# Keys, pads and sockets refine the original1.08m MIDI-controller footprint.
material('keyWhite95',(.74,.73,.68),.28)
for i in range(36):
 z=2.568+i*.024
 box('MAT95 | tecla natural %02d'%i,[18.79,4.272,z],[.20,.009,.0225],'keyWhite95','STUDIO',.001)
 if i<35 and i%7 in [0,1,3,4,5]:
  box('MAT95 | tecla sostenido %02d'%i,[18.744,4.282,z+.012],[.11,.014,.013],'rubber95','STUDIO',.001)
for i in range(8):
 for j in range(2):box('MAT95 | pad MIDI',[18.30+j*.075,4.274,2.58+i*.058],[.047,.010,.047],'rubber95','STUDIO',.003)
box('MAT95 | pantalla controlador',[18.34,4.271,3.24],[.16,.004,.20],'screen','STUDIO',.001)
for z in [3.12,3.20,3.28,3.36]:
 cyl('MAT95 | encoder maestro',[18.52,4.27,z],[18.52,4.293,z],.012,'rubber95','STUDIO')
# Panel fasteners and wood cheeks are supported by the original enclosure.
for z in [1.47,4.55]:
 for x in [17.77,18.12,18.57]:
  y=top(x,z)+.004;cyl('MAT95 | tornillo panel',[x,y,z],[x,y+.002,z],.003,'silver95','STUDIO')
for z in [1.38,4.62]:cbox('lateral madera consola',18.18,z,1.03,.05,.025,'wood',.0) if 'wood' in M else None
# Four cables dressed below the console, out of all circulation paths.
for i,z in enumerate([1.80,2.82,3.10,4.20]):
 curve('MAT95 | cable balanceado %d'%i,[[17.50,4.45,z],[17.55,4.2,z],[17.76,3.67,z],[18.04,3.62,z],[18.12,3.92,z]],.003,'rubber95')
# Loudspeaker roll-surrounds and cone dishes: mechanical detail within source cabinets.
for old in list(S.objects):
 if old.name.startswith(('Woofer estudio ','Tweeter estudio ')):bpy.data.objects.remove(old,do_unlink=True)
for z in [1.78,4.22]:
 for h,r in [(4.56,.103),(4.82,.046)]:
  vs=[];fs=[];profile=[(r,17.598),(r*.91,17.612),(r*.78,17.604),(r*.33,17.586),(0,17.608)];N=48
  for rr,x in profile:
   vs.extend([cv([x,h+rr*math.cos(k*math.tau/N),z+rr*math.sin(k*math.tau/N)]) for k in range(N)])
  for j in range(len(profile)-1):
   for k in range(N):q=(k+1)%N;fs.append((j*N+k,j*N+q,(j+1)*N+q,(j+1)*N+k))
  o=mesh('MAT95 | suspensión y cono monitor',vs,fs,'rubber95','STUDIO')
  for p in o.data.polygons:p.use_smooth=True
# Replace regular blanket wave with draped cloth and localized, asymmetric tension creases.
old=bpy.data.objects.get('Cama dormitorio manta')
if old:bpy.data.objects.remove(old,do_unlink=True)
vs=[];fs=[];nx,nz=100,80
creases=[(15.13,7.38,.33,.011),(16.46,7.35,-.48,.012),(15.55,8.20,.76,.008),(16.24,7.90,-.87,.006)]
for j in range(nz+1):
 z=7.26+(8.579-7.26)*j/nz
 for i in range(nx+1):
  x=14.779+(16.68-14.779)*i/nx
  left=max(0,(14.97-x)/.191);foot=max(0,(z-8.35)/.229)
  h=3.865-.37*max(left**1.45,foot**1.5)
  h+=.008*math.sin(4.9*x+2.2*z)*math.sin(3.6*z-1.4*x)
  for cx,cz,a,amp in creases:
   dx=x-cx;dz=z-cz;along=dx*math.cos(a)+dz*math.sin(a);across=-dx*math.sin(a)+dz*math.cos(a)
   h+=amp*math.exp(-(across/.024)**2-(along/.32)**2)
  vs.append(cv([x,h,z]))
for j in range(nz):
 for i in range(nx):
  a=j*(nx+1)+i;fs.append((a,a+1,a+nx+2,a+nx+1))
cloth=mesh('Cama dormitorio manta',vs,fs,'linen95')
md=cloth.modifiers.new('Tejido con espesor2mm','SOLIDIFY');md.thickness=.002
for p in cloth.data.polygons:p.use_smooth=True
# Pillow envelopes with pinched sewn perimeter and irregular folds.
for i in [1,2]:
 ob=bpy.data.objects['Cama dormitorio almohada '+str(i)];a,b=bounds(ob);cx=(a[0]+b[0])/2;cz=-(a[1]+b[1])/2;w=b[0]-a[0];d=b[1]-a[1]
 bpy.data.objects.remove(ob,do_unlink=True);vs=[];fs=[];N,K=64,18
 for j in range(K+1):
  lat=-math.pi/2+math.pi*j/K;sl=math.sin(lat);cl=max(0,math.cos(lat))
  for k in range(N):
   ang=k*math.tau/N;ux=math.copysign(abs(math.cos(ang))**.40,math.cos(ang));uz=math.copysign(abs(math.sin(ang))**.40,math.sin(ang))
   px=cx+w*.5*ux*cl**.32;pz=cz+d*.5*uz*cl**.32
   edge=max(0,1-abs(sl)*5);wrinkle=.003*edge*math.sin(ang*17+i*.7)*(math.sin(ang*3.1)**2)
   h=3.934+.075*sl+wrinkle
   vs.append(cv([px,h,pz]))
 for j in range(K):
  for k in range(N):q=(k+1)%N;fs.append((j*N+k,j*N+q,(j+1)*N+q,(j+1)*N+k))
 ob=mesh('Cama dormitorio almohada '+str(i),vs,fs,'cotton95')
 for p in ob.data.polygons:p.use_smooth=True
# Add soft microfinish to exposed cabinetry instead of uniform specular planes.
for m in bpy.data.materials:
 if m.use_nodes and ('Roble' in m.name or 'Nogal' in m.name):
  bs=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
  if bs:bs.inputs['Coat Weight'].default_value=.08;bs.inputs['Coat Roughness'].default_value=.34
# Botanical assets: branch hierarchy supports coherent clusters of individually folded leaves.
bark=next(m for m in bpy.data.materials if m.name.startswith('Corteza'))
M['bark95']=bark
lm=M['leaf95'];nodes=lm.node_tree.nodes;links=lm.node_tree.links;bs=next(q for q in nodes if q.type=='BSDF_PRINCIPLED');bs.inputs['Subsurface Weight'].default_value=.06
attr=nodes.new('ShaderNodeVertexColor');attr.layer_name='botanical_tint';links.new(attr.outputs['Color'],bs.inputs['Base Color'])
trans=nodes.new('ShaderNodeBsdfTranslucent');links.new(attr.outputs['Color'],trans.inputs[0]);mix=nodes.new('ShaderNodeMixShader');mix.inputs[0].default_value=.18;links.new(bs.outputs[0],mix.inputs[1]);links.new(trans.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],next(q for q in nodes if q.type=='OUTPUT_MATERIAL').inputs['Surface'])
def botanical(seed):
 rng=random.Random(seed);branches=[];tips=[]
 root=Vector((0,0,0));fork=Vector((.08,-.035,1.52));branches.append((root,fork,.15,.068))
 for k in range(9):
  ang=k*math.tau/9+rng.uniform(-.19,.19);end=Vector((math.cos(ang)*rng.uniform(.75,1.25),math.sin(ang)*rng.uniform(.75,1.25),rng.uniform(2.35,3.32)))
  start=fork+Vector((0,0,rng.uniform(-.20,.15)));branches.append((start,end,.045,.022))
  for j in range(5):
   a=ang+rng.uniform(-.85,.85);tip=end+Vector((math.cos(a)*rng.uniform(.24,.58),math.sin(a)*rng.uniform(.24,.58),rng.uniform(.10,.45)));branches.append((end,tip,.014,.0045));tips.append(tip)
 bv=[];bf=[]
 for a,b,r1,r2 in branches:
  t=(b-a).normalized();u=t.cross(Vector((1,0,0))).normalized();v=t.cross(u);off=len(bv);N=9
  for p,rad in [(a,r1),(b,r2)]:
   for k in range(N):bv.append(p+rad*(u*math.cos(k*math.tau/N)+v*math.sin(k*math.tau/N))*(1+.08*math.sin(k*2.3)))
  for k in range(N):q=(k+1)%N;bf.append((off+k,off+q,off+N+q,off+N+k))
 bme=bpy.data.meshes.new('MAT95 | rama especie %d'%seed);bme.from_pydata(bv,[],bf);bme.materials.append(bark);bme.update()
 lv=[];lf=[];colors=[]
 for tip in tips:
  for j in range(900):
   a=rng.random()*math.tau;t=rng.uniform(-1,1);rad=rng.random()**(1/3);pos=tip+Vector((math.cos(a)*math.sqrt(1-t*t)*.49,math.sin(a)*math.sqrt(1-t*t)*.43,t*.32))*rad
   angle=rng.random()*math.tau;length=rng.uniform(.06,.108);width=length*rng.uniform(.33,.54)
   u=Vector((math.cos(angle),math.sin(angle),rng.uniform(-.8,.8))).normalized();v=u.cross(Vector((0,0,1))).normalized();normal=u.cross(v)
   off=len(lv);lv.extend([pos-u*length*.5,pos-v*width*.5,pos+normal*.004,pos+v*width*.5,pos+u*length*.5])
   lf.extend([(off,off+1,off+2),(off,off+2,off+3),(off+1,off+4,off+2),(off+2,off+4,off+3)])
   tone=rng.uniform(.65,1.5);colors.extend([(.033*tone,.077*tone,.016*tone,1)]*5)
 lme=bpy.data.meshes.new('MAT95 | copa especie %d'%seed);lme.from_pydata(lv,[],lf);lme.materials.append(lm);lme.update()
 co=lme.color_attributes.new(name='botanical_tint',type='FLOAT_COLOR',domain='POINT');co.data.foreach_set('color',np.array(colors,dtype=np.float32).reshape(-1))
 for m in [bme,lme]:
  for f in m.polygons:f.use_smooth=True
 return bme,lme
variants=[botanical(95420+i) for i in range(5)]
# Six owner-source tree centres; environment group centres derived from original trunks.
poses=[(2,11.7,1.04),(4.3,16.8,1.17),(8.2,13.55,.98),(9.85,17.85,.88),(9.2,4.4,.80),(1.95,17.2,.98)]
# Existing distant trees are collection instances. Read their root transforms, not only scene meshes.
original_roots={2:[4.3,0,16.8],3:[8.2,0,13.55],5:[9.2,0,4.4]}
for ob in S.objects:
 if ob.instance_type=='COLLECTION' and ob.name.startswith('Paisaje | árbol exterior '):
  number=int(ob.instance_collection.name.rsplit(' ',1)[-1]);root=ob.matrix_world@cv(original_roots[number]);sc=ob.matrix_world.to_scale()
  poses.append((root.x,-root.y,sc.z*{2:1.17,3:.98,5:.80}[number]))
  ob.hide_render=True;ob.hide_set(True)
groups={}
for ob in S.objects:
 if ob.name.startswith('Arboleda exterior'):
  idx=ob.name.split(' | ')[0];groups.setdefault(idx,[]).append(ob)
for idx,group in sorted(groups.items()):
 trunks=[o for o in group if 'tronco' in o.name]
 if trunks:
  a,b=bounds(min(trunks,key=lambda o:bounds(o)[0][2]));poses.append(((a[0]+b[0])/2,-(a[1]+b[1])/2,R.uniform(1.70,2.25)))
for ob in S.objects:
 if ob.name.startswith(('Árbol lote ','Arboleda exterior ')):ob.hide_render=True;ob.hide_set(True)
for i,(x,z,scale) in enumerate(poses):
 bm,lm=variants[i%len(variants)];angle=R.uniform(-math.pi,math.pi);sx=scale*R.uniform(.92,1.04);sy=scale*R.uniform(.93,1.08)
 transform=Matrix.Translation(cv([x,.03,z]))@Matrix.Rotation(angle,4,'Z')@Matrix.Diagonal((sx,sy,scale,1))
 for label,me in [('ramas',bm),('hojas',lm)]:
  o=bpy.data.objects.new('MAT95 | árbol %02d %s'%(i,label),me);COL['LANDSCAPE'].objects.link(o);o.matrix_world=transform;o['vegetation_detail']='Branched crown; source planting centre preserved for trees0..5. Surroundings illustrative.'
# Source building coordinates are untouched in this pass.
S['review_iteration']='95 / pass2 manufactured detail, cloth and botanical crowns';S['video_render_requires_explicit_approval']=True
S['materiality95']=json.dumps({'encoder_channels':32,'faders':18,'midi_keys':61,'fader_travel_m':.100,'cap_m':[.018,.026],'tree_variants':5,'tree_count':len(poses),'leaves_per_crown':40500,'cloth_thickness_m':.002,'source_building_unchanged':True})
bpy.context.view_layer.update();S.frame_set(1);bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_95_Pass2.blend'),compress=True)
print('PASS2_SAVED_NO_VIDEO',S['materiality95'],flush=True)
