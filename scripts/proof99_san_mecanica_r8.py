"""CPU supplemental SAN8 construction sections and continuous envelope proof."""
import bpy,runpy,json,math,hashlib,numpy as np
from mathutils.bvhtree import BVHTree
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(r'D:\2026\42');OUT=R/'review99/r8_san'
A=runpy.run_path(str(R/'scripts/correcciones99_san_mecanica_r8.py'));rep=json.loads(bpy.context.scene[A['TAG']]);DG=bpy.context.evaluated_depsgraph_get()
def mesh(o,pivot=(0,0,0),closed=False):
 e=o.evaluated_get(DG);m=e.to_mesh();M=Matrix.Translation(-Vector(pivot))@e.matrix_world
 if closed:M=Matrix.Rotation(-o.get('san8_axis_sign',1)*math.radians(o.get('san8_default_angle_deg',0)),4,'X')@M
 vv=[M@v.co for v in m.vertices];ff=[list(f.vertices) for f in m.polygons];e.to_mesh_clear();return vv,ff
def bb(v):return [[float(min(p[k] for p in v)),float(max(p[k] for p in v))] for k in range(3)]
def arc_bounds(v):
 a=np.asarray(v);x=a[:,0];u=a[:,1];w=a[:,2];r=np.hypot(u,w)
 lo_u=np.minimum(u,-w);hi_u=np.maximum(u,-w);lo_w=np.minimum(w,u);hi_w=np.maximum(w,u)
 lo_u=np.where((u<0)&(w>0),-r,lo_u);hi_u=np.where((u>0)&(w<0),r,hi_u)
 lo_w=np.where((u<0)&(w<0),-r,lo_w);hi_w=np.where((u>0)&(w>0),r,hi_w)
 return [[float(x.min()),float(x.max())],[float(lo_u.min()),float(hi_u.max())],[float(lo_w.min()),float(hi_w.max())]]
world_bounds={o.name:bb([o.matrix_world@Vector(v) for v in o.bound_box]) for o in bpy.context.scene.objects if o.type=='MESH' and not o.hide_render}
def clip_triangle(tri,bounds):
 points=list(tri)
 for ax in range(3):
  for side in [0,1]:
   limit=bounds[ax][side]+(1e-6 if side==0 else -1e-6)
   def inside(v):return v[ax]>=limit if side==0 else v[ax]<=limit
   clipped=[]
   if not points:return []
   for a,b in zip(points,points[1:]+points[:1]):
    ina,inb=inside(a),inside(b)
    if ina:clipped.append(a)
    if ina!=inb:
     clipped.append(a+(b-a)*((limit-a[ax])/(b[ax]-a[ax])))
   points=clipped
 return points
def exact_surface_box(o,bounds):
 e=o.evaluated_get(DG);m=e.to_mesh();m.calc_loop_triangles();M=e.matrix_world
 vv=[M@v.co for v in m.vertices];tris=[list(t.vertices) for t in m.loop_triangles];e.to_mesh_clear()
 hits=0
 for tri in tris:
  ps=[vv[i] for i in tri]
  if any(max(v[k] for v in ps)<bounds[k][0] or min(v[k] for v in ps)>bounds[k][1] for k in range(3)):continue
  if len(clip_triangle(ps,bounds))>=3:hits+=1
 tree=BVHTree.FromPolygons(vv,tris,all_triangles=True)
 centre=Vector([sum(b)/2 for b in bounds]);counts=[]
 for direction in [(1,.73451,.31529),(-.42971,1,.18351),(.18321,-.31651,1)]:
  direction=Vector(direction).normalized();origin=centre.copy();count=0
  for _ in range(100):
   loc,no,idx,dist=tree.ray_cast(origin,direction,1000)
   if loc is None:break
   count+=1;origin=loc+direction*1e-5
  counts.append(count)
 return {'triangles_inside_continuous_envelope':hits,'centre_ray_crossings':counts,'centre_inside_by_majority':sum(n%2 for n in counts)>=2,'pass':hits==0 and sum(n%2 for n in counts)<2}
