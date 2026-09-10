"""Vector architectural documentation from an explicitly selected Blender model.
Run: python scripts/planos95_build.py --model output/Casa_de_Campo_95_Pass1.blend --out planos95/pass1
DXF modelspace uses metres. SVG/PDF paper is A2 594 x 420 mm.
"""
from pathlib import Path
import sys,os,json,math,hashlib,argparse,subprocess,datetime,textwrap,re,html
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'planos95/_vendor'))
import numpy as np
from shapely.geometry import Polygon,LineString,box,MultiLineString
from shapely.ops import unary_union,polygonize
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import ezdxf,pymupdf as fitz
P=argparse.ArgumentParser();P.add_argument('--model',required=True);P.add_argument('--out',default='planos95/pass1');P.add_argument('--status',default='EN REVISION');P.add_argument('--reuse-geometry',action='store_true');a=P.parse_args()
OUT=(ROOT/a.out).resolve();OUT.mkdir(parents=True,exist_ok=True);MODEL=(ROOT/a.model).resolve();GEO=OUT/'geometry.json'
if not a.reuse_geometry:subprocess.run([r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe','-b',str(MODEL),'--python',str(ROOT/'scripts/planos95_extract.py'),'--',str(GEO)],check=True,stdout=open(OUT/'extract.log','w'),stderr=subprocess.STDOUT)
DATA=json.loads(GEO.read_text(encoding='utf8'));OB=DATA['objects'];BY={o['name']:o for o in OB};SHA=hashlib.sha256(MODEL.read_bytes()).hexdigest()
if SHA!=DATA['sha256']:raise RuntimeError('Model differs from extracted geometry; regenerate without --reuse-geometry')
for o in OB:
 if 'v' in o:o['np']=np.array(o['v'])
CORRECTED=any(o['name'].startswith('AC95 | acabado descanso') for o in OB)
LANDING=3.25 if CORRECTED else 3.20
START=0.06 if CORRECTED else None
RAILO=BY.get('Baranda lateral pasamanos');RAILCENTER=(RAILO['lo'][2]+RAILO['hi'][2])/2 if RAILO else 4.25
SOURCE=json.loads((ROOT/'source/scene.json').read_text(encoding='utf8'));CFG=SOURCE['config']
FONTP=Path('C:/Windows/Fonts/arial.ttf');FONTB=Path('C:/Windows/Fonts/arialbd.ttf')
pdfmetrics.registerFont(TTFont('Arial',str(FONTP)));pdfmetrics.registerFont(TTFont('ArialB',str(FONTB)))
W,H=594,420;MM=72/25.4;INK='#172b35';GREY='#6f7e83';BLUE='#236a86';PALE='#edf2f3';ORANGE='#ac5b27'
C=canvas.Canvas(str(OUT/'Casa_de_Campo_Planos_A2.pdf'),pagesize=(W*MM,H*MM));C.setTitle('Casa de Campo | Planos de revision | '+MODEL.name)
SHEETS=[];METRICS={'dimensions':[],'scales':[],'warnings':[]};svg=[];DX=None;MS=None;PAGE=None

def line(x1,y1,x2,y2,width=.18,col=INK,dash=False,layer='ANOTACIONES'):
 C.setStrokeColor(HexColor(col));C.setLineWidth(width*MM);C.setDash([2*MM,1*MM] if dash else []);C.line(x1*MM,(H-y1)*MM,x2*MM,(H-y2)*MM)
 svg.append(f'<line x1="{x1:.4f}" y1="{y1:.4f}" x2="{x2:.4f}" y2="{y2:.4f}" stroke="{col}" stroke-width="{width}"'+(' stroke-dasharray="2 1"' if dash else '')+'/>')

def poly(points,width=.18,col=INK,fill=None,closed=True):
 if len(points)<2:return
 C.setStrokeColor(HexColor(col));C.setLineWidth(width*MM);C.setDash([]);p=C.beginPath();p.moveTo(points[0][0]*MM,(H-points[0][1])*MM)
 for x,y in points[1:]:p.lineTo(x*MM,(H-y)*MM)
 if closed:p.close()
 if fill:C.setFillColor(HexColor(fill))
 C.drawPath(p,stroke=1,fill=int(fill is not None))
 svg.append(f'<{"polygon" if closed else "polyline"} points="'+ ' '.join(f'{x:.4f},{y:.4f}' for x,y in points)+f'" fill="{fill or "none"}" stroke="{col}" stroke-width="{width}"/>')

def rect(x,y,w,h,fill=None,col=INK,width=.18):poly([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],width,col,fill)
def text(x,y,s,size=2.8,col=INK,bold=False,anchor='start',bg=False):
 s=str(s).replace('–','-').replace('—','-');f='ArialB' if bold else 'Arial';tw=pdfmetrics.stringWidth(s,f,size*MM)/MM
 xx=x-(tw/2 if anchor=='middle' else tw if anchor=='end' else 0)
 if bg:rect(xx-.8,y-size,tw+1.6,size+1.3,'#ffffff','#ffffff',0)
 C.setFillColor(HexColor(col));C.setFont(f,size*MM);C.drawString(xx*MM,(H-y)*MM,s)
 svg.append(f'<text x="{x:.4f}" y="{y:.4f}" font-family="Arial" font-size="{size}" font-weight="{"bold" if bold else "normal"}" fill="{col}" text-anchor="{anchor}">{html.escape(s)}</text>')
 if size<2.4:METRICS['warnings'].append('Small text '+s)

def para(x,y,s,w=140,size=2.8,col=INK,leading=4.4):
 words=s.split();row=''
 for word in words:
  z=(row+' '+word).strip()
  if pdfmetrics.stringWidth(z,'Arial',size*MM)/MM>w and row:text(x,y,row,size,col);y+=leading;row=word
  else:row=z
 if row:text(x,y,row,size,col);y+=leading
 return y

def notes(x,y,title,items,w=145):
 text(x,y,title,3.7,BLUE,True);y+=7
 for item in items:y=para(x,y,item,w);y+=3
 return y

def table(x,y,widths,headers,rows,rowh=9,size=2.7):
 total=sum(widths);rect(x,y,total,rowh,INK,INK)
 xx=x
 for h,w in zip(headers,widths):text(xx+2,y+6,h,size,'#ffffff',True);xx+=w
 y+=rowh
 for i,row in enumerate(rows):
  rect(x,y,total,rowh,PALE if i%2==0 else '#ffffff','#ccd5d8',.1);xx=x
  for val,w in zip(row,widths):
   para(xx+2,y+5,str(val),w-4,size,leading=3.7);xx+=w
  y+=rowh
 return y

def begin(code,title,subtitle=''):
 global svg,DX,MS,PAGE
 PAGE=code;svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" viewBox="0 0 594 420">','<rect width="594" height="420" fill="white"/>'];DX=ezdxf.new('R2010');DX.units=6;MS=DX.modelspace()
 for l,c in [('CORTE',7),('VISTA',8),('COTAS',4),('TEXTOS',7),('EJES',3),('SISTEMAS',5)]:DX.layers.new(l,dxfattribs={'color':c})
 rect(10,10,574,400,None,INK,.35);text(18,21,'CASA DE CAMPO',4.8,INK,True);text(18,28,'VIRREY DEL PINO - BUENOS AIRES | CALLE CEDRO MISIONERO',2.6,GREY)
 text(577,21,code+' | '+title,4.2,INK,True,'end');text(577,28,subtitle or 'Geometria del modelo seleccionado; desarrollo documental en revision',2.6,GREY,anchor='end');line(10,34,584,34,.25)
 line(10,384,584,384,.3);text(18,393,a.status+' | NO APTO PARA CONSTRUCCION',3,ORANGE,True)
 text(18,401,'Modelo: '+MODEL.name+' | SHA256 '+SHA[:16]+' | 10/09/2026',2.5,GREY)
 text(375,393,'A2 594 x 420 mm | imprimir al 100 %',2.8,INK);text(375,401,'Metros salvo indicacion | cotas prevalecen al escalimetro',2.5,GREY)
 text(577,407,f'{len(SHEETS)+1:02d}',2.6,INK,anchor='end');SHEETS.append({'id':code,'title':title,'svg':code+'.svg','dxf':code+'.dxf'})

def end():
 (OUT/(PAGE+'.svg')).write_text('\n'.join(svg+['</svg>']),encoding='utf8');DX.saveas(OUT/(PAGE+'.dxf'));C.showPage()

def isstruct(o):
 n=o['name'].lower();return any(t in n for t in ['muro','fachada','medianera','pilar','columna','tabique','separaci','dintel','antepecho','losa','cubierta','frontón','cielorraso','viga','cabio','correa','aislaci','recrecido','cierre alto'])
def isarch(o):
 n=o['name'].lower();return o['name'].startswith(('PL95 |','AC95 |')) or isstruct(o) or any(c in o['collections'] for c in ['STAIR','ROOF','CONSTRUCTION','DOORS','VENTILATION']) or any(t in n for t in ['puerta','ventana','vidrio','balcón','baranda','umbral','descanso','marco','bajada','canaleta'])
def selected(o,groups=None):return 'np' in o and (not groups or any(g in o['collections'] for g in groups))
CACHE={}
def shape_project(o,axes):
 key=(o['name'],tuple(axes));
 if key in CACHE:return CACHE[key]
 pts=o['np'];sh=[]
 for f in o['f']:
  if len(f)<3:continue
  p=Polygon(pts[f][:,axes]);
  if p.is_valid and p.area>1e-7:sh.append(p)
 try:res=unary_union(sh).simplify(.0015,preserve_topology=True)
 except:res=Polygon()
 CACHE[key]=res;return res

def shape_cut(o,axis,level,axes):
 p=o['np'];segments=[]
 if o['lo'][axis]>level or o['hi'][axis]<level:return []
 for f in o['f']:
  q=p[f];d=q[:,axis]-level
  if d.min()>0 or d.max()<0:continue
  hits=[]
  for i in range(len(q)):
   j=(i+1)%len(q)
   if (d[i]<0<=d[j]) or (d[j]<0<=d[i]):hits.append((q[i]+(q[j]-q[i])*(d[i]/(d[i]-d[j])))[axes])
  if len(hits)==2 and np.linalg.norm(hits[0]-hits[1])>.00005:segments.append([hits[0].tolist(),hits[1].tolist()])
 return segments

class View:
 def __init__(self,x,y,ext,scale=50,plan=True,name=''):
  self.x=x;self.y=y;self.ext=ext;self.scale=scale;self.k=1000/scale;self.plan=plan;self.name=name;self.off=len(METRICS['scales'])*40
  self.clip=box(ext[0],ext[2],ext[1],ext[3]);METRICS['scales'].append({'sheet':PAGE,'view':name,'scale':scale,'width_mm':(ext[1]-ext[0])*self.k,'height_mm':(ext[3]-ext[2])*self.k})
  if name:text(x,y-7,name+' | 1:'+str(scale),3.2,BLUE,True)
 def p(self,p):return (self.x+(p[0]-self.ext[0])*self.k,self.y+((p[1]-self.ext[2]) if self.plan else (self.ext[3]-p[1]))*self.k)
 def cad(self,p):return (p[0]+self.off,-p[1] if self.plan else p[1])
 def line(self,p,q,width=.18,col=INK,dash=False,layer='VISTA'):
  line(*self.p(p),*self.p(q),width,col,dash);MS.add_line(self.cad(p),self.cad(q),dxfattribs={'layer':layer})
 def poly(self,p,width=.18,col=INK,fill=None,layer='VISTA'):
  poly([self.p(t) for t in p],width,col,fill);MS.add_lwpolyline([self.cad(t) for t in p],close=True,dxfattribs={'layer':layer})
 def shp(self,sh,width=.18,col=INK,fill=None,layer='VISTA'):
  try:sh=sh.intersection(self.clip)
  except:return
  if sh.is_empty:return
  gs=list(sh.geoms) if hasattr(sh,'geoms') else [sh]
  for g in gs:
   if g.geom_type=='Polygon':
    self.poly(list(g.exterior.coords),width,col,fill,layer)
    for ring in g.interiors:self.poly(list(ring.coords),width,col,'#ffffff',layer)
   elif g.geom_type=='LineString':
    ps=list(g.coords)
    for p,q in zip(ps,ps[1:]):self.line(p,q,width,col,layer=layer)
 def label(self,x,y,s,size=2.7,col=INK,bold=False):
  p=self.p((x,y));text(*p,s,size,col,bold,'middle',True);MS.add_text(s,dxfattribs={'height':size/self.k,'insert':self.cad((x,y)),'layer':'TEXTOS'})
 def dimx(self,x1,x2,y,ref=None,label=None):
  val=label or f'{x2-x1:.2f}';p=self.p((x1,y));q=self.p((x2,y));line(*p,*q,.13,BLUE)
  for x in [x1,x2]:
   u=self.p((x,y));line(u[0]-1,u[1]+1,u[0]+1,u[1]-1,.2,BLUE)
   if ref is not None:line(*self.p((x,ref)),u[0],u[1]+1.5,.1,GREY)
  text((p[0]+q[0])/2,p[1]-1.5,val,2.5,BLUE,anchor='middle',bg=True)
  MS.add_linear_dim(base=self.cad((x1,y)),p1=self.cad((x1,ref if ref is not None else y)),p2=self.cad((x2,ref if ref is not None else y)),angle=0,override={'dimtxt':.13,'dimasz':.09},dxfattribs={'layer':'COTAS'}).render()
  METRICS['dimensions'].append({'sheet':PAGE,'view':self.name,'axis':'horizontal','from':x1,'to':x2,'value_m':round(x2-x1,6),'label':val})
 def dimy(self,y1,y2,x,ref=None,label=None):
  val=label or f'{y2-y1:.2f}';p=self.p((x,y1));q=self.p((x,y2));line(*p,*q,.13,BLUE)
  for y in [y1,y2]:
   u=self.p((x,y));line(u[0]-1,u[1]+1,u[0]+1,u[1]-1,.2,BLUE)
   if ref is not None:line(*self.p((ref,y)),u[0]+1.5,u[1],.1,GREY)
  text(p[0]+2,(p[1]+q[1])/2+.9,val,2.5,BLUE,bg=True)
  MS.add_linear_dim(base=self.cad((x,y1)),p1=self.cad((ref if ref is not None else x,y1)),p2=self.cad((ref if ref is not None else x,y2)),angle=90,override={'dimtxt':.13,'dimasz':.09},dxfattribs={'layer':'COTAS'}).render()
  METRICS['dimensions'].append({'sheet':PAGE,'view':self.name,'axis':'vertical','from':y1,'to':y2,'value_m':round(y2-y1,6),'label':val})
 def level(self,x,h,label=None):
  u=self.p((x,h));poly([(u[0],u[1]),(u[0]+2.3,u[1]-2.5),(u[0]+4.6,u[1])],.2,BLUE,BLUE);line(u[0],u[1],u[0]+25,u[1],.15,BLUE);text(u[0]+6,u[1]-1,label or f'{h:+.2f}',2.6,BLUE,bg=True);MS.add_text(label or f'{h:+.2f}',dxfattribs={'height':2.6/self.k,'insert':self.cad((x+.3,h+.1)),'layer':'TEXTOS'})
 def bar(self,x,y,length=5):
  p=self.p((x,y));total=length*self.k
  for i in range(5):rect(p[0]+i*total/5,p[1],total/5,1.8,INK if i%2==0 else '#ffffff',INK,.15)
  text(p[0],p[1]+5,'0',2.5);text(p[0]+total,p[1]+5,f'{length:g} m',2.5,anchor='end')

def draw_plan(v,level,groups=None,filter_fn=None):
 cuts=[];projs=[]
 for o in OB:
  if not selected(o,groups) or filter_fn and not filter_fn(o):continue
  lo,hi=o['lo'],o['hi'];n=o['name'].lower()
  if hi[0]<v.ext[0] or lo[0]>v.ext[1] or hi[1]<v.ext[2] or lo[1]>v.ext[3]:continue
  if hi[2]<level and hi[2]>(.15 if level<3 else 3.21) and lo[2]<level and not any(t in n for t in ['losa','piso','cielorraso','agua']):
   if max(hi[0]-lo[0],hi[1]-lo[1])>.12:projs.append(o)
  if lo[2]<=level<=hi[2]:cuts.append(o)
 for o in sorted(projs,key=lambda z:z['hi'][2]):v.shp(shape_project(o,[0,1]),.12,GREY,'#fafcfc')
 for o in cuts:
  seg=shape_cut(o,2,level,[0,1]);st=isstruct(o)
  if seg:
   g=unary_union([LineString(s) for s in seg]);ps=list(polygonize(g))
   if ps:v.shp(unary_union(ps),.5 if st else .15,INK if st else GREY,'#b8c1c5' if st else '#ffffff','CORTE' if st else 'VISTA')
   else:v.shp(g,.5 if st else .15,INK if st else GREY,layer='CORTE' if st else 'VISTA')

def draw_cut(v,axis,level,axes,filter_fn=None):
 for o in OB:
  if 'np' not in o or filter_fn and not filter_fn(o):continue
  if o['lo'][axis]>level or o['hi'][axis]<level:continue
  if o['hi'][axes[0]]<v.ext[0] or o['lo'][axes[0]]>v.ext[1] or o['hi'][axes[1]]<v.ext[2] or o['lo'][axes[1]]>v.ext[3]:continue
  seg=shape_cut(o,axis,level,axes)
  if not seg:continue
  st=isstruct(o);g=unary_union([LineString(s) for s in seg]);ps=list(polygonize(g))
  v.shp(unary_union(ps) if ps else g,.5 if st else .16,INK if st else GREY,'#b8c1c5' if st and ps else None,'CORTE' if st else 'VISTA')

def draw_elev(v,axis,sign,axes,filter_fn=None):
 obs=[o for o in OB if 'np' in o and (filter_fn(o) if filter_fn else isarch(o)) and o['hi'][0]>=12 and o['lo'][0]<=22.5 and o['hi'][1]>=-.3 and o['lo'][1]<=13.2]
 for o in sorted(obs,key=lambda o:sign*(o['lo'][axis]+o['hi'][axis])/2,reverse=True):
  n=o['name'].lower();v.shp(shape_project(o,axes),.13,INK,'#e4f0f3' if any(t in n for t in ['vidrio','dvh']) else '#ffffff')

def plan_refs(v):
 v.line((18,-.5),(18,13.7),.2,BLUE,True,'EJES');v.label(18,-.65,'A / A06',2.6,BLUE,True);v.label(18,13.65,'A',2.6,BLUE,True)
 v.line((12.5,3),(22.6,3),.2,BLUE,True,'EJES');v.label(12.35,3,'B',2.6,BLUE,True);v.label(22.6,3,'B / A06',2.6,BLUE,True)

def dims_envelope(v):
 v.dimx(14,22,-1.35,0);v.dimx(14,14.2,-.7,0);v.dimx(14.2,21.8,-.7,0);v.dimx(21.8,22,-.7,0)
 v.dimy(0,12,23.05,22);v.dimy(0,6,22.55,22);v.dimy(6,12,22.55,22)

def room(v,x,z,title,sub=''):
 v.label(x,z,title,3.0,INK,True)
 if sub:v.label(x,z+.24,sub,2.6,GREY)

def pivot(v,p,rad,theta0,theta1,label):
 pts=[(p[0]+rad*math.cos(t),p[1]+rad*math.sin(t)) for t in np.linspace(theta0,theta1,18)]
 for q,r in zip(pts,pts[1:]):v.line(q,r,.12,BLUE,True)
 v.line(p,pts[-1],.3,BLUE);v.label(p[0],p[1]-.16,label,2.5,BLUE)

# PAGE 00
begin('A00','Indice y criterios','Juego coordinado para revision independiente; video pausado')
text(22,56,'LA PROPIEDAD COMPLETA, EN UNA MISMA VERSION',7.5,INK,True)
para(22,70,'Plantas, fachadas, cortes y detalles extraidos del archivo Blender indicado en cada cartela. Las anotaciones distinguen fuente dimensional, geometria medida y propuestas pendientes.',535,3.5,leading=5.5)
INDEX=[('A01','Implantacion, paisaje y perimetro','1:100 / 1:50'),('A02','Planta baja y vanos','1:50'),('A03','Planta alta, estudio y vivienda','1:50'),('A04','Cubiertas y coordinacion pluvial','1:50 / esquema'),('A05a / A05b','Cuatro fachadas','1:50'),('A06','Cortes generales A-A y B-B','1:50'),('A07','Escalera, descanso y acceso','1:20 / 1:5'),('A08','Pileta y bordes','1:25'),('A09','Banos: plantas y elevaciones','1:20'),('A10','Quincho y cocinas','1:25'),('A11','Estudio y tratamiento acustico','1:25 / 1:50'),('A12','Carpinterias y herreria','Cuadros / 1:25'),('A13 / A13b','Encuentros de envolvente','1:5 / 1:10'),('A14','Estructura conceptual','1:50 / 1:10'),('A15','Instalaciones coordinadas','1:100 / esquemas'),('A16','Superficies, decisiones y trazabilidad','Cuadros')]
table(22,93,[30,193,50],['Hoja','Contenido','Escala'],INDEX,13)
notes(330,96,'COMO LEER ESTE JUEGO',[
'F - Fuente: cotas expresas del HTML original y decisiones del propietario.',
'G - Geometria: medida derivada de la version Blender identificada por SHA256. No equivale a un relevamiento de obra.',
'P - Propuesta: coordinacion o solucion grafica inferida. Validar antes de construir.',
'Niveles referidos al cero del modelo. No hay relevamiento altimetrico ni mensura catastral.',
'Ubicacion declarada: Virrey del Pino, Buenos Aires. Norte orientativo segun propietario: con la calle arriba, abajo a la izquierda.',
'Servicios de red disponibles segun propietario. Posiciones, cotas y condiciones exactas de acometida pendientes.',
'Escalas fisicas para impresion al 100 %. DXF en metros; cada vista se separa horizontalmente en espacio modelo.'
],228)
notes(330,286,'JERARQUIA GRAFICA',[
'0,50 mm: contorno de piezas cortadas. Relleno gris: material seccionado.',
'0,18 / 0,13 mm: proyecciones, mobiliario y contexto.',
'Azul: cotas, niveles, referencias y criterios de coordinacion.',
'No constituye proyecto ejecutivo ni calculo estructural, sanitario, electrico o acustico.'
],228)
end()
# PAGE 01
begin('A01','Implantacion, paisaje y perimetro','Calle arriba; norte orientativo segun propietario')
v=View(36,76,[-1,24,-2,22],100,True,'01 Implantacion general')
v.poly([(0,0),(22,0),(22,20),(0,20)],.45);v.poly([(14,0),(22,0),(22,12),(14,12)],.4,INK,PALE)
v.poly([(13,5),(14,5),(14,12),(22,12),(22,13),(13,13)],.2)
v.poly([(12,14),(21,14),(21,19),(12,19)],.2,GREY,'#f5f2ec');v.poly([(13,15),(20,15),(20,18),(13,18)],.3,BLUE,'#e5f1f5')
for o in OB:
 n=o['name'].lower();lo,hi=o['lo'],o['hi']
 if any(t in n for t in ['huerta cantero','huerta sendero','banco huerta','camino acceso']) and not 'marco' in n:v.poly([(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])],.13,GREY,PALE)
 if 'tronco' in n and 'lote' in n and lo[0]>=0 and hi[0]<=22 and lo[1]>=0 and hi[1]<=20:
  x,z=(lo[0]+hi[0])/2,(lo[1]+hi[1])/2;v.poly([(x+1.1*math.cos(t),z+1.1*math.sin(t)) for t in np.linspace(0,2*math.pi,40)],.15,'#779084')
v.label(11,-.85,'CALLE CEDRO MISIONERO',3.4,INK,True);v.label(18,2.5,'CASA 8,00 x 12,00',3.0);v.label(18,4,'PB + PA',2.7);v.label(16.5,16.5,'PILETA 7,00 x 3,00',2.7);v.label(4.7,8.5,'HUERTA',2.7)
v.dimx(0,22,-1.65,0);v.dimy(0,20,23,22);v.dimx(0,14,20.75,20);v.dimx(14,22,20.75,20);v.dimy(12,15,22.5,22);v.dimy(18,20,22.5,22);v.dimx(20,22,19.75,18)
v.dimx(11,14,-.2,0,'Hoja 3,00 / luz 2,75');v.bar(0,21.7,5)
# north vector down-left on page
line(312,78,298,92,.6,BLUE);poly([(298,92),(300,85),(305,90)],.2,BLUE,BLUE);text(294,101,'N',4,BLUE,True);para(286,112,'Orientativo; rumbo no relevado.',39,2.6)
notes(341,51,'IMPLANTACION CONSERVADA',[
'F: lote nominal 22,00 x 20,00 m. Casa X=14,00; Z=0,00. Dos modulos de 6,00 m.',
'F: pileta X=13,00; Z=15,00. Distancias nominales del vaso: 2,00 m al fondo y 2,00 m al lateral derecho.',
'F: borde pavimentado de 1,00 m; huerta y centros de los seis arboles de fuente conservados.',
'G: cotas de pavimentos se detallan en A02, A07 y A08. Rasante general del terreno por relevar.',
'G: porton de hoja 3,00 m, luz entre pilares 2,75 m y carrera 3,05 m. No confundir hoja con paso libre.'
],220)
h=View(362,220,[1.6,8.9,3.2,8.6],50,True,'02 Huerta y caminos')
for o in OB:
 n=o['name'].lower();lo,hi=o['lo'],o['hi']
 if any(t in n for t in ['huerta cantero','huerta sendero','banco huerta']) and 'marco' not in n:h.poly([(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])],.2,GREY,PALE)
