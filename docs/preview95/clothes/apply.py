"""Replace exactly seven wardrobe capsules in the loaded scene. Never saves a blend.
Coordinates are measured source metres. The original hook X positions are retained; adult garments fit the measured cabinet cavity;
wire hangers extend upward into the existing free space to contact the original rod.
"""
import bpy,math,os,json,hashlib,numpy as np
from mathutils import Vector,Matrix
ROOT=r'D:/2026/42';OUT=os.path.join(ROOT,'docs','preview95','clothes');S=bpy.context.scene
names=['Vestidor prenda '+str(i) for i in range(7)]
original=[bpy.data.objects[n] for n in names]
assert all(o.type=='MESH' for o in original),'Garment patch already applied or source changed'
cache={}
def fingerprint(o):
 h=hashlib.sha256(np.array(o.matrix_world,dtype=np.float64).tobytes());h.update(str([(s.material.name if s.material else None) for s in o.material_slots]).encode());h.update(str(o.hide_render).encode())
 if o.type=='MESH':
  key=o.data.as_pointer()
  if key not in cache:
   q=hashlib.sha256();a=np.empty(len(o.data.vertices)*3,np.float32);o.data.vertices.foreach_get('co',a);q.update(a.tobytes());a=np.empty(len(o.data.loops),np.int32);o.data.loops.foreach_get('vertex_index',a);q.update(a.tobytes());cache[key]=q.digest()
  h.update(cache[key])
 return h.hexdigest()
before={o.name:fingerprint(o) for o in S.objects if o.name not in names}
def bounds(o):
 return [[min((o.matrix_world@Vector(c))[i] for c in o.bound_box) for i in range(3)],[max((o.matrix_world@Vector(c))[i] for c in o.bound_box) for i in range(3)]]
def material(name,color,metal=0,rough=.8):
 m=bpy.data.materials.new(name);m.use_nodes=True;bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal;m.diffuse_color=(*color,1)
 if not metal:bs.inputs['Sheen Weight'].default_value=.22;bs.inputs['Sheen Roughness'].default_value=.6
 return m
metal=material('GAR95 | brushed wire hanger',(.32,.34,.35),1,.28)
colors=[(.54,.51,.43),(.075,.12,.16),(.40,.32,.23),(.24,.27,.23),(.53,.55,.50),(.11,.14,.19),(.42,.30,.24)]
mats=[material('GAR95 | woven garment '+str(i)+' | GarmentUV',c) for i,c in enumerate(colors)]
# Tiny textile weave uses source normal map with metric UVs, while silhouette/folds are geometry.
im=bpy.data.images.load(os.path.join(ROOT,'source','textures','clothWhite_normal.png'),check_existing=False);im.colorspace_settings.name='Non-Color'
for m in mats:
 n=m.node_tree.nodes;l=m.node_tree.links;tex=n.new('ShaderNodeTexImage');tex.image=im;uv=n.new('ShaderNodeUVMap');uv.uv_map='GarmentUV';l.new(uv.outputs['UV'],tex.inputs['Vector']);no=n.new('ShaderNodeNormalMap');no.uv_map='GarmentUV';no.inputs['Strength'].default_value=.14;l.new(tex.outputs['Color'],no.inputs['Color']);bs=next(x for x in n if x.type=='BSDF_PRINCIPLED');l.new(no.outputs['Normal'],bs.inputs['Normal']);m['photographic_garment']=True
created=[];rows=[]
def mesh_obj(name,verts,faces,mat,family,uvs=None):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);S.collection.objects.link(o);me.materials.append(mat);o.parent=family;o['source_layer']='upperDetail';o['garment_detail']=True
 uv=me.uv_layers.new(name='GarmentUV')
 for p in me.polygons:
  p.use_smooth=True
  for li in p.loop_indices:
   v=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(v.y/.12,v.z/.12)
 created.append(o);return o
def tube(name,points,radius,mat,family,closed=False):
 # Mesh tube avoids a dependency on curve conversion and retains exact contact geometry.
 verts=[];n=8
 for j,p in enumerate(points):
  p=Vector(p);t=Vector(points[(j+1)%len(points)])-Vector(points[j-1 if j else (len(points)-1 if closed else 0)])
  if t.length<1e-7:t=Vector((0,0,1))
  t.normalize();a=t.cross(Vector((1,0,0)));a.normalize();b=t.cross(a).normalized()
  for k in range(n):verts.append(tuple(p+radius*(a*math.cos(k*math.tau/n)+b*math.sin(k*math.tau/n))))
 faces=[]
 for j in range(len(points) if closed else len(points)-1):
  for k in range(n):faces.append((j*n+k,j*n+(k+1)%n,((j+1)%len(points))*n+(k+1)%n,((j+1)%len(points))*n+k))
 return mesh_obj(name,verts,faces,mat,family)