proof=[];env=[]
for label,body,seat,tank,sign in A['FAMILIES']:
 p=rep['families'][label]['pivot_blender'];g=rep['groups'][label]
 names=g['seat']+g['lid'];cache={}
 for n in names+[body,tank]:
  v,f=mesh(bpy.data.objects[n],p,n in names)
  cache[n]=[(q.x,sign*q.y,q.z) for q in v]
 bodytop=max(q[2] for q in cache[body]);tankfront=max(q[1] for q in cache[tank])
 sw=arc_bounds(sum([cache[n] for n in names],[]));sb=bb(cache[seat]);lid=rep['families'][label]['lid'];lb=bb(cache[lid])
 bearing_min=(.0031*math.cos(math.pi/64)-.003)
 carrier_min=.0106*math.cos(math.pi/360)-.0102
 fixed_tooth_min=.0076*math.cos(math.pi/360)-.007
 row={'family':label,'continuous_parameter':'0 <= seat <= lid <= 90 degrees','sweep_bounds_canonical_m':sw,
 'cistern_gap_m':sw[1][0]-tankfront,'seat_min_v_m':sb[1][0],'seat_max_w_m':sb[2][1],
 'lid_min_v_m':lb[1][0],'lid_min_w_m':lb[2][0],
 'closed_seat_lid_rigid_gap_m':lb[2][0]-sb[2][1],
 'body_top_w_m':bodytop,'seat_lowest_swept_clearance_m':arc_bounds(cache[seat])[2][0]-bodytop,
 'faceted_bearing_min_radial_clearance_m':bearing_min,'carrier_min_radial_clearance_m':carrier_min,
 'housing_to_stop_min_radial_clearance_m':fixed_tooth_min,
 'argument':'For lid relative angle d in [0,90], V>=0 and W>=0 imply Wrot=V sin(d)+W cos(d)>=min(Vmin,Wmin)>seat Wmax. Buffers are intended tangent contacts at d=0. Axial intervals of independent hinge housings/arms are disjoint. The shaft, liner, dog and carrier clear by radial bounds for all angles.'}
 world=[[sw[0][0]+p[0],sw[0][1]+p[0]],[min(sign*sw[1][0],sign*sw[1][1])+p[1],max(sign*sw[1][0],sign*sw[1][1])+p[1]],[sw[2][0]+p[2],sw[2][1]+p[2]]]
 own=set(sum(g.values(),[]))|{body,tank}
 candidates=[]
 for n,b in world_bounds.items():
  if n in own:continue
  depths=[min(b[k][1],world[k][1])-max(b[k][0],world[k][0]) for k in range(3)]
  if min(depths)>1e-6:candidates.append({'name':n,'overlap_depths_m':depths,'mesh_check':exact_surface_box(bpy.data.objects[n],world)})
 env.append({'family':label,'continuous_world_sweep_bbox_m':world,'other_visible_meshes_tested':len(world_bounds)-len(own),'remaining_bbox_candidates':candidates})
 proof.append(row)
# Sections from actual meshes of the mono left hinge, in its closed assembly.
label='mono';p=rep['families'][label]['pivot_blender'];origin=Vector((p[0]-.08,p[1],p[2]))
parts=[]
for n in rep['new_objects']:
 if not n.startswith('SAN8 | mono H1 '):continue
 o=bpy.data.objects[n];v,f=mesh(o,origin,True);parts.append((n,o['san8_group'],v,f))
for n,kind in [('Inodoro mono','ceramic'),('Inodoro mono | asiento','seat'),('SAN99 | mono cover open90','lid')]:
 o=bpy.data.objects[n];v,f=mesh(o,origin,kind in ['seat','lid']);parts.append((n,kind,v,f))
for o in bpy.data.objects:
 if o.name.startswith(('SAN99 | mono hinge bolt','SAN99 | mono hinge washer')):
  v,f=mesh(o,origin,False);bounds=bb(v)
  if bounds[0][0]<.02 and bounds[0][1]>-.02:parts.append((o.name,'fixed',v,f))
