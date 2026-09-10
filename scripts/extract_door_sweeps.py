import bpy,os,json
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;data=json.load(open(os.path.join(ROOT,'review','revision_checks.json'),encoding='utf8'))
result=[]
def hull(points):
 p=sorted(set(tuple(round(float(c),5) for c in v) for v in points))
 def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 def half(seq):
  out=[]
  for v in seq:
   while len(out)>=2 and cross(out[-2],out[-1],v)<=0:out.pop()
   out.append(v)
  return out
 return half(p)[:-1]+half(p[::-1])[:-1]
for key,objects in data['tested_moving_meshes'].items():
 parts=[bpy.data.objects[n] for n in objects];o=parts[0];rig=bpy.data.objects['DOOR | '+key];entry={'key':key,'object':o.name,'motion':rig['motion']}
 for fr,label in [(1,'closed'),(150,'open')]:
  S.frame_set(fr);bpy.context.view_layer.update();pts=[ob.matrix_world@Vector(v) for ob in parts for v in ob.bound_box];entry[label]=hull([[v.x,-v.y] for v in pts])
  if fr==1:entry['pivot']=[rig.location.x,-rig.location.y]
 result.append(entry)
json.dump(result,open(os.path.join(ROOT,'review','door_glyphs.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
print('DOOR_GLYPHS_EXPORTED',len(result),flush=True)
