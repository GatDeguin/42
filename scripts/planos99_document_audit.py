"""Read-only dimensional/documentary audit from a frozen drawing extraction."""
from pathlib import Path
import argparse,json,hashlib,sys,csv,math
R=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(R/'planos95/_vendor'))
import ezdxf
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args();out=(R/args.out).resolve()
load=lambda n:json.loads((out/n).read_text('utf8'))
g=load('geometry.json');m=load('measurements.json');base=load('manifest.json');det=load('details/manifest.json');ob={o['name']:o for o in g['objects']};closed=g['closed_envelopes'];sha=g['sha256'];checks=[];measure=[]
def check(n,ok,e):checks.append({'check':n,'pass':bool(ok),'evidence':e})
def item(n,value,expected,source,units='m',tol=.00002):
 measure.append({'item':n,'class':'G','value':value,'units':units,'source':source,'expected':expected,'tolerance':tol,'pass':abs(value-expected)<=tol});return value
def top(n):return ob[n]['hi'][2]
def height(n):return ob[n]['hi'][2]-ob[n]['lo'][2]
check('All source SHAs equal',sha==base['model_sha256']==det['model_sha256']==hashlib.sha256(Path(g['model']).read_bytes()).hexdigest(),sha)
for axis,expected in [(0,8),(1,12)]:item('House structural footprint '+str(axis),ob['Losa planta baja']['hi'][axis]-ob['Losa planta baja']['lo'][axis],expected,'Losa planta baja hi-lo')
item('Study finished floor',top('Piso estudio'),3.25,'Piso estudio.maxH')
item('Bath PA finished floor',top('Piso baño vivienda'),3.25,'Piso baño vivienda.maxH')
item('Bath PA ceiling',ob['Cielorraso baño | 2.60m sobre porcelanato']['lo'][2],5.85,'Cielorraso baño.minH')
for n,expected in [('Mesa mono tapa',.75),('Silla mono 1 asiento',.46),('Silla mono 2 asiento',.46),('Isla cocina mono tapa',.90),('Mesada cocina mono lateral',.90)]:item(n+' above NPT',top(n)-.21,expected,n+'.maxH minus .21')
for n,expected in [('Mesa comedor tapa',.75),('Mesa baja vivienda',.40)]:item(n+' above NPT',top(n)-3.25,expected,n+'.maxH minus3.25',tol=.0001)
item('Dining approach to wallZ9.07',ob['Mesa comedor tapa']['lo'][1]-9.07,.805,'Mesa comedor tapa.minZ minus9.07')
item('Mono island to fridge handle',ob['Heladera mono | tirador']['lo'][1]-ob['Isla cocina mono tapa']['hi'][1],1.076,'Handle.minZ minus island.maxZ')
for prefix,floor,w,d in [('mono',.21,.420,.620),('quincho',.21,.420,.620),('suite',3.25,.450,.660)]:
 body=ob['Inodoro vivienda' if prefix=='suite' else 'Inodoro '+prefix];seat=ob['Inodoro '+prefix+' | asiento'];item('WC '+prefix+' body width',body['hi'][0]-body['lo'][0],w,body['name']+' hiX-loX');item('WC '+prefix+' body depth',body['hi'][1]-body['lo'][1],d,body['name']+' hiZ-loZ');item('WC '+prefix+' body height',body['hi'][2]-body['lo'][2],.430,body['name']+' hiH-loH');item('WC '+prefix+' seat height',seat['hi'][2]-floor,.455,seat['name']+' hiH-NPT');item('WC '+prefix+' seat width',seat['hi'][0]-seat['lo'][0],.380,seat['name']+' hiX-loX');item('WC '+prefix+' seat depth',seat['hi'][1]-seat['lo'][1],.445,seat['name']+' hiZ-loZ')
