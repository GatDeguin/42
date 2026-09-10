"""Dimensional construction supplement, distinct measured geometry G and proposed details P.
No model mutation. PDF/SVG A2 at real scale; DXF in metres.
"""
import sys,json,math,hashlib,argparse,datetime,xml.etree.ElementTree as ET,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT/'planos95/_vendor'))
import numpy as np,ezdxf,pymupdf
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from shapely.geometry import Polygon,box
from shapely.ops import unary_union
AP=argparse.ArgumentParser();AP.add_argument('--out',default='planos95/details95');AP.add_argument('--geometry',default='planos95/pass3c/geometry.json');AP.add_argument('--anchor-geometry');AP.add_argument('--bearing-details',default='review95/bearing_details_3c.json');args=AP.parse_args()
OUT=ROOT/args.out;OUT.mkdir(parents=True,exist_ok=True);DATA=json.loads((ROOT/args.geometry).read_text(encoding='utf8'));OB={o['name']:o for o in DATA['objects']};ANCH=json.loads((ROOT/args.anchor_geometry).read_text(encoding='utf8')) if args.anchor_geometry else None
assert hashlib.sha256(Path(DATA['model']).read_bytes()).hexdigest()==DATA['sha256'], 'Geometry/model SHA mismatch'
W,H=594,420;MM=72/25.4;G='#384c55';P='#1c6b92';R='#a25228';GREY='#75838a';LIGHT='#edf1f2';PLIGHT='#e4f2f8';WHITE='#ffffff'
pdfmetrics.registerFont(TTFont('A','C:/Windows/Fonts/arial.ttf'));pdfmetrics.registerFont(TTFont('AB','C:/Windows/Fonts/arialbd.ttf'))
PDFNAME='Suplemento_Detalles_95_A2.pdf';C=canvas.Canvas(str(OUT/PDFNAME),pagesize=(W*MM,H*MM));C.setTitle('Casa de Campo | Detalles G y propuestas P');SHEETS=[];DIMS=[];PROPOSALS=[];MEAS=[];SVG=[];CAD=None;MS=None;PAGE='';vi=0
SOURCES={
'R1':('Lysaght: Roofing & Walling Installation Manual, §§7.9 y11','https://cdn.dcs.lysaght.com/download/lysaght-roofing-walling-installation-manual'),
'R2':('Vitro TD-140: Large Insulating Glass Units, p.4','https://www.vitroglazings.com/media/fzzavcjr/tech_doc_140.pdf'),
'R3':('GIK Acoustics: How to Hang Acoustic Panels','https://www.gikacoustics.net/en-gb/blogs/knowledge-base/how-to-hang-acoustic-panels'),
'R4':('TROX: Splitter sound attenuator, installation manual','https://cdn.trox.de/46e8cdbf6ec5f664/8d90dc4ef7b3/XS_MS_XK_MK_RK_IM_A00000090240_V2_2024_11_GB_en.pdf'),
'R5':('Hilti: Base plates - design considerations','https://www.hilti.com.sg/content/hilti/A2/SG/en/engineering/design-center/anchor-systems/typical-applications/base-plate.html'),
'R6':('ROCKWOOL: Acoustic insulation - installation and flanking','https://www.rockwool.com/north-america/applications/acoustic-insulation/')}
import html

def line(p,q,col=G,w=.18,dash=False):
 C.setStrokeColor(HexColor(col));C.setLineWidth(w*MM);C.setDash([1.8*MM,.9*MM] if dash else []);C.line(p[0]*MM,(H-p[1])*MM,q[0]*MM,(H-q[1])*MM)
 SVG.append(f'<line x1="{p[0]:.4f}" y1="{p[1]:.4f}" x2="{q[0]:.4f}" y2="{q[1]:.4f}" stroke="{col}" stroke-width="{w}"'+(' stroke-dasharray="1.8 .9"' if dash else '')+'/>')
def poly(pts,col=G,fill=None,w=.18,closed=True):
 if len(pts)<2:return
 C.setStrokeColor(HexColor(col));C.setLineWidth(w*MM);C.setDash([]);path=C.beginPath();path.moveTo(pts[0][0]*MM,(H-pts[0][1])*MM)
 for x,y in pts[1:]:path.lineTo(x*MM,(H-y)*MM)
 if closed:path.close()
 if fill:C.setFillColor(HexColor(fill))
 C.drawPath(path,stroke=1,fill=int(fill is not None));SVG.append(f'<{"polygon" if closed else "polyline"} points="'+ ' '.join(f'{x:.4f},{y:.4f}' for x,y in pts)+f'" stroke="{col}" stroke-width="{w}" fill="{fill or "none"}"/>')
def rect(x,y,w,h,col=G,fill=None,lw=.18):poly([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],col,fill,lw)
def text(x,y,s,size=2.9,col=G,bold=False,anchor='start',bg=False):
 s=str(s).replace('–','-').replace('—','-');font='AB' if bold else 'A';width=pdfmetrics.stringWidth(s,font,size*MM)/MM;xx=x-(width/2 if anchor=='middle' else width if anchor=='end' else 0)
 if bg:rect(xx-.6,y-size,width+1.2,size+1,WHITE,WHITE,.0)
 C.setFont(font,size*MM);C.setFillColor(HexColor(col));C.drawString(xx*MM,(H-y)*MM,s)
 SVG.append(f'<text x="{x}" y="{y}" fill="{col}" font-family="Arial" font-size="{size}" font-weight="{"bold" if bold else "normal"}" text-anchor="{anchor}">{html.escape(s)}</text>')
def para(x,y,s,width=170,size=2.8,col=G,leading=4.2):
 row=''
 for word in s.split():
  nxt=(row+' '+word).strip()
  if pdfmetrics.stringWidth(nxt,'A',size*MM)/MM>width and row:text(x,y,row,size,col);y+=leading;row=word
  else:row=nxt
 if row:text(x,y,row,size,col);y+=leading
 return y

def note(x,y,title,items,width=170):
 text(x,y,title,3.5,P,True);y+=7
 for s in items:y=para(x,y,s,width);y+=3
 return y

def source(x,y,key,width=250):
 title,url=SOURCES[key];text(x,y,key+' | '+title,2.5,G);C.linkURL(url,(x*MM,(H-y-1)*MM,(x+width)*MM,(H-y+3)*MM),relative=0,thickness=0)
 SVG.append(f'<a href="{html.escape(url,quote=True)}"><rect x="{x}" y="{y-3}" width="{width}" height="5" fill="transparent"/></a>')

def begin(code,title,subtitle):
 global SVG,CAD,MS,PAGE,vi
 PAGE=code;vi=0;SVG=[f'<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" viewBox="0 0 594 420"><rect width="594" height="420" fill="white"/>'];CAD=ezdxf.new('R2010');CAD.units=6;MS=CAD.modelspace()
 for name,color in [('G_MEDIDO',8),('P_PROPUESTO',5),('COTAS',4),('TEXTOS',7),('REVISAR',30)]:CAD.layers.new(name,dxfattribs={'color':color})
 rect(10,10,574,400,G,None,.3);text(19,22,'CASA DE CAMPO / DETALLES 95',4.8,G,True);text(575,22,code+' | '+title,4.2,G,True,'end');text(19,30,'VIRREY DEL PINO, BUENOS AIRES',2.6,GREY);text(575,30,subtitle,2.6,GREY,anchor='end');line((10,37),(584,37),G,.25)
 text(20,47,'G = medido / gris',2.7,G,True);text(112,47,'P = propuesta dimensional / azul',2.7,P,True);text(288,47,'Todas las cotas en mm salvo niveles en m',2.7,GREY)
 line((10,383),(584,383),G,.3);text(20,391,'EN REVISION - PROPUESTAS DE COORDINACION, SIN CALCULO DE CAPACIDAD',2.9,R,True)
 text(20,399,'Base G: '+Path(DATA['model']).name+' / '+DATA['sha256'][:16],2.5,GREY);text(20,406,'G acredita geometria, no capacidad. P completa detalles aun no incorporados al modelo.',2.5,GREY)
 text(575,392,'A2 / imprimir al 100 %',2.8,G,anchor='end');text(575,405,f'{len(SHEETS)+1:02d} / 10-09-2026',2.5,GREY,anchor='end');SHEETS.append({'id':code,'title':title,'svg':code+'.svg','dxf':code+'.dxf'})
def end():
 (OUT/(PAGE+'.svg')).write_text('\n'.join(SVG+['</svg>']),encoding='utf8');CAD.saveas(OUT/(PAGE+'.dxf'));C.showPage()

