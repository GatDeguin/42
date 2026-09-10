"""Final geometric cleanup: coherent dining shift and grass excluded under real bench pads."""
import bpy,bmesh,json,os,hashlib
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
assert not S.get('r6k_cleanup_applied',False)
P=json.load(open(ROOT+'/planos95/layout_r4/propuesta_bano_cocina.json',encoding='utf8'))
names=set(P['dining']['objects'])
names.update(['Lámpara comedor','Cable lámpara comedor 17.69','Cable lámpara comedor 18.61','Florero comedor','MOB95 | difusor opal Lámpara comedor'])
names.update(o.name for o in S.objects if o.type=='LIGHT' and 'comedor' in o.name.lower())
moved=[]
for name in sorted(names):
 o=bpy.data.objects.get(name)
 if o:
  m=o.matrix_world.copy();m.translation.y-=.010;o.matrix_world=m;moved.append(name)
bpy.context.view_layer.update()
def box(o):
 pts=[o.matrix_world@Vector(c) for c in o.bound_box]
 return ([min(p[i] for p in pts) for i in range(3)],[max(p[i] for p in pts) for i in range(3)])
pads=[o for o in S.objects if o.name.startswith('Banco huerta | loseta hormigón P')]
assert len(pads)==4
footprints=[box(o) for o in pads];grass=[]
for ob in [o for o in S.objects if (o.name.startswith('Césped botánico ') or o.name=='Paisaje | pradera de transición') and o.type=='MESH' and not o.hide_render]:
 lo,hi=box(ob)
 if not any(all(hi[k]>=a[k]-.007 and lo[k]<=b[k]+.007 for k in (0,1)) for a,b in footprints):continue
 ob.data=ob.data.copy();bm=bmesh.new();bm.from_mesh(ob.data);bm.verts.ensure_lookup_table();seen=set();remove=[]
 for v in bm.verts:
  if v.index in seen:continue
  comp=[];todo=[v];seen.add(v.index)
  while todo:
   q=todo.pop();comp.append(q)
   for e in q.link_edges:
    t=e.other_vert(q)
    if t.index not in seen:seen.add(t.index);todo.append(t)
  hit=False
  for q in comp:
   p=ob.matrix_world@q.co
   if any(a[0]-.007<=p.x<=b[0]+.007 and a[1]-.007<=p.y<=b[1]+.007 for a,b in footprints):hit=True;break
  if hit:remove.extend(comp)
 before=len(bm.verts)
 if remove:bmesh.ops.delete(bm,geom=remove,context='VERTS')
 bm.to_mesh(ob.data);bm.free();ob.data.update()
 grass.append({'object':ob.name,'vertices_before':before,'vertices_removed':len(remove),'vertices_after':len(ob.data.vertices)})
S['r6k_cleanup_applied']=True;S['review_iteration']='95 / R6K geometric coordination, independent approval pending';S['video_render_requires_explicit_approval']=True
report={'source':bpy.data.filepath,'source_sha256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),'dining_group_shift_source_z_m':.010,'dining_objects':moved,'grass_exclusions':grass,'pad_objects':[o.name for o in pads],'note':'0.80m dining passage is a project objective, not a claim of regulatory compliance; each drawing measures evaluated geometry.'}
bpy.context.view_layer.update();S.frame_set(1);bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/output/Casa_de_Campo_95_R6K_geometry.blend',compress=True)
json.dump(report,open(ROOT+'/review95/r6k_cleanup.json','w',encoding='utf8'),ensure_ascii=False,indent=2)
print('R6K_GEOMETRY_READY',len(moved),grass,flush=True)
