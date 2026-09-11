import bpy, math, json, os, hashlib, random
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if '__file__' in globals() else 'D:/2026/42'
# Set ROOT explicitly when executing this file from Blender's loaded-scene wrapper.
if not os.path.isdir(os.path.join(ROOT,'source')):ROOT='D:/2026/42'
PREFIX='R8B | ';TAG='revision99_textiles_botanica_r8';S=bpy.context.scene
OUT=os.path.join(ROOT,'review99','r8_textiles_botanica');os.makedirs(OUT,exist_ok=True)

def bounds(o):
 dg=bpy.context.evaluated_depsgraph_get();ev=o.evaluated_get(dg)
 if o.type in {'MESH','CURVE','FONT','SURFACE'}:
  me=ev.to_mesh();a=np.array([tuple(ev.matrix_world@v.co) for v in me.vertices]);ev.to_mesh_clear()
  if len(a):return a.min(0),a.max(0)
 return np.zeros(3),np.zeros(3)

def original_scope(o):
 n=o.name
 return n=='Cama dormitorio manta' or n.startswith(('MOB95 | dobladillo manta','Cama dormitorio almohada ','MOB95 | costura funda almohada','Cortina suite ','MOB95 | dobladillo cortina','Vestidor prenda ','Hojas de huerta ','Tallo hortaliza ')) or (n.startswith('Huerta cantero ') and n.endswith(' sustrato'))

def fingerprints(objects):
 cache={};out={}
 for o in objects:
  h=hashlib.sha256(np.array(o.matrix_world,dtype=np.float64).tobytes());h.update(str([(m.name,m.type,getattr(m,'thickness',None),getattr(m,'use_even_offset',None)) for m in o.modifiers]).encode());h.update(str((o.hide_render,o.hide_viewport,o.hide_get(),[m.name if m else None for m in o.data.materials] if hasattr(o.data,'materials') else [],o.parent.name if o.parent else None)).encode())
  if o.type=='MESH':
   key=o.data.as_pointer()
   if key not in cache:
    v=np.empty(len(o.data.vertices)*3,np.float32);o.data.vertices.foreach_get('co',v);f=np.empty(len(o.data.loops),np.int32);o.data.loops.foreach_get('vertex_index',f);cache[key]=hashlib.sha256(v.tobytes()+f.tobytes()).digest()
   h.update(cache[key])
  out[o.name]=h.hexdigest()
 return out

def material(name,color,rough=.65,metal=0):
 m=bpy.data.materials.new(PREFIX+name);m.use_nodes=True;m.diffuse_color=(*color,1);m['photographic99']=True;m[TAG]=True
 p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 return m

def image_load(path,noncolor=False):
 im=bpy.data.images.load(path,check_existing=True)
 if noncolor:im.colorspace_settings.name='Non-Color'
 return im

def textile(name,key,normal=.28):
 m=material(name,(.5,.5,.5));ns=m.node_tree.nodes;ls=m.node_tree.links;p=next(n for n in ns if n.type=='BSDF_PRINCIPLED');p.inputs['Sheen Weight'].default_value=.25;p.inputs['Sheen Roughness'].default_value=.62
 uv=ns.new('ShaderNodeUVMap');uv.uv_map='UV0'
 for channel,file in [('color','r7b/'+key+'_basecolor.png'),('rough','terlenka_rough_2k.png'),('normal','terlenka_nor_gl_2k.png')]:
  t=ns.new('ShaderNodeTexImage');t.image=image_load(os.path.join(ROOT,'source','assets','terlenka',file),channel!='color');ls.new(uv.outputs['UV'],t.inputs['Vector'])
  if channel=='color':ls.new(t.outputs['Color'],p.inputs['Base Color'])
  elif channel=='rough':ls.new(t.outputs['Color'],p.inputs['Roughness'])
  else:
   n=ns.new('ShaderNodeNormalMap');n.uv_map='UV0';n.inputs['Strength'].default_value=normal;ls.new(t.outputs['Color'],n.inputs['Color']);ls.new(n.outputs['Normal'],p.inputs['Normal'])
 m['source_asset']='Poly Haven Terlenka / CC0';m['texture_module_m']=[.2657081476760712,.2662999927997589];m['material_note']='Measured photographic weave, linear dye calibration. Shape and seams are geometry.'
 return m

