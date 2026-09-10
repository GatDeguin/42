import bpy, math, json, os
from mathutils import Vector,Matrix
def setup_doors(g):
 D,O,cv,empty,box,COL=g['DATA'],g['OBJS'],g['cv'],g['empty'],g['box'],g['COL']
 rigs={}
 def reparent(o,rig):
  o.parent=rig;o.matrix_parent_inverse=Matrix.Translation(-rig.location)
 def rig(key,pos,parts,angle=None,move=None):
  e=empty('DOOR | '+key,pos,'DOORS');e['open']=0.0;e.id_properties_ui('open').update(min=0,max=1,description='0 closed / 1 open')
  e['motion']='hinge' if angle is not None else 'slide'
  for o in parts:reparent(o,e)
  if angle is not None:
   dr=e.driver_add('rotation_euler',2).driver;dr.expression='opening * '+str(angle)
  else:
   delta=cv(move);axis=max(range(3),key=lambda j:abs(delta[j]));dr=e.driver_add('location',axis).driver;dr.expression=str(e.location[axis])+' + opening * '+str(delta[axis])
  v=dr.variables.new();v.name='opening';v.type='SINGLE_PROP';v.targets[0].id=e;v.targets[0].data_path='["open"]'
  for fr,val in [(1,0),(30,0),(105,1),(1400,1),(1480,0)]:
   e['open']=val;e.keyframe_insert(data_path='["open"]',frame=fr)
  e['open']=0;rigs[key]=e
  return e
 for key in ['studio','suiteEntry','bedroomLink','bathLink','poolBath']:
  ids=D['doors'][key];main=D['meshes'][ids[0]];parts=[O[i] for i in ids+main['userData'].get('linkedMeshes',[]) if i in O]
  spec=D['doorSpecs'].get(key,{'pivot':[13.97,5.76],'angle':-math.pi*.52})
  rig(key,[spec['pivot'][0],main['position'][1]-main['scale'][1]/2,spec['pivot'][1]],parts,angle=spec['angle'])
 for side,idx in zip([-1,1],D['doors']['mono']):
  m=D['meshes'][idx];prefix=m['name'].replace(' vidrio','')
  parts=[O[mm['id']] for mm in D['meshes'] if mm['name'].startswith(prefix) and 'alféizar' not in mm['name'] and mm['id'] in O]
  rig('mono_'+('L' if side<0 else 'R'),[m['position'][0],.21,m['position'][2]],parts,move=[side*.78,0,0])
 # Side panels use real parallel tracks: A slides over B, opening the left bay completely.
 idx=D['doors']['balconySide'][0];m=D['meshes'][idx];prefix='Corrediza lateral A'
 parts=[O[mm['id']] for mm in D['meshes'] if mm['name'].startswith(prefix) and 'alféizar' not in mm['name'] and mm['id'] in O]
 for o in parts:o.location.x-=.035
 rig('balconySide',[13.95,3.22,9.75],parts,move=[0,0,1.20])
 # Split each rear DVH bay into fixed and sliding leaves, retaining the exact glazed extents and thickness.
 for label,idx in zip(['A','B'],D['doors']['balconyRear']):
  m=D['meshes'][idx];cx,cy,z=m['position'];width=m['scale'][0];height=m['scale'][1];parts=[]
  for i in [idx]+m['userData'].get('linkedMeshes',[]):
   o=O[i];o.scale.x*=.5;o.location.x-=width*.25;o['detail']='Original rear DVH split into two parallel sliding leaves within the source bay.'
   fixed=o.copy();fixed.data=o.data;fixed.name=o.name+' | paño fijo';COL['UPPER_FLOOR'].objects.link(fixed);fixed.location.x+=width*.5;fixed.location.y-=.035
   parts.append(o)
  lx=cx-width*.25;w=width/2
  for xx,yy,ww,hh in [(lx,cy+height/2,w,.045),(lx,cy-height/2,w,.045),(lx-w/2,cy,.04,height),(lx+w/2,cy,.04,height)]:
   parts.append(box('Hoja posterior '+label+' | perfil móvil',[xx,yy,z-.035],[ww,hh,.045],'blackMetal','DOORS',.002))
  parts.append(box('Hoja posterior '+label+' | tirador',[lx+w/2-.10,4.43,z-.08],[.025,.27,.025],'stainless','DOORS',.003))
  rig('balconyRear_'+label,[lx,3.22,z],parts,move=[width/2,0,0])
 bathroom=next((o for o in O.values() if o.name=='Baño mono puerta'),None)
 if bathroom:
  handle=box('Baño mono | manija',[20.07,1.22,4.24],[.12,.024,.032],'stainless','DOORS',.002)
  rig('bathroomMono',[19.46,.21,4.28],[bathroom,handle],angle=math.pi*.51)
 gate=[o for o in O.values() if o.name=='Portón negro' or o.name.startswith('Nervio portón')]
 rig('gate',[11,0,.02],gate,move=[-3.05,0,0])
 g['corrections'].append('Carpentry: complete moving leaf assemblies; rear glass bays split into fixed/sliding double-glazed leaves on parallel tracks inside the original bay; side panel A slides over B. Closed exterior opening dimensions preserved.')
 return rigs

