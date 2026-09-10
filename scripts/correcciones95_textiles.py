"""R4B: supported furnishings, textiles, light housings and restrained real-scale finishes."""
import bpy,os,math,json,ast,numpy as np
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
for m in bpy.data.materials:
 if m.name.startswith('MAT95 | '):M[m.name.split(' | ',1)[1]]=m
def cv(p):return Vector((p[0],-p[2],p[1]))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_materialidad.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['box','cyl','curve','mesh']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<fast>','exec'))
def bounds(o):
 bpy.context.view_layer.update()
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get())
 a=np.array([e.matrix_world@Vector(v) for v in e.bound_box]);return a.min(0),a.max(0)
def deform(o,fn):
 if o.type!='MESH':return
 bpy.context.view_layer.update();o.data=o.data.copy();inv=o.matrix_world.inverted()
 for v in o.data.vertices:v.co=inv@fn(o.matrix_world@v.co)
 o.data.update()
def map_h(o,lo,hi):
 a,b=bounds(o)
 deform(o,lambda p:Vector((p.x,p.y,lo+(p.z-a[2])*(hi-lo)/(b[2]-a[2]))))
def erase(names):
 for o in list(S.objects):
  if o.name.startswith(tuple(names)):bpy.data.objects.remove(o,do_unlink=True)
# Fix independent re-open findings using evaluated world bounds after every move.
for side in ['izq','der']:map_h(bpy.data.objects['Mesa de luz suite '+side],3.50,3.78)
head=bpy.data.objects['Cabezal dormitorio'];a,b=bounds(head)
deform(head,lambda p:Vector((p.x,-6.135+(p.y-(a[1]+b[1])/2)*.07/(b[1]-a[1]),p.z)))
# Counter has a real40mm top, with cabinet tops touching its underside.
map_h(bpy.data.objects['Mesada apoyo quincho'],1.04,1.08)
# Balcony is an uninterrupted1m circulation; preserve removed alternatives separately.
for o in S.objects:
 if o.name.startswith(('Mesa balcón ','Silla balcón ')):
  o.hide_render=True;o.hide_set(True);o['layout_revision']='Inactive alternative: conflicts with circulation on1m balcony. No occupied furniture in operative plan.'
# Ground-floor island and stools use finished-floor datum, not model origin.
o=bpy.data.objects.get('Isla cocina mono base')
if o:map_h(o,.21,1.07)
for name in ['Isla cocina mono tapa','Voladizo isla mono']:
 o=bpy.data.objects.get(name)
 if o:map_h(o,1.07,1.11)
o=bpy.data.objects.get('Canto mesada isla mono')
if o:map_h(o,1.095,1.11)
for o in [v for v in S.objects if v.name.startswith('Taburete isla mono')]:map_h(o,.21,.86)
# Studio seated workstation: lower the complete working assembly223mm; maintain supports.
prefix=('Consola estudio','Base consola estudio','Pantalla estudio','Medidor consola','Controlador estudio','Monitor izquierdo','Monitor derecho')
for o in S.objects:
 if o.name.startswith(prefix) or (o.name.startswith('MAT95 | ') and any(c.name=='STUDIO' for c in o.users_collection)):
  o.location.z-=.223
for name in ['Soporte monitor izquierdo','Soporte monitor derecho']:
 o=bpy.data.objects.get(name)
 if o:
  a,b=bounds(o);map_h(o,3.30,b[2]-.223)
o=bpy.data.objects.get('Base consola estudio')
if o:
 a,b=bounds(o);map_h(o,3.25,b[2])
erase(['Pata consola estudio','Travesaño consola estudio'])
desk=bpy.data.objects['Consola estudio'];e=desk.evaluated_get(bpy.context.evaluated_depsgraph_get());me=e.to_mesh()
tree=BVHTree.FromPolygons([e.matrix_world@v.co for v in me.vertices],[list(p.vertices) for p in me.polygons]);e.to_mesh_clear()
a,b=bounds(desk)
for x in [a[0]+.13,b[0]-.13]:
 for z in [-b[1]+.18,-a[1]-.18]:
  hit=tree.ray_cast(cv([x,3.31,z]),Vector((0,0,1)),1.2)[0]
  if hit:
   top=hit.z
   box('MOB95 | apoyo consola',[x,(3.25+top)/2,z],[.045,top-3.25,.045],'blackMetal','STUDIO',.002)
