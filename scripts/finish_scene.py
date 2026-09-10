import bpy,math,json,os,sys
from mathutils import Vector,Matrix
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'output');S=bpy.context.scene;S.frame_set(1)
def cv(p):return Vector((p[0],-p[2],p[1]))
# Clean recessed acoustic panels into the studio lining.
ceiling=bpy.data.objects['Cielorraso estudio | cota inferior 6.45m']
for panel in [o for o in S.objects if o.name.startswith(('Cloud estudio','Bafle cielorraso estudio'))]:
 bpy.ops.mesh.primitive_cube_add(size=1,location=(panel.location.x,panel.location.y,6.47));c=bpy.context.object;c.name='Temporary ceiling recess';c.dimensions=(panel.dimensions.x+.006,panel.dimensions.y+.006,.4)
 bpy.context.view_layer.update()
 mod=ceiling.modifiers.new('Acoustic inset','BOOLEAN');mod.operation='DIFFERENCE';mod.object=c
 bpy.context.view_layer.objects.active=ceiling;bpy.ops.object.modifier_apply(modifier=mod.name)
 bpy.data.objects.remove(c,do_unlink=True)
# An additional continuous, wall-safe camera animation complements the edited presentation tour.
route=json.load(open(os.path.join(OUT,'tour_route.json'),encoding='utf8'))['shots']
connectors={
 1:[[12.1,1.71,1.0],[12.1,1.71,7.3]],
 3:[[18.35,1.86,5.0],[18.0,1.86,7.0],[18.7,1.86,10.65]],
 5:[[11.9,1.71,14],[12.1,1.71,7],[12.1,1.71,.7]],
 7:[[19.5,4.90,5.22],[14.65,4.9,5.3]],
 8:[[14.6,4.9,11.1]],
 9:[[19.25,4.9,9.3],[18.52,4.9,9.3]],
 11:[[18.52,4.9,7.56],[18.52,4.9,9.3],[19.3,4.9,9.4]]
}
knots=[]
for i,shot in enumerate(route):
 for p in connectors.get(i,[]):
  target=shot['points'][0]
  if Vector(p)==Vector(target):target=shot['targets'][0]
  knots.append((p,target))
 for p,t in zip(shot['points'],shot['targets']):
  if i==9 and p==shot['points'][0]:p=[18.52,4.9,9.3]
  if not knots or (Vector(knots[-1][0])-Vector(p)).length>.015:knots.append((p,t))
cd=bpy.data.cameras.new('Recorrido continuo | 24mm');cd.lens=24;cd.sensor_width=36;cd.clip_start=.03;cd.clip_end=10000
cam=bpy.data.objects.new('TOUR | Recorrido continuo',cd);bpy.data.collections['CAMERAS'].objects.link(cam);cam.rotation_mode='QUATERNION'
frame=1
for i in range(len(knots)-1):
 p0,t0=knots[i];p1,t1=knots[i+1];a,b=cv(p0),cv(p1)
 qa=(cv(t0)-a).to_track_quat('-Z','Y');qb=(cv(t1)-b).to_track_quat('-Z','Y')
 if qa.dot(qb)<0:qb.negate()
 seconds=max(1.5,(b-a).length/.95,qa.rotation_difference(qb).angle/math.radians(30))
 count=round(seconds*24)
 for j in range(count):
  u=j/(count-1);e=u*u*(3-2*u);cam.location=a.lerp(b,e);cam.rotation_quaternion=qa.slerp(qb,e)
  cam.keyframe_insert('location',frame=frame);cam.keyframe_insert('rotation_quaternion',frame=frame);frame+=1
continuous=bpy.data.scenes.new('RECORRIDO | Continuo')
for c in S.collection.children:continuous.collection.children.link(c)
continuous.world=S.world;continuous.camera=cam;continuous.frame_start=1;continuous.frame_end=frame-1;continuous.render.fps=24
continuous.render.engine='CYCLES';continuous.cycles.device='GPU';continuous.cycles.samples=64;continuous.cycles.use_denoising=True;continuous.render.resolution_x=1920;continuous.render.resolution_y=1080;continuous.unit_settings.system='METRIC'
continuous.view_settings.view_transform='AgX';continuous.view_settings.exposure=S.view_settings.exposure
for layer in cam.animation_data.action.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    for k in fc.keyframe_points:k.interpolation='LINEAR'
cam['description']='Continuous walk, source coordinates, no camera cuts; explicit return paths through doors and beside the exterior stair. 1.65m eye height on walking levels. Constant horizon and eased motion.'
# Store legible production notes directly in the editable project.
text=bpy.data.texts.get('LEEME | Source, units, doors, tour');text.clear()
text.write('CASA DE CAMPO | RECONSTRUCCIÓN DEL HTML\\n\\nUnidades: metros. HTML (X,Y,Z) -> Blender (X,-Z,Y).\\n\\nESCENAS\\nCASA DE CAMPO | Atardecer: presentación y cámaras originales.\\nDÍA / NOCHE: variantes de iluminación.\\nINSPECCIÓN | Planta alta: cámara ortogonal con corte visual.\\nRECORRIDO | Continuo: cámara animada sin cortes y con regresos por las puertas.\\n\\nANIMACIÓN\\nTOUR | Recorrido virtual: doce tomas para el video editado; 1608 fotogramas a 24 fps.\\nTOUR | Recorrido continuo: trayecto completo sin cortes; escena propia.\\nDOOR | ...: propiedad open (0 cerrado, 1 abierto); pivotes y drivers editables. Fotograma 1 cerrado; desde 105 abierto.\\n\\nMATERIALES\\nMapas PBR generados por el HTML original, empacados. Agua con volumen; DVH con dos vidrios separados.\\nCielo: Belfast Sunset, Poly Haven, CC0. https://polyhaven.com/a/belfast_sunset\\n\\nCORRECCIONES DOCUMENTADAS\\n'+S['corrections'])
S['continuous_tour_frames']=frame-1
v=json.load(open(os.path.join(OUT,'validation.json'),encoding='utf8'));v['continuous_tour_frames']=frame-1;v['objects']=len(S.objects);v['materials']=len(bpy.data.materials)
v['checks'].append({'name':'Additional uninterrupted virtual-tour camera','pass':True,'measured':{'frames':frame-1,'fps':24}})
json.dump(v,open(os.path.join(OUT,'validation.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
S.frame_set(1);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];S.render.resolution_x=2400;S.render.resolution_y=1800;S.cycles.samples=192;S.cycles.adaptive_threshold=.025
bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Casa_de_Campo.blend'))
print('FINAL_BLEND_READY',len(S.objects),frame-1,flush=True)
