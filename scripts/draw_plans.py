from PIL import Image,ImageDraw,ImageFont
import json,os,html,math
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'review')
data=json.load(open(os.path.join(OUT,'drawing_geometry.json'),encoding='utf8'))
for spec in data:
 W,H=2200,1900;im=Image.new('RGB',(W,H),'#fcfbf7');dr=ImageDraw.Draw(im)
 font=lambda sz:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',sz)
 xmin,xmax,ymin,ymax=spec['extent'];scale=min((W-330)/(xmax-xmin),(H-330)/(ymax-ymin))
 def p(v):return (140+(v[0]-xmin)*scale,200+((v[1]-ymin) if spec['axis']==1 else (ymax-v[1]))*scale)
 svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="100%" height="100%" fill="#fcfbf7"/>']
 def line(a,b,color='#282a29',width=2):
  A,B=p(a),p(b);dr.line([A,B],fill=color,width=width);svg.append(f'<path d="M{A[0]:.2f},{A[1]:.2f} L{B[0]:.2f},{B[1]:.2f}" stroke="{color}" stroke-width="{width}" fill="none"/>')
 def label(xy,txt,sz=24,color='#222',raw=False):
  q=xy if raw else p(xy);dr.text(q,txt,font=font(sz),fill=color,anchor='mm');svg.append(f'<text x="{q[0]}" y="{q[1]+sz*.3}" font-size="{sz}" text-anchor="middle" fill="{color}" font-family="Segoe UI,sans-serif">{html.escape(txt)}</text>')
 label((W/2,60),spec['title'],40,raw=True)
 label((W/2,112),'CASA DE CAMPO · Geometría del archivo Blender · Medidas en metros',25,'#69736d',True)
 for t in spec['context']:
  qs=[p(x) for x in t];dr.polygon(qs,fill='#edede6');svg.append('<polygon points="'+' '.join(f'{q[0]:.2f},{q[1]:.2f}' for q in qs)+'" fill="#edede6"/>')
 for l in spec['lines']:line(*l['p'],color='#53828b' if l['glass'] else '#252b28',width=2 if l['glass'] else 3)
 def dim(a,b,text,offset=.35):
  line(a,b,'#9b5641',2)
  for v in [a,b]:line([v[0]-.07,v[1]-.07],[v[0]+.07,v[1]+.07],'#9b5641',2)
  label([(a[0]+b[0])/2,(a[1]+b[1])/2-offset],text,24,'#9b5641')
 if spec['key']=='planta_baja':
  dim([0,-.6],[22,-.6],'22,00');dim([22.6,0],[22.6,20],'20,00',0)
  dim([14,12.8],[22,12.8],'8,00');dim([13,18.7],[20,18.7],'7,00')
  for xy,s in [([18,2],'MONOAMBIENTE'),([18,9.3],'QUINCHO'),([16.5,16.5],'PILETA 7 × 3'),([4.8,4.8],'HUERTA'),([7,12],'JARDÍN'),([8,-1.25],'CEDRO MISIONERO')]:label(xy,s,26)
 elif spec['key']=='planta_alta':
  dim([14,-.4],[22,-.4],'8,00');dim([22.5,0],[22.5,12],'12,00',.05)
  for xy,s in [([18,1.35],'ESTUDIO'),([15.65,7.35],'DORMITORIO'),([18.52,6.7],'VESTIDOR'),([20.7,7.7],'BAÑO'),([18,10.3],'COCINA / COMEDOR'),([13.4,10.5],'BALCÓN')]:label(xy,s,23)
 else:
  left=xmin+.08
  for y,txt in [(0,'±0,00'),(3,'+3,00 estructura'),(3.25,'+3,25 piso PA'),(6.45,'+6,45 cielorraso')]:
   line([xmin,y],[xmax,y],'#bcc6bc',1);label([left+1.1,y+.13],txt,20,'#69736d')
  if spec['key']=='corte_estudio':dim([22.35,3.25],[22.35,6.45],'3,20 libre',.02)
  if spec['key']=='corte_escalera':dim([1.2,-.1],[5,-.1],'3,80 / 18 peldaños');dim([5.05,3.4],[6.05,3.4],'Descanso 1,00')
 label((W/2,H-96),'Negro: intersección real del corte · Gris: proyección de equipamiento · Azul: vidrio · Terreno y vegetación omitidos para lectura',20,'#69736d',True)
 label((W/2,H-60),'Ejes fuente: X horizontal del lote, Z profundidad, Y altura. Se muestran puertas abiertas.',20,'#69736d',True)
 svg.append('</svg>');open(os.path.join(OUT,spec['key']+'.svg'),'w',encoding='utf8').write('\n'.join(svg));im.save(os.path.join(OUT,spec['key']+'.png'))
print('DRAWINGS_PUBLISHED',len(data))