h.dimx(2.05,4.25,3.45,3.675);h.dimx(5.05,7.25,3.45,3.675);h.dimy(3.675,4.725,7.8,7.25);h.dimy(6.625,7.675,7.8,7.25);h.label(4.65,5.7,'Paso 0,72 m',2.7)
para(342,348,'Perimetro y desniveles: confirmar mensura, cotas de terreno y drenajes exteriores. El norte grafico refleja la referencia del propietario y no un azimut topografico.',219,2.8)
end()
# PB
begin('A02','Planta baja','Corte horizontal G a +1,20 m | referencias A06, A09 y A10')
v=View(54,60,[12,24,-2,14],50,True,'01 Planta baja amoblada');draw_plan(v,1.2,filter_fn=lambda o:'SITE' not in o['collections'] and 'POOL' not in o['collections']);dims_envelope(v);plan_refs(v)
room(v,18,1.2,'MONOAMBIENTE','Piso G +0,21');room(v,16.7,10.45,'QUINCHO','Piso G +0,18');room(v,20.6,5.25,'BANO 01','+0,21');room(v,21.2,10.6,'BANO 03','+0,21')
v.dimx(14.2,19.25,3.55);v.dimx(19.39,21.8,3.55);v.dimy(.2,5.9,23.55,22);v.dimy(4.35,5.9,20.55);v.dimx(14,16.75,6.6,6.1);v.dimx(16.75,19.25,6.6,6.1);v.dimx(19.25,22,6.6,6.1);v.dimx(20.7,21.8,12.55,12);v.dimy(10.17,11.83,23.55,22)
v.label(18,6.28,'P01',2.6,BLUE,True);v.label(19.8,4.1,'P02',2.6,BLUE,True);v.label(21.22,12.17,'P03',2.6,BLUE,True)
pivot(v,(19.46,4.28),.72,0,math.pi/2,'');pivot(v,(21.63,11.92),.82,math.pi,math.pi/2,'');v.bar(12.8,13.8,3)
notes(333,54,'DIMENSIONES Y NIVELES',[
'F: envolvente nominal 8,00 x 12,00 m; espesor exterior 0,20 m. La geometria de piezas puede incluir juntas y salientes.',
'G: piso monoambiente +0,21; quincho +0,18; ambos banos PB +0,21. Saltos entre acabados visibles: no se omiten.',
'G: vano doble monoambiente 2,50 m entre jambas. Las hojas y rieles se describen en A12.',
'G: tabique bano mono 0,14 m. Ancho interior entre pared lateral y medianera aprox. 2,41 m; verificar acabados.',
'G: bano de pileta exterior con acceso desde jardin. Detalle acotado en A09.',
'Barridos azules: pose de apertura esquematica de hojas; la ausencia de colision se audita en el modelo y no se presume por este simbolo.'
],223)
notes(333,223,'LECTURA DE LOS EQUIPOS',[
'Cocina en L e isla del monoambiente: plantas y alturas de mesada en A10.',
'Quincho: horno, bacha y parrilla mantienen la linea de fuente; extracciones independientes hacia patinillo. Ver A10 y A15.',
'La circulacion y los usos se muestran con el mobiliario actual. No se certifican accesibilidad ni condiciones reglamentarias locales.'
],223)
table(333,311,[46,75,94],['Ref.','Ambito','Consultar'],[('P01','Corredera PB','A12 carpinterias'),('P02 / P03','Banos PB / pileta','A09 locales'),('A-A / B-B','Secciones reales','A06 cortes generales')],13)
end()
# PA
begin('A03','Planta alta','Corte horizontal G a +4,50 m | estudio libre 3,20 / vivienda 2,60 m')
v=View(54,60,[12,24,-2,14],50,True,'01 Planta alta amoblada');draw_plan(v,4.5,filter_fn=lambda o:'SITE' not in o['collections']);dims_envelope(v);plan_refs(v)
room(v,17.7,1.1,'ESTUDIO','Piso +3,25 / cielorraso +6,45');room(v,15.8,7.2,'DORMITORIO','+3,25');room(v,18.5,6.65,'VESTIDOR','+3,25');room(v,20.65,6.65,'BANO 02','+3,30');room(v,18.2,10.55,'COCINA / COMEDOR','Piso +3,25 / cielorraso +5,85')
v.dimx(14.2,17.55,8.6);v.dimx(17.69,19.35,8.6);v.dimx(19.49,21.8,8.6);v.dimy(6.1,8.93,23.55,22);v.dimy(9.07,11.8,23.55,22);v.dimx(13,14,12.45,12);v.dimy(12,13,22.65,22)
v.dimy(1.5,4.5,12.6,14);v.dimy(4.84,5.76,12.6,14);v.label(13.65,5.3,'P04',2.5,BLUE,True);v.label(14.38,2,'V01',2.5,BLUE,True);v.label(14.4,7.75,'V02',2.5,BLUE,True);v.label(14.4,10.5,'P08',2.5,BLUE,True);v.label(15.8,12.15,'P09',2.5,BLUE,True);v.label(19.6,12.15,'P10',2.5,BLUE,True)
pivot(v,(18.105,9),.83,0,math.pi/2,'P05');pivot(v,(17.62,8.09),.82,-math.pi/2,0,'P06');pivot(v,(19.42,7.97),.82,-math.pi/2,-math.pi,'P07');v.bar(12.8,13.8,3)
notes(333,55,'ALTURAS AUTORIZADAS',[
'F/G: piso estudio +3,25; cara inferior del cielorraso +6,45 = 3,20 m libres.',
'F/G: piso vivienda +3,25; cielorraso general +5,85 = 2,60 m libres.',
'G: piso bano +3,30; cielorraso bano +5,90 = 2,60 m libres. El escalon local de 50 mm requiere detalle de impermeabilizacion.',
'G: losa entre plantas +3,00 a +3,20; espesor 0,20 m. Acabado general superior 0,05 m.',
'F: acceso exterior unico al nivel alto. Escalera y descanso 1,00 m nominal; detalle del umbral en A07.'
],222)
notes(333,221,'CERRAMIENTOS Y VANOS',[
'F: ventana del estudio 3,00 m. G: paños DVH y marco segun cuadro A12.',
'G: dormitorio, vestidor y bano con puertas operables; cadenas interiores miden entre caras de tabiques del modelo.',
'G: balcon lateral 1,00 m y posterior 1,00 m nominal. Barandas y borde de losa en A12/A13.',
'La composicion acustica, ventilacion silenciosa, ruido de instalaciones y sellado se coordinan en A11; prestaciones aun no calculadas.'
],222)
end()
# CUBIERTAS
begin('A04','Cubiertas y pluviales','Geometria G / trazados P diferenciados | detalles A13')
v=View(52,67,[12,24,-1,14],50,True,'01 Cubiertas y captacion')
for o in sorted([o for o in OB if 'np' in o and any(c in o['collections'] for c in ['ROOF','VENTILATION']) or o['name'].startswith('PL95 |') and 'np' in o],key=lambda o:o['hi'][2]):
 n=o['name'].lower()
 if any(t in n for t in ['nervadura','soporte','patinillo','frontón','revestimiento','abrazadera','ménsula','cámara']):continue
 v.shp(shape_project(o,[0,1]),.2,INK,'#ffffff')