class V:
 def __init__(self,x,y,w,h,scale,title):
  global vi
  self.x=x;self.y=y;self.w=w;self.h=h;self.s=scale;self.off=vi*10;vi+=1;self.title=title;text(x,y-7,title+' | 1:'+str(scale),3.2,P,True)
 def p(self,p):return self.x+p[0]/self.s,self.y+(self.h-p[1])/self.s
 def cad(self,p):return self.off+p[0]/1000,p[1]/1000
 def layer(self,c):return 'P_PROPUESTO' if c==P else 'REVISAR' if c==R else 'G_MEDIDO'
 def line(self,p,q,c=G,w=.2,dash=False):line(self.p(p),self.p(q),c,w,dash);MS.add_line(self.cad(p),self.cad(q),dxfattribs={'layer':self.layer(c)})
 def poly(self,ps,c=G,fill=None,w=.2):poly([self.p(p) for p in ps],c,fill,w);MS.add_lwpolyline([self.cad(p) for p in ps],close=True,dxfattribs={'layer':self.layer(c)})
 def path(self,ps,c=P,w=.3):
  for a,b in zip(ps,ps[1:]):self.line(a,b,c,w)
 def rect(self,x,y,w,h,c=G,fill=None,lw=.2):self.poly([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],c,fill,lw)
 def circle(self,x,y,r,c=P,fill=None):self.poly([(x+r*math.cos(t),y+r*math.sin(t)) for t in np.linspace(0,2*math.pi,40)],c,fill,.18)
 def tag(self,x,y,s,c=G):text(*self.p((x,y)),s,2.6,c,True,'middle',True)
 def label(self,x,y,s,c=G,size=2.8):text(*self.p((x,y)),s,size,c,False,'middle',True);MS.add_text(s,dxfattribs={'insert':self.cad((x,y)),'height':size*self.s/1000,'layer':'TEXTOS'})
 def call(self,p,xy,s,c=P,width=160):
  a=self.p(p);x,y=xy;mid=(x-4,y-1);line(a,mid,c,.15);line(mid,(x-1,y-1),c,.15);para(x,y,s,width,2.7,c,4.0)
 def dx(self,a,b,y,ref=None,label=None,c=P):
  p,q=self.p((a,y)),self.p((b,y));line(p,q,c,.13)
  for x in [a,b]:
   p0=self.p((x,y));line((p0[0]-1,p0[1]+1),(p0[0]+1,p0[1]-1),c,.2)
   if ref is not None:line(self.p((x,ref)),(p0[0],p0[1]+1.5),GREY,.1)
  text((p[0]+q[0])/2,p[1]-1.5,label or f'{b-a:g}',2.6,c,anchor='middle',bg=True);DIMS.append({'sheet':PAGE,'view':self.title,'axis':'x','from_mm':a,'to_mm':b,'value_mm':b-a,'label':label,'class':'P' if c==P else 'G'})
  MS.add_linear_dim(base=self.cad((a,y)),p1=self.cad((a,ref if ref is not None else y)),p2=self.cad((b,ref if ref is not None else y)),angle=0,override={'dimtxt':2.6*self.s/1000,'dimasz':.007},dxfattribs={'layer':'COTAS'}).render()
 def dy(self,a,b,x,ref=None,label=None,c=P):
  p,q=self.p((x,a)),self.p((x,b));line(p,q,c,.13)
  for y in [a,b]:
   p0=self.p((x,y));line((p0[0]-1,p0[1]+1),(p0[0]+1,p0[1]-1),c,.2)
   if ref is not None:line(self.p((ref,y)),(p0[0]+1.5,p0[1]),GREY,.1)
  text(p[0]+2,(p[1]+q[1])/2+1,label or f'{b-a:g}',2.6,c,bg=True);DIMS.append({'sheet':PAGE,'view':self.title,'axis':'y','from_mm':a,'to_mm':b,'value_mm':b-a,'label':label,'class':'P' if c==P else 'G'})
  MS.add_linear_dim(base=self.cad((x,a)),p1=self.cad((ref if ref is not None else x,a)),p2=self.cad((ref if ref is not None else x,b)),angle=90,override={'dimtxt':2.6*self.s/1000,'dimasz':.007},dxfattribs={'layer':'COTAS'}).render()
 def arrow(self,p,q,c=P):
  self.line(p,q,c,.4);a=np.array(q)-np.array(p);a=a/(np.linalg.norm(a) or 1);n=np.array([-a[1],a[0]]);v=np.array(q);self.poly([v,v-a*self.s*3+n*self.s,v-a*self.s*3-n*self.s],c,c)
 def hatch(self,x,y,w,h,c=GREY,step=40):
  for k in np.arange(-h,w,step):
   p=(max(x,x+k),y+max(0,-k));q=(min(x+w,x+k+h),y+min(h,w-k))
   if q[0]>=p[0] and q[1]>=p[1]:self.line(p,q,c,.1)
 def profile(self,name,axes,origin,c=G):
  o=OB[name];verts=np.array(o['v'])[:,axes]*1000-np.array(origin);pol=[]
  for f in o['f']:
   p=Polygon(verts[f]);
   if p.is_valid and p.area>.005:pol.append(p)
  sh=unary_union(pol).intersection(box(0,0,self.w,self.h))
  for p in list(sh.geoms) if hasattr(sh,'geoms') else [sh]:
   if p.geom_type=='Polygon':self.poly(list(p.exterior.coords),c,LIGHT,.25)

