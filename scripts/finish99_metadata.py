"""Finish R7 semantic collection membership and authored still-camera formats.
No object transforms, architecture, material changes, save, or rendering.
"""
import bpy,json
def apply():
 S=bpy.context.scene;rows=[]
 for o in list(S.objects):
  if not o.name.startswith('R7B |'):continue
  layer=o.get('source_layer')
  targets=['LANDSCAPE'] if layer=='garden' else ['INTERIORS','FURNITURE']
  for name in targets:
   c=bpy.data.collections.get(name)
   if not c:c=bpy.data.collections.new(name);S.collection.children.link(c)
   if o.name not in c.objects:c.objects.link(o)
  if o.name in S.collection.objects:S.collection.objects.unlink(o)
  rows.append(dict(name=o.name,sourceLayer=layer,collections=[c.name for c in o.users_collection]))
 cameras=[]
 for o in S.objects:
  if o.type!='CAMERA' or not o.name.startswith(('CAM |','REV |','LUZ99 |')):continue
  resolution=[1800,2400] if o.name.startswith('LUZ99 |') and 'retrato' in o.name.lower() else [2400,1800]
  o['presentation_resolution']=resolution;cameras.append(dict(name=o.name,resolution=resolution))
 S.render.resolution_x=2400;S.render.resolution_y=1800;S.render.resolution_percentage=100
 S['r7_presentation_metadata']=json.dumps(dict(objects=rows,cameras=cameras),ensure_ascii=False)
 return dict(objects=rows,cameras=cameras)
