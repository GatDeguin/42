"""D13/D14: measured R8 use geometry with declared bodies from same-SHA evidence."""
import json,math
from pathlib import Path
import numpy as np
from shapely.geometry import MultiPoint,box
from planos99_detail_views import install,section,projected

def draw_use_sheets(ctx,evidence):
 install(ctx)
 V=ctx['V'];G=ctx['G'];P=ctx['P'];R=ctx['R'];OB=ctx['OB'];begin=ctx['begin'];end=ctx['end'];text=ctx['text'];note=ctx['note'];para=ctx['para'];MEAS=ctx['MEAS'];DATA=ctx['DATA'];source=ctx['source'];SOURCES=ctx['SOURCES']
 ev=json.loads(evidence.read_text('utf8'));bodies=json.loads((evidence.parent/'geometry.json').read_text('utf8'))
 if ev['sha256']!=DATA['sha256'] or bodies['sha256']!=DATA['sha256'] or ev['status']!='PASS':raise RuntimeError('R8 use evidence must PASS and match the exact drawing source SHA')
 assert not {'D13','D14'}.intersection(s['id'] for s in ctx['SHEETS'])
 SOURCES['U1']=('NKBA Kitchen Planning Guidelines, Guideline9: seating','https://kb.nkba.org/uploads/2022/05/Kitchen-Planning-Guidelines.pdf')
 SOURCES['U2']=('OSHA computer workstation evaluation: neutral posture','https://www.osha.gov/etools/computer-workstations/checklists/evaluation')
 def bounds(n):return OB[n]['lo'],OB[n]['hi']
 def span(n,ax):lo,hi=bounds(n);return (hi[ax]-lo[ax])*1000
 def body(v,objects,axes,origin,invert=False):
  for o in objects:
   # Evidence X,H,Z -> drawing extraction X,Z,H.
   a=np.array(o['v'])[:,[0,2,1]][:,axes]*1000-np.array(origin)
   if invert:a[:,1]=v.h-a[:,1]
   shape=MultiPoint(a).convex_hull.intersection(box(0,0,v.w,v.h))
   if shape.geom_type=='Polygon':v.poly(list(shape.exterior.coords),P,None,.16)
 def outlines(v,predicate,axes,origin,c=G,invert=False,dash=False,shift=(0,0)):
  for o in OB.values():
   if not predicate(o) or not o.get('v'):continue
   a=np.array(o['v'])[:,axes]*1000-np.array(origin)+np.array(shift)
   if invert:a[:,1]=v.h-a[:,1]
   shape=MultiPoint(a).convex_hull.intersection(box(0,0,v.w,v.h))
   if shape.geom_type=='Polygon':
    ps=list(shape.exterior.coords)
    if dash:
     for aa,bb in zip(ps,ps[1:]):v.line(aa,bb,c,.16,True)
    else:v.path(ps,c,.18)
 def measured(label,value,n):MEAS.append({'item':label,'value_mm':round(value,4),'source':n,'class':'G','source_sha256':DATA['sha256']})
 floor=OB['Piso estudio']['hi'][2];seat=OB['Silla estudio asiento']['hi'][2]
 white=next(o for n,o in OB.items() if n.startswith('MAT95 | tecla natural'));black=next(o for n,o in OB.items() if n.startswith('MAT95 | tecla sostenido'));tray=OB['USO99 | MIDI bandeja18'];control=OB['Controlador estudio']
 hwhite=(white['hi'][2]-floor)*1000;hblack=(black['hi'][2]-floor)*1000;hseat=(seat-floor)*1000;headroom=(tray['lo'][2]-floor)*1000
 begin('D13','MIDI: uso y apoyo','Ver A11 | G malla medida / P operador declarado / sin producto ni capacidad certificados')
 v=V(31,84,2700,1800,10,'27 Puesto central / corte Z3,00')
 origin=np.array([17500,floor*1000]);pred=lambda o:o['name'].startswith(('Consola estudio','Base consola estudio','Controlador estudio','Silla estudio','USO99 | MIDI','MAT95 | tecla','MAT95 | pad MIDI','MAT95 | pantalla controlador','MAT95 | encoder maestro'))
 section(v,1,3.00,[0,2],origin,pred)
 body(v,bodies['operator'],[0,2],origin)
 outlines(v,lambda o:o['name'].startswith('Silla estudio pata'),[0,2],origin,G,dash=True)
 outlines(v,lambda o:o['name'] in ['USO99 | MIDI brazo40x30 0','USO99 | MIDI placa asiento base 0','USO99 | MIDI calce8 0'],[0,2],origin,R,dash=True)
 v.line((0,0),(2550,0),G,.35);v.dy(0,hwhite,2480,label=f'{hwhite:.0f} G teclas',c=G);v.dy(0,hseat,2220,label=f'{hseat:.0f} G asiento',c=G);v.dy(0,headroom,760,label=f'{headroom:.0f} G libre',c=G)
 x0,x1=control['lo'][0]*1000-origin[0],control['hi'][0]*1000-origin[0]
 v.dx(x0,x1,1120,label=f'{x1-x0:.0f} G cuerpo',c=G);v.dx(1310,1720,1520,label='410 P codo / tecla',c=P)
 note(335,78,'COORDINACION DE USO',[
 f'G controlador generico {span("Controlador estudio",1):.0f} x {span("Controlador estudio",0):.0f} x {span("Controlador estudio",2):.0f} mm. Teclas blancas {hwhite:.1f} / negras {hblack:.1f} mm sobre NPT.',
 'P operador: brazo283, antebrazo249 y mano150 mm; codo280 mm sobre asiento. Pelvis15 mm adelantada; pies sobre alfombra a9 mm del NPT. Dimensiones declaradas, no percentiles.',
 'G las teclas y el ancho se conservaron; pads, pantalla y encoders quedaron en la banda posterior. El uso primario se distingue de los controles de mezcla auxiliares.',
 'La evidencia de cuerpos y contactos corresponde a este SHA. No valida comodidad universal, resistencia ni producto comercial.'
 ],231)
 v2=V(336,237,1120,500,5,'28 Bandeja, raiz y consola / Z2,43')
 section(v2,1,2.430,[0,2],np.array([18200,3800]),pred,interruptions=True)
 v2.dy(75,115,990,label='40 G brazo',c=G);v2.dy(115,133,830,label='18 G bandeja',c=G);v2.dy(63,67,140,label='4 G placa',c=G)
 para(336,348,'G apoyos3 mm, brazo hueco40x30x2, calce8 y placa4 mm. Filetes propuestos3 mm unen placa y base metalica; el recorte inferior conserva la superficie de mezcla. Seccion y soldadura pendientes de dimensionamiento.',230,2.7)
 note(32,292,'LECTURA DEL CORTE Y LIMITES',[
 'Gris: corte G. Trazos grises: patas laterales. Ocre: brazo fuera del corte central. Azul: cuerpo de ensayo P, separado de la malla del edificio.',
 f'G intrados de bandeja {headroom:.0f} mm. El ensayo de muslos llega600 mm sobre piso; la reserva vertical medida es {headroom-600:.0f} mm. No se rebajo la base central de la consola.',
 'El montaje demuestra contacto y continuidad geometrica. No asigna capacidad, estabilidad, vibracion ni ajuste a todas las tallas.'
 ],282)
 source(32,374,'U2',530);end()
 for label,value,n in [('MIDI white key height',hwhite,white['name']),('MIDI black key height',hblack,black['name']),('MIDI seat height',hseat,'Silla estudio asiento'),('MIDI tray headroom',headroom,'USO99 | MIDI bandeja18'),('MIDI body depth',span('Controlador estudio',0),'Controlador estudio')]:measured(label,value,n)
 # Island page uses the very same measured geometry, with separate occupancy/retraction states.
 cap=OB['Isla cocina mono tapa'];back=OB['Isla cocina mono base | fondo'];floor=OB['Piso monoambiente']['hi'][2];left=OB['Taburete isla mono A | pata izq frente'];right=OB['Taburete isla mono A | pata der frente'];stool=OB['Taburete isla mono A | asiento 30 mm'];seatx=(stool['lo'][0]+stool['hi'][0])/2
 height=(cap['hi'][2]-floor)*1000;sh=(stool['hi'][2]-floor)*1000;knee=(back['lo'][1]-cap['lo'][1])*1000;leg=(right['lo'][0]-left['hi'][0])*1000
 begin('D14','Isla PB: dos plazas y soporte','Ver A02/A10b | G medidas / P cuerpos y maniobras alternativas, sin certificacion de accesibilidad')
 v=V(30,83,2550,1800,10,'29 Corte por plaza A / X'+f'{seatx:.2f}')
 origin=np.array([1800,floor*1000]);pred=lambda o:o['name'].startswith(('Isla cocina mono','Taburete isla mono A','USO99 | isla'))
 section(v,0,seatx,[1,2],origin,pred);body(v,[o for o in bodies['diners'] if o['name'].startswith('USE PROBE diner0')],[1,2],origin)
 outlines(v,lambda o:o['name'].startswith(('Taburete isla mono A | pata','Taburete isla mono A | apoyo elast')),[1,2],origin,G,dash=True)
 outlines(v,lambda o:o['name'].startswith(('USO99 | isla montante 0','USO99 | isla larguero extremo 0','USO99 | isla apoyo elastomerico 0')),[1,2],origin,R,dash=True)
 v.line((0,0),(2460,0),G,.35);v.dy(0,height,2340,label=f'{height:.0f} G tapa',c=G);v.dy(0,sh,680,label=f'{sh:.0f} G asiento',c=G);v.dx(cap['lo'][1]*1000-1800,back['lo'][1]*1000-1800,1150,label=f'{knee:.0f} G rodillas',c=G)
 rail=OB['USO99 | isla travesano superior 0'];v.dy(sh,(rail['lo'][2]-floor)*1000,960,label=f'{(rail["lo"][2]-stool["hi"][2])*1000:.0f} G a viga',c=G)
 v.dx(1250,1850,1560,label='600 P sensibilidad',c=P)
 note(334,77,'GEOMETRIA Y USO',[
 f'G tapa {span("Isla cocina mono tapa",0):.0f}x{span("Isla cocina mono tapa",1):.0f}x{span("Isla cocina mono tapa",2):.0f} mm; rodillas {knee:.0f} mm. P dos bandas610 mm. Interior de almacenaje222 mm; pasillo de cocina conservado.',
 f'G taburetes: asiento {sh:.0f} mm, huella380 mm y {leg:.0f} mm entre patas delanteras. P cuerpos sentados con pies en travesanos; rodillas largas y recorridoØ450 mm comprobados para esta fuente.',
 'G porticos25x25x2 y vigas25x20x2, elastomero3 mm bajo tapa. Resistencia, soldaduras y vinculacion requieren dimensionamiento; no se acredita capacidad.'
 ],235)
 vp=V(366,229,3250,2350,20,'30 Planta de huellas y maniobra / Cedro arriba')
 origin=np.array([15550,1700]);names=['Isla cocina mono tapa','Taburete isla mono A | asiento 30 mm','Taburete isla mono B | asiento 30 mm']
 outlines(vp,lambda o:o['name'] in names,[0,1],origin,G,True);body(vp,bodies['diners'],[0,1],origin,True)
 outlines(vp,lambda o:o['name'] in names[1:],[0,1],origin,R,True,True,shift=(0,-450))
 def pp(x,z):return ((x-15.55)*1000,vp.h-(z-1.70)*1000)
 for z in [2.145,2.37,2.595]:vp.line(pp(15.65,z),pp(18.25,z),P,.16,True)
 vp.line(pp(16.82,2.37),pp(16.82,3.05),R,.2,True);vp.line(pp(16.82,3.05),pp(16.35,3.05),R,.2,True)
 vp.label(*pp(16.95,2.07),'P paso450 / plazas ocupadas',P,2.5)
 for x in [16.35,17.29]:vp.dx((x-.305-15.55)*1000,(x+.305-15.55)*1000,0,label='610 P plaza',c=P)
 vp.dx((left['hi'][0]-15.55)*1000,(right['lo'][0]-15.55)*1000,520,label=f'{leg:.0f} G entre patas',c=G)
 note(31,292,'ESCENARIOS Y APOYOS',[
 'G patas fuera del corte: trazos grises. Ocre: portico lateral fuera de las bandas de rodilla. La tapa mantiene apoyos fisicos hasta el piso.',
 'P paso posterior con ambos comensales sentados. Retirada450 mm de cada taburete en21 poses, uno a la vez; acceso y salida en18 posiciones por el espacio central. Ocre en planta: asiento retirado, estado alternativo.',
 'Los ensayos no simulan equilibrio, esfuerzo ni todos los gestos de sentarse. La referencia NKBA610x381 mm se toma como criterio de diseno, no como reglamento argentino.'
 ],281)
 source(32,374,'U1',530);end()
 for label,value,n in [('Island counter height',height,'Isla cocina mono tapa'),('Island knee depth',knee,'fondo.minZ minus cap.minZ'),('Island stool height',sh,stool['name']),('Island front leg clearance',leg,'right.minX minus left.maxX')]:measured(label,value,n)
 ctx['MEAS'].append({'item':'R8 use evidence','source':str(evidence),'source_sha256':DATA['sha256'],'status':ev['status'],'body_scenarios':'P declared dimensions; no population or structural certification'})