v.dimx(13.7,22.3,-.55,0);v.dimy(0,6,23,22);v.dimy(6,12,23,22);v.dimx(13.7,14,12.8,12);v.label(17.6,2.65,'CUBIERTA ESTUDIO',3.1,INK,True);v.label(17.6,9.25,'CUBIERTA VIVIENDA',3.1,INK,True)
for z1,z2 in [(4.5,1),(7.5,11)]:
 v.line((18,z1),(18,z2),.5,BLUE);endz=z2+.25 if z2<z1 else z2-.25;v.poly([(18,z2),(17.9,endz),(18.1,endz)],.2,BLUE,BLUE)
 v.label(18,z1,'Pendiente G ~18,33 %',2.7,BLUE)
v.label(17.5,5.55,'Escalon entre cubiertas +0,60 m',2.7,BLUE);v.label(17.5,-.18,'Canaleta frontal C1',2.6,BLUE);v.label(17.5,12.25,'Canaleta posterior C2',2.6,BLUE)
for xx,z in ([(13.62,.5),(21.78,12.24)] if CORRECTED else [(21.72,.08),(21.72,11.92)]):v.poly([(xx-.1,z-.1),(xx+.1,z-.1),(xx+.1,z+.1),(xx-.1,z+.1)],.35,BLUE);v.label(xx-.6,z+.35,'BP',2.5,BLUE)
v.bar(13,13.55,3)
notes(327,50,'CONTINUIDAD DEL AGUA',[
'G: pendientes principales conservadas, 1,10 m de subida en 6,00 m de desarrollo horizontal nominal (18,33 %). No es una pendiente pluvial de caneria.',
'G: estudio elevado 0,60 m respecto de la cubierta de vivienda. Alero lateral nominal 0,30 m.',
'Captacion: revisar seccion abierta, embudo, codo y abrazaderas en el modelo de esta emision. El corte de abajo reproduce sus piezas reales.',
'P: conduccion de descarga hasta punto de red pluvial propuesto. Conexion, cota, caudal y diametros finales pendientes de datos de servicio y calculo.',
'No se presume que una bajada dibujada llega a una red existente. A15 identifica el limite de coordinacion.'
],227)
r=View(342,214,[-.45,1.2,-.7,7.5],50,False,'02 Circuito frontal / proyeccion')
if CORRECTED:draw_elev(r,0,1,[1,2],lambda o:o['name'].startswith('PL95 |') and any(t in o['name'].lower() for t in ['frontal','colector','enlace']))
else:draw_cut(r,0,21.72,[1,2],lambda o:any(t in o['name'].lower() for t in ['pluvial','canaleta','captacion','bajada','embudo','codo','registro','descarga']))
r.level(.8,0);r.level(.8,-.57,'Salida P -0,57' if CORRECTED else '-0,57 P');r.level(.8,6.95)
notes(417,242,'PUNTOS DE CONTROL',[
'1. Cubierta hacia canaleta receptora.',
'2. Fondo de canaleta hacia salida.',
'3. Conexion estanca entre piezas.',
'4. Bajada continua y registrable.',
'5. Descarga con destino definido.',
'La continuidad fisica y la prueba de paso se documentan en la auditoria del modelo.'
],142)
end()
# FACADES
for code,pair in [('A05a',[(1,1,[0,2],'01 Frente / Cedro Misionero'),(1,-1,[0,2],'02 Contrafrente / pileta')]),('A05b',[(0,1,[1,2],'03 Lateral de acceso'),(0,-1,[1,2],'04 Medianera lateral')])]:
 begin(code,'Fachadas','Cuatro orientaciones identificadas por la propiedad, sin azimut inventado')
 for idx,(axis,sgn,axes,title) in enumerate(pair):
  ext=[12.5,22.7,-.35,9.25] if axis==1 else [-.4,13.1,-.35,9.25]
  v=View(30+idx*280,78,ext,50,False,title);draw_elev(v,axis,sgn,axes)
  v.line((ext[0],0),(ext[1],0),.3,GREY)
  for h,lab in [(0,'+0,00 modelo'),(3.2,'+3,20 losa'),(6.4,'+6,40 base fuente'),(7,'+7,00 estudio'),(8.1,'+8,10 cumbrera')]:v.level(ext[0]-.1,h,lab)
  v.dimx(14,22,-.9,0) if axis==1 else v.dimx(0,12,-.9,0)
  v.bar(ext[0],-1.35,3)
 notes(42,310,'MATERIALIDAD REPRESENTADA',[
'Ladrillo visto en cerramientos; hormigon en losas, pilares y vigas; cubierta metalica con encuentros y remates; DVH en carpinterias; herreria en balcones y escalera.',
'Los contornos son proyecciones simplificadas de las mallas evaluadas. Los detalles de hojas, capas y fijaciones se leen en A12 y A13; no representan un despiece de fabricacion.'
],510)
 end()
