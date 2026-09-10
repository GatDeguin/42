"""Read-only R4A spatial proposal for bathroom access and kitchen, source X/Y/Z metres."""
from pathlib import Path
import json,math,html,sys
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'planos95/layout_r4';OUT.mkdir(exist_ok=True)
data=json.loads((OUT/'geometry.json').read_text(encoding='utf8'));ob={o['name']:o for o in data['objects']}
# Plan coordinates X,Z; heights always identified as sourceY. Preserve all corrected R4A heights.
def bbox(n):
 o=ob[n];return [o['lo'][0],o['lo'][1],o['hi'][0],o['hi'][1]]
def transform(x,z):return 17.75-(z-10.48),10.7+(x-18.15)
def rb(b):
 a=[transform(x,z) for x,z in [(b[0],b[1]),(b[2],b[1]),(b[2],b[3]),(b[0],b[3])]];return [min(p[0] for p in a),min(p[1] for p in a),max(p[0] for p in a),max(p[1] for p in a)]
dining=[n for n in ob if n.startswith(('Mesa comedor ','Silla comedor '))]
bath_prefix=['Vanitory vivienda','Espejo baño','Vanitory bajo suite','Mesada baño suite','Grifería baño suite','Espejo baño suite','Revestimiento ducha suite','Mampara ducha suite','Toallero baño suite','Rejilla ducha suite','Bacha apoyo suite','Bañera vivienda','Inodoro vivienda','Bidet vivienda','Ducha |','Bañera |','Inodoro suite |','Ducha baño vivienda','Barra toalla baño vivienda']
bath=[n for n in ob if any(n.startswith(p) for p in bath_prefix) and ob[n]['lo'][2]>3.1]
remove=[n for n in ob if n.startswith(('Península cocina ','Despiece península cocina','Banco cocina refinado '))]
proposal={'status':'P / PROPUESTA DIMENSIONAL PARA INCORPORACION','source_model':data['model'],'source_sha256':data['sha256'],'coordinate_convention':'source X horizontal, Y height, Z depth. All metres; plan boxes [xmin,zmin,xmax,zmax]. Blender=(X,-Z,Y).','door':{'type':'corredera exterior sobre cara comedor; desplazamiento al este (+X)','wall_to_cut':'Baño tabique posterior','rough_opening_source_box':{'x':[19.55,20.52],'y':[3.205,5.51],'z':[8.57,8.71]},'finished_jamb_inner_x':[19.585,20.485],'clear_width_m':.90,'clear_head_y':5.47,'floor_y':3.25,'leaf_closed_source_box':{'x':[19.51,20.56],'y':[3.26,5.50],'z':[8.745,8.785]},'translation_when_open_source':[1.02,0,0],'leaf_open_x':[20.53,21.58],'track_source_box':{'x':[19.48,21.63],'y':[5.54,5.62],'z':[8.72,8.82]},'handle':'Tirador embutido: centro X19.56 cerrado/X20.58 abierto, Y4.30; accesible al oeste del retorno X20.74. Sin manija saliente.','hardware_requirements':'Dos carros, topes y antidescarrilamiento; guia inferior lateral fuera del paso; tapa de riel desmontable. Herrajes y anclaje por peso/fabricante.','alternatives_rejected':[{'type':'abatible interior, bisagra oeste','reason':'Hoja abierta intercepta parcialmente acceso existente desde vestidor.'},{'type':'abatible interior, bisagra este','reason':'Barrido invade huella del bidet o exige comprimir separacion de sanitarios.'},{'type':'abatible exterior','reason':'Despeja sanitarios pero ocupa corredor entre comedor y cocina.'}]},'bath_floor':{'structural_slab':'Losa entre plantas','structural_top_y':3.20,'existing_floor':'Piso baño vivienda','existing_y':[3.24,3.30],'new_y':[3.20,3.25],'new_main_plan_box':[19.49,6.10,21.80,8.57],'door_extension_plan_box':[19.55,8.57,20.52,8.71],'subtract_from':'Piso vivienda','reason':'No trasladar el piso60mm hacia abajo50mm: pisaria losa10mm. Reconstruir acabado50mm y descontar su huella del acabado general para evitar duplicacion.','layers_P_mm':[{'layer':'base/mortero','thickness':30},{'layer':'impermeabilizacion continua','thickness':2},{'layer':'adhesivo','thickness':8},{'layer':'baldosa','thickness':10}],'waterproof_transition':'P membrana bajo ambas terminaciones con banda flexible y retorno a jambas; extender150mm lado seco, junta elastica5mm en linea de puerta. Piso continuo+3.25; el desague de bañera sigue dentro de su vaso, no se inventa pendiente general ni cañeria.','ceiling_move':{'name':'Cielorraso baño | 2.60m sobre porcelanato','source_delta':[0,-.05,0],'new_underside_y':5.85,'clear_height':2.60}},'bath_objects_moves':[{'name':n,'source_delta':[.40 if n.startswith(('Bidet vivienda','Inodoro vivienda','Inodoro suite |')) else 0,-.05,0]} for n in bath],'bath_coordination':['Trasladar geometria sanitaria y sus conexiones visibles; replantear desagues antes de ejecutar.','Mantener nicho y cerco mural en cota actual; quedan50mm mas altos respecto a piso nuevo. No mover piezas fuera del vaciado existente.','No trasladar tabiques, jambas ni puerta existente; verificar guia inferior contra nuevo piso.'],'kitchen':{'linear_to_keep':[n for n in ob if n.startswith(('Cocina lineal','Frente cocina vivienda','Bacha cocina','Grifería cocina','Anafe cocina','Inductor cocina','Horno empotrado cocina','Horno cocina vidrio','Heladera','Campana cocina'))],'remove_and_rebuild':remove,'new_return_top_source_box':{'x':[20.74,21.79],'y':[4.1025,4.1575],'z':[8.86,9.48]},'new_return_base_plan_box':[20.765,8.885,21.135,9.455],'return_rule':'Unir la mesada de retorno con mesada lineal existente; evitar tapas coplanares duplicadas. Cierre posterior desmontable, no cargar ni fijar al riel de la puerta. Sin bancos en el paso nuevo.','leaf_to_counter_back_clearance':.075,'handle_to_counter_side_clearance':.16,'upper_storage_change':'Iniciar volumen de alacena y primer modulo en Z9.18; reordenar modulos hastaZ10.67. Dejar acceso visual/manual al extremo del riel; no taparlo con alacena.','lighting_change':'Reubicar Lampara lineal cocina y carcasa sobre nuevo retorno, centroX21.18/Z9.17. Corregir/eliminar colgantes heredados fuera de mesada; alturas R4A se conservan.'},'dining':{'apply_to_model':'R4A or newer preserving its heights','objects':dining,'pivot_source':[18.15,0,10.48],'target_pivot_source':[17.75,0,10.70],'plan_transform':'Xnew=17.75-(Zold-10.48); Znew=10.70+(Xold-18.15); Ynew=Yold','blender_vertical_rotation_deg':-90,'table_new_plan_box':rb(bbox('Mesa comedor tapa')),'table_top_y_preserved':4.0,'chair_seat_top_y_preserved':3.72,'chair_withdrawal_m':.35,'decor_and_lighting':'Florero comedor y Lampara comedor centrados en X17.75/Z10.70; no mantener duplicados curados fuera de la mesa.'},'use_zones_P':{'bath_walk_080':[[19.605,8.90],[20.405,8.90],[20.405,7.20],[19.49,7.20],[19.49,8.00],[19.605,8.00]],'oven_open_plan_box':[20.567,10.06,21.067,10.58],'oven_operator_060_plan_box':[19.967,10.06,20.567,10.58],'fridge_open_sweep_box':[20.417,10.885,21.111,11.595],'fridge_operator_060_plan_box':[19.817,10.885,20.417,11.595],'counter_operator_090_plan_box':[20.17,9.48,21.07,10.01]},'measured_clearance_review':{'bath_route_min_m':.80,'bath_side_to_shifted_bidet_m':.855,'vestidor_face_to_rotated_table_m':.795,'table_end_to_rear_frame_m':.385,'table_end_note':'Sin sillas en cabeceras; acceso al balcon por lateral este, no por esa franja posterior.','withdrawn_east_chair_to_oven_operator_m':.974,'withdrawn_east_chair_to_fridge_operator_m':.824,'withdrawn_west_chair_to_reoriented_coffee_m':.807,'limitation':'Huellas dimensionales propuestas:0.824m junto a heladera en uso y0.807m al oeste con mesa baja ajustada. Verificar apertura real de equipos y herrajes en nueva malla; no implica conformidad normativa.'},'not_certified':['No structural sizing for lintel/rail fixings','No jurisdictional accessibility/code approval','No sanitary network or waterproof-product calculation','No completed 3D modification by this script']}
proposal['living_coffee']={'name':'Mesa baja vivienda','pivot_source':[15.60,0,10.47],'target_pivot_source':[15.44,0,10.62],'blender_vertical_rotation_deg':-90,'plan_box':[15.18,10.23,15.70,11.01],'preserve_y':False,'top_y':3.65,'new_supports':'Añadir apoyos hasta piso+3.25; altura mesa baja400mm sobre terminado.','clearances_m':{'sofa_front':.37,'TV_front':.495,'withdrawn_west_chair':.807},'purpose':'Acompaña desplazamiento comedor150mm oeste sin estrechar acceso a sillas occidentales.'}
(OUT/'propuesta_bano_cocina.json').write_text(json.dumps(proposal,indent=2,ensure_ascii=False),encoding='utf8')
# Physical A2 schematic at1:25, with source figures only. Green is a proposed use footprint.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" viewBox="0 0 594 420"><rect width="594" height="420" fill="white"/>'];G='#5c686f';P='#1b6d9a';U='#28866c';R='#b16447'
def txt(x,y,t,size=2.6,c=G):svg.append(f'<text x="{x}" y="{y}" fill="{c}" font-family="Arial" font-size="{size}">{html.escape(t)}</text>')
def pt(x,z):return (30+(x-14)*40,75+(z-6)*40)
def poly(ps,c=G,fill='none',dash=False,width=.25):svg.append('<polygon points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in ps)+f'" stroke="{c}" stroke-width="{width}" fill="{fill}"'+(' stroke-dasharray="1.5,1"' if dash else '')+'/>')
def rect(b,c=G,fill='none',dash=False):poly([pt(b[0],b[1]),pt(b[2],b[1]),pt(b[2],b[3]),pt(b[0],b[3])],c,fill,dash)
def lin(p,q,c=G,w=.2,dash=False):svg.append(f'<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" stroke="{c}" stroke-width="{w}"'+(' stroke-dasharray="1.5,1"' if dash else '')+'/>')
def label(x,z,t,c=G,sz=2.5):xx,yy=pt(x,z);txt(xx,yy,t,sz,c)
def dx(a,b,z,t,c=P):
 p,q=pt(a,z),pt(b,z);lin(p,q,c,.15)
 for x,y in [p,q]:lin((x-1,y+1),(x+1,y-1),c,.2)
 txt((p[0]+q[0])/2-6,p[1]-1.6,t,2.5,c)
def dy(a,b,x,t,c=P):
 p,q=pt(x,a),pt(x,b);lin(p,q,c,.15)
 for x,y in [p,q]:lin((x-1,y+1),(x+1,y-1),c,.2)
 txt(p[0]+2,(p[1]+q[1])/2,t,2.5,c)
poly([(10,10),(584,10),(584,410),(10,410)],G);txt(20,25,'CASA DE CAMPO / PROPUESTA BAÑO-COMEDOR Y COCINA PA',5,P);txt(20,35,'Base R4A | '+data['sha256'][:24]+' | Coordenadas X/Z en metros; alturas sourceY',2.7);txt(20,47,'G gris: medido   P azul: propuesta   Verde: huellas de uso   Naranja: sustituido',2.7)
# bounding finished faces and fixed partitions
rect([14.2,6.1,21.8,11.8],G)
for n in ['Baño tabique posterior','Vestidor tabique baño paño A','Vestidor tabique baño paño B','Vestidor cierre al estar paño A','Vestidor cierre al estar paño B','Dormitorio tabique transversal']:
 if n in ob:rect(bbox(n),G,'#e9eded')
# wipe door cut and show frames
rect([19.55,8.565,20.52,8.715],'white','white');rect([19.55,8.56,19.585,8.72],P,'#e3f2fb');rect([20.485,8.56,20.52,8.72],P,'#e3f2fb')
# Floor is level; no hidden step left.
rect([19.49,6.1,21.8,8.57],P,'none');label(19.6,6.30,'BAÑO +3.25 P',P)
for n in ['Vanitory vivienda','Bañera vivienda','Sofá vivienda base','Mueble TV','Cocina lineal mesada','Heladera']:
 if n in ob:rect(bbox(n),G,'#f0f2f2')
for n in ['Bidet vivienda','Inodoro vivienda']:
 b=bbox(n);rect(b,R,'none',True);rect([b[0]+.4,b[1],b[2]+.4,b[3]],P,'#e3f2fb')
rect(bbox('Mesa baja vivienda'),R,'none',True);rect([15.18,10.23,15.70,11.01],P,'#e3f2fb')
# bathroom 800mm route between new and existing door
poly([pt(x,z) for x,z in proposal['use_zones_P']['bath_walk_080']],U,'none',True,.25)
rect([19.51,8.745,20.56,8.785],P,'none',True);rect([20.53,8.745,21.58,8.785],P,'#e3f2fb');label(19.53,9.19,'P CORREDERA →',P)
rect([20.74,8.86,21.79,9.48],P,'#e3f2fb');label(20.85,9.12,'RETORNO',P,2.3)
# dining geometry and chair footprints after R4A-height-preserving plan rotation
rect(rb(bbox('Mesa comedor tapa')),P,'#e3f2fb')
for n in [n for n in dining if n.endswith(' asiento')]:
 b=rb(bbox(n));rect(b,P,'#e3f2fb');shift=.35 if (b[0]+b[2])/2>17.75 else -.35;rect([b[0]+shift,b[1],b[2]+shift,b[3]],U,'none',True)
label(17.57,10.7,'MESA',P);label(17.44,10.9,'4 plazas',P)
for k,b in proposal['use_zones_P'].items():
 if k.endswith('plan_box') or k.endswith('sweep_box'):rect(b,U,'none',True)
dx(19.585,20.485,8.37,'0.90 libre');dx(19.605,20.405,7.60,'0.80',U);dy(9.07,9.865,18.40,'0.795');dx(18.993,19.967,10.18,'0.974',U);dx(18.993,19.817,11.39,'0.824',U);dx(15.70,16.507,10.85,'0.807',U)
label(20.57,10.35,'HORNO',G,2.3);label(21.12,11.11,'HELADERA',G,2.3);label(14.6,11.6,'ESTAR / contexto R4A',G)
# Right-hand explanatory column, readable at printed size.
y=70
notes=[('PUERTA Y RECORRIDO','Corredera exterior a derecha; vano0.97, libre entre jambas0.90. Hoja1.05, carrera1.02. Tirador embutido accesible junto a retorno; sin arco en comedor.'),('SANITARIOS','Bidet e inodoro completos +0.40 en X y -0.05 en altura. Paso dibujado0.80 entre nueva puerta y puerta del vestidor. No se suprime ningun aparato.'),('PISO CONTINUO','Losa real+3.20. Reconstruir acabado50mm hasta+3.25; no bajar bloque60mm dentro de losa. Restar misma huella al piso general. Cielorraso baja a+5.85:2.60 libres.'),('IMPERMEABILIZACION P','30 mortero +2 membrana +8 adhesivo +10 baldosa =50mm. Membrana y banda flexible cruzan puerta, prolongacion150 al seco y junta elastica5; sin resalto.'),('MESADA Y SERVICIO','Retorno X20.74..21.79/Z8.86..9.48; hoja pasa por detras con75mm libres. Mantener160mm entre tirador abierto y extremo de mesada. Retirar bancos anteriores.'),('COMEDOR Y USO','Mesa gira90° a X17.75/Z10.70; conservar alturas R4A: mesa750 y asientos470 sobre piso. Cuatro sillas en laterales; retirada350mm dibujada.'),('PASOS CON USO PROPUESTO','Mesa baja gira90° aX15.44/Z10.62:0.807m a silla oeste retirada. Ante heladera abierta+usuario600 quedan0.824m; ante horno0.974m. Validar con aperturas y cuerpos finales; no se atribuye conformidad normativa.')]
import textwrap
for title,body in notes:
 txt(380,y,title,3.2,P);y+=6
 for row in textwrap.wrap(body,94):txt(380,y,row,2.7,R if title=='LIMITACION VISIBLE' else G);y+=4.4
 y+=5
# cross-reference and quantitative dimensions
text1='Fuente geometrica R4A. Cambios de planta propuestos; aplicar sobre R4A o posterior conservando las alturas corregidas.'
for i,row in enumerate(textwrap.wrap(text1,175)):txt(25,345+i*5,row,2.8)
txt(25,365,'JSON: propuesta_bano_cocina.json contiene objetos, deltas, cajas fuente, capas y alternativas de puerta.',2.8)
lin((10,383),(584,383),G,.3);txt(20,394,'EN REVISION / P - SIN MODIFICAR MODELO NI CERTIFICAR NORMATIVA',3,R);txt(20,403,'A2 | escala del plano 1:25 | imprimir100% | areas de usuario propuestas para contrastar, no datos antropometricos certificados',2.5)
svg.append('</svg>');(OUT/'propuesta_bano_cocina.svg').write_text('\n'.join(svg),encoding='utf8')
print(json.dumps({'json':str(OUT/'propuesta_bano_cocina.json'),'svg':str(OUT/'propuesta_bano_cocina.svg'),'model_sha':data['sha256'],'bath_moves':len(bath),'dining_objects':len(dining),'remove_rebuild':len(remove)},indent=2))
