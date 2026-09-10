"""P: shower face2.10m above finalfloor. Execute on loaded model; optionallysave."""
import bpy,json,sys,argparse,hashlib
from pathlib import Path
from mathutils import Vector
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
def ys(o):return [(o.matrix_world@Vector(v)).z for v in o.bound_box]
def set_world_height_map(o,fn):
 mw=o.matrix_world.copy();mi=mw.inverted()
 for v in o.data.vertices:
  p=mw@v.co;p.z=fn(p.z);v.co=mi@p
 o.data.update()
head=bpy.data.objects['Ducha baño mono'];old=min(ys(head));target=2.31;delta=target-old
set_world_height_map(head,lambda h:h+delta)
set_world_height_map(bpy.data.objects['BTH95 | ducha brazo rociador'],lambda h:h+delta)
set_world_height_map(bpy.data.objects['BTH95 | ducha columna'],lambda h:1.31+(h-1.31)*(2.02+delta-1.31)/(2.02-1.31))
for name in ['BTH95 | ducha ménsula.001','BTH95 | ducha roseta.001']:
 if name in bpy.data.objects:set_world_height_map(bpy.data.objects[name],lambda h:h+delta)
bpy.context.view_layer.update();assert abs(min(ys(head))-.21-2.10)<2e-6
head['P_clearance_above_floor_m']=2.10
report={'floor_m':.21,'head_low_face_m':min(ys(head)),'clear_height_m':min(ys(head))-.21,'delta_m':delta,'status':'P dimensioned placement; mixerunchanged; upperarm,column,bracket continuous. No product certification.'}
if '--' in sys.argv:
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--report',required=True);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out).resolve();bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True);report.update(model=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest());Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('SHOWER_CLEARANCE',report,flush=True)
