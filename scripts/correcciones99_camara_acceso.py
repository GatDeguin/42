"""Add the real living-room approach camera without changing architecture or existing views."""
import bpy,json
from mathutils import Vector
NAME='LUZ99 | Acceso dormitorio desde estar'
def apply():
 scene=bpy.context.scene
 cam=bpy.data.objects.get(NAME)
 if cam is None:
  cam=bpy.data.objects.new(NAME,bpy.data.cameras.new(NAME))
  collection=bpy.data.collections.get('LUZ99_LIGHTING') or scene.collection
  collection.objects.link(cam)
 p=(17.08,4.85,10.55);t=(16.20,4.85,7.32)
 cam.location=(p[0],-p[2],p[1]);target=Vector((t[0],-t[2],t[1]))
 cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
 cam.data.lens=20;cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL';cam.data.shift_y=-.12;cam.data.shift_x=0;cam.data.clip_start=.035;cam.data.clip_end=250;cam.data.dof.use_dof=False
 cam['presentation_frame']=150;cam['aspect_width']=4;cam['aspect_height']=3;cam['supplemental_camera']=True;cam['photographic_exposure_compensation_ev']=0.0
 cam['camera99_note']='View from living-room approach through the actual bedroomDining opening, with both doors open. Horizontal optical axis preserves verticals; lens shift includes floor.'
 bpy.context.view_layer.update()
 return {'name':NAME,'position_source':list(p),'target_source':list(t),'lens_mm':20,'shift_y':-.12,'presentation_frame':150,'aspect':[4,3],'video_rendered':False}
