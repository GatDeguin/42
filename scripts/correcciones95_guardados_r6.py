"""R6C closes remaining support gaps and defines sliding TV cabinet fronts."""
import bpy,os,math,json,ast,numpy as np,sys
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
for m in bpy.data.materials:
 if m.name.startswith('MAT95 | '):M[m.name.split(' | ',1)[1]]=m
def cv(p):return Vector((p[0],-p[2],p[1]))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_textiles.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['bounds','deform','map_h']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_materialidad.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['box','cyl']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<fast>','exec'))
def cut(o,c):
 bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;m=o.modifiers.new('Reserva real R6C','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=c;bpy.ops.object.modifier_apply(modifier=m.name)
# Four supports reach the actual underside of studio storage cabinet.
ob=bpy.data.objects['Mueble apoyo estudio'];a,b=bounds(ob)
for x in [a[0]+.10,b[0]-.10]:
 for z in [-b[1]+.07,-a[1]-.07]:box('MOB95 | apoyo mueble estudio',[x,(3.25+a[2])/2,z],[.028,a[2]-3.25,.028],'blackMetal','STUDIO',.002)
# Wardrobe base carries all vertical panels; inset face keeps original visual shadow line.
box('MOB95 | zócalo portante vestidor',[18.52,3.265,6.44],[1.61,.030,.585],'blackMetal','INTERIORS',.001)
for o in [v for v in S.objects if v.name.startswith('Vestidor zapatero ')]:o.location.z-=.015
map_h(bpy.data.objects['Vestidor cajón 0'],3.665,3.905)
for i in range(3):
 ob=bpy.data.objects['Vestidor cajón '+str(i)];a,b=bounds(ob)
 for x in [17.753,18.247]:
  box('MOB95 | guía fija cajón vestidor',[x,(a[2]+b[2])/2,6.475],[.012,.025,.450],'stainless','INTERIORS',.001)
  box('MOB95 | guía móvil cajón vestidor',[x+(.008 if x<18 else -.008),(a[2]+b[2])/2,6.475],[.005,.018,.445],'blackMetal','INTERIORS',.0005)
# TV storage is used through sliding fronts, not a400mm drawer into345mm clearance.
tv=bpy.data.objects['Mueble TV'];a,b=bounds(tv)
box('MOB95 | zócalo portante TV',[(a[0]+b[0])/2,(3.25+a[2])/2,-(a[1]+b[1])/2],[b[0]-a[0]-.06,a[2]-3.25,b[1]-a[1]-.06],'blackMetal','INTERIORS',.001)
c=box('TEMP interior TV',[(a[0]+b[0])/2,(a[2]+b[2])/2,-b[1]+.133],[b[0]-a[0]-.036,b[2]-a[2]-.036,.300],'blackMetal','REFERENCE',0);cut(tv,c);bpy.data.objects.remove(c,do_unlink=True)
for h in [3.312,3.938]:
 for z in [11.489,11.508]:
  box('MOB95 | riel corredero TV',[15.60,h,z],[1.55,.004,.004],'blackMetal','INTERIORS',.0005)
for label,x,z in [('izquierda',15.22,11.493),('derecha',15.98,11.512)]:
 box('MOB95 | frente corredero TV '+label,[x,3.625,z],[.79,.616,.014],'wood','INTERIORS',.002)
 box('MOB95 | uñero frente TV '+label,[x+(-.30 if label=='izquierda' else .30),3.73,z-.0075],[.016,.10,.001],'blackMetal','INTERIORS',.002)
S['review_iteration']='95 / R6C support and cabinet use details'
S['r6c_supports']=json.dumps({'studio_sideboard_legs':4,'wardrobe_plinth_mm':30,'tv_plinth_mm':30,'wardrobe_drawer0_bottom':3.665,'wardrobe_lower_shelf_top':3.6525,'tv_fronts':'two sliding fronts, no drawer projection into coffee-table gap','warning':'Cabinet hardware geometry is an unbranded proposal, not load-certified.'})
S.frame_set(1);bpy.context.view_layer.update();bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
name='Casa_de_Campo_95_R6C_preview.blend' if '--preview' in sys.argv else 'Casa_de_Campo_95_R6C.blend'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output',name),compress=True);print('R6C_SAVED',flush=True)
