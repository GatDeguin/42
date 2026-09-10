"""Read-only re-open checks of furnishings and every door against static fit-out."""
import bpy,json,os,ast,numpy as np,math,hashlib,sys
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
for nd in ast.parse(open(os.path.join(ROOT,'scripts','verificar95_construccion.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['geometry','intersect','cv']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<check>','exec'))
def bb(o):
 bpy.context.view_layer.update();e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());a=np.array([e.matrix_world@Vector(v) for v in e.bound_box]);return a.min(0),a.max(0)
checks=[]
def check(name,ok,value):checks.append({'name':name,'pass':bool(ok),'measured':value})
for side in ['izq','der']:
 a,b=bb(bpy.data.objects['Mesa de luz suite '+side]);check('Bedside '+side+' bottom3.50/top3.78',abs(a[2]-3.50)<.0001 and abs(b[2]-3.78)<.0001,[list(a),list(b)])
 lamp=bpy.data.objects['Lámpara mesa suite '+side+' base'];la,lb=bb(lamp);check('Lamp '+side+' bears on top',abs(la[2]-b[2])<.0001,float(la[2]-b[2]))
a,b=bb(bpy.data.objects['Cabezal dormitorio']);check('Headboard70mm and aligned north wall',abs(b[1]-a[1]-.07)<.0001 and abs(-b[1]-6.10)<.0001,[list(a),list(b)])
check('Operative balcony furniture removed',not [o.name for o in S.objects if o.name.startswith(('Mesa balcón ','Silla balcón ')) and not o.hide_render],'inactive')
rigs=[o for o in S.objects if o.name.startswith('DOOR | ')];check('Thirteen actual operable door rigs',len(rigs)==13,len(rigs))
# Build all collision targets once, exclude vegetation and authored reference objects.
def moving(o):
 p=o.parent
 while p:
  if p.name.startswith('DOOR | '):return True
  p=p.parent
 return False
statics=[]
for o in S.objects:
 if o.type!='MESH' or o.hide_render or moving(o) or any(c.name in ['REFERENCE','LANDSCAPE','POOL','SITE'] for c in o.users_collection):continue
 a,b=bb(o)
 if b[0]<13 or a[0]>22.5 or b[1]<-13 or a[1]>1 or b[2]<.18 or a[2]>5.65:continue
 statics.append((o,geometry(o)))
print('STATIC_FITOUT_TARGETS',len(statics),flush=True)
# Read-only temporary detachment of actions enables exact0..1 property fractions.
for r in rigs:
 if r.animation_data:r.animation_data.action=None
hits=[]
for i in range(41):
 f=i/40
 for r in rigs:r['open']=f;r.update_tag()
 S.frame_set(1);bpy.context.view_layer.update()
 for r in rigs:
  for o in r.children_recursive:
   if o.type!='MESH':continue
   g=geometry(o)
   for target,tg in statics:
    count=intersect(g,tg)
    if count:hits.append({'opening':round(f,3),'rig':r.name,'moving':o.name,'static':target.name,'pairs':count})
 if i%10==0:print('DOOR_FRACTION',f,'collisions',len(hits),flush=True)
check('All moving components versus active static fitout41states',not hits,hits)
# More useful metrics than collision absence: actual bedside/finish levels.
levels={}
for key,name in [('bath','Piso baño vivienda'),('dwelling','Piso vivienda'),('quincho','Piso quincho')]:
 a,b=bb(bpy.data.objects[name]);levels[key]=float(b[2])
check('New bath entrance is level with dwelling',abs(levels['bath']-levels['dwelling'])<.0001,levels)
result={'model':bpy.data.filepath,'sha256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),'checks':checks,'all_pass':all(c['pass'] for c in checks),'limitations':'No structural or statutory certification; overlaps at explicitly designed bearing joints require interpretation.'}
json.dump(result,open(os.path.join(ROOT,'review95',(sys.argv[sys.argv.index('--out')+1] if '--out' in sys.argv else 'r4c_furniture_door_checks.json')),'w',encoding='utf8'),indent=2,ensure_ascii=False,default=float)
unique={(h['rig'],h['moving'],h['static']) for h in hits}
print(json.dumps({'all_pass':result['all_pass'],'checks':[(c['name'],c['pass']) for c in checks],'collision_pair_count':len(unique),'collision_pair_sample':sorted(unique)[:20]},ensure_ascii=False),flush=True)