CREATED=[]
def mesh(name,verts,faces,mat,uvs=None,layer='upperDetail',smooth=True):
 me=bpy.data.meshes.new(PREFIX+name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(PREFIX+name,me);S.collection.objects.link(o);o[TAG]=True;o['source_layer']=layer;o['status']='P';o['proposal']='R8B visual/physical textile and planting refinement; existing architecture retained'
 if mat:me.materials.append(mat)
 uv=me.uv_layers.new(name='UV0')
 for p in me.polygons:
  p.use_smooth=smooth
  for li in p.loop_indices:
   vi=me.loops[li].vertex_index;v=me.vertices[vi].co;uv.data[li].uv=uvs[vi] if uvs else (v.x/.2663,v.y/.2663)
 CREATED.append(o);return o

def tube(name,points,radius,mat,sides=8,closed=False,layer='upperDetail'):
 vs=[];fs=[];uv=[];arclength=0
 for j,point in enumerate(points):
  p=Vector(point);p0=Vector(points[j-1 if j else (len(points)-1 if closed else 0)]);p1=Vector(points[(j+1)%len(points)] if closed or j<len(points)-1 else points[j]);t=p1-p0
  if t.length<1e-8:t=Vector((0,0,1))
  t.normalize();ref=Vector((1,0,0)) if abs(t.x)<.8 else Vector((0,1,0));a=t.cross(ref).normalized();b=t.cross(a).normalized()
  if j:arclength+=(p-p0).length
  r=radius(j/(len(points)-1)) if callable(radius) else radius
  for k in range(sides):
   v=p+r*(a*math.cos(k*math.tau/sides)+b*math.sin(k*math.tau/sides));vs.append(tuple(v));uv.append((k/sides*2*math.pi*r/.2663,arclength/.2663))
 for j in range(len(points) if closed else len(points)-1):
  for k in range(sides):fs.append((j*sides+k,j*sides+(k+1)%sides,((j+1)%len(points))*sides+(k+1)%sides,((j+1)%len(points))*sides+k))
 if not closed:fs.extend([tuple(reversed(range(sides))),tuple((len(points)-1)*sides+k for k in range(sides))])
 return mesh(name,vs,fs,mat,uv,layer)

def solid(o,thickness):
 m=o.modifiers.new('Physical cloth thickness','SOLIDIFY');m.thickness=thickness;m.offset=0;m.use_even_offset=False

def apply():
 global CREATED;CREATED=[];frame=S.frame_current;S.frame_set(1);bpy.context.view_layer.update()
 originals=[o for o in S.objects if original_scope(o)]
 stable=[o for o in S.objects if not original_scope(o) and not o.get(TAG) and not o.get('revision99_textiles_botanica')]
 before=fingerprints(stable);baseline=len(stable)
 for o in list(bpy.data.objects):
  if o.get(TAG) or o.get('revision99_textiles_botanica'):bpy.data.objects.remove(o,do_unlink=True)
 for me in list(bpy.data.meshes):
  if me.users==0 and me.name.startswith((PREFIX,'R7B | ')):bpy.data.meshes.remove(me)
 for m in list(bpy.data.materials):
  if m.get(TAG) and m.users==0:bpy.data.materials.remove(m)
 # The fixed supports are measured afresh; fail safely if the layout moved.
 mattress=bpy.data.objects['Cama dormitorio colchón'];ml,mh=bounds(mattress)
 assert np.allclose(ml,[14.957,-8.105,3.605],atol=.003) and np.allclose(mh,[16.683,-6.205,3.855],atol=.003),'Mattress moved: rebuild cloth cache against new support'
 blanket=textile('Manta tejido y caída','blanket',.22);pillow=textile('Funda almohada','pillow',.18);curtain=textile('Cortina tejido','curtain',.17)
 # CPU-simulated blanket against a rounded mattress, self collisions and placed head edge.
 c=json.load(open(os.path.join(ROOT,'scripts','assets','r8','blanket-drape-cache.json')));N,M=c['grid'];uv=[((i%(N+1))/N*2.06/.265708,(i//(N+1))/M*1.34/.2663) for i in range(len(c['vertices']))]
 # Closed light duvet: gravity-set lower fabric remains on the mattress; soft fill raises its upper face.
 base=np.array(c['vertices'],dtype=float)
 # Resolve the small difference between simulation proxy bevel and the exact existing mattress.
 ev=mattress.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();mv=[ev.matrix_world@v.co for v in m.vertices];mf=[tuple(p.vertices) for p in m.polygons];ev.to_mesh_clear();support=BVHTree.FromPolygons(mv,mf,all_triangles=False);projected=0;maximum_projection=0
 for i,p in enumerate(base):
  q,n,fi,d=support.find_nearest(Vector(p))
  if q is not None and (Vector(p)-q).dot(n)<.0008 and d<.04:
   delta=(q+n*.0012)-Vector(p);base[i]=q+n*.0012;projected+=1;maximum_projection=max(maximum_projection,delta.length)
 norm=np.zeros_like(base)
 for face in c['faces']:
  a,b,d=face[0],face[1],face[3];n=np.cross(base[b]-base[a],base[d]-base[a]);n=n/max(np.linalg.norm(n),1e-12)
  for k in face:norm[k]+=n
 norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-9);loft=[]
 for k,p in enumerate(base):
  u=(k%(N+1))/N;v=(k//(N+1))/M;edge=(max(0,math.sin(math.pi*u)*math.sin(math.pi*v)))**.48
  # Local compression follows the sewn return; the fill is 3–14 mm, not a floating offset surface.
  cushion=.011*math.exp(-(((u-.53)/.25)**2+((v-.35)/.30)**2))
  crease=.007*math.exp(-((u-(.28+.20*v))/.040)**2-((v-.35)/.31)**2)+.005*math.exp(-((u-(.78-.16*v))/.050)**2-((v-.48)/.25)**2)
  head_taper=.55+.45*(1-v);loft.append(.004+head_taper*max(0,.020*edge+cushion-crease))
 top=base+norm*np.array(loft)[:,None];num=len(base);closedv=top.tolist()+base.tolist();closedf=list(c['faces'])+[tuple(num+i for i in reversed(f)) for f in c['faces']]
 boundary=list(range(N+1))+[j*(N+1)+N for j in range(1,M+1)]+[M*(N+1)+i for i in range(N-1,-1,-1)]+[j*(N+1) for j in range(M-1,0,-1)]
 for a,b in zip(boundary,boundary[1:]+boundary[:1]):closedf.append((a,b,num+b,num+a))
 ob=mesh('Manta dormitorio | caída CPU',closedv,closedf,blanket,uv+uv);ob['fill_thickness_m']=[float(min(loft)),float(max(loft))];ob['support_projection_vertices']=projected;ob['maximum_support_projection_m']=maximum_projection;ob['cloth_method']=c['method'];ob['cloth_simulation_frames']=c['frames'];ob['placement_constraint']='Headward line held on mattress; gravity and self collision settle overhangs. Static evaluated mesh.'
 # Real hems track the actual evaluated cloth boundary; no free floating curve approximations.
 edges=[list(range(N+1)),[j*(N+1)+N for j in range(M+1)],list(range(M*(N+1),(M+1)*(N+1))),[j*(N+1) for j in range(M+1)]]
 for k,ids in enumerate(edges):tube('Manta | costura doble '+str(k),[((base[i]+top[i])*.5).tolist() for i in ids],.00065,blanket,6)
 textile_report={'blanket_bounds':[list(x) for x in bounds(ob)],'cpu_drape_seconds':c['seconds'],'blanket_fill_thickness_m':[float(min(loft)),float(max(loft))],'support_projection_vertices':projected,'maximum_support_projection_m':maximum_projection,'fixed_mattress_bounds':[ml.tolist(),mh.tolist()]}
 # Two sewn pillowcases: compressed underside, unequal loft, corner tension and an inset seam.
 for idx,cx in enumerate([15.384,16.256]):
  nx,ny=72,48;vs=[];fs=[];uv=[];cy=-6.64;rx=.366;ry=.219;ang=math.radians([-2.3,2.1][idx]);rot=Matrix.Rotation(ang,3,'Z');zcontact=float(mh[2])+.0015;phase=idx*1.7
  def point(u,v,side):
   x=rx*u*(1-.055*abs(v)**8);y=ry*v*(1-.055*abs(u)**8);full=max(0,(1-u*u)*(1-v*v))**.40
   # Creases radiate from pulled sewn corners, tapering toward the filled centre.
   crease=0
   for su,sv,strength in [(-1,-1,.011),(1,-1,.007),(-1,1,.008),(1,1,.013)]:
    along=(1-su*u)*.7+(1-sv*v)*.3;cross=(1-su*u)-(1-sv*v)*.52
    crease-=strength*math.exp(-(cross/.065)**2)*math.exp(-(along/.5)**2)
   loft=[.116,.132][idx]*(1+.065*u-.045*v)
   # Local compression lobes and diagonal seam tension, different on the two pillows.
   dent=.017*math.exp(-(((u-[-.40,.28][idx])/.31)**2+((v-[.38,-.35][idx])/.40)**2))
   tension=-.0035*math.exp(-((u+.52)/.12)**2-((v+.79)/.15)**2)-.0024*math.exp(-((u-.64)/.09)**2-((v-.75)/.18)**2)
   top=zcontact+.024+loft*full+(crease-dent+tension)*full**.7
   bottom=zcontact+.021*(1-min(1,full*1.65))**2
   zz=top if side==0 else bottom
   q=rot@Vector((x,y,0));return(cx+q.x,cy+q.y,zz)
  for side in [0,1]:
   for j in range(ny+1):
    v=-1+2*j/ny
    for i in range(nx+1):
     u=-1+2*i/nx;vs.append(point(u,v,side));uv.append((u*rx/.265708,v*ry/.2663))
  grid=(nx+1)*(ny+1)
  for side in [0,1]:
   for j in range(ny):
    for i in range(nx):
     a=side*grid+j*(nx+1)+i;f=(a,a+1,a+nx+2,a+nx+1);fs.append(f if side==0 else tuple(reversed(f)))
  perimeter=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
  for a,b in zip(perimeter,perimeter[1:]+perimeter[:1]):fs.append((a,b,grid+b,grid+a))
  separation=min(vs[k][2]-vs[grid+k][2] for k in range(grid));assert separation>.0029,('Pillow upper/lower shell inversion',idx,separation)
  po=mesh('Almohada '+str(idx+1)+' | funda relleno y compresión',vs,fs,pillow,uv);po['compressed_support_z']=zcontact;po['minimum_top_bottom_gap_m']=separation
  seam=[]
  for a in perimeter:
   p=np.array(vs[a]);p[2]-=.001;seam.append(p.tolist())
  tube('Almohada '+str(idx+1)+' | costura perimetral',seam,.0006,pillow,6,True)
 # Curtain folds follow seven existing carriers. Pinched heading, irregular paired pleats, sewn hems.
 for idx,(y0,y1) in enumerate([(-7.24,-6.72),(-8.38,-7.86)]):
  nx,ny=144,120;vs=[];fs=[];uv=[];fullheight=5.69-3.297
  def cp(u,t):
   seg=min(5,int(u*6));q=u*6-seg;amplitudes=[.026,.032,.022,.035,.027,.030];amp=amplitudes[(seg+idx*2)%6]
   # Same fixed carriers; between them each pleat opens and twists with depth.
   gather=math.sin(math.pi*q);shift=.13*math.sin(t*2.2+seg*.72)*t;wave=math.sin(math.tau*(q+shift))
   x=14.24+amp*(.20+.80*t**.22)*gather*wave+.0025*math.sin(7*t+seg)*t*gather
   y=y0+(y1-y0)*u+.003*math.sin(t*3+u*10)*math.sin(math.pi*u)*t
   z=5.69-fullheight*t+.004*t**4*math.sin(u*17+idx)
   return(x,y,z)
  for j in range(ny+1):
   t=j/ny
   for i in range(nx+1):u=i/nx;vs.append(cp(u,t));uv.append((u*.93/.265708,t*fullheight/.2663))
  for j in range(ny):
   for i in range(nx):a=j*(nx+1)+i;fs.append((a,a+1,a+nx+2,a+nx+1))
  cu=mesh('Cortina '+str(idx+1)+' | pliegues suspendidos',vs,fs,curtain,uv);solid(cu,.0006)
  for t,label in [(.012,'cabezal'),(.985,'dobladillo')]:tube('Cortina '+str(idx+1)+' | '+label,[cp(k/144,t) for k in range(145)],.00045,curtain,6)
  for k in range(7):
   y=y0+(y1-y0)*k/6;tube('Cortina '+str(idx+1)+' | cinta al carro '+str(k),[(14.24,y,5.682),(14.24,y,5.699)],.0025,curtain,8)
 textile_report['curtain_bottom_min_m']=min(bounds(o)[0][2] for o in CREATED if 'Cortina' in o.name)
 print('R7B textiles built',len(CREATED),flush=True)
 # Adult garments: tailored hollow torso, shoulder-supported sleeves, collars and differing hems.
 garment_rows=[];rod=bpy.data.objects['Vestidor barral'];rl,rh=bounds(rod);rod_y=(rl[1]+rh[1])/2;rod_z=(rl[2]+rh[2])/2
 wire=material('Perchas acero cepillado',(.34,.36,.38),.29,1);button=material('Botón mate',(.36,.34,.30),.4)
 angles=[2,-4,5,-3,0,5,-5];centres=[18.33,18.44,18.55,18.66,18.77,18.88,18.99]
 for idx,cx in enumerate(centres):
  start=len(CREATED);cy=float(rod_y);mat=textile('Prenda adulta '+str(idx),'garment'+str(idx),.20);hem=[4.25,4.32,4.27,4.34,4.26,4.31,4.245][idx];top=5.034;thickness=[.027,.032,.029,.032,.022,.030,.030][idx];angle=math.radians(angles[idx]);rot=Matrix.Rotation(angle,3,'Z');pivot=Vector((cx,cy,0));phase=idx*1.23
  def gp(x,y,z):return tuple(pivot+rot@Vector((x*(.75 if idx==4 else 1),y,z)))
  def surface(a,t):
   width=float(np.interp(t,[0,.075,.16,.43,.8,1],[.048,.207,.195,.178,.19,.184]));depth=thickness*(.66+.34*math.sin(math.pi*t/2))
   # Longitudinal folds descend from shoulder seams; shorter creases form near elbow/waist constraints.
   fold=.0055*math.sin(5*a+.8*math.sin(t*2)+phase)*math.sin(math.pi*t*.87)+.0024*math.sin(9*a-t*3+phase)*t
   x=(depth+fold)*math.sin(a)+.003*math.sin(t*4+phase)*t
   y=width*math.cos(a)+.007*math.sin(t*3.5+phase)*t
   z=top-(top-hem)*t+.006*math.cos(a*2+phase)*t*t
   z+=.012*math.exp(-((t-.42)/.18)**2)*math.sin(a*2+phase)
   return gp(x,y,z)
  vs=[];fs=[];uv=[];nr,nt=64,65;rings=[]
  for j in range(nt):
   t=j/(nt-1);r=[]
   for k in range(nr):a=k*math.tau/nr;p=surface(a,t);vs.append(p);r.append(p);uv.append((k/nr*.81/.265708,t*(top-hem)/.2663))
   rings.append(r)
  for j in range(nt-1):
   for k in range(nr):fs.append((j*nr+k,j*nr+(k+1)%nr,(j+1)*nr+(k+1)%nr,(j+1)*nr+k))
  body=mesh('Prenda '+str(idx)+' | torso tejido',vs,fs,mat,uv);solid(body,.00065);tube('Prenda '+str(idx)+' | bajo cosido',rings[-1],.00045,mat,6,True)
  # Collar stand and folded collar tips, actual hollow opening below the supported hook.
  pts=[gp(.012*math.sin(a),.047*math.cos(a),top+.011+.003*math.sin(a)) for a in np.linspace(0,math.tau,65)]
  tube('Prenda '+str(idx)+' | cuello',pts,.0030,mat,8,True)
  for sg in [-1,1]:
   verts=[gp(.016,sg*.023,top+.011),gp(.025,sg*.054,top-.010),gp(.029,sg*.043,top-.064),gp(.023,sg*.006,top-.019)]
   collar=mesh('Prenda '+str(idx)+' | solapa cuello '+str(sg),verts,[(0,1,2,3)],mat);solid(collar,.0009)
   # Sleeves hang in a slight elbow bend, remaining inside cabinet depth and their allotted X span.
   L=47;K=28;v=[];f=[];uv=[];sr=[];length=[.49,.42,.48,.39,.48,.46,.52][idx]
   for j in range(L):
    t=j/(L-1);yy=sg*(.163+.034*math.sin(t*2.0))+.006*math.sin(t*4+phase);zz=top-.057-length*t;xx=-.002+.008*math.sin(t*2.4+phase)
    ry=.032*(1-.42*t);rx=thickness*.73*(1-.18*t)
    ring=[]
    for k in range(K):
     a=k*math.tau/K;crease=.0025*math.sin(a*3+phase+t*8)*math.sin(math.pi*t)+.002*math.sin(t*24+sg)*math.exp(-((t-.48)/.15)**2)
     p=gp(xx+(rx+crease)*math.sin(a),yy+ry*math.cos(a),zz+.008*math.sin(a+phase)*math.sin(math.pi*t));v.append(p);ring.append(p);uv.append((k/K*.13/.265708,t*length/.2663))
    sr.append(ring)
   for j in range(L-1):
    for k in range(K):f.append((j*K+k,j*K+(k+1)%K,(j+1)*K+(k+1)%K,(j+1)*K+k))
   sleeve=mesh('Prenda '+str(idx)+' | manga '+str(sg),v,f,mat,uv);solid(sleeve,.00065);tube('Prenda '+str(idx)+' | puño '+str(sg),sr[-1],.00065,mat,6,True)
  # Placket follows the body surface; small stitches/buttons provide scale, not decoration floating off it.
  front=[surface(math.pi/2,t) for t in np.linspace(.09,.96,65)];tube('Prenda '+str(idx)+' | tapeta',front,.0010,mat,6)
  for t in np.linspace(.18,.84,6):
   p=Vector(surface(math.pi/2,t));n=rot@Vector((1,0,0));tube('Prenda '+str(idx)+' | botón '+str(round(t,2)),[p+n*.0008,p+n*.0020],.0028,button,10)
  hook_r=float((rh[2]-rl[2])/2)+.0015
  hook=[(cx,rod_y+hook_r*math.cos(a),rod_z+hook_r*math.sin(a)) for a in np.linspace(math.radians(-50),math.radians(220),45)]+[(cx,cy,rod_z-.027),(cx,cy,top+.009)]
  tube('Prenda '+str(idx)+' | gancho apoyado barral',hook,.0015,wire,8)
  shoulder=[gp(0,0,top+.009),gp(0,-.208,top-.058),gp(0,-.202,top-.066),gp(0,.202,top-.066),gp(0,.208,top-.058),gp(0,0,top+.009)]
  tube('Prenda '+str(idx)+' | percha hombros 420',shoulder,.0015,wire,8)
  bpy.context.view_layer.update();bb=[bounds(o) for o in CREATED[start:]];lo=np.min([b[0] for b in bb],axis=0);hi=np.max([b[1] for b in bb],axis=0)
  gaps=[]
  for panel in [o for o in S.objects if o.name.startswith('Vestidor lateral módulo')]:
   pl,ph=bounds(panel);gap=max(pl[0]-hi[0],lo[0]-ph[0]);gaps.append(gap)
  assert min(gaps)>.002,('Garment intersects wardrobe panel',idx,lo,hi,min(gaps))
  assert lo[1]>-6.740+.008 and hi[1]<-6.193-.008,('Garment depth',idx,lo,hi)
  assert lo[2]>3.653+.1 and hi[2]<5.297,('Garment shelf',idx)
  garment_rows.append({'garment':idx,'bounds':[lo.tolist(),hi.tolist()],'min_panel_clearance_m':min(gaps),'front_clearance_m':lo[1]+6.74,'back_clearance_m':-6.193-hi[1],'hanger_nominal_width_m':.420,'hanger_wire_outer_width_unrotated_m':.419,'hem_height_m':hem,'angle_degrees':angles[idx],'hook_contact_tolerance_m':1e-6})
 for a,b in zip(garment_rows,garment_rows[1:]):
  gap=b['bounds'][0][0]-a['bounds'][1][0];assert gap>.003,('Adjacent garment envelopes touch',a['garment'],b['garment'],gap);a['next_garment_clearance_m']=gap
 print('R7B garments built',len(CREATED),flush=True)
 # Four existing garden beds, authored species morphology at the established 0.50 x 0.48 m centres.
 build_garden()
 bpy.context.view_layer.update()
 # Original assets are hidden only after every replacement and clearance assertion has passed.
 for o in originals:o.hide_render=True;o.hide_set(True);o['r7b_replaced']=True
 after=fingerprints([bpy.data.objects[n] for n in before]);assert before==after,'Unrelated object geometry/transform/material/visibility changed'
 # No persistent modifier state, simulator or extra camera/light is introduced.
 assert all(o.type=='MESH' for o in CREATED)
 report={'input':bpy.data.filepath,'input_sha256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),'script':'scripts/correcciones99_textiles_botanica_r8.py','scope':'Textiles, seven adult garments, four garden-bed plants and soil only','status':'P / visual review pending; no formal score asserted','created_objects':len(CREATED),'created_mesh_vertices':sum(len(o.data.vertices) for o in CREATED),'hidden_replaced_objects':len(originals),'unrelated_objects_unchanged':baseline,'materials_photographic99':all(m.get('photographic99') for o in CREATED for m in o.data.materials),'uv0_on_every_mesh':all(o.data.uv_layers.get('UV0') is not None for o in CREATED),'textiles':textile_report,'garments':garment_rows,'garden':GARDEN_REPORT,'gpu_rendered':False,'saved_by_apply':False,'idempotent_rebuild':True}
 S.frame_set(frame);json.dump(report,open(os.path.join(OUT,'application-report.json'),'w'),ensure_ascii=False,indent=2);print('R8B_APPLIED',len(CREATED),baseline,flush=True);return report

GARDEN_REPORT=[]

def add_soil_photography(m):
 ns=m.node_tree.nodes;ls=m.node_tree.links;p=next(n for n in ns if n.type=='BSDF_PRINCIPLED');uv=ns.new('ShaderNodeUVMap');uv.uv_map='UV0';data=json.load(open(os.path.join(ROOT,'source','assets','brown_mud','provenance.json')))
 for item in data['files']:
  t=ns.new('ShaderNodeTexImage');t.image=image_load(os.path.join(ROOT,'source','assets','brown_mud',item['file']),item['channel']!='Diffuse');ls.new(uv.outputs['UV'],t.inputs['Vector'])
  if item['channel']=='Diffuse':ls.new(t.outputs['Color'],p.inputs['Base Color'])
  elif item['channel']=='Rough':ls.new(t.outputs['Color'],p.inputs['Roughness'])
  else:
   n=ns.new('ShaderNodeNormalMap');n.uv_map='UV0';n.inputs['Strength'].default_value=.35;ls.new(t.outputs['Color'],n.inputs['Color']);ls.new(n.outputs['Normal'],p.inputs['Normal'])
 m['source_asset']='Poly Haven Brown Mud, Rob Tuytel, CC0';m['texture_module_m']=1.299996018409729

def build_garden():
 global GARDEN_REPORT;GARDEN_REPORT=[]
 species=['lechuga de hoja','pimiento compacto','acelga','albahaca'];leaf_mats=[]
 for name,col,rough in [('lechuga',(.16,.30,.052),.54),('pimiento',(.028,.12,.027),.37),('acelga',(.048,.18,.046),.46),('albahaca',(.06,.21,.045),.44)]:
  m=material('Hoja '+name,col,rough);p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Subsurface Weight'].default_value=.06;p.inputs['Subsurface Radius'].default_value=(.0018,.0012,.0005);p.inputs['Coat Weight'].default_value=.06;p.inputs['Coat Roughness'].default_value=.42
  vc=m.node_tree.nodes.new('ShaderNodeVertexColor');vc.layer_name='R7B pigmento foliar';m.node_tree.links.new(vc.outputs['Color'],p.inputs['Base Color']);m['leaf_thickness_m']=.00028;m['species']=name;leaf_mats.append((m,col))
 vein_mats=[material('Nervio '+str(i),c,.48) for i,c in enumerate([(.24,.34,.095),(.12,.22,.05),(.31,.38,.17),(.17,.30,.074)])]
 stem_mats=[material('Tallo '+str(i),c,.52) for i,c in enumerate([(.26,.35,.12),(.065,.15,.035),(.36,.39,.20),(.08,.21,.04)])]
 fruit=material('Pimiento verde',(.045,.18,.024),.27);next(n for n in fruit.node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Coat Weight'].default_value=.17
 soil=material('Suelo franco y compost',(.095,.066,.042),.91);add_soil_photography(soil);aggregate=[material('Agregado suelo '+str(i),c,.88) for i,c in enumerate([(.07,.044,.026),(.13,.091,.052),(.095,.072,.048),(.16,.12,.076)])]
 # Physical relief is geometry at millimetre scale, not centimetre shader noise.
 for bi,(x0,yc) in enumerate([(2.09,-4.20),(5.09,-4.20),(2.09,-7.15),(5.09,-7.15)]):
  x1=x0+2.12;y0=yc-.485;y1=yc+.485;start=len(CREATED);rng=random.Random(9900+bi)
  centres=[(x0+.31+.5*i,yc+row*.24) for row in [-1,1] for i in range(4)]
  def soilz(x,y):
   # Tilled surface relief: aggregate-scale undulation plus shallow watering basins around each stem.
   fine=.0015*math.sin(x*161+y*91)*math.sin(y*131-x*29)+.0011*math.sin(x*283-y*251)
   broad=.003*math.sin(x*8+y*11)+.002*math.sin(x*21-y*13)
   basins=sum(-.004*math.exp(-(((x-cx)/.07)**2+((y-cy)/.07)**2)) for cx,cy in centres)
   return .270+fine+broad+basins
  nx,ny=212,97;vs=[];fs=[];uv=[]
  for j in range(ny+1):
   y=y0+(y1-y0)*j/ny
   for i in range(nx+1):x=x0+(x1-x0)*i/nx;vs.append((x,y,soilz(x,y)));uv.append((x/1.299996,y/1.299996))
  for j in range(ny):
   for i in range(nx):a=j*(nx+1)+i;fs.append((a,a+1,a+nx+2,a+nx+1))
  # Watertight substrate volume below the surface, preserving the original bottom elevation.
  edge=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
  baseid=len(vs)
  for vi in edge:x,y,z=vs[vi];vs.append((x,y,.05));uv.append((x/1.299996,y/1.299996))
  for k,a in enumerate(edge):b=edge[(k+1)%len(edge)];fs.append((a,baseid+k,baseid+(k+1)%len(edge),b))
  fs.append(tuple(reversed([baseid+k for k in range(len(edge))])))
  su=mesh('Huerta '+str(bi+1)+' | sustrato labrado',vs,fs,soil,uv,'garden');su['soil_relief_m']=.014;su['fixed_bed_inner_bounds']=[x0,x1,y0,y1]
  # Real small porous aggregates, 3–11 mm, sunk into soil; four material bins, batched geometry.
  bins=[([],[]) for _ in aggregate]
  for k in range(620):
   x=rng.uniform(x0+.018,x1-.018);y=rng.uniform(y0+.018,y1-.018);r=rng.uniform(.0015,.0055);z=soilz(x,y)-r*.28;verts,faces=bins[k%4];offset=len(verts)
   for j in range(5):
    a=math.tau*j/5;rr=r*(.85+.25*rng.random());verts.append((x+rr*math.cos(a),y+rr*math.sin(a),z))
   verts.append((x+r*.14,y-r*.12,z+r*.8));verts.append((x,y,z-r*.6))
   for j in range(5):faces.extend([(offset+j,offset+(j+1)%5,offset+5),(offset+(j+1)%5,offset+j,offset+6)])
  for k,(vs,fs) in enumerate(bins):mesh('Huerta '+str(bi+1)+' | agregados milimétricos '+str(k),vs,fs,aggregate[k],layer='garden',smooth=False)
  lm,basecol=leaf_mats[bi];vm=vein_mats[bi];sm=stem_mats[bi]
  allv=[];allf=[];alluv=[];allcolors=[];veinv=[];veinf=[];stemv=[];stemf=[];nleaves=0
  # Batch stems and leaf veins to avoid thousands of objects and preserve complete leaves in export.
  def branch(points,radius,target='stem',sides=6):
   vv,ff=(stemv,stemf) if target=='stem' else (veinv,veinf);base=len(vv)
   for j,p0 in enumerate(points):
    p=Vector(p0);a=Vector(points[max(0,j-1)]);b=Vector(points[min(len(points)-1,j+1)]);t=(b-a).normalized();ref=Vector((1,0,0)) if abs(t.x)<.8 else Vector((0,1,0));u=t.cross(ref).normalized();w=t.cross(u).normalized();rr=radius*(1-.72*j/max(1,len(points)-1))
    for k in range(sides):vv.append(tuple(p+rr*(u*math.cos(k*math.tau/sides)+w*math.sin(k*math.tau/sides))))
   for j in range(len(points)-1):
    for k in range(sides):ff.append((base+j*sides+k,base+j*sides+(k+1)%sides,base+(j+1)*sides+(k+1)%sides,base+(j+1)*sides+k))
  def leaf(base,az,L,W,rise,cup,phase,maturity=1,kind=None):
   nonlocal nleaves;nleaves+=1;kind=bi if kind is None else kind;N=56;K=24;base=Vector(base);direction=Vector((math.cos(az),math.sin(az),0));side=Vector((-math.sin(az),math.cos(az),0));offset=len(allv);mid=[]
   def point(t,s):
    profile=math.sin(math.pi*t)**(.40 if kind in [0,2] else .72);edge=1
    if kind==0:edge=1+.025*math.sin(9*math.pi*t+phase)+.009*math.sin(19*math.pi*t+phase)
    elif kind==2:edge=1+.022*math.sin(11*math.pi*t+phase)
    width=W*.5*profile*edge*(1+.085*math.sin(phase+2*t)*(1 if s>=0 else -1))
    # Blade midrib arch + gravity tip droop; cup produces genuine cross-section, not flat polygons.
    horizontal=L*t*(.94-.16*t);height=rise*math.sin(math.pi*t*.65)-L*.12*t*t
    if kind==0:
     horizontal=L*(t-.075*t*t);height=rise*math.sin(math.pi*t*.50)-L*.10*t**3
    elif kind==2:
     horizontal=L*t*(.78-.12*t);height=rise*math.sin(t*math.pi*.52)-L*.09*t*t
    z=height+cup*s*s*math.sin(math.pi*t)+s*width*.16*math.sin(phase+1.4*t)*t*t+.0014*math.cos(10*math.pi*t+abs(s)*3+phase)*abs(s)*math.sin(math.pi*t)
    # Minor corrugations connect to secondary veins, with restrained ruffled leaf margins.
    z+=L*.009*math.sin(t*math.pi*10+phase+abs(s)*4)*abs(s)**1.4*math.sin(math.pi*t)
    return base+direction*horizontal+side*(s*width)+Vector((0,0,z))
   for j in range(N+1):
    t=.002+.996*j/N;mid.append(tuple(point(t,0)+Vector((0,0,.0004))))
    for k in range(K+1):
     s=-1+2*k/K;p=point(t,s);allv.append(tuple(p));alluv.append((t*L,s*W*.5))
     vein=math.exp(-(s/.07)**2)*.20;young=(1-maturity)*.14;edgefade=.025*abs(s)
     allcolors.append(tuple(min(.8,c*(1+vein+young+edgefade)*(1+.05*math.sin(phase))) for c in basecol)+(1,))
   for j in range(N):
    for k in range(K):a=offset+j*(K+1)+k;allf.append((a,a+K+1,a+K+2,a+1))
   branch(mid,L*.0035,'vein',5)
   for vstart in [.18,.32,.46,.60,.74]:
    for sg in [-1,1]:
     pts=[tuple(point(vstart+.14*q,sg*.87*q)+Vector((0,0,.00045))) for q in np.linspace(0,1,8)];branch(pts,L*.0011,'vein',4)
  plant_rows=[]
  for pi,(cx,cy) in enumerate(centres):
   beforev=len(allv);z=soilz(cx,cy)-.006;origin=Vector((cx,cy,z));scale=[.94,.69,1.035,.85,.78,1.00,.92,.73][(pi+bi*3)%8];phase=pi*2.399+bi*.77
   if bi in [0,2]:
    # Phyllotactic rosettes: older leaves spread outward; younger blades remain upright inside.
    count=18 if bi==0 else 15
    for li in range(count):
     age=1-li/(count-1);az=phase+li*2.399963+.16*math.sin(li*1.37+pi)
     if bi==0:
      L=(.058+.12*age)*scale;W=(.055+.110*age)*scale;rise=(.085-.045*age)*scale;pet=.008+.014*age;stemrise=.009+.032*(1-age)
     else:
      L=(.11+.125*age)*scale;W=(.055+.080*age)*scale;rise=(.20-.075*age)*scale;pet=.030+.022*age;stemrise=.035+.045*age
     end=origin+Vector((math.cos(az)*pet,math.sin(az)*pet,stemrise));branch([origin,origin.lerp(end,.5)+Vector((0,0,.013)),end],.0035 if bi==2 else .0025)
     leaf(end,az,L,W,rise,.021 if bi==0 else .014,phase+li*.7,age)
   else:
    H=(.57+.12*rng.random()) if bi==1 else (.39+.13*rng.random());H*=scale
    nodes=[]
    for j in range(10):
     t=j/9;nodes.append(origin+Vector((.015*math.sin(t*3+phase)*t,.012*math.sin(t*4+phase)*t,H*t)))
    branch(nodes,.006 if bi==1 else .004)
    # Alternate pepper leaves; opposite decussate pairs for basil, progressively smaller near shoot tips.
    for nodeidx in range(2,9):
     nd=nodes[nodeidx];az=phase+nodeidx*(2.40 if bi==1 else math.pi*.5);t=nodeidx/9
     for sg in ([-1,1] if bi==3 else [1]):
      aa=az+(math.pi if sg<0 else 0);spread=(.055 if bi==1 else .05)*(1-.3*t);tip=nd+Vector((math.cos(aa)*spread,math.sin(aa)*spread,.014));branch([nd,tip],.002)
      leaf(tip,aa,(.13 if bi==1 else .078)*scale*(1-.28*t),(.069 if bi==1 else .048)*scale*(1-.15*t),.026,.004,phase+nodeidx+sg,t)
      # Lateral shoots rooted at real stem nodes, carrying leaves of decreasing maturity.
      if nodeidx in [2,3,4,5,6,7]:
       shoot=[nd,nd+Vector((math.cos(aa)*.08,math.sin(aa)*.08,.035)),nd+Vector((math.cos(aa)*.10,math.sin(aa)*.10,.095))];branch(shoot,.0027)
       for j in range(2):
        for ss in [-1,1]:leaf(shoot[j+1],aa+ss*1.0,(.096 if bi==1 else .062)*scale,.05 if bi==1 else .04,.025,.003,phase+j+ss,.55)
    if bi==1 and pi%3!=1:
     # Two immature fruits on a peduncle below the leaf canopy, not repeated unsupported balls.
     nd=nodes[4];center=nd+Vector((.034*math.cos(phase),.034*math.sin(phase),-.059));branch([nd,center+Vector((0,0,.052))],.0024)
     vs=[];fs=[];nr,nz=24,20
     for j in range(nz+1):
      t=j/nz;rad=.029*math.sin(math.pi*t)**.52*(1-.19*t)
      for k in range(nr):
       a=k*math.tau/nr;r=rad*(1+.13*math.cos(4*a));vs.append(tuple(center+Vector((r*math.cos(a),r*math.sin(a),.050-.091*t))))
     for j in range(nz):
      for k in range(nr):a=j*nr+k;fs.append((a,j*nr+(k+1)%nr,(j+1)*nr+(k+1)%nr,(j+1)*nr+k))
     mesh('Huerta '+str(bi+1)+' | fruto '+str(pi),vs,fs,fruit,layer='garden')
   pverts=np.array(allv[beforev:]);plant_rows.append({'centre_m':[cx,cy,z],'leaf_bounds':[pverts.min(0).tolist(),pverts.max(0).tolist()]})
  leaves=mesh('Huerta '+str(bi+1)+' | '+species[bi]+' hojas',allv,allf,lm,alluv,'garden');solid(leaves,.00028)
  col=leaves.data.color_attributes.new(name='R7B pigmento foliar',type='FLOAT_COLOR',domain='POINT');col.data.foreach_set('color',np.array(allcolors,dtype=np.float32).ravel());leaves['leaf_count']=nleaves;leaves['preserve_complete_leaves']=True
  mesh('Huerta '+str(bi+1)+' | nervaduras',veinv,veinf,vm,layer='garden');mesh('Huerta '+str(bi+1)+' | tallos pecíolos',stemv,stemf,sm,layer='garden')
  bpy.context.view_layer.update();bb=[bounds(o) for o in CREATED[start:] if 'sustrato' not in o.name and 'agregados' not in o.name];lo=np.min([b[0] for b in bb],axis=0);hi=np.max([b[1] for b in bb],axis=0)
  assert lo[0]>=x0-.003 and hi[0]<=x1+.003 and lo[1]>=y0-.003 and hi[1]<=y1+.003,('Plants extend into path/wood edge',bi,lo,hi,[x0,x1,y0,y1])
  GARDEN_REPORT.append({'bed':bi+1,'proposed_species':species[bi],'plant_count':8,'leaf_count':nleaves,'plant_spacing_m':[.50,.48],'unchanged_bed_inner_bounds_m':[x0,x1,y0,y1],'plant_bounds':[lo.tolist(),hi.tolist()],'plant_centres':plant_rows,'soil_particle_diameter_m':[.003,.011],'planting_status':'P — proposed maintained vegetable beds; no season/date asserted'})
  print('R7B garden',bi+1,nleaves,len(allv),flush=True)

if __name__=='__main__':
 R7B_REPORT=apply()