# Display has a floor stand behind the screen, not a suspended rectangle.
box('MOB95 | base soporte pantalla',[17.43,3.267,3],[.30,.034,.40],'blackMetal','STUDIO',.007)
cyl('MOB95 | columna soporte pantalla',[17.43,3.284,3],[17.43,4.52,3],.018,'blackMetal','STUDIO')
cyl('MOB95 | brazo VESA pantalla',[17.43,4.49,3],[17.495,4.49,3],.014,'blackMetal','STUDIO')
# Oiled timber grain follows each manufactured member. Reuse retained source-derived shaders.
woods={}
for m in bpy.data.materials:
 if m.name.startswith(('Roble aceitado | ','Nogal mate | ')) and 'parquet' not in m.name:
  parts=m.name.split(' | ',1)[1].split();axis=int(parts[0]);woods[('wood' if m.name.startswith('Roble') else 'woodDark',axis)]=m
for o in S.objects:
 if o.type!='MESH' or o.hide_render:continue
 for slot in o.material_slots:
  key=slot.material.get('source_material_key') if slot.material else None
  if key in ['wood','woodDark']:
   ax=int(np.argmax([o.dimensions.x,o.dimensions.y,o.dimensions.z]))
   if (key,ax) in woods:slot.link='OBJECT';slot.material=woods[key,ax]
# Smooth paint / cement use millimetric finish, not large high-contrast cloud textures.
def mineral(key,base,rough,amplitude,scale):
 m=M[key];n=m.node_tree.nodes;l=m.node_tree.links;n.clear()
 out=n.new('ShaderNodeOutputMaterial');bs=n.new('ShaderNodeBsdfPrincipled');l.new(bs.outputs[0],out.inputs['Surface']);bs.inputs['Roughness'].default_value=rough
 tc=n.new('ShaderNodeTexCoord');tc.object=bpy.data.objects['Material coordinates | metres / world']
 broad=n.new('ShaderNodeTexNoise');broad.inputs['Scale'].default_value=3.2;broad.inputs['Detail'].default_value=2.4;l.new(tc.outputs['Object'],broad.inputs['Vector'])
 ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=tuple(v*.98 for v in base)+(1,);ramp.color_ramp.elements[1].color=tuple(v*1.02 for v in base)+(1,);l.new(broad.outputs['Fac'],ramp.inputs['Fac']);l.new(ramp.outputs['Color'],bs.inputs['Base Color'])
 grain=n.new('ShaderNodeTexNoise');grain.inputs['Scale'].default_value=scale;grain.inputs['Detail'].default_value=2;l.new(tc.outputs['Object'],grain.inputs['Vector'])
 bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=amplitude;bump.inputs['Strength'].default_value=.22;l.new(grain.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],bs.inputs['Normal'])
 m['finish_scale_m']=1/scale;m['albedo_variation_percent']=2
mineral('whitePlaster',(.65,.625,.565),.79,.00020,350)
mineral('cement',(.34,.335,.315),.61,.00035,190)
# Sewn, thin curtains with full-height folds, exact original plan footprint and actual support.
erase(['Cortina suite '])
for i,(z0,z1) in enumerate([(6.72,7.24),(7.86,8.38)],1):
 vs=[];fs=[];NX,NY=100,100
 for j in range(NY+1):
  t=j/NY;h=5.69-(5.69-3.30)*t
  for k in range(NX+1):
   u=k/NX;z=z0+(z1-z0)*u
   phase=math.tau*(u*5.8)+.10*math.sin(t*3.2)+.045*math.sin(u*13+t*7)
   x=14.24+.034*math.sin(phase)+.003*math.sin(phase*2+t*2)
   h2=h+.004*t**4*math.sin(u*29+i)
   vs.append(cv([x,h2,z]))
 for j in range(NY):
  for k in range(NX):
   q=j*(NX+1)+k;fs.append((q,q+1,q+NX+2,q+NX+1))
 ob=mesh('Cortina suite %d | lino plisado'%i,vs,fs,'linen95','INTERIORS')
 for p in ob.data.polygons:p.use_smooth=True
 mod=ob.modifiers.new('Tejido0.7mm','SOLIDIFY');mod.thickness=.0007
 # Hem and hanging tabs follow the actual folded surface.
 for h,t in [(3.315,1),(5.675,0)]:
  pts=[]
  for k in range(61):
   u=k/60;phase=math.tau*u*5.8+.10*math.sin(t*3.2)+.045*math.sin(u*13+t*7)
   pts.append([14.24+.034*math.sin(phase)+.003*math.sin(phase*2+t*2),h,z0+(z1-z0)*u])
  curve('MOB95 | dobladillo cortina',pts,.0011,'linen95','INTERIORS')
 for k in range(7):
  z=z0+(z1-z0)*k/6;box('MOB95 | carro cortina',[14.24,5.704,z],[.009,.020,.012],'stainless','INTERIORS',.001)
