"""R7 D08: inspectable supply/extract reserve with ducts, filters, silencers and access.
Generic dimensional proposal only: no airflows, acoustic ratings, equipment capacity or certification.
apply() mutates the loaded R7 layout candidate without saving, and is idempotent after success.
"""
import bpy,bmesh,json,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree

def apply():
 S=bpy.context.scene
 if 'r7_vent_details' in S:
  finish_contacts();r=json.loads(S['r7_vent_details']);r['objects']=[o.name for o in S.objects if o.name.startswith('VENT99 |')];r['contact_finish']='liner0.8, absorber inner76.2mm; conforming elastomer-lined duct bands';S['r7_vent_details']=json.dumps(r,ensure_ascii=False);return r
 assert 'r7_layout' in S
 S.frame_set(1);bpy.context.view_layer.update();C=bpy.data.collections.new('99 | D08 Ventilación P');S.collection.children.link(C)
 VC=bpy.data.collections.get('VENTILATION')
 if not VC:VC=bpy.data.collections.new('VENTILATION');S.collection.children.link(VC)
 mats={}
 for key,col,rough,metal in [('metal',(.43,.46,.47,1),.32,1),('aislacion',(.42,.38,.28,1),.9,0),('sello',(.03,.035,.033,1),.6,0),('filtro',(.72,.74,.71,1),.95,0),('tapa',(.86,.855,.825,1),.5,0)]:
  m=bpy.data.materials.new('VENT99 | '+key);m.diffuse_color=col;m.use_nodes=True;m.node_tree.nodes.clear();bs=m.node_tree.nodes.new('ShaderNodeBsdfPrincipled');out=m.node_tree.nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(bs.outputs['BSDF'],out.inputs['Surface']);bs.inputs['Base Color'].default_value=col;bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal;mats[key]=m
 def cv(p):return Vector((p[0],-p[2],p[1]))
 def mesh(n,v,f,k='metal'):
  me=bpy.data.meshes.new(n);me.from_pydata([cv(p) for p in v],[],f);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();o=bpy.data.objects.new('VENT99 | '+n,me);C.objects.link(o);VC.objects.link(o);me.materials.append(mats[k]);o['detail_status']='P / reserva dimensional; dimensionamiento y selección profesional pendientes';return o
 def box(n,x,y,z,k='metal'):
  v=[(xx,yy,zz) for yy in y for zz in z for xx in x];return mesh(n,v,[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)],k)
 def boolean(o,c,operation='DIFFERENCE'):
  bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;m=o.modifiers.new('VENT99 reserva','BOOLEAN');m.operation=operation;m.solver='EXACT';m.object=c;bpy.ops.object.modifier_apply(modifier=m.name)
 def rm(o):bpy.data.objects.remove(o,do_unlink=True)
 def tube(n,path,r,ri,k='metal'):
  pp=[Vector(p) for p in path];N=32;vs=[];lastu=None
  for i,p in enumerate(pp):
   tangent=(pp[min(i+1,len(pp)-1)]-pp[max(0,i-1)]).normalized()
   if lastu is None:
    u=tangent.cross(Vector((0,1,0)))
    if u.length<.05:u=tangent.cross(Vector((1,0,0)))
   else:u=lastu-tangent*lastu.dot(tangent)
   u.normalize();v=tangent.cross(u);lastu=u
   for rr in ([r,ri] if ri else [r]):
    vs.extend([tuple(p+rr*(u*math.cos(j*2*math.pi/N)+v*math.sin(j*2*math.pi/N))) for j in range(N)])
  F=[];stride=N*2 if ri else N
  for a in range(len(pp)-1):
   for j in range(N):
    jj=(j+1)%N;q=a*stride;w=(a+1)*stride;F.append((q+j,q+jj,w+jj,w+j))
    if ri:F.append((q+N+j,w+N+j,w+N+jj,q+N+jj))
  if ri:
   e=(len(pp)-1)*stride
   for j in range(N):
    jj=(j+1)%N;F.extend([(j,N+j,N+jj,jj),(e+j,e+jj,e+N+jj,e+N+j)])
  else:
   a=len(vs);vs.extend([tuple(pp[0]),tuple(pp[-1])]);e=(len(pp)-1)*stride
   for j in range(N):jj=(j+1)%N;F.extend([(a,jj,j),(a+1,e+j,e+jj)])
  return mesh(n,vs,F,k)
 def rounded(path,r=.35):
  P=[Vector(p) for p in path];Q=[P[0]]
  for i in range(1,len(P)-1):
   a,b,c=P[i-1:i+2];u=(b-a).normalized();v=(c-b).normalized();d=min(r,(b-a).length*.45,(c-b).length*.45);s=b-u*d;e=b+v*d;Q.append(s)
   for j in range(1,13):
    t=j/12;Q.append((1-t)**2*s+2*t*(1-t)*b+t*t*e)
  Q.append(P[-1]);return [tuple(p) for p in Q]
 def loft(n,a,b,outer_a,outer_b,inner_a,inner_b,k='metal'):
  N=32;vv=[]
  def section(spec,t):
   if isinstance(spec,(list,tuple)):
    c,d=math.cos(t),math.sin(t);f=1/max(abs(c),abs(d));return spec[0]*c*f,spec[1]*d*f
   return spec*math.cos(t),spec*math.sin(t)
  for center,oo,ii in [(a,outer_a,inner_a),(b,outer_b,inner_b)]:
   for spec in [oo,ii]:
    for j in range(N):
     dx,dh=section(spec,2*math.pi*j/N);vv.append((center[0]+dx,center[1]+dh,center[2]))
  ff=[]
  for j in range(N):
   q=(j+1)%N;ff.extend([(j,q,2*N+q,2*N+j),(N+j,3*N+j,3*N+q,N+q),(j,N+j,N+q,q),(2*N+j,2*N+q,3*N+q,3*N+j)])
  return mesh(n,vv,ff,k)
 routes=[]
 def duct(n,path):
  p=rounded(path);tube(n+' chapa1',p,.076,.075);tube(n+' aislacion25',p,.101,.076,'aislacion');tube(n+' camisa0.5',p,.1015,.101)
  routes.append({'id':n,'centerline_source':path,'air_diameter_m':.15,'outside_diameter_m':.203,'insulation_m':.025,'rounding':'12-step smooth bends, generic fabricated proposal'})
 # Main body remains within the selected plenum reserve; all air passages are hollow.
 height=6.89;units=[];filter_parts=[];hangers=[]
 for key,z in [('impulsion',4.68),('extraccion',5.10)]:
  # Filter box200 long x250x250,2mm casing, removable bottom and200mm cassette.
  pieces=[]
  for label,xx,yy,zz in [('fondo',[18.70,18.90],[height-.125,height+.125],[z-.125,z-.123]),('frente',[18.70,18.90],[height-.125,height+.125],[z+.123,z+.125]),('techo',[18.70,18.90],[height+.123,height+.125],[z-.123,z+.123]),('tapa inferior desmontable',[18.702,18.898],[height-.125,height-.123],[z-.123,z+.123])]:pieces.append(box(key+' filtro '+label,xx,yy,zz))
  for xx,label in [(18.70,'entrada'),(18.898,'salida')]:
   o=box(key+' filtro '+label,[xx,xx+.002],[height-.123,height+.123],[z-.123,z+.123]);c=tube('TEMP boca filtro',[(xx-.002,height,z),(xx+.004,height,z)],.075,0);boolean(o,c);rm(c);pieces.append(o)
  media=box(key+' cartucho medio poroso P',[18.793,18.795],[height-.10,height+.10],[z-.10,z+.10],'filtro');media['porous_medium']='Filter placeholder: selection, resistance and grade not assigned';filter_parts.append(media.name)
  for zz in [z-.108,z+.10]:pieces.append(box(key+' cartucho marco',[18.785,18.803],[height-.108,height+.108],[zz,zz+.008]))
  for hh in [height-.108,height+.10]:pieces.append(box(key+' cartucho marco',[18.785,18.803],[hh,hh+.008],[z-.10,z+.10]))
  # Flexible connectors50mm, hollow; fan is a200mm removable module.
  tube(key+' flexible entrada',[(18.90,height,z),(18.95,height,z)],.078,.075,'sello')
  fan=tube(key+' ventilador carcasa',[(18.95,height,z),(19.15,height,z)],.078,.075)
  rotor=tube(key+' ventilador rotor',[(19.01,height,z),(19.09,height,z)],.026,0)
  for j in range(3):
   a=j*2*math.pi/3;v=[]
   for x,rr,theta in [(19.035,.025,a),(19.035,.066,a+.14),(19.065,.066,a+.57),(19.065,.025,a+.2)]:v.append((x,height+rr*math.cos(theta),z+rr*math.sin(theta)))
   # Generic0.8mm blades joined to hub; no rated fan selection is implied.
   vv=[(x+dx,h,zz) for dx in [-.0004,.0004] for x,h,zz in v]
   blade=mesh(key+' ventilador pala'+str(j),vv,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)])
   boolean(rotor,blade,'UNION');rm(blade)
  tube(key+' flexible salida',[(19.15,height,z),(19.20,height,z)],.078,.075,'sello')
  tube(key+' acople salida silenciador50',[(19.80,height,z),(19.85,height,z)],.078,.075,'sello')
  tube(key+' manta acople salida silenciador50',[(19.80,height,z),(19.85,height,z)],.1015,.078,'aislacion')
  sil=tube(key+' silenciador absorbente50',[(19.202,height,z),(19.798,height,z)],.125,.076,'aislacion')
  tube(key+' silenciador camisa0.8',[(19.20,height,z),(19.80,height,z)],.1258,.125)
  # Inner perforated liner has real longitudinal holes, represented as separate narrow metal strips.
  for j in range(20):
   a=j*2*math.pi/20;da=.065;v=[]
   for x in [19.202,19.798]:
    for rr in [.075,.0758]:
     for t in [a-da,a+da]:v.append((x,height+rr*math.cos(t),z+rr*math.sin(t)))
   mesh(key+' camisa perforada interna'+str(j),v,[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)])
  for x in [19.20,19.798]:tube(key+' silenciador tapa aro',[(x,height,z),(x+.002,height,z)],.125,.075)
  for x in [19.30,19.70]:
   tube(key+' abrazadera silenciador',[(x-.010,height,z),(x+.010,height,z)],.127,.1258)
   hangers.append((x,height+.127,z))
  hangers.extend([(18.74,height+.125,z),(18.86,height+.125,z)])
  units.append({'id':key,'bounds_source':{'x':[18.70,19.80],'y':[6.7642,7.0158],'z':[z-.127,z+.127]},'filter_box_m':[.20,.25,.25],'fan_length_m':.20,'silencer_length_m':.60,'air_diameter_m':.15,'cassette':media.name,'service':'isolate, remove hatch panels; release bottom cover/filter or detach flexible couplings and hangers, lower modules through hatch'})
 # Supply and extract terminals are distinct, neither shares a combustion duct.
 # Low rectangular façade crossings fit below the real beam while preserving3.20m room height.
 for key,x in [('aire exterior',17.64),('descarga exterior',20.16)]:
  aa=(x,6.565,0);bb=(x,6.565,1.15);cc=(x,6.73,1.75)
  for nm,ra,rb,k in [('chapa1',(.151,.041),(.15,.04),'metal'),('aislacion25',(.176,.066),(.151,.041),'aislacion'),('camisa0.5',(.1765,.0665),(.176,.066),'metal')]:loft(key+' rectangular '+nm,aa,bb,ra,ra,rb,rb,k)
  for nm,ra,rb,ca,cb,k in [('chapa1',(.151,.041),(.15,.04),.076,.075,'metal'),('aislacion25',(.176,.066),(.151,.041),.101,.076,'aislacion'),('camisa0.5',(.1765,.0665),(.176,.066),.1015,.101,'metal')]:loft(key+' transicion600 '+nm,bb,cc,ra,ca,rb,cb,k)
  routes.append({'id':key+' tramo rectangular','centerline_source':[aa,bb,cc],'air_section_m':[.300,.080],'air_area_m2':.024,'outside_section_m':[.353,.133],'lowest_indoor_m':6.4985,'top_m':6.6315,'beam_underside_m':6.6983334,'beam_gap_m':.0668334,'transition_length_m':.60})
 duct('aire exterior redondo',[(17.64,6.73,1.75),(17.64,6.73,3.65),(17.64,6.89,4.68),(18.70,6.89,4.68)])
 duct('impulsion ambiente',[(19.85,6.89,4.68),(20.70,6.89,4.68),(20.70,6.462,4.68)])
 duct('extraccion ambiente',[(16.50,6.462,5.10),(16.50,6.89,5.10),(18.70,6.89,5.10)])
 duct('descarga exterior redondo',[(19.85,6.89,5.10),(21.08,6.89,5.10),(21.08,6.89,3.90),(20.16,6.73,3.00),(20.16,6.73,1.75)])
 ceiling=bpy.data.objects['Cielorraso estudio | cota inferior 6.45m'];penetrated=[]
 # Grilles are real open slats at the ceiling, with collars and local bore reservations.
 for key,x,z in [('impulsion',20.70,4.68),('extraccion',16.50,5.10)]:
  cut=box('TEMP paso difusor',[x-.125,x+.125],[6.449,6.469],[z-.125,z+.125]);boolean(ceiling,cut);rm(cut)
  tube(key+' manguito cielorraso',[(x,6.462,z),(x,6.49,z)],.104,.1015);tube(key+' sello paso cielorraso',[(x,6.462,z),(x,6.468,z)],.105,.104,'sello')
  back=box(key+' cierre adaptador rejilla',[x-.125,x+.125],[6.460,6.462],[z-.125,z+.125]);hole=tube('TEMP hueco adaptador',[(x,6.459,z),(x,6.463,z)],.105,0);boolean(back,hole);rm(hole)
  for j in range(11):
   zz=z-.11+j*.022;box(key+' lama difusor',[x-.12,x+.12],[6.453,6.457],[zz-.0015,zz+.0015],'tapa')
  for xx in [x-.125,x+.12]:box(key+' marco rejilla',[xx,xx+.005],[6.453,6.460],[z-.12,z+.12],'tapa')
  for zz in [z-.125,z+.12]:box(key+' marco rejilla',[x-.125,x+.125],[6.453,6.460],[zz,zz+.005],'tapa')
 # Shallow rectangular weather terminals; no tall external riser, no roof or beam cut.
 facade=[o for o in S.objects if o.type=='MESH' and 'fachada' in o.name.lower()]
 for key,x in [('toma exterior',17.64),('descarga exterior',20.16)]:
  h=6.565;cut=box('TEMP paso fachada rectangular',[x-.1785,x+.1785],[h-.0685,h+.0685],[-.002,.202])
  for o in facade:
   vv=[o.matrix_world@Vector(v) for v in o.bound_box]
   if min(v.x for v in vv)<x<max(v.x for v in vv) and min(v.z for v in vv)<h<max(v.z for v in vv) and min(-v.y for v in vv)<.20:boolean(o,cut);penetrated.append(o.name)
  rm(cut)
  #2mm perimeter compression sleeve across the wall; proposal with no fire/water rating.
  for xx in [x-.1785,x+.1765]:box(key+' sello lateral',[xx,xx+.002],[h-.0685,h+.0685],[0,.20],'sello')
  for yy in [h-.0685,h+.0665]:box(key+' sello horizontal',[x-.1765,x+.1765],[yy,yy+.002],[0,.20],'sello')
  # Closed top and sides, downward-angled louvers within a60mm projection.
  box(key+' capuchon techo',[x-.20,x+.20],[h+.086,h+.089],[-.06,-.003])
  for xx in [x-.20,x+.197]:box(key+' capuchon costado',[xx,xx+.003],[h-.086,h+.086],[-.06,-.003])
  box(key+' capuchon vierteaguas',[x-.20,x+.20],[h-.089,h-.086],[-.06,-.003])
  for j in range(4):
   yy=h-.045+j*.03;mesh(key+' lama lluvia'+str(j),[(x-.197,yy,-.057),(x+.197,yy,-.057),(x+.197,yy+.018,-.02),(x-.197,yy+.018,-.02),(x-.197,yy+.002,-.057),(x+.197,yy+.002,-.057),(x+.197,yy+.02,-.02),(x-.197,yy+.02,-.02)],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])
  for xx in [x-.20,x+.19]:box(key+' flange lateral',[xx,xx+.01],[h-.089,h+.089],[-.003,0])
  for yy in [h-.089,h+.079]:box(key+' flange horizontal',[x-.19,x+.19],[yy,yy+.01],[-.003,0])
 # Seal strips conform to the evaluated bevels at the four corners of the facade openings.
 for o in list(C.objects):
  if o.name.startswith(('VENT99 | toma exterior sello','VENT99 | descarga exterior sello')):
   for host in sorted(set(penetrated)):boolean(o,bpy.data.objects[host])
 # Service hatch behind the acoustic clouds: no cloud has to be removed.
 raw={'x':[18.55,20.0],'z':[4.45,5.33]};cut=box('TEMP hueco registro',raw['x'],[6.44,6.47],raw['z']);boolean(ceiling,cut);rm(cut)
 # Reframe three ceiling channels; replacement headers carry their cut ends, supported to rafters.
 cut=box('TEMP recercado canales',[18.54,20.01],[6.59,6.66],[4.42,5.36]);channels=[]
 for n in ['Estudio | canal de cielorraso 07','Estudio | canal de cielorraso 08','Estudio | canal de cielorraso 09']:
  boolean(bpy.data.objects[n],cut);channels.append(n)
 rm(cut)
 for zz in [4.42,5.33]:box('cabecero recercado registro',[18.55,20.0],[6.605,6.645],[zz,zz+.03])
 # Frame on the back of the ceiling, with700mm removable panels and perimeter compression gasket.
 for xx in [18.55,19.975]:box('marco registro lateral',[xx,xx+.025],[6.477,6.480],[4.45,5.33]);box('junta registro lateral',[xx,xx+.025],[6.473,6.477],[4.45,5.33],'sello')
 for zz in [4.45,5.305]:box('marco registro extremo',[18.575,19.975],[6.477,6.480],[zz,zz+.025]);box('junta registro extremo',[18.575,19.975],[6.473,6.477],[zz,zz+.025],'sello')
 panels=[]
 for lo,hi in [(18.553,19.2735),(19.2765,19.997)]:
  o=box('panel registro desmontable',[lo,hi],[6.455,6.473],[4.453,5.327],'tapa');panels.append(o.name)
  for x in [lo+.05,hi-.05]:
   for z in [4.505,5.275]:
    hole=tube('TEMP alojamiento cierre',[(x,6.454,z),(x,6.474,z)],.0042,0);boolean(o,hole);rm(hole)
    tube('cierre cuarto vuelta panel vastago',[(x,6.455,z),(x,6.483,z)],.004,0)
    tube('cierre cuarto vuelta panel cabeza',[(x,6.453,z),(x,6.455,z)],.006,0)
    box('cierre cuarto vuelta panel leva',[x-.007,x+.007],[6.483,6.485],[z-.004,z+.004])
    keep=box('contraplaca fija cierre registro',[x-.012,x+.012],[6.480,6.483],[4.45,z+.012] if z<4.9 else [z-.012,5.33])
    hole=tube('TEMP contraplaca cierre',[(x,6.479,z),(x,6.484,z)],.0042,0);boolean(keep,hole);rm(hole)
 # Two cross rails for the unit, with physical rods and bearing plates to existing rafters.
 for z in [4.68,5.10]:box('travesaño suspendido equipos',[18.44,19.944],[7.10,7.13],[z-.025,z+.025])
 for x,y,z in hangers:tube('varilla equipo M6',[(x,y,z),(x,7.10,z)],.003,0);tube('tuerca equipo',[(x,y,z),(x,y+.005,z)],.006,.003)
 supports=[]
 def underside(x,z):
  best=None
  for o in S.objects:
   if not o.name.startswith('Estudio | cabio'):continue
   e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();v=[e.matrix_world@p.co for p in m.vertices];f=[list(p.vertices) for p in m.polygons];t=BVHTree.FromPolygons(v,f);hit=t.ray_cast(cv((x,6.5,z)),Vector((0,0,1)),3);e.to_mesh_clear()
   if hit[0] is not None and (best is None or hit[0].z<best[0]):best=(hit[0].z,o.name)
  assert best is not None,(x,z);return best
 for x in [18.496,19.888]:
  for z,start in [(4.68,7.13),(5.10,7.13),(4.435,6.645),(5.345,6.645)]:
   h,host=underside(x,z);h0,_=underside(x,z-.025);h1,_=underside(x,z+.025);vv=[(xx,hh-dd,zz) for dd in [.003,0] for zz,hh in [(z-.025,h0),(z+.025,h1)] for xx in [x-.025,x+.025]];plate=mesh('placa conformada bajo cabio',vv,[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]);tube('varilla a cabio M6',[(x,start,z),(x,h-.003,z)],.003,0)
   for dx in [-.016,.016]:tube('tornillo cabio P',[(x+dx,h-.003,z),(x+dx,h+.04,z)],.002,0)
   supports.append({'x':x,'z':z,'rod_bottom':start,'rafter_underside':h,'rafter':host,'status':'P; loads, timber condition, fastener design not validated'})
 # Duct hangers: low rectangular trapezes and round lined bands, all above clear-height datum.
 def anchored_carrier(label,xa,xb,z):
  ha,oa=underside(xa,z);hb,ob=underside(xb,z);rail_top=min(ha,hb)-.030;rail_bottom=rail_top-.025
  box(label+' travesano',[xa-.025,xb+.025],[rail_bottom,rail_top],[z-.02,z+.02])
  for x,h,host in [(xa,ha,oa),(xb,hb,ob)]:
   h0,_=underside(x,z-.025);h1,_=underside(x,z+.025);vv=[(xx,hh-dd,zz) for dd in [.003,0] for zz,hh in [(z-.025,h0),(z+.025,h1)] for xx in [x-.025,x+.025]];mesh(label+' placa conformada',vv,[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)])
   tube(label+' suspension a cabio',[(x,rail_top,z),(x,h-.003,z)],.003,0)
   for dx in [-.016,.016]:tube('tornillo cabio P',[(x+dx,h-.003,z),(x+dx,h+.04,z)],.002,0)
   supports.append({'x':x,'z':z,'rod_bottom':rail_top,'rafter_underside':h,'rafter':host,'status':'P / support for duct carrier; capacity not validated'})
  return rail_bottom
 for key,x,xa,xb in [('toma',17.64,17.104,17.80),('descarga',20.16,19.888,20.584)]:
  z=.65;rh=anchored_carrier(key+' rectangular',xa,xb,z)
  box(key+' rectangular apoyo inferior',[x-.205,x+.205],[6.4765,6.4965],[z-.012,z+.012]);box(key+' rectangular apoyo elastomerico',[x-.1765,x+.1765],[6.4965,6.4985],[z-.012,z+.012],'sello')
  for xx in [x-.19,x+.19]:tube(key+' rectangular varilla',[(xx,6.4965,z),(xx,rh,z)],.003,0)
  for z in ([2.5,3.05] if key=='toma' else [2.25,2.60]):
   rh=anchored_carrier(key+' redondo',xa,xb,z);tube(key+' abrazadera ducto',[(x,6.73,z-.012),(x,6.73,z+.012)],.103,.1015);tube(key+' suspension ducto',[(x,6.833,z),(x,rh,z)],.003,0)
 rh=anchored_carrier('extraccion interior',17.104,17.80,5.10);tube('extraccion interior abrazadera',[(17.588,6.89,5.10),(17.612,6.89,5.10)],.103,.1015);tube('extraccion interior suspension',[(17.60,6.993,5.10),(17.60,rh,5.10)],.003,0)
 # Drill the steel plate portion of each proposed wood fixing; only timber embedment remains intentional.
 for screw in [o for o in C.objects if o.name.startswith('VENT99 | tornillo cabio P')]:
  pts=[screw.matrix_world@v.co for v in screw.data.vertices];xx=sum(p.x for p in pts)/len(pts);zz=-sum(p.y for p in pts)/len(pts);hlo=min(p.z for p in pts);hhi=max(p.z for p in pts)
  cut=tube('TEMP taladro placa',[(xx,hlo-.001,zz),(xx,hhi,zz)],.0022,0)
  for plate in [o for o in C.objects if 'placa conformada' in o.name]:
   pp=[plate.matrix_world@v.co for v in plate.data.vertices]
   if min(p.x for p in pp)<xx<max(p.x for p in pp) and min(-p.y for p in pp)<zz<max(-p.y for p in pp):boolean(plate,cut)
  rm(cut)
 finish_contacts()
 report={'status':'P / geometría coordinada, selección y dimensionamiento pendientes','unit_bodies':units,'routes':routes,'hatch_raw':raw,'hatch_clear_m':[1.40,.83],'removable_panels':panels,'modified_ceiling_channels':channels,'rafter_supports':supports,'façade_hosts':sorted(set(penetrated)),'terminal_centres_source':[[17.64,6.565,0],[20.16,6.565,0]],'terminal_separation_m':2.52,'service_platform_plan':{'x':[18.95,19.55],'z':[4.48,5.68],'floor':3.25,'height_to_hatch_m':3.205,'lowest_fixed_accessory_m':6.453},'service_extraction':'Filter frames200mm and detachable fan/silencer modules up to600x254mm lower vertically through the open hatch after couplings/hangers are removed; no cloud removal needed.','limits':['No airflow, dB, RT, fire rating, motor power, filter grade or equipment capacity is assigned.','Professional mechanical sizing and environmental separation check remain required.','Local façade bores and new ceiling framing are proposals requiring substrate/loads verification.','Supply/extract are independent of existing combustion ducts.','The two small exterior hoods are necessary new façade elements of this proposal.'],'objects':[o.name for o in C.objects]}
 S['r7_vent_details']=json.dumps(report,ensure_ascii=False);bpy.context.view_layer.update();return report


