"""R7 photographic refinement: sanitary silhouettes, metric tile PBR, PB camera.
Callable apply(); does not save or render. All dimensions are metres.
"""
import bpy,bmesh,json,math
from mathutils import Vector
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
TAG='sanitary_floor99_v2'
BODY=['Inodoro mono','Inodoro quincho','Inodoro vivienda']
SEAT=['Inodoro mono | asiento','Inodoro quincho | asiento','Inodoro suite | asiento']
TANK=['Inodoro mono | mochila compacta','Inodoro quincho | mochila compacta','Inodoro suite | mochila compacta']
CAM='REV | Baño mono'
def bounds(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();pts=[ev.matrix_world@v.co for v in me.vertices];ev.to_mesh_clear()
 return [[min(p[i] for p in pts),max(p[i] for p in pts)] for i in range(3)]
def metric_uv(o,period,indices=None):
 if o.data.users>1:o.data=o.data.copy()
 uv=o.data.uv_layers[0] if o.data.uv_layers else o.data.uv_layers.new(name='UVMap')
 uv.name='UVMap';o.data.uv_layers.active=uv;uv.active_render=True
 for p in o.data.polygons:
  if indices is not None and p.material_index not in indices:continue
  normal=o.matrix_world.to_3x3().inverted().transposed()@p.normal;axis=max(range(3),key=lambda k:abs(normal[k]));axes=[k for k in range(3) if k!=axis]
  for li in p.loop_indices:
   co=o.matrix_world@o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]]/period,co[axes[1]]/period)
 o['photographic99_uv_period_m']=period
def replace(o,verts,faces):
 mats=list(o.data.materials);inv=o.matrix_world.inverted();me=bpy.data.meshes.new(o.name+' | R7 smooth ceramic')
 me.from_pydata([inv@Vector(v) for v in verts],[],faces);me.update()
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 for m in mats:me.materials.append(m)
 o.data=me
 for p in me.polygons:p.use_smooth=True
 metric_uv(o,mats[0].get('texture_period_m',.05))
 o['sanitary99_refined']=True
def pchip_values(xs,ys,count):
 n=len(xs);h=[xs[i+1]-xs[i] for i in range(n-1)];delta=[(ys[i+1]-ys[i])/h[i] for i in range(n-1)];m=[delta[0]]+[0]*(n-2)+[delta[-1]]
 for i in range(1,n-1):
  if delta[i-1]*delta[i]>0:
   w1=2*h[i]+h[i-1];w2=h[i]+2*h[i-1];m[i]=(w1+w2)/(w1/delta[i-1]+w2/delta[i])
 values=[]
 for j in range(count):
  x=xs[0]+(xs[-1]-xs[0])*j/(count-1);i=min(n-2,next((k for k in range(n-1) if x<=xs[k+1]),n-2));t=(x-xs[i])/h[i]
  y=(2*t**3-3*t*t+1)*ys[i]+(t**3-2*t*t+t)*h[i]*m[i]+(-2*t**3+3*t*t)*ys[i+1]+(t**3-t*t)*h[i]*m[i+1]
  values.append((y,x))
 return values
def rings_mesh(cx,cy,rx,ry,z0,height,profile,power=1,n=192,closed=False,caps=False):
 verts=[];faces=[]
 for r,h in profile:
  for j in range(n):
   a=j*math.tau/n;c=math.cos(a);s=math.sin(a)
   verts.append((cx+rx*r*math.copysign(abs(c)**power,c),cy+ry*r*math.copysign(abs(s)**power,s),z0+height*h))
 for k in range(len(profile)-1):
  for j in range(n):q=(j+1)%n;faces.append((k*n+j,k*n+q,(k+1)*n+q,(k+1)*n+j))
 if closed:
  last=(len(profile)-1)*n
  for j in range(n):q=(j+1)%n;faces.append((last+j,last+q,q,j))
 if caps:
  for k,reverse in [(0,True),(len(profile)-1,False)]:
   center=len(verts);verts.append((cx,cy,z0+height*profile[k][1]))
   for j in range(n):q=(j+1)%n;face=(center,k*n+j,k*n+q);faces.append(tuple(reversed(face)) if reverse else face)
 return verts,faces