# GENERAL SECTIONS
begin('A06','Cortes generales','A-A longitudinal X=18,00 | B-B transversal Z=3,00 | ver trazas A02/A03')
v=View(37,74,[-.8,14,-.5,9.2],50,False,'A-A Longitudinal por ambas alturas');draw_cut(v,0,18,[1,2],lambda o:'SITE' not in o['collections']);v.line((-.5,0),(13.5,0),.25,GREY)
for h,lab in [(.21,'PB +0,21'),(3,'Losa +3,00'),(3.25,'PA +3,25'),(5.85,'Vivienda +5,85'),(6.45,'Estudio +6,45')]:v.level(-.55,h,lab)
v.dimy(3.25,6.45,3.3,label='3,20 libre');v.dimy(3.25,5.85,9,label='2,60 libre');v.dimx(0,6,-.95,0);v.dimx(6,12,-.95,0);v.label(3,4.4,'ESTUDIO',3.2);v.label(9,4.4,'VIVIENDA',3.2)
v2=View(365,74,[12.6,23.3,-.5,9.2],50,False,'B-B Transversal por estudio');draw_cut(v2,1,3,[0,2],lambda o:'SITE' not in o['collections']);v2.line((13,0),(22.8,0),.25,GREY);v2.dimx(14,22,-.95,0);v2.dimy(3.25,6.45,22.6,label='3,20 libre')
for h in [.21,3.25,6.45]:v2.level(13,h)
notes(37,303,'NIVELES Y CONSTRUCCION',[
'G: losa entre plantas 0,20 m; piso general superior 0,05 m; cielorraso estudio +6,45 y vivienda +5,85. Corte A-A comprueba ambos volumenes y el escalon exterior.',
'F: alturas libres autorizadas 3,20 / 2,60 m. La diferencia se conserva sin desplazar la implantacion ni las huellas de los ambientes.',
'P: continuidad de cargas, fundaciones y conexiones por dimensionar. No hay estudio geotecnico ni verificacion estructural; ver A14.'
],510)
end()
# STAIRS
begin('A07','Escalera, descanso y umbral','18 peldaños de fuente | huella de avance distinta de profundidad de tabla')
v=View(35,70,[12.7,14.6,.8,6.3],20,True,'01 Planta / acceso')
# individual treads projected regardless height
for o in OB:
 if 'np' in o and any(t in o['name'].lower() for t in ['peldaño exterior','descanso escalera','umbral puerta estudio']):v.shp(shape_project(o,[0,1]),.18,INK,'#ffffff')
