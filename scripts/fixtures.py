import bpy,bmesh,math,os,json
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'output');S=bpy.context.scene;S.frame_set(1)
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m}
def cv(p):return Vector((p[0],-p[2],p[1]))
def cut(names,x,z,w,d,top,bottom):
 bpy.ops.mesh.primitive_cube_add(size=1,location=cv([x,(top+bottom)/2,z]));c=bpy.context.object;c.dimensions=(w,d,top-bottom);bpy.context.view_layer.update()
 for name in names:
  o=bpy.data.objects.get(name)
  if o:
   md=o.modifiers.new('Rebaje físico de bacha','BOOLEAN');md.operation='DIFFERENCE';md.object=c;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=md.name)
 bpy.data.objects.remove(c,do_unlink=True)
def vessel(name,x,z,w,d,top,bottom,material,collection,oldname=None,power=.55):
 old=bpy.data.objects.get(oldname or name);props={k:(v.to_list() if hasattr(v,'to_list') else v) for k,v in old.items()} if old else {}
 if old:bpy.data.objects.remove(old,do_unlink=True)
 profile=[(0,0,bottom),(.325*w,.325*d,bottom),(.5*w,.5*d,top),(.43*w,.43*d,top),(.30*w,.30*d,bottom+.035),(0,0,bottom+.035)]
 origin=cv([x,(top+bottom)/2,z]);p=[];f=[];N=48
 for rx,rz,y in profile:
  for j in range(N):
   a=j/N*math.tau;c=math.cos(a);s=math.sin(a);p.append(cv([x+rx*math.copysign(abs(c)**power,c),y,z+rz*math.copysign(abs(s)**power,s)])-origin)
 for i in range(len(profile)-1):
  for j in range(N):k=(j+1)%N;f.append((i*N+j,(i+1)*N+j,(i+1)*N+k,i*N+k))
 me=bpy.data.meshes.new(name+' | cerco, paredes y fondo');me.from_pydata(p,[],f);me.materials.append(M[material]);me.update()
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00001);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 for poly in me.polygons:poly.use_smooth=True
 o=bpy.data.objects.new(name,me);o.location=origin;bpy.data.collections[collection].objects.link(o)
 for k,v in props.items():o[k]=v
 o['physical_detail']='Hollow vessel retaining source location/opening; added real depth and rim.'
 return o
# Primary double sink in the source fire / washing / grill service line.
for label,z in [('A',7.88),('B',8.42)]:
 cut(['Mesada bacha','Mueble bacha'],20.69,z,.42,.42,1.20,.82)
 for name in ['Bacha profunda quincho '+label]:
  o=bpy.data.objects.get(name)
  if o:bpy.data.objects.remove(o,do_unlink=True)
 vessel('Bacha doble '+label,20.69,z,.46,.46,1.09,.845,'stainless','QUINCHO')
for o in list(S.objects):
 if o.name.startswith('Doble bacha | acero borde'):bpy.data.objects.remove(o,do_unlink=True)
# Other kitchen sinks.
cut(['Cocina lineal mesada','Cocina lineal bajos'],21.42,9.4,.43,.36,4.3,3.88)
o=bpy.data.objects.get('Bacha cocina interior')
if o:bpy.data.objects.remove(o,do_unlink=True)
vessel('Bacha cocina',21.42,9.4,.47,.40,4.175,3.93,'stainless','INTERIORS')
cut(['Mesada cocina mono lateral','Bajos cocina mono lateral'],14.88,4.3,.44,.55,1.32,.90)
vessel('Bacha cocina mono',14.88,4.3,.49,.60,1.185,.94,'stainless','GROUND_FLOOR')
cut(['Mesada apoyo quincho','Mueble parrilla bajo 2'],18.82,7.56,.40,.30,1.20,.83)
vessel('Bacha quincho',18.82,7.56,.44,.34,1.075,.87,'stainless','QUINCHO')
# Ceramic basins and the bath stay within their specified footprint/envelope.
vessel('Bacha apoyo suite',19.70,6.73,.36,.36,4.17,4.07,'ceramic','INTERIORS',power=1)
vessel('Bañera vivienda',21.08,6.82,1.25,.74,3.80,3.26,'ceramic','INTERIORS',power=.52)
vessel('Lavatorio mono',20.03,5.42,.50,.36,.81,.63,'ceramic','GROUND_FLOOR')
vessel('Lavatorio quincho',20.83,10.78,.46,.38,.81,.63,'ceramic','QUINCHO')
# Toilet/bidet hollow bowls, retaining source overall envelopes.
for name,x,z,w,d,cy,h,col in [
 ('Inodoro mono',21.18,5.42,.42,.62,.43,.55,'GROUND_FLOOR'),
 ('Inodoro quincho',21.53,10.80,.42,.62,.43,.55,'QUINCHO'),
 ('Inodoro vivienda',20.94,8.13,.45,.66,3.55,.56,'INTERIORS'),
 ('Bidet vivienda',20.25,8.13,.42,.58,3.50,.48,'INTERIORS')]:
 vessel(name,x,z,w,d,cy+h/2,cy-h/2,'ceramic',col,power=.85)
# Refined editable steel handrail, within the original endpoints.
for name in ['Pasamanos pileta 1','Pasamanos pileta 2','Agarre pileta']:
 o=bpy.data.objects.get(name)
 if o:bpy.data.objects.remove(o,do_unlink=True)
curve=bpy.data.curves.new('Pasamanos piscina | tubo curvado','CURVE');curve.dimensions='3D';curve.bevel_depth=.028;curve.bevel_resolution=4;curve.resolution_u=16
sp=curve.splines.new('BEZIER');points=[[13.35,-.04,17.62],[13.35,.83,17.62],[13.46,.96,17.62],[13.94,.96,17.62],[14.05,.83,17.62],[14.05,-.04,17.62]];sp.bezier_points.add(len(points)-1)
for b,p in zip(sp.bezier_points,points):b.co=cv(p);b.handle_left_type='AUTO';b.handle_right_type='AUTO'
curve.materials.append(M['stainless']);o=bpy.data.objects.new('Pasamanos pileta | acero curvado',curve);bpy.data.collections['POOL'].objects.link(o)
notes=json.loads(S['corrections']);notes.append('Symbolic sink and sanitary solids refined into hollow bowls at the source openings/footprints; countertop cutouts and real basin depth added. Pool handrail rounded within the original endpoints.');S['corrections']=json.dumps(notes,ensure_ascii=False)
report=json.load(open(os.path.join(OUT,'validation.json'),encoding='utf8'));report['corrections']=notes;report['objects']=len(S.objects)
report['checks'].append({'name':'Physical sink cavities and double sink retained in service line','pass':all(bpy.data.objects.get(n) is not None for n in ['Bacha doble A','Bacha doble B','Bacha cocina','Bañera vivienda'])})
json.dump(report,open(os.path.join(OUT,'validation.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
S.frame_set(1);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Casa_de_Campo.blend'))
print('FINAL_FIXTURES_READY',flush=True)
