"""R7 door-hand coordination, callable on an integrated candidate; no save or render.
Same structural openings. Positive object determinants; reflected mesh winding is corrected.
Generic dimensional hardware proposal, not product certification.
"""
import bpy,bmesh,json,math,ast,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parent.parent
TAG='door_hands99_v1';PREFIX='HAND99 | '

def source_bounds(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());p=[ev.matrix_world@Vector(v) for v in ev.bound_box]
 return {'x':[min(v.x for v in p),max(v.x for v in p)],'z':[-max(v.y for v in p),-min(v.y for v in p)],'h':[min(v.z for v in p),max(v.z for v in p)]}

def owned_existing(o):
 return (o.name in ['DOOR | bedroomLink','DOOR | bedroomDining','Puerta dormitorio','Puerta dormitorio manija']
 or o.name.startswith(('Puerta dormitorio marco ','Premarco dormitorio |','Puerta dormitorio comedor |')))

def transform_mesh_world(o,F,old=None):
 old=old.copy() if old is not None else o.matrix_world.copy()
 if F.determinant()>0:
  o.matrix_world=F@old
 else:
  assert o.type=='MESH',o.name
  new=old.copy();new.translation=F@old.translation
  me=o.data.copy();o.data=me;me.transform(new.inverted()@F@old);me.flip_normals();me.update()
  bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
  o.matrix_world=new
  assert o.matrix_world.determinant()>0,o.name

def deform_world(o,fn):
 if o.data.users>1:o.data=o.data.copy()
 inv=o.matrix_world.inverted()
 for v in o.data.vertices:v.co=inv@fn(o.matrix_world@v.co)
 o.data.update()

