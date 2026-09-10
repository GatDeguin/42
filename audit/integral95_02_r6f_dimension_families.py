import json,re,numpy as np
from pathlib import Path
p=Path(r'D:\2026\42\audit\integral95_dimensions_Casa_de_Campo_95_R6F_route.json');d=json.loads(p.read_text(encoding='utf8'))
objects=[o for o in d['objects'] if o['render_enabled_by_collection']]
rules=[
('Sofá cama mono',r'^Sofá cama mono ',.21,r'cojín \d+$'),
('Mesa mono',r'^(Mesa mono |MOB95 \| faldón mesa mono)',.21,r'tapa'),
('Silla mono 1',r'^Silla mono 1 ',.21,r'asiento'),
('Silla mono 2',r'^Silla mono 2 ',.21,r'asiento'),
('Taburete isla A',r'^Taburete isla mono A$',.21,None),
('Taburete isla B',r'^Taburete isla mono B$',.21,None),
('Mesada cocina mono L',r'^Mesada cocina mono lateral$',.21,None),
('Isla mono',r'^Isla cocina mono (base|tapa|frente|tirador)',.21,r'tapa'),
('Heladera mono',r'^Heladera mono',.21,None),
('Bacha mono',r'^Bacha cocina mono$',.21,None),
('Lavatorio mono',r'^Lavatorio mono$',.21,None),
('Inodoro mono',r'^Inodoro mono',.21,r'asiento'),
('Ducha mono rociador',r'^Ducha baño mono$',.21,None),
('Horno quincho volumen',r'^(Base horno|Cúpula horno|Boca horno)$',.18,None),
('Mesada lavado quincho',r'^Mesada bacha$',.18,None),
('Bachas dobles quincho',r'^Bacha doble [AB]$',.18,None),
('Barra quincho tapa',r'^Mesada apoyo quincho$',.18,None),
('Parrilla volumen',r'^Parrilla (base|campana|rejilla)$',.18,None),
('Mesa quincho',r'^Mesa quincho ',.18,r'tapa tabla'),
('Silla quincho 1',r'^Silla quincho 1 ',.18,r'asiento tabla'),
('Silla quincho 2',r'^Silla quincho 2 ',.18,r'asiento tabla'),
('Silla quincho 3',r'^Silla quincho 3 ',.18,r'asiento tabla'),
('Silla quincho 4',r'^Silla quincho 4 ',.18,r'asiento tabla'),
('Lavatorio quincho',r'^Lavatorio quincho$',.21,None),
('Inodoro quincho',r'^Inodoro quincho',.21,r'asiento'),
('Consola estudio',r'^Consola estudio$',3.25,None),
('Silla estudio',r'^Silla estudio ',3.25,r'asiento'),
('Monitor izquierdo',r'^Monitor izquierdo$',3.25,None),
('Monitor derecho',r'^Monitor derecho$',3.25,None),
('Pantalla DAW',r'^Pantalla estudio$',3.25,None),
('Sofá estudio',r'^Sofá estudio ',3.25,r'cojín \d+$'),
('Rack estudio',r'^(Rack (audio|lateral estudio|estudio)|Subsuelo rack)',3.25,None),
('Vestidor guardado',r'^Vestidor (estante|cajón|lateral|fondo)',3.25,None),
('Cocina PA mesada',r'^Cocina lineal mesada$',3.25,None),
('Heladera PA',r'^Heladera( |$)(?!mono)',3.25,None),
('Horno PA',r'^(Horno (empotrado cocina|cocina)|MOB95 \| chasis horno)',3.25,None),
('Alacena PA',r'^Alacena cocina ',3.25,None),
('Mesa comedor',r'^Mesa comedor ',3.25,r'tapa'),
('Silla comedor norte -0.49',r'^Silla comedor norte -0\.49 ',3.25,r'asiento'),
('Silla comedor norte 0.49',r'^Silla comedor norte 0\.49 ',3.25,r'asiento'),
('Silla comedor sur -0.49',r'^Silla comedor sur -0\.49 ',3.25,r'asiento'),
('Silla comedor sur 0.49',r'^Silla comedor sur 0\.49 ',3.25,r'asiento'),
('Sofá vivienda',r'^Sofá vivienda ',3.25,r'cojín \d+$'),
('Mesa baja vivienda',r'^(Mesa baja vivienda|MOB95 \| apoyo mesa baja)',3.25,None),
('TV',r'^Pantalla TV$',3.25,None),
('Cama conjunto',r'^Cama dormitorio ',3.25,r'colchón$'),
('Mesita luz izquierda',r'^Mesa de luz suite izq$',3.25,None),
('Mesita luz derecha',r'^Mesa de luz suite der$',3.25,None),
('Vanitory PA mesada',r'^Mesada baño suite$',3.25,None),
('Bacha apoyo PA',r'^Bacha apoyo suite$',3.25,None),
('Bañera PA',r'^Bañera vivienda$',3.25,None),
('Inodoro PA',r'^(Inodoro vivienda|Inodoro suite)',3.25,r'asiento'),
('Bidet PA',r'^Bidet vivienda$',3.25,None),
('Banco huerta',r'^Banco huerta$',.05,None)]
out={'source':d['source'],'sha256':d['sha256'],'units':'meters','status':'Dimensional inventory and review input; no blanket approval. Component groups may exclude separately named supports; explicit members retained. Height datums are finished floors documented in model, not terrain zero.','families':[]}
for title,pat,floor,func in rules:
 oo=[o for o in objects if re.search(pat,o['name'])]
 if not oo:out['families'].append({'family':title,'missing_query':pat});continue
 a=np.min([o['world_bounds_source_m']['min'] for o in oo],axis=0);b=np.max([o['world_bounds_source_m']['max'] for o in oo],axis=0)
 row={'family':title,'members':[o['name'] for o in oo],'bbox_source_min':a.tolist(),'bbox_source_max':b.tolist(),'envelope_m':(b-a).tolist(),'datum_floor_m':floor,'lowest_point_above_floor_m':float(a[1]-floor),'highest_point_above_floor_m':float(b[1]-floor),'classification':'G measured / P unbranded assembly; product model not identified'}
 ff=[o for o in oo if func and 'costura' not in o['name'].lower() and re.search(func,o['name'])]
 if ff:row['functional_surface_heights_above_floor_m']={o['name']:o['world_bounds_source_m']['max'][1]-floor for o in ff}
 out['families'].append(row)
out['confirmed_architectural_dimensions']={}
for n in ['Césped del lote','Losa planta baja','Losa entre plantas','Descanso escalera','Cielorraso estudio | cota inferior 6.45m','Cielorraso vivienda | 2.60m sobre piso general','Cielorraso baño | 2.60m sobre porcelanato','Piso estudio','Piso vivienda','Piso baño vivienda','Ventana DVH estudio vidrio','Portón negro']:
 o=next((o for o in objects if o['name']==n),None)
 if o:out['confirmed_architectural_dimensions'][n]=o['world_bounds_source_m']
json.dump(out,open(r'D:\2026\42\audit\integral95_02_r6f_dimension_families.json','w',encoding='utf8'),ensure_ascii=False,indent=2)
for r in out['families']:
 if 'missing_query' in r:print('MISSING',r)
 else:print(r['family'],','.join(f'{q:.3f}' for q in r['envelope_m']),f"high {r['highest_point_above_floor_m']:.3f}",'functional',list({round(x,3) for x in r.get('functional_surface_heights_above_floor_m',{}).values()}))
