"""Actual R7 wet/vent construction views, called by the33-sheet vector generator."""
import math
import numpy as np
from shapely.geometry import Polygon,LineString,box
from shapely.ops import unary_union

def install(ctx):
 global OB,V,G,P,LIGHT,PLIGHT,text,para,begin,end,line,poly,MEAS,DIMS
 for k in ['OB','V','G','P','LIGHT','PLIGHT','text','para','begin','end','line','poly','MEAS','DIMS']:globals()[k]=ctx[k]

def section(v,axis,at,axes,origin,predicate=lambda o:True,interruptions=False):
 clip=box(0,0,v.w,v.h);groups={G:[],P:[]};cuts={k:[] for k in ('left','right','bottom','top')}
 for o in OB.values():
  if not o.get('v') or not predicate(o) or not o['lo'][axis]-1e-6<=at<=o['hi'][axis]+1e-6:continue
  arr=np.array(o['v']);low=np.array(o['lo'])[axes]*1000-origin;high=np.array(o['hi'])[axes]*1000-origin
  if high[0]<0 or high[1]<0 or low[0]>v.w or low[1]>v.h:continue
  color=P if o['name'].startswith(('VENT99 |','WET99 |')) else G
  for f in o['f']:
   a=arr[f];d=a[:,axis]-at
   if min(d)>1e-7 or max(d)<-1e-7 or max(abs(d))<1e-7:continue
   pts=[]
   for i,p in enumerate(a):
    q=a[(i+1)%len(a)];da=p[axis]-at;db=q[axis]-at
    if abs(da)<1e-8:pts.append(p)
    elif da*db<0:pts.append(p+(q-p)*(-da)/(db-da))
   if len(pts)<2:continue
   ps=np.unique(np.round(np.array(pts)[:,axes]*1000-origin,6),axis=0)
   if len(ps)<2:continue
   ps=ps[np.argsort(ps[:,int(np.argmax(np.ptp(ps,axis=0)))])]
   for i in range(0,len(ps)-1,2):
    if np.linalg.norm(ps[i]-ps[i+1])>1e-5:
     raw=LineString([ps[i],ps[i+1]]);clipped=raw.intersection(clip);groups[color].append(clipped)
     if interruptions and clipped.geom_type=='LineString' and raw.length-clipped.length>1e-5:
      for xx,yy in clipped.coords:
       if abs(xx)<1e-5:cuts['left'].append(yy)
       if abs(xx-v.w)<1e-5:cuts['right'].append(yy)
       if abs(yy)<1e-5:cuts['bottom'].append(xx)
       if abs(yy-v.h)<1e-5:cuts['top'].append(xx)
 for c,ss in groups.items():
  def emit(g):
   if g.geom_type=='LineString':
    p=list(g.coords)
    for a,b in zip(p,p[1:]):v.line(a,b,c,.24)
   elif hasattr(g,'geoms'):
    for p in g.geoms:emit(p)
  if ss:emit(unary_union(ss))
 if interruptions:
  # Conventional zigzag at the cropped continuation; no fictitious endcap.
  for edge,values in cuts.items():
   runs=[]
   for value in sorted(values):
    if not runs or value-runs[-1][-1]>6*v.s:runs.append([value])
    else:runs[-1].append(value)
   for run in runs:
    lo=min(run)-1.0*v.s;hi=max(run)+1.0*v.s;mid=(lo+hi)/2;d=1.2*v.s
    if edge in ('left','right'):
     lo=max(0,lo);hi=min(v.h,hi);fixed=0 if edge=='left' else v.w
     pts=[(fixed,lo),(fixed,mid-d),(fixed-d,mid-d/2),(fixed+d,mid+d/2),(fixed,mid+d),(fixed,hi)]
    else:
     lo=max(0,lo);hi=min(v.w,hi);fixed=0 if edge=='bottom' else v.h
     pts=[(lo,fixed),(mid-d,fixed),(mid-d/2,fixed-d),(mid+d/2,fixed+d),(mid+d,fixed),(hi,fixed)]
    v.path(pts,G,.26)


def projected(v,axes,origin,predicate,invert_y=False,color=None):
 clip=box(0,0,v.w,v.h)
 for o in OB.values():
  if not o.get('v') or not predicate(o):continue
  a=np.array(o['v'])[:,axes]*1000-origin
  if invert_y:a[:,1]=v.h-a[:,1]
  if a[:,0].max()<0 or a[:,1].max()<0 or a[:,0].min()>v.w or a[:,1].min()>v.h:continue
  ps=[]
  for f in o['f']:
   p=Polygon(a[f])
   if p.is_valid and p.area>.05:ps.append(p)
  if not ps:continue
  sh=unary_union(ps).intersection(clip);c=color or (P if o['name'].startswith(('VENT99 |','WET99 |')) else G)
  def emit(g):
   if g.geom_type=='Polygon':
    v.path(list(g.exterior.coords),c,.15)
    for r in g.interiors:v.path(list(r.coords),c,.10)
   elif hasattr(g,'geoms'):
    for p in g.geoms:emit(p)
  emit(sh)