def finish_contacts():
 """Build elastomer seats from the actual straight duct polygon, preserving its exterior envelope."""
 S=bpy.context.scene
 for o in list(S.objects):
  if 'silenciador absorbente50' not in o.name or o.get('contact99_finished'):continue
  zz=4.68 if 'impulsion' in o.name else 5.10;inv=o.matrix_world.inverted()
  for v in o.data.vertices:
   p=o.matrix_world@v.co;dy=p.y+zz;dh=p.z-6.89;r=math.hypot(dy,dh)
   if r<.10:p.y=-zz+dy*.0762/r;p.z=6.89+dh*.0762/r;v.co=inv@p
  o.data.update();o['contact99_finished']=True
 for o in [q for q in S.objects if q.name.startswith('VENT99 |') and ('abrazadera ducto' in q.name or 'extraccion interior abrazadera' in q.name)]:
  if o.get('seat99_raycast'):continue
  pp=[o.matrix_world@v.co for v in o.data.vertices];ctr=sum(pp,Vector())/len(pp);axis=0 if 'interior' in o.name else 1;rad=[i for i in range(3) if i!=axis];lo=min(p[axis] for p in pp);hi=max(p[axis] for p in pp)
  host='extraccion ambiente' if 'interior' in o.name else 'aire exterior redondo' if 'toma' in o.name else 'descarga exterior redondo'
  h=bpy.data.objects['VENT99 | '+host+' camisa0.5'];e=h.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();hv=[e.matrix_world@v.co for v in m.vertices];hf=[list(p.vertices) for p in m.polygons];tree=BVHTree.FromPolygons(hv,hf);e.to_mesh_clear()
  angles=[j*2*math.pi/128 for j in range(128)]
  # Include every straight-section corner, so inner polygon edges never chord through the sheet.
  for p in hv:
   dd=p-ctr;rr=math.hypot(dd[rad[0]],dd[rad[1]])
   if .1008<rr<.1018:angles.append(math.atan2(dd[rad[1]],dd[rad[0]])%(2*math.pi))
  angles=sorted(set(round(t,9) for t in angles));N=len(angles);inner=[]
  for t in angles:
   d=Vector();d[rad[0]]=math.cos(t);d[rad[1]]=math.sin(t);hit=tree.ray_cast(ctr+d*.15,-d,.12);assert hit[0] is not None,(o.name,t)
   rr=(hit[0]-ctr).length;assert .100<rr<.103,(o.name,rr);inner.append(rr+.000001)
  def annulus(name,outer,inside,target=None):
   vv=[]
   for station in [lo,hi]:
    for radius in [outer,inside]:
     for j,t in enumerate(angles):
      rr=radius[j] if isinstance(radius,list) else radius;p=ctr.copy();p[axis]=station;p[rad[0]]+=rr*math.cos(t);p[rad[1]]+=rr*math.sin(t);vv.append(p)
   ff=[]
   for j in range(N):
    k=(j+1)%N;ff.extend([(j,k,2*N+k,2*N+j),(N+j,3*N+j,3*N+k,N+k),(j,N+j,N+k,k),(2*N+j,2*N+k,3*N+k,3*N+j)])
   me=bpy.data.meshes.new(name);me.from_pydata(vv,[],ff);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
   if target:target.data=me;target.matrix_world.identity();me.materials.append(bpy.data.materials['VENT99 | metal']);return target
   q=bpy.data.objects.new(name,me)
   for c in o.users_collection:c.objects.link(q)
   me.materials.append(bpy.data.materials['VENT99 | sello']);return q
  linename=o.name.replace('abrazadera','forro elastomerico');old=bpy.data.objects.get(linename)
  if old:bpy.data.objects.remove(old,do_unlink=True)
  annulus(linename,.103,inner);annulus(o.name,.105,.103,o);o['seat99_raycast']=True;o['contact99_finished']=True
 for o in S.objects:
  if not o.name.startswith('VENT99 |') or not('suspension ducto' in o.name or 'extraccion interior suspension' in o.name) or o.get('contact99_finished'):continue
  inv=o.matrix_world.inverted();points=[o.matrix_world@v.co for v in o.data.vertices];low=min(p.z for p in points)
  for v in o.data.vertices:
   p=o.matrix_world@v.co
   if abs(p.z-low)<1e-6:p.z+=.002;v.co=inv@p
  o.data.update();o['contact99_finished']=True
 bpy.context.view_layer.update()