for n,w in [('Baño mono puerta | hoja',.915),('Puerta dormitorio comedor | hoja',.908),('Puerta dormitorio',.820)]:
 o=closed[n];item(n+' closed leaf width',max(o['hi'][i]-o['lo'][i] for i in [0,1]),w,n+' evaluated frame1 max plan span')
item('P05 conservative projected clearance',ob['Puerta dormitorio comedor | manija palanca.001']['lo'][0]-ob['Puerta dormitorio comedor | galce cierre']['hi'][0],.806,'Frame150: inward handle.minX minus closing rebate.maxX; full open leaf depth projected')
item('P05 opening throat at wall',ob['Puerta dormitorio comedor | hoja']['lo'][0]-ob['Puerta dormitorio comedor | galce cierre']['hi'][0],.848,'Frame150: open leaf.minX minus closing rebate.maxX at wall throat')
for h,e in [('lo',-1.390),('hi',-.030)]:item('Pool water '+h,ob['Agua de pileta'][h][2],e,'Agua de pileta.'+h+'H')
item('Wet shelf depth of water',ob['Agua de pileta']['hi'][2]+.080,.050,'water.maxH minus shelf H-.080')
head=[o for n,o in ob.items() if n.startswith('Ducha baño mono')];item('Shower lowest nozzle above floor',min(o['lo'][2] for o in head)-.21,2.0999,'Ducha baño mono* minH minus .21',tol=.00003)
vparts=[o for n,o in ob.items() if n.startswith('VENT99 |')];item('Minimum new ventilation height',min(o['lo'][2] for o in vparts),6.453,'All VENT99 minH')
wet=g['scene_metadata']['r7_wet_details'];check('Full-depth wet joints',wet['PB_grout_width_mm']==2 and wet['PB_grout_depth_mm']==8 and wet['PB_tile_mesh_version']==2,{'width_mm':wet['PB_grout_width_mm'],'depth_mm':wet['PB_grout_depth_mm'],'tile_components':wet['PB_tile_components']})
check('Former suite entry absent',not any('Puerta acceso vestidor' in n for n in ob),[n for n in ob if 'Puerta acceso vestidor' in n]);check('Orphan WC kitchen plinth absent','Zócalo columna cocina' not in ob,'source id853 removed')
check('Door hand metadata incorporated',bool(g['scene_metadata'].get('door_hands99_v1')),'door_hands99_v1')
if g.get('scene_metadata',{}).get('r8_uso_details'):
 for prefix,expected in [('MAT95 | tecla natural',.750),('MAT95 | tecla sostenido',.7625)]:
  n=next(n for n in ob if n.startswith(prefix));item(prefix+' above study NPT',top(n)-top('Piso estudio'),expected,n+'.maxH minus study.maxH')
 item('MIDI tray underside above NPT',ob['USO99 | MIDI bandeja18']['lo'][2]-top('Piso estudio'),.665,'tray.minH minus study.maxH')
 item('MIDI body depth',ob['Controlador estudio']['hi'][0]-ob['Controlador estudio']['lo'][0],.400,'Controlador estudio hiX-loX')
 item('Island knee depth',ob['Isla cocina mono base | fondo']['lo'][1]-ob['Isla cocina mono tapa']['lo'][1],.400,'base.fondo.minZ minus top.minZ')
 for p in ['Taburete isla mono A |','Taburete isla mono B |']:
  item(p+' front leg clearance',ob[p+' pata der frente']['lo'][0]-ob[p+' pata izq frente']['hi'][0],.305,'inner faces of front legs')
 check('R8 use sheets present',all(any(s['id']==n for s in det['sheets']) for n in ['D13','D14']),'D13 and D14')
 evidence=json.loads((out/'use_evidence/use_validation.json').read_text('utf8'));check('R8 use evidence same source',evidence['sha256']==sha and evidence['status']=='PASS',evidence['sha256'])
