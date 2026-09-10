"""Read-only proof of fixed-DVH rebates andbearingcontact; does notsave."""
import bpy,bmesh,json,ast,sys,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();ROOT=Path(__file__).resolve().parent.parent
for nd in ast.parse((ROOT/'scripts/planos95_juntas_check.py').read_text(encoding='utf-8-sig')).body:
 if isinstance(nd,ast.FunctionDef):exec(compile(ast.Module(body=[nd],type_ignores=[]),'<test helper>','exec'))
def tree(o):
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();v=[e.matrix_world@p.co for p in m.vertices];f=[list(p.vertices) for p in m.polygons];t=BVHTree.FromPolygons(v,f,epsilon=1e-8);e.to_mesh_clear();return t
d=json.loads(S['dv_h_fixed_bearings_r6k']);hits=[];count=0;contacts=[]
for f in d['families']:
 host_names=list(dict.fromkeys(n for op in f['reservations'] for n in op['hosts']));targets=[o for o in S.objects if o.type=='MESH' and o.name.startswith(f['prefix']+' ') and (' marco ' in o.name or 'vidrio' in o.name.lower())]+[bpy.data.objects[n] for n in f['new_pieces']]
 for a in targets:
  for n in host_names:
   b=bpy.data.objects[n]
   if not overlap(bounds(a),bounds(b)):continue
   v=vol(a,b);count+=1
   if v>1e-9:hits.append({'a':a.name,'b':b.name,'volume_m3':v})
 lo,hi=f['seat_common_footprint_source_m']['x'];za,zb=f['seat_common_footprint_source_m']['z'];bed=f['rebate_bottom_m'];top=f['frame_bottom_m'];st=tree(bpy.data.objects[f['sill']]);ft=tree(bpy.data.objects[f['prefix']+' marco inferior'])
 for frac in [.2,.5,.8]:
  x=(lo+hi)/2;z=za+frac*(zb-za);hd=st.ray_cast(Vector((x,-z,bed+.0001)),Vector((0,0,-1)),.003);hu=ft.ray_cast(Vector((x,-z,top-.0001)),Vector((0,0,1)),.003);ok=hd[0] is not None and hu[0] is not None and abs(hd[3]-.0001)<2e-6 and abs(hu[3]-.0001)<2e-6;contacts.append({'family':f['id'],'source_x':x,'source_z':z,'support_gap_m':None if hd[0] is None else hd[3]-.0001,'frame_gap_m':None if hu[0] is None else hu[3]-.0001,'pass':ok})
 print('CHECK_DVH_BEARING',f['id'],'done',flush=True)
model=Path(bpy.data.filepath);r={'model':str(model),'sha256':hashlib.sha256(model.read_bytes()).hexdigest(),'pass':not hits and all(x['pass'] for x in contacts),'intersections':hits,'boolean_pairs':count,'contact_rays':contacts,'rig_count':len([o for o in S.objects if o.name.startswith('DOOR |')]),'scope':'Only fixedframe/glass/bearing against affectedhostmeshes; measuredcontacts at3 interior stations each. No capacity/weathering certification.'};out=Path(sys.argv[sys.argv.index('--')+1]) if '--' in sys.argv else ROOT/'review95/apoyos_dvh_checks.json';out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(r,ensure_ascii=False,indent=2),flush=True)
