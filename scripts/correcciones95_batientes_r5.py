"""R5A: real leaf/frame geometry and collision-free fixed fittings. Proposed construction, not engineering certification."""
import bpy,os,math,json,ast,numpy as np
from mathutils import Vector,Matrix
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
for m in bpy.data.materials:
 if m.name.startswith('MAT95 | '):M[m.name.split(' | ',1)[1]]=m
def cv(p):return Vector((p[0],-p[2],p[1]))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_textiles.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['bounds','deform','map_h']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_materialidad.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['box','cyl']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<fast>','exec'))
def bb(name,x,h,z,mat='blackMetal',col='STUDIO',bev=.001):
 return box(name,[(x[0]+x[1])/2,(h[0]+h[1])/2,(z[0]+z[1])/2],[x[1]-x[0],h[1]-h[0],z[1]-z[0]],mat,col,bev)
def child(o,rig):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=rig;o.matrix_world=mw;return o
def erase(prefixes):
 for o in list(S.objects):
  if o.name.startswith(tuple(prefixes)):bpy.data.objects.remove(o,do_unlink=True)
def cut(o,c):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;m=o.modifiers.new('Reserva constructiva R5','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=c;bpy.ops.object.modifier_apply(modifier=m.name)
# Studio keeps the900mm rough opening; hinges project60mm into room to preserve805mm usable width.
rig=bpy.data.objects['DOOR | studio']
for o in list(rig.children_recursive):bpy.data.objects.remove(o,do_unlink=True)
erase(['Marco puerta estudio','Tapajunta puerta estudio','Burlete perimetral estudio'])
rig.location=cv([14.260,3.25,5.750])
for fc in rig.animation_data.drivers:
 if fc.data_path=='rotation_euler':fc.driver.expression='opening * -1.5707963267948966'
bpy.context.view_layer.update()
child(bb('Puerta acceso estudio',[14.195,14.260],[3.26,5.60],[4.885,5.740],'woodDark'),rig)
# Three-sided rebated frame. The rear return finishes behind leaf's closed edge.
bb('Marco puerta estudio frente',[14.000,14.265],[3.25,5.64],[4.850,4.880])
bb('Marco puerta estudio fondo base',[14.000,14.190],[3.25,5.64],[5.720,5.750])
bb('Marco puerta estudio fondo retorno',[14.190,14.265],[3.25,5.64],[5.745,5.780])
bb('Marco puerta estudio superior',[14.000,14.265],[5.605,5.640],[4.850,5.780])
# Closing stops and EPDM gasket touch the outward leaf face in the closed position only.
for name,z in [('frente',[4.880,4.905]),('fondo',[5.716,5.740])]:
 bb('Marco puerta estudio galce '+name,[14.172,14.189],[3.26,5.605],z)
 bb('Burlete perimetral estudio '+name,[14.189,14.195],[3.26,5.600],z,'rubber95',bev=.0005)
bb('Marco puerta estudio galce superior',[14.172,14.189],[5.578,5.610],[4.88,5.74])
bb('Burlete perimetral estudio superior',[14.189,14.195],[5.578,5.600],[4.905,5.716],'rubber95',bev=.0005)
# Slim lower seal and aluminum carrier are attached to the door.
child(bb('Puerta estudio | portaburlete inferior',[14.219,14.237],[3.260,3.275],[4.892,5.733],'blackMetal',bev=.0005),rig)
child(bb('Puerta estudio | labio elastomérico inferior',[14.225,14.231],[3.250,3.263],[4.892,5.733],'rubber95',bev=.0002),rig)
# Hinge knuckles use separated axial segments around one pin. Plates bear on leaf/frame.
for h in [3.52,4.40,5.32]:
 bb('Herraje estudio | placa fija',[14.253,14.265],[h-.045,h+.045],[5.754,5.785])
 child(bb('Herraje estudio | placa hoja',[14.260,14.263],[h-.044,h+.044],[5.695,5.744]),rig)
 cyl('Herraje estudio | eje',[14.260,h-.045,5.750],[14.260,h+.045,5.750],.0025,'stainless','STUDIO')
 for j in range(3):
  a=h-.045+j*.030+.001;b=a+.028
  o=cyl('Herraje estudio | nudillo '+('hoja' if j==1 else 'marco'),[14.260,a,5.750],[14.260,b,5.750],.0055,'stainless','STUDIO')
  if j==1:child(o,rig)
 # Connecting webs connect the knuckle to each plate without overlapping each other.
 child(bb('Herraje estudio | ala móvil',[14.260,14.263],[h-.014,h+.014],[5.736,5.750]),rig)
 for a,b in [(h-.044,h-.017),(h+.017,h+.044)]:bb('Herraje estudio | ala fija',[14.257,14.263],[a,b],[5.750,5.758])
# Short lever handles: spindle, roses and90mm lever on both sides.
for side,face,out in [('exterior',14.195,-1),('interior',14.260,1)]:
 z=5.00;h=4.34
 child(cyl('Manija puerta estudio '+side+' roseta',[face,h,z],[face+out*.006,h,z],.027,'stainless','STUDIO'),rig)
 child(cyl('Manija puerta estudio '+side+' vástago',[face+out*.006,h,z],[face+out*.040,h,z],.007,'stainless','STUDIO'),rig)
 child(cyl('Manija puerta estudio '+side,[face+out*.040,h,z],[face+out*.040,h,z+.095],.007,'stainless','STUDIO'),rig)
# Extend existing threshold to interior frame plane, keeping finished level+3.25.
o=bpy.data.objects['Umbral puerta estudio'];a,b=bounds(o)
deform(o,lambda p:Vector((a[0]+(p.x-a[0])*(14.270-a[0])/(b[0]-a[0]),p.y,p.z)))
# Preserve acoustic treatment while clearing the leaf and handle swing.
bpy.data.objects['Panel acústico trasero 1'].location.x+=.13
# Side skirting must stop at the opening and the leaf sweep behind it.
c=bb('TEMP studio opening skirting',[13.85,14.29],[3.20,3.45],[4.84,5.785],col='REFERENCE',bev=0)
for o in list(S.objects):
 if o.type=='MESH' and 'zócalo' in o.name.lower():
  a,b=bounds(o);ca,cb=bounds(c)
  if np.all(np.minimum(b,cb)-np.maximum(a,ca)>.0001):cut(o,c)
bpy.data.objects.remove(c,do_unlink=True)
# Exterior wall lights cannot occupy a door opening or sliding handle route.
for name in ['Aplique descanso','Aplique descanso | difusor inferior','Aplique descanso | difusor superior','LED | Aplique descanso']:
 o=bpy.data.objects.get(name)
 if o:o.location+=cv([-.075,0,-.80])
bb('Aplique descanso | placa de montaje',[13.9875,14.005],[4.62,4.88],[4.59,4.71],col='LIGHTS')
for name in ['Aplique exterior | carcasa.002','Aplique exterior | lavado cálido.002']:
 bpy.data.objects[name].location.z+=1.18
for name in ['Aplique exterior | carcasa.003','Aplique exterior | lavado cálido.003']:
 bpy.data.objects[name].location.x+=.17
# Positive mechanical connection from shifted bodies to wall surface.
bb('Aplique posterior alto | soporte',[17.60,17.66],[5.94,6.02],[12.0,12.06],col='LIGHTS')
bb('Aplique baño quincho | soporte',[21.82,21.88],[2.06,2.14],[11.97,12.06],col='LIGHTS')
# Towel rail relocated to north solid wall, with two standoffs.
o=bpy.data.objects['Toallero baño suite'];a,b=bounds(o);ctr=(a+b)/2
rot=Matrix.Rotation(math.pi/2,4,'Z');target=cv([20.30,4.35,6.18])
deform(o,lambda p:target+rot@(p-Vector(ctr)))
for x in [20.06,20.54]:
 cyl('Toallero baño suite | soporte',[x,4.35,6.10],[x,4.35,6.18],.011,'stainless','INTERIORS')
# Remove obsolete trims crossing the wardrobe; replace only along existing masonry piers.
erase(['Zócalo vestidor frente','Premarco suite '])
bb('Zócalo vestidor frente izquierdo',[17.70,18.055],[3.25,3.35],[8.915,8.935],col='INTERIORS')
bb('Zócalo vestidor frente derecho',[18.985,19.345],[3.25,3.35],[8.915,8.935],col='INTERIORS')
S['review_iteration']='95 / R5A usable hinged door and fixed fittings'
S['studio_door_detail95']=json.dumps({'rough_opening_m':.90,'usable_open90_m':.805,'leaf_thickness_m':.065,'hinge_source':[14.26,3.25,5.75],'leaf_height_m':2.34,'frame_head_underside':5.605,'acoustic_panel1_shift_x_m':.13,'status':'Modeled proposed assembly; no certification of acoustic rating or hardware capacity.'})
S['tour_route_requires_revalidation_after_layout']=True
S.frame_set(1);bpy.context.view_layer.update();bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_95_R5A.blend'),compress=True)
print('R5A_SAVED',flush=True)
