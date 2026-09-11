import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
S=bpy.context.scene
rigs=[bpy.data.objects['DOOR | '+k] for k in ['bedroomLink','bedroomDining']]
movnames={o.name for r in rigs for o in r.children_recursive if o.type=='MESH' and not o.hide_render}
checks=[]
for name in ['REV | Dormitorio acceso','REV | Dormitorio completo','LUZ99 | Dormitorio desde paso']:
 cam=bpy.data.objects[name]
 S.frame_set(cam.get('presentation_frame',1));bpy.context.view_layer.update()
 S.render.resolution_x=int(300*cam.get('aspect_width',16));S.render.resolution_y=int(300*cam.get('aspect_height',9))
 dg=bpy.context.evaluated_depsgraph_get();corners=cam.data.view_frame(scene=S)
 xmin=min(p.x for p in corners);xmax=max(p.x for p in corners);ymin=min(p.y for p in corners);ymax=max(p.y for p in corners);zz=corners[0].z
 origin=cam.matrix_world.translation;hits=[]
 for iy in range(11):
  for ix in range(15):
   u=.05+ix*.9/14;v=.05+iy*.9/10;direction=cam.matrix_world.to_quaternion()@Vector((xmin*(1-u)+xmax*u,ymin*(1-v)+ymax*v,zz)).normalized()
   ray_origin=origin.copy();hit=False
   for retry in range(30):
    hit,loc,n,idx,ob,mat=S.ray_cast(dg,ray_origin,direction,distance=100)
    if not hit or not ob.hide_render:break
    ray_origin=loc+direction*.0001
   if hit:hits.append({'sample':[ix,iy],'object':ob.name,'distance_m':float((loc-origin).length),'door':ob.name in movnames})
 checks.append({'name':name,'source_position':[origin.x,origin.z,-origin.y],'lens_mm':cam.data.lens,'aspect':[cam.get('aspect_width',16),cam.get('aspect_height',9)],'presentation_frame':S.frame_current,'door_opens':{r.name:float(r['open']) for r in rigs},'ray_grid':[15,11],'moving_door_coverage_fraction':sum(h['door'] for h in hits)/165,'near_obstruction':any(h['distance_m']<.035 for h in hits),'minimum_distance_m':min(h['distance_m'] for h in hits),'central_first_hit':next((h for h in hits if h['sample']==[7,5]),None),'door_hits':[h for h in hits if h['door']]})
out=Path(r'D:\2026\42\review99\door_hands\cameras.json')
out.write_text(json.dumps({'source':bpy.data.filepath,'sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'checks':checks},ensure_ascii=False,indent=2),'utf8')
print('HANDS_CAMERAS',json.dumps([{k:v for k,v in c.items() if k!='door_hits'} for c in checks],ensure_ascii=True),flush=True)