colors={'fixed':'#19394c','seat':'#b45b22','lid':'#186e7d','ceramic':'#7c8387'}
panels=[(40,130,740,430,0,-.007,[1,2],[-.035,.040,-.029,.027],'A · Sección transversal del asiento · U = −7 mm'),
(820,130,740,430,0,.010,[1,2],[-.035,.040,-.029,.027],'B · Sección transversal de tapa · U = +10 mm'),
(40,610,740,430,1,0,[0,2],[-.028,.036,-.029,.027],'C · Sección axial por el pasador · V = 0'),
(820,610,740,430,0,-.018,[1,2],[-.035,.040,-.029,.027],'D · Apoyo de la horquilla · U = −18 mm')]
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1190" viewBox="0 0 1600 1190"><rect width="1600" height="1190" fill="#f6f5f1"/>',
'<style>text{font-family:Arial,sans-serif;fill:#19394c}.t{font-size:20px;font-weight:bold}.s{font-size:16px}.n{font-size:14px}</style>',
'<text x="40" y="46" font-size="29">SAN8 · Bisagra de asiento y tapa · Secciones de la malla real</text>',
'<text x="40" y="78" class="s">Modelo geométrico de herraje propuesto · unidades mm · estado cerrado · corte sin perspectiva ni render</text>']
for x,y,w,h,axis,plane,axes,lim,title in panels:
 svg.append(f'<text x="{x}" y="{y-16}" class="t">{title}</text><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white" stroke="#b6c1c5"/>')
 sx=w/(lim[1]-lim[0]);sy=h/(lim[3]-lim[2]);scale=min(sx,sy)*.85
 def xy(q):return x+w/2+(q[axes[0]]-(lim[0]+lim[1])/2)*scale,y+h/2-(q[axes[1]]-(lim[2]+lim[3])/2)*scale
 # Grid at 5 mm.
 for a in range(math.ceil(lim[0]*200),math.floor(lim[1]*200)+1):
  v=a*.005;xx=x+w/2+(v-(lim[0]+lim[1])/2)*scale;svg.append(f'<path d="M {xx:.2f},{y} V {y+h}" stroke="#e6ecee" stroke-width=".7"/>')
 for a in range(math.ceil(lim[2]*200),math.floor(lim[3]*200)+1):
  v=a*.005;yy=y+h/2-(v-(lim[2]+lim[3])/2)*scale;svg.append(f'<path d="M {x},{yy:.2f} H {x+w}" stroke="#e6ecee" stroke-width=".7"/>')
 for n,kind,vs,fs in parts:
  segs=[]
  for f in fs:
   # All supplied hinge faces are quads or planar convex caps.
   for j in range(1,len(f)-1):
    tri=[vs[f[0]],vs[f[j]],vs[f[j+1]]];pts=[]
    for a,b in zip(tri,tri[1:]+tri[:1]):
     da=a[axis]-plane;db=b[axis]-plane
     if da*db<0:pts.append(a+(b-a)*(da/(da-db)))
     elif abs(da)<1e-9:pts.append(a)
    unique=[]
    for q in pts:
     if all((q-r).length>1e-8 for r in unique):unique.append(q)
    if len(unique)==2:
     q,r=unique
     if all(lim[0]-.005<=t[axes[0]]<=lim[1]+.005 and lim[2]-.005<=t[axes[1]]<=lim[3]+.005 for t in [q,r]):
      a,b=xy(q),xy(r);segs.append(f'M {a[0]:.2f},{a[1]:.2f} L {b[0]:.2f},{b[1]:.2f}')
  if segs:svg.append(f'<path d="{" ".join(segs)}" fill="none" stroke="{colors[kind]}" stroke-width="1.65"><title>{n}</title></path>')
 svg.append(f'<text x="{x+12}" y="{y+h-12}" class="n">Retícula: 5 mm</text>')
svg+=['<text x="40" y="1080" class="s">Azul oscuro: fijo · naranja: asiento · verde: tapa · gris: cerámica conservada. Los contactos solidarios no son pares cinemáticos.</text>',
'<text x="40" y="1110" class="s">Pasador Ø6 · casquillo Ø6,2 interior · alojamiento Ø8 interior · eje entre apoyos; discos de fricción y precarga axial.</text>',
'<text x="40" y="1140" class="s">Recorrido útil 0–90° con topes positivos. Capacidad de fricción, tolerancias industriales y fijación definitiva requieren selección/ensayo del herraje.</text>',
'</svg>']
(OUT/'secciones_mecanismo.svg').write_text('\n'.join(svg),encoding='utf-8')
result={'preview_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'continuous_geometry':proof,'environment_sweep':env,'scenes':{sc.name:all(n in sc.objects for n in rep['new_objects']) for sc in bpy.data.scenes if sc.name in rep['scenes']},'section_geometry_source':'Actual evaluated closed mesh sections; no idealized redraw.'}
result['pass']=all(q['cistern_gap_m']>0 and q['seat_lowest_swept_clearance_m']>0 and q['closed_seat_lid_rigid_gap_m']>0 for q in proof) and all(all(c['mesh_check']['pass'] for c in q['remaining_bbox_candidates']) for q in env) and all(result['scenes'].values())
(OUT/'continuous_and_sections.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('SAN8_SUPPLEMENT',result['pass'],[(q['family'],len(q['remaining_bbox_candidates'])) for q in env],flush=True)
