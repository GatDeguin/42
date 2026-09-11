"""Create review contacts and image-integrity evidence from completed source-identified stills.
Reads PNGs only; never modifies source images or the Blender model.
"""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import hashlib,json,argparse,math
ap=argparse.ArgumentParser();ap.add_argument('--directory',required=True);args=ap.parse_args()
base=Path(args.directory).resolve();data=json.loads((base/'manifest.json').read_text('utf8'))
out=base/'contacts';out.mkdir(exist_ok=True)
font_path=Path('C:/Windows/Fonts/arial.ttf')
font=ImageFont.truetype(str(font_path),23) if font_path.exists() else ImageFont.load_default()
small=ImageFont.truetype(str(font_path),18) if font_path.exists() else ImageFont.load_default()
rows={r['key']:r for r in data['images']}
groups=[
 ('exteriores',['exterior','pileta','huerta','quincho','cubiertas','escalera'],3),
 ('vivienda',['cocina','dormitorio','dormitorio_acceso','vestidor','bano','puerta_bano'],3),
 ('servicios',['bano_acceso','mono_cocina','mono_distribucion','bano_mono','bano_mono_sanitarios','bano_quincho'],3),
 ('complementarias',['estudio','bano_humano','dormitorio_puerta'],3),
 ('retratos',['estudio_retrato','dormitorio_retrato','vestidor_retrato','exterior_retrato'],4),
]
report={'source':data['source'],'sourceSHA256':data['sourceSHA256'],'images':[],'contacts':[],'status':'Technical integrity and contact generation only; visual critique is separate.'}
for row in data['images']:
 p=base/row['file'];raw=p.read_bytes();digest=hashlib.sha256(raw).hexdigest();assert digest==row['sha256'],row['file']
 im=Image.open(p);im.load();assert list(im.size)==row['pixels'];assert im.format=='PNG'
 report['images'].append({'key':row['key'],'file':str(p),'size':list(im.size),'sha256':digest,'mode':im.mode})
for name,keys,columns in groups:
 assert all(k in rows for k in keys),(name,[k for k in keys if k not in rows])
 portrait=name=='retratos';cell_w=450 if portrait else 600;cell_h=600 if portrait else 450
 label_h=70;margin=18;count=math.ceil(len(keys)/columns)
 sheet=Image.new('RGB',(columns*cell_w+(columns+1)*margin,count*(cell_h+label_h)+(count+1)*margin+54),(24,28,29))
 draw=ImageDraw.Draw(sheet);draw.text((margin,14),name.upper()+' | R7 | fuente '+data['sourceSHA256'][:12],font=font,fill=(230,230,223))
 for index,key in enumerate(keys):
  row=rows[key];im=Image.open(base/row['file']).convert('RGB');im=ImageOps.contain(im,(cell_w,cell_h),Image.Resampling.LANCZOS)
  col=index%columns;rr=index//columns;x=margin+col*(cell_w+margin);y=54+margin+rr*(cell_h+label_h+margin)
  sheet.paste(im,(x+(cell_w-im.width)//2,y+(cell_h-im.height)//2))
  draw.text((x,y+cell_h+9),row['title'],font=small,fill=(238,238,232))
  draw.text((x,y+cell_h+34),key+' | '+str(row['pixels'][0])+'x'+str(row['pixels'][1])+' | frame '+str(row['frame']),font=small,fill=(170,185,185))
 path=out/(name+'.jpg');sheet.save(path,quality=93,subsampling=0)
 report['contacts'].append({'file':str(path),'keys':keys,'size':list(sheet.size),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(out/'integrity.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf8')
print(json.dumps({'verifiedImages':len(report['images']),'contactSheets':len(report['contacts']),'sourceSHA256':report['sourceSHA256']},indent=2))