def profile_mesh(rows,n=192,closed=False,caps=False):
 verts=[];faces=[]
 for row in rows:
  cx,cy,rx,ry,z,power,clip=row
  for j in range(n):
   a=j*math.tau/n;c=math.cos(a);s=math.sin(a)
   x=cx+rx*math.copysign(abs(c)**power,c);y=cy+ry*math.copysign(abs(s)**power,s)
   if clip is not None:y=max(y,clip)
   verts.append((x,y,z))
 for k in range(len(rows)-1):
  for j in range(n):q=(j+1)%n;faces.append((k*n+j,k*n+q,(k+1)*n+q,(k+1)*n+j))
 if closed:
  k=(len(rows)-1)*n
  for j in range(n):q=(j+1)%n;faces.append((k+j,k+q,q,j))
 if caps:
  for k,reverse in [(0,True),(len(rows)-1,False)]:
   c=len(verts);verts.append((rows[k][0],rows[k][1],rows[k][4]))
   for j in range(n):
    q=(j+1)%n;face=(c,k*n+j,k*n+q);faces.append(tuple(reversed(face)) if reverse else face)
 return verts,faces
def body(o,seat_name):
 bb=bounds(o);sb=bounds(bpy.data.objects[seat_name]);cx=sum(bb[0])/2;cy=sum(bb[1])/2;rx=(bb[0][1]-bb[0][0])/2;ry=(bb[1][1]-bb[1][0])/2;z0=bb[2][0];height=bb[2][1]-z0
 front=-sb[1][1];mouth_cy=-(front+.230);rows=[]
 prof=pchip_values([0,.06,.14,.36,.64,.82,.92,.975],[.65,.671,.70,.78,.91,.98,1,1],45)
 for r,h in prof:rows.append((cx,cy,rx*r,ry*r,z0+height*h,.85,None))
 for j in range(1,9):
  a=math.pi/2*j/8;r=.985+.015*math.cos(a);h=.975+.025*math.sin(a);rows.append((cx,cy,rx*r,ry*r,z0+height*h,.85,None))
 rows.append((cx,mouth_cy,.145,.185,z0+height,1,None))
 for j in range(1,9):
  a=math.pi/2*j/8;rows.append((cx,mouth_cy,.145-.003*math.sin(a),.185-.003*math.sin(a),z0+height-.005*(1-math.cos(a)),1,None))
 # Bowl transitions to the preserved lower ceramic interface; no hydraulic performance claimed.
 low=z0+.02736364305
 for j in range(1,29):
  t=j/28;rows.append((cx,mouth_cy*(1-t)+cy*t,.142*(1-t)+rx*.60*t,.182*(1-t)+ry*.60*t,(z0+height-.005)*(1-t)+low*t,1*(1-t)+.85*t,None))
 vs,fs=profile_mesh(rows,caps=True);replace(o,vs,fs)
 return {'before':bb,'after':bounds(o),'radial_segments':192,'profile_rings':len(rows),'support_plane_m':z0,'outer_foot_radius_factor':.65,'bowl_opening_mm':[290,370],'mouth_source_center':[cx,z0+height,-mouth_cy],'seat_front_source_z':front}
