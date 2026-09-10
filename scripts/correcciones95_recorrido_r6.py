"""R6F prepared edited tour path around revised furnishings. Does not render video."""
import bpy,os,json,math,ast,numpy as np,sys
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1)
def cv(p):return Vector((p[0],-p[2],p[1]))
R=json.load(open(os.path.join(ROOT,'output','tour_route.json'),encoding='utf8'));shots=R['shots']
def change(i,points,targets):
 shots[i-1]['points']=points;shots[i-1]['targets']=targets;shots[i-1]['knot_times']=list(np.linspace(0,1,len(points)))
change(2,[[12.1,1.71,7.3],[12.3,1.74,8.5],[14.8,1.83,8.7],[16.1,1.86,8.7],[18.0,1.86,7.0]],[[17.8,1.45,9],[18,1.5,8.8],[20.7,1.5,8.9],[20.7,1.5,8.5],[18,1.5,4.3]])
change(4,[[18.0,1.86,10.7],[19.2,1.86,10.8],[19.8,1.86,11.2],[20.7,1.86,12.8],[21.15,1.86,12.9]],[[20.6,1.6,8.4],[20.95,1.6,8.25],[21.1,1.65,8.3],[21.25,1.35,10.8],[21.22,1.3,10.8]])
shots[6]['points'][3]=[19.35,4.98,5.28];shots[6]['points'][4]=[19.35,4.9,3.65]
change(9,[[16.67,4.9,10.55],[16.67,4.9,9.40],[17.75,4.9,9.35],[19.65,4.9,9.35],[20.0,4.9,10.6]],[[20.8,4.3,9.7],[21.1,4.3,9.7],[21.4,4.25,9.7],[21.4,4.3,9.7],[21.4,4.4,9.4]])
change(10,[[18.52,4.9,9.6],[18.52,4.9,8.5],[18.38,4.9,8.35],[18.38,4.9,8.1],[18.28,4.9,7.68],[17.25,4.9,7.68],[16.95,4.9,7.68]],[[18.52,4.5,6.45],[18.52,4.5,7.68],[18.3,4.5,6.45],[18.0,4.4,7.45],[16.6,4.3,7.4],[15.1,4.15,7.45],[14.8,4.2,7.4]])
change(12,[[19.3,4.9,10.8],[19.0,4.9,11.70],[18.35,4.9,11.70],[18.35,4.85,12.5],[18.35,5.60,12.60],[16,6,16.2],[7.5,7,23]],[[18.3,4.3,12.5],[18.3,3.9,14],[17,2.5,16.5],[17,2.5,16.5],[17.2,2.5,16.5],[17.8,3,10.5],[16.4,3,10.5]])
for nd in ast.parse(open(os.path.join(ROOT,'scripts','iteration2_pass2.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name=='interp':exec(compile(ast.Module(body=[nd],type_ignores=[]),'<interp>','exec'))
cam=bpy.data.objects['TOUR | Recorrido virtual'];target=bpy.data.objects['TOUR | Punto de mirada']
cam.animation_data_clear();cam.data.animation_data_clear();target.animation_data_clear();cam.rotation_mode='QUATERNION'
S.timeline_markers.clear();frame=1;prev=None
for shot in shots:
 N=int(shot['seconds']*R['fps']);shot['start']=frame;shot['end']=frame+N-1
 times=shot.get('knot_times',list(np.linspace(0,1,len(shot['points']))));samples=[];S.timeline_markers.new(shot['title'],frame=frame)
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
S.frame_end=frame-1;R['frames']=frame-1;R['video_status']='PAUSED_PENDING_EXPLICIT_USER_APPROVAL';R['revision']='R6 corrected furniture route'
json.dump(R,open(os.path.join(ROOT,'review95','r6_tour_route.json'),'w'),ensure_ascii=False,indent=2)
S['video_render_requires_explicit_approval']=True;S['tour_route_requires_revalidation_after_layout']=True
S['review_iteration']='95 / R6F coordinated furnishings and prepared tour';S.frame_set(1);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas']
for tx in bpy.data.texts:
 if tx.name.startswith('LEEME'):
  text=tx.as_string().replace('baño2.60m sobre+3.30','baño2.60m sobre+3.25')
  tx.clear();tx.write(text)
note=bpy.data.texts.get('LEEME | Revisión R6 vigente') or bpy.data.texts.new('LEEME | Revisión R6 vigente');note.clear();note.write('''CASA DE CAMPO · CANDIDATO EN REVISIÓN R6
Unidades métricas. Estudio3,20m y vivienda/baño2,60m libres. Piso PA+3,25.
Trece puertas animadas, incluida conexión baño-comedor. Se conservan cámaras de fuente y se agregan cámarasREV.
Mobiliario corregido según indicaciones del propietario: barra paralela a parrilla, mesa quincho al jardín, ventana a la derecha de la cama, mesada cocina reordenada.
BañosPB y cocina mono coordinados; espejos/frentes duplicados retirados; apoyos y guías definidos.
Recorrido virtual editado1968fotogramas/24fps: preparado, pendiente revisión visual antes de cualquier renderizado.
VIDEO PAUSADO hasta aprobación explícita. La escena alternativa continua anterior es histórica y no se ha revalidado.
Criterio de aprobación integral9,5 pendiente. Medidas de productos sin fabricante y detalles constructivos son propuestas, no cálculo/certificación.
''')
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_95_R6F_route.blend'),compress=True);print('R6F_ROUTE_READY_NO_VIDEO',flush=True)
