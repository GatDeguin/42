import bpy,json,math,os
from mathutils import Vector
S=bpy.context.scene;S.frame_set(150);bpy.context.view_layer.update();cam=bpy.data.objects['REV | Dormitorio completo'];S.camera=cam
results=[]
for u in [.2,.4,.5,.6,.8]:
 for v in [.3,.5,.7]:
  d=cam.matrix_world.to_quaternion()@Vector(((u-.5)*cam.data.sensor_width/cam.data.lens,(v-.5)*cam.data.sensor_width/cam.data.lens*.75,-1));d.normalize();origin=cam.matrix_world.translation.copy()
  seen=[]
  for i in range(12):
   hit,pos,n,idx,ob,mw=S.ray_cast(bpy.context.evaluated_depsgraph_get(),origin,d,distance=20)
   if not hit:break
   seen.append({'name':ob.name,'hidden_render':ob.hide_render,'hit':list(pos),'materials':[s.material.name if s.material else None for s in ob.material_slots]})
   if not ob.hide_render:break
   origin=pos+d*.001
  results.append({'uv':[u,v],'hits':seen})
json.dump(results,open('review95/bedroom_camera_hits.json','w',encoding='utf8'),ensure_ascii=False,indent=2)
print(json.dumps(results,ensure_ascii=False))