v.dimx(12.98,13.98,.95,1.194,'1,00 nominal');v.dimy(5,6,14.4,14,'1,00');v.label(13.48,5.5,'DESCANSO',2.8);v.line((13.48,1.55),(13.48,4.75),.5,BLUE);v.label(13.48,3.3,'SUBE 18',2.8,BLUE)
v2=View(161,79,[.1,6.5,-.3,4.65],20,False,'02 Seccion y proyeccion lateral');draw_elev(v2,0,1,[1,2],lambda o:'STAIR' in o['collections'] or o['name'].startswith('AC95 | pavimento'));draw_cut(v2,0,13.48,[1,2],lambda o:any(c in o['collections'] for c in ['STAIR','UPPER_FLOOR','CONSTRUCTION']) or '95' in o['name'])
steps=sorted([o for o in OB if re.fullmatch('Peldaño exterior [0-9]+',o['name'])],key=lambda o:o['hi'][2])
for i,o in enumerate(steps):
 z=o['lo'][1];h=o['hi'][2];v2.label(z+.1,h+.09,str(i+1),2.5,BLUE)
v2.dimy(steps[0]['hi'][2],steps[-1]['hi'][2],5.8,label=f"17 x {(steps[-1]['hi'][2]-steps[0]['hi'][2])/17*1000:.1f} mm")
v2.dimx(steps[0]['lo'][1],steps[-1]['lo'][1],-.1,label=f"17 avances x {(steps[-1]['lo'][1]-steps[0]['lo'][1])/17*1000:.1f} mm")
v2.level(.65,steps[0]['hi'][2],f"Primera tabla {steps[0]['hi'][2]:+.3f}");v2.level(5.1,LANDING,f'Descanso {LANDING:+.2f}');v2.level(.15,.06,'Arranque +0,06') if CORRECTED else None
# Actual threshold cross-section in source X-height at Z=5.3
v3=View(464,84,[13.72,14.3,3.12,3.5],5,False,'03 Umbral / corte Z=5,30');draw_cut(v3,1,5.3,[0,2],lambda o:any(t in o['name'].lower() for t in ['umbral','descanso','piso estudio','rampa','transicion','transición','95']))
v3.level(13.73,3.2,'Losa +3,20');v3.level(13.73,3.25,'NPT +3,25');v3.dimy(3.2,3.25,14.25,label='50 mm')
notes(474,191,'ACCESO',[
('G: acabado del descanso elevado hasta +3,25 en el umbral; la diferencia de 50 mm se absorbe en la capa de terminacion. Pendiente hacia esquina +3,235.' if CORRECTED else 'G: resalto entre descanso y piso de estudio = 50 mm. La geometria del encuentro se muestra ampliada.'),
'F: recorrido nominal 3,80 m; ancho de tabla 1,00 m; descanso 1,00 x 1,00 m.',
f'G: avance repetido {(steps[-1]["lo"][1]-steps[0]["lo"][1])/17*1000:.1f} mm; contrahuella {(steps[-1]["hi"][2]-steps[0]["hi"][2])/17*1000:.1f} mm. No confundir solape con huella util.',
'Arranque, ancho libre entre barandas, altura de pasamanos, anclajes y alcance de manija: comprobar con la auditoria geometrica de esta version.'
],97)
notes(159,339,'COMPROBACIONES DE USO Y ANCLAJES',[
'En el modelo: comprobar pavimento inicial y primera contrahuella, continuidad de pasamanos, proteccion del descanso y recorrido de apertura de la puerta. Secciones de anclaje en A14. No se modifican las cotas de fuente por ajuste grafico.'
],294)
end()
# POOL
begin('A08','Pileta y borde pavimentado','Vaso nominal de fuente 7,00 x 3,00 m | borde 1,00 m')
v=View(43,74,[11.5,21.6,13.5,19.7],25,True,'01 Planta del vaso y playa humeda')
for o in sorted([o for o in OB if selected(o,['POOL'])],key=lambda o:o['hi'][2]):
 if any(t in o['name'].lower() for t in ['agua','baliza','espejo','toallero','baño','zócalo']):continue
 v.shp(shape_project(o,[0,1]),.17,INK,'#ffffff')