box('MOB95 | riel cortina dormitorio',[14.24,5.723,7.55],[.022,.018,1.87],'blackMetal','INTERIORS',.002)
for z in [6.69,7.55,8.41]:
 box('MOB95 | soporte riel cortina',[14.20,5.748,z],[.10,.055,.025],'blackMetal','INTERIORS',.002)
# Pillow top and bottom are sewn patches with pinched edges and local tension wrinkles.
erase(['Cama dormitorio almohada ','Cama dormitorio ribete almohada '])
for i,cx in enumerate([15.384,16.256],1):
 vs=[];fs=[];N,K=64,40;cz=6.64
 for side in [1,-1]:
  for j in range(K+1):
   v=-1+2*j/K
   for k in range(N+1):
    u=-1+2*k/N;rounding=1-.045*abs(v)**8
    x=cx+.37*u*rounding;z=cz+.225*v*(1-.045*abs(u)**8)
    fullness=max(0,(1-u*u)*(1-v*v))**.43
    edge=(abs(u)**8+abs(v)**8)
    wrinkle=.005*math.sin(30*u+8*v+i)*math.exp(-((abs(v)-.75)/.21)**2)*max(0,1-u*u)
    h=3.895+side*(.061*fullness+.003)+wrinkle*(1 if side>0 else .3)
    vs.append(cv([x,h,z]))
 grid=(N+1)*(K+1)
 for si in [0,1]:
  for j in range(K):
   for k in range(N):
    a=si*grid+j*(N+1)+k;f=(a,a+1,a+N+2,a+N+1);fs.append(f if si==0 else tuple(reversed(f)))
 edge=list(range(N+1))+[j*(N+1)+N for j in range(1,K+1)]+[K*(N+1)+k for k in range(N-1,-1,-1)]+[j*(N+1) for j in range(K-1,0,-1)]
 for a,b in zip(edge,edge[1:]+edge[:1]):fs.append((a,b,grid+b,grid+a))
 ob=mesh('Cama dormitorio almohada %d'%i,vs,fs,'cotton95','INTERIORS')
 for p in ob.data.polygons:p.use_smooth=True
 pts=[[vs[a].x,3.895,-vs[a].y] for a in edge[::4]];pts.append(pts[0]);curve('MOB95 | costura funda almohada',pts,.0010,'cotton95','INTERIORS')
# Opaque luminaire enclosures with inset opal diffuser maintain the existing finished clear heights.
for o in list(S.objects):
 if o.type!='MESH' or 'lineal' not in o.name.lower() or 'carcasa' in o.name.lower():continue
 if not any(m and m.get('source_material_key')=='warmLight' for m in o.data.materials):continue
 a,b=bounds(o)
 if b[2]-a[2]>.10:continue
 o.data=o.data.copy();o.data.materials.clear();o.data.materials.append(M['blackMetal'])
 cx,cy,cz=(a+b)/2
 box('MOB95 | difusor opal '+o.name,[cx,a[2]+.001,-cy],[max(.01,b[0]-a[0]-.009),.002,max(.01,b[1]-a[1]-.009)],'warmLight','LIGHTS',.0005)
# Reframe bedroom to read the side window, aligned headboard and access rather than a frontal close-up.
for name,p,t,lens in [('REV | Dormitorio completo',[17.19,4.85,8.49],[15.78,4.25,6.66],24),('REV | Dormitorio acceso',[17.35,4.85,7.65],[15.38,4.18,6.95],23)]:
 o=bpy.data.objects[name];o.location=cv(p);o.rotation_euler=(cv(t)-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=lens;o.data.dof.use_dof=False
S['review_iteration']='95 / R4B real-scale finishes and support corrections';S['video_render_requires_explicit_approval']=True
S['furnishing_changes_r4b']=json.dumps({'bedside_real_bounds':[3.5,3.78],'headboard_thickness_m':.07,'balcony':'Continuous circulation; inactive bistro alternatives','studio_workstation_lowered_m':.223,'island_top':1.11,'island_floor':.21,'island_seat':.86,'curtain_fullness_geometry':'100x100 fold grid and actual rail'},ensure_ascii=False)
bpy.context.view_layer.update();S.frame_set(1);bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_95_R4B.blend'),compress=True)
print('R4B_MATERIAL_AND_SUPPORT_SAVED',flush=True)
