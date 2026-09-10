import bpy,os
from mathutils import Vector
S=bpy.context.scene
def cv(p):return Vector((p[0],-p[2],p[1]))
for name,p,target,lens in [('REV | Baño mono',[19.85,1.85,4.60],[21.10,1.10,5.13],22),('REV | Baño quincho',[21.23,1.80,11.50],[21.18,1.10,10.5],22)]:
 o=bpy.data.objects.get(name)
 if not o:
  d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);bpy.data.collections['CAMERAS'].objects.link(o)
 o.location=cv(p);o.rotation_euler=(cv(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=lens;o.data.clip_start=.035;o['presentation_frame']=150
S.frame_set(1);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas']
S['review_iteration']='95 / R6F coordinated photographic candidate';S['architect_review_approval']='PENDING_GLOBAL_9_5';S['video_render_requires_explicit_approval']=True
print('R6F_PRESENTATION_SET_NO_GEOMETRY_CHANGE')