v.dimx(13,20,14.55,15);v.dimx(12,13,13.8,14);v.dimx(20,21,13.8,14);v.dimy(15,18,21.35,20);v.dimy(14,15,21.35,21);v.dimy(18,19,21.35,21);v.label(16.8,16.5,'VASO NOMINAL 7,00 x 3,00',3.2,BLUE);v.label(19.15,16.5,'PLAYA',2.8);v.label(13.6,18.5,'ESCALONES',2.6)
notes(467,61,'NIVELES DEL MODELO',[
'G: pavimento perimetral +0,09 m; borde vertical del vaso hasta +0,07 m.',
'G: fondo del vaso entre -1,57 y -1,39 m; espesor representado 0,18 m.',
'G: tres escalones con caras superiores -0,14 / -0,43 / -0,72 m.',
'G: playa humeda superior -0,08 m; escalon intermedio -0,31 m.',
'Agua es un volumen de visualizacion. Nivel operativo, rebalse y resguardo deben definirse en proyecto de pileta.',
'P: skimmer, retornos, toma de fondo, equipo de filtrado y desague requieren ubicacion, dimensionado y seguridad especifica. Esquema en A15.'
],96)
s=View(49,336,[12.5,20.5,-1.8,.4],50,False,'02 Corte transversal al largo / Z=16,50');draw_cut(s,1,16.5,[0,2],lambda o:'POOL' in o['collections'] and 'Agua' not in o['name']);s.level(13,-1.39,'Fondo -1,39');s.level(18.5,-.08,'Playa -0,08')
end()
# BATHROOMS
begin('A09','Banos: plantas y elevaciones','B01 monoambiente | B02 vivienda | B03 pileta / quincho')
baths=[('B01 Monoambiente',[19.1,22.1,4,6.15],1.2,(19.39,21.8,4.35,5.9),.21),('B02 Vivienda',[19.15,22.1,5.95,8.85],4.5,(19.49,21.8,6.1,8.57),3.3),('B03 Pileta',[20.25,22.25,9.85,12.25],1.2,(20.7,21.8,10.17,11.83),.21)]
for i,(title,ext,z,inside,floor) in enumerate(baths):
 x=32+i*189;v=View(x,74,ext,20,True,title);draw_plan(v,z,filter_fn=lambda o:'SITE' not in o['collections']);l,r,t,b=inside;v.dimx(l,r,ext[2]-.14,t);v.dimy(t,b,ext[1]+.15,r);v.label((l+r)/2,(t+b)/2,f'Piso {floor:+.2f}',2.7,BLUE)
 # vertical cut through the sanitary zone
 e=View(x,242,[ext[0],ext[1],floor-.1,floor+2.65],20,False,'Elevacion interior / artefactos');e.poly([(l,floor),(r,floor),(r,floor+2.6),(l,floor+2.6)],.22,INK,None)
 for o in sorted(OB,key=lambda o:o['lo'][1],reverse=True):
  if 'np' not in o:continue
  cx,cz=(o['lo'][0]+o['hi'][0])/2,(o['lo'][1]+o['hi'][1])/2
  if ext[0]<cx<ext[1] and ext[2]<cz<ext[3] and floor-.1<o['lo'][2]<floor+2.6 and any(t in o['name'].lower() for t in ['inodoro','lavatorio','mampara','ducha','espejo','grifer','toallero','bañera','bidet']):e.shp(shape_project(o,[0,2]),.16,INK,None if 'mampara' in o['name'].lower() else '#ffffff')
 e.level(ext[0],floor)
para(32,222,'Los artefactos y mamparas se proyectan desde la malla actual. Cotas interiores entre caras del modelo; confirmar terminaciones, pendientes, accesos de mantenimiento y sellos. Las plantas muestran los vanos; el cuadro de hojas esta en A12.',530,2.8)
end()
# QUINCHO AND KITCHENS
begin('A10','Quincho y cocinas','Equipos, mesadas y extracciones | geometria G / criterios pendientes P')
v=View(33,74,[17.7,22.1,5.8,10.15],25,True,'01 Linea del quincho');draw_plan(v,1.2,filter_fn=lambda o:'SITE' not in o['collections']);v.dimy(6.15,7.35,22.25,21.8,'Horno 1,20');v.dimy(7.5,8.8,22.25,21.8,'Bacha 1,30');v.dimy(8.89,9.99,22.25,21.8,'Parrilla 1,10');v.label(19.3,6.4,'HORNO',2.8);v.label(19.3,8.4,'BACHA',2.8);v.label(19.3,9.45,'PARRILLA',2.8)
c1=View(261,74,[13.95,18.1,3.5,6.2],25,True,'02 Cocina mono / isla');draw_plan(c1,1.2);c1.dimx(15.99,17.71,3.72,4.09,'Isla 1,72');c1.dimy(4.09,5.01,18.2,17.71,'0,92');c1.label(16.85,5.75,'Mesada +1,175',2.7,BLUE)
c2=View(261,223,[18.4,22.1,9.1,12.2],25,True,'03 Cocina vivienda');draw_plan(c2,4.5);c2.label(20.2,12,'NPT +3,25',2.7,BLUE)
notes(450,62,'EXTRACCION Y MANTENIMIENTO',[
'G: horno y parrilla con conductos independientes hacia el patinillo junto al estudio; cocina vivienda con salida independiente.',
'G: diametros representados de horno / parrilla ~0,21 / 0,32 m; son dimensiones de malla, no resultado de calculo.',
'P: verificar longitud desarrollada, radios, caudal, reposicion de aire, temperatura, aislamiento, registro y limpieza.',
'P: conexiones sanitarias de bachas y lavatorios, llaves de corte y sifones requieren detalle de instalacion. A15 ubica los puntos de coordinacion.',
'El patinillo comparte proximidad con el estudio. A11 identifica control termico, vibratorio y acustico pendiente.'
],117)
notes(33,279,'ALTURAS Y RELACION CON LOS LOCALES',[
'G: mesada bacha quincho hasta +1,08 m; mesa quincho +0,825 m; isla mono +1,155 m. Valores medidos sobre el cero del modelo.',
'Comparar alturas de trabajo descontando el piso terminado de cada ambiente. No se confunden cotas absolutas con altura sobre piso.',
'La campana, el faldon y la boca de cada equipo se leen en los cortes del modelo. El tiro de combustion no esta certificado.'
],189)
end()
# STUDIO
begin('A11','Estudio y estrategia acustica','Tratamiento representado; prestaciones sin calcular')
v=View(35,69,[13.8,22.2,-.2,6.25],25,True,'01 Estudio / posiciones y cerramientos');draw_plan(v,4.5,filter_fn=lambda o:'SITE' not in o['collections']);v.dimx(14.2,21.8,-.5,0);v.dimy(.2,5.8,22.4,22);v.label(17.9,1,'FRENTE DE ESCUCHA',3.1,BLUE,True);v.label(18,3.4,'Punto de escucha / verificar',2.8,BLUE);v.line((18,3.1),(18,1.4),.35,BLUE,True)
# Acoustic cloud projection included from actual mesh
for o in OB:
 if 'np' in o and any(t in o['name'].lower() for t in ['cloud estudio','bafle cielorraso']):v.shp(shape_project(o,[0,1]),.13,BLUE,None)
v.label(21.05,5.45,'PATINILLO',2.5,ORANGE);v.label(14.4,3,'DVH',2.5,BLUE);v.label(14.45,5.25,'PUERTA',2.5,BLUE)
notes(407,55,'CRITERIO ACUSTICO PROPUESTO',[
'G: altura libre 3,20 m; cielorraso a +6,45. Paneles y nubes seccionados/coordinados con esa cota.',
'P: identificar primeras reflexiones con posicion final de monitores y oidos. El trazado de escucha es una referencia grafica, no un calculo acustico.',
'P: definir objetivo de aislamiento, RT60 y ruido de fondo antes de asignar espesores o prestaciones.',
'P: sellado perimetral continuo en puerta, DVH y pasos; juntas elasticas y desacople donde el sistema constructivo lo requiera.',
'P: ventilacion silenciosa con recorridos atenuados; controlar vibracion y ruido de equipos. No hay sistema de acondicionamiento dimensionado.',
'P: patinillo de combustion: definir proteccion termica, separacion, juntas y acceso de limpieza sin comprometer el estudio.'
],154)
notes(35,348,'VERIFICACION PENDIENTE',[
'Medicion o simulacion acustica con absorcion real de materiales, volumen util, posiciones definitivas y ruido de instalaciones. No se asignan valores de dB ni tiempos de reverberacion sin evidencia.'
],335)
end()
# CARPENTRY
begin('A12','Carpinterias y herreria','Cuadro de hojas / paños medidos del modelo; vanos y pases en A02/A03')
DOORROWS=[]
REFS=[('P01i','Puerta doble mono izquierda vidrio','Corredera PB / vidrio'),('P01d','Puerta doble mono derecha vidrio','Corredera PB / vidrio'),('P02','Baño mono puerta','Abatible bano mono'),('P03','Puerta baño quincho','Abatible bano pileta'),('P04','Puerta acceso estudio','Acceso estudio'),('P05','Puerta acceso vestidor','Acceso vestidor'),('P06','Puerta dormitorio','Dormitorio'),('P07','Puerta baño vivienda','Bano vivienda'),('V01','Ventana DVH estudio vidrio','DVH estudio / paño'),('V02','Puerta ventana dormitorio vidrio','Lateral dormitorio / paño')]
REFS += [('P08a','Corrediza lateral A vidrio','Corredera lateral A / vidrio'),('P08b','Corrediza lateral B vidrio','Corredera lateral B / vidrio'),('P09','Corrediza posterior A vidrio','Corredera posterior A / vidrio'),('P10','Corrediza posterior B vidrio','Corredera posterior B / vidrio'),('H01','Portón negro','Porton / hoja') ]
for ref,name,desc in REFS:
 o=BY.get(name)
 if not o:continue
 d=[o['hi'][i]-o['lo'][i] for i in range(3)];DOORROWS.append((ref,desc,f'{max(d[:2]):.3f}',f'{d[2]:.3f}',f"{o['lo'][2]:+.3f}",f"{o['hi'][2]:+.3f}"))
