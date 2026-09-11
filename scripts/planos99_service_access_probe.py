"""Read-only spatial probe for proposed D08 service platform and handling sequence."""
import bpy,bmesh,ast,json,hashlib,math,sys,argparse
from pathlib import Path
from mathutils import Vector
R=Path(r'D:/2026/42')
ap=argparse.ArgumentParser();ap.add_argument('--out',default='review99/service_access_r7d.json');ap.add_argument('--expected-sha');ar=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
model=Path(bpy.data.filepath);source_sha=hashlib.sha256(model.read_bytes()).hexdigest()
if ar.expected_sha and source_sha!=ar.expected_sha.lower():raise RuntimeError('Service probe source SHA mismatch')
out=(R/ar.out).resolve()
if R not in out.parents or R/'docs' in out.parents:raise ValueError('Service probe output must be local outside docs')
S=bpy.context.scene;S.frame_set(150);bpy.context.view_layer.update()
for node in ast.parse((R/'scripts/planos95_juntas_check.py').read_text('utf8')).body:
 if isinstance(node,ast.FunctionDef) and node.name in ['bounds','overlap','vol']:exec(compile(ast.Module(body=[node],type_ignores=[]),'<helper>','exec'),globals())
temporarily_moved=[o.name for o in S.objects if o.name=='Mueble apoyo estudio' or o.name.startswith('MOB95 | apoyo mueble estudio')]
others=[o for o in S.objects if o.type=='MESH' and not o.hide_render and o.name not in temporarily_moved];bb={o.name:bounds(o) for o in others};rows=[]
def box(n,x,h,z):
 v=[(xx,-zz,hh) for hh in h for zz in z for xx in x];f=[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)];m=bpy.data.meshes.new(n);m.from_pydata(v,[],f);bm=bmesh.new();bm.from_mesh(m);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(m);bm.free();o=bpy.data.objects.new(n,m);S.collection.objects.link(o);return o
for side,zc in [('central',5.00)]:
 p=box('PROBE platform '+side,[18.70,19.90],[3.251,4.65],[zc-.30,zc+.30]);bpy.context.view_layer.update();hits=[];pairs=0
 for o in others:
  if overlap(bounds(p),bb[o.name]):
   vv=vol(p,o);pairs+=1
   if vv>1e-8:hits.append({'object':o.name,'volume':vv})
 rows.append({'id':p.name,'source_bounds':{'x':[18.70,19.90],'h':[3.251,4.65],'z':[zc-.30,zc+.30]},'hits':hits,'pairs':pairs});bpy.data.objects.remove(p,do_unlink=True)
 for kind,cx,xa,xb,hmax,zr,unit_z in [(kind,cx,xa,xb,hm,zr,uz) for kind,cx,xa,xb,hm,zr in [('filter',19.15,18.783,18.805,6.999,.110),('fan',19.55,18.949,19.151,6.969,.079),('silencer',18.925,19.199,19.801,7.018,.128)] for uz in [4.68,5.10]]:
  bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=.225,depth=1.72,location=(cx,-zc,4.65+.86));person=bpy.context.object;person.name='PROBE operator '+side+' '+kind;bpy.context.view_layer.update();hits=[];pairs=0
  for o in others:
   if overlap(bounds(person),bb[o.name]):
    vv=vol(person,o);pairs+=1
    if vv>1e-8:hits.append({'object':o.name,'volume':vv})
  transfer=box('PROBE transfer',[xa,xb],[4.65,5.655],[min(zc-zr,unit_z-zr),max(zc+zr,unit_z+zr)]);bpy.context.view_layer.update();pv=vol(person,transfer)
  th=[]
  for o in others:
   if overlap(bounds(transfer),bb[o.name]):
    vv=vol(transfer,o);pairs+=1
    if vv>1e-8:th.append({'object':o.name,'volume':vv})
  rows.append({'id':person.name,'person_source_center':[cx,5.51,zc],'body_mm':[450,1720],'head_height':6.37,'head_clearance_to_ceiling_m':.08,'operator_hits':hits,'transfer_hits':th,'operator_transfer_overlap_m3':pv,'pairs':pairs,'module_x':[xa,xb],'unit_z':unit_z,'receive_z':zc,'transfer_height':[4.65,5.655]})
  bpy.data.objects.remove(person,do_unlink=True);bpy.data.objects.remove(transfer,do_unlink=True)
r={'model':bpy.data.filepath,'sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'proposal':'P temporary mobile elevating work platform1200x600, deck1.40m above NPT. Central placement X18.70..19.90/Z4.70..5.30; operator shifts laterally for each component. Temporarily move the support cabinet and its four legs before placing platform. Module drops toH5.4 then moves horizontally to platform and lowers with platform to floor. Access equipment/product/stability/load capacity not selected or validated. No claim of normative access.','temporarily_moved_furniture':temporarily_moved,'rows':rows,'pass':not any(q.get('hits') or q.get('operator_hits') or q.get('transfer_hits') or q.get('operator_transfer_overlap_m3',0)>1e-8 for q in rows),'source_mutation':'None; no save.'}
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(r,ensure_ascii=False,indent=2),'utf8')
if out.name=='service_access_proposal.json':
 template=(R/'scripts/planos99_service_access.md').read_text('utf8')
 template=template.replace('{MODEL_NAME}',model.name).replace('{MODEL_SHA256}',source_sha)
 template+='\nEnsayo repetido sobre la fuente indicada. No se infiere equivalencia por el nombre de revision; el JSON contiene la SHA medida en esta ejecucion.\n'
 (out.parent/'ACCESO_MANTENIMIENTO_D08.md').write_text(template,'utf8')
assert hashlib.sha256(model.read_bytes()).hexdigest()==source_sha,'Source changed during probe'
print(json.dumps({'pass':r['pass'],'sha256':r['sha256'],'out':str(out),'cases':len(rows)},ensure_ascii=True),flush=True)
if not r['pass']:sys.exit(1)
