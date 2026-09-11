"""Read-only R8 environment/camera inventory and full textile rebuild equality."""
import bpy,runpy,json,hashlib,time
from pathlib import Path
from mathutils import Vector
R=Path(r'D:/2026/42');S=bpy.context.scene;source=Path(bpy.data.filepath);sha=hashlib.sha256(source.read_bytes()).hexdigest()
assert sha=='9d4501a26630b5679fbaa1a6e75026f4ae0645fb80f4cf2cc94951ba221a24f0'
S.frame_set(1);bpy.context.view_layer.update()
def val(v):
 try:return list(v)
 except TypeError:return v
report={'source':str(source),'sourceSHA256':sha,'world':{'name':S.world.name,'nodes':[]},'lights':[],'cameras':[],'environment':[]}
for n in S.world.node_tree.nodes:
 report['world']['nodes'].append({'name':n.name,'type':n.type,'image':n.image.filepath if hasattr(n,'image') and n.image else None,'inputs':{s.name:val(s.default_value) for s in n.inputs if hasattr(s,'default_value') and not s.is_linked}})
for o in S.objects:
 if o.type=='LIGHT':report['lights'].append({'name':o.name,'type':o.data.type,'power':o.data.energy,'color':list(o.data.color),'location':list(o.matrix_world.translation),'rotation':list(o.rotation_euler)})
 if o.type=='CAMERA' and any(x in o.name for x in ['Pileta','Exterior','exterior','Presentación']):report['cameras'].append({'name':o.name,'p':list(o.matrix_world.translation),'quaternion':list(o.matrix_world.to_quaternion()),'lens':o.data.lens,'shift':[o.data.shift_x,o.data.shift_y]})
 if o.type=='MESH' and ('Entorno' in o.name or 'pradera' in o.name):
  pts=[o.matrix_world@Vector(p) for p in o.bound_box]
  report['environment'].append({'name':o.name,'hidden':o.hide_render,'bounds':[[min(p[k] for p in pts),max(p[k] for p in pts)] for k in range(3)],'materials':[m.name for m in o.data.materials]})
(R/'review99/r8_visual/environment_inventory.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),'utf8')
m=runpy.run_path(str(R/'scripts/correcciones99_textiles_botanica_r8.py'));before=m['fingerprints'](S.objects);counts=[len(bpy.data.objects),len(bpy.data.meshes),len(bpy.data.materials)];t=time.time();applied=m['apply']();runpy.run_path(str(R/'scripts/sync99_scene_variants.py'))['apply']();S.frame_set(1);bpy.context.view_layer.update();after=m['fingerprints'](S.objects)
changes={'added':sorted(after.keys()-before.keys()),'removed':sorted(before.keys()-after.keys()),'changed':sorted(n for n in before.keys()&after.keys() if before[n]!=after[n])}
result={'sourceSHA256':sha,'pass':before==after,'changes':changes,'counts_before':counts,'counts_after':[len(bpy.data.objects),len(bpy.data.meshes),len(bpy.data.materials)],'seconds':time.time()-t,'sourceUnchanged':hashlib.sha256(source.read_bytes()).hexdigest()==sha}
(R/'review99/r8_visual/textiles_idempotence.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),'utf8');print('TEXTILES_R8_REAPPLY',result,flush=True);assert result['pass'] and result['sourceUnchanged']
