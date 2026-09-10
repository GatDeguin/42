import bpy,sys,ast,json,hashlib,bmesh
from pathlib import Path
from mathutils import Vector,Matrix
root=Path(__file__).resolve().parent.parent;S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();COL=bpy.data.collections['95 | Baños PB R6D'];M={m.get('source_material_key'):m for m in bpy.data.materials if m.get('source_material_key')}
for m in bpy.data.materials:
 if m.name.startswith(('MAT95 | ','SL95 | ')):M[m.name.split(' | ',1)[1]]=m
for path in ['correcciones95_corredizas_r5.py','correcciones95_banos_r6.py']:
 for nd in ast.parse((root/'scripts'/path).read_text(encoding='utf8')).body:
  if isinstance(nd,ast.FunctionDef):exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
operations=[];changes=[];cx,cz=21.35,5.075
# Grille bearing ring and bonded membrane collar: no floating gap or open annulus.
for a,b in [([cx-.05,cx-.04],[cz-.05,cz+.05]),([cx+.04,cx+.05],[cz-.05,cz+.05]),([cx-.04,cx+.04],[cz-.05,cz-.04]),([cx-.04,cx+.04],[cz+.04,cz+.05])]:bb('ducha aro apoyo rejilla',a,[.188,.1915],b,'stainless')
reg={'x':[cx-.06,cx+.06],'y':[.1725,.1785],'z':[cz-.06,cz+.06]}
reserve([o.name for o in S.objects if o.name.startswith(('BTH95 | ducha mortero','BTH95 | ducha membrana2','BTH95 | ducha adhesivo8'))],reg,'alojamiento collar desagüe')
for name,hh,rad,key in [('brida desagüe',[.1725,.1745],.045,'stainless'),('collar sellado desagüe',[.1745,.1785],.045,'rubber95')]:
 o=bb('ducha '+name,[cx-.06,cx+.06],hh,[cz-.06,cz+.06],key);c=cylinder('TMP collar bore',[cx,.17,cz],[cx,.18,cz],rad);boolean(o,c);bpy.data.objects.remove(c,do_unlink=True)

S['bath_grille_support']='P continuous bearing ring under grate and bonded collar linking shower membrane to trap body.'
p=root/'output/Casa_de_Campo_95_R6D.blend';bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(p),compress=True)
rp=root/'review95/banos_r6d_details.json';d=json.loads(rp.read_text(encoding='utf8'));d['model']=str(p);d['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();d['reservations']+=operations;d['grate_bearing_and_membrane_collar']=True;rp.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf8');print('R6D_FINAL',d['sha256'],flush=True)
