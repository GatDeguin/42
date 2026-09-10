"""R5C: hinge rebates, kitchen extraction continuity and finished furniture dimensions."""
import bpy,os,math,json,ast,numpy as np,sys
from mathutils import Vector,Matrix
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
for m in bpy.data.materials:
 if m.name.startswith('MAT95 | '):M[m.name.split(' | ',1)[1]]=m
def cv(p):return Vector((p[0],-p[2],p[1]))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_textiles.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['bounds','deform','map_h']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_materialidad.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['box','cyl','mesh','curve']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<fast>','exec'))
def bb(name,x,h,z,mat='blackMetal',col='STUDIO',bev=.001):
 return box(name,[(x[0]+x[1])/2,(h[0]+h[1])/2,(z[0]+z[1])/2],[x[1]-x[0],h[1]-h[0],z[1]-z[0]],mat,col,bev)
def cut(o,c):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;m=o.modifiers.new('Rebaje real R5C','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=c;bpy.ops.object.modifier_apply(modifier=m.name)
def erase(prefixes):
 for o in list(S.objects):
  if o.name.startswith(tuple(prefixes)):bpy.data.objects.remove(o,do_unlink=True)
# Three hinge mortises retain10mm of rear frame material and the actual wall attachment.
for h in [3.52,4.40,5.32]:
 c=bb('TEMP caja bisagra',[14.240,14.280],[h-.050,h+.050],[5.730,5.770],col='REFERENCE',bev=0)
 cut(bpy.data.objects['Marco puerta estudio fondo retorno'],c);bpy.data.objects.remove(c,do_unlink=True)
 c=bb('TEMP alojamiento nudillo central',[14.245,14.272],[h-.016,h+.016],[5.730,5.760],col='REFERENCE',bev=0)
 for o in [v for v in S.objects if v.name.startswith('Herraje estudio | placa fija')]:
  a,b=bounds(o)
  if a[2]<h<b[2]:cut(o,c)
 bpy.data.objects.remove(c,do_unlink=True)
 c=cyl('TEMP paso eje articulación',[14.260,h-.060,5.750],[14.260,h+.060,5.750],.0027,'stainless','REFERENCE')
 for o in [v for v in S.objects if v.name.startswith(('Herraje estudio | nudillo','Herraje estudio | ala móvil','Herraje estudio | ala fija'))]:
  a,b=bounds(o)
  if a[2]<h+.05 and b[2]>h-.05:cut(o,c)
 bpy.data.objects.remove(c,do_unlink=True)
 # Actual screw shanks and heads into rear frame/wall side, outside moving envelope.
 for dh in [-.033,.033]:
  cyl('Herraje estudio | tornillo marco',[14.245,h+dh,5.778],[14.268,h+dh,5.778],.0018,'stainless','STUDIO')
# Ground-floor furniture datum:750mm table,460mm chair,35mm tabletop, supports grounded.
map_h(bpy.data.objects['Mesa mono tapa'],.925,.960)
for o in [v for v in S.objects if v.name.startswith('Mesa mono pata')]:map_h(o,.210,.925)
for o in [v for v in S.objects if v.name.startswith('Silla mono ')]:
 if 'asiento' in o.name:map_h(o,.635,.670)
 elif 'respaldo' in o.name:map_h(o,.650,1.075)
 elif 'pata' in o.name:map_h(o,.210,.635)
for x in [17.568,18.533]:
 box('MOB95 | faldón mesa mono longitudinal',[x,.888,2.80],[.025,.074,.545],'woodDark','GROUND_FLOOR',.002)
for z in [2.5264,3.0736]:
 box('MOB95 | faldón mesa mono transversal',[18.05,.888,z],[.965,.074,.025],'woodDark','GROUND_FLOOR',.002)
# Hood: hollow four-sided canopy joins filter carrier and existing continuous duct.
erase(['Campana cocina'])
x0,x1,z0,z1=21.185,21.790,10.000,10.620
vs=[cv([x,h,z]) for h,xs,zs in [(4.825,[x0,x1],[z0,z1]),(5.170,[21.440,21.640],[10.210,10.410])] for x,z in [(xs[0],zs[0]),(xs[1],zs[0]),(xs[1],zs[1]),(xs[0],zs[1])]]
hood=mesh('Campana cocina | campana hueca',vs,[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],'stainless','INTERIORS')
mo=hood.modifiers.new('Chapa1.2mm','SOLIDIFY');mo.thickness=.0012
mo=hood.modifiers.new('Pliegue chapa','BEVEL');mo.width=.001;mo.segments=2
# Four lip profiles form a real open cassette frame, with two removable metal filters.
for z in [z0+.008,z1-.008]:box('Campana cocina | bastidor filtro',[21.4875,4.831,z],[.605,.012,.016],'stainless','INTERIORS',.001)
for x in [x0+.008,x1-.008]:box('Campana cocina | bastidor filtro',[x,4.831,10.31],[.016,.012,.588],'stainless','INTERIORS',.001)
box('Campana cocina | travesaño filtros',[21.4875,4.834,10.31],[.573,.012,.014],'stainless','INTERIORS',.001)
for za,zb in [(10.022,10.299),(10.321,10.598)]:
 for j in range(18):
  z=za+(zb-za)*j/17
  box('Campana cocina | lama filtro',[21.4875,4.840,z],[.557,.002,.006],'stainless','INTERIORS',.0004)
 for x in [21.28,21.49,21.69]:box('Campana cocina | soporte malla filtro',[x,4.843,(za+zb)/2],[.006,.002,zb-za],'stainless','INTERIORS',.0004)
# Trim original duct precisely at neck, preserving its route through roof and clear structural reserves.
duct=bpy.data.objects['Extracción cocina | salida independiente']
c=bb('TEMP base conducto',[21.0,21.9],[4.8,5.170],[9.9,10.8],col='REFERENCE',bev=0);cut(duct,c);bpy.data.objects.remove(c,do_unlink=True)
# Transition collar surrounding170mm OD tube; inner bore remains open.
collar=cyl('Campana cocina | collar unión',[21.54,5.16,10.31],[21.54,5.20,10.31],.092,'stainless','INTERIORS')
c=cyl('TEMP collar hueco',[21.54,5.15,10.31],[21.54,5.21,10.31],.0852,'stainless','REFERENCE');cut(collar,c);bpy.data.objects.remove(c,do_unlink=True)
for h in [4.93,5.08]:box('Campana cocina | ménsula muro',[21.765,h,10.31],[.05,.03,.28],'stainless','INTERIORS',.001)
# Recessed general light in bedroom keeps the finished2.60m plane clear.
cx,cz=15.82,7.30
ceil=bpy.data.objects['Cielorraso vivienda | 2.60m sobre piso general']
c=cyl('TEMP reserva plafón dormitorio',[cx,5.848,cz],[cx,5.960,cz],.182,'blackMetal','REFERENCE');cut(ceil,c);bpy.data.objects.remove(c,do_unlink=True)
housing=cyl('MOB95 | plafón dormitorio aro empotrado',[cx,5.850,cz],[cx,5.910,cz],.181,'whitePlaster','LIGHTS')
c=cyl('TEMP interior aro',[cx,5.84,cz],[cx,5.92,cz],.171,'blackMetal','REFERENCE');cut(housing,c);bpy.data.objects.remove(c,do_unlink=True)
cyl('MOB95 | plafón dormitorio fondo',[cx,5.912,cz],[cx,5.915,cz],.178,'whitePlaster','LIGHTS')
opal=bpy.data.materials.new('MOB95 | opal dormitorio');opal.use_nodes=True;bs=next(n for n in opal.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(.8,.8,.8,1);bs.inputs['Roughness'].default_value=.55;bs.inputs['Emission Color'].default_value=(1,.83,.66,1);bs.inputs['Emission Strength'].default_value=2.0;M['opal_bed']=opal
cyl('MOB95 | plafón dormitorio difusor',[cx,5.854,cz],[cx,5.857,cz],.172,'opal_bed','LIGHTS')
ld=bpy.data.lights.new('Suite | luz general plafón','AREA');lo=bpy.data.objects.new(ld.name,ld);COL['LIGHTS'].objects.link(lo);lo.location=cv([cx,5.852,cz]);ld.shape='DISK';ld.size=.32;ld.energy=32;ld.color=(1,.87,.73)
# Shape a thin woven cover continuously across mattress top, sides and foot.
erase(['Cama dormitorio manta','MOB95 | dobladillo manta'])
N,K=164,136;vs=[];fs=[]
creases=[(15.10,7.20,.9,.009),(16.51,7.30,-.7,.008),(15.50,7.83,1.4,.005),(16.32,7.92,-.6,.007)]
for j in range(K+1):
 v=j/K;z=6.945+1.20*v
 for i in range(N+1):
  u=i/N;x=14.898+1.84*u
  side=max(0,(14.970-x)/.072,(x-16.675)/.063);foot=max(0,(z-8.072)/.073)
  h=3.874-.277*max(min(1,side)**1.20,min(1,foot)**1.22)
  topfactor=max(0,1-max(side,foot))
  h+=topfactor*(.0035*math.sin(4.9*x+2.2*z)*math.sin(3.6*z-1.4*x))
  h+=.018*math.exp(-((z-6.962)/.022)**2)*(1-min(1,side))
  for a,b,theta,amp in creases:
   dx=x-a;dz=z-b;along=dx*math.cos(theta)+dz*math.sin(theta);cross=-dx*math.sin(theta)+dz*math.cos(theta)
   h+=amp*math.exp(-(cross/.022)**2-(along/.25)**2)*topfactor
  # Gravity folds on hanging portions, smaller than retained passage tolerance.
  h+=.002*math.sin((z-6.945)*50+u*7)*min(1,side)
  vs.append(cv([x,h,z]))
for j in range(K):
 for i in range(N):
  a=j*(N+1)+i;fs.append((a,a+1,a+N+2,a+N+1))
o=mesh('Cama dormitorio manta',vs,fs,'linen95','INTERIORS');mo=o.modifiers.new('Lino tejido2mm','SOLIDIFY');mo.thickness=.002
for p in o.data.polygons:p.use_smooth=True
for inds in [[j*(N+1) for j in range(K+1)],[j*(N+1)+N for j in range(K+1)],[K*(N+1)+i for i in range(N+1)]]:
 pts=[[vs[q].x,vs[q].z+.001,-vs[q].y] for q in inds[::2]];curve('MOB95 | dobladillo manta',pts,.0011,'linen95','INTERIORS')
# Fine directional timber finish for all newly created joinery.
woods={}
for m in bpy.data.materials:
 if m.name.startswith(('Roble aceitado | ','Nogal mate | ')) and 'parquet' not in m.name:
  axis=int(m.name.split(' | ',1)[1].split()[0]);woods[('wood' if m.name.startswith('Roble') else 'woodDark',axis)]=m
for o in S.objects:
 if o.type!='MESH' or o.hide_render:continue
 for slot in o.material_slots:
  key=slot.material.get('source_material_key') if slot.material else None
  if key in ['wood','woodDark']:
   axis=int(np.argmax(o.dimensions))
   if (key,axis) in woods:slot.link='OBJECT';slot.material=woods[key,axis]
S['review_iteration']='95 / R5C coordinated use and finish'
S['r5c_details']=json.dumps({'mono_floor':.21,'mono_table_top':.96,'mono_chair_seat':.67,'hood_filter_underside':4.825,'hood_connection_neck':5.17,'hood_status':'Proposed manufactured assembly; manufacturer flow and installation distances remain to confirm.','bedroom_general_light':'Recessed at finished ceiling+5.85; illustrative32W Blender emission power, not an electrical calculation.','hinges':'Three mortises and5.4mm knuckle bores around5mm pin','mattress_cover_bounds':[14.898,16.738,6.945,8.145]},ensure_ascii=False)
S['video_render_requires_explicit_approval']=True
S.frame_set(1);bpy.context.view_layer.update();bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
name='Casa_de_Campo_95_R5C_preview.blend' if '--preview' in sys.argv else 'Casa_de_Campo_95_R5C.blend'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output',name),compress=True);print('R5C_SAVED',name,flush=True)