table(25,55,[25,128,46,46,46,46],['Ref.','Pieza medida G','Ancho m','Alto m','Base','Tope'],DOORROWS,12)
notes(437,55,'LECTURA DEL CUADRO',[
'Las dimensiones son de hoja o vidrio nombrado. No equivalen automaticamente al vano de obra ni al paso libre.',
'Los marcos, burletes y herrajes amplian o reducen las dimensiones utiles. Ver cotas entre jambas en plantas.',
'G: DVH con dos paños de vidrio; espesor y separacion segun modelo. Prestaciones y composicion final por especificar.',
'P08/P09/P10: correderas vivienda; replantear rieles, solapes, desagues y retenedores a partir del vano real.',
'Porton: hoja 3,00 m; paso libre 2,75 m; carrera 3,05 m. No modificar pilares silenciosamente.'
],132)
notes(26,256,'HERRERIA Y PROTECCION',[
f'F: baranda nominal 1,05 m sobre nivel de balcon. G: eje pasamanos lateral {RAILCENTER:+.2f}; NPT alto {LANDING:+.2f}; diferencia {RAILCENTER-LANDING:.2f} m. Medir altura util donde cambie el acabado.',
'G: postes, barrotes y zancas representados. Separacion de barrotes, resistencia horizontal, soldaduras, placas y anclajes requieren validacion de proyecto.',
'Escalera: 18 tablas de 1,00 m; avance entre tablas ~211,1 mm. A07 muestra el recorrido y el encuentro de acceso; A14 las piezas de soporte.',
'Pendiente: cuadro de fabricacion definitivo con materiales, espesores, tratamientos, sellos, drenajes, tolerancias y accesorios del fabricante.'
],535)
end()
# ENVELOPE DETAILS
begin('A13','Detalles de envolvente','Secciones reales ampliadas; P indica lo que requiere definicion de proyecto')
v=View(36,80,[-.22,1.13,6.65,7.45],5,False,'D01 Alero estudio / X=17,80');draw_cut(v,0,17.8,[1,2],lambda o:isarch(o));v.dimy(6.95,7.03,1.17,label='80 mm aislacion representada')
v2=View(346,80,[5.75,6.6,7.3,8.3],5,False,'D02 Escalon cubiertas / X=17,80');draw_cut(v2,0,17.8,[1,2],lambda o:isarch(o));v2.dimy(7.5,8.1,6.65,label='0,60 m')
notes(36,258,'CAPAS Y GESTION DEL AGUA',[
'G: cubierta metalica, aislacion representada de 80 mm, revestimiento inferior y cabios/correas. La seccion corta las piezas de la malla a su escala real.',
'P: chapa nominal 0,8 mm, fijaciones con sellos, continuidad y solape de membrana, goteron y conexion a canaleta deben confirmarse con el sistema constructivo.',
'P: babeta/contrababeta del salto, retorno de membrana y sellos alrededor de conductos deben formar un drenaje continuo. Dimensionar solapes y fijaciones segun exposicion.',
'P: validar condensacion, viento, dilatacion y puentes termicos con datos climaticos y especificaciones definitivas.'
],270)
notes(346,303,'DVH, UMBRALES Y BALCON',[
'D03: umbral estudio ampliado en A07. D04: borde de balcon y anclaje en A14. D05-D07 en A13b.',
'P: junta perimetral con respaldo y sello compatible; apoyo y calzos de vidrio, drenaje del marco, continuidad de aislacion e impermeabilizacion.',
'Estos textos describen decisiones por desarrollar; no sustituyen piezas ausentes del modelo ni especificaciones de fabricante.'
],218)
end()
# PENETRATIONS AND GUTTER DETAIL
begin('A13b','Captacion, DVH y penetraciones','Ampliaciones de geometria G; especificacion final pendiente')
g=View(35,79,[-.23,.09,6.82,7.18],2,False,'D05 Canaleta abierta / X=14,00')
draw_cut(g,0,14,[1,2],lambda o:'canaleta' in o['name'].lower());g.dimx(-.16,0,6.84,label='0,16 m G');g.label(-.07,7.12,'BOCA RECEPTORA',2.7,BLUE)
d=View(228,80,[13.82,14.3,3.86,4.46],5,False,'D06 DVH / antepecho / Z=3,00')
draw_cut(d,1,3,[0,2],lambda o:any(t in o['name'].lower() for t in ['ventana dvh','estudio antepecho','alféizar','sello']));d.dimx(14,14.2,3.88,label='Muro 0,20')
t=View(370,80,[4.91,5.89,7.7,8.4],5,False,'D07 Paso de conductos / X=21,50')
draw_cut(t,0,21.5,[1,2],lambda o:isarch(o));t.label(5.35,8.3,'CONDUCTOS INDEPENDIENTES',2.7,BLUE)
notes(35,284,'D05 CAPTACION / FIJACION',[
'G: seccion de canaleta recortada directamente de la malla. Verificar apertura superior, fondo, salida lateral y continuidad en la prueba del modelo.',
'P: pendiente longitudinal, caudal, fijacion y sellos requieren dimensionado; el ancho grafico no certifica capacidad pluvial.'
],155)
notes(227,242,'D06 ENCUENTRO DE VENTANA',[
'G: dos paños, marco, antepecho y alféizar representados. La ampliacion permite revisar solapes y contacto.',
'P: definir calzos de apoyo, sellos perimetrales, drenaje del marco y conexion de aislacion sin bloquear las salidas.',
'Ver A12 para anchos, alturas y cotas de cada pieza.'
],125)
notes(370,245,'D07 PENETRACION / PATINILLO',[
'G: conductos independientes, babetas perforadas y remate de patinillo. Se muestra la interseccion con cubierta.',
'P: continuidad de membrana, cuello y contrababetas, dilataciones, aislamiento termico y acceso de limpieza por especificar.',
'No se asignan distancias reglamentarias a combustibles ni caudales sin proyecto de combustion.'
],193)
end()

# STRUCTURE
begin('A14','Estructura conceptual y apoyos','Secciones representadas; sin verificacion de resistencia o suelo')
v=View(45,66,[12.6,23,-.7,13.4],50,True,'01 Planta de apoyos y lineas estructurales')
draw_plan(v,2.8,filter_fn=lambda o:isstruct(o) and 'ROOF' not in o['collections'])
for x,lab in [(14.15,'1'),(21.9,'2')]:v.line((x,-.5),(x,12.6),.17,BLUE,True,'EJES');v.label(x,-.55,lab,3,BLUE,True)
for z,lab in [(.13,'A'),(6.1,'B'),(9,'C'),(11.85,'D')]:v.line((13.2,z),(22.5,z),.17,BLUE,True,'EJES');v.label(13.1,z,lab,3,BLUE,True)
v.dimx(14.15,21.9,-.25,label='7,75 entre ejes representativos');v.dimy(6.1,9,22.6,label='2,90');v.dimy(9,11.85,22.6,label='2,85')
notes(315,55,'CAMINO DE CARGAS A VALIDAR',[
'Cubierta: chapa / aislacion -> correas -> cabios -> vigas de apoyo -> cerramientos / apoyos inferiores.',
'Entrepiso: losa de 0,20 m -> muros y vigas / columnas representados -> fundacion por proyectar.',
'Quincho: columnas 0,30 x 0,30 m y vigas de 0,30 x 0,36 m representadas. Son secciones de malla, no un dimensionado estructural.',
'Balcones: proyeccion 1,00 m; verificar voladizo, continuidad y anclaje con la losa. No se infieren armaduras.',
'Escalera: dos zancas y apoyos de peldaños; definir placas, soldaduras, bulones y anclajes superior/inferior con calculo.',
'Fundaciones ausentes de la fuente: tipo, profundidad, armaduras y capacidad del terreno pendientes de estudio geotecnico y proyecto profesional.'
],250)
e=View(320,281,[12.88,14.25,2.85,4.45],20,False,'D04 Balcon / baranda / Z=9,00');draw_cut(e,1,9,[0,2],lambda o:isarch(o));e.dimy(LANDING,RAILCENTER,14.32,label=f'{RAILCENTER-LANDING:.2f} m eje / NPT')
notes(485,281,'UNIONES',[
'El corte documenta las piezas presentes y sus apoyos aparentes.',
'Los anclajes no se consideran resueltos por estar dibujados: validar sustrato, borde, profundidad y solicitaciones.',
'Acero/hormigon: especificar corrosion, drenajes y juntas.'
],82)
end()
# SYSTEMS
begin('A15','Instalaciones coordinadas','Nodos reales de consumo; enlaces funcionales propuestos P')
v=View(32,80,[0,24,-1,21],100,True,'01 Coordinacion general / PB')
v.poly([(0,0),(22,0),(22,20),(0,20)],.35);v.poly([(14,0),(22,0),(22,12),(14,12)],.25);v.poly([(13,15),(20,15),(20,18),(13,18)],.25,BLUE)
points=[(14.88,4.3,'AF-1'),(20,5.42,'B-1'),(20.69,8.15,'Q-1'),(20.83,10.78,'B-3'),(21.3,7.56,'B-2 PA'),(21.5,10.4,'C-2 PA')]
for x,z,lab in points:
 v.poly([(x-.08,z-.08),(x+.08,z-.08),(x+.08,z+.08),(x-.08,z+.08)],.2,BLUE,BLUE);v.label(x-.7,z,lab,2.5,BLUE)
 v.line((x,z),(21.3,z),.2,BLUE,True,'SISTEMAS')