def seat(o,body_name):
 bb=bounds(o);b=bounds(bpy.data.objects[body_name]);cx=sum(bb[0])/2;front=-bb[1][1];back=front+.445;cy=-(front+.235);inner_cy=-(front+.230);support=b[2][1];lo=support+.004;hi=support+.025;height=hi-lo
 rows=[(cx,cy,.190,.235,lo,1,-back),(cx,cy,.190,.235,lo+.74*height,1,-back)]
 for j in range(1,9):
  a=math.pi/2*j/8;dr=.003*(1-math.cos(a));rows.append((cx,cy,.190-dr,.235-dr,lo+height*(.74+.26*math.sin(a)),1,-back+dr))
 rows.append((cx,inner_cy,.128,.1655,hi,1,None))
 for j in range(1,9):
  a=math.pi/2*j/8;dr=.003*math.sin(a);rows.append((cx,inner_cy,.128-dr,.1655-dr,lo+height*(.74+.26*math.cos(a)),1,None))
 rows.append((cx,inner_cy,.125,.1625,lo,1,None));vs,fs=profile_mesh(rows,closed=True);replace(o,vs,fs)
 return {'before':bb,'after':bounds(o),'outer_mm':[380,445],'opening_mm':[250,325],'assembly_height_with_stops_mm':25,'plastic_thickness_mm':21,'front_source_z':front,'back_source_z':back,'support_plane_m':support,'radial_segments':192,'profile_rings':len(rows)}
def new_mesh(name,vs,fs,mat):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.materials.append(mat)
 o=bpy.data.objects.new('SAN99 | '+name,me);COL.objects.link(o)
 for p in me.polygons:p.use_smooth=True
 metric_uv(o,mat.get('texture_period_m',.05));o['sanitary99_detail']=True;return o
def box_detail(name,xx,yy,zz,mat,bevel=0):
 a,b=xx;c,d=yy;e,f=zz;vs=[(a,c,e),(b,c,e),(b,d,e),(a,d,e),(a,c,f),(b,c,f),(b,d,f),(a,d,f)];fs=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
 o=new_mesh(name,vs,fs,mat)
 if bevel:
  m=o.modifiers.new('Rounded manufactured edge','BEVEL');m.width=bevel;m.segments=4;m.harden_normals=True
  w=o.modifiers.new('Weighted planar normals','WEIGHTED_NORMAL');w.keep_sharp=True
 return o
def cyl_detail(name,a,b,r,mat,inner=None,n=48):
 a,b=Vector(a),Vector(b);t=(b-a).normalized();u=t.cross(Vector((1,0,0)) if abs(t.x)<.9 else Vector((0,1,0))).normalized();v=t.cross(u);vs=[];fs=[]
 specs=[(a,r),(b,r)] if inner is None else [(a,r),(b,r),(b,inner),(a,inner)]
 for p,rr in specs:vs.extend([p+rr*(u*math.cos(j*math.tau/n)+v*math.sin(j*math.tau/n)) for j in range(n)])
 for k in range(len(specs)-1):
  for j in range(n):q=(j+1)%n;fs.append((k*n+j,k*n+q,(k+1)*n+q,(k+1)*n+j))
 if inner is not None:
  for j in range(n):q=(j+1)%n;fs.append((3*n+j,3*n+q,q,j))
 else:fs.extend([tuple(range(n-1,-1,-1)),tuple(range(n,2*n))])
 return new_mesh(name,vs,fs,mat)
