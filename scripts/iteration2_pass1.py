import bpy,os,json,math,ast,numpy as np
from mathutils import Vector,Matrix
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'output')
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
# Reuse only the geometric helper definitions, never the first-pass mutations.
tree=ast.parse(open(os.path.join(ROOT,'scripts','iteration1_pass1.py'),encoding='utf8').read())
for nd in tree.body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['cv','put','box','cyl','remove','cut','bounds','pipe']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helpers>','exec'))
def reset_box(name):
 o=bpy.data.objects[name];pts=np.array([v.co for v in o.data.vertices]);lo=pts.min(0);hi=pts.max(0)
 vs=[(x,y,z) for x in [lo[0],hi[0]] for y in [lo[1],hi[1]] for z in [lo[2],hi[2]]]
 fs=[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]
 me=bpy.data.meshes.new(name+' | perforaciones coordinadas');me.from_pydata(vs,[],fs)
 for m in o.data.materials:me.materials.append(m)
 o.data=me;return o
# Move both leaves onto the quincho face, outside the complete bathroom wall.
for side in ['L','R']:
 o=bpy.data.objects['DOOR | mono_'+side];o.location.y-=.44
 o['construction_note']='Shared sliding track on quincho face Z6.22; complete movable assembly clears PB bathroom.'
rail=bpy.data.objects['Monoambiente | carril doble superior'];rail.location.y-=.44
for x in [16.5,17.25,18.0,18.75,19.5]:box('Corredera PB | ménsula superior',[x,2.69,6.16],[.045,.045,.22],col='DOORS')
# Hinge pin moved outside the face; closed leaf is unchanged.
rig=bpy.data.objects['DOOR | bathroomMono'];transforms={o:o.matrix_world.copy() for o in rig.children}
rig.location.y+=.055;bpy.context.view_layer.update()
for o,mw in transforms.items():o.matrix_parent_inverse=rig.matrix_world.inverted();o.matrix_basis=mw
rig['construction_note']='Hinge pin offset55mm toward exterior face to clear entrance stub across full92degree swing.'
gate=bpy.data.objects['DOOR | gate'];gate['construction_note']='Source leaf3.00m; net between source250mm pillars2.75m. Track offset220mm into lot, slide3.05m.'
# Replace all old inferred ventilation parts; their old holes are rebuilt rather than covered.
for o in list(COL['VENTILATION'].objects):bpy.data.objects.remove(o,do_unlink=True)
for name in ['Losa entre plantas','Piso estudio','Cielorraso estudio | cota inferior 6.45m','Cubierta pendiente Cedro Misionero','Estudio | aislación y membrana bajo chapa','Cubierta pendiente pileta','Vivienda | aislación y membrana bajo chapa','Revestimiento interior | Cubierta pendiente pileta','Separación mono quincho derecha','Cielorraso vivienda | 2.60m sobre piso general']:
 if bpy.data.objects.get(name):reset_box(name)
c=box('Temporal techo baño',[20.65,5.87,7.3],[2.28,.5,2.37],col='REFERENCE',bev=0);cut(bpy.data.objects['Cielorraso vivienda | 2.60m sobre piso general'],c);bpy.data.objects.remove(c,do_unlink=True)
# Thin profiles are framed around the service shaft. No supporting beam is cut.
chan=bpy.data.objects['Estudio | canal de cielorraso 12'];chan.location.y=-(.24+4.92)/2;chan.dimensions.y=4.92-.24
box('Estudio | bastidor transversal de patinillo',[21.37,6.625,4.94],[.50,.04,.035],col='CONSTRUCTION')
box('Estudio | bastidor longitudinal de patinillo',[21.14,6.625,5.365],[.035,.04,.815],col='CONSTRUCTION')
# New paths fit between roof purlins and inside service shaft, with actual wall sleeves.
routes=[
('Horno',.105,[[21.25,2.60,6.75],[21.25,2.68,6.75],[21.16,2.70,6.56],[21.16,2.73,5.47],[21.25,2.78,5.25],[21.50,2.88,5.20],[21.50,3.08,5.20],[21.50,8.70,5.20]]),
('Parrilla',.16,[[21.49,2.65,9.44],[21.49,2.65,9.10],[21.49,2.69,6.20],[21.49,2.71,5.94],[21.50,2.78,5.68],[21.50,2.95,5.57],[21.50,3.13,5.57],[21.50,8.70,5.57]])]
wall=bpy.data.objects['Separación mono quincho derecha']
for name,r,pts in routes:
 ob=pipe('Extracción '+name+' | conducto continuo aislado',pts,r)
 x,y=(21.16,2.715) if name=='Horno' else (21.49,2.71)
 c=cyl('Temporal pasamuros',[x,y,5.7],[x,y,6.3],r+.04,col='REFERENCE');cut(wall,c);bpy.data.objects.remove(c,do_unlink=True)
 x,z=pts[-1][0],pts[-1][2]
 for nm in ['Losa entre plantas','Piso estudio','Cielorraso estudio | cota inferior 6.45m','Cubierta pendiente Cedro Misionero','Estudio | aislación y membrana bajo chapa']:
  c=cyl('Temporal paso',[x,2.9,z],[x,8.5,z],r+.027,col='REFERENCE');cut(bpy.data.objects[nm],c);bpy.data.objects.remove(c,do_unlink=True)
 h=7.0+z*1.1/6
 boot=box(name+' | babeta perforada',[x,h+.042,z],[r*2+.14,.016,r*2+.14],col='VENTILATION',bev=.001);boot.rotation_euler.x=-math.atan(1.1/6)
 c=cyl('Temporal babeta',[x,h-.3,z],[x,h+.3,z],r+.008,col='REFERENCE');cut(boot,c);bpy.data.objects.remove(c,do_unlink=True)
 for angle in [0,math.tau/3,2*math.tau/3]:
  xx=x+r*.75*math.cos(angle);zz=z+r*.75*math.sin(angle);cyl(name+' | soporte sombrerete',[xx,8.65,zz],[xx,8.85,zz],.006,col='VENTILATION')
 bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=r+.055,radius2=.025,depth=.07,location=cv([x,8.865,z]));cap=bpy.context.object;cap.name=name+' | sombrerete antilluvia';cap.data.materials.append(M['blackMetal']);put(cap,'VENTILATION')