v.line((21.3,1),(21.3,11),.3,BLUE,True,'SISTEMAS');v.line((21.3,1),(12,1),.3,BLUE,True,'SISTEMAS');v.label(11.7,.5,'ACOMETIDAS P',2.8,ORANGE,True)
v.poly([(20.4,16),(21.4,16),(21.4,17),(20.4,17)],.2,ORANGE);v.label(18.5,19,'Equipo pileta P',2.8,ORANGE);v.line((20,16.5),(20.4,16.5),.2,BLUE,True,'SISTEMAS')
notes(302,52,'AGUA / DESAGUE / PLUVIAL',[
'AF-1 cocina mono; B-1 bano mono; Q-1 quincho; B-3 bano pileta; B-2 bano PA; C-2 cocina PA. Nodos sobre equipos reales del modelo.',
'Las lineas punteadas son relaciones funcionales, no tuberias ejecutivas. Recorridos, diametros, pendientes, ventilaciones, registros y acometidas se definen con el proyecto sanitario.',
'Pluvial: captacion y bajadas en A04. Destino final de descarga propuesto; red y cota de conexion exactas pendientes.',
'Pileta P: skimmer / toma de fondo -> prefiltro / bomba -> filtro -> retornos. Prever valvulas, vaciado, renovacion y medidas de seguridad; equipo y tuberias por calcular.'
],260)
notes(302,200,'ELECTRICIDAD / ILUMINACION / EXTRACCION',[
'Servicios de red disponibles segun propietario. Tablero y medidor propuestos junto al acceso; ubicacion final segun prestador.',
'P: separar circuitos de iluminacion, tomas generales, cocinas, pileta y estudio. Definir potencias, protecciones, puesta a tierra y equipotencialidad.',
'G: luminarias representadas no equivalen a calculo luminotecnico ni conexion electrica.',
'G: conductos de horno, parrilla y cocina presentes. Ver A10: caudal, limpieza, aislamiento y reposicion de aire pendientes.',
'P: ventilacion sanitaria y acondicionamiento del estudio sin dimensionar. Coordinar penetraciones para mantener continuidad termica, acustica y de agua.'
],260)
para(33,334,'CRITERIO DE COORDINACION: localizar consumos y cruces antes de dimensionar redes. Sin cotas de servicio ni calculos no se presenta este esquema como instalacion completa o certificada.',230,3.1,ORANGE,5.1)
end()
# TRACEABILITY AND SURFACES
begin('A16','Superficies y trazabilidad','Registro F / G / P | superficies geometricas no catastrales')
SURF=[('Lote nominal F',22*20,'22,00 x 20,00; limites nominales'),('Huella casa F',8*12,'8,00 x 12,00; incluye quincho'),('Dos niveles nominales F',2*8*12,'192 m2 brutos geometricos; no computo legal'),('Vaso pileta F',7*3,'7,00 x 3,00 nominal'),('Borde pavimentado F',9*5-7*3,'Anillo de 1,00 m nominal')]
for key in ['Piso estudio','Piso vivienda','Piso monoambiente','Piso baño mono','Piso baño vivienda','Piso quincho','Piso baño quincho','Balcón lateral','Balcón posterior','Descanso escalera']:
 o=BY.get(key)
 if o and 'np' in o:SURF.append((key+' G',shape_project(o,[0,1]).area,'Proyeccion real de la pieza; puede solapar otras'))
table(24,55,[100,36,185],['Area / pieza','m2','Metodo / alcance'],[(n,f'{area:.2f}',method) for n,area,method in SURF],13)
notes(375,55,'FUENTES Y REVISION',[
'F: source/scene.json, configuracion y geometria original. Coordenadas fuente X / Z horizontal; Y altura. Blender X / -Z / Y.',
'F: docs/DECISIONES.md: estudio 3,20 m libres, vivienda 2,60 m y video pausado.',
'G: modelo '+MODEL.name+'; SHA256 '+SHA[:24]+'...',
'G: extraccion de mallas evaluadas a cuadro 150, con puertas en su pose de documentacion. Los detalles omiten microgeometria menor para permitir lectura.',
'P: desarrollos constructivos y sistemas inferidos se identifican en sus hojas. No se presentan como verificacion profesional.',
'Las superficies de piezas no son utiles netas de recintos. Existen superposiciones: no sumar pisos de banos a pisos generales sin descontar intersecciones.'
],194)
notes(375,279,'PENDIENTES PARA EMISION FINAL',[
'Mensura y topografia; servicios y cotas exactas; suelos; calculo de estructura, instalaciones, seguridad, clima y acustica.',
'Cierre de observaciones de la auditoria y coherencia con modelo / visor congelados. Umbral critico 9,5 y realismo fotografico siguen siendo condiciones de entrega.'
],194)
para(24,342,'ARCHIVOS: un PDF multipagina vectorial A2; un SVG y un DXF por lamina; geometria.json de extraccion; manifest.json de versiones; verification.json de controles. Los DXF contienen las vistas metricas separadas y cotas; la cartela completa se conserva en PDF/SVG.',322,2.8)
end()
# Final exports and validation
C.save()
manifest={'project':'Casa de Campo','place':'Virrey del Pino, Buenos Aires','status':a.status,'model':str(MODEL),'model_sha256':SHA,'source_sha256':hashlib.sha256((ROOT/'source/scene.json').read_bytes()).hexdigest(),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pdf':'Casa_de_Campo_Planos_A2.pdf','paper_mm':[W,H],'dxf_units':'metres','sheets':SHEETS,'notes':['North indicative from owner; no surveyed azimuth','Network services available per owner; exact connection locations pending','Not a construction-certified project'],'metrics':{'dimension_count':len(METRICS['dimensions']),'view_count':len(METRICS['scales'])}}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf8');(OUT/'measurements.json').write_text(json.dumps(METRICS,indent=2,ensure_ascii=False),encoding='utf8')
PDF=fitz.open(OUT/'Casa_de_Campo_Planos_A2.pdf');verify={'pages':len(PDF),'page_sizes_mm':[[round(p.rect.width/MM,3),round(p.rect.height/MM,3)] for p in PDF],'raster_images':sum(len(p.get_images()) for p in PDF),'text_characters':[len(p.get_text()) for p in PDF],'vector_drawings':[len(p.get_drawings()) for p in PDF],'dxf':[],'minimum_font_mm':2.5,'dimension_count':len(METRICS['dimensions'])}
(OUT/'qa').mkdir(exist_ok=True)
for i,p in enumerate(PDF):p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(OUT/'qa'/f'{SHEETS[i]["id"]}.png')
for sh in SHEETS:
 d=ezdxf.readfile(OUT/sh['dxf']);aud=d.audit();verify['dxf'].append({'file':sh['dxf'],'units':d.units,'entities':len(d.modelspace()),'errors':len(aud.errors)})
(OUT/'verification.json').write_text(json.dumps(verify,indent=2,ensure_ascii=False),encoding='utf8')
from PIL import Image,ImageOps,ImageDraw
thumbs=[]
for i,sh in enumerate(SHEETS):
 im=Image.open(OUT/'qa'/f'{sh["id"]}.png').convert('RGB');im.thumbnail((594,420));tile=Image.new('RGB',(614,450),'#dce3e5');tile.paste(im,(10,10));ImageDraw.Draw(tile).text((12,433),sh['id']+' '+sh['title'],fill='black');thumbs.append(tile)
contact=Image.new('RGB',(614*3,450*math.ceil(len(thumbs)/3)),'white')
for i,t in enumerate(thumbs):contact.paste(t,((i%3)*614,(i//3)*450))
contact.save(OUT/'qa/contact.png')
(OUT/'README.md').write_text('# Planos de revision\n\nEstado: '+a.status+'\n\nModelo: '+MODEL.name+'\nSHA256: '+SHA+'\n\nImprimir PDF/SVG en A2 al 100 %. DXF en metros, vistas separadas en espacio modelo. Cotizaciones y coordenadas fuente en measurements.json.\n\nEste juego documenta el modelo y señala pendientes; no es proyecto ejecutivo certificado.\n',encoding='utf8')
print(json.dumps({'out':str(OUT),'pages':len(PDF),'dimensions':len(METRICS['dimensions']),'vector_drawings':sum(verify['vector_drawings']),'raster_images':verify['raster_images'],'dxf_errors':sum(x['errors'] for x in verify['dxf'])},indent=2))
