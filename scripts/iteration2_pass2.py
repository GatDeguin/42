import bpy,os,json,math,ast,numpy as np
from mathutils import Vector,Matrix
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'output');S=bpy.context.scene;S.frame_set(1)
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
# Small final coordination adjustment: kitchen riser between rafter10 and ceiling channel12.
tree=ast.parse(open(os.path.join(ROOT,'scripts','iteration2_pass1.py'),encoding='utf8').read())
base=ast.parse(open(os.path.join(ROOT,'scripts','iteration1_pass1.py'),encoding='utf8').read())
for nd in base.body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['cv','put','box','cyl','cut','pipe']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helpers>','exec'))
for nd in tree.body:
 if isinstance(nd,ast.FunctionDef) and nd.name=='reset_box':exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helpers>','exec'))
p=bpy.data.objects['Extracción cocina | salida independiente']
for v in p.data.vertices:v.co.x+=.07*max(0,min(1,(v.co.z-5.2)/.2))
for nm in ['Cielorraso vivienda | 2.60m sobre piso general','Cubierta pendiente pileta','Vivienda | aislación y membrana bajo chapa','Revestimiento interior | Cubierta pendiente pileta']:
 if bpy.data.objects.get(nm):
  ob=reset_box(nm);c=cyl('Temporal cocina libre de cabio',[21.46,5.5,10.49],[21.46,8,10.49],.112,col='REFERENCE');cut(ob,c);bpy.data.objects.remove(c,do_unlink=True)
c=box('Temporal techo baño',[20.65,5.87,7.3],[2.28,.5,2.37],col='REFERENCE',bev=0);cut(bpy.data.objects['Cielorraso vivienda | 2.60m sobre piso general'],c);bpy.data.objects.remove(c,do_unlink=True)
for nm in ['Cocina | babeta perforada','Cocina | remate superior']:bpy.data.objects[nm].location.x+=.07
details=json.load(open(os.path.join(ROOT,'review','construction_details.json'),encoding='utf8'))
for p in details['kitchen_route']:
 if p[1]>=5.4:p[0]+=.07
