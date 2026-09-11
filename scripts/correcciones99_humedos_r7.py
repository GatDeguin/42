"""R7 C2: dimensional wet-area lining proposal, no performance/product certification.
apply() changes the loaded layout candidate only; no save, no render. Idempotent after success.
"""
import bpy,bmesh,json,math
from mathutils import Vector

def apply():
 S=bpy.context.scene
 if 'r7_wet_details' in S:return upgrade_grout()
 assert 'r7_layout' in S,'Requires R7 layout'
 S.frame_set(1);bpy.context.view_layer.update()
 C=bpy.data.collections.new('99 | Acabados húmedos P');S.collection.children.link(C)
 shared=bpy.data.collections.get('CONSTRUCTION')
 if not shared:shared=bpy.data.collections.new('CONSTRUCTION');S.collection.children.link(shared)
 mats={}
 for key,color,rough in [('ceramica',(.78,.80,.77,1),.26),('junta',(.52,.55,.53,1),.68),('adhesivo',(.28,.29,.27,1),.8),('membrana',(.09,.25,.25,1),.66),('sello',(.11,.13,.12,1),.5),('base',(.55,.56,.53,1),.85),('metal',(.48,.5,.5,1),.23)]:
  m=bpy.data.materials.new('WET99 | '+key);m.diffuse_color=color;m.use_nodes=True;m.node_tree.nodes.clear();bs=m.node_tree.nodes.new('ShaderNodeBsdfPrincipled');out=m.node_tree.nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(bs.outputs['BSDF'],out.inputs['Surface']);bs.inputs['Base Color'].default_value=color;bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=1 if key=='metal' else 0;mats[key]=m
 def cv(p):return (p[0],-p[2],p[1])
 def mesh(n,v,f,k):
  me=bpy.data.meshes.new(n);me.from_pydata([cv(p) for p in v],[],f);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();o=bpy.data.objects.new('WET99 | '+n,me);C.objects.link(o);shared.objects.link(o);o.data.materials.append(mats[k]);o['detail_status']='P / capas y encuentros propuestos; selección compatible y ejecución profesional pendientes';return o
 def box(n,x,y,z,k):
  v=[(x0,y0,z0) for y0 in y for z0 in z for x0 in x];return mesh(n,v,[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)],k)
 def boolean(o,c):
  bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;m=o.modifiers.new('WET99 reserva local','BOOLEAN');m.solver='EXACT';m.operation='DIFFERENCE';m.object=c;bpy.ops.object.modifier_apply(modifier=m.name)
 def remove(o):bpy.data.objects.remove(o,do_unlink=True)
 def ring(n,x0,x1,z0,z1,inner,outer,y0,y1,k):
  # Nested rectangular annulus, exact corner continuity with one manifold mesh.
  q=[(x0-outer,z0-outer),(x1+outer,z0-outer),(x1+outer,z1+outer),(x0-outer,z1+outer),(x0-inner,z0-inner),(x1+inner,z0-inner),(x1+inner,z1+inner),(x0-inner,z1+inner)]
  v=[(x,h,z) for h in [y0,y1] for x,z in q];f=[]
  for i in range(4):
   j=(i+1)%4;f.extend([(i,j,j+4,i+4),(i+8,i+12,j+12,j+8),(i,i+8,j+8,j),(i+4,j+4,j+12,i+12)])
  return mesh(n,v,f,k)
 def tube(n,a,b,r,ri,k):
  va,vb=Vector(a),Vector(b);axis=(vb-va).normalized();u=axis.cross(Vector((0,1,0)))
  if u.length<.1:u=axis.cross(Vector((1,0,0)))
  u.normalize();v=axis.cross(u).normalized();points=[];N=32
  for c in [va,vb]:
   for rr in [r,ri]:
    for i in range(N):points.append(tuple(c+rr*(u*math.cos(i*2*math.pi/N)+v*math.sin(i*2*math.pi/N))))
  if ri==0:
   points=[points[i] for i in range(N)]+[points[2*N+i] for i in range(N)]+[tuple(va),tuple(vb)];f=[]
   for i in range(N):
    j=(i+1)%N;f.extend([(i,j,N+j,N+i),(2*N,j,i),(2*N+1,N+i,N+j)])
   return mesh(n,points,f,k)
  f=[]
  for i in range(N):
   j=(i+1)%N;f.extend([(i,j,2*N+j,2*N+i),(N+i,3*N+i,3*N+j,N+j),(i,N+i,N+j,j),(2*N+i,2*N+j,3*N+j,3*N+i)])
  return mesh(n,points,f,k)
 def sb(o):
  pts=[o.matrix_world@Vector(v) for v in o.bound_box];return {'x':[min(p.x for p in pts),max(p.x for p in pts)],'y':[min(p.z for p in pts),max(p.z for p in pts)],'z':[min(-p.y for p in pts),max(-p.y for p in pts)]}
 operations=[]
 # PB: retain every clear finished face by recessing14mm into the conceptual substrate.
 x0,x1,z0,z1=19.39,21.80,.26,1.81;y0,y1=.19,2.61
 for o in list(S.objects):
  if o.name.startswith(('BTH95 | ducha remonte membrana','BTH95 | ducha membrana puente','BTH95 | ducha protección retorno')):remove(o)
 cutter=ring('TEMP rebaje perimetral14',x0,x1,z0,z1,0,.014,y0,y1,'base')
 hosts=['LAY99 | baño mono trasdosado frontal60','LAY99 | baño mono oeste norte','LAY99 | baño mono oeste sur','LAY99 | baño mono oeste dintel','LAY99 | baño mono posterior','Medianera constructiva baja','Pilar esquina frontal derecha']
 for n in hosts:boolean(bpy.data.objects[n],cutter)
 remove(cutter)
 layers=[ring('PB membrana continua2',x0,x1,z0,z1,.012,.014,.192,y1,'membrana'),ring('PB adhesivo4',x0,x1,z0,z1,.008,.012,.192,y1,'adhesivo'),ring('PB ceramica8',x0,x1,z0,z1,0,.008,.192,y1,'ceramica'),ring('PB retorno piso muro2',x0,x1,z0,z1,0,.014,.19,.192,'membrana')]
 opening=box('TEMP hueco puerta PB',[19.24,19.391],[.18,2.4601],[.36,1.36],'base')
 for o in layers:boolean(o,opening)
 remove(opening)
 # The frame joins the perimeter lining at the raw reveal; silicone joint is recessed into the finish.
 for zz,zzs in [(.36,[.357,.36]),(1.36,[1.36,1.363])]:
  c=box('TEMP junta jamba',[19.387,19.3901],[.21,2.46],zzs,'base')
  for o in layers:boolean(o,c)
  remove(c);box('PB sello lateral marco',[19.387,19.39],[.21,2.46],zzs,'sello')
 # Grout2mm wide through the full8mm ceramic thickness; adhesive and membrane remain continuous.
 grooves=[]
 for hh in [.51,.81,1.11,1.41,1.71,2.01,2.31]:
  grooves.extend([box('PB junta horizontal frontal',[x0,x1],[hh-.001,hh+.001],[z0-.008,z0],'junta'),box('PB junta horizontal posterior',[x0,x1],[hh-.001,hh+.001],[z1,z1+.008],'junta'),box('PB junta horizontal este',[x1,x1+.008],[hh-.001,hh+.001],[z0,z1],'junta')])
 for xx in [19.99,20.59,21.19,21.79]:
  grooves.extend([box('PB junta vertical frontal',[xx-.001,xx+.001],[.21,y1],[z0-.008,z0],'junta'),box('PB junta vertical posterior',[xx-.001,xx+.001],[.21,y1],[z1,z1+.008],'junta')])
 for zz in [.86,1.46]:grooves.append(box('PB junta vertical este',[x1,x1+.008],[.21,y1],[zz-.001,zz+.001],'junta'))
 # Apply each manifold groove separately; overlapping multi-solid cutters are not valid Boolean operands.
 # Final separated tiles and full-depth grout are built below, after penetration coordinates are known.
 # Wall penetrations have a real local collar from membrane to finish; services beyond remain unallocated.
 penetrations=[]
 targets=[o for o in S.objects if o.name.startswith(('BTH95 | grifo mono toma','BTH95 | ramal lavatorio mono','BTH95 | anclaje ménsula mono','BTH95 | mampara anclaje muro'))]
 for o in targets:
  b=sb(o);x=sum(b['x'])/2;h=sum(b['y'])/2;r=max(b['x'][1]-b['x'][0],b['y'][1]-b['y'][0])/2;rr=r+.002
  c=tube('TEMP paso '+o.name,(x,h,z0-.017),(x,h,z0+.002),rr,0,'base')
  for lay in layers:boolean(lay,c)
  for g in grooves:
   gb=sb(g)
   if gb['x'][0]<x+rr and gb['x'][1]>x-rr and gb['y'][0]<h+rr and gb['y'][1]>h-rr and gb['z'][0]<z0+.003:boolean(g,c)
  remove(c);tube('PB collar '+o.name,(x,h,z0-.014),(x,h,z0),rr,r,'sello');penetrations.append({'hosted_part':o.name,'center_source':[x,h,z0],'outer_radius_m':rr,'inner_radius_m':r})
 # Shower brackets are connected to proposed embedded stubs instead of stopping at the finish.
 for h in [1.31,2.23]:
  c=tube('TEMP paso ducha',(21.35,h,z0-.02),(21.35,h,z0+.001),.009,0,'base')
  for lay in layers:boolean(lay,c)
  remove(c);tube('PB conexion empotrada ducha',(21.35,h,z0-.03),(21.35,h,z0),.007,0,'metal');tube('PB collar ducha',(21.35,h,z0-.014),(21.35,h,z0),.009,.007,'sello')
 # PA: preserve existing shower facing Z6.165 and medianera X21.80; bridge its old5mm rear gap.
 old=bpy.data.objects.get('Revestimiento ducha suite')
 if old:remove(old)
 # North panel is enlarged only to enclose the bathtub splash footprint, with no change to existing face.
 nx0,nx1=20.40,21.80;zf=6.165;zback=6.10;zhigh=7.45;fy=3.232;top=5.57
 base=box('PA base continua tras revestimiento',[nx0,nx1],[fy,top],[zback,zf-.014],'base')
 pa=[box('PA membrana frontal2',[nx0,nx1],[3.232,top],[zf-.014,zf-.012],'membrana'),box('PA adhesivo frontal4',[nx0,nx1],[fy,top],[zf-.012,zf-.008],'adhesivo'),box('PA ceramica frontal8',[nx0,nx1],[fy,top],[zf-.008,zf],'ceramica')]
 # Side wall finishes are recessed; corner turns overlap neither layer nor facing.
 c=box('TEMP PA medianera',[21.80,21.814],[3.23,top+.008],[zf-.014,zhigh],'base');boolean(bpy.data.objects['Medianera alta vivienda'],c);remove(c)
 pa.extend([box('PA membrana lateral2',[21.812,21.814],[3.232,top],[zf-.014,zhigh],'membrana'),box('PA adhesivo lateral4',[21.808,21.812],[fy,top],[zf-.012,zhigh],'adhesivo'),box('PA ceramica lateral8',[21.8,21.808],[fy,top],[zf,zhigh],'ceramica')])
 # Closed corner bridge behind the visible ceramic: concrete dimensional connection, not a claimed product seal.
 pa.extend([box('PA membrana esquina',[21.8,21.812],[3.232,top],[zf-.014,zf-.012],'membrana'),box('PA adhesivo esquina',[21.8,21.808],[fy,top],[zf-.012,zf],'adhesivo')])
 # Floor tie: existing2mm PA floor membrane is at3.230..3.232.
 for xx,zz,n in [([nx0-.008,nx1],[6.10,zf],'frontal'),([21.8,21.814],[zf-.014,zhigh],'lateral')]:
  c=box('TEMP PA reserva piso '+n,xx,[3.2299,3.25],zz,'base')
  for o in list(S.objects):
   if o.name.startswith(('Piso baño vivienda','MOB95 | piso baño')):boolean(o,c)
  remove(c);pa.append(box('PA retorno piso '+n,xx,[3.23,3.232],zz,'membrana'))
 # End returns cap the coating edge and its backing; upper edges use a washable cap.
 pa.append(box('PA retorno borde izquierdo8',[nx0-.008,nx0],[fy,top],[zback,zf],'ceramica'))
 pa.append(box('PA tapa superior8',[nx0-.008,21.80],[top,top+.008],[zback,zf],'ceramica'))
 pa.append(box('PA tapa superior lateral8',[21.8,21.808],[top,top+.008],[zf-.014,zhigh],'ceramica'))
 # Preserve the existing niche void and extend its ceramic returns to the unchanged finish face.
 nc=box('TEMP hueco nicho existente',[21.1945,21.4055],[4.6195,5.0805],[6.098,zf+.001],'base')
 for o in pa+[base]:boolean(o,nc)
 remove(nc)
 for n,xx,yy in [('izq',[21.1975,21.2125],[4.64,5.06]),('der',[21.3875,21.4025],[4.64,5.06]),('inferior',[21.20,21.40],[4.6225,4.6375]),('superior',[21.20,21.40],[5.0625,5.0775])]:
  pa.append(box('PA retorno nicho '+n,xx,yy,[6.130001,zf],'ceramica'))
 # A continuous four-sided elastic collar seals the existing niche perimeter to the new membrane.
 for n,xx,yy in [('izq',[21.1945,21.1975],[4.6195,5.0805]),('der',[21.4025,21.4055],[4.6195,5.0805]),('inferior',[21.1975,21.4025],[4.6195,4.6225]),('superior',[21.1975,21.4025],[5.0775,5.0805])]:pa.append(box('PA collar nicho '+n,xx,yy,[6.13,zf],'sello'))
 # The towel rail has a real socket and collar where the enlarged backing now reaches its existing support.
 c=tube('TEMP PA paso toallero',(20.54,4.35,6.098),(20.54,4.35,6.181),.013,0,'base')
 for o in pa+[base]:boolean(o,c)
 remove(c);pa.append(tube('PA collar toallero',(20.54,4.35,zf-.014),(20.54,4.35,zf),.013,.011,'sello'))
 # Extend the observed35mm faucet gap with housed metal stems and separate membrane collars.
 for label,x,h,r in [('llenador',21.10,3.98,.014),('mando',21.17,4.0,.026)]:
  c=tube('TEMP PA paso '+label,(x,h,6.118),(x,h,6.202),r+.002,0,'base')
  for o in pa+[base]:boolean(o,c)
  remove(c);tube('PA cuerpo empotrado '+label,(x,h,6.12),(x,h,6.20),r,0,'metal');tube('PA collar '+label,(x,h,zf-.014),(x,h,zf),r+.002,r,'sello');tube('PA roseta '+label,(x,h,zf),(x,h,zf+.004),r+.014,r,'metal')
 report={'status':'P / propuesta dimensional incorporada','PB_clear_finished_faces':{'x':[x0,x1],'z':[z0,z1]},'layers_mm':{'ceramic':8,'adhesive':4,'membrane':2},'PB_grout_width_mm':2,'PB_grout_depth_mm':8,'PB_tile_module_mm':[600,300],'PB_tile_top_m':y1,'PA_facing_Z':zf,'PA_wall_X':21.8,'PA_tile_top_m':top,'PA_faucet_gap_closed_mm':35,'penetrations':penetrations,'objects':[o.name for o in C.objects],'limits':['No product, waterproofing performance or structural capacity is certified.','Proposed collars/returns require compatible product specification and installation design.','Services behind embedded stubs are reservations; no invented network sizing.','The14mm recess represents finish build-up within conceptual wall volumes; real substrate/reinforcement survey required.']}
 S['r7_wet_details']=json.dumps(report,ensure_ascii=False);bpy.context.view_layer.update();return rebuild_pb_tiles()


