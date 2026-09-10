"""R6J practical lighting bodies and calibrated local task lights. No video."""
import bpy,os,math,ast,json,numpy as np
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
for m in bpy.data.materials:
 if m.name.startswith(('MAT95 | ','FIT95 | ')):M[m.name.split(' | ',1)[1]]=m
def cv(p):return Vector((p[0],-p[2],p[1]))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_textiles.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name=='bounds':exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_materialidad.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['box','cyl','mesh']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<fast>','exec'))
for key,color,rough,em in [('lacado marfil',(.67,.64,.58),.34,0),('opal cálido',(.80,.78,.72),.42,2.5)]:
 m=bpy.data.materials.new('PHOTO95 | '+key);m.use_nodes=True;bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Emission Color'].default_value=(1,.85,.7,1);bs.inputs['Emission Strength'].default_value=em;M[key]=m
def drum(name,x,z,lo,hi,r,material='lacado marfil'):
 n=96;vs=[]
 for rr,h in [(r,lo),(r,hi),(r-.003,lo),(r-.003,hi)]:
  vs += [cv([x+rr*math.cos(i*math.tau/n),h,z+rr*math.sin(i*math.tau/n)]) for i in range(n)]
 fs=[]
 for i in range(n):
  j=(i+1)%n
  fs.extend([(i,j,n+j,n+i),(2*n+j,2*n+i,3*n+i,3*n+j),(i,2*n+i,2*n+j,j),(n+j,3*n+j,3*n+i,n+i)])
 o=mesh(name,vs,fs,material,'LIGHTS')
 for p in o.data.polygons:p.use_smooth=(p.index%4)<2
 return o
def area(name,p,power,size=.27,target=None):
 o=bpy.data.objects.get(name)
 if not o:
  d=bpy.data.lights.new(name,'AREA');o=bpy.data.objects.new(name,d);COL['LIGHTS'].objects.link(o)
 o.location=cv(p);o.data.type='AREA';o.data.shape='DISK';o.data.size=size;o.data.energy=power;o.data.color=(1,.84,.68)
 o.rotation_euler=(cv(target)-o.location).to_track_quat('-Z','Y').to_euler() if target else (0,0,0)
 return o
# Three formerly wholly emissive drums receive metal bodies, recessed opal and suspension.
for name,power in [('Lámpara mono',28),('Colgante isla mono A',16),('Colgante isla mono B',16)]:
 old=bpy.data.objects[name];a,b=bounds(old);x=float((a[0]+b[0])/2);z=float(-(a[1]+b[1])/2);lo=float(a[2]);hi=float(b[2]);r=float((b[0]-a[0])/2)
 bpy.data.objects.remove(old,do_unlink=True);drum(name,x,z,lo,hi,r)
 cyl('PHOTO95 | tapa '+name,[x,hi-.003,z],[x,hi,z],r-.003,'lacado marfil','LIGHTS')
 cyl('PHOTO95 | difusor '+name,[x,lo+.001,z],[x,lo+.003,z],r-.004,'opal cálido','LIGHTS')
 cyl('PHOTO95 | suspensión '+name,[x,hi,z],[x,2.982,z],.0018,'blackMetal','LIGHTS')
 cyl('PHOTO95 | florón '+name,[x,2.98,z],[x,3.0,z],.031,'lacado marfil','LIGHTS')
 area('LED | '+name,[x,lo-.004,z],power,2*(r-.005))
# Existing mono indirect fill is tied to ceiling illumination, less orange and less dominant.
o=bpy.data.objects.get('Indirecta | monoambiente')
if o:o.data.energy=45;o.data.color=(1,.86,.73)
# Add the actual wall-mounted task light corresponding to retained kitchen LED.
box('PHOTO95 | aplique lineal mesada mono',[14.295,1.720,4.35],[.050,.040,1.10],'blackMetal','LIGHTS',.002)
box('PHOTO95 | difusor mesada mono',[14.295,1.6995,4.35],[.040,.001,1.075],'opal cálido','LIGHTS',.0003)
for z in [3.90,4.80]:box('PHOTO95 | anclaje mesada mono',[14.245,1.720,z],[.09,.020,.025],'blackMetal','LIGHTS',.0005)
o=area('LED | Luz bajo alacena mono',[14.295,1.696,4.35],17.36)
o.data.shape='RECTANGLE';o.data.size=.040;o.data.size_y=1.075
# Two small ceiling-mounted adjustable spots light the cooking work zone from outside the hood.
for i,z in enumerate([8.10,9.35],1):
 x=19.70;drum('PHOTO95 | foco quincho '+str(i),x,z,2.91,2.99,.07,'blackMetal')
 cyl('PHOTO95 | base foco quincho',[x,2.989,z],[x,3.0,z],.055,'blackMetal','LIGHTS')
 p=cv([x+.005,2.93,z]);q=cv([20.8,1.15,z]);direction=(q-p).normalized()
 a=p-direction*.004;b=p+direction*.004
 cyl('PHOTO95 | óptica orientable quincho',[a.x,a.z,-a.y],[b.x,b.z,-b.y],.043,'opal cálido','LIGHTS')
 o=area('LED | tarea quincho '+str(i),[b.x+direction.x*.006,b.z+direction.z*.006,-b.y-direction.y*.006],24,.075,[20.8,1.15,z]);o.data.spread=math.radians(90)
# Bathrooms retain soft lighting but use less amber balance; these are proposed ceiling sources.
for name in ['Indirecta | baño mono','Indirecta | baño pileta']:
 o=bpy.data.objects.get(name)
 if o:o.data.energy=45;o.data.color=(1,.86,.74)
S['r6j_lighting_scope']=json.dumps({'mono_drums':'same envelopes, opaque metal housings, opal diffusers and suspensions','quincho':'two24W Blender radiometric area lights at real ceiling-mounted fixtures; not electrical nameplate wattage','task_light_mono':'retained source17.36W now attached to modelled wall fixture','status':'P lighting/fixtures; no lux or electrical design certification.'},ensure_ascii=False)
S['review_iteration']='95 / R6J photographic lighting candidate';S.frame_set(1);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_95_R6J.blend'),compress=True);print('R6J_SAVED_NO_VIDEO',flush=True)
