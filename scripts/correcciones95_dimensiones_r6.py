"""R6H dimensional corrections: tread bearing/nosing and studio knee clearance.
Run on loaded coordinated model. No video. Unbranded connection geometry requires structural design.
"""
import bpy,os,json,math,ast,numpy as np,sys
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
for m in bpy.data.materials:
 if m.name.startswith(('MAT95 | ','FIT95 | ')):M[m.name.split(' | ',1)[1]]=m
def cv(p):return Vector((p[0],-p[2],p[1]))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_textiles.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['bounds','deform','map_h']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_materialidad.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['box','cyl','mesh','curve']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<fast>','exec'))
def bb(name,x,h,z,mat='blackMetal',col='STAIR',bev=.0005):
 return box(name,[(x[0]+x[1])/2,(h[0]+h[1])/2,(z[0]+z[1])/2],[x[1]-x[0],h[1]-h[0],z[1]-z[0]],mat,col,bev)
def cut(o,c):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;m=o.modifiers.new('Reserva R6H','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=c;bpy.ops.object.modifier_apply(modifier=m.name)
def remove(n):
 o=bpy.data.objects.get(n)
 if o:bpy.data.objects.remove(o,do_unlink=True)
def stringer_centre(z):return .06+(z-1.20)*3.19/3.80-.10
report={'stairs':[],'console':{}}
for i in range(1,19):
 tread=bpy.data.objects['Peldaño exterior '+str(i)];a,b=bounds(tread);zb,zt=float(-b[1]),float(-a[1]);zc=(zb+zt)/2;bottom=float(a[2]);top=float(b[2])
 remove('Soporte peldaño '+str(i))
 # Hollow transverse 35x35x3 tube terminates on side plates, clear of stringer solids.
 tube=bb('Soporte peldaño '+str(i),[13.0685,13.8915],[bottom-.035,bottom],[zc-.0175,zc+.0175])
 c=bb('TEMP interior travesaño',[13.06,13.90],[bottom-.032,bottom-.003],[zc-.0145,zc+.0145],col='REFERENCE',bev=0);cut(tube,c);remove(c.name)
 # Side plates touch exact inner faces of existing85mm stringers.
 for label,xa,xb,face in [('exterior',13.0625,13.0685,13.0625),('interior',13.8915,13.8975,13.8975)]:
  zz=[zc-.035,zc+.035];low=[stringer_centre(z)-.045 for z in zz]
  # Six-mm web plate has a bottom parallel to the stringer and a horizontal bearing top.
  vs=[cv([x,h,z]) for x in [xa,xb] for z,h in [(zz[0],low[0]),(zz[1],low[1]),(zz[1],bottom),(zz[0],bottom)]]
  plate=mesh('DIM95 | cartela peldaño '+str(i)+' '+label,vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],'blackMetal','STAIR')
  # Weld seam is confined to the stringer web overlap; represents an unsized weld proposal.
  curve('DIM95 | soldadura cartela '+str(i)+' '+label,[[face,stringer_centre(zz[0])-.04,zz[0]],[face,stringer_centre(zz[1])-.04,zz[1]]],.002,'blackMetal','STAIR')
 for x in [13.19,13.77]:
  c=cyl('TEMP paso fijación peldaño',[x,bottom-.05,zc],[x,bottom+.002,zc],.0035,'blackMetal','REFERENCE');cut(tube,c);remove(c.name)
  cyl('DIM95 | tornillo apoyo peldaño',[x,bottom-.040,zc],[x,bottom+.030,zc],.003,'stainless','STAIR')
  cyl('DIM95 | cabeza tornillo apoyo peldaño',[x,bottom-.044,zc],[x,bottom-.035,zc],.0055,'stainless','STAIR')
 # Recess each6mm grip strip4mm into tread;2mm projection. No hidden strip or trip lip.
 nose=bpy.data.objects['Nariz antideslizante peldaño '+str(i)];na,nb=bounds(nose);map_h(nose,top-.004,top+.002)
 c=bb('TEMP rebaje nariz',[float(na[0])-.0002,float(nb[0])+.0002],[top-.0042,top+.004],[float(-nb[1])-.0002,float(-na[1])+.0002],col='REFERENCE',bev=.0002);cut(tread,c);remove(c.name)
 report['stairs'].append({'step':i,'wood_bottom':bottom,'top':top,'support_top':bottom,'nose_projection_m':.002,'plate_thickness_m':.006,'tube_mm':[35,35,3]})
# Lift only work surface and attached console controls by56mm; independent screen/speaker stands stay fixed.
delta=.056;raised=[]
for o in S.objects:
 if o.name.startswith(('Consola estudio','Medidor consola','Controlador estudio')) or (o.name.startswith('MAT95 | ') and any(c.name=='STUDIO' for c in o.users_collection)):
  o.location.z+=delta;raised.append(o.name)
base=bpy.data.objects['Base consola estudio'];a,b=bounds(base);map_h(base,3.25,float(b[2])+delta)
for o in [v for v in S.objects if v.name.startswith('MOB95 | apoyo consola')]:
 a,b=bounds(o);map_h(o,3.25,float(b[2])+delta)
# Real knee/foot opening:900mm wide,600mm deep under front,700mm high from floor.
for ob in [bpy.data.objects['Consola estudio'],base]:
 c=bb('TEMP reserva rodillas consola',[18.177,18.91],[3.249,3.950],[2.55,3.45],col='REFERENCE',bev=.004);cut(ob,c);remove(c.name)
report['console']={'surface_equipment_raise_m':delta,'raised_objects':raised,'knee_void_source':[18.177,3.25,2.55,18.777,3.95,3.45],'floor':3.25,'seat_top':3.72,'minimum_knee_clearance_above_seat':.230,'nominal_worktop_front_height_above_floor':.750,'screen_and_speakers':'independent stands retained','details':'Proposed digital-control console chassis; no manufacturer identification or equipment certification.'}
# Remove low duplicate shower head; preserve the assembled replacement fixture.
remove('Ducha baño vivienda')
bpy.data.objects['Bañera vivienda']['fixture_classification']='Bañera compacta/asiento 1.25x0.74m; producto a seleccionar. No inmersión adulta extendida.'
# Physical freeboard: wave crest100mm below basin wall cap+0.070, not above it.
water=bpy.data.objects['Agua de pileta'];wa,wb=bounds(water);map_h(water,float(wa[2]),-.030)
water['design_water_crest_y']=-.030;water['freeboard_to_basin_cap_m']=.100
report['pool']={'basin_cap':.070,'water_crest':-.030,'freeboard_m':.100,'status':'P cota operativa de agua; filtración/skimmer/equipos requieren proyecto hidráulico.'}
report['bath_compact']='1.25x0.74m compact/asiento, producto a seleccionar'
S['r6h_dimensional_corrections']=json.dumps(report,ensure_ascii=False);S['review_iteration']='95 / R6H dimensional coordination'
S.frame_set(1);bpy.context.view_layer.update();bpy.context.preferences.filepaths.save_version=0
name='Casa_de_Campo_95_R6H_preview.blend' if '--preview' in sys.argv else 'Casa_de_Campo_95_R6H.blend'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output',name),compress=True)
json.dump(report,open(os.path.join(ROOT,'review95','r6h_dimension_corrections.json'),'w'),ensure_ascii=False,indent=2);print('R6H_SAVED',name,flush=True)