# source measurement register
outer=OB['Ventana DVH estudio vidrio'];inner=OB['Ventana DVH estudio Vidrio interior'];glass1=(outer['hi'][0]-outer['lo'][0])*1000;glass2=(inner['hi'][0]-inner['lo'][0])*1000;gap=(inner['lo'][0]-outer['hi'][0])*1000;total=(inner['hi'][0]-outer['lo'][0])*1000
MEAS += [{'item':'DVH exterior','value_mm':glass1,'source':outer['name']},{'item':'DVH interior','value_mm':glass2,'source':inner['name']},{'item':'DVH clear cavity','value_mm':gap,'source':'inner.minX - outer.maxX'},{'item':'DVH total package','value_mm':total,'source':'inner.maxX - outer.minX'}]
# D01
begin('D01','Alero, capas y union de remates','Responde C1 / C3 | relacion con A04 y A13 del juego general')
v=V(31,88,1200,780,5,'01 Alero propuesto sobre espesores G');s=.183333
h=lambda x:450+s*(x-160)
# insulation and metal profiles
v.poly([(120,h(120)-80),(1150,h(1150)-80),(1150,h(1150)),(120,h(120))],G,LIGHT,.3)
for x in range(170,1120,80):v.line((x,h(x)-76),(x+45,h(x)-4),GREY,.12)
v.poly([(80,h(80)+20),(1150,h(1150)+20),(1150,h(1150)+20.8),(80,h(80)+20.8)],G,None,.25)
v.line((80,h(80)),(1150,h(1150)),P,.5);v.line((80,h(80)),(80,h(80)-30),P,.5)
# underlay below insulation and substructure
v.line((190,h(190)-82),(1150,h(1150)-82),P,.4);v.rect(280,h(280)-137,45,55,G,LIGHT);v.rect(310,130,80,240,G,LIGHT)
v.rect(200,0,200,220,G,LIGHT);v.hatch(200,0,200,220)
# open gutter and its bracket
v.poly([(0,420),(0,280),(160,280),(160,420),(159,420),(159,281),(1,281),(1,420)],G,None,.3)
v.poly([(-10,270),(175,270),(175,335),(170,335),(170,275),(-10,275)],P,None,.3)
v.line((80,h(80)-30),(80,365),P,.25);v.arrow((600,h(600)+70),(70,350));v.tag(1080,h(1080)+22,'1');v.tag(1000,h(1000)-35,'2');v.tag(910,h(910)-87,'3')
v.dx(0,160,245,280,'160 G',G);v.dy(h(980)-80,h(980),1170,label='80 G',c=G);v.dx(80,120,390,label='40 P');v.dy(280,420,-25,label='140 G',c=G)
v.call((320,h(320)-115),(31,272),'G correa 45 x55; cabio 80 x220 nominal. Secciones del modelo, sin capacidad atribuida.',G,229)
v.call((175,300),(31,289),'P soporte de canaleta: pletina 30 x5, modulo inicial 600; revisar cantidad por carga y soporte real.',P,228)
v2=V(323,88,1100,600,5,'02 Solape de babetas / fijacion P')
v2.rect(40,280,630,.8,P,None,.3);v2.rect(520,282,520,.8,P,None,.3)
for x in [550,640]:v2.circle(x,281.5,3,P,P)
v2.rect(570,230,5.5,70,P,None,.2);v2.rect(561,296,24,3,P,PLIGHT);v2.poly([(567,300),(579,300),(582,306),(579,312),(567,312),(564,306)],P,PLIGHT,.25)
v2.dx(520,670,390,282,'150 P solape');v2.dy(280,295,1070,label='separacion grafica');v2.call((573,310),(327,218),'P tornillo Ø5,5 con arandela EPDM Ø24; penetracion y longitud segun soporte seleccionado.',P,217)
v2.call((640,281),(327,241),'P dos cordones continuos de sellador compatible; espesor final segun producto. La union se fija mecanicamente.',P,219)
note(31,323,'CAPAS / IDENTIFICACION',[
'1 G chapa nominal 0,8. P camara ventilada de20 sobre aislacion; necesita separadores que no aplasten la manta.',
'2 G aislacion80. P membrana exterior drenante y retorno30 al goteron. 3 P continuidad de control de aire/vapor por debajo; tipo segun estudio higrotermico.'
],250)
note(323,292,'DECISION DIMENSIONAL P',[
'Solape150 de remates; retorno20 de borde; sello neutro compatible; fijacion inicial cada300 en remate. No se traslada como tabla de fijacion de la chapa a correas.',
'El detalle muestra orden de capas y salida del agua. Los espesores submilimetricos se dibujan con peso de linea legible, sin escalarlos como material mas grueso.'
],245)
source(323,367,'R1',245);end()
# D02
begin('D02','Escalon de cubierta y penetraciones','Responde C3 / C5 | laminas A13 y A13b')
v=V(30,78,1300,1200,5,'03 Encuentro escalonado / seccion P')
# upper and lower roof ends; 600 step at x600
v.poly([(0,900),(600,1010),(600,1010.8),(0,900.8)],G,None,.3);v.poly([(0,820),(600,930),(600,1010),(0,900)],G,LIGHT,.3)
v.poly([(650,410),(1300,290.8),(1300,291.6),(650,410.8)],G,None,.3);v.poly([(650,330),(1300,210.8),(1300,290.8),(650,410)],G,LIGHT,.3)
v.rect(565,300,160,600,G,LIGHT);v.hatch(565,300,160,600)
# proposed metal cap and apron, underlay returns and movement fold
v.path([(440,999),(625,1033),(758,1010),(758,660),(748,650),(748,545),(915,514),(928,494)],P,.45)
v.path([(670,795),(675,795),(675,445),(960,393),(960,388),(670,440)],P,.4)
v.line((675,590),(745,590),P,.4);v.line((675,615),(745,615),P,.4)
v.path([(645,922),(647,925),(662,922),(662,575),(690,570),(690,420),(1050,354)],P,.35)
v.arrow((785,775),(800,520));v.arrow((950,540),(1160,490))
v.dy(410,1010,1260,label='600 G desnivel',c=G);v.dy(545,795,1140,label='250 P solape vertical');v.dx(758,928,850,label='170 P ala');v.dy(590,615,460,label='25 P pliegue')
v.call((665,575),(29,330),'P membrana continua con pliegue flexible25; retorno vertical180 sobre faldon inferior. No puente rigido entre paños que impida dilatacion.',P,245)
v2=V(338,83,1000,920,5,'04 Paso de conducto / remate P')
v2.rect(0,260,1000,80,G,LIGHT);v2.line((0,342),(1000,342),G,.3)
v2.rect(400,180,210,700,G,None,.3);v2.rect(385,180,15,700,P,PLIGHT);v2.rect(610,180,15,700,P,PLIGHT)
# curb and weather collar
v2.path([(150,341),(320,341),(320,575),(695,575),(695,341),(850,341)],P,.45)
v2.path([(285,550),(350,620),(388,620),(388,650),(620,650),(620,620),(667,620),(730,550)],P,.4)
v2.path([(170,345),(310,345),(310,570),(315,570)],P,.3);v2.arrow((220,580),(180,420));v2.arrow((745,545),(900,360))
v2.dy(342,575,920,label='233 P zocalo');v2.dx(400,610,830,label='210 G conducto',c=G);v2.dx(320,695,740,label='375 P hueco exterior')
v2.call((389,600),(337,282),'P collar partido desmontable, abrazadera y junta compatible con temperatura. Conducto aislado no queda rigidamente pegado a la babeta.',P,228)
note(337,319,'SERVICIO Y AGUA',[
'P bandeja superior con desvio lateral; retorno200 contra cuello, solape150 en falda y goteron20. No obstruir canales del perfil.',
'P acceso desmontable de300 x300 al registro del patinillo. Aislamiento y distancias a combustibles requieren seleccion del sistema de combustion.'
],232);source(30,370,'R1',260);end()
from shapely.geometry import LineString
def model_section(view,cut_axis,cut_m,display_axes,origin_mm):
 segs=[];clip=box(0,0,view.w,view.h)
 for o in OB.values():
  if not o.get('v') or o['lo'][cut_axis]>cut_m+1e-6 or o['hi'][cut_axis]<cut_m-1e-6:continue
  lo=np.array(o['lo'])[display_axes]*1000-np.array(origin_mm);hi=np.array(o['hi'])[display_axes]*1000-np.array(origin_mm)
  if hi[0]<0 or hi[1]<0 or lo[0]>view.w or lo[1]>view.h:continue
  verts=np.array(o['v'])
  for face in o['f']:
   vs=verts[face];ds=vs[:,cut_axis]-cut_m
   if min(ds)>1e-7 or max(ds)<-1e-7 or max(abs(ds))<1e-7:continue
   hits=[]
   for j,pa in enumerate(vs):
    pb=vs[(j+1)%len(vs)];da=pa[cut_axis]-cut_m;db=pb[cut_axis]-cut_m
    if abs(da)<1e-8:hits.append(pa)
    elif da*db<0:hits.append(pa+(pb-pa)*(-da)/(db-da))
   if len(hits)<2:continue
   ps=np.unique(np.round(np.array(hits)[:,display_axes]*1000-np.array(origin_mm),6),axis=0)
   if len(ps)<2:continue
   ordering=int(np.argmax(np.ptp(ps,axis=0)));ps=ps[np.argsort(ps[:,ordering])]
   for j in range(0,len(ps)-1,2):
    if np.linalg.norm(ps[j]-ps[j+1])>1e-5:segs.append(LineString([ps[j],ps[j+1]]).intersection(clip))
 merged=unary_union(segs)
 def emit(g):
  if g.geom_type=='LineString':
   pts=list(g.coords)
   for a,b in zip(pts,pts[1:]):view.line(a,b,G,.24)
  elif hasattr(g,'geoms'):
   for part in g.geoms:emit(part)
 emit(merged)

# D03
if 'GL95 | E junta vidrio1 exterior base' in OB:
 begin('D03','DVH: galces y juntas','G vidrio9 / camara17 / vidrio9 | P conexion del marco a obra')
 v=V(34,84,360,300,2,'05 Antepecho / corte real G')
 model_section(v,1,2.25,[0,2],[13800,3980])
 v.dx(167.5,202.5,280,label='35 G DVH',c=G);v.dy(74,80,285,label='6 G taco',c=G)
 if 'GL95 | E asiento alféizar EPDM3' in OB:
  so=OB['GL95 | E asiento alféizar EPDM3'];v.dy((so['lo'][2]-3.98)*1000,(so['hi'][2]-3.98)*1000,285,label='3 G asiento',c=G)
 v2=V(331,84,360,300,2,'06 Jamba / corte real G')
 model_section(v2,2,4.9,[0,1],[13800,1350])
 v2.dx(165.5,204.5,280,label='39 G galce',c=G);v2.dx(176.5,193.5,330,label='17 G camara',c=G)
 para(34,253,'G galce comun39: paquete35 y2mm por cara exterior. Juntas elastomericas2mm a cada cara de los vidrios; toma12mm. El sellador de borde une ambas caras internas sin atravesar los vidrios.',247,2.8)
 para(34,285,('G tacos100x6 por vidrio a1/4 y3/4 de luz; calzo conformado bajo el vidrio interior. Bajo el marco: apoyo continuo3 y juntas1 en rebaje local. Envolvente original conservada; sin carga sobre sello de camara.' if 'GL95 | E asiento alféizar EPDM3' in OB else 'G tacos100x6 por vidrio a1/4 y3/4 de luz; calzo conformado bajo el vidrio interior. No apoya sobre el sellador de camara.'),247,2.8)
 para(34,323,'G se retiraron los24 burletes metalicos macizos incompatibles. Las juntas nuevas son geometria P incorporada; no certifican hermeticidad, capacidad, termica ni acustica. D10 amplía las correderas de balcon.',247,2.8)
 v3=V(333,277,1100,380,5,'P Conexion del marco al soporte')
 v3.rect(80,0,220,230,G,LIGHT,.3);v3.hatch(80,0,220,230)
 v3.rect(260,60,250,12,P,PLIGHT,.3);v3.rect(290,0,10,60,P,PLIGHT,.3)
 for yy in [18,44]:v3.rect(245,yy-4,60,8,P,None,.25);v3.rect(300,yy-7,5,14,P,None,.2)
 v3.rect(315,72,125,3,P,PLIGHT,.2);v3.rect(315,75,125,170,G,None,.3)
 for yy in [85,225]:v3.circle(307.5,yy,6,P,None);v3.rect(300,yy-5,15,10,P,PLIGHT,.2)
 v3.dx(300,315,340,label='15 P junta');v3.dx(260,510,300,label='250 P repisa')
 para(332,357,'P apoyo continuo12 sobre escuadra10, fijacionesØ8 por dimensionar. Junta15 con respaldo y sellos; drenaje a exterior y compatibilidad del sistema pendientes de proyecto.',234,2.7)
 source(34,374,'R2',270);end()