def boolean_cut(a,b):
 bpy.context.view_layer.objects.active=a;m=a.modifiers.new('Manufactured mounting bore','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=b;bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(b,do_unlink=True)
def details(index,report):
 body_o=bpy.data.objects[BODY[index]];seat_o=bpy.data.objects[SEAT[index]];tank=bpy.data.objects[TANK[index]];label=['mono','quincho','suite'][index]
 d=report['seats'][SEAT[index]];b=report['bodies'][BODY[index]];cx=sum(b['after'][0])/2;support=b['after'][2][1];front=d['front_source_z'];back=d['back_source_z'];hinge_z=back+.022;hinge_h=support+.026
 rubber=bpy.data.materials.get('LUZ99 | elastomero base sanitario') or bpy.data.materials.get('rubber95')
 if rubber is None:
  rubber=bpy.data.materials.new('SAN99 | rubber stops');rubber.use_nodes=True;bs=next(n for n in rubber.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(.12,.12,.11,1);bs.inputs['Roughness'].default_value=.75
 rubber['photographic99']=True
 chrome=bpy.data.materials.get('LUZ99 | cromado sanitario') or next(m for m in bpy.data.materials if m.get('source_material_key')=='stainless')
 uf=seat_o.data.materials[0]
 for x in [cx-.08,cx+.08]:
  for z in [front+.045,front+.42]:box_detail(label+' seat rubber stop',[x-.012,x+.012],[-z-.006,-z+.006],[support,support+.004],rubber,.001)
 tb=bounds(tank);tank_front=-tb[1][1];padz=tank_front+.055
 for x in [cx-.10,cx+.10]:box_detail(label+' tank support pad',[x-.01,x+.01],[-padz-.01,-padz+.01],[support,support+.005],rubber,.001)
 # Two mounting bores in the rear ceramic deck and160mm fixing centres.
 for x in [cx-.08,cx+.08]:
  cut=cyl_detail('TEMP hinge bore',(x,-hinge_z,support-.025),(x,-hinge_z,support+.006),.0045,chrome);boolean_cut(body_o,cut)
  cyl_detail(label+' hinge bolt',(x,-hinge_z,support-.015),(x,-hinge_z,support+.008),.004,chrome)
  cyl_detail(label+' hinge washer',(x,-hinge_z,support+.001),(x,-hinge_z,support+.004),.009,chrome,inner=.0045)
  cyl_detail(label+' hinge pedestal',(x,-hinge_z,support+.004),(x,-hinge_z,hinge_h),.006,chrome)
  cyl_detail(label+' hinge pin',(x-.019,-hinge_z,hinge_h),(x+.019,-hinge_z,hinge_h),.003,chrome)
  cyl_detail(label+' seat hinge sleeve',(x-.012,-hinge_z,hinge_h),(x+.002,-hinge_z,hinge_h),.007,chrome,inner=.0035)
  box_detail(label+' seat hinge arm',[x-.008,x+.004],[-hinge_z,-back+.004],[support+.021,support+.027],chrome,.001)
 # Matching closed cover, stored physically open90degrees; sweep remains ahead of tank.
 cy=-(front+.235);rows=[(cx,cy,.187,.232,support+.029,1,-back+.003),(cx,cy,.190,.235,support+.032,1,-back),(cx,cy,.190,.235,support+.040,1,-back),(cx,cy,.187,.232,support+.043,1,-back+.003)]
 vs,fs=profile_mesh(rows,caps=True);lid=new_mesh(label+' cover open90',vs,fs,uf)
 from mathutils import Matrix
 pivot=Vector((cx,-hinge_z,hinge_h));R=Matrix.Translation(pivot)@Matrix.Rotation(math.pi/2,4,'X')@Matrix.Translation(-pivot)
 lid.matrix_world=R;lid['hinge_source']=[cx,hinge_h,hinge_z];lid['opening_deg']=90;lid['closed_matrix']=json.dumps([v for row in Matrix.Identity(4) for v in row])
 for x in [cx-.08,cx+.08]:
  sleeve=cyl_detail(label+' cover hinge sleeve',(x+.004,-hinge_z,hinge_h),(x+.016,-hinge_z,hinge_h),.007,chrome,inner=.0035);sleeve.matrix_world=R
  arm=cyl_detail(label+' cover hinge arm',(x+.01,-hinge_z,hinge_h),(x+.01,-back,support+.035),.004,chrome);arm.matrix_world=R
 clearance=tank_front-(hinge_z+.017)
 return {'seat_to_tank_gap_m':tank_front-back,'hinge_centres_m':.160,'cover_angle_deg':90,'cover_sweep_plane_max_source_z':hinge_z+.017,'cover_cistern_min_plane_gap_m':clearance,'tank_support_thickness_m':.005,'seat_stops_m':.004,'lid':lid.name,'body_bores_mm':9,'external_drain_unchanged':True}

def tile_material():
 m=next(m for m in bpy.data.materials if m.get('source_material_key')=='tile')
 m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;n.clear();out=n.new('ShaderNodeOutputMaterial');bs=n.new('ShaderNodeBsdfPrincipled');l.new(bs.outputs['BSDF'],out.inputs['Surface'])
 bs.inputs['Base Color'].default_value=(.665,.642,.586,1);bs.inputs['Roughness'].default_value=.275;bs.inputs['IOR'].default_value=1.5;bs.inputs['Coat Weight'].default_value=.12;bs.inputs['Coat Roughness'].default_value=.19
 uv=n.new('ShaderNodeUVMap');uv.uv_map='UVMap'
 for suffix,socket,color in [('basecolor','Base Color','sRGB'),('roughness','Roughness','Non-Color'),('normal',None,'Non-Color')]:
  im=n.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(ROOT/'source/photographic99_pavimento'/('tile300_'+suffix+'.png')),check_existing=True);im.image.colorspace_settings.name=color;im.image.pack();im.interpolation='Linear';im.extension='REPEAT';l.new(uv.outputs['UV'],im.inputs['Vector'])
  if socket:l.new(im.outputs['Color'],bs.inputs[socket])
  else:
   normal=n.new('ShaderNodeNormalMap');normal.uv_map='UVMap';normal.inputs['Strength'].default_value=1;l.new(im.outputs['Color'],normal.inputs['Color']);l.new(normal.outputs['Normal'],bs.inputs['Normal'])
 m['photographic99']=True;m['texture_period_m']=1.2;m['tile300_pbr_spec']=json.dumps({'module_m':.3,'grout_width_m':.0035,'recess_m':.0006,'bevel_transition_m':.0008})
 users=[]
 for o in bpy.context.scene.objects:
  if o.type=='MESH' and not o.hide_render:
   indices={i for i,q in enumerate(o.data.materials) if q==m}
   if indices:metric_uv(o,1.2,indices);users.append(o.name)
 return {'material':m.name,'objects':users,'module_m':.3,'grout_m':.0035,'recess_m':.0006,'period_m':1.2,'uv_layer':'UVMap','pbr_exportable':True}
def reflect_world_objects(objects,mid_y):
 for o in objects:
  if o.type!='MESH':continue
  if o.data.users>1:o.data=o.data.copy()
  inv=o.matrix_world.inverted()
  for v in o.data.vertices:
   p=o.matrix_world@v.co;p.y=2*mid_y-p.y;v.co=inv@p
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
 bpy.context.view_layer.update()

def apply():
 global COL
 S=bpy.context.scene
 if S.get(TAG):return json.loads(S[TAG])
 COL=bpy.data.collections.get('SAN99 | sanitary details') or bpy.data.collections.new('SAN99 | sanitary details')
 if COL.name not in S.collection.children:S.collection.children.link(COL)
 S.frame_set(1);bpy.context.view_layer.update();report={'bodies':{},'seats':{},'tanks':{},'source':bpy.data.filepath}
 quincho_mid_y=sum(bounds(bpy.data.objects[BODY[1]])[1])/2
 reflect_world_objects([bpy.data.objects[q[1]] for q in [BODY,SEAT,TANK]],quincho_mid_y)
 for i,name in enumerate(BODY):
  report['bodies'][name]=body(bpy.data.objects[name],SEAT[i]);print('SAN99_BODY_READY',name,flush=True)
 for i,name in enumerate(SEAT):report['seats'][name]=seat(bpy.data.objects[name],BODY[i])
 for name in TANK:
  o=bpy.data.objects[name];before=bounds(o)
  if o.data.users>1:o.data=o.data.copy()
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
  i=TANK.index(name);support=report['bodies'][BODY[i]]['after'][2][1];lo=before[2][0];hi=before[2][1];inv=o.matrix_world.inverted()
  for v in o.data.vertices:
   q=o.matrix_world@v.co;q.z=support+.005+(q.z-lo)*(hi-support-.005)/(hi-lo);v.co=inv@q
  o.data.update()
  for m in o.modifiers:
   if m.type=='BEVEL':m.segments=12;m.harden_normals=True
  for p in o.data.polygons:p.use_smooth=True
  wn=o.modifiers.get('SAN99 weighted normals') or o.modifiers.new('SAN99 weighted normals','WEIGHTED_NORMAL');wn.keep_sharp=True;wn.weight=50
  bpy.context.view_layer.update();report['tanks'][name]={'before':before,'after':bounds(o),'bevel_segments':12,'smoothing':'Smooth faces and weighted planar normals'}
 for name,d in report['bodies'].items():
  d['max_bbox_delta_m']=max(abs(d['before'][i][j]-d['after'][i][j]) for i in range(3) for j in range(2));assert d['max_bbox_delta_m']<.00002,(name,d)
 for section in ['seats','tanks']:
  for name,d in report[section].items():d['bbox_delta_m']=[[d['after'][i][j]-d['before'][i][j] for j in range(2)] for i in range(3)]
 report['details']={BODY[i]:details(i,report) for i in range(3)}

 reflect_world_objects([bpy.data.objects[q[1]] for q in [BODY,SEAT,TANK]]+[o for o in S.objects if o.name.startswith('SAN99 | quincho ')],quincho_mid_y)
 for section,nm in [('bodies',BODY[1]),('seats',SEAT[1]),('tanks',TANK[1])]:
  d=report[section][nm]
  for field in ['before','after']:
   lo,hi=d[field][1];d[field][1]=[2*quincho_mid_y-hi,2*quincho_mid_y-lo]
  for field in ['seat_front_source_z','front_source_z','back_source_z']:
   if field in d:d[field]=(-2*quincho_mid_y)-d[field]
  d['faces_source_z']='increasing'
 d=report['details'][BODY[1]];d['mirror_mid_source_z']=-quincho_mid_y;d['cover_sweep_plane_min_source_z']=-2*quincho_mid_y-d.pop('cover_sweep_plane_max_source_z')
 for o in S.objects:
  if o.name.startswith('SAN99 | quincho ') and 'hinge_source' in o:
   q=list(o['hinge_source']);q[2]=-2*quincho_mid_y-q[2];o['hinge_source']=q;o['opening_axis_x_sign']=-1
 report['new_objects']=[o.name for o in S.objects if o.name.startswith('SAN99 |')]

 orphan=bpy.data.objects.get('Zócalo columna cocina')
 assert orphan is not None,'Expected authorized orphan plinth missing before patch'
 report['removed_orphan_plinth']={'name':orphan.name,'bbox_blender':bounds(orphan),'source_id':853,'signed_volume_m3':.047107013,'reason':'Orphan source plinth; no column above. Intersects original WC, current lower cabinet and another kitchen plinth. Removal individually authorized; current kitchen cabinets, countertop and fridge retained.'}
 bpy.data.objects.remove(orphan,do_unlink=True)
 report['tile']=tile_material()
 cam=bpy.data.objects[CAM];report['camera_before']={'positionBlender':list(cam.matrix_world.translation),'quaternionBlender':list(cam.matrix_world.to_quaternion()),'lens':cam.data.lens,'shift_y':cam.data.shift_y}
 p=(19.52,1.65,1.70);t=(20.8,1.65,.70);cam.location=(p[0],-p[2],p[1]);target=Vector((t[0],-t[2],t[1]));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=18;cam.data.shift_y=-.10;cam.data.sensor_fit='HORIZONTAL'
 cam['camera99_note']='Human eye height, level optical axis,18mm and lens shift: includes shower head, lavatory and drain in compact PB bathroom.'
 report['camera']={'name':CAM,'source_position':p,'source_target':t,'lens_mm':18,'shift_y':-.10,'presentation_frame':cam.get('presentation_frame',1)}
 report['interfaces']='Complete assembly plan extents, body footprint, floor support and BTH95 outlet/seals retained. Adult seat proportions and rear deck coordinated as a set. Generic fixture; not certified manufacturer geometry.'
 S[TAG]=json.dumps(report,ensure_ascii=False);bpy.context.view_layer.update();return report
