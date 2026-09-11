"""Synchronize lighting/inspection scene memberships with the authoritative R7 model.
Does not save or render. Removes only the superseded generated continuous-tour variant;
the authored HTML cameras and the newly validated TOUR | Recorrido virtual remain.
"""
import bpy,json
def apply():
 main=bpy.context.scene
 assert main.name=='CASA DE CAMPO | Atardecer'
 before=[dict(name=s.name,objects=len(s.objects),camera=s.camera.name if s.camera else None) for s in bpy.data.scenes]
 legacy=bpy.data.scenes.get('RECORRIDO | Continuo')
 if legacy:bpy.data.scenes.remove(legacy)
 old=bpy.data.objects.get('TOUR | Recorrido continuo')
 if old:bpy.data.objects.remove(old,do_unlink=True)
 def exclusions(layer):
  rows={}
  def walk(c):
   rows[c.collection.name]=c.exclude
   for child in c.children:walk(child)
  walk(layer.layer_collection);return rows
 def restore(layer,values):
  def walk(c):
   if c.collection.name in values:c.exclude=values[c.collection.name]
   for child in c.children:walk(child)
  walk(layer.layer_collection)
 expected=set(main.objects)
 rows=[]
 for scene in bpy.data.scenes:
  scene['video_render_requires_explicit_approval']=True
  scene['revision99_authoritative_geometry']='R7 shared scene membership'
  if scene==main:continue
  assert scene.camera in expected,(scene.name,scene.camera.name)
  previous={layer.name:exclusions(layer) for layer in scene.view_layers}
  for ob in list(scene.collection.objects):scene.collection.objects.unlink(ob)
  for child in list(scene.collection.children):scene.collection.children.unlink(child)
  for ob in main.collection.objects:scene.collection.objects.link(ob)
  for child in main.collection.children:scene.collection.children.link(child)
  for layer in scene.view_layers:restore(layer,previous.get(layer.name,{}))
  scene.frame_start=main.frame_start;scene.frame_end=main.frame_end;scene.render.fps=main.render.fps
  scene.frame_set(1)
  assert set(scene.objects)==expected,scene.name
  rows.append(dict(name=scene.name,objects=len(scene.objects),sameMembership=True,world=scene.world.name if scene.world else None,camera=scene.camera.name))
 main.frame_set(1)
 report=dict(before=before,after=rows,mainObjects=len(expected),removedGeneratedLegacy=['RECORRIDO | Continuo','TOUR | Recorrido continuo'],retainedTour='TOUR | Recorrido virtual',videoRendered=False)
 main['r7_scene_sync']=json.dumps(report)
 return report