def vent(ctx):
 install(ctx);begin('D08','Ventilacion: montaje y mantenimiento','Propuesta P modelada / cotas geometricas G / sin caudal ni atenuacion asignados')
 p=V(27,79,8400,6200,50,'16 Planta de cielorraso y plenum')
 pred=lambda o:o['name'].startswith('VENT99 |') and not any(t in o['name'] for t in ['cartucho','perforada','tornillo','varilla','tuerca','lama','junta','sello','cierre','aislacion'])
 projected(p,[0,1],np.array([13800,-100]),pred,True)
 p.rect(400,300,7600,5600,G,None,.22)
 # Measured roof plan coordinates reflected into this view.
 def planpt(x,z):return ((x-13.8)*1000,6200-(z+.1)*1000)
 for x,z,t in [(17.64,0,'TOMA'),(20.16,0,'EXPULSION'),(20.70,4.68,'IMP.'),(16.50,5.10,'EXT.'),(19.3,5.52,'REGISTRO')]:p.label(*planpt(x,z),t,P,2.5)
 for a,b in [((18.70,4.70),(19.90,5.30)),((14.3,5.0),(18.95,5.6))]:
  q=[planpt(a[0],a[1]),planpt(b[0],a[1]),planpt(b[0],b[1]),planpt(a[0],b[1]),planpt(a[0],a[1])]
  for aa,bb in zip(q,q[1:]):p.line(aa,bb,P,.19,True)
 p.label(*planpt(16.5,5.88),'P aproximacion600 / puerta abierta',P,2.5)
 p.label(*planpt(20.25,5.65),'P apartar mueble apoyo',P,2.5)
 p.dx(3840,6360,-200,label='2,52m G centros terminales',c=G)
 # Exploded-free axonometry of the actual assembled outer surfaces.
 text(313,72,'17 Axonometria de montaje / sin escala',3.2,P,True)
 rows=[]
 for o in OB.values():
  n=o['name']
  if not o.get('v') or not n.startswith('VENT99 |') or any(t in n for t in ['aislacion','perforada','cartucho','ventilador rotor','lama','junta','sello','tornillo','tuerca','cierre']):continue
  a=np.array(o['v']);q=np.column_stack((.866*(a[:,0]-a[:,1]),.5*(a[:,0]+a[:,1])-a[:,2]));rows.append((o,a,q))
 pts=np.concatenate([q for _,_,q in rows]);mn=pts.min(axis=0);mx=pts.max(axis=0);fac=min(248/(mx[0]-mn[0]),155/(mx[1]-mn[1]))
 for o,a,q in sorted(rows,key=lambda item:float(np.mean(item[1][:,0]+item[1][:,1]))):
  q=(q-mn)*fac+[313,82]
  edge=set()
  for f in o['f']:
   for i,k in enumerate(f):
    j=f[(i+1)%len(f)];e=tuple(sorted((k,j)))
    if e in edge:continue
    edge.add(e)
    if np.linalg.norm(q[k]-q[j])>.15:line(tuple(q[k]),tuple(q[j]),P,.10)
 # Actual section along the filter, fan and silencer axis.
 s=V(27,239,1600,1400,10,'18 Equipo / corte Z4,68')
 section(s,1,4.68,[0,2],np.array([18500,6400]),lambda o:o['name'].startswith('VENT99 |') or 'cabio' in o['name'],interruptions=True)
 s.dx(200,400,1190,label='200 G filtro',c=G);s.dx(700,1300,1190,label='600 G silenciador',c=G)
 s.label(800,20,'REGISTRO DESMONTABLE',P,2.5);s.arrow((1100,480),(1100,20),P)
 s.dy(364.2,615.8,1530,label='Ø251,6 G',c=G)
 # Transverse full-height access: floor, fixed hatch and rafters are measured.
 t=V(211,174,1750,5100,25,'19 Acceso / X19,40 + P')
 section(t,0,19.4,[1,2],np.array([4100,3200]),lambda o:o['name'].startswith('VENT99 |') or any(k in o['name'].lower() for k in ['cabio','cielorraso estudio','piso estudio','bafle','cubierta']))
 t.rect(600,50,600,40,P,None,.2);t.rect(600,1430,600,20,P,None,.25)
 t.line((625,90),(1175,1430),P,.2,True);t.line((1175,90),(625,1430),P,.2,True)
 # P operator envelope1720x450: headH6.37 remains80mm below ceiling.
 t.rect(675,1450,450,1720,P,None,.16);t.circle(900,3060,105,P,None)
 t.line((900,2955),(900,2320),P,.25);t.line((900,2320),(720,1450),P,.25);t.line((900,2320),(1080,1450),P,.25)
 t.line((900,2860),(720,3330),P,.23);t.line((900,2860),(1120,3270),P,.23)
 t.arrow((580,3690),(580,2200),P);t.arrow((1000,3690),(1000,2200),P)
 t.arrow((580,2200),(900,2200),P);t.arrow((1380,1450),(1380,90),P)
 t.dy(50,1450,150,label='1400 P tablero',c=P)
 t.label(875,1400,'Tablero P +4,65',P,2.5)
 t.dy(50,3253,1700,label='3,203m G',c=G);t.dx(375,1205,2500,label='830 G libre',c=G)
 t.label(875,0,'NPT +3,25 G',G,2.5);t.label(900,2140,'Recepcion P +5,40',P,2.5)
 # Longitudinal crossing below the real front beam and above the ceiling.
 c=V(309,278,5200,1300,20,'20 Frente / corte X17,64')
 section(c,0,17.64,[1,2],np.array([-100,6300]),lambda o:o['name'].startswith('VENT99 |') or any(k in o['name'].lower() for k in ['cubierta','cabio','fachada','cielorraso estudio','viga']),interruptions=True)
 c.label(2000,60,'Cielorraso G +6,450',G,2.5);c.dy(331.5,398.3334,560,label='66,8 G a viga',c=G)
 c.dx(1250,1850,1140,label='600 G transicion',c=G)
 para(309,354,'G seccion rectangular300x80; area0,024m2. Chapa1 + aislacion25 + camisa0,5: exterior353x133. P seleccion, caudal, ruido, condensacion y fijaciones pendientes de proyecto.',256,2.7)
 para(313,244,'P medio auxiliar no modelado: plataforma elevadora1200x600, tablero+4,65; cuerpo450x1720, cabeza+6,37. Apartar mueble apoyo y4patas. Retirar a+5,40; trasladar sobre tablero y descender al piso. Operario cambia X segun modulo; seleccionar equipo, alcance, herramienta y capacidad.',256,2.5,leading=3.7)
 para(27,216,'P retiro: tapas; filtro por abajo; fan con dos flexibles; silenciador con acoples, abrazaderas y sus dos colgantes. El otro circuito y los bastidores permanecen. No se desmontan nubes.',174,2.6)
 end()