else:
 begin('D03','DVH: apoyo, sello y drenaje','Paquete medido 9 +17 +9 =35 | 26 entre ejes, no camara libre')
 v=V(34,84,1100,1000,5,'05 Corte vertical / marco propuesto P')
 # wall and sill with fall outward (left)
 v.rect(360,0,200,450,G,LIGHT);v.hatch(360,0,200,450)
 # Proposed load path: anchored continuous shelf, bedding, flashing, support profile.
 v.rect(310,450,250,12,P,PLIGHT,.3);v.rect(360,345,8,105,P,PLIGHT,.3)
 v.poly([(310,450),(360,400),(360,450)],P,None,.25)
 for yy in [368,420]:v.rect(355,yy-4,105,8,P,None,.2);v.rect(350,yy-7,5,14,P,PLIGHT,.2)
 v.poly([(310,462),(560,462),(560,477.7),(310,463.4)],P,PLIGHT,.2)
 v.poly([(250,460),(600,480),(600,489),(250,469)],P,PLIGHT,.25);v.line((265,455),(265,425),P,.4)
 v.poly([(310,472.4),(435,479.6),(435,497),(310,497)],P,None,.3);v.rect(310,497,125,3,P,PLIGHT,.25)

 # frame as hollow extrusion envelope125x82
 v.rect(310,500,125,82,P,None,.35);v.rect(315,506,115,55,P,None,.18);v.rect(315,570,115,7,P,None,.18)
 # fixed 9-17-9 package centred
 v.rect(349,582,9,375,G,'#e9f4f9',.2);v.rect(375,582,9,375,G,'#e9f4f9',.2);v.rect(358,582,17,12,P,PLIGHT,.2);v.rect(358,579,17,3,P,P,.2)
 # setting block5 high width45 and under support
 v.rect(344,577,45,5,P,PLIGHT,.25);v.rect(339,570,55,7,P,PLIGHT,.25)
 # weather seals internal external, mechanical fixing and drips
 v.rect(341,590,8,12,P,PLIGHT,.25);v.rect(384,590,8,12,P,PLIGHT,.25);v.path([(305,496),(305,525),(313,525)],P,.4);v.path([(435,496),(435,525),(427,525)],P,.4)
 v.circle(295,511,6,P,None);v.circle(441,511,6,P,None);v.line((327,510),(265,475),P,.4);v.arrow((330,546),(276,506));v.arrow((265,474),(230,443))
 v.call((353.5,925),(158,107),'9 G vidrio exterior',G,102);v.call((366.5,880),(158,119),'17 G camara libre',G,102);v.call((379.5,830),(158,131),'9 G vidrio interior',G,102);v.dx(349,384,1100,label='35 total G',c=G);v.dx(310,435,685,label='125 G envolvente',c=G)
 v.call((340,450),(34,272),'P repisa continua250 x12 con escuadra8 y2 fijacionesØ8 por modulo400; apoyo conformado bajo vierteaguas y perfil de marco, juntaEPDM3. Dimensionar vinculacion al muro.',P,230)
 v.call((370,580),(34,309),'P taco de apoyo100 x45 x5; plataforma portante55 de ancho. Apoya ambos vidrios; no carga sobre el sellador de borde.',P,226)
 v.call((310,510),(34,333),'P drenaje de camara de marco: ranura5 x25 hacia exterior, dos por paño como inicio de desarrollo. No perforar el sello del DVH.',P,227)
 v2=V(337,86,1100,690,5,'06 Jamba / dos lineas de sello P')
 v2.rect(0,100,400,200,G,LIGHT);v2.hatch(0,100,400,200);v2.rect(415,125,125,150,P,None,.3);v2.rect(421,131,113,138,P,None,.2)
 v2.rect(540,181,480,9,G,'#e9f4f9');v2.rect(540,207,480,9,G,'#e9f4f9');v2.rect(540,190,12,17,P,PLIGHT)
 v2.circle(407.5,146,6,P,None);v2.circle(407.5,279,6,P,None);v2.rect(400,130,15,8,P,PLIGHT);v2.rect(400,284,15,8,P,PLIGHT)
 v2.line((452,201),(343,201),P,.35);v2.rect(320,198,130,6,P,PLIGHT);v2.dx(400,415,340,label='15 P junta');v2.dy(190,207,1040,label='17 G',c=G)
 v2.call((409,147),(337,246),'P junta perimetral15: fondo de junta compresible y cordon8 x8 en ambas caras. Centro aislado, sin rellenar los drenajes.',P,228)
 note(337,287,'CALZOS, RETENCION Y MANTENIMIENTO',[
 'P dos tacos de100 en el cuarto y tres cuartos del ancho de cada unidad. Dimension y material finales por peso, compatibilidad y fabricante [R2].',
 'P fijacion de marco Ø6 inicial cada400, primera a150 de esquina; acceso por tapa. Longitud, apoyo y resistencia se dimensionan con muro y carga real.',
 'G el marco del modelo es volumetrico. Cavidades, drenajes y tacos dibujados en azul son un perfil propuesto, no una seccion existente.'
 ],231);source(34,369,'R2',270);end()
# D04
plate=OB['FIX95 | placa interior Baranda lateral poste 1'];grout=OB['FIX95 | grout hasta sustrato Baranda lateral poste 1']
rods=[o for o in DATA['objects'] if o['name'].startswith('FIX95 | v') and 'M10 continuo' in o['name']]
assert len(rods)==68, f'Expected 68 baranda rods, got {len(rods)}'
BEARING=json.loads((ROOT/args.bearing_details).read_text(encoding='utf8'));anchor_checks=[]
for con in BEARING['balcony_connections']:
 for an in con['individual_anchors']:
  near=min(rods,key=lambda o:abs((o['lo'][0]+o['hi'][0])/2-an['x'])+abs((o['lo'][1]+o['hi'][1])/2-an['z']))
  delta=abs(near['lo'][2]-an['anchor_bottom']);embed=an['substrate_top']-near['lo'][2]
  anchor_checks.append({'post':con['post'],'rod':near['name'],'x':an['x'],'z':an['z'],'substrate':an['concrete_object'],'embedment_mm':round(embed*1000,3),'rod_length_mm':round((near['hi'][2]-near['lo'][2])*1000,3),'matches_evidence':delta<.00001})
assert len(anchor_checks)==68 and all(a['matches_evidence'] and abs(a['embedment_mm']-100)<.01 for a in anchor_checks)
(OUT/'anclajes_medidos.json').write_text(json.dumps({'model_sha256':DATA['sha256'],'source':args.bearing_details,'anchors':anchor_checks},indent=2,ensure_ascii=False),encoding='utf8')
MEAS += [{'item':'Baranda regular plate','value_mm':[round((plate['hi'][i]-plate['lo'][i])*1000,2) for i in range(3)],'source':plate['name']},{'item':'Baranda grout at post1','value_mm':round((grout['hi'][2]-grout['lo'][2])*1000,2),'source':grout['name']},{'item':'Baranda rods','count':len(rods),'source':'FIX95 | vastago M10 continuo*'}]
begin('D04','Baranda: placa, apoyo y anclajes','Geometria G / '+Path(DATA['model']).stem.split('_')[-1]+' | propuesta modelada, capacidad pendiente de calculo')
v=V(34,83,1200,970,5,'07 Planta G / placa lateral regular')
v.rect(350,100,750,650,G,None,.25);v.line((350,80),(350,850),G,.45);v.rect(350,400,210,110,G,LIGHT,.4)
v.rect(352.5,437.5,35,35,G,WHITE,.3)
for x in [440,520]:
 for z in [422,488]:v.circle(x,z,11,G,None);v.rect(x-8.5,z-8.5,17,17,G,None,.2);v.circle(x,z,5,G,None)
