import bpy,json
from mathutils import Vector
S=bpy.context.scene;R=json.load(open(r'D:\2026\42\output\tour_route.json',encoding='utf8'));cam=bpy.data.objects['TOUR | Recorrido virtual'];errors=[]
for shot in R['shots']:
 for j in [0,len(shot['samples'])//2,len(shot['samples'])-1]:
  fr=shot['start']+j;S.frame_set(fr);bpy.context.view_layer.update();p=shot['samples'][j];err=(cam.location-Vector((p[0],-p[2],p[1]))).length
  if err>.002:errors.append({'shot':shot['title'],'frame':fr,'error_m':err})
r={'file':bpy.data.filepath,'blend_frame_end':S.frame_end,'json_frames':R['frames'],'camera_position_mismatches':errors}
json.dump(r,open(r'D:\2026\42\review\saved_route_final.json','w',encoding='utf8'),ensure_ascii=False,indent=2);print(json.dumps(r,ensure_ascii=False))
