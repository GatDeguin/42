"""R6I visual evidence corrections: supported pillows, supple cover and usable inspection cameras."""
import bpy,os,math,ast,json,numpy as np
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
for m in bpy.data.materials:
 if m.name.startswith(('MAT95 | ','FIT95 | ')):M[m.name.split(' | ',1)[1]]=m
def cv(p):return Vector((p[0],-p[2],p[1]))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_materialidad.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['mesh','curve']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<fast>','exec'))
for o in list(S.objects):
 if o.name.startswith(('Cama dormitorio almohada ','MOB95 | costura funda almohada')):bpy.data.objects.remove(o,do_unlink=True)
for ii,cx in enumerate([15.384,16.256],1):
 vs=[];fs=[];N,K=80,54;cz=6.64
 for side in [1,-1]:
  for j in range(K+1):
   v=-1+2*j/K
   for k in range(N+1):
    u=-1+2*k/N;x=cx+.37*u*(1-.08*abs(v)**10);z=cz+.225*v*(1-.08*abs(u)**10)
    fullness=max(0,(1-u*u)*(1-v*v))**.34
    seam=3.880+.0014*math.sin(u*22+v*5+ii)*abs(v)**8
    if side==1:
     h=seam+.140*fullness
     # Small converging tension wrinkles and irregular soft crown, not parallel corrugations.
     h+=.0045*math.sin(34*u+8*v+ii)*math.exp(-((abs(v)-.78)/.20)**2)*max(0,1-u*u)
     h-=.009*math.exp(-((u-.18*ii)/.43)**2-((v+.1)/.38)**2)*fullness
     h+=.003*math.sin(u*5+v*2+ii)*fullness
    else:
     # Flat central contact patch at mattress top+3.855; rise only near sewn perimeter.
     edge=max(abs(u),abs(v));h=3.855+(.023+.0014*math.sin(u*22+v*5+ii)*abs(v)**8)*edge**10
    vs.append(cv([x,h,z]))
 grid=(N+1)*(K+1)
 for si in [0,1]:
  for j in range(K):
   for k in range(N):
    a=si*grid+j*(N+1)+k;f=(a,a+1,a+N+2,a+N+1);fs.append(f if si==0 else tuple(reversed(f)))
 edge=list(range(N+1))+[j*(N+1)+N for j in range(1,K+1)]+[K*(N+1)+k for k in range(N-1,-1,-1)]+[j*(N+1) for j in range(K-1,0,-1)]
 for a,b in zip(edge,edge[1:]+edge[:1]):fs.append((a,b,grid+b,grid+a))
 ob=mesh('Cama dormitorio almohada '+str(ii),vs,fs,'cotton95','INTERIORS')
 for p in ob.data.polygons:p.use_smooth=True
 pts=[[vs[a].x,vs[a].z,-vs[a].y] for a in edge[::3]];pts.append(pts[0]);curve('MOB95 | costura funda almohada',pts,.0008,'cotton95','INTERIORS')
# Existing drape retains its footprint; softened fold at upper edge and broad shallow wrinkles.
o=bpy.data.objects['Cama dormitorio manta'];bpy.context.view_layer.update();inv=o.matrix_world.inverted();o.data=o.data.copy()
def lift(x,z):
 side=max(0,(14.970-x)/.072,(x-16.675)/.063)
 foot=max(0,(z-8.072)/.073);fade=max(0,1-max(side,foot))
 return fade*(.015+.006*math.sin(x*5.3-z*3.7)*math.sin(z*4.1+x*.7)+.036*math.exp(-((z-7.105-.012*math.sin(x*5))/.080)**2))
for v in o.data.vertices:
 p=o.matrix_world@v.co;p.z+=lift(p.x,-p.y);v.co=inv@p
for md in o.modifiers:
 if md.type=='SOLIDIFY':md.thickness=.006
o.data.update()
for o in S.objects:
 if o.name.startswith('MOB95 | dobladillo manta') and o.type=='CURVE':
  for sp in o.data.splines:
   for b in sp.bezier_points:
    p=o.matrix_world@b.co;dz=lift(p.x,-p.y);b.co.z+=dz;b.handle_left.z+=dz;b.handle_right.z+=dz
def camera(name,p,target,lens,frame=1):
 o=bpy.data.objects.get(name)
 if not o:
  d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);COL['CAMERAS'].objects.link(o)
 o.location=cv(p);o.rotation_euler=(cv(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=lens;o.data.dof.use_dof=False;o.data.clip_start=.035;o['presentation_frame']=frame
camera('REV | Vestidor circulación',[18.52,4.86,8.60],[18.52,4.42,6.44],22)
camera('REV | Dormitorio completo',[17.12,4.86,8.54],[15.63,4.15,7.02],22)
bpy.data.objects['REV | Dormitorio acceso']['presentation_frame']=1
camera('REV | Baño mono',[20.50,1.82,5.60],[20.70,1.20,4.42],18,150)
camera('REV | Baño mono sanitarios',[20.62,1.80,4.98],[19.82,1.10,5.50],22,150)
S['r6i_visual_scope']='Pillow bottoms contact mattress at+3.855, loft~160mm; cover folds within unchanged footprint; wardrobe camera inside room; bedroom camera closed-door pose.'
S['review_iteration']='95 / R6I visual and dimensional candidate'
S.frame_set(1);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_95_R6I.blend'),compress=True);print('R6I_SAVED_NO_VIDEO',flush=True)
