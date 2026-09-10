"""R6B implements the critic's coordinated monoambiente plan, preserving walls and door rigs."""
import bpy,os,math,json,ast,numpy as np,sys
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
for m in bpy.data.materials:
 if m.name.startswith('MAT95 | '):M[m.name.split(' | ',1)[1]]=m
 if m.name.startswith('FIT95 | '):M[m.name.split(' | ',1)[1]]=m
def cv(p):return Vector((p[0],-p[2],p[1]))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_textiles.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['bounds','deform','map_h']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_materialidad.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['box','cyl','mesh','curve']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<fast>','exec'))
def bb(name,x,h,z,mat='woodDark',bev=.002):
 return box(name,[(x[0]+x[1])/2,(h[0]+h[1])/2,(z[0]+z[1])/2],[x[1]-x[0],h[1]-h[0],z[1]-z[0]],mat,'GROUND_FLOOR',bev)
def cut(o,c):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;m=o.modifiers.new('Reserva fabricada R6B','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=c;bpy.ops.object.modifier_apply(modifier=m.name)
def erase(prefixes):
 for o in list(S.objects):
  if o.name.startswith(tuple(prefixes)):bpy.data.objects.remove(o,do_unlink=True)
erase(['Bajos cocina mono','Mesada cocina mono','Frente cocina mono','Tirador cocina mono','Zócalo cocina mono','Isla cocina mono','Canto mesada isla mono','Voladizo isla mono','Luz bajo alacena mono','Heladera mono','Grifería cocina mono'])
# Countertop is one closedL-shaped mesh, not two intersecting blocks.
outline=[(14.24,3.20),(14.86,3.20),(14.86,5.20),(15.78,5.20),(15.78,5.82),(14.24,5.82)];N=len(outline)
vs=[cv([x,h,z]) for h in [1.075,1.110] for x,z in outline];fs=[tuple(range(N)),tuple(range(2*N-1,N-1,-1))]
for i in range(N):j=(i+1)%N;fs.append((i,N+i,N+j,j))
counter=mesh('Mesada cocina mono lateral',vs,fs,'concrete','GROUND_FLOOR');be=counter.modifiers.new('Canto2mm','BEVEL');be.width=.002;be.segments=2
# Open carcasses with18mm walls, bottom and partitions;100mm recessed plinth.
bb('Bajos cocina mono lateral | fondo',[14.26,14.278],[.31,1.075],[3.22,5.80])
bb('Bajos cocina mono lateral | piso',[14.26,14.82],[.31,.328],[3.22,5.80])
for z in [3.229,3.82,4.45,5.19,5.791]:bb('Bajos cocina mono lateral | lateral',[14.26,14.82],[.328,1.075],[z-.009,z+.009])
# Straps support countertop without closing sink space.
for z in [3.24,3.79,4.48,5.17,5.77]:bb('Bajos cocina mono lateral | travesaño',[14.26,14.82],[1.045,1.075],[z-.022,z+.022])
bb('Zócalo cocina mono lateral',[14.26,14.76],[.21,.31],[3.28,5.74],'blackMetal')
bb('Bajos cocina mono fondo | piso',[14.86,15.76],[.31,.328],[5.24,5.80])
bb('Bajos cocina mono fondo | respaldo',[14.86,15.76],[.328,1.075],[5.782,5.80])
for x in [14.869,15.751]:bb('Bajos cocina mono fondo | lateral',[x-.009,x+.009],[.328,1.075],[5.24,5.80])
for z in [5.26,5.77]:bb('Bajos cocina mono fondo | travesaño',[14.86,15.76],[1.045,1.075],[z-.02,z+.02])
bb('Zócalo cocina mono fondo',[14.90,15.70],[.21,.31],[5.30,5.75],'blackMetal')
# Doors now face the working aisle. Handles do not exceed countertop envelope.
for i,(za,zb) in enumerate([(3.23,3.805),(3.835,4.435),(4.465,5.18)],1):
 bb('Frente cocina mono lateral '+str(i),[14.816,14.834],[.33,1.055],[za,zb],'wood',.002)
 z=(za+zb)/2
 for h in [.70,.91]:cyl('Tirador cocina mono lateral | separador',[14.834,h,z],[14.849,h,z],.0035,'stainless','GROUND_FLOOR')
 cyl('Tirador cocina mono lateral '+str(i),[14.849,.70,z],[14.849,.91,z],.004,'stainless','GROUND_FLOOR')
for i,(xa,xb) in enumerate([(14.87,15.302),(15.318,15.75)],1):
 bb('Frente cocina mono fondo '+str(i),[xa,xb],[.33,1.055],[5.223,5.241],'wood',.002)
 x=(xa+xb)/2
 for xx in [x-.11,x+.11]:cyl('Tirador cocina mono fondo | separador',[xx,.94,5.223],[xx,.94,5.207],.0035,'stainless','GROUND_FLOOR')
 cyl('Tirador cocina mono fondo '+str(i),[x-.11,.94,5.207],[x+.11,.94,5.207],.004,'stainless','GROUND_FLOOR')
# Source basin is resized and repositioned as one complete hollow shell.
sink=bpy.data.objects['Bacha cocina mono'];a,b=bounds(sink)
deform(sink,lambda p:cv([14.34+(p.x-a[0])*.44/(b[0]-a[0]),.875+(p.z-a[2])*.240/(b[2]-a[2]),3.68+(-p.y+b[1])*.60/(b[1]-a[1])]))
c=bb('TEMP hueco bacha',[14.355,14.765],[.85,1.14],[3.70,4.26],'blackMetal',.025);cut(counter,c);bpy.data.objects.remove(c,do_unlink=True)
curve('Grifería cocina mono | caño',[[14.31,1.11,4.00],[14.31,1.39,4.00],[14.50,1.39,4.00],[14.56,1.28,4.00]],.012,'stainless','GROUND_FLOOR')
cyl('Grifería cocina mono | base',[14.31,1.11,4],[14.31,1.145,4],.027,'stainless','GROUND_FLOOR')
cyl('Grifería cocina mono | palanca',[14.31,1.16,3.975],[14.31,1.19,3.915],.004,'stainless','GROUND_FLOOR')
# Hob retains its role and uses a flat ceramic surface with printed cooking zones.
erase(['Anafe cocina mono'])
bb('Anafe cocina mono',[15.06,15.64],[1.110,1.125],[5.24,5.70],'vidrio vitrocerámico',.002)
for x in [15.19,15.50]:
 for z in [5.36,5.59]:
  curve('MOB95 | inducción mono serigrafía',[[x+.085*math.cos(k*math.tau/72),1.1253,z+.085*math.sin(k*math.tau/72)] for k in range(73)],.0005,'serigrafía tenue','GROUND_FLOOR')
# A recirculating hood is a declared proposed appliance, with removable filters; no invented flue through studio.
bb('MOB95 | campana mono recirculación',[15.045,15.655],[1.775,1.905],[5.40,5.81],'blackMetal',.004)
for x in [15.10,15.60]:bb('MOB95 | campana mono soporte',[x-.014,x+.014],[1.82,1.86],[5.78,5.90],'blackMetal',.001)
for j in range(17):
 z=5.43+j*.021;bb('MOB95 | filtro campana mono',[15.10,15.60],[1.775,1.776],[z,z+.004],'stainless',.0003)
# Refrigerator is clear of the L and opens towards the room, with its own ventilation gaps.
bb('Heladera mono',[15.84,16.54],[.21,2.28],[5.12,5.82],'blackMetal',.004)
bb('Heladera mono puerta superior',[15.855,16.525],[.83,2.245],[5.098,5.120],'blackMetal',.003)
bb('Heladera mono puerta congelador',[15.855,16.525],[.26,.816],[5.098,5.120],'blackMetal',.003)
for h in [.252,.823,2.252]:bb('Heladera mono | junta',[15.854,16.526],[h-.003,h+.003],[5.115,5.122],'rubber95',.0005)
for h in [1.24,1.59]:cyl('Heladera mono | soporte tirador',[15.90,h,5.099],[15.90,h,5.081],.004,'stainless','GROUND_FLOOR')
cyl('Heladera mono | tirador',[15.90,1.24,5.081],[15.90,1.59,5.081],.005,'stainless','GROUND_FLOOR')
# Compact island retains two stools and250mm knee overhang. Cabinet fronts face rear working aisle.
bb('Isla cocina mono tapa',[15.96,17.68],[1.075,1.110],[3.32,4.00],'concrete',.003)
bb('Isla cocina mono base | fondo',[16.00,17.64],[.31,1.075],[3.57,3.588])
bb('Isla cocina mono base | piso',[16.00,17.64],[.31,.328],[3.588,3.96])
for x in [16.009,16.82,17.631]:bb('Isla cocina mono base | costilla',[x-.009,x+.009],[.328,1.075],[3.588,3.96])
for z in [3.595,3.93]:bb('Isla cocina mono base | travesaño',[16.00,17.64],[1.045,1.075],[z-.02,z+.02])
bb('Isla cocina mono base | zócalo',[16.06,17.58],[.21,.31],[3.63,3.90],'blackMetal')
for i in range(4):
 xa=16.008+i*.407;xb=xa+.397
 bb('Isla cocina mono frente '+str(i),[xa,xb],[.33,1.055],[3.957,3.975],'wood',.002)
 x=(xa+xb)/2;cyl('Isla cocina mono tirador',[x-.10,.94,3.984],[x+.10,.94,3.984],.004,'blackMetal','GROUND_FLOOR')
# Reposition entire movable assemblies and their supports, keeping their corrected heights.
for o in S.objects:
 if o.name.startswith('Sofá cama mono'):o.location.y+=.70
 if o.name.startswith(('Mesa mono ','Silla mono ','MOB95 | faldón mesa mono')):o.location+=cv([1.15,0,-.74])
 if o.name.startswith('Taburete isla mono'):o.location.y+=.77
 if ('isla mono' in o.name.lower() and ('colgante' in o.name.lower() or 'cable' in o.name.lower())):o.location.y+=.89
# Place actual illumination at the new work zones; direct light remains associated with fixture positions.
for o in S.objects:
 if o.type=='LIGHT' and 'isla' in o.name.lower() and 'mono' in o.name.lower():o.location.y+=.89
S['mono_layout_r6']=json.dumps({'counter_lateral':[14.24,3.20,14.86,5.82],'counter_return':[14.86,5.20,15.78,5.82],'counter_top_y':1.11,'fridge':[15.84,5.10,16.54,5.82],'island':[15.96,3.32,17.68,4.00],'sofa_delta_z':-.70,'dining_delta':[1.15,-.74],'stools_delta_z':-.77,'reference':'audit/integral95_02_mono_layout_proposal.json','hood':'Proposed recirculating hood; selection/air renewal to be designed. No new through-studio exhaust route claimed.'},ensure_ascii=False)
S['review_iteration']='95 / R6B functional monoambiente layout';S['tour_route_requires_revalidation_after_layout']=True
S.frame_set(1);bpy.context.view_layer.update();bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
name='Casa_de_Campo_95_R6B_preview.blend' if '--preview' in sys.argv else 'Casa_de_Campo_95_R6B.blend'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output',name),compress=True);print('R6B_SAVED',flush=True)