v.dx(350,560,735,label='210 G',c=G);v.dx(350,440,660,label='90 G',c=G);v.dx(440,520,660,label='80 G',c=G);v.dx(350,520,580,label='170 G al 2do eje',c=G);v.dy(400,510,770,label='110 G',c=G);v.dy(422,488,655,label='66 G',c=G)
v.call((350,350),(34,282),'G canto de losa X=13,00. Ejes interiores a90 y170 mm. Reticula80 x66; cuatro vastagos continuos Ø10 por placa.',G,235)
v.call((370,450),(34,306),'G poste35 x35, centro a20 del canto. La placa210 x110 x12 desarrolla el apoyo hacia el interior.',G,235)
v2=V(333,83,1200,970,5,'08 Corte G / sustrato y anclaje continuo')
v2.rect(350,40,800,160,G,LIGHT);v2.hatch(350,40,800,160);v2.poly([(562,200),(1150,200),(1150,246.55),(562,237.95)],G,LIGHT)
v2.rect(350,254,210,12,G,LIGHT);v2.rect(352.5,266,35,420,G,LIGHT);v2.rect(352,200,206,54,G,LIGHT);v2.hatch(352,200,206,54,G,24)
for x in [440,520]:
 v2.rect(x-5,100,10,184,G,WHITE,.25);v2.rect(x-11,266,22,3,G,LIGHT);v2.rect(x-8.5,269,17,9,G,LIGHT);v2.line((x-6,100),(x+6,100),G,.3)
v2.dx(350,560,755,label='210 G',c=G);v2.dy(100,200,710,label='100 G en H°',c=G);v2.dy(254,266,850,label='12 G',c=G);v2.dy(100,284,1040,label='184 G',c=G)
v2.call((390,224),(334,290),'G cajeado y grout conformado al H° real:54 sobre+3,20;44 sobre+3,21. En junta se adapta al escalon. Placa inferior+3,254.',G,232)
v2.call((520,275),(334,314),'G arandelaØ22 x3, tuerca17 x17 x9 y vástagoØ10 hasta+3,284. Extremo inferior+3,10/+3,11:100 mm dentro de H°.',G,232)
note(34,345,'CASOS Y ALCANCE RESISTENTE',[
'G17 postes unicos. Esquinas:210 x210; primera placa envolvente210 x232 por prolongacion al descanso. Capacidad de placa, soldadura, anclajes, borde y hormigon pendiente por cargas/armado [R5].'
],525);source(34,374,'R5',430);end()
# D05
begin('D05','Escalera: placas, bulones y apoyo','Responde C4 | desarrollo dimensional de union superior e inferior')
v=V(31,84,1250,950,5,'09 Union superior G / envolventes reales')
# normalized G projection plate and bolt heads at local y relative2.8,depth4.6
for nm in ['Placa unión escalera descanso -1','Zanca exterior','Bulón unión escalera -10','Bulón unión escalera -11']:
 v.profile(nm,[1,2],[4600,2800],G)
v.rect(400,240,750,160,G,LIGHT);v.line((400,450),(1100,450),G,.3)
v.dx(305,515,695,label='210 G caja placa',c=G);v.dy(208.8,440,680,label='231,2 G envolvente',c=G);v.dy(260,350,800,label='90 G ejes cabezas',c=G)
v.call((410,310),(31,290),'G la pieza llamada placa es un volumen de130 x210 x231,2 mm. No se interpreta como chapa de130 mm ni como union fabricable.',R,249)
v.call((440,260),(31,314),'G cabezas22 x26 x26; rosca, vástago y tuerca no quedan demostrados por esa envolvente.',G,249)
v2=V(330,84,1200,950,5,'10 P doble cartela / seccion transversal')
v2.rect(400,330,80,330,G,LIGHT);v2.rect(388,330,10,330,P,PLIGHT);v2.rect(482,330,10,330,P,PLIGHT)
for y in [410,500]:
 v2.rect(370,y-8,145,16,P,None,.25);v2.rect(366,y-15,4,30,P,PLIGHT);v2.rect(356,y-12,10,24,P,PLIGHT);v2.rect(498,y-15,4,30,P,PLIGHT);v2.rect(502,y-12,13,24,P,PLIGHT)
v2.dx(388,398,740,label='10 P');v2.dx(400,480,790,label='80 G zanca',c=G);v2.dx(482,492,740,label='10 P');v2.dx(398,400,690,label='2 P holgura');v2.dy(410,500,770,label='90 P ejes');v2.dy(330,660,950,label='330 P cartela')
v2.call((515,500),(332,291),'P2 bulones M16 pasantes por cada union, arandela y tuerca accesible. AgujerosØ18. Longitud inicial145; rosca fuera del plano de corte a definir con proveedor.',P,230)
v2.call((485,620),(332,317),'P cartelas de10, alma entre placas con holgura2 a cada lado. Union a apoyo mediante placa210 x160 x12 y2M12; revisar soldadura y solicitaciones.',P,230)
note(31,349,'ARRANQUE PROPUESTO P',[
'Placa inferior180 x160 x12 sobre grout20;2M12 ejes100 con empotramiento conceptual100 en dado300 x300 x250. Estos tamaños dibujan una reserva de coordinacion: suelo, fundacion, armado y resistencia no estan calculados.'
],525)
source(31,374,'R5',410);end()
# D05b
begin('D05b','Escalera: arranque y plantilla','Propuesta P dibujada para coordinacion | complemento de D05, sin calculo')
v=V(31,84,1200,1060,5,'11 Apoyo inferior / seccion P')
# Ground and a proposed isolated plinth. No reinforcement is inferred.
v.line((60,270),(1060,270),G,.25,True);v.rect(360,50,300,250,P,PLIGHT,.4);v.hatch(360,50,300,250,P,35)
v.rect(420,300,180,20,P,PLIGHT,.25);v.rect(420,320,180,12,P,None,.4)
# Steel stringer end meets the plate; schematic projection preserves80 nominal web depth.
v.poly([(470,332),(550,332),(810,680),(746,728)],P,None,.35)
for x in [460,560]:
 v.rect(x-6,200,12,150,P,WHITE,.25);v.rect(x-13,332,26,3,P,PLIGHT);v.rect(x-9,335,18,10,P,PLIGHT)
v.poly([(470,332),(460,332),(470,342)],P,P,.2);v.poly([(550,332),(560,332),(550,342)],P,P,.2)
v.dx(360,660,0,label='300 P dado');v.dx(420,600,470,label='180 P placa');v.dx(460,560,415,label='100 P ejes');v.dy(50,300,860,label='250 P');v.dy(200,300,735,label='100 P en H°')
v.call((600,320),(32,311),'P placa180 x160 x12; grout20 sobre dado300 x300 x250. Vástagos M12 con100 dentro del hormigon; cabeza, arandela y tuerca accesibles.',P,241)
v.call((740,670),(32,339),'P zanca soldada a placa: contacto continuo, limpieza y proteccion anticorrosiva. Espesor y largo del cordon requieren solicitaciones y material.',P,241)
v2=V(334,84,1200,1060,5,'12 Plantilla de arranque / planta P')
v2.rect(300,250,300,300,P,None,.3);v2.rect(360,320,180,160,P,PLIGHT,.35)
#80 web footprint set aside from the anchor positions
v2.rect(428,330,44,140,P,None,.3)
for x in [400,500]:v2.circle(x,400,13,P,None);v2.circle(x,400,7,P,None)
v2.dx(360,540,695,label='180 P');v2.dx(400,500,630,label='100 P ejes');v2.dy(320,480,690,label='160 P');v2.dx(360,400,560,label='40 P borde');v2.dy(250,550,900,label='300 P dado')
v2.call((500,400),(335,301),'P2 agujerosØ14 para M12. El dibujo reserva montaje y acceso de llave; diametro, tipo de anclaje y tolerancias finales segun sistema seleccionado.',P,233)
v2.call((300,250),(335,331),'P apoyo propuesto fuera del pavimento terminado; ajustar cota a la primera contrahuella del recorrido A07. Suelo, zapata real, armado y cargas no calculados.',P,233)
source(31,374,'R5',430);end()
# D06
begin('D06','Acustica: panel, cielorraso y fijaciones','Responde C6 | se conserva cara inferior libre +6,45 y piso +3,25')
v=V(30,85,1220,1020,5,'11 Panel de80 / montaje P dentro de huella')
v.rect(150,100,200,720,G,LIGHT);v.hatch(150,100,200,720);v.rect(350,200,80,600,G,None,.3)
#50 wool +29 air +1 cloth within80
v.rect(379,212,50,576,P,PLIGHT);v.rect(429,200,1,600,P,None,.35);v.rect(350,200,80,12,P,PLIGHT);v.rect(350,788,80,12,P,PLIGHT)
for y in [240,748]:
 v.poly([(350,y),(374,y),(374,y+16),(367,y+16),(367,y+7),(350,y+7)],P,None,.25);v.rect(320,y,40,6,P,None,.25)
