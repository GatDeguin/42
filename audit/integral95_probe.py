import bpy,os,json,hashlib
from mathutils import Vector
from datetime import datetime,timezone
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));s=bpy.context.scene
s.frame_set(1);bpy.context.view_layer.update()
materials={};objects=[]
for o in s.objects:
 if o.type=='MESH':
  used=[]
  for slot in o.material_slots:
   m=slot.material
   if not m:continue
   used.append(m.name)
   if m.name not in materials:
    bs=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None) if m.use_nodes else None
    inputs={}
    if bs:
     for key in ['Base Color','Metallic','Roughness','IOR','Alpha','Normal','Transmission Weight']:
      if key not in bs.inputs:continue
      sock=bs.inputs[key]
      value=sock.default_value
      inputs[key]={'linked':sock.is_linked,'value':list(value) if hasattr(value,'__len__') else value}
    nodes=list(m.node_tree.nodes) if m.use_nodes else []
    materials[m.name]={'objects':0,'principled':inputs,'node_types':sorted(set(n.type for n in nodes)),'images':[{'name':n.image.name,'size':list(n.image.size),'packed':bool(n.image.packed_file),'color_space':n.image.colorspace_settings.name} for n in nodes if n.type=='TEX_IMAGE' and n.image]}
   materials[m.name]['objects']+=1
  bounds=[o.matrix_world@Vector(co) for co in o.bound_box]
  objects.append({'name':o.name,'collections':[c.name for c in o.users_collection],'vertices':len(o.data.vertices),'polygons':len(o.data.polygons),'materials':used,'modifiers':[{'type':m.type,'name':m.name} for m in o.modifiers],'render_hidden':o.hide_render,'bounds':{'min':[min(p[i] for p in bounds) for i in range(3)],'max':[max(p[i] for p in bounds) for i in range(3)]}})
lights=[{'name':o.name,'type':o.data.type,'energy':o.data.energy,'color':list(o.data.color),'position':list(o.matrix_world.translation)} for o in s.objects if o.type=='LIGHT']
cameras=[{'name':o.name,'lens':o.data.lens,'shift_x':o.data.shift_x,'shift_y':o.data.shift_y,'position':list(o.matrix_world.translation),'dof':o.data.dof.use_dof} for o in s.objects if o.type=='CAMERA']
report={'timestamp':datetime.now(timezone.utc).isoformat(),'file':os.path.basename(bpy.data.filepath),'sha256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),'render':{'engine':s.render.engine,'samples':s.cycles.samples,'view_transform':s.view_settings.view_transform,'look':s.view_settings.look,'exposure':s.view_settings.exposure,'resolution':[s.render.resolution_x,s.render.resolution_y],'world_nodes':[n.type for n in s.world.node_tree.nodes] if s.world and s.world.use_nodes else []},'counts':{'meshes':len(objects),'materials':len(materials),'lights':len(lights),'cameras':len(cameras)},'materials':materials,'lights':lights,'cameras':cameras,'objects':objects}
json.dump(report,open(os.path.join(ROOT,'audit','integral95_inventory.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
print(json.dumps(report['counts']),flush=True)
print('AUDIT_ONLY_NO_BLEND_SAVED',report['sha256'],flush=True)
