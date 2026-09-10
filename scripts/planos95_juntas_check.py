import bpy,json,sys,bmesh,hashlib
from pathlib import Path
from mathutils import Vector
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
def bounds(o):
 p=[o.matrix_world@Vector(v) for v in o.bound_box];return ([min(v[i] for v in p) for i in range(3)],[max(v[i] for v in p) for i in range(3)])
def overlap(a,b):return all(min(a[1][i],b[1][i])-max(a[0][i],b[0][i])>.00001 for i in range(3))
def vol(a,b):
 dg=bpy.context.evaluated_depsgraph_get();o=bpy.data.objects.new('TEST intersection',bpy.data.meshes.new_from_object(a.evaluated_get(dg)));S.collection.objects.link(o);o.matrix_world=a.matrix_world.copy();m=o.modifiers.new('intersection','BOOLEAN');m.operation='INTERSECT';m.solver='EXACT';m.object=b;e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=e.to_mesh();bm=bmesh.new();bm.from_mesh(me);bm.transform(e.matrix_world);v=abs(bm.calc_volume(signed=True));bm.free();e.to_mesh_clear();mesh=o.data;bpy.data.objects.remove(o,do_unlink=True);bpy.data.meshes.remove(mesh);return v
pre=['Puerta doble mono izquierda','Puerta doble mono derecha','Puerta ventana dormitorio','Corrediza lateral A','Corrediza lateral B','Ventana DVH estudio'];hits=[];pairs=0;sealhits=[]
for prefix in pre:
 glass=[o for o in S.objects if o.type=='MESH' and o.name.startswith(prefix+' ') and 'vidrio' in o.name.lower()];frame=[o for o in S.objects if o.type=='MESH' and o.name.startswith(prefix+' marco ')];legacy=[o.name for o in S.objects if o.name.startswith(prefix+' Burlete ')];assert not legacy
 for g in glass:
  for m in frame:
   if not overlap(bounds(g),bounds(m)):continue
   v=vol(g,m);pairs+=1
   if v>1e-9:hits.append([g.name,m.name,v])
 print('CHECK_GLASS',prefix,flush=True)
for g in [o for o in S.objects if o.type=='MESH' and any(o.name.startswith(p+' ') for p in pre) and 'vidrio' in o.name.lower()]:
 for j in [o for o in S.objects if o.type=='MESH' and o.name.startswith('GL95 |')]:
  if not overlap(bounds(g),bounds(j)):continue
  v=vol(g,j);pairs+=1
  if v>1e-9:sealhits.append([g.name,j.name,v])
out=Path(sys.argv[sys.argv.index('--')+1]);model=Path(bpy.data.filepath);r={'model':str(model),'sha256':hashlib.sha256(model.read_bytes()).hexdigest(),'pass':not(hits or sealhits),'hard_metal_glass_intersections':hits,'seal_glass_intersections':sealhits,'boolean_pairs':pairs,'rig_count':len([o for o in S.objects if o.name.startswith('DOOR |')]),'scope':'6families; positiveevaluatedBooleanvolume>1e-9m3; no product/performance certification.'};out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(r,ensure_ascii=False),flush=True)
