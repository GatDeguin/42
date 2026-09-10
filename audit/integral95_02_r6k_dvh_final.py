"""Independent exact final fixed-DVH coordination probe; read-only file, no render."""
import bpy,bmesh,json,hashlib,sys,itertools
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
SOURCE=Path(bpy.data.filepath);EXPECTED='a3663a5081dac391303f25b8e9994b1a412a008e971642af29fc2cbee849aa90'
digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest();assert digest==EXPECTED
out={'source':str(SOURCE),'sha256':digest,'method':'Independent evaluated mesh EXACT Boolean, plus rays to measured original faces of frame/EPDM/sill. Includes GL95 glazing parts versus neighbouring hosts, not only builder selected frames. Does not save the source.','pairs':[],'contacts':[],'scope':'Geometric coordination only, no watertightness/capacity/acoustic certification.'}
geo_cache={}
def geom(o):
 if o.name in geo_cache:return geo_cache[o.name]
 e=o.evaluated_get(dg);m=e.to_mesh();v=[e.matrix_world@p.co for p in m.vertices];f=[list(p.vertices) for p in m.polygons];e.to_mesh_clear()
 a=[min(p[i] for p in v) for i in range(3)];b=[max(p[i] for p in v) for i in range(3)]
 g=(v,f,a,b,BVHTree.FromPolygons(v,f));geo_cache[o.name]=g;return g
def copy_mesh(o):
 v,f,*_=geom(o);m=bpy.data.meshes.new('AUDIT_TEMP_MESH');m.from_pydata(v,[],f);m.update();q=bpy.data.objects.new('AUDIT_TEMP_OBJ',m);S.collection.objects.link(q);return q
def intersection(a,b):
 qa,qb=copy_mesh(a),copy_mesh(b)
 mod=qa.modifiers.new('audit exact intersection','BOOLEAN');mod.operation='INTERSECT';mod.solver='EXACT';mod.object=qb
 bpy.context.view_layer.objects.active=qa;bpy.ops.object.modifier_apply(modifier=mod.name)
 bm=bmesh.new();bm.from_mesh(qa.data);vol=abs(bm.calc_volume(signed=True));bm.free()
 for q in [qa,qb]:m=q.data;bpy.data.objects.remove(q,do_unlink=True);bpy.data.meshes.remove(m)
 return vol
def overlap(a,b):
 aa,ab=geom(a)[2:4];ba,bb=geom(b)[2:4]
 return min(min(ab[i],bb[i])-max(aa[i],ba[i]) for i in range(3))>1e-6
families=[('E','Ventana DVH estudio',['Estudio antepecho ventana','Estudio dintel ventana','Estudio lateral frente','Estudio paño entre ventana y puerta','Vierteaguas DVH estudio']),('D','Puerta ventana dormitorio',['Dormitorio antepecho lateral','Dormitorio dintel lateral','Paño lateral medio vivienda','Vivienda lateral junto estudio'])]
for ident,prefix,hosts in families:
 hosts.append(prefix+' alféizar')
 targets=[o for o in S.objects if o.type=='MESH' and not o.hide_render and ((o.name.startswith(prefix+' ') and (' marco ' in o.name or 'vidrio' in o.name.lower())) or o.name.startswith('GL95 | '+ident+' '))]
 for a in targets:
  for n in hosts:
   b=bpy.data.objects[n]
   if overlap(a,b):
    vol=intersection(a,b);out['pairs'].append({'a':a.name,'b':b.name,'intersection_volume_m3':vol,'pass_geometry':vol<=1e-9})
 # Glass to metal remains checked independently, no global frame exclusion.
 glasses=[o for o in targets if 'vidrio' in o.name.lower() and o.name.startswith(prefix+' ')]
 frames=[o for o in targets if ' marco ' in o.name]
 for a,b in itertools.product(glasses,frames):
  if overlap(a,b):
   vol=intersection(a,b);out['pairs'].append({'a':a.name,'b':b.name,'intersection_volume_m3':vol,'pass_geometry':vol<=1e-9})
 frame=bpy.data.objects[prefix+' marco inferior'];sill=bpy.data.objects[prefix+' alféizar'];pad=bpy.data.objects['GL95 | '+ident+' asiento alféizar EPDM3']
 pa,pb=geom(pad)[2:4];fa,fb=geom(frame)[2:4]
 for fx in [.25,.5,.75]:
  for fz in [.15,.5,.85]:
   x=pa[0]+fx*(pb[0]-pa[0]);y=pa[1]+fz*(pb[1]-pa[1])
   faces={}
   for name,obj,level,direction in [('sill_top',sill,pa[2]+.001,-1),('pad_bottom',pad,pa[2]-.001,1),('pad_top',pad,pb[2]+.001,-1),('frame_bottom',frame,pb[2]-.001,1)]:
    p,_,_,_=geom(obj)[4].ray_cast(Vector((x,y,level)),Vector((0,0,direction)),.015);faces[name]=float(p.z) if p else None
   ok=all(v is not None for v in faces.values())
   gaps={'sill_pad':faces['pad_bottom']-faces['sill_top'],'pad_frame':faces['frame_bottom']-faces['pad_top']} if ok else None
   out['contacts'].append({'family':ident,'point_source_xz':[x,-y],'faces_y':faces,'gaps_m':gaps,'pass_geometry':ok and all(abs(v)<=2e-6 for v in gaps.values())})
 print('INDEPENDENT_DVH_FAMILY_DONE',ident,flush=True)
out['summary']={'pairs':len(out['pairs']),'failed_pairs':[p for p in out['pairs'] if not p['pass_geometry']],'contact_stations':len(out['contacts']),'failed_contacts':[r for r in out['contacts'] if not r['pass_geometry']]}
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==digest
Path(r'D:\2026\42\audit\integral95_02_r6k_dvh_final.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out['summary'],ensure_ascii=False,indent=2),flush=True)
