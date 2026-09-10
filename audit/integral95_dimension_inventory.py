import bpy,json,hashlib,numpy as np,os,csv,sys,math
from mathutils import Vector
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
stem=os.path.splitext(os.path.basename(bpy.data.filepath))[0]
render_paths={}
def walk_collection(c,enabled=True):
 enabled=enabled and not c.hide_render
 for o in c.objects:render_paths[o.name]=render_paths.get(o.name,False) or enabled
 for ch in c.children:walk_collection(ch,enabled)
walk_collection(S.collection)
out={'source':bpy.data.filepath,'sha256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),'units':{'system':S.unit_settings.system,'scale_length':S.unit_settings.scale_length,'length_unit':S.unit_settings.length_unit},'method':'Read-only complete evaluated dimensional inventory. Source axes X/Yheight/Zdepth. World AABB and transformed local bounding-edge lengths are separately recorded; AABB is not a door clear opening nor a manufactured nominal size. Non-unity object scale is flagged, not treated automatically as incorrect physical dimensions.','objects':[],'unmeasured':[]}
scale=float(S.unit_settings.scale_length)
def fv(v):return [float(x) for x in v]
for o in S.objects:
 if o.type not in ['MESH','CURVE','FONT','SURFACE','META']:
  if o.instance_type!='NONE':out['unmeasured'].append({'name':o.name,'type':o.type,'instance_type':o.instance_type,'reason':'collection instance; evaluate separately for total geometry envelope'})
  continue
 e=o.evaluated_get(dg)
 try:m=e.to_mesh()
 except Exception as ex:out['unmeasured'].append({'name':o.name,'reason':str(ex)});continue
 if not m or not len(m.vertices):
  out['unmeasured'].append({'name':o.name,'reason':'No evaluated vertices'});e.to_mesh_clear();continue
 loc=np.empty((len(m.vertices),3),dtype=float);m.vertices.foreach_get('co',loc.ravel())
 mat=np.array(e.matrix_world);world=loc@mat[:3,:3].T+mat[:3,3]
 src=world[:,[0,2,1]].copy()*scale;src[:,2]*=-1
 amin=src.min(0);amax=src.max(0);size=amax-amin
 edge=(loc.max(0)-loc.min(0))*np.linalg.norm(mat[:3,:3],axis=0)*scale
 det=float(np.linalg.det(mat[:3,:3]))
 flags=[]
 if not np.isfinite(src).all():flags.append('NONFINITE_GEOMETRY')
 if max(size)>1000:flags.append('ENVELOPE_OVER1000m')
 if min(size)<1e-6:flags.append('ZERO_OR_SUB_MICRON_DIMENSION_CHECK_SURFACE')
 if max(abs(np.array(o.scale)-1))>1e-5:flags.append('NON_UNITY_OBJECT_SCALE_REVIEW_CONTEXT')
 if det<0:flags.append('NEGATIVE_WORLD_DETERMINANT_REVIEW_NORMALS')
 cols=[c.name for c in o.users_collection]
 out['objects'].append({'name':o.name,'type':o.type,'collections':cols,'parent':o.parent.name if o.parent else None,'hide_render':o.hide_render,'render_enabled_by_collection':bool(render_paths.get(o.name,False) and not o.hide_render),'hide_viewport':o.hide_viewport,'visible_in_viewlayer':o.visible_get(),'object_scale':fv(o.scale),'world_determinant':det,'world_bounds_source_m':{'min':fv(amin),'max':fv(amax),'size':fv(size)},'evaluated_local_edges_world_m':fv(edge),'vertex_count':len(m.vertices),'face_count':len(m.polygons),'materials':[ma.name if ma else None for ma in m.materials],'flags':flags})
 e.to_mesh_clear()
out['summary']={'measured_objects':len(out['objects']),'render_enabled_objects':sum(o['render_enabled_by_collection'] for o in out['objects']),'non_unity_scale':sum('NON_UNITY_OBJECT_SCALE_REVIEW_CONTEXT' in o['flags'] for o in out['objects']),'negative_world_determinant':sum('NEGATIVE_WORLD_DETERMINANT_REVIEW_NORMALS' in o['flags'] for o in out['objects']),'unmeasured':len(out['unmeasured'])}
out['instance_envelopes']=[]
for inst in dg.object_instances:
 if not inst.is_instance:continue
 o=inst.object
 if o.type not in ['MESH','CURVE','SURFACE','META','FONT']:continue
 v=np.array([inst.matrix_world@Vector(c) for c in o.bound_box]);ss=v[:,[0,2,1]]*scale;ss[:,2]*=-1
 out['instance_envelopes'].append({'name':o.name,'parent':inst.parent.name if inst.parent else None,'method':'conservative transformed local evaluated bounding box; geometry object measured separately','min_source_m':fv(ss.min(0)),'max_source_m':fv(ss.max(0)),'persistent_id':list(inst.persistent_id)})
out['summary']['evaluated_instance_envelopes']=len(out['instance_envelopes'])
path=r'D:\2026\42\audit\integral95_dimensions_'+stem
json.dump(out,open(path+'.json','w',encoding='utf8'),ensure_ascii=False,indent=2)
with open(path+'.csv','w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['Objeto','ActivoRender','Colecciones','Xmin_m','AlturaMin_m','Zmin_m','Xmax_m','AlturaMax_m','Zmax_m','DX_m','Altura_m','DZ_m','EscalaX','EscalaY','EscalaZ','Alertas_no_dictamen'])
 for o in out['objects']:
  b=o['world_bounds_source_m'];w.writerow([o['name'],o['render_enabled_by_collection'],' / '.join(o['collections']),*b['min'],*b['max'],*b['size'],*o['object_scale'],' / '.join(o['flags'])])
print(json.dumps({'source':out['source'],'sha256':out['sha256'],'units':out['units'],'summary':out['summary'],'unmeasured':out['unmeasured']},ensure_ascii=False,indent=2))
