import bpy,json,hashlib,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
def raw(o):
 e=o.evaluated_get(dg);m=e.to_mesh();m.calc_loop_triangles()
 v=np.array([e.matrix_world@p.co for p in m.vertices]);f=[list(p.vertices) for p in m.loop_triangles];e.to_mesh_clear();return v,f
def geo(o):
 v,f=raw(o);return v.min(0),v.max(0),BVHTree.FromPolygons([Vector(x) for x in v],f)
def area(p):
 if len(p)<3:return 0.0
 q=np.array(p,dtype=float);q-=q[0].copy()
 return float(abs(sum(q[i][0]*q[(i+1)%len(q)][1]-q[(i+1)%len(q)][0]*q[i][1] for i in range(len(q))))/2)
def clip(subject,cp):
 # Convex clip, orient counterclockwise
 cp=list(cp)
 if sum(cp[i][0]*cp[(i+1)%len(cp)][1]-cp[(i+1)%len(cp)][0]*cp[i][1] for i in range(len(cp)))<0:cp.reverse()
 out=list(subject)
 for i,a in enumerate(cp):
  b=cp[(i+1)%len(cp)];old=out;out=[]
  if not old:break
  def cross(p):return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
  for j,q in enumerate(old):
   p=old[j-1];ip=cross(p)>=-1e-10;iq=cross(q)>=-1e-10
   if iq!=ip:
    dp=cross(p);dq=cross(q);t=dp/(dp-dq);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
   if iq:out.append(tuple(q))
 return out
def plane_tris(o,x):
 v,f=raw(o);return [v[t][:,[1,2]] for t in f if max(abs(v[t][:,0]-x))<.00003]
def contact(a,b,x):
 aa=plane_tris(a,x);bb=plane_tris(b,x)
 return {'x_plane':x,'triangles_a':len(aa),'triangles_b':len(bb),'coplanar_overlap_m2':sum(area(clip(pa,pb)) for pa in aa for pb in bb)}
out={'source':bpy.data.filepath,'sha256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),'method':'Actual evaluated mesh coplanar side-face intersection area for tube/cartela/stringer. Vertical rays below timber/above knee void. Geometry only, no weld/fastener capacity certification.','stairs':[],'console':[]}
for i in range(1,19):
 wood=bpy.data.objects[f'Peldaño exterior {i}'];support=bpy.data.objects[f'Soporte peldaño {i}'];nose=bpy.data.objects[f'Nariz antideslizante peldaño {i}']
 wg,sg,ng=geo(wood),geo(support),geo(nose);a,b=wg[0],wg[1];z=(a[1]+b[1])/2
 r={'step':i,'wood_bottom':float(a[2]),'wood_top':float(b[2]),'support_top':float(sg[1][2]),'support_gap_m':float(a[2]-sg[1][2]),'nose_top':float(ng[1][2]),'nose_projection_m':float(ng[1][2]-b[2]),'contacts':[]}
 for side,tn,sn,tx,sx in [('exterior','exterior','Zanca exterior',13.0685,13.0625),('interior','interior','Zanca lado edificio',13.8915,13.8975)]:
  plate=bpy.data.objects[f'DIM95 | cartela peldaño {i} {tn}'];stringer=bpy.data.objects[sn]
  r['contacts'].append({'side':side,'tube_plate':contact(support,plate,tx),'plate_stringer':contact(plate,stringer,sx)})
 out['stairs'].append(r)
cons=[bpy.data.objects[n] for n in ['Consola estudio','Base consola estudio']]
gg=[geo(o) for o in cons]
for x in [18.19,18.35,18.55,18.72]:
 for z in [2.6,3.0,3.4]:
  hits=[]
  for o,g in zip(cons,gg):
   loc,_,_,_=g[2].ray_cast(Vector((x,-z,3.2501)),Vector((0,0,1)),1.5)
   if loc:hits.append({'object':o.name,'height':float(loc.z),'clearance_from_floor':float(loc.z)-3.25})
  out['console'].append({'x':x,'source_z':z,'first_surface_above_floor':min(hits,key=lambda r:r['height']) if hits else None})
json.dump(out,open(r'D:\2026\42\audit\integral95_02_r6h_bearing_knees.json','w',encoding='utf8'),ensure_ascii=False,indent=2,default=float)
print('SHA',out['sha256'])
print('STAIR',[(r['step'],round(r['support_gap_m']*1e3,5),round(r['nose_projection_m']*1e3,5),[(round(c['tube_plate']['coplanar_overlap_m2']*1e6,3),round(c['plate_stringer']['coplanar_overlap_m2']*1e6,3)) for c in r['contacts']]) for r in out['stairs']])
print('CONSOLE',out['console'])
