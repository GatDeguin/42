"""Read-only camera metadata. Blender camera local axes equal Three: -Z forward, +Y up."""
import bpy,math
from mathutils import Matrix,Vector
C=Matrix(((1,0,0,0),(0,0,1,0),(0,-1,0,0),(0,0,0,1)))
def camera_optics(scene):
    result=[];saved_frame=scene.frame_current
    try:
        for obj in scene.objects:
            if obj.type!='CAMERA' or not obj.name.startswith(('CAM | ','REV | ')):continue
            frame=int(obj.get('presentation_frame',1));scene.frame_set(frame);bpy.context.view_layer.update()
            camera=obj.data
            if camera.type!='PERSP':continue
            corners=[v/abs(v.z) for v in camera.view_frame(scene=scene)]
            left,right=min(v.x for v in corners),max(v.x for v in corners)
            bottom,top=min(v.y for v in corners),max(v.y for v in corners)
            position=C@obj.matrix_world.translation;rotation=(C@obj.matrix_world).to_quaternion()
            target=position+(rotation@Vector((0,0,-1)))*4
            result.append(dict(name=obj.name,position=list(position),target=list(target),quaternion=[rotation.x,rotation.y,rotation.z,rotation.w],fov=math.degrees(2*math.atan((top-bottom)/2)),frustum=dict(left=left,right=right,bottom=bottom,top=top),sourceAspect=(right-left)/(top-bottom),presentationFrame=frame,lensMm=camera.lens,sensorFit=camera.sensor_fit,sourceResolution=[scene.render.resolution_x,scene.render.resolution_y],pixelAspect=[scene.render.pixel_aspect_x,scene.render.pixel_aspect_y]))
    finally:scene.frame_set(saved_frame);bpy.context.view_layer.update()
    return result