v.dx(350,430,905,label='80 G huella',c=G);v.dx(350,379,850,label='29 P aire');v.dx(379,429,980,label='50 P lana');v.dy(200,800,600,label='600 P modulo');v.call((429,450),(33,308),'P tela porosa1 y velo de contencion; lana mineral50, bastidor12. Aire posterior29. Dos grapas Z desmontables y retenida inferior.',P,232)
v.call((340,747),(33,331),'P fijaciones murales Ø6 a soporte resistente. El bastidor recibe el herraje; no se cuelga de la tela ni de la lana.',P,232)
v2=V(333,85,1220,1010,5,'Cielorraso P sobre bafle G / corte parcial')
# ceiling normalized y0=6.30, keep cloud face150=>6.45
v2.rect(250,150,600,120,G,LIGHT);v2.rect(70,150,150,18,G,LIGHT);v2.rect(880,150,280,18,G,LIGHT)
v2.rect(70,300,1090,15,P,PLIGHT);v2.rect(70,315,1090,15,P,PLIGHT)
v2.rect(70,332,1090,35,P,None,.25);v2.rect(80,375,80,220,G,LIGHT);v2.rect(776,375,80,220,G,LIGHT)
# P secondary steel member bears on brackets screwed to G timber joists.
v2.rect(160,410,616,40,P,PLIGHT,.3);v2.rect(166,416,604,28,P,WHITE,.18)
for x in [160,770]:v2.rect(x,390,6,80,P,PLIGHT,.25)
for xx in [105,765]:
 for yy in [402,459]:v2.rect(xx,yy-4,70,8,P,None,.25)
for x in [280,680]:
 v2.rect(x,270,6,198,P,None,.25);v2.rect(x-9,286,24,5,P,PLIGHT);v2.rect(x-9,337,24,5,P,PLIGHT);v2.rect(x-12,350,30,15,P,PLIGHT);v2.rect(x-8,450,22,3,P,PLIGHT);v2.rect(x-4,453,14,7,P,PLIGHT)
v2.dx(120,816,690,label='696 G ejes cabios',c=G)

v2.path([(210,148),(210,300),(220,300)],P,.3);v2.path([(875,148),(875,300),(865,300)],P,.3)
v2.dy(150,270,1140,label='120 G',c=G);v2.dy(270,300,990,label='30 P aire');v2.dy(300,330,1040,label='2x15 P');v2.label(600,90,'G cara inferior +6,45 =3,20 libre',G)
v2.call((683,452),(333,282),'P4 M6 continuos desde bastidor hasta perfil secundario40 x40 x3, con arandela/tuerca superior y retenida secundaria independiente.',P,232)
v2.call((775,460),(333,305),'P escuadras60 x60 x6 con2 fijacionesØ8 al cabio en cada extremo. Espesor, tornillos y separacion por calcular; la carga no termina en el yeso.',P,232)
v2.call((750,315),(333,327),'P barrera hermetica2x15 a +6,60/+6,63, juntas alternadas y sello perimetral. La nube y la cara visible conservan +6,45. Espacio disponible se coteja contra cabios.',P,232)
source(31,370,'R3',265);source(333,370,'R6',230);end()
# D07
begin('D07','Sellos, pasos y relieve acustico','Responde C6 | puerta hermetica, penetracion y montaje de difusor')
v=V(29,82,1250,980,5,'13 Puerta estudio / umbral y doble sello P')
v.rect(250,50,600,180,G,LIGHT);v.line((160,280),(1120,280),G,.35);v.rect(470,290,65,570,G,LIGHT)
v.rect(447,340,18,540,P,None,.25);v.rect(541,340,18,540,P,None,.25);v.rect(465,355,5,10,P,PLIGHT);v.rect(535,355,5,10,P,PLIGHT)
v.rect(475,290,55,22,P,None,.25);v.rect(479,280,47,10,P,PLIGHT);v.path([(160,278),(1090,278),(1090,255)],P,.35)
v.dy(280,290,680,label='10 P sello caida');v.dx(470,535,930,label='65 G hoja',c=G);v.dx(447,465,860,label='18 P galce');v.call((503,285),(29,308),'P sello automatico de caida10 contra umbral liso; doble junta compresible de5 en galces. Sin nuevo escalon sobre +3,25.',P,249)
v.call((720,278),(29,330),'P bandeja continua bajo umbral y retorno30 a jambas; extremos sellados. El agua drena hacia exterior sin atravesar la linea interior de aire.',P,249)
v2=V(331,84,1210,730,5,'14 Paso de servicio frio / sellado P')
v2.rect(340,100,200,480,G,LIGHT);v2.hatch(340,100,200,480);v2.rect(300,290,285,100,P,WHITE,.25);v2.rect(180,327.5,540,25,P,None,.25)
#annular compressible sealing and collars
for x in [340,525]:
 v2.rect(x,290,15,37.5,P,PLIGHT);v2.rect(x,352.5,15,37.5,P,PLIGHT)
