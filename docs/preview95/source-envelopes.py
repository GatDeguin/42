"""Read-only source envelopes for the exported candidate, before any web LOD mutation.
Each envelope uses evaluated vertices in metres, not transformed bounding-box corners.
"""
import bpy,os,json,hashlib,numpy as np
ROOT=r'D:/2026/42';S=bpy.context.scene

def measure_source(destination):
 oldframe=S.frame_current;unit=float(S.unit_settings.scale_length);assert abs(unit-1)<1e-9,'Expected source Blender metre scale'
 rigs={o.name:o for o in S.objects if o.name.startswith('DOOR | ')};rows=[];omitted=[];lod=[]
 def door(o):
  p=o.parent
  while p:
   if p.name in rigs:return p.name
   p=p.parent
  return None
 eligible=[]
 for o in S.objects:
  if o.type not in ['MESH','CURVE','FONT'] or o.hide_render:continue
  if any(c.name=='REFERENCE' for c in o.users_collection):continue
  if any(w in o.name for w in ['Entorno | terreno continuo','Paisaje | pradera de transición']):omitted.append({'name':o.name,'reason':'Explicit web ground replacement; source ground retained in Blender'});continue
  if o.name.startswith(('BOT95 | árbol ','Césped botánico','MAT95 | árbol','Árbol lote')) or (o.type=='MESH' and len(o.data.vertices)>50000 and any(c.name=='LANDSCAPE' for c in o.users_collection)):
   lod.append({'name':o.name,'reason':'Vegetation LOD; not an architectural measurement'});continue
  eligible.append(o)
 def capture(objects):
  dg=bpy.context.evaluated_depsgraph_get();cache={};out={}
  for o in objects:
   e=o.evaluated_get(dg);m=e.to_mesh();key=e.data.as_pointer() if o.type=='MESH' else o.as_pointer()
   if key not in cache:
    a=np.empty(len(m.vertices)*3,np.float64);m.vertices.foreach_get('co',a);cache[key]=a.reshape(-1,3)
   a=cache[key]
   if not len(a):e.to_mesh_clear();continue
   matrix=np.array(o.matrix_world,dtype=np.float64);world=a@matrix[:3,:3].T+matrix[:3,3];world=world[:,[0,2,1]];world[:,2]*=-1
   out[o.name]={'min':world.min(axis=0).tolist(),'max':world.max(axis=0).tolist(),'evaluatedVertices':len(a)}
   if door(o):
    c=np.array([[1,0,0,0],[0,0,1,0],[0,-1,0,0],[0,0,0,1]],dtype=float);out[o.name]['localMatrixThree']=(c@np.array(o.matrix_local,dtype=float)@c.T).T.reshape(-1).tolist()
   e.to_mesh_clear()
  return out
 S.frame_set(1);bpy.context.view_layer.update();closed=capture(eligible)
 movable=[o for o in eligible if door(o)];S.frame_set(150);bpy.context.view_layer.update();opened=capture(movable)
 for o in eligible:
  if o.name not in closed:continue
  rows.append({'sourceName':o.name,'webLabel':o.name+(' | web mesh' if o.type in ['FONT','CURVE'] else ''),'sourceType':o.type,'door':door(o),'closed':closed[o.name],**({'open':opened[o.name]} if o.name in opened else {})})
 S.frame_set(oldframe);bpy.context.view_layer.update()
 report={'source':bpy.data.filepath,'sourceSHA256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),'sourceMetresPerUnit':unit,'webMetresPerUnit':1,'axes':'Three=(Blender X,Blender Z,-Blender Y)','method':'Actual evaluated vertices, world transform then axis conversion; frame 1 closed, frame 150 open','doorCount':len(rigs),'rows':rows,'omitted':omitted,'vegetationLOD':lod,'measurementNote':'These are object envelopes, not clear internal dimensions. Blender remains the detailed measurement source.'}
 os.makedirs(os.path.dirname(destination),exist_ok=True);json.dump(report,open(destination,'w'),ensure_ascii=False,indent=2);print('METRE_REFERENCE',len(rows),len(movable),'LOD',len(lod),flush=True);return report
if __name__=='__main__':
 import sys
 destination=sys.argv[sys.argv.index('--out')+1] if '--out' in sys.argv else os.path.join(ROOT,'docs','preview95','assets','source-envelopes.json')
 measure_source(destination)
