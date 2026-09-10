import bpy,json
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
p='D:/2026/42/scripts/correcciones95_rociador_final.py';exec(compile(open(p,encoding='utf8').read(),p,'exec'),{'__file__':p,'__name__':'__main__'})
S=bpy.context.scene;c=bpy.data.objects['REV | Baño mono'];S.camera=c;S.render.resolution_x=1800;S.render.resolution_y=1350;S.frame_set(150)
def cv(v):return Vector((v[0],-v[2],v[1]))
c.location=cv([19.74,1.72,4.92]);c.rotation_euler=(cv([21.30,1.31,4.90])-c.location).to_track_quat('-Z','Y').to_euler();c.data.lens=19;bpy.context.view_layer.update()
r=[]
for name in ['Ducha baño mono','BTH95 | ducha cuerpo sifón','Lavabo baño mono','BTH95 | ducha mezclador']:
 o=bpy.data.objects.get(name)
 if not o:continue
 pts=[world_to_camera_view(S,c,o.matrix_world@Vector(v)) for v in o.bound_box]
 r.append({'name':name,'x':[min(p.x for p in pts),max(p.x for p in pts)],'y':[min(p.y for p in pts),max(p.y for p in pts)]})
print('FRAMING',r)
