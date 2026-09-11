"""R8 SAN mechanical repair. apply() is idempotent; no save/render, no published patch edits.
Nominal custom friction hinge: independent seat/lid, positive0..90stops, no certified torque claim.
All local construction dimensions are metres.
"""
import bpy,bmesh,json,math
from mathutils import Matrix,Vector
TAG='san_mechanical_r8_v1'
PFX='SAN8 | '
FAMILIES=[('mono','Inodoro mono','Inodoro mono | asiento','Inodoro mono | mochila compacta',1),('quincho','Inodoro quincho','Inodoro quincho | asiento','Inodoro quincho | mochila compacta',-1),('suite','Inodoro vivienda','Inodoro suite | asiento','Inodoro suite | mochila compacta',1)]
REMOVE=['hinge pedestal','hinge pin','seat hinge sleeve','seat hinge arm','cover hinge sleeve','cover hinge arm']
COL=None

def matrix_rows(m):return [[float(v) for v in row] for row in m]
def bounds(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();ps=[ev.matrix_world@v.co for v in me.vertices];ev.to_mesh_clear()
 return [[min(v[k] for v in ps),max(v[k] for v in ps)] for k in range(3)]
def group(o,label,kind,pivot,sign,default=0):
 o['san8_family']=label;o['san8_group']=kind;o['san8_pivot']=pivot;o['san8_axis_sign']=sign;o['san8_default_angle_deg']=default;o['san8_default_matrix']=json.dumps(matrix_rows(o.matrix_world));return o
def make(name,vs,fs,material,frame,label,kind,pivot,sign):
 me=bpy.data.meshes.new(PFX+name);me.from_pydata(vs,[],fs);me.update()
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 me.materials.append(material)
 uv=me.uv_layers.new(name='UVMap');uv.active_render=True
 for poly in me.polygons:
  axes=[i for i in range(3) if i!=max(range(3),key=lambda k:abs(poly.normal[k]))]
  for li in poly.loop_indices:
   q=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(q[axes[0]]/.05,q[axes[1]]/.05)
 o=bpy.data.objects.new(PFX+name,me);COL.objects.link(o);o.matrix_world=frame
 o['san8_part']=True;o['photographic99_uv_period_m']=.05
 if kind=='lid':
  pv=Vector(pivot);o.matrix_world=Matrix.Translation(pv)@Matrix.Rotation(sign*math.pi/2,4,'X')@Matrix.Translation(-pv)@frame
 group(o,label,kind,pivot,sign,90 if kind=='lid' else 0)
 return o
def box(name,xx,yy,zz,*args):
 a,b=xx;c,d=yy;e,f=zz
 vs=[(a,c,e),(b,c,e),(b,d,e),(a,d,e),(a,c,f),(b,c,f),(b,d,f),(a,d,f)]
 fs=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
 return make(name,vs,fs,*args)
def ring(name,xx,ro,ri,*args,n=64,flat=None,outer_n=None):
 # Extruded along X; optional double-D bore for the fixed friction discs.
 a,b=xx;vs=[];fs=[]
 for x,r,isinner in [(a,ro,False),(b,ro,False),(b,ri,True),(a,ri,True)]:
  for j in range(n):
   t=math.tau*j/n;y=r*math.cos(t);z=r*math.sin(t)
   if outer_n and not isinner:
    rr=r*math.cos(math.pi/outer_n)/math.cos((t+math.pi/outer_n)%(math.tau/outer_n)-math.pi/outer_n);y=rr*math.cos(t);z=rr*math.sin(t)
   if flat is not None and isinner:y=max(-flat,min(flat,y))
   vs.append((x,y,z))
 for k in range(4):
  q=(k+1)%4
  for j in range(n):
   jj=(j+1)%n;fs.append((k*n+j,k*n+jj,q*n+jj,q*n+j))
 return make(name,vs,fs,*args)
def solid_cylinder(name,xx,r,*args,n=64,flat=None):
 a,b=xx;vs=[];fs=[]
 for x in [a,b]:
  for j in range(n):
   t=math.tau*j/n;y=r*math.cos(t);z=r*math.sin(t)
   if flat is not None:y=max(-flat,min(flat,y))
   vs.append((x,y,z))
 for j in range(n):q=(j+1)%n;fs.append((j,q,n+q,n+j))
 fs.extend([tuple(range(n-1,-1,-1)),tuple(range(n,2*n))])
 return make(name,vs,fs,*args)
def sector(name,xx,ri,ro,degrees,*args,step=2):
 a,b=xx;t0,t1=map(math.radians,degrees);n=max(2,math.ceil((degrees[1]-degrees[0])/step));vs=[];fs=[]
 for x,r in [(a,ri),(a,ro),(b,ro),(b,ri)]:
  for j in range(n+1):
   t=t0+(t1-t0)*j/n;vs.append((x,r*math.cos(t),r*math.sin(t)))
 q=n+1
 for k in range(4):
  kk=(k+1)%4
  for j in range(n):fs.append((k*q+j,k*q+j+1,kk*q+j+1,kk*q+j))
 fs.extend([(0,q,2*q,3*q),(n,3*q+n,2*q+n,q+n)])
 return make(name,vs,fs,*args)
def spring(name,xx,ro,ri,thick,*args,n=64):
 # Compressed coned disc: outer rim bears left, inner rim bears right.
 a,b=xx;vs=[];fs=[]
 for x,r in [(a,ro),(a+thick,ro),(b,ri),(b-thick,ri)]:
  for j in range(n):t=math.tau*j/n;vs.append((x,r*math.cos(t),r*math.sin(t)))
 for k in range(4):
  q=(k+1)%4
  for j in range(n):jj=(j+1)%n;fs.append((k*n+j,k*n+jj,q*n+jj,q*n+j))
 return make(name,vs,fs,*args)
def cylinder_z(name,zz,ro,ri,*args,n=64):
 a,b=zz;vs=[];fs=[]
 for z,r in [(a,ro),(b,ro),(b,ri),(a,ri)]:
  for j in range(n):t=math.tau*j/n;vs.append((r*math.cos(t),r*math.sin(t),z))
 for k in range(4):
  q=(k+1)%4
  for j in range(n):jj=(j+1)%n;fs.append((k*n+j,k*n+jj,q*n+jj,q*n+j))
 return make(name,vs,fs,*args)
def material(name,color,rough,metal=0):
 m=bpy.data.materials.get(name)
 if m is None:
  m=bpy.data.materials.new(name);m.use_nodes=True;bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal
 m['photographic99']=True;m['san8_material']=True;return m

def pose(label,seat_deg=0,lid_deg=90):
 if not (0<=seat_deg<=lid_deg<=90):raise ValueError('Useful motion requires 0 <= seat <= lid <= 90 degrees')
 for o in bpy.data.objects:
  if o.get('san8_family')!=label or o.get('san8_group') not in ['seat','lid']:continue
  deg=seat_deg if o['san8_group']=='seat' else lid_deg;delta=deg-o['san8_default_angle_deg'];M=Matrix(json.loads(o['san8_default_matrix']))
  if abs(delta)<1e-12:o.matrix_world=M
  else:
   pv=Vector(o['san8_pivot']);o.matrix_world=Matrix.Translation(pv)@Matrix.Rotation(o['san8_axis_sign']*math.radians(delta),4,'X')@Matrix.Translation(-pv)@M
 bpy.context.view_layer.update()

def apply():
 global COL
 S=bpy.context.scene
 if S.get(TAG):
  report=json.loads(S[TAG]);assert all(n in bpy.data.objects for n in report['new_objects']);return report
 assert S.get('sanitary_floor99_v2'),'Apply after the existing SAN99 assembly'
 original=json.loads(S['sanitary_floor99_v2'])
 for label,body,seat,tank,sign in FAMILIES:
  assert all(n in bpy.data.objects for n in [body,seat,tank,'SAN99 | '+label+' cover open90'])
 targets=[o for o in bpy.data.objects if any(o.name.startswith('SAN99 | '+label+' '+stem) for label,*_ in FAMILIES for stem in REMOVE)]
 assert len(targets)==36,[(o.name) for o in targets]
 relevant_scenes=[sc for sc in bpy.data.scenes if 'Inodoro mono' in sc.objects]
 COL=bpy.data.collections.new('SAN8 | mechanism repair')
 for sc in relevant_scenes:sc.collection.children.link(COL)
 report={'version':TAG,'replaces':[o.name for o in targets],'families':{},'scenes':[sc.name for sc in relevant_scenes],'source_file':bpy.data.filepath}
 for o in targets:bpy.data.objects.remove(o,do_unlink=True)
 chrome=bpy.data.materials.get('LUZ99 | cromado sanitario') or next(m for m in bpy.data.materials if m.get('source_material_key')=='stainless')
 liner=material('SAN8 | bearing polymer',(.13,.135,.13),.55)
 friction=material('SAN8 | friction composite',(.10,.09,.075),.68)
 rubber=bpy.data.materials.get('SAN99 | rubber stops') or material('SAN8 | elastomer',(.12,.12,.11),.75)
 for label,body_name,seat_name,tank_name,sign in FAMILIES:
  body=bpy.data.objects[body_name];seat_obj=bpy.data.objects[seat_name];lid=bpy.data.objects['SAN99 | '+label+' cover open90']
  hp=list(lid['hinge_source']);pivot=[hp[0],-hp[2],hp[1]];support=hp[1]-.026
  group(seat_obj,label,'seat',pivot,sign,0);group(lid,label,'lid',pivot,sign,90)
  for o in list(bpy.data.objects):
   if o.name.startswith('SAN99 | '+label+' seat rubber stop'):group(o,label,'seat',pivot,sign,0)
   elif o.name.startswith('SAN99 | '+label+' '):group(o,label,'fixed',pivot,sign,0)
  # Restore lid group after the broad fixed-family registration.
  group(lid,label,'lid',pivot,sign,90)
  for hi,x in enumerate([hp[0]-.08,hp[0]+.08]):
   origin=Vector((x,pivot[1],pivot[2]));frame=Matrix.Translation(origin)@Matrix.Rotation(0 if sign==1 else math.pi,4,'Z')
   prefix=label+' H'+str(hi+1)+' '
   fixed=(chrome,frame,label,'fixed',pivot,sign)
   fixed_f=(friction,frame,label,'fixed',pivot,sign)
   # Cast yoke stands on the existing mounting washer, clear below the rotor sweep.
   box(prefix+'base yoke',[-.022,.026],[-.007,.007],[-.022,-.018],*fixed)
   for side,ab in [('L',[-.022,-.014]),('R',[.018,.026])]:
    ring(prefix+'ear '+side,ab,.008,.0031,*fixed,flat=.00245)
    box(prefix+'ear stem '+side,ab,[-.008,.008],[-.020,-.004],*fixed)
   # A thin elastomer gasket closes the1mm original washer-to-ceramic gap.
   cylinder_z(prefix+'anchor gasket',[-.026,-.025],.009,.0045,rubber,frame,label,'fixed',pivot,sign)
   # Double-D nominal shaft and keyed axial friction discs; housing bore stays circular.
   solid_cylinder(prefix+'axle doubleD',[-.023,.026],.003,*fixed,flat=.0024)
   solid_cylinder(prefix+'axle thread blank M6',[.026,.034],.003,*fixed)
   solid_cylinder(prefix+'axle head',[-.026,-.022],.01/math.sqrt(3),*fixed,n=6)
   ring(prefix+'clamp washer',[.026,.027],.0055,.00305,*fixed)
   ring(prefix+'clamp nut M6 nominal',[.027,.032],.01/math.sqrt(3),.00255,*fixed,n=96,outer_n=6)
   spring(prefix+'preload coned spring',[-.014,-.012],.0075,.0031,.00045,*fixed)
   ring(prefix+'friction centre',[.002,.004],.0075,.0031,*fixed_f,flat=.00245)
   ring(prefix+'friction outer',[.016,.018],.0075,.0031,*fixed_f,flat=.00245)
   for kind,ab,armx,armz,stopx in [('seat',[-.012,.002],[-.010,0],[-.005,.001],[-.011,-.003]),('lid',[.004,.016],[.006,.014],[.003,.011],[.007,.013])]:
    moving=(chrome,frame,label,kind,pivot,sign)
    ring(prefix+kind+' housing',ab,.007,.004,*moving)
    ring(prefix+kind+' bearing',ab,.004,.0031,liner,frame,label,kind,pivot,sign)
    box(prefix+kind+' arm',armx,[.0045,.030],armz,*moving)
    sector(prefix+kind+' dog',stopx,.0067,.0102,[180,190],*moving,step=1)
    sector(prefix+kind+' stop carrier',stopx,.0106,.0125,[165,295],*fixed,step=1)
    sector(prefix+kind+' stop0',stopx,.0076,.0106,[170,180],*fixed,step=1)
    sector(prefix+kind+' stop90',stopx,.0076,.0106,[280,290],*fixed,step=1)
    box(prefix+kind+' stop stand',stopx,[-.004,.004],[-.018,-.0122],*fixed)
  # Four lid buffers: closed lid rests on the unchanged seat, separated4mm.
  front=original['seats'][seat_name]['front_source_z']
  if sign==-1:
   # The R7 report already stores the actual increasing-Z front.
   dist=lambda dz:front-dz
  else:dist=lambda dz:front+dz
  family_frame=Matrix.Translation(Vector(pivot))@Matrix.Rotation(0 if sign==1 else math.pi,4,'Z')
  for i,u in enumerate([-.10,.10]):
   for j,dz in enumerate([.09,.36]):
    worldz=dist(dz);v=((-worldz)-pivot[1])/sign
    box(label+' lid buffer '+str(i)+str(j),[u-.007,u+.007],[v-.005,v+.005],[-.001,.003],rubber,family_frame,label,'lid',pivot,sign)
  report['families'][label]={'body':body_name,'seat':seat_name,'lid':lid.name,'cistern':tank_name,'pivot_blender':pivot,'axis_sign':sign,'mount_centres_mm':160,'seat_range_deg':[0,90],'lid_range_deg':[0,90],'coupled_rule':'0 <= seat <= lid <= 90','bearing_radial_clearance_mm':.1,'faceted_bearing_min_radial_clearance_mm':(.0031*math.cos(math.pi/64)-.003)*1000,'head_and_nut_across_flats_mm':10,'axle_anti_rotation':'Double-D shaft in matching fixed yoke bores; clamped by hex head and nut; round M6 nominal threaded blank beyond right ear','stop_radial_clearance_mm':.4,'housing_to_stop_radial_clearance_mm':.6,'friction_retention':'Axial keyed composite discs with represented coned preload washer and clamp nut; torque capacity is not certified.','stop_definition':'Rotor dog 180–190 degrees sweeps inside sector 180–280 degrees; fixed stops bound 0 and 90 degrees.','presentation_pose':{'seat':0,'lid':90}}
 report['new_objects']=[o.name for o in COL.objects]
 report['groups']={label:{kind:[o.name for o in bpy.data.objects if o.get('san8_family')==label and o.get('san8_group')==kind] for kind in ['fixed','seat','lid']} for label,*_ in FAMILIES}
 report['same_group_contacts']='Cast/welded yoke members, sleeve/arm/dog assemblies, sleeve/liner interference-free press fit, and nominal threaded/clamped fixed members are explicitly solidary.'
 report['main_geometry_unchanged']=[q for _,b,s,t,_ in FAMILIES for q in [b,s,t]]+['SAN99 | '+q[0]+' cover open90' for q in FAMILIES]
 for sc in relevant_scenes:sc[TAG]=json.dumps(report,ensure_ascii=False)
 bpy.context.view_layer.update();return report
