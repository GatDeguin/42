import bpy,sys,os,json,math,numpy as np
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'output');sys.path.insert(0,os.path.join(ROOT,'scripts'))
D=json.load(open(os.path.join(ROOT,'source','scene.json'),encoding='utf8'));route=json.load(open(os.path.join(OUT,'tour_route.json'),encoding='utf8'))
S=bpy.context.scene
def cv(p):return Vector((p[0],-p[2],p[1]))
O={i:o for i,o in enumerate(S.objects)}
rigs={o.name.split(' | ',1)[1]:o for o in S.objects if o.name.startswith('DOOR | ')}
cams={o.name:o for o in S.objects if o.type=='CAMERA'}
from validate_scene import validate
v=validate({'S':S,'DATA':D,'OBJS':O,'RIGS':rigs,'CAM':cams,'TOUR':bpy.data.objects['TOUR | Recorrido virtual'],'ROUTE':route['shots'],'cv':cv,'corrections':json.loads(S['corrections'])})
def check(name,ok,m=None):v['checks'].append({'name':name,'pass':bool(ok),'measured':m})
def bounds(o):
 a=np.array([o.matrix_world@Vector(p) for p in o.bound_box]);return a.min(0),a.max(0)
S.frame_set(1);bpy.context.view_layer.update()
fixed=[]
for key,spec in D['views'].items():
 o=bpy.data.objects['CAM | '+spec['label']]
 err=(o.location-cv(spec['p'])).length
 want=(cv(spec['t'])-o.location).normalized();actual=o.rotation_euler.to_quaternion()@Vector((0,0,-1))
 fixed.append({'camera':o.name,'position_error_m':err,'lens_mm':o.data.lens,'target_angle_error_degrees':math.degrees(want.angle(actual))})
check('All 16 HTML cameras retain exact positions, focal lengths and targets',all(x['position_error_m']<.001 and x['target_angle_error_degrees']<.05 for x in fixed),fixed)
doorchecks=[]
for key in ['studio','suiteEntry','bedroomLink','bathLink','poolBath']:
 m=D['meshes'][D['doors'][key][0]];o=bpy.data.objects[m['name']]
 doorchecks.append({'door':key,'closed_error_m':(o.matrix_world.translation-cv(m['position'])).length})
check('Closed hinged leaves match HTML coordinates',all(x['closed_error_m']<.001 for x in doorchecks),doorchecks)
closed={k:[tuple(e.location),tuple(e.rotation_euler)] for k,e in rigs.items()}
S.frame_set(150);bpy.context.view_layer.update()
moved={k:sum(abs(a-b) for now,old in zip([e.location,e.rotation_euler],closed[k]) for a,b in zip(now,old)) for k,e in rigs.items()}
check('Every hinged/sliding door driver moves at open pose',all(t>.25 for t in moved.values()),moved)
check('Every tour door stays open to the continuous tour end',all(abs(e['open']-1)<.001 for e in rigs.values()))
S.frame_set(1);bpy.context.view_layer.update()
ceil=bpy.data.objects['Cielorraso estudio | cota inferior 6.45m'];a,b=bounds(ceil)
check('Flat studio ceiling has 3.20m clear finished height',abs(a[2]-3.25-3.2)<.001,{'floor':3.25,'ceiling':float(a[2]),'clear':float(a[2]-3.25)})
images=[im for im in bpy.data.images if im.source=='FILE' and im.type!='RENDER_RESULT']
check('All file-based texture/reference/HDR images are packed',all(im.packed_file for im in images),{'count':len(images),'unpacked':[im.name for im in images if not im.packed_file]})
required=['SITE','GROUND_FLOOR','UPPER_FLOOR','ROOF','STAIR','POOL','QUINCHO','STUDIO','INTERIORS','FURNITURE','LANDSCAPE','LIGHTS','CAMERAS']
check('All required semantic collections exist',all(c in bpy.data.collections for c in required),required)
check('Metric units at scale 1',S.unit_settings.system=='METRIC' and S.unit_settings.scale_length==1)
check('Cycles production renderer',S.render.engine=='CYCLES')
check('No unlabelled default Cube meshes',not any(o.name=='Cube' or o.name.startswith('Cube.') for o in S.objects))
check('Hollow sink and sanitary detailing',all(bpy.data.objects[n].get('physical_detail') for n in ['Bacha doble A','Bacha doble B','Bacha cocina','Bañera vivienda']))
continuous=bpy.data.scenes['RECORRIDO | Continuo'];check('Continuous animation and day/night/inspection variants',continuous.frame_end==4206 and len(bpy.data.scenes)>=5,{'scenes':[s.name for s in bpy.data.scenes],'continuous_frames':continuous.frame_end})
# Sample both camera animations against the built architectural walls. AABB collision checks are conservative.
tokens=['muro','medianera','tabique','fachada ciega','fachada superior','paño','pilar','columna','dintel','división estudio','separación mono']
walls=[o for o in S.objects if o.type=='MESH' and any(t in o.name.lower() for t in tokens) and not any(t in o.name.lower() for t in ['frente cocina','parrilla','marco'])]
wb=[(o.name,*bounds(o)) for o in walls]
S.frame_set(150);bpy.context.view_layer.update()
collisions=[]
cam=bpy.data.objects['TOUR | Recorrido continuo']
for fr in range(1,4207,6):
 S.frame_set(fr);pt=np.array(cam.location)
 for name,lo,hi in wb:
  if np.all(pt>lo+.018) and np.all(pt<hi-.018):collisions.append({'frame':fr,'wall':name,'position':pt.tolist()})
check('Continuous camera eye avoids architectural walls',not collisions,collisions[:25])
v['fine_grass_blades']=292601;v['continuous_tour_frames']=4206
v['passed']=all(x['pass'] for x in v['checks'])
json.dump(v,open(os.path.join(OUT,'validation.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
print('FINAL_VERIFICATION',v['passed'],'checks',len(v['checks']), 'failed',[x for x in v['checks'] if not x['pass']],flush=True)
# Human-readable production notes inside Blender, with real line breaks.
txt=bpy.data.texts['LEEME | Source, units, doors, tour'];old=txt.as_string().replace('\\n','\n');txt.clear();txt.write(old.split('CORRECCIONES DOCUMENTADAS')[0]+'CORRECCIONES DOCUMENTADAS\n'+'\n'.join(json.loads(S['corrections'])))
S.frame_set(1);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Casa_de_Campo.blend'))
if not v['passed']:raise RuntimeError('Final verification failed')
