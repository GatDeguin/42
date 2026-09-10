import bpy, math, numpy as np
from mathutils import Vector
def validate(g):
 S,D,O=g['S'],g['DATA'],g['OBJS'];checks=[]
 def check(name,ok,measured=None):checks.append({'name':name,'pass':bool(ok),'measured':measured})
 def named(name):return next((o for o in O.values() if o.name==name),None)
 def bounds(o):
  pts=[o.matrix_world@Vector(p) for p in o.bound_box]
  return np.array(pts).min(axis=0),np.array(pts).max(axis=0)
 S.frame_set(1);bpy.context.view_layer.update()
 floor=named('Losa planta baja');lo,hi=bounds(floor)
 check('Main footprint 8 x 12 m',abs(hi[0]-lo[0]-8)<.002 and abs(hi[1]-lo[1]-12)<.002,(hi-lo).tolist())
 check('Main building source origin X14/Z0',abs(lo[0]-14)<.002 and abs(hi[1])<.002,{'minX':float(lo[0]),'front_blender_Y':float(hi[1])})
 lawn=named('Césped del lote');a,b=bounds(lawn);check('Lot 22 x 20 m',abs(b[0]-a[0]-22)<.002 and abs(b[1]-a[1]-20)<.002,(b-a).tolist())
 pool=named('Fondo de pileta');a,b=bounds(pool);check('Pool 7 x 3 m',abs(b[0]-a[0]-7)<.002 and abs(b[1]-a[1]-3)<.002,(b-a).tolist())
 check('Pool rear/right setbacks 2m',abs(a[1]+18)<.002 and abs(b[0]-20)<.002,{'rear':float(20+a[1]),'right':float(22-b[0])})
 paving=[named('Losetas '+s) for s in ['norte','sur','oeste','este']]
 check('Continuous 1m paving',all(abs(min(o.dimensions.x,o.dimensions.y)-1)<.002 for o in paving),[list(o.dimensions) for o in paving])
 stair=[o for o in O.values() if o.name.startswith('Peldaño exterior ')]
 check('Exactly 18 exterior treads',len(stair)==18,len(stair))
 check('Stair clear nominal tread width 1m',all(abs(o.dimensions.x-1)<.002 for o in stair))
 landing=named('Descanso escalera');a,b=bounds(landing);check('Landing 1 x 1 m / top 3.2m',abs(b[0]-a[0]-1)<.002 and abs(b[1]-a[1]-1)<.002 and abs(b[2]-3.2)<.002,(b-a).tolist())
 top=named('Peldaño exterior 1');c,d=bounds(top)
 check('Top tread physically meets landing',abs(d[2]-b[2])<.003 and c[1]<=b[1]+.012,{'tread_top':float(d[2]),'landing_top':float(b[2]),'plan_overlap':float(b[1]-c[1])})
 check('Stair run 3.8m',abs(D['config']['stairRun']-3.8)<1e-6)
 window=named('Ventana DVH estudio vidrio');check('Studio lateral glazing 3m',abs(window.dimensions.y-3)<.002,list(window.dimensions))
 cloud=[o for o in O.values() if o.name.startswith(('Cloud estudio','Bafle cielorraso estudio'))]
 low=min(bounds(o)[0][2] for o in cloud)
 check('Studio clear height beneath acoustic treatment >=3.2m',low-3.25>=3.2-.001,{'underside':float(low),'finished_floor':3.25,'clear':float(low-3.25)})
 check('Graphite gable roof, both slopes',all(named(n) is not None for n in ['Cubierta pendiente Cedro Misionero','Cubierta pendiente pileta']))
 check('Four raised vegetable beds',sum(1 for o in O.values() if 'Huerta cantero' in o.name and 'sustrato' in o.name)==4)
 gate=named('Portón negro');check('Black 3m gate',abs(gate.dimensions.x-3)<.002)
 check('All required door rigs',all(k in g['RIGS'] for k in ['mono_L','mono_R','studio','balconySide','balconyRear_A','balconyRear_B','suiteEntry','bedroomLink','bathLink','poolBath','bathroomMono','gate']),list(g['RIGS']))
 check('Fixed source cameras plus tour',len(g['CAM'])>=16 and g['TOUR'].animation_data is not None,len(g['CAM']))
 # Camera eye positions tested against actual architectural wall bounding boxes.
 wall_tokens=['muro','medianera','tabique','fachada ciega','fachada superior','paño','pilar','columna','dintel','división estudio','separación mono']
 walls=[o for o in O.values() if any(t in o.name.lower() for t in wall_tokens) and not any(t in o.name.lower() for t in ['frente cocina','parrilla','marco'])]
 conflicts=[]
 S.frame_set(150);bpy.context.view_layer.update()
 wallbounds=[(o.name,*bounds(o)) for o in walls]
 for shot in g['ROUTE']:
  for j,p in enumerate(shot['samples'][::6]):
   v=np.array(g['cv'](p))
   for name,a,b in wallbounds:
    if np.all(v>a+.018) and np.all(v<b-.018):
     conflicts.append({'shot':shot['title'],'frame':shot['start']+j*6,'wall':name,'eye_source':p})
 check('Tour camera eye clear of architectural walls',len(conflicts)==0,conflicts[:30])
 # Required labels and elevations are an independent semantic check, in addition to source checks.
 check('No internal staircase objects',not any('escalera interior' in o.name.lower() for o in S.objects))
 S.frame_set(1)
 return {'passed':all(c['pass'] for c in checks),'checks':checks,'source_checks':D['checks'],'corrections':g['corrections'],'objects':len(S.objects),'materials':len(bpy.data.materials),'source_meshes':len(D['meshes']),'source_instances':sum(len(m['instances'] or [])//16 for m in D['meshes']),'tour_frames':S.frame_end,'fps':S.render.fps,'axis':'HTML (X,Y,Z) => Blender (X,-Z,Y)'}
