import bpy,os,json,math,numpy as np
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'review');os.makedirs(OUT,exist_ok=True)
S=bpy.context.scene;S.frame_set(150);bpy.context.view_layer.update()
mesh=[]
for o in S.objects:
 if o.type!='MESH' or o.hide_render or any(c.name in ['LANDSCAPE','REFERENCE'] for c in o.users_collection):continue
 if o.name.startswith(('Cielo ','Sky ')) or any(w in o.name.lower() for w in ['terreno','césped','camino acceso','calle cedro']):continue
 p=np.array([o.matrix_world@v.co for v in o.data.vertices])
 if len(p)==0:continue
 # source axes, with height as axis1.
 p=p[:,[0,2,1]]*np.array([1,1,-1]);lo=p.min(0);hi=p.max(0)
 if hi[0]<-1 or lo[0]>23 or hi[2]<-2 or lo[2]>21:continue
 o.data.calc_loop_triangles();tri=np.array([t.vertices for t in o.data.loop_triangles])
 mesh.append((o.name,p,tri,lo,hi))
sections=[('planta_baja','Planta baja | corte a +1,20 m',1,1.20,[0,2],[-1,23,-2,21]),('planta_alta','Planta alta | corte a +4,50 m',1,4.50,[0,2],[12,23,-1,14]),('corte_longitudinal','Corte longitudinal A-A | X = 18,00 m',0,18,[2,1],[-1,14,-.4,8.5]),('corte_estudio','Corte transversal B-B | Z fuente = 3,00 m',2,3,[0,1],[12,23,-.4,8.5]),('corte_escalera','Detalle de escalera C-C | X = 13,48 m',0,13.48,[2,1],[0,6.8,-.2,5.7])]
sections += [('detalle_alero_estudio','Alero del estudio | corte X = 17,80 m',0,17.8,[2,1],[-.35,1.45,6.30,7.55]),('detalle_cubierta_escalonada','Encuentro entre cubiertas | corte X = 17,80 m',0,17.8,[2,1],[5.45,6.65,7.20,8.45]),('plano_acustico','Tratamiento acústico | corte a +6,485 m',1,6.485,[0,2],[13.8,22.2,-.2,6.2]),('elevacion_escalera','Escalera | sección por zanca exterior X = 13,02 m',0,13.02,[2,1],[.5,6.6,-.2,4.6])]
drawings=[]
for key,title,axis,level,axes,extent in sections:
 lines=[];context=[]
 for name,p,tri,lo,hi in mesh:
  if key=='plano_acustico' and not name.startswith(('Bafle cielorraso','Cloud estudio','Cielorraso estudio')):continue
  if lo[axis]>level or hi[axis]<level:
   # Ground/upstairs floor furniture projections, only in the floor zone.
   if axis==1 and hi[1]<level and hi[1]>(.18 if level<2 else 3.22) and lo[1]<(2 if level<2 else 5.5):
    if any(t in name.lower() for t in ['losa','piso','losetas']):continue
    pts=p[tri];normal=np.cross(pts[:,1]-pts[:,0],pts[:,2]-pts[:,0]);lens=np.linalg.norm(normal,axis=1)
    keep=(normal[:,1]>lens*.93)&(lens>1e-8)
    # Skip mini objects in this scale.
    if max(hi[axes]-lo[axes])>.15:
     for t in pts[keep]:context.append(t[:,axes].tolist())
   continue
  for t in p[tri]:
   cross=[]
   for i in range(3):
    a,b=t[i],t[(i+1)%3];da,db=a[axis]-level,b[axis]-level
    if (da<0<=db) or (db<0<=da):
     if abs(da-db)>1e-9:cross.append((a+(b-a)*(da/(da-db)))[axes])
   if len(cross)==2 and np.linalg.norm(cross[0]-cross[1])>.00005:
    lines.append({'p':[x.tolist() for x in cross],'glass':any(x in name.lower() for x in ['vidrio','dvh']),'object':name})
 drawings.append({'key':key,'title':title,'axis':axis,'level':level,'axes':axes,'extent':extent,'lines':lines,'context':context})
json.dump(drawings,open(os.path.join(OUT,'drawing_geometry.json'),'w',encoding='utf8'),ensure_ascii=False)
print('DRAWINGS',[(d['key'],len(d['lines']),len(d['context'])) for d in drawings],flush=True)