v2.rect(360,296,150,25,P,PLIGHT);v2.rect(360,359,150,25,P,PLIGHT)
v2.dx(340,540,650,label='200 G cerramiento',c=G);v2.dy(290,390,770,label='100 P manguito');v2.dy(327.5,352.5,925,label='25 P tubo');v2.call((525,300),(330,249),'P relleno compresible en anillo y sellos15 de profundidad en ambas caras. Manguito independiente del tubo; registrar conexiones, sin empotrar uniones desmontables.',P,233)
# diffuser actual depths
v3=V(334,305,1180,260,5,'15 Relieve G / soporte posterior P')
depths=[35,58,110,45,85,125,70,28,92]
v3.rect(0,0,756,12,P,PLIGHT)
for i,d in enumerate(depths):v3.rect(i*84,12,52,d,G,LIGHT);v3.label(i*84+26,155,str(d),G,2.5)
v3.dx(0,52,215,label='52 G',c=G);v3.dx(0,84,260,label='84 G paso',c=G);v3.dy(12,137,835,label='125 G max.',c=G)
para(331,370,'G relieve sin desempeño QRD demostrado. P respaldo12, grapa Z18 y retenida inferior; absorcion/difusion se verifican con sala terminada.',238,2.7)
source(29,370,'R6',285);end()
# D08
begin('D08','Ventilacion silenciosa y mantenimiento','Responde C5 / C6 | reserva geometrica P, sin caudal o atenuacion inventados')
v=V(31,83,1630,1160,5,'16 Silenciador recto / planta P')
# internal box1500x600; 50perimeterlining and100centralsplitter, two200passages
v.rect(50,490,1500,600,P,None,.35);v.rect(50,490,1500,50,P,PLIGHT);v.rect(50,1040,1500,50,P,PLIGHT)
v.poly([(200,740),(1350,740),(1500,790),(1350,840),(200,840),(50,790)],P,PLIGHT,.3)
for yy in [640,940]:v.arrow((70,yy),(1520,yy))
v.rect(470,475,660,15,P,None,.25);v.rect(500,465,600,10,P,PLIGHT);v.line((500,460),(500,60),P,.2,True);v.line((1100,460),(1100,60),P,.2,True);v.line((500,60),(1100,60),P,.2,True)
v.label(800,250,'600 P espacio de servicio');v.dx(50,1550,1140,label='1500 P');v.dy(490,1090,1610,label='600 P');v.dy(540,740,-5,label='200 libre P');v.dy(740,840,-5,label='100 P');v.dy(840,1040,-5,label='200 libre P');v.dx(500,1100,425,label='600 P tapa extraible')
v.call((1160,520),(32,327),'P revestimiento absorbente50 retenido con velo y chapa perforada; divisor100. Paso paralelo continuo, sin bafles alternados que estrangulen el recorrido [R4].',P,311)
v.call((800,465),(32,349),'P tapa600 x300 con junta cerrada, tornillos cautivos y acceso600. Dos apoyos de ancho completo, juntas flexibles100 en conexiones.',P,311)
# roomrouting miniature 1:50 inmm
p=V(387,82,8000,6200,50,'17 Reserva P en estudio / coordinacion')
p.rect(200,200,7600,5600,G,None,.3);p.rect(200,5400,600,400,G,None,.2);p.rect(7270,5025,510,780,G,LIGHT)
# transforms sourceX14+ mm, Z direct
p.rect(4300,2800,1500,600,P,PLIGHT);p.rect(5000,3700,1500,600,P,PLIGHT)
p.line((5000,2800),(3000,2800),P,.35);p.line((3000,2800),(3000,400),P,.35);p.rect(2700,300,600,150,P,PLIGHT)
p.line((5750,4300),(6500,4300),P,.35);p.line((6500,4300),(6500,5550),P,.35);p.rect(6200,5550,600,150,P,PLIGHT)
p.label(5050,2300,'Impulsion P',P,2.5);p.label(5750,4700,'Retorno P',P,2.5);p.label(6700,5300,'Patinillo G',G,2.5)
note(389,229,'SECUENCIA FUNCIONAL P',[
'Aire exterior -> filtro -> ventilador -> silenciador -> impulsion. Retorno -> silenciador -> expulsion. Mantener ambos circuitos diferenciados.',
'Reserva de cajas en plenum: X18,30..20,50; Z2,80..4,30; +6,68..+7,08. No ocupa la altura libre3,20; comprobar soportes y accesos antes del modelado.',
'Ductos inicialesØ200, rejillas600 x150 y mangas flexibles100. Secciones P para coordinacion; velocidad, presion, caudal, ruido y condensados se dimensionan con ocupacion y equipo.',
'Tomas exteriores y expulsion deben separarse de combustion y entre si; terminales y distancias finales necesitan la seleccion del sistema.'
],174);source(31,374,'R4',330);end()
# D09 only when a level bathroom finish is present in the selected model.
BATH_NPT=OB.get('Piso baño vivienda',{'hi':[0,0,3.30]})['hi'][2]
if abs(BATH_NPT-3.25)<.01:
 begin('D09','Baño: piso continuo y corredera','G capas y herrajes modelados | solucion dimensional propuesta, sin capacidad validada')
 v=V(32,83,1300,1080,5,'18 Transicion humedo-seco / geometria G')
 v.rect(0,100,1200,200,G,LIGHT,.4);v.hatch(0,100,1200,200,G,45)
 v.rect(0,300,1200,50,G,None,.4)
 # Layers occupy the measured50mm envelope, no raised threshold.
 v.rect(0,300,1200,30,G,None,.2);v.hatch(0,300,1200,30,G,30)
 v.rect(0,330,1200,2,G,LIGHT,.35);v.rect(0,332,1200,8,G,None,.2);v.rect(0,340,610,10,G,LIGHT,.25);v.rect(615,340,585,10,G,LIGHT,.25)
 v.rect(610,332,5,18,G,LIGHT,.35);v.path([(460,331),(760,331)],G,.6)
 v.rect(645,360,40,450,G,None,.3)
 v.dx(610,760,475,label='150 G al seco',c=G);v.dy(300,350,1100,label='50 G',c=G);v.dy(350,360,875,label='10 G bajo hoja',c=G);v.dx(645,685,865,label='40 G hoja',c=G);v.label(260,410,'BAÑO +3,25 G',G);v.label(970,410,'COMEDOR +3,25 G',G)
 v.call((610,342),(33,304),'G junta elastica5 en terminacion; banda flexible bajo baldosa, prolongacion150 al lado seco y retorno en jambas. El paso queda sin resalto.',G,245)
 v.call((490,315),(33,330),'G composicion dentro de50: mortero30 + membrana2 + adhesivo8 + baldosa10. Verificar espesores del sistema elegido y soporte; no duplicar piso general bajo la zona humeda.',G,245)
 v2=V(350,77,2000,2740,10,'19 Corredera modelada / vista parcial G')
 v2.rect(-30,100,140,150,G,LIGHT,.3);v2.rect(-30,2510,140,230,G,LIGHT,.3)
 v2.line((-30,250),(1700,250),G,.35);v2.rect(145,260,40,2240,G,None,.35)
 # Actual rail34x35 and Ø42 external wheels: measured from the selected model.
 v2.rect(156,2555,34,35,G,LIGHT,.3);v2.circle(180,2611,21,G,None)
 v2.rect(194,2465,9,138,G,LIGHT,.25);v2.rect(170,2470.5,33,7,G,None,.25);v2.rect(170,2490.5,33,7,G,None,.25)
 v2.path([(107,2530),(115,2530),(115,2610),(165,2610)],G,.3);v2.rect(80,2564,98,12,G,None,.25)
 v2.line((110,2470),(210,2470),G,.2,True);v2.dy(2470,2500,430,label='30 G solape',c=G);v2.dy(250,2470,-580,ref=110,label='2220 G paso alto',c=G);v2.dy(260,2500,-180,ref=145,label='2240 G hoja',c=G);v2.dx(145,185,1850,label='40 G',c=G)
 vin=V(433,90,260,250,2,'Herraje ampliado G')
 vin.rect(56,55,34,35,G,LIGHT,.35);vin.circle(80,111,21,G,None);vin.rect(94,-35,9,138,G,LIGHT,.25)
 vin.path([(7,30),(15,30),(15,110),(65,110)],G,.3);vin.rect(-20,64,98,12,G,None,.25)
 vin.dx(56,90,175,label='34 G',c=G);vin.dy(55,90,160,label='35 G',c=G);vin.call((80,131),(432,252),'G2 ruedasØ42 apoyan en cara superior+5,590. Pletinas9 y pernosØ7 vinculan carros con hoja.',G,136)
 v2.call((169,261),(397,294),'G guia inferior lateral fuera del paso. Tiradores embutidos en ambas caras, junto al extremo de mesada.',G,164)
 para(355,344,'G hoja superior+5,50; cabezal+5,47; riel+5,555..+5,590. Geometria propuesta incorporada: dimensiones no equivalen a capacidad del herraje ni certificacion de impermeabilidad.',216,2.7)
 source(32,374,'R5',420);end()
# D10: real sectional linework through modelled slider components, not schematic boxes.
if 'SL95 | A rodillo1 diámetro20' in OB:
 begin('D10','Corredizas: pistas, vidrio y drenaje','G componentes medidos de solucion P modelada | ver A03, A05a/b y A12')
 wheel=OB['SL95 | A rodillo1 diámetro20'];cut=(wheel['lo'][0]+wheel['hi'][0])/2
 v=V(35,82,320,370,2,'20 Rodadura / corte exacto de la geometria')
 model_section(v,0,cut,[1,2],[11860,3120])
 v.dx(54.5,99.5,325,label='45 G perfil',c=G);v.dy(77.5,122.5,227,label='45 G',c=G)
 v.call((77,84.5),(34,279),'G rodilloØ20 / ejeØ4; carril8x2; bandeja3; lecho3. Alojamiento26x14x19 en perfil original. Carga, desgaste y seleccion del herraje requieren dimensionamiento.',G,171)
 padname=next(n for n in OB if n.startswith('SL95 | A taco vidrio1-1'))
 pad=OB[padname];cutpad=(pad['lo'][0]+pad['hi'][0])/2
 v2=V(235,82,320,370,2,'21 Acristalamiento / corte por tacos')
 model_section(v2,0,cutpad,[1,2],[11860,3120])
 v2.dx(107.5,142.5,325,label='35 G /9-17-9',c=G);v2.dy(94,100,265,label='6 G taco',c=G)
 v2.call((140,96),(234,279),'G tacos100mm en cuartos de luz;6mm de altura bajo cada vidrio. Puentes metalicos y junquillos conectan vidrio y perfiles; el vidrio interior conserva su retiro vertical3,81mm.',G,174)
 note(427,86,'GEOMETRIA / LIMITES',[
 'G conserva13 rigs, carrera y dimensiones de vidrios. Se vaciaron galces y perfiles; no se movieron los vanos.',
 'Holgura nominal3mm al contorno movil terminado;2mm en galce de vidrio. Felpas y EPDM son geometria propuesta, sin ensayo de estanqueidad.',
 'Rodillos y tacos son una propuesta de montaje. No hay capacidad, durabilidad ni especificacion de producto validada.',
 'Rebajes de losas y dinteles, y perforacionesØ16 para tubosØ14, requieren coordinacion con armado y calculo. No se declara aptitud resistente.'
 ],140)
 v3=V(35,316,320,120,2,'22 Guia superior / corte G')
 model_section(v3,0,cut,[1,2],[11860,5700])
 v4=V(235,312,1300,650,10,'23 Drenaje al borde / corte G')
 drain=OB['SL95 | A drenaje1 Ø14 interior10'];dcut=(drain['lo'][0]+drain['hi'][0])/2
 model_section(v4,0,dcut,[1,2],[11800,2850])
 v4.arrow((310,320),(1210,300),P)
 para(428,325,'G dos salidas por corredera: tuboØ14 / luz10, pendiente2% y codo hueco. Descarga en cara libre del balcon. Requiere prueba de agua y acceso de limpieza antes de obra.',141,2.7)
 end()