def apply():
 global S,COL,M
 S=bpy.context.scene
 if S.get(TAG):return json.loads(S[TAG])
 S.frame_set(1);bpy.context.view_layer.update()
 rl=bpy.data.objects['DOOR | bedroomLink'];rd=bpy.data.objects['DOOR | bedroomDining']
 assert abs(-rl.location.y-8.09)<.002 and abs(rd.location.x-16.5825)<.002,'Unexpected door base; review before applying'
 affected=[o for o in S.objects if owned_existing(o)]
 originals={o.name:o.matrix_world.copy() for o in affected}
 report={'version':1,'source':bpy.data.filepath,'existing_scope':[o.name for o in affected],'geometry_proposal':'Same raw openings; north-hand bedroomLink, right-hand/inward bedroomDining, 7mm wider closing jamb.'}
 # Mirror bedroomLink along sourceZ=7.680; bake the reflection into mesh winding, never a negative rig scale.
 F=Matrix.Identity(4);F[1][1]=-1;F[1][3]=-15.36
 rl.location=F@originals[rl.name].translation
 for fc in rl.animation_data.drivers:
  if fc.data_path=='rotation_euler' and fc.array_index==2:fc.driver.expression='opening * -1.5707963267948966'
 bpy.context.view_layer.update()
 for o in affected:
  if o==rl or o.name.startswith('Puerta dormitorio comedor |') or o==rd:continue
  transform_mesh_world(o,F,originals[o.name])
 # Give the inherited leaf a real10mm bottom clearance, retaining its head and plan.
 leaf=bpy.data.objects['Puerta dormitorio'];b=source_bounds(leaf)
 deform_world(leaf,lambda p:Vector((p.x,p.y,3.26+(p.z-3.25)*(b['h'][1]-3.26)/(b['h'][1]-3.25))))
 # Dining assembly turns180deg in plan; posts remain in the unchanged140mm wall.
 centre=Vector((17.04,-9.0,0));R=Matrix.Translation(centre)@Matrix.Rotation(math.pi,4,'Z')@Matrix.Translation(-centre)
 hardware_shift=Matrix.Translation((0,-.0775,0));RF=hardware_shift@R
 rd.location=RF@originals[rd.name].translation
 bpy.context.view_layer.update()
 for o in affected:
  if not o.name.startswith('Puerta dormitorio comedor |'):continue
  frame=o.name in ['Puerta dormitorio comedor | jamba bisagra','Puerta dormitorio comedor | jamba cierre','Puerta dormitorio comedor | dintel']
  transform_mesh_world(o,R if frame else RF,originals[o.name])
 # 35->42mm closing jamb keeps a7.5mm leaf-to-frame gap; leaf915->908mm.
 pj=bpy.data.objects['Puerta dormitorio comedor | jamba cierre']
 deform_world(pj,lambda p:Vector((16.54+(p.x-16.54)*.042/.035,p.y,p.z)))
 pivot=17.4975
 for name in ['Puerta dormitorio comedor | hoja','Puerta dormitorio comedor | burlete inferior soporte']:
  o=bpy.data.objects[name];deform_world(o,lambda p:Vector((pivot+(p.x-pivot)*.908/.915,p.y,p.z)))
 for o in affected:
  if o.name.startswith(('Puerta dormitorio comedor | manija','Puerta dormitorio comedor | galce cierre','Puerta dormitorio comedor | junta cierre')):
   mw=o.matrix_world.copy();mw.translation.x+=.007;o.matrix_world=mw
 for name in ['Puerta dormitorio comedor | galce superior','Puerta dormitorio comedor | junta superior']:
  o=bpy.data.objects[name];bb=source_bounds(o);hi=bb['x'][1];lo=bb['x'][0]
  deform_world(o,lambda p:Vector((hi+(p.x-hi)*(hi-lo-.007)/(hi-lo),p.y,p.z)))
 bpy.context.view_layer.update()
 # Local hardware helpers; do not execute the source construction script.
 COL=bpy.data.collections.get('99 | Door hand hardware') or bpy.data.collections.new('99 | Door hand hardware')
 if COL.name not in S.collection.children:S.collection.children.link(COL)
 M={m.get('source_material_key'):m for m in bpy.data.materials if m.get('source_material_key')}
 for m in bpy.data.materials:
  if m.name.startswith(('SL95 | ','MAT95 | ')):M[m.name.split(' | ',1)[1]]=m
 for nd in ast.parse((ROOT/'scripts/correcciones95_corredizas_r5.py').read_text(encoding='utf-8-sig')).body:
  if isinstance(nd,ast.FunctionDef) and nd.name in ['mat','cv','src','child','box','boolean','cylinder']:
   exec(compile(ast.Module(body=[nd],type_ignores=[]),'<hardware helper>','exec'),globals())
 def erase(o):bpy.data.objects.remove(o,do_unlink=True)
 def pt(t,h,d):return (-d,h,t)
 def part(n,tt,hh,dd,key='blackMetal',parent=None):
  return box(PREFIX+n,{'x':[-dd[1],-dd[0]],'y':hh,'z':tt},key,parent)
 ll=7.27;D=-17.5975;floor=3.25;head=5.43
 north=bpy.data.objects['Puerta dormitorio marco 1']
 # Three12mm knuckle hinges,2.5mm pins,2mm axial gaps, real sleeve bores.
 for index,h in enumerate([floor+.28,floor+1.05,head-.25],1):
  cut=cylinder('TEMP HAND mortise',pt(ll,h-.046,D),pt(ll,h+.046,D),.0062)
  boolean(leaf,cut);boolean(north,cut);erase(cut)
  part('bedroomLink bisagra fija '+str(index),[ll-.035,ll-.008],[h-.045,h+.045],[D,D+.0025],'stainless')
  part('bedroomLink bisagra movil '+str(index),[ll+.006,ll+.036],[h-.014,h+.014],[D,D+.002],'stainless',rl)
  cylinder(PREFIX+'bedroomLink eje '+str(index),pt(ll,h-.046,D),pt(ll,h+.046,D),.0025,'stainless')
  for j,(a,b) in enumerate([(h-.044,h-.016),(h-.014,h+.014),(h+.016,h+.044)]):
   cylinder(PREFIX+'bedroomLink nudillo '+str(index)+'-'+str(j),pt(ll,a,D),pt(ll,b,D),.006,'stainless',rl if j==1 else None,inner=.0028)
   wing=part('bedroomLink ala '+str(index)+'-'+str(j),[ll-.008,ll] if j!=1 else [ll,ll+.008],[a,b],[D,D+.002],'stainless',rl if j==1 else None)
   bore=cylinder('TEMP HAND eje ala',pt(ll,a-.002,D),pt(ll,b+.002,D),.0028);boolean(wing,bore);erase(bore)
  for dh in [-.032,.032]:cylinder(PREFIX+'bedroomLink tornillo marco '+str(index),pt(ll-.023,h+dh,D-.014),pt(ll-.023,h+dh,D+.003),.0018,'stainless')
  for tt in [ll+.015,ll+.028]:cylinder(PREFIX+'bedroomLink tornillo hoja '+str(index),pt(tt,h,D-.014),pt(tt,h,D+.003),.0018,'stainless',rl)
 # Replace the old single cuboid handle with operating handles on both faces.
 old_handle=bpy.data.objects['Puerta dormitorio manija'];old_handle.hide_render=True;old_handle.hide_viewport=True
 ht=4.33;handle_t=7.985;back=D-.045
 for side,face in [(1,D),(-1,back)]:
  cylinder(PREFIX+'bedroomLink manija roseta',pt(handle_t,ht,face),pt(handle_t,ht,face+side*.003),.023,'stainless',rl)
  cylinder(PREFIX+'bedroomLink manija vastago',pt(handle_t,ht,face+side*.003),pt(handle_t,ht,face+side*.035),.006,'stainless',rl)
  cylinder(PREFIX+'bedroomLink manija palanca',pt(handle_t,ht,face+side*.035),pt(handle_t-.10,ht,face+side*.035),.006,'stainless',rl)
 bore=cylinder("TEMP HAND handle bore",(17.590,ht,handle_t),(17.650,ht,handle_t),.0045);boolean(leaf,bore);erase(bore)
 cylinder(PREFIX+"bedroomLink spindle",(17.591,ht,handle_t),(17.649,ht,handle_t),.004,"stainless",rl)
 # Fixed13mm stops plus2mm resilient seals, behind the closed leaf.
 for name,tt in [('bisagra',[7.265,7.2875]),('cierre',[8.0725,8.095])]:
  part('bedroomLink galce '+name,tt,[3.26,5.43],[D-.060,D-.047])
  part('bedroomLink junta '+name,tt,[3.26,5.43],[D-.047,D-.045],'rubber95')
 part('bedroomLink galce superior',[7.2875,8.0725],[5.4125,5.43],[D-.060,D-.047])
 part('bedroomLink junta superior',[7.2875,8.0725],[5.4125,5.43],[D-.047,D-.045],'rubber95')
 # Source rig and keyframes stay intact; only bedroomLink changes driver handedness.
 bpy.context.view_layer.update()
 for r in [rl,rd]:r['hand99_coordinated']=True
 report['bedroomLink']={'pivot_source':[rl.location.x,rl.location.z,-rl.location.y],'driver':'opening * -pi/2','raw_opening_source_z':[7.23,8.13],'leaf_m':[.82,.045,2.17],'bottom_clearance_m':.01,'hardware':'3x12mm sleeved knuckle hinges;5mm pins; two lever handles;13+2mm stops/seals'}
 report['bedroomDining']={'pivot_source':[rd.location.x,rd.location.z,-rd.location.y],'driver':'opening * -pi/2','raw_opening_source_x':[16.54,17.54],'leaf_width_m':.908,'closing_jamb_mm':42,'hinge_jamb_mm':35,'wall_depth_source_z':[8.93,9.07],'galce_max_source_z':9.07}
 report['new_objects']=[o.name for o in S.objects if o.name.startswith(PREFIX)]
 report['rig_count']=len([o for o in S.objects if o.name.startswith('DOOR |')])
 assert report['rig_count']==13
 layout=json.loads(S['r7_layout'])
 for spec in layout['new_doors']:
  if spec['key']=='bedroomDining':
   spec.update({'pivot_source':report['bedroomDining']['pivot_source'],'hinge_side':'right','opens_toward':'bedroom','leaf_width_m':.908,'clear_frame_m':.923,'closing_jamb_mm':42,'wall_range_local_d':[8.93,9.07],'moving_objects':[o.name for o in rd.children_recursive],'clear_min_including_handle_estimate_m':None})
 S['r7_layout']=json.dumps(layout,ensure_ascii=False);S[TAG]=json.dumps(report,ensure_ascii=False)
 S.frame_set(1);bpy.context.view_layer.update()
 return report