json.dump(details,open(os.path.join(ROOT,'review','construction_details.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
# Correct outward-facing sign, preserving the plaque centre.
plaque=bpy.data.objects['Placa calle | Cedro Misionero'];plaque.rotation_euler=(math.pi/2,0,math.pi);plaque.data.align_x='CENTER';plaque.data.align_y='CENTER';plaque.location=cv([10.03,1.64,-.10])
R=json.load(open(os.path.join(OUT,'tour_route.json'),encoding='utf8'));shots=R['shots']
def change(i,points,targets,seconds=None,times=None,lens=None):
 s=shots[i-1];s['points']=points;s['targets']=targets
 if seconds:s['seconds']=seconds
 if times:s['knot_times']=times
 if lens:s['lens']=lens
change(4,[[15.6,1.86,11.35],[17.4,1.86,10.8],[18.8,1.86,10.55],[19.3,1.86,11.1],[21.15,1.86,12.9]],[[20.6,1.6,8.4],[20.95,1.6,8.25],[21.1,1.65,8.3],[21.3,1.5,10.7],[21.22,1.3,10.8]],8,[0,.30,.65,.8,1],23)
change(6,[[13.48,1.71,.8],[13.48,1.885,1.31],[13.48,3.31,3.13],[13.48,4.85,4.89],[13.5,4.85,5.4]],[[13.5,1.20,3],[13.5,1.65,3.6],[13.5,2.90,4.7],[13.5,3.8,5.7],[16.5,4.7,4.7]],8)
change(7,[[13.5,4.85,5.3],[14.65,4.9,5.3],[16.,4.9,5.48],[20.2,4.98,5.28],[19.55,4.9,3.65]],[[16.4,4.55,5.35],[18.5,4.6,5.35],[19.8,4.65,4.3],[17.2,4.5,2.6],[17.4,4.4,3.0]],10,[0,.12,.24,.50,1],21)
change(10,[[18.52,4.90,9.60],[18.52,4.90,8.5],[18.52,4.9,7.68],[17.25,4.90,7.68],[16.95,4.90,7.68]],[[18.52,4.5,6.45],[18.52,4.5,7.68],[16.6,4.3,7.4],[15.1,4.15,7.45],[14.8,4.2,7.4]],8,[0,.15,.30,.48,1])
change(11,[[17.0,4.90,7.68],[18.52,4.90,7.68],[19.68,4.90,7.68],[19.84,4.90,8.25],[19.84,4.90,8.55]],[[19.5,4.55,7.68],[20.6,4.5,7.3],[21.1,4.25,7.1],[20.8,4.23,6.72],[20.8,4.23,6.72]],8,[0,.2,.4,.55,1],18)
# Piecewise Hermite with no overshoot; time allocation gives rooms a readable reveal.
def interp(vals,u,times):
 i=min(len(vals)-2,next((j for j in range(len(times)-1) if times[j+1]>=u),len(vals)-2));dt=times[i+1]-times[i];t=(u-times[i])/dt
 out=[]
 for axis in range(3):
  y=[v[axis] for v in vals];d=[(y[j+1]-y[j])/(times[j+1]-times[j]) for j in range(len(vals)-1)];sl=[0]*len(vals)
  for j in range(1,len(vals)-1):sl[j]=0 if d[j-1]*d[j]<=0 else 2*d[j-1]*d[j]/(d[j-1]+d[j])
  out.append((2*t**3-3*t*t+1)*y[i]+(t**3-2*t*t+t)*sl[i]*dt+(-2*t**3+3*t*t)*y[i+1]+(t**3-t*t)*sl[i+1]*dt)
 return out
cam=bpy.data.objects['TOUR | Recorrido virtual'];target=bpy.data.objects['TOUR | Punto de mirada']
cam.animation_data_clear();cam.data.animation_data_clear();target.animation_data_clear();cam.rotation_mode='QUATERNION'
S.timeline_markers.clear();frame=1;prev=None
for shot in shots:
 N=int(shot['seconds']*R['fps']);shot['start']=frame;shot['end']=frame+N-1
 times=shot.get('knot_times',list(np.linspace(0,1,len(shot['points']))));samples=[]
 S.timeline_markers.new(shot['title'],frame=frame)
 path=bpy.data.objects.get('PATH | '+shot['title'])
 if path:
  path.data.splines.clear();sp=path.data.splines.new('POLY');sp.points.add(len(shot['points'])-1)
  for bp,pos in zip(sp.points,shot['points']):bp.co=(*cv(pos),1)
 for j in range(N):
  u=j/(N-1);p=interp(shot['points'],u,times);t=interp(shot['targets'],u,times);q=(cv(t)-cv(p)).to_track_quat('-Z','Y')
  if prev is not None and prev.dot(q)<0:q.negate()
  prev=q.copy();cam.location=cv(p);cam.rotation_quaternion=q;cam.keyframe_insert('location',frame=frame);cam.keyframe_insert('rotation_quaternion',frame=frame)
  cam.data.lens=shot['lens'];cam.data.keyframe_insert('lens',frame=frame);target.location=cv(t);target.keyframe_insert('location',frame=frame);samples.append(p);frame+=1
 shot['samples']=samples
for ob in [cam,cam.data,target]:
 for layer in ob.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='LINEAR'
S.frame_end=frame-1;R['frames']=frame-1;R['video_status']='PAUSED_PENDING_EXPLICIT_USER_APPROVAL'
json.dump(R,open(os.path.join(OUT,'tour_route.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
S['review_iteration']='2 / pass2 route and outward sign';S.frame_set(1);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Casa_de_Campo_Revision.blend'),compress=True)
print('PASS2_2_SAVED_NO_VIDEO',flush=True)