# D11 documents the newlymodelled groundfloor wetassembly and usable showerheight.
if 'BTH95 | ducha columna' in OB:
 begin('D11','Ducha: pendientes y conexiones','G geometria incorporada / solucion P de coordinacion | ver A09')
 v=V(34,84,1060,1650,10,'24 Ducha / planta G')
 v.rect(80,100,900,1450,G,None,.4);v.rect(480,775,100,100,G,LIGHT,.3)
 for p0,p1 in [((80,100),(480,775)),((980,100),(580,775)),((980,1550),(580,875)),((80,1550),(480,875))]:v.line(p0,p1,G,.25)
 v.dx(80,980,1600,ref=1550,label='900 G',c=G);v.dy(100,1550,0,ref=80,label='1450 G',c=G)
 v.arrow((200,820),(440,820),G);v.arrow((860,820),(620,820),G);v.arrow((530,1350),(530,930),G);v.arrow((530,300),(530,710),G)
 v.label(530,1260,'2,15% G',G,2.6);v.label(530,405,'2,15% G',G,2.6)
 v.label(530,30,'Laterales3,63% G',G,2.6)
 para(34,271,'G perimetro +0,210; rejilla +0,1955. Cuatro planos medidos: caida14,5mm en400 /675mm hasta borde de desague100x100.',108,2.7)
 para(34,302,'G vidrio fijo12mm y acceso actual944mm. El giro de puerta y las huellas de sanitarios se representan en A09; no se afirma accesibilidad normativa.',108,2.7)
 para(34,340,'G retornos de membrana protegidos tras acabado. P compatibilidad del sistema, prueba de estanqueidad y mantenimiento pendientes.',108,2.7)
 v2=V(172,83,1190,2700,10,'25 Rociador / corte G')
 model_section(v2,0,21.35,[1,2],[4300,0])
 head=OB['Ducha baño mono'];headparts=[o for n,o in OB.items() if n.startswith('Ducha baño mono')];headlow=min(o['lo'][2] for o in headparts)*1000;floor=.21*1000
 if any(n.startswith('Ducha baño mono | boquilla') for n in OB):
  hx0,hx1=head['lo'][1]*1000-4300,head['hi'][1]*1000-4300;bh0,bh1=head['lo'][2]*1000,head['hi'][2]*1000
  v2.dx(hx0,hx1,2440,label=f'Ø{hx1-hx0:.0f} G',c=G);v2.dy(bh0,bh1,800,label=f'{bh1-bh0:.0f} G cuerpo',c=G)
  MEAS.append({'item':'Rociador mono cuerpo y cota libre','diameter_mm':round(hx1-hx0,3),'body_thickness_mm':round(bh1-bh0,3),'minimum_clearance_mm':round(headlow-floor,3),'source':'Ducha baño mono + boquillas'})
 v2.dy(floor,headlow,1090,ref=600,label=f'{headlow-floor:.0f} G libre',c=G)
 v2.label(630,150,'Piso +0,21 G',G,2.6);v2.label(600,2520,f'Cara +{headlow/1000:.2f} G',G,2.6)
 v3=V(315,84,520,510,2,'26 Sumidero / corte de malla G')
 model_section(v3,1,5.075,[0,2],[21090,-150])
 v3.dy(217,267,470,label='50 G',c=G);v3.dx(210,310,475,label='100 G rejilla',c=G)
 v3.dy(310,360,40,label='50 G borde',c=G)
 para(316,352,'G: rejilla apoyada, brida/collar, bajante sumergida y salida localØ40. La cota50 es propuesta geometrica de sello; el ramal y la ventilacion sanitaria requieren proyecto y ensayo.',254,2.7)
 end()
# final outputs
C.save()
# save explicit proposal inventory, not a certified engineering spec
PROPOSALS=[{'sheet':'D01','detail':'Alero','dimensions':'chapa0.8 G; aislacion80 G; camara20 P; solape150 P; goteron30 P; remates cada300 P'}, {'sheet':'D02','detail':'Escalon/penetracion','dimensions':'salto600 G; solapevertical250 P; pliegue25 P; zocalo233 P; cuello375 P'}, {'sheet':'D03','detail':'DVH','dimensions':'9/17/9 G; tacos100x45x5 P; junta15 P; drenajes5x25 P'}, {'sheet':'D04','detail':'Baranda','dimensions':'placa210x110x12 G;4M10 G; ejes90/170 del canto G;100 dentro hormigon G; capacidad pendiente'}, {'sheet':'D05','detail':'Escalera','dimensions':'cartelas10 P;2M16 P; agujeros18 P; ejes90 G/P; dado300x300x250 P'}, {'sheet':'D05b','detail':'Arranque escalera','dimensions':'placa180x160x12 P; grout20 P;2M12 ejes100 P; dado300x300x250 P'}, {'sheet':'D06','detail':'Tratamiento/acondicionamiento','dimensions':'huella80 G; lana50+aire29+tela1 P; barrera2x15 P;4M6 por nube P'}, {'sheet':'D07','detail':'Sellos','dimensions':'juntas5 P; sello caida10 P; manguito100 para tubo25 P; sellos15 P; relieve G28..125'}, {'sheet':'D08','detail':'Ventilacion','dimensions':'caja1500x600x400 P;2pasos200x300 P; splitter100 P; tapa600x300 P; ductos200 P; reserva espacial no cerrada'}]
if 'GL95 | E junta vidrio1 exterior base' in OB:
 PROPOSALS[2]['dimensions']='9/17/9 G; galce39 G; juntas2 G; tacos100x9x6 G por vidrio; repisa250x12 y junta15 P'
manifest={'project':'Casa de Campo','status':'EN REVISION / SUPLEMENTO G-P','model':DATA['model'],'model_sha256':DATA['sha256'],'anchor_model':ANCH['model'] if ANCH else None,'anchor_sha256':ANCH['sha256'] if ANCH else None,'paper_mm':[W,H],'pdf':PDFNAME,'sheets':SHEETS,'proposal_scope':'All P measures are dimensional coordination proposals, not calculations or certified manufacturer details','sources':SOURCES,'measurements':MEAS,'proposal_register':PROPOSALS,'dimensions':DIMS}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf8')
(OUT/'fuentes.md').write_text('# Referencias primarias\n\nSe utilizan principios de montaje; ninguna referencia valida las medidas P ni certifica este proyecto.\n\n'+'\n\n'.join(f'- {k}: [{title}]({url})' for k,(title,url) in SOURCES.items()),encoding='utf8')
(OUT/'README.md').write_text('# Suplemento de detalles95\n\nLaminas A2 con detalles medidos G y propuestas P. Milimetros en detalles; niveles en metros. PDF/SVG al100%; DXF en metros y vistas separadas.\n\nBase G: '+Path(DATA['model']).name+'\nSHA256: '+DATA['sha256']+'\n\nD04 documenta la solucion de apoyo incorporada al modelo identificado: placas interiores, grout hasta hormigon y vastagos continuos. G acredita geometria, no capacidad. No se cambia el modelo ni se presupone que cada pieza P este modelada.\n\nGenerador: scripts/planos95_details_build.py\n',encoding='utf8')
DOC=pymupdf.open(OUT/PDFNAME);(OUT/'qa').mkdir(exist_ok=True);outside=[];minsize=100;svgwrong=[];dxerrors=[];dxcount=0
for i,page in enumerate(DOC):
 page.get_pixmap(matrix=pymupdf.Matrix(1,1),alpha=False).save(OUT/'qa'/f'{SHEETS[i]["id"]}.png')
 for b in page.get_text('dict')['blocks']:
  for l in b.get('lines',[]):
   for sp in l['spans']:
    minsize=min(minsize,sp['size']/MM);x0,y0,x1,y1=sp['bbox']
    if x0<9*MM or x1>585*MM or y0<9*MM or y1>411*MM:outside.append([SHEETS[i]['id'],sp['text'],[round(v/MM,2) for v in sp['bbox']]])
for sh in SHEETS:
 d=ezdxf.readfile(OUT/sh['dxf']);aud=d.audit();dxcount+=len(d.modelspace().query('DIMENSION'))
 if aud.errors or d.units!=6:dxerrors.append([sh['id'],len(aud.errors),d.units])
 r=ET.parse(OUT/sh['svg']).getroot()
 if r.get('width')!='594mm' or r.get('height')!='420mm':svgwrong.append(sh['id'])
validation={'pages':len(DOC),'dimensions':len(DIMS),'native_dxf_dimensions':dxcount,'raster_images':sum(len(p.get_images()) for p in DOC),'paths':sum(len(p.get_drawings()) for p in DOC),'text_outside_frame':outside,'minimum_font_mm':round(minsize,3),'dxf_errors':dxerrors,'svg_size_errors':svgwrong,'model_sha256':DATA['sha256'],'dv_h_gap_mm':gap,'anchor_count':len(anchor_checks),'anchor_evidence_matches':all(a['matches_evidence'] for a in anchor_checks),'limitations':['Proposals not incorporated into the model by this script','No performance, load, code or statutory certification']}
(OUT/'validation.json').write_text(json.dumps(validation,indent=2,ensure_ascii=False),encoding='utf8')
from PIL import Image,ImageDraw
contact=Image.new('RGB',(1228,450*math.ceil(len(SHEETS)/2)),'#dde4e6')
for i,sh in enumerate(SHEETS):
 im=Image.open(OUT/'qa'/f'{sh["id"]}.png');im.thumbnail((594,420));contact.paste(im,(10+(i%2)*614,10+(i//2)*450));ImageDraw.Draw(contact).text((12+(i%2)*614,433+(i//2)*450),sh['id']+' '+sh['title'],fill='black')
contact.save(OUT/'qa/contact.png')
with zipfile.ZipFile(OUT/'Suplemento_Detalles_95_Editables.zip','w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
 for p in OUT.iterdir():
  if p.suffix.lower() in ['.pdf','.svg','.dxf','.md','.json']:z.write(p,p.name)
print(json.dumps(validation,indent=2))