for idx,old in enumerate(original):
 lo,hi=bounds(old);cx=(lo[0]+hi[0])/2;cy=(lo[1]+hi[1])/2;family=bpy.data.objects.new(old.name+' replacement',None);S.collection.objects.link(family)
 for key in old.keys():family[key]=old[key]
 family['garment_replacement']=True;family['design_note']='Adult shirts and light jackets on 420 mm wire hangers, inside measured 547 mm wardrobe depth. Original hook X centres retained; all cabinet clearances checked.'
 start=len(created);mat=mats[idx];phase=idx*1.37;hem=4.285+[0,.021,.044,.015,.037,.055,.012][idx];top=hi[2]-.012
 # Hollow cloth shell with an open neck and hem. Cross-section is a soft, thin folded ellipse.
 verts=[];faces=[];N=40;M=33;rings=[]
 for j in range(M):
  t=j/(M-1);z=top-(top-hem)*t
  width=np.interp(t,[0,.065,.15,.35,1],[.051,.207,.198,.187,.195]);thick=np.interp(t,[0,.07,.4,1],[.007,.013,.012,.014])
  ring=[]
  for k in range(N):
   a=k*math.tau/N;u=width*math.cos(a);fold=(.0042*math.sin(5*a+1.4*t+phase)+.002*math.sin(11*a-3*t+phase))*(.25+.75*t)
   x=cx+(thick+fold)*math.sin(a)+.002*math.sin(7*t+phase)*t
   y=cy+u+.003*math.sin(4*t+phase)*t
   zz=z+.0035*math.cos(a*4+phase)*t*t
   verts.append((x,y,zz));ring.append((x,y,zz))
  rings.append(ring)
 for j in range(M-1):
  for k in range(N):faces.append((j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k))
 body=mesh_obj(old.name+' | cloth body',verts,faces,mat,family);solid=body.modifiers.new('Woven fabric thickness 0.8 mm','SOLIDIFY');solid.thickness=.0008;solid.offset=0
 tube(old.name+' | sewn hem',rings[-1],.0009,mat,family,True)
 tube(old.name+' | collar seam',rings[0],.0011,mat,family,True)
 # Two narrow long sleeves fold down beside the torso; open cuffs, shoulder gussets and wrist seams.
 for sign in [-1,1]:
  verts=[];faces=[];sleeve_rings=[];L=25;K=24
  length=.44+[.075,.005,0,.065,.025,.015,.08][idx]
  for j in range(L):
   t=j/(L-1);u=sign*(.177+.036*math.sin(t*1.4))+.007*math.sin(t*5+phase)*t;z=top-.048-length*t;rx=.0155*(1-.25*t);ry=.023*(1-.17*t);r=[]
   for k in range(K):
    a=k*math.tau/K;fold=.0025*math.sin(a*3+t*9+phase)*math.sin(math.pi*t)
    p=(cx+(rx+fold)*math.sin(a)+.005*math.sin(t*4+phase)*t,cy+u+ry*math.cos(a),z+.005*math.sin(a+phase)*math.sin(math.pi*t));verts.append(p);r.append(p)
   sleeve_rings.append(r)
  for j in range(L-1):
   for k in range(K):faces.append((j*K+k,j*K+(k+1)%K,(j+1)*K+(k+1)%K,(j+1)*K+k))
  sleeve=mesh_obj(old.name+' | sleeve '+str(sign),verts,faces,mat,family);mod=sleeve.modifiers.new('Woven fabric thickness 0.8 mm','SOLIDIFY');mod.thickness=.0008;mod.offset=0
  tube(old.name+' | cuff '+str(sign),sleeve_rings[-1],.001,mat,family,True)
 # Front placket seam follows the cloth and is 1 mm in diameter.
 line=[(cx+.017,cy+.006*math.sin(t*4+phase),top-.06-t*(top-hem-.07)) for t in np.linspace(0,1,35)]
 tube(old.name+' | placket stitching',line,.00065,mat,family)
 # 3 mm stainless wire hanger. Hook curls around the unmodified 22 mm diameter bar.
 rod=bpy.data.objects['Vestidor barral'];rl,rh=bounds(rod);rod_y=(rl[1]+rh[1])/2;rod_z=(rl[2]+rh[2])/2
 hook_r=(rh[2]-rl[2])/2+.0015;wire=.0015
 hook=[(cx,rod_y+hook_r*math.cos(a),rod_z+hook_r*math.sin(a)) for a in np.linspace(math.radians(-50),math.radians(220),45)]
 # End at the lower inner hook point, then neck and triangular shoulder support.
 neck=(cx,cy,top+.006)
 hook += [(cx,cy,rod_z-.027),neck]
 tube(old.name+' | hanger hook',hook,wire,metal,family)
 shoulder=[neck,(cx,cy-.210,top-.064),(cx,cy-.202,top-.072),(cx,cy+.202,top-.072),(cx,cy+.210,top-.064),neck]
 tube(old.name+' | hanger shoulders',shoulder,wire,metal,family)
 # Slight independent hanger/garment rotations retain each hook's support on the bar.
 angle=math.radians([3.5,-4,4.5,-3,.5,6,8][idx])
 pivot=Vector((cx,cy,0));rot=Matrix.Rotation(angle,3,'Z')
 for o in created[start:]:
  if 'hanger hook' not in o.name:
   for v in o.data.vertices:v.co=pivot+rot@(v.co-pivot)
 bpy.context.view_layer.update()
 # Inspect evaluated geometry, including cloth thickness, before removing source capsule.
 points=[]
 for o in created[start:]:
  ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());points.extend([o.matrix_world@Vector(c) for c in ev.bound_box])
 newlo=[min(v[k] for v in points) for k in range(3)];newhi=[max(v[k] for v in points) for k in range(3)]
 panels=[o for o in S.objects if o.name.startswith('Vestidor lateral módulo')]
 panel_clearances=[]
 for panel in panels:
  pl,ph=bounds(panel)
  gap=max(pl[0]-newhi[0],newlo[0]-ph[0]);assert gap>.002,(old.name,'Panel clearance',panel.name,gap)
  panel_clearances.append(gap)
 assert newlo[1]>-6.740+.010 and newhi[1]<-6.193-.025,'Cabinet depth clearance failed'
 assert newlo[2]>3.653+.1 and newhi[2]<5.297,'Shelf clearance failed'
 # Hanger top is tangent to the rod: radius rod + wire, inner surface equals rod surface.
 assert abs((rod_z+hook_r-wire)-rh[2])<1e-7
 name=old.name;bpy.data.objects.remove(old,do_unlink=True);family.name=name
 rows.append({'name':name,'sourceBounds':[lo,hi],'newBounds':[newlo,newhi],'originalHangerXRetained':True,'hangerRotationDegrees':math.degrees(angle),'minimumPanelClearanceMetres':min(panel_clearances),'garmentDepthMetres':newhi[1]-newlo[1],'garmentLengthMetres':top-hem,'hangerWidthMetres':.420,'cabinetDepthMetres':.547,'frontClearanceMetres':newlo[1]-(-6.740),'backClearanceMetres':-6.193-newhi[1],'rodTop':rh[2],'hookInnerTop':rod_z+hook_r-wire,'hookContactToleranceMetres':1e-7,'parts':len(created)-start,'hemZ':hem})
cache.clear();after={o.name:fingerprint(o) for o in S.objects if o.name in before};assert before==after,'Unrelated source geometry, transform or material changed'
report={'source':bpy.data.filepath,'sourceSHA256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),'garments':rows,'count':len(rows),'parts':len(created),'unrelatedObjectsUnchanged':len(before),'savedBlend':False,'sourceGeometryOutsideSevenGarmentsUnchanged':True,'originalHangerXRetained':True,'cabinetClearancePassed':True,'wireDiameterMetres':.003,'note':'Hook contact adds 0.1 m above the original disconnected capsules, below the unchanged shelf. Adult hanging silhouettes fit measured cabinet clearances.'}
json.dump(report,open(os.path.join(OUT,'application-report.json'),'w'),ensure_ascii=False,indent=2);print('GAR95_APPLIED',len(rows),len(created),len(before),flush=True)