def setup_tour(g):
 S,COL,cv=g['S'],g['COL'],g['cv']
 # One animated camera, twelve gently moving shots. The exported film dissolves between shots.
 # Points and targets use source XYZ. Interior eyes are 1.65m above the source finished floor.
 shots=[
 ('01 · Cedro Misionero',5,24,[[10.7,1.71,-5.5],[12.45,1.71,-1.1],[12.45,1.71,.80]],[[17.7,3.3,2.0],[15,2.8,3.7],[13.5,3.3,4.6]]),
 ('02 · Acceso al quincho',5,23,[[12.10,1.71,7.3],[12.3,1.74,10.3],[15.8,1.83,10.65],[18.0,1.86,7.0]],[[17.8,1.45,9.0],[18.0,1.5,8.8],[20.70,1.5,8.9],[18,1.5,4.3]]),
 ('03 · Monoambiente',5,22,[[18,1.86,7.0],[18,1.86,5.15],[18.5,1.86,3.7]],[[17.2,1.4,4.5],[16.4,1.3,3.9],[14.8,1.4,4.7]]),
 ('04 · Línea de fuego y baño pileta',5,22,[[18.7,1.86,10.65],[19.7,1.86,12.7],[21.15,1.86,12.9]],[[20.70,1.40,8.8],[21.3,1.45,10.9],[21.22,1.3,10.8]]),
 ('05 · Pileta y jardín',5,25,[[20.9,1.71,13.5],[17.6,1.71,13.5],[12.0,1.71,14.2],[11.9,2.1,17.8]],[[17.5,.5,16.5],[17.3,.6,16.6],[17.7,2.0,12.5],[18,2.8,10.5]]),
 ('06 · Escalera exterior',7,23,[[13.48,1.71,.8],[13.48,1.885,1.31],[13.48,3.31,3.13],[13.48,4.85,4.89],[13.5,4.85,5.4]],[[13.5,3.1,4.7],[13.5,3.8,5.2],[13.7,4.7,5.3],[14.5,4.7,5.3],[16.5,4.7,4.7]]),
 ('07 · Estudio de grabación',6,21,[[13.5,4.85,5.30],[14.65,4.90,5.30],[18.9,4.90,5.05],[19.55,4.90,3.65]],[[17,4.5,3],[17.4,4.3,3],[17.7,4.4,2.8],[17.4,4.4,3.0]]),
 ('08 · Balcón lateral',6,23,[[14.65,4.90,5.3],[13.5,4.85,5.3],[13.5,4.85,7.7],[13.5,4.85,9.72],[14.6,4.90,9.72]],[[13.5,4.4,7.4],[13.5,4.4,9.8],[13.7,4.4,10.4],[16.8,4.2,10.6],[18.8,4.2,10.5]]),
 ('09 · Cocina y comedor',5,22,[[16.2,4.90,11.18],[19.15,4.90,11.48],[20.0,4.90,10.6]],[[20.8,4.3,9.7],[21.4,4.25,9.7],[21.4,4.4,9.4]]),
 ('10 · Dormitorio y vestidor',6,21,[[18.52,4.90,9.60],[18.52,4.90,8.5],[18.10,4.90,7.68],[16.95,4.90,7.68]],[[18.52,4.5,6.45],[18.2,4.4,6.5],[15.8,4.0,7.4],[14.8,4.2,7.4]]),
 ('11 · Baño en suite',5,18,[[17.0,4.90,7.68],[18.45,4.90,7.68],[20.05,4.90,7.50]],[[18.52,4.6,6.5],[20.7,4.3,6.9],[21.15,4.15,6.85]]),
 ('12 · Balcón, pileta y paisaje',7,26,[[19.3,4.90,10.8],[18.4,4.90,11.55],[18.35,4.85,12.5],[16,6.0,16.2],[7.5,7.0,23.0]],[[18.3,4.3,12.5],[18.3,3.9,14.0],[17.0,2.5,16.5],[17.8,3.0,10.5],[16.4,3,10.5]])
 ]
 # Monotone Hermite prevents overshooting the one-metre balcony/stair footprint.
 def hermite(vals,u):
  N=len(vals);x=u*(N-1);i=min(N-2,int(x));t=x-i
  out=[]
  for axis in range(3):
   y=[v[axis] for v in vals];d=[y[j+1]-y[j] for j in range(N-1)];sl=[0]*N
   for j in range(1,N-1):sl[j]=0 if d[j-1]*d[j]<=0 else 2*d[j-1]*d[j]/(d[j-1]+d[j])
   a,b=y[i],y[i+1];ma,mb=sl[i],sl[i+1]
   out.append((2*t**3-3*t*t+1)*a+(t**3-2*t*t+t)*ma+(-2*t**3+3*t*t)*b+(t**3-t*t)*mb)
  return out
 cam=g['target_cam']('TOUR | Recorrido virtual',shots[0][3][0],shots[0][4][0],24)
 cam.rotation_mode='QUATERNION';route=[];frame=1;previous=None
 target=g['empty']('TOUR | Punto de mirada',[0,0,0],'CAMERAS')
 for title,duration,lens,points,targets in shots:
  length=duration*S.render.fps;start=frame
  curve=bpy.data.curves.new(title+' | Bézier route','CURVE');curve.dimensions='3D';curve.resolution_u=24
  spline=curve.splines.new('BEZIER');spline.bezier_points.add(len(points)-1)
  for b,p in zip(spline.bezier_points,points):b.co=cv(p);b.handle_left_type='AUTO';b.handle_right_type='AUTO'
  path=bpy.data.objects.new('PATH | '+title,curve);COL['CAMERAS'].objects.link(path);path.hide_render=True;path.display_type='WIRE'
  S.timeline_markers.new(title,frame=start)
  sample=[]
  for j in range(length):
   u=j/(length-1);p=hermite(points,u);t=hermite(targets,u);loc=cv(p);quat=(cv(t)-loc).to_track_quat('-Z','Y')
   if previous is not None and previous.dot(quat)<0:quat.negate()
   previous=quat.copy()
   cam.location=loc;cam.rotation_quaternion=quat;cam.keyframe_insert('location',frame=frame);cam.keyframe_insert('rotation_quaternion',frame=frame)
   cam.data.lens=lens;cam.data.keyframe_insert('lens',frame=frame)
   target.location=cv(t);target.keyframe_insert('location',frame=frame)
   sample.append(p);frame+=1
  route.append({'title':title,'start':start,'end':frame-1,'seconds':duration,'lens':lens,'points':points,'targets':targets,'samples':sample})
 # Dense samples are the equivalent rig; use linear interpolation between samples, no camera roll.
 for ob in [cam,target]:
  action=ob.animation_data.action
  for layer in action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='LINEAR'
 S.frame_start=1;S.frame_end=frame-1
 for e in g['RIGS'].values():
  # Keep all doors open throughout walking sections and finish with open balcony view.
  if e.animation_data:
   for layer in e.animation_data.action.layers:
    for strip in layer.strips:
     for bag in strip.channelbags:
      for fc in bag.fcurves:
       for k in fc.keyframe_points:
        if k.co.x>=1400:k.co.y=1
 json.dump({'fps':S.render.fps,'frames':S.frame_end,'shots':route},open(os.path.join(g['OUT'],'tour_route.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
 cam['route_description']='Twelve smooth travelling shots in source coordinates. Video dissolves at shot boundaries. Walking eye height 1.65m above finished surfaces.'
 return cam,route