# Hollow source grill hood with aligned new outlet.
hood=reset_box('Parrilla campana')
c=box('Temporal interior campana',[21.17,2.105,9.44],[1.23,1.10,.92],col='REFERENCE',bev=0);cut(hood,c);bpy.data.objects.remove(c,do_unlink=True)
c=cyl('Temporal toma campana',[21.49,2.65,8.7],[21.49,2.65,9.55],.147,col='REFERENCE');cut(hood,c);bpy.data.objects.remove(c,do_unlink=True)
# Service shaft leaves30mm at its anterior wall and50mm at posterior wall.
box('Patinillo extracción | frente registrable',[21.28,5.68,5.415],[.025,5.1,.78],'whitePlaster','VENTILATION')
box('Patinillo extracción | lateral anterior',[21.535,5.68,5.025],[.51,5.1,.025],'whitePlaster','VENTILATION')
box('Patinillo extracción | lateral posterior',[21.535,5.68,5.805],[.51,5.1,.025],'whitePlaster','VENTILATION')
box('Patinillo | registro estudio',[21.260,3.82,5.41],[.012,.62,.42],'whitePlaster','VENTILATION')
for p,d,n in [([21.262,8.09,5.415],[.012,.32,.82],'frente'),([21.529,8.09,5.007],[.54,.32,.012],'lateral anterior'),([21.529,8.09,5.823],[.54,.32,.012],'lateral posterior')]:box('Patinillo | remate exterior '+n,p,d,col='VENTILATION',bev=.001)
kitchen=[[21.54,5.,10.31],[21.54,5.20,10.31],[21.39,5.40,10.49],[21.39,5.62,10.49],[21.39,7.95,10.49]]
pipe('Extracción cocina | salida independiente',kitchen,.085)
for nm in ['Cielorraso vivienda | 2.60m sobre piso general','Cubierta pendiente pileta','Vivienda | aislación y membrana bajo chapa','Revestimiento interior | Cubierta pendiente pileta']:
 if bpy.data.objects.get(nm):
  c=cyl('Temporal paso cocina',[21.39,5.5,10.49],[21.39,8,10.49],.112,col='REFERENCE');cut(bpy.data.objects[nm],c);bpy.data.objects.remove(c,do_unlink=True)
boot=box('Cocina | babeta perforada',[21.39,6.744,10.49],[.33,.016,.33],col='VENTILATION',bev=.001);boot.rotation_euler.x=math.atan(1.1/6)
c=cyl('Temporal babeta',[21.39,6.4,10.49],[21.39,7.,10.49],.092,col='REFERENCE');cut(boot,c);bpy.data.objects.remove(c,do_unlink=True)
cyl('Cocina | remate superior',[21.39,7.99,10.49],[21.39,8.015,10.49],.13,col='VENTILATION')
json.dump({'routes':routes,'kitchen_route':kitchen,'shaft_source_bounds':{'x':[21.2675,21.79],'z':[5.0125,5.8175]},'studio_roof_rise':.6,'studio_clear':3.2,'dwelling_clear':2.6},open(os.path.join(ROOT,'review','construction_details.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
S['review_iteration']='2 / pass1 coordinated doors and extraction';S['video_render_requires_explicit_approval']=True
notes=json.loads(S['corrections']);notes.append('Iteration2 pass1: PB sliders moved onto quincho face and bathroom hinge offset55mm. Independent flues relocated clear of beams/purlins; former holes rebuilt and recut. Ceiling channel framed around shaft. Source gate leaf3m, actual source pillar gap2.75m.');S['corrections']=json.dumps(notes,ensure_ascii=False)
S.frame_set(1);bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Casa_de_Campo_Revision.blend'),compress=True)
print('PASS2_1_SAVED',flush=True)
