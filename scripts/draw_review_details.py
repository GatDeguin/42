from PIL import Image,ImageDraw,ImageFont
import json,os,html,math
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'review')
font=lambda s:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',s)
class Sheet:
 def __init__(self,w,h,title,sub):
  self.w,self.h=w,h;self.im=Image.new('RGB',(w,h),'#fcfbf7');self.d=ImageDraw.Draw(self.im);self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="#fcfbf7"/>'];self.text((w/2,42),title,31);self.text((w/2,86),sub,19,'#64716a')
 def line(self,pts,color='#2c342f',width=2):
  self.d.line(pts,fill=color,width=width);self.svg.append('<polyline points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)+f'" fill="none" stroke="{color}" stroke-width="{width}"/>')
 def polygon(self,pts,color,outline=None):
  self.d.polygon(pts,fill=color,outline=outline);self.svg.append('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)+f'" fill="{color}"'+(f' stroke="{outline}"' if outline else '')+'/>')
 def text(self,p,t,size=20,color='#28372f'):
  self.d.text(p,t,font=font(size),fill=color,anchor='mm');self.svg.append(f'<text x="{p[0]}" y="{p[1]+size*.3}" font-family="Segoe UI,sans-serif" font-size="{size}" text-anchor="middle" fill="{color}">{html.escape(t)}</text>')
 def save(self,name):
  self.im.save(os.path.join(OUT,name+'.png'));open(os.path.join(OUT,name+'.svg'),'w',encoding='utf8').write('\n'.join(self.svg+['</svg>']))
data=json.load(open(os.path.join(OUT,'door_glyphs.json'),encoding='utf8'));s=Sheet(1650,1940,'Carpinterías | poses reales y barridos','Gris: cerrado · Verde: abierto · Pivote y posición extraídos del Blender · Metros')
for i,g in enumerate(data):
 col,row=i%3,i//3;ox,oy=col*550+35,row*435+155
 pts=g['closed']+g['open'];xmin=min(v[0] for v in pts)-.15;xmax=max(v[0] for v in pts)+.15;ymin=min(v[1] for v in pts)-.15;ymax=max(v[1] for v in pts)+.15
 sc=min(430/max(xmax-xmin,.8),290/max(ymax-ymin,.8))
 def p(v):return (ox+32+(v[0]-xmin)*sc,oy+60+(v[1]-ymin)*sc)
 s.text((ox+240,oy),g['key'],24)
 for key,color in [('closed','#bdc5bd'),('open','#3f7866')]:s.polygon([p(v) for v in g[key]],color)
 if g['motion']=='hinge':
  c=g['pivot'];pc=p(c);s.line([(pc[0]-6,pc[1]),(pc[0]+6,pc[1])],'#a75335',2);s.line([(pc[0],pc[1]-6),(pc[0],pc[1]+6)],'#a75335',2)
  # Trace the farthest door corner about its actual pivot through the angular sweep.
  a=max(g['closed'],key=lambda v:(v[0]-c[0])**2+(v[1]-c[1])**2);b=max(g['open'],key=lambda v:(v[0]-c[0])**2+(v[1]-c[1])**2)
  r=math.hypot(a[0]-c[0],a[1]-c[1]);aa=math.atan2(a[1]-c[1],a[0]-c[0]);bb=math.atan2(b[1]-c[1],b[0]-c[0]);da=(bb-aa+math.pi)%(2*math.pi)-math.pi
  arc=[p([c[0]+r*math.cos(aa+da*j/32),c[1]+r*math.sin(aa+da*j/32)]) for j in range(33)]
  for j in range(0,31,2):s.line(arc[j:j+2],'#a75335',2)
 else:
  center=lambda z:[sum(v[k] for v in z)/len(z) for k in [0,1]]
  a,b=center(g['closed']),center(g['open']);s.line([p(a),p(b)],'#a75335',2)
 s.text((ox+240,oy+365),('Giro sobre bisagra' if g['motion']=='hinge' else 'Traslación sobre riel'),19,'#64716a')
s.text((825,1900),'27 poses verificadas contra muros · Hoja del portón 3,00 m; luz entre pilares fuente 2,75 m',21)
s.save('barridos_puertas')
d=json.load(open(os.path.join(OUT,'construction_details.json'),encoding='utf8'));s=Sheet(1900,1450,'Extracción | horno y parrilla independientes','Trayectorias coordinadas con la geometría real; detalle desarrollado donde el HTML no define instalaciones')
# Left panel, longitudinal projection along depth and height.
def elev(z,h):return (115+(z-4.8)*145,1180-(h-0)*111)
s.text((570,145),'Proyección longitudinal | Z fuente / altura',25)
for h,label in [(0,'±0,00'),(2.60,'+2,60'),(3.00,'Losa +3,00 / +3,20'),(3.25,'Piso PA +3,25'),(6.45,'Cielorraso estudio +6,45'),(8.70,'Salida +8,70')]:
 s.line([elev(4.8,h),elev(10.3,h)],'#adb8af',1);s.text((80,elev(4.8,h)[1]),label.split(' ')[0],17,'#64716a')
s.polygon([elev(4.8,3),elev(10.3,3),elev(10.3,3.2),elev(4.8,3.2)],'#d0d2ca')
s.line([elev(4.8,7.0+4.8*1.1/6),elev(6,8.1),elev(6,7.5),elev(10.3,7.5-(10.3-6)*1.1/6)],'#303d37',5)
colors=['#a95536','#347986']
for (name,r,points),color in zip(d['routes'],colors):
 s.line([elev(p[2],p[1]) for p in points],color,round(r*2*111));s.line([elev(p[2],p[1]) for p in points],'#fcfbf7',round((r-.014)*2*111))
 s.text(elev(points[0][2],1.9),name,21,color)
s.text((570,1280),'Conductos bajo losa → patinillo → pasos de cubierta → sombreretes',21)
# Right panel, true plan coordinates of the coordinated section.
def plan(x,z):return (1100+(x-19.2)*220,210+(z-4.8)*160)
s.text((1460,145),'Planta de coordinación | X / Z fuente',25)
def rect(x0,z0,x1,z1,color,txt):
 s.polygon([plan(x0,z0),plan(x1,z0),plan(x1,z1),plan(x0,z1)],color,'#909a91');s.text(plan((x0+x1)/2,(z0+z1)/2),txt,17)
rect(20.455,6.45,21.705,7.19,'#e4e6de','BAÑERA')
rect(21.02,8.95,21.78,10.7,'#e4e6de','COCINA')
rect(21.3025,5.0725,21.8275,5.9275,'#d4e0d4','PATINILLO')
for (name,r,points),color in zip(d['routes'],colors):
 s.line([plan(p[0],p[2]) for p in points],color,max(3,round(r*2*160)))
 # Ends at same XY across levels: distinguish vertical shaft locations.
 q=plan(points[-1][0],points[-1][2]);s.text((q[0]-115,q[1]),name,18,color)
s.text((1460,1250),'Los tramos horizontales pertenecen al nivel bajo losa.',19)
s.text((950,1380),'Diámetros exteriores representados: horno 0,21 m / parrilla 0,32 m. Rutas independientes. Se conserva distribución de ambientes.',21,'#64716a')
s.save('extraccion_coordinada')
print('TECHNICAL_SHEETS_READY')
