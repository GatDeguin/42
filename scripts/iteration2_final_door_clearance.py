import bpy,os,json
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
door=bpy.data.objects['DOOR | bathLink']
for fc in door.animation_data.drivers:
 if fc.data_path=='rotation_euler':fc.driver.expression='opening * 1.6022122533307945'
door['construction_note']='Outward swing into wardrobe circulation, preserving closed source location and existing opening; frees bidet and bath camera.'
blanket=bpy.data.objects['Cama dormitorio manta'];mw=blanket.matrix_world.copy();inv=mw.inverted();p=[mw@v.co for v in blanket.data.vertices];lo=min(v.x for v in p);hi=max(v.x for v in p)
if hi>16.68:
 for v,w in zip(blanket.data.vertices,p):w.x=lo+(w.x-lo)*(16.68-lo)/(hi-lo);v.co=inv@w
blanket['construction_note']='Throw folded back within mattress area to keep foot-end door swing clear; bed body retained.'
S.frame_set(1);bpy.context.view_layer.update()
# Test modified sense against walls and all fixtures before saving.
exec(compile(open(os.path.join(ROOT,'scripts','verify_coordination.py'),encoding='utf8').read(),'coordination','exec'),{})
script=open(os.path.join(ROOT,'audit','door_fixtures_03.py'),encoding='utf8').read().replace('audit\\door_fixtures_03.json','review\\door_fixtures_final.json').replace('[1,50,66,78,90,105]','list(range(1,106,4))+[105]')
exec(compile(script,'door_fixture_check','exec'),{})
S.frame_set(1);S.camera=bpy.data.objects['CAM | Presentación verticales corregidas'];bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo_Revision.blend'),compress=True)
print('DOOR_FIXTURE_REPAIR_SAVED',flush=True)
