"""Add one source-matched pool photograph from inside the garden; no geometry change."""
import bpy,json,math
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
NAME='LUZ99 | Pileta desde jardin'
def apply():
 S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();o=bpy.data.objects.get(NAME)
 if o is None:
  d=bpy.data.cameras.new(NAME);o=bpy.data.objects.new(NAME,d);c=bpy.data.collections.get('LUZ99_LIGHTING');(c.objects if c else S.collection.objects).link(o)
 o.location=(10.0,-14.25,1.72);target=Vector((16.5,-16.5,.35));o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
 d=o.data;d.lens=25;d.sensor_width=36;d.sensor_height=24;d.sensor_fit='HORIZONTAL';d.clip_start=.035;d.clip_end=1000;d.shift_x=d.shift_y=0;d.dof.use_dof=False
 o['presentation_frame']=1;o['supplemental_camera']=True;o['aspect_width']=4;o['aspect_height']=3;o['photographic_exposure_compensation_ev']=0.;o['camera99_note']='R8: garden-side human-height pool view; complete near coping visible. Original pool camera retained.'
 S.render.resolution_x=2000;S.render.resolution_y=1500;bpy.context.view_layer.update()
 points=[Vector((x,-z,.10)) for x in [13,20] for z in [15,18]];p=[list(world_to_camera_view(S,o,q)) for q in points];assert all(.025<x<.975 and .025<y<.975 and z>0 for x,y,z in p),p
 # A ray to each point along the near coping must not cross an unrelated object.
 dg=bpy.context.evaluated_depsgraph_get();rays=[]
 for i in range(25):
  q=Vector((13.05+6.90*i/24,-15.035,.11));delta=q-o.location;dist=delta.length;hit,loc,normal,index,ob,matrix=S.ray_cast(dg,o.location,delta.normalized(),distance=dist-.04)
  rays.append({'sample':i,'point':list(q),'blockingObject':ob.name if hit else None,'distanceBeforeTarget':dist-(loc-o.location).length if hit else None})
 checks={'positionBlender':list(o.location),'heightAboveGarden_m':o.location.z-.04,'lens_mm':d.lens,'nearCopingSamples':rays,'poolCornerNDC':p,'blocking':[r for r in rays if r['blockingObject']],'preservedOriginalCamera':'CAM | Pileta & playa húmeda'}
 assert not checks['blocking'],checks['blocking'];S['r8_pool_camera']=json.dumps(checks);return checks
