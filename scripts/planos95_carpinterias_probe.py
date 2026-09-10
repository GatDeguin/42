import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
out=Path(sys.argv[sys.argv.index('--')+1]);out.parent.mkdir(parents=True,exist_ok=True)
S=bpy.context.scene
rig_names=['DOOR | balconySide','DOOR | balconyRear_A','DOOR | balconyRear_B']
def bounds(o):
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());ps=[e.matrix_world@Vector(v) for v in e.bound_box];src=[(p.x,p.z,-p.y) for p in ps]
 return {'x':[min(p[0] for p in src),max(p[0] for p in src)],'y':[min(p[1] for p in src),max(p[1] for p in src)],'z':[min(p[2] for p in src),max(p[2] for p in src)]}
def descendants(o):
 r=[]
 for c in o.children:r.append(c);r+=descendants(c)
 return r
families={}
for rn in rig_names:
 r=bpy.data.objects[rn];children=[o for o in descendants(r) if o.type=='MESH'];families[rn]={'children':sorted(o.name for o in children),'states':[],'motion':r.get('motion'),'driver_expressions':[d.driver.expression for d in r.animation_data.drivers]}
 for fr in [1,30,45,67,90,105,150]:
  S.frame_set(fr);bpy.context.view_layer.update();families[rn]['states'].append({'frame':fr,'open':float(r.get('open',0)),'rig_location':[float(v) for v in r.location],'objects':{o.name:bounds(o) for o in children}})
S.frame_set(1);bpy.context.view_layer.update()
static={};hosts={}
for o in S.objects:
 if o.type!='MESH':continue
 n=o.name.lower()
 if ('lateral' in n or 'posterior' in n) and any(t in n for t in ['corrediza','perfil móvil','marco corrediza','umbral corrediza','hoja posterior']):static[o.name]=bounds(o)
 if any(t in n for t in ['losa','piso vivienda','acabado balcon','acabado balcón','mortero','niveladora','base adherida','umbral','dintel']):
  b=bounds(o)
  if 2.8<b['y'][0]<5.85 and b['x'][1]>12.8 and b['z'][1]>8.8:hosts[o.name]=b
allrig=[o.name for o in S.objects if o.name.startswith('DOOR |')]
data={'model':bpy.data.filepath,'sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'coordinates':'source metres X,Y(height),Z(depth)','all_door_rigs':allrig,'families':families,'static_frames_and_leaves_at_closed':static,'host_meshes':hosts}
out.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf8');print('CARPENTRY_PROBE',out,'rigs',len(allrig),'families',len(families),'static',len(static),'hosts',len(hosts))