def upgrade_grout():return rebuild_pb_tiles()

def rebuild_pb_tiles():
 """Separated600x300 tiles with8mm through joints; no cutting a connected corner annulus."""
 S=bpy.context.scene;r=json.loads(S['r7_wet_details'])
 if r.get('PB_tile_mesh_version')==2:return r
 C=bpy.data.collections['99 | Acabados húmedos P'];shared=bpy.data.collections['CONSTRUCTION'];tilemat=bpy.data.materials['WET99 | ceramica'];groutmat=bpy.data.materials['WET99 | junta'];sealmat=bpy.data.materials['WET99 | sello']
 for o in list(S.objects):
  if o.name=='WET99 | PB ceramica8' or o.name.startswith(('WET99 | PB junta ','WET99 | PB pastina juntas','WET99 | PB sello esquina')):bpy.data.objects.remove(o,do_unlink=True)
 def make(name,pts,faces,material):
  me=bpy.data.meshes.new(name);me.from_pydata([(p[0],-p[2],p[1]) for p in pts],[],faces);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();o=bpy.data.objects.new(name,me);C.objects.link(o);shared.objects.link(o);me.materials.append(material);return o
 def cube(name,x,h,z,material=tilemat):return make(name,[(xx,hh,zz) for hh in h for zz in z for xx in x],[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)],material)
 def sb(o):
  p=[o.matrix_world@Vector(v) for v in o.bound_box];return ([min(q[i] for q in p) for i in range(3)],[max(q[i] for q in p) for i in range(3)])
 def hit(a,b):return all(min(a[1][i],b[1][i])-max(a[0][i],b[0][i])>1e-7 for i in range(3))
 def diff(a,b):
  bpy.context.view_layer.update();bpy.context.view_layer.objects.active=a;m=a.modifiers.new('local tile opening','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=b;bpy.ops.object.modifier_apply(modifier=m.name)
 cuts=[cube('TEMP door',[19.24,19.391],[.18,2.4601],[.36,1.36]),cube('TEMP jamb sealN',[19.387,19.3901],[.21,2.46],[.357,.36]),cube('TEMP jamb sealS',[19.387,19.3901],[.21,2.46],[1.36,1.363])]
 for index,spec in enumerate(r['penetrations']+[{'center_source':[21.35,h,.26],'outer_radius_m':.009} for h in [1.31,2.23]]):
  x,h,z=spec['center_source'];rad=spec['outer_radius_m'];N=64;v=[(x+rad*math.cos(j*2*math.pi/N),h+rad*math.sin(j*2*math.pi/N),zz) for zz in [.24,.28] for j in range(N)];v.extend([(x,h,.24),(x,h,.28)]);f=[]
  for j in range(N):k=(j+1)%N;f.extend([(j,k,N+k,N+j),(2*N,k,j),(2*N+1,N+j,N+k)])
  cuts.append(make('TEMP collar'+str(index),v,f,tilemat))
 bpy.context.view_layer.update();cb={o.name:sb(o) for o in cuts}
 joints_h=[.51,.81,1.11,1.41,1.71,2.01,2.31];rows=[];last=.192
 for h in joints_h:rows.append((last,h-.001));last=h+.001
 rows.append((last,2.61))
 # Symmetric305mm edge cuts avoid a10mm sliver while preserving the600mm module.
 joints_x=[19.695,20.295,20.895,21.495];joints_z=[.86,1.46]
 def spans(lo,hi,joints):
  rr=[];last=lo
  for x in joints:rr.append((last,x-.001));last=x+.001
  rr.append((last,hi));return rr
 tileparts=[];groutparts=[]
 def part(name,x,h,z,isgrout=False):
  if min(x[1]-x[0],h[1]-h[0],z[1]-z[0])<=1e-7:return
  o=cube(name,x,h,z,groutmat if isgrout else tilemat);bpy.context.view_layer.update();ob=sb(o)
  for cut in cuts:
   if hit(ob,cb[cut.name]):diff(o,cut)
  if not o.data.polygons:bpy.data.objects.remove(o,do_unlink=True);return
  (groutparts if isgrout else tileparts).append(o)
 for label,zz in [('frontal',(.252,.26)),('posterior',(1.81,1.818))]:
  for xx in spans(19.392,21.798,joints_x):
   for hh in rows:part('TEMP baldosa '+label,xx,hh,zz)
  for hh in joints_h:part('TEMP pastina '+label,(19.392,21.798),(hh-.001,hh+.001),zz,True)
  for xx in joints_x:
   for hh in rows:part('TEMP pastina '+label,(xx-.001,xx+.001),hh,zz,True)
 for label,xx in [('oeste',(19.382,19.39)),('este',(21.8,21.808))]:
  for zz in spans(.262,1.808,joints_z):
   for hh in rows:part('TEMP baldosa '+label,xx,hh,zz)
  for hh in joints_h:part('TEMP pastina '+label,xx,(hh-.001,hh+.001),(.262,1.808),True)
  for zz in joints_z:
   for hh in rows:part('TEMP pastina '+label,xx,hh,(zz-.001,zz+.001),True)
 def combine(items,name,material):
  vv=[];ff=[]
  for o in items:
   offset=len(vv);vv.extend([(v.co.x,v.co.z,-v.co.y) for v in o.data.vertices]);ff.extend([[offset+i for i in f.vertices] for f in o.data.polygons]);bpy.data.objects.remove(o,do_unlink=True)
  return make(name,vv,ff,material)
 count=len(tileparts);cer=combine(tileparts,'WET99 | PB ceramica8',tilemat);combine(groutparts,'WET99 | PB pastina juntas8',groutmat)
 for ix,x in enumerate([19.39,21.8]):
  for iz,z in enumerate([.26,1.81]):
   # L shaped2mm exposed silicone joint connecting the8mm side and front tile returns.
   signx=1 if ix==0 else -1;signz=1 if iz==0 else -1;q=[(-.008,-.008),(.002,-.008),(.002,0),(0,0),(0,.002),(-.008,.002)];pts=[(x+signx*dx,h,z+signz*dz) for h in [.192,2.61] for dx,dz in q];N=6;f=[tuple(range(N-1,-1,-1)),tuple(range(N,2*N))]
   for j in range(N):k=(j+1)%N;f.append((j,k,N+k,N+j))
   make('WET99 | PB sello esquina'+str(ix)+str(iz),pts,f,sealmat)
 for o in cuts:bpy.data.objects.remove(o,do_unlink=True)
 r.update({'PB_grout_width_mm':2,'PB_grout_depth_mm':8,'PB_tile_module_mm':[600,300],'PB_tile_mesh_version':2,'PB_tile_components':count,'PB_joint_lines_source_x':joints_x,'PB_joint_lines_height':joints_h,'PB_corner_exposed_seal_mm':2,'PB_symmetric_nominal_edge_cut_mm':305,'objects':[o.name for o in C.objects],'grout_upgrade':'Separate ceramic tile bodies and full-depth grout; adhesive/membrane and finished faces unchanged'})
 S['r7_wet_details']=json.dumps(r,ensure_ascii=False);bpy.context.view_layer.update();return r
