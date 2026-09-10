import bpy,json,math,os,hashlib,sys
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(150);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
r=json.load(open(os.path.join(ROOT,'review95','r6_tour_route.json') if '--r6' in sys.argv else os.path.join(ROOT,'output','tour_route.json'),encoding='utf8'))
out={'model':bpy.data.filepath,'sha256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),'scope':'Existing edited tour camera positions; fixed still-open doors; underside clearance1.35m below eye and200mm horizontal clearance at torso. No video. Read-only path audit.','shots':[]}
for shot in r['shots']:
 hits={}
 for j in range(0,len(shot['samples']),6):
  p=shot['samples'][j];v=Vector((p[0],-p[2],p[1]))
  rays=[(v,Vector((0,0,-1)),1.35,'below')]
  for k in range(8):
   a=k*math.tau/8;rays.append((v-Vector((0,0,.60)),Vector((math.cos(a),math.sin(a),0)),.20,'torso'))
  for origin,direction,dist,kind in rays:
   h,pt,n,idx,obj,mat=S.ray_cast(dg,origin,direction,distance=dist)
   if h:
    key=(obj.name,kind);hits.setdefault(key,[]).append(shot['start']+j)
 out['shots'].append({'title':shot['title'],'hits':[{'object':n,'kind':k,'frames':fs} for (n,k),fs in hits.items()]})
 print('ROUTE',shot['title'],len(hits),flush=True)
json.dump(out,open(os.path.join(ROOT,'review95','r6f_route_body_checks.json' if '--r6' in sys.argv else 'r6_route_body_checks.json'),'w'),ensure_ascii=False,indent=2)
print(json.dumps(out,ensure_ascii=False))
