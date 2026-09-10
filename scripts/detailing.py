import bpy, math, random
from mathutils import Vector,Matrix
def enrich(g):
 D,O,box,cv,COL,M=g['DATA'],g['OBJS'],g['box'],g['cv'],g['COL'],g['MATS']
 notes=[]
 def source(name):return next((O[m['id']] for m in D['meshes'] if m['name']==name and m['id'] in O),None)
 def remove(o):
  if o:
   for k in [k for k,v in O.items() if v==o]:O.pop(k)
   bpy.data.objects.remove(o,do_unlink=True)
 # Correct the explicitly authorized conflict between source cloud positions and 3.2m clear working height.
 for m in D['meshes']:
  if m['name'].startswith(('Bafle cielorraso estudio','Cloud estudio')) or m['name']=='Luz lineal estudio':
   o=O[m['id']];o.location.z=6.45+m['scale'][1]/2;o['correction']='Lowest face raised to 6.45m; source finished floor 3.25m => 3.20m clear.'
 notes.append('Authorized: studio suspended acoustic baffles, clouds and linear fixture raised to a minimum underside of 6.45m (3.20m above the 3.25m finished floor). External roof coordinates retained.')
 # Roof lining follows the original roof planes, preserving the eave and ridge.
 for name in ['Cubierta pendiente Cedro Misionero','Cubierta pendiente pileta']:
  roof=source(name)
  if roof:
   liner=roof.copy();liner.data=roof.data.copy();liner.name='Revestimiento interior | '+name;COL['ROOF'].objects.link(liner)
   liner.data.materials.clear();liner.data.materials.append(M['whitePlaster'])
   liner.scale.y*=.22 # mesh local source height becomes Blender local Z after conversion; set using native scale below
   # use original matrix and thin vertical translation; don't change exterior roof
   liner.matrix_world=roof.matrix_world.copy();liner.scale.z*=.16;liner.location.z-=.065
   liner['detail']='Thin plaster lining follows source roof slope'
 # Correct isolated decorative trim that the last HTML patch places across clear suite openings.
 for name in ['Premarco suite lateral A','Premarco suite lateral B','Premarco suite superior','Tapajunta acceso vestidor A','Tapajunta acceso vestidor B']:
  remove(source(name))
 for x in [18.02,19.02]:box('Premarco acceso vestidor | jamba', [x,4.36,9.0],[.045,2.22,.08],'wood','INTERIORS')
 box('Premarco acceso vestidor | dintel',[18.52,5.49,9.0],[1.04,.045,.08],'wood','INTERIORS')
 for z in [7.19,8.17]:box('Premarco dormitorio | jamba',[17.62,4.36,z],[.08,2.22,.04],'wood','INTERIORS')
 notes.append('Repositioned late-patch suite trims that were centred inside doorways to the actual jambs. Room partitions and door-opening coordinates retained.')
 # Real opening behind the ground-floor bathroom door; source originally overlaid a leaf on a solid wall.
 remove(source('Baño mono muro frente'))
 for a,b in [(19.39,19.44),(20.20,21.81)]:
  box('Baño mono frente | paño',[ (a+b)/2,1.3,4.28],[b-a,2.6,.14],'whitePlaster','GROUND_FLOOR')
 box('Baño mono frente | dintel',[19.82,2.49,4.28],[.76,.22,.14],'whitePlaster','GROUND_FLOOR')
 door=source('Baño mono puerta')
 if door:door.location.z=1.285
 notes.append('Opened the existing ground-floor bathroom doorway through its solid source wall, keeping the source door centre; aligned the leaf to the finished floor.')
 # Original source water is an open surface. Give it a closed underwater volume for correct optical depth.
 water=source('Agua de pileta')
 if water:
  mod=water.modifiers.new('Water volume | basin depth','SOLIDIFY');mod.thickness=1.45;mod.offset=-1
 # Exposed metal roof ribs: source texture encoded corrugation, use fine real ridge geometry too.
 for side in [0,1]:
  for i in range(45):
   x=13.73+i*.194;z=3 if side==0 else 9;y=6.985
   o=box('Chapa | nervadura %s %02d'%(side,i),[x,y,z],[.019,.012,6.27],'roof','ROOF',.002)
   o.rotation_euler.x=(-1 if side==0 else 1)*math.atan(1.1/6)
 # Small facade wall sconces at source structural supports.
 for x,z,h,axis in [(14.0,6.8,2.05,'x'),(14.0,10.7,2.05,'x'),(17.63,12.12,4.8,'z'),(21.68,12.12,2.10,'z'),(14.0,8.8,4.8,'x')]:
  body=box('Aplique exterior | carcasa',[x,h,z],[.10,.25,.12],'blackMetal','LIGHTS')
  if axis=='x':p=[x-.07,h,z];t=[x-.24,h-.7,z]
  else:p=[x,h,z+.09];t=[x,h-.7,z+.2]
  g['light']('Aplique exterior | lavado cálido',p,45,(1,.66,.35),.085,t)
 # Instrument display: a physical front screen with six editable audio tracks and waveform segments.
 rng=random.Random(90)
 for i in range(6):
  y=4.98-i*.085
  box('DAW | pista %d'%i,[17.553,y,3.0],[.008,.056,.97],'screen','STUDIO',0)
  for j in range(34):
   amp=.009+abs(math.sin(j*.82+i*2.1))*rng.uniform(.007,.030)
   box('DAW | onda %d %02d'%(i,j),[17.56,y,2.56+j*.026],[.007,amp,.005],'meterCyan' if i%2==0 else 'meterAmber','STUDIO',0)
 for i in range(8):
  box('Rack audio | unidad %d'%i,[20.457,3.45+i*.105,1.55],[.025,.082,.49],'blackMetal','STUDIO')
  box('Rack audio | display %d'%i,[20.44,3.45+i*.105,1.42],[.012,.029,.14],'meterCyan','STUDIO',0)
  box('Rack audio | indicador %d'%i,[20.438,3.45+i*.105,1.68],[.01,.013,.013],'meterGreen','STUDIO',0)
 # Microphone and boom stand, spatially clear of the entrance and workstation.
 def tube(name,a,b,r,mat,col):
  dv=cv(b)-cv(a);bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=dv.length,location=(cv(a)+cv(b))/2)
  o=bpy.context.object;o.name=name;o.rotation_euler=dv.to_track_quat('Z','Y').to_euler();o.data.materials.append(M[mat])
  for c in list(o.users_collection):c.objects.unlink(o)
  COL[col].objects.link(o)
  for p in o.data.polygons:p.use_smooth=True
  return o
 tube('Micrófono | pie',[15.7,3.27,1.0],[15.7,4.85,1.0],.018,'blackMetal','STUDIO')
 tube('Micrófono | brazo',[15.7,4.8,1.0],[16.35,4.94,1.25],.012,'blackMetal','STUDIO')
 tube('Micrófono | condensador',[16.35,4.84,1.25],[16.35,5.02,1.25],.04,'stainless','STUDIO')
 for a in [0,2.094,4.189]:tube('Micrófono | trípode',[15.7,3.31,1.0],[15.7+.32*math.cos(a),3.28,1+.32*math.sin(a)],.013,'blackMetal','STUDIO')
 # Fine QRD diffusion depth on existing timber acoustic panels.
 for zc in [1.1,2.35,3.6]:
  for i in range(9):
   dep=[.035,.058,.11,.045,.085,.125,.07,.028,.092][i]
   box('Difusor QRD | lama',[21.61-dep/2,4.95,zc-.34+i*.084],[dep,1.43,.052],'wood','STUDIO',.002)
 # Grill grate, ash handle and restrained real embers.
 for i in range(20):tube('Parrilla | varilla acero %02d'%i,[20.38,1.125,9.08+i*.038],[20.86,1.125,9.08+i*.038],.004,'stainless','QUINCHO')
 box('Cajón ceniza | tirador',[20.41,.79,9.44],[.025,.025,.30],'stainless','QUINCHO')
 for i in range(14):box('Brasero | carbón %02d'%i,[20.53+rng.random()*.24,1.01,9.11+rng.random()*.64],[.035,.018,.032],'embers' if i%3==0 else 'blackMetal','QUINCHO',.005)
 # Practical double-sink perimeter, sink cavities remain below the source countertop.
 for z in [7.88,8.42]:
  for dx,dz,sx,sz in [(-.23,0,.018,.48),(.23,0,.018,.48),(0,-.23,.46,.018),(0,.23,.46,.018)]:
   box('Doble bacha | acero borde',[20.64+dx,1.089,z+dz],[sx,.014,sz],'stainless','QUINCHO',.003)
 # Landscaping supplementary trees outside the exact lot, reusing source tree meshes.
 treeparts=[o for o in O.values() if o and o.name.startswith('Árbol lote 2')]
 external=[(-3,8),(-4,17),(-2,24),(3,24),(8,25),(13,25),(19,24),(25,22),(26,16),(26,9),(25,2),(-4,0)]
 for i,(x,z) in enumerate(external):
  factor=1.6+rng.random()*.9
  T=Matrix.Translation(cv([x,0,z]))@Matrix.Diagonal((factor,factor,factor,1))@Matrix.Translation(-cv([4.3,0,16.8]))
  for o in treeparts:
   dup=o.copy();dup.data=o.data;dup.name='Entorno arbolado %02d | %s'%(i,o.name);COL['LANDSCAPE'].objects.link(dup);dup.matrix_world=T@o.matrix_world
 # Fine grasses in modest border clumps, avoiding the pool's 1m paving and circulation.
 for i in range(28):
  x,z=([(1.0,10+i*.32)] if i<12 else [(1.8+(i-12)*.62,19.2)])[0]
  for j in range(7):
   a=rng.random()*math.tau;h=rng.uniform(.22,.6)
   tube('Herbácea perimetral %02d %02d'%(i,j),[x,.04,z],[x+.17*math.cos(a),h,z+.17*math.sin(a)],.006,'grass','LANDSCAPE')
 # Street name is a normal text object.
 font=bpy.data.curves.new('Cedro Misionero | texto','FONT');font.body='CEDRO MISIONERO';font.size=.10;font.extrude=.0005;font.materials.append(M['clothWhite'])
 txt=bpy.data.objects.new('Placa calle | Cedro Misionero',font);COL['SITE'].objects.link(txt);txt.location=cv([9.35,1.6,-.10]);txt.rotation_euler=(math.pi/2,0,0)
 box('Placa calle | fondo',[10.03,1.64,-.075],[1.48,.22,.02],'blackMetal','SITE')
 return notes
