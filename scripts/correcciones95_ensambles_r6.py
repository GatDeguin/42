"""R6E: third corrective pass after R6C independent cabinet audit.
Run on R6D coordinated bathrooms. --preview permits R6C local geometry proof.
The hardware is dimensioned unbranded geometry, not certified product engineering.
"""
import bpy,os,math,json,ast,numpy as np,sys
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
for m in bpy.data.materials:
 for pre in ['MAT95 | ','FIT95 | ']:
  if m.name.startswith(pre):M[m.name.split(' | ',1)[1]]=m
def cv(p):return Vector((p[0],-p[2],p[1]))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_textiles.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['bounds','deform','map_h']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_materialidad.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['box','cyl','mesh','curve']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<fast>','exec'))
def bb(name,x,h,z,mat='wood',col='INTERIORS',bev=.0004):
 return box(name,[(x[0]+x[1])/2,(h[0]+h[1])/2,(z[0]+z[1])/2],[x[1]-x[0],h[1]-h[0],z[1]-z[0]],mat,col,bev)
def cut(o,c):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;m=o.modifiers.new('Reserva fabricada R6E','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=c;bpy.ops.object.modifier_apply(modifier=m.name)
def remove(n):
 o=bpy.data.objects.get(n)
 if o:bpy.data.objects.remove(o,do_unlink=True)
# Retire eight old solid metal strips superseded by manufactured SL95 seals.
for side in ['A','B']:
 for part in ['superior','inferior','izquierdo','derecho']:remove('Corrediza posterior '+side+' Burlete '+part)
# One replacement top with one hole, correctly positioned between cabinet partitions.
remove('Mesada cocina mono lateral')
outline=[(14.24,3.20),(14.86,3.20),(14.86,5.20),(15.78,5.20),(15.78,5.82),(14.24,5.82)];N=len(outline)
vs=[cv([x,h,z]) for h in [1.075,1.110] for x,z in outline];fs=[tuple(range(N)),tuple(range(2*N-1,N-1,-1))]
for i in range(N):j=(i+1)%N;fs.append((i,N+i,N+j,j))
counter=mesh('Mesada cocina mono lateral',vs,fs,'concrete','GROUND_FLOOR')
for o in S.objects:
 if o.name=='Bacha cocina mono' or o.name.startswith('Grifería cocina mono | '):o.location.y-=.155
c=bb('TEMP hueco único bacha',[14.355,14.765],[.85,1.14],[3.855,4.415],'blackMetal','REFERENCE',.025);cut(counter,c);remove(c.name)
be=counter.modifiers.new('Canto2mm','BEVEL');be.width=.002;be.segments=3
# Drain collar and trap are visible inside the open cabinet, connecting basin to proposed rear service stub.
# Basin drain opening is bored at its bottom; plumbing route beyond stub remains a coordination proposal.
sink=bpy.data.objects['Bacha cocina mono']
c=cyl('TEMP desagüe bacha mono',[14.56,.85,4.135],[14.56,.93,4.135],.020,'blackMetal','REFERENCE');cut(sink,c);remove(c.name)
outer=cyl('MOB95 | válvula bacha mono',[14.56,.848,4.135],[14.56,.887,4.135],.024,'stainless','GROUND_FLOOR')
inner=cyl('TEMP paso válvula',[14.56,.84,4.135],[14.56,.90,4.135],.020,'blackMetal','REFERENCE');cut(outer,inner);remove(inner.name)
curve('MOB95 | sifón propuesto bacha mono',[[14.56,.848,4.135],[14.56,.65,4.135],[14.47,.59,4.135],[14.38,.65,4.135],[14.38,.72,4.135],[14.27,.72,4.135]],.020,'stainless','GROUND_FLOOR')
# Remove actual duplicates; preserve one suite mirror and one set of dwelling cabinet fronts.
remove('Espejo baño')
for i in range(4):remove('Frente cocina vivienda detalle '+str(i))
remove('Frente cocina vivienda 2');remove('Tirador cocina vivienda 2')
body=bpy.data.objects['Cocina lineal bajos']
c=bb('TEMP alojamiento horno',[21.07,21.72],[3.44,3.96],[10.05,10.59],'blackMetal','REFERENCE',0);cut(body,c);remove(c.name)
bb('MOB95 | frente inferior horno',[21.1025,21.134],[3.39,3.435],[10.04,10.58])
bb('MOB95 | frente superior horno',[21.1025,21.134],[3.965,4.07],[10.04,10.58])
bb('MOB95 | chasis horno',[21.091,21.68],[3.456,3.944],[10.066,10.574],'blackMetal',bev=.002)
# TV actual double channel profiles and low-friction shoes. Preserve 760mm opening travel.
for o in list(S.objects):
 if o.name.startswith('MOB95 | riel corredero TV'):remove(o.name)
for side,x,z in [('izquierda',15.22,11.493),('derecha',15.98,11.512)]:
 o=bpy.data.objects['MOB95 | frente corredero TV '+side];a,b=bounds(o);deform(o,lambda p:Vector((x+(p.x-x)*.780/(b[0]-a[0]),p.y,p.z)))
 for xx in [x-.27,x+.27]:
  for h in [[3.300,3.317],[3.933,3.940]]:
   p=bb('MOB95 | patín TV '+side,[xx-.023,xx+.023],h,[z-.005,z+.005],'rubber95')
   p['motion_group']='TV '+side;p['proposed_travel_x']=.76 if side=='izquierda' else -.76
for h in [[3.298,3.300],[3.940,3.942]]:
 bb('MOB95 | perfil soporte TV',[14.829,16.371],h,[11.482,11.54],'blackMetal')
for za,zb in [(11.482,11.484),(11.502,11.504),(11.520,11.522)]:
 for h in [[3.300,3.309],[3.930,3.940]]:bb('MOB95 | canal retención TV',[14.829,16.371],h,[za,zb],'blackMetal',bev=.0002)
for x in [14.91,15.60,16.29]:
 for a,b in [(3.287,3.302),(3.937,3.952)]:cyl('MOB95 | fijación perfil TV',[x,a,11.533],[x,b,11.533],.0016,'stainless','INTERIORS')
# Three-stage telescopic wardrobe guide, real nested channels and shim contacts.
for o in list(S.objects):
 if o.name.startswith(('MOB95 | guía fija cajón vestidor','MOB95 | guía móvil cajón vestidor')):remove(o.name)
def railpart(name,q,h,z,wall,sgn,shim,mat='stainless',stage=0,i=0):
 xa,xb=sorted([wall+sgn*(shim+v) for v in q])
 o=bb(name,[xa,xb],h,z,mat,bev=.0001);o['wardrobe_drawer']=i;o['proposed_stage_travel_z']=stage
 return o
for i in range(3):
 a,b=bounds(bpy.data.objects['Vestidor cajón '+str(i)]);hc=float((a[2]+b[2])/2)
 for side,wall,sgn,gap in [('L',17.743,1,.022),('R',18.267,-1,.032)]:
  shim=gap-.022;pr='MOB95 | guía vestidor '+str(i)+side+' '
  # Spacer meets actual wood face, screws penetrate it by8mm.
  railpart(pr+'calzo',[0,.003+shim],[hc-.024,hc+.024],[6.27,6.68],wall,sgn,0,'blackMetal',0,i)
  for z in [6.32,6.62]:cyl(pr+'fijación fija',[wall-sgn*.008,hc,z],[wall+sgn*(shim+.005),hc,z],.0016,'stainless','INTERIORS')
  # Fixed C opens into room of guide; middle C and mobile reverse C remain clear.
  spec=[('fija',.003,.005,.005,.015,.021,.023,0),('intermedia',.009,.011,.011,.020,.015,.017,.225),('móvil',.019,.021,.015,.019,.011,.013,.450)]
  for label,wa,wb,fa,fb,inner,outer,travel in spec:
   railpart(pr+label+' alma',[wa,wb],[hc-outer,hc+outer],[6.25,6.70],wall,sgn,shim,stage=travel,i=i)
   for sg in [-1,1]:
    h=sorted([hc+sg*inner,hc+sg*outer]);railpart(pr+label+' ala',[fa,fb],h,[6.25,6.70],wall,sgn,shim,stage=travel,i=i)
  railpart(pr+'calzo móvil',[.021,.022],[hc-.009,hc+.009],[6.27,6.68],wall,sgn,shim,'blackMetal',.450,i)
  for z in [6.32,6.62]:
   o=cyl(pr+'fijación móvil',[wall+sgn*(shim+.019),hc,z],[wall+sgn*(gap+.008),hc,z],.0015,'stainless','INTERIORS');o['wardrobe_drawer']=i;o['proposed_stage_travel_z']=.450
  # Hardened rollers run in the clearance between upper/lower nested race faces.
  for stage,q,h,travel in [('exterior',.012,.019,.1125),('interior',.0175,.014,.3375)]:
   for z in [6.38,6.47,6.56]:
    for sg in [-1,1]:
     x=wall+sgn*(shim+q)
     o=cyl(pr+'rodillo '+stage,[x-.001,hc+sg*h,z],[x+.001,hc+sg*h,z],(.002 if stage=='exterior' else .001),'stainless','INTERIORS');o['wardrobe_drawer']=i;o['proposed_stage_travel_z']=travel
# Camera choices describe the final geometry and prevent open leaves obscuring cabinetry.
def camera(name,p,target,lens=24,frame=1):
 o=bpy.data.objects.get(name)
 if not o:
  data=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,data);COL['CAMERAS'].objects.link(o)
 o.location=cv(p);o.rotation_euler=(cv(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=lens;o.data.clip_start=.04;o['presentation_frame']=frame
 return o
for o in S.objects:
 if o.type=='CAMERA' and 'vestidor' in o.name.lower():o['presentation_frame']=1
camera('REV | Mono cocina e isla',[18.8,1.86,1.0],[15.95,1.1,4.85],24)
camera('REV | Mono distribución',[19.08,1.86,5.45],[16.9,1.18,2.95],22)
S['review_iteration']='95 / R6E coordinated furniture fabrication';S['r6e_scope']=json.dumps({'sink_shift_source_z':.155,'single_sink_hole':[14.355,3.855,14.765,4.415],'tv_leaf_width_m':.780,'tv_proposed_travel_m':.760,'wardrobe_guide':'nested3stage channels;fixed0/middle225/mobile450mm;shim contacts;design proposal','removed':'one duplicate suite mirror;four duplicate kitchen fronts;front behind oven','sink_drain':'40mm local siphon proposal; route downstream unverified'},ensure_ascii=False)
S.frame_set(1);bpy.context.view_layer.update();bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
name='Casa_de_Campo_95_R6E_preview.blend' if '--preview' in sys.argv else 'Casa_de_Campo_95_R6E.blend'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output',name),compress=True);print('R6E_SAVED',flush=True)