def wet(ctx):
 install(ctx);begin('D11','Banos: continuidad humeda y ducha','P capas modeladas / medidas G de pisos, retornos, penetraciones y rociador')
 # Actual shower plan, with tile, membrane and perimeter contacts.
 p=V(27,82,1250,1800,10,'24 Ducha PB / planta')
 projected(p,[0,1],np.array([20750,100]),lambda o:o['name'].startswith(('BTH95 | ducha','WET99 | PB')) or 'Mampara baño mono' in o['name'],True)
 p.dx(150,1050,1770,label='900 G',c=G);p.dy(190,1640,80,label='1450 G',c=G)
 p.label(600,750,'+0,1955 G',G,2.5);p.label(600,1600,'+0,210 G',G,2.5)
 para(27,280,'G ducha a piso: rejilla100x100 y caida14,5mm; pendientes2,15% /3,63% hasta el borde del desague.',127,2.7)
 j=V(27,312,120,48,1,'24a Junta pasante / X21,35')
 section(j,0,21.35,[1,2],np.array([240,490]),lambda o:o['name'].startswith('WET99 | PB'))
 j.dx(12,20,43,label='8 G',c=G);j.dy(19,21,48,label='2 G',c=G)
 j.label(86,30,'Membrana2',P,2.5);j.label(86,22,'Adhesivo4',P,2.5)
 para(27,372,'P modulo600x300; juntas2x8 y esquinas2. Compatibilidad y ensayo de estanqueidad pendientes.',127,2.7)
 s=V(170,82,1900,2850,10,'25 Ducha PB / X21,35')
 section(s,0,21.35,[1,2],np.array([100,0]))
 head=OB['Ducha baño mono'];headparts=[o for n,o in OB.items() if n.startswith('Ducha baño mono')];hmin=min(o['lo'][2] for o in headparts)*1000
 s.dy(210,hmin,1720,label=f'{hmin-210:.0f} G libre',c=G)
 s.dx(head['lo'][1]*1000-100,head['hi'][1]*1000-100,2450,label='Ø200 G',c=G)
 s.label(600,2690,'Cuerpo12 G / boquillas+2,310',G,2.5)
 s.label(800,80,'NPT +0,210 G',G,2.5)
 # Pipe stems and rosettes now bridge the original35mm gap without moving taps.
 a=V(385,83,380,220,2,'26 Griferia PA / X21,10')
 section(a,0,21.10,[1,2],np.array([6030,3870]),interruptions=True)
 a.dx(135,170,205,label='35 G antes del cuerpo',c=G)
 para(385,204,'P vastago metalico hasta cuerpo empotrado, collar impermeable y roseta en cara terminada Z6,165; griferia conserva posicion. Se conecta al sustrato, sin tubo flotante.',176,2.7)
 b=V(385,267,170,220,2,'27 Piso-muro PB / Z1,40')
 section(b,1,1.40,[0,2],np.array([21700,130]))
 b.dx(100,114,205,label='14 G capas',c=G);b.label(70,42,'retorno continuo',P,2.5)
 d=V(490,268,430,440,5,'28 Sumidero PB / Z0,985')
 section(d,1,.985,[0,2],np.array([21130,-150]))
 d.dx(170,270,408,label='100 G',c=G)
 para(385,372,'P sanitario: brida, collar y sello geometrico50; ramal, ventilacion y prueba pendientes.',177,2.6)
 end()
