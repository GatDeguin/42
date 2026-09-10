import bpy,os,json,math
from mathutils import Matrix
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1)
def cube(p,d):
 bpy.ops.mesh.primitive_cube_add(size=1,location=(p[0],-p[2],p[1]));o=bpy.context.object;o.dimensions=(d[0],d[2],d[1]);bpy.context.view_layer.update();return o
def cut(o,c):
 bpy.context.view_layer.objects.active=o;md=o.modifiers.new('Interior hueco de extracción','BOOLEAN');md.operation='DIFFERENCE';md.object=c;bpy.ops.object.modifier_apply(modifier=md.name)
c=cube([21.25,2.17,6.75],[.10,1.14,.10]);cut(bpy.data.objects['Chimenea horno'],c);bpy.data.objects.remove(c,do_unlink=True)
c=cube([21.17,2.105,9.44],[1.23,1.10,.92]);cut(bpy.data.objects['Parrilla campana'],c);bpy.data.objects.remove(c,do_unlink=True)
bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.147,depth=.9,location=(21.65,-9.12,2.65),rotation=(math.pi/2,0,0));c=bpy.context.object;cut(bpy.data.objects['Parrilla campana'],c);bpy.data.objects.remove(c,do_unlink=True)
# Explicit sheet/insulation thicknesses. Preserve the outer roof surfaces exactly.
for name in ['Cubierta pendiente Cedro Misionero','Cubierta pendiente pileta']:
 o=bpy.data.objects[name];low=min(v.co.z for v in o.data.vertices);high=max(v.co.z for v in o.data.vertices);ratio=.0008/(high-low)
 o.data.transform(Matrix.Translation((0,0,high*(1-ratio)))@Matrix.Diagonal((1,1,ratio,1)));o['sheet_thickness_m']=.0008
for name in ['Estudio | aislación y membrana bajo chapa','Vivienda | aislación y membrana bajo chapa']:
 o=bpy.data.objects[name];low=min(v.co.z for v in o.data.vertices);high=max(v.co.z for v in o.data.vertices);ratio=.080/(high-low)
 o.data.transform(Matrix.Translation((0,0,high*(1-ratio)))@Matrix.Diagonal((1,1,ratio,1)));o.location.z+=.067;o['insulation_thickness_m']=.08
for o in S.objects:
 if o.name.startswith('Chapa | nervadura'):o.location.z+=.025
m=next(m for m in bpy.data.materials if m.get('source_material_key')=='roof');bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
for socket in ['Base Color','Roughness']:
 for link in list(bs.inputs[socket].links):m.node_tree.links.remove(link)
bs.inputs['Base Color'].default_value=(.029,.032,.034,1);bs.inputs['Roughness'].default_value=.43;bs.inputs['Metallic'].default_value=.55
# Weather-resistant metal cover on the portion of service shaft above the roof.
black=next(m for m in bpy.data.materials if m.get('source_material_key')=='blackMetal')
for p,d,n in [([21.302,8.09,5.5],[.012,.32,.86],'frente'),([21.565,8.09,5.066],[.54,.32,.012],'lateral anterior'),([21.565,8.09,5.934],[.54,.32,.012],'lateral posterior')]:
 o=cube(p,d);o.name='Patinillo | remate exterior '+n;o.data.materials.append(black)
 for co in list(o.users_collection):co.objects.unlink(o)
 bpy.data.collections['VENTILATION'].objects.link(o)
notes=json.loads(S['corrections']);notes.append('Roof detail resolved as0.8mm external metal skin over80mm insulation, with visible standing seams; original outside planes preserved after user-authorized0.60m module step. Existing oven chimney and grill hood now have true hollow interiors continuous with new flues; exposed shaft receives metal weathering cover.')
S['corrections']=json.dumps(notes,ensure_ascii=False);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_Revision.blend'),compress=True)
print('CONSTRUCTION_ENCOUNTERS_REFINED',flush=True)