all_dims=[]
for d in m['dimensions']:all_dims.append(dict(sheet=d['sheet'],view=d['view'],axis=d['axis'],from_m=d['from'],to_m=d['to'],value_m=d['value_m'],label=d['label'],kind='base'))
for d in det['dimensions']:all_dims.append(dict(sheet=d['sheet'],view=d['view'],axis=d['axis'],from_m=d['from_mm']/1000,to_m=d['to_mm']/1000,value_m=d['value_mm']/1000,label=d.get('label') or '',kind='detail',classification=d.get('class')))
check('Every dimension arithmetic',all(abs(abs(d['to_m']-d['from_m'])-abs(d['value_m']))<1e-6 for d in all_dims),len(all_dims))
cad_fail=[];cad_count=0
for sheet in base['sheets']+det['sheets']:
 ds=[d for d in all_dims if d['sheet']==sheet['id']];folder=out/('details' if sheet['id'].startswith('D') else '');doc=ezdxf.readfile(folder/sheet['dxf']);dd=list(doc.modelspace().query('DIMENSION'));cad_count+=len(dd)
 if len(dd)!=len(ds):cad_fail.append([sheet['id'],'count',len(dd),len(ds)])
 for i,(a,b) in enumerate(zip(dd,ds)):
  val=abs(float(a.get_measurement()))
  if abs(val-abs(b['value_m']))>1e-6:cad_fail.append([sheet['id'],i,val,b['value_m']])
check('Every native CAD dimension agrees with register',not cad_fail,{'count':cad_count,'failures':cad_fail})
check('All physical view scales positive',all(d['scale']>0 and d['width_mm']>0 and d['height_mm']>0 for d in m['scales']),len(m['scales']))
check('Measured critical dimensions match displayed intent',all(d['pass'] for d in measure),{'count':len(measure),'failures':[d for d in measure if not d['pass']]})
r={'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','model':g['model'],'model_sha256':sha,'coordinate_axes':['X','Z depth','H height'],'checks':checks,'measured_items':measure,'all_dimension_count':len(all_dims),'carpentry_schedule':m.get('carpentry_schedule',[]),'north':{'page_direction':'down-left with Cedro Misionero at top','source_vector':[-1,0,1],'authority':'Owner reference; no measured azimuth'},'limits':['Every CAD dimension and register arithmetic checked; selected critical dimensions independently recomputed from evaluated mesh bounds.','This does not prove every annotation by physical survey or validate normative ergonomics, load capacity, hydraulics, acoustics or products.','P maintenance platform is a separate spatial proposal, not a modeled or selected certified product.']}
(out/'dimensional_audit.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),'utf8')
with (out/'dimension_register.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=['sheet','view','axis','from_m','to_m','value_m','label','kind','classification']);writer.writeheader();writer.writerows(all_dims)
lines=['# Auditoría dimensional documental '+('R8' if g.get('scene_metadata',{}).get('r8_uso_details') else 'R7'), '', 'Modelo: '+Path(g['model']).name, 'SHA256: '+sha,'','Estado: '+r['status']+'. '+str(len(all_dims))+' cotas nativas y '+str(len(measure))+' dimensiones críticas recalculadas.','','| Medida G | Valor | Fuente geométrica |','|---|---:|---|']
for d in measure:lines.append('| '+d['item']+' | '+format(d['value'],'.6f')+' '+d['units']+' | '+d['source']+' |')
lines+=['','El registro CSV incluye todas las cotas, sus extremos y unidades. El JSON enlaza el cuadro de carpinterías con envolventes cerradas del frame1.','Norte orientativo -X/+Z del propietario; no es rumbo topográfico.','Se verifica documentación digital y geometría nombrada; no mensura, cálculo ni certificación de productos.']
(out/'AUDITORIA_DIMENSIONAL.md').write_text('\n'.join(lines)+'\n','utf8');print(json.dumps({'status':r['status'],'checks':len(checks),'dimensions':len(all_dims),'measured':len(measure),'failed':[c for c in checks if not c['pass']]},indent=2))
if r['status']!='PASS':sys.exit(1)
