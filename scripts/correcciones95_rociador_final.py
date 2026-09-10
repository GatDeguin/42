"""P flat rain-shower head, source mounting point preserved; inspection camera faces its wall. No save."""
import bpy,math,ast,json,os
from mathutils import Vector
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m.get('source_material_key'):m for m in bpy.data.materials if m.get('source_material_key')};COL={c.name:c for c in bpy.data.collections}
def cv(p):return Vector((p[0],-p[2],p[1]))
for nd in ast.parse(open(R+'/scripts/correcciones95_materialidad.py',encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['mesh','cyl']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
assert not bpy.data.objects.get('Ducha baño mono | conexión vertical')
old=bpy.data.objects['Ducha baño mono'];bpy.data.objects.remove(old,do_unlink=True)
vs=[];fs=[];N=96;cx,cz=21.35,4.60;prof=[(.098,2.310),(.100,2.312),(.100,2.320),(.098,2.322)]
for rad,h in prof:
 vs.extend([cv([cx+rad*math.cos(k*math.tau/N),h,cz+rad*math.sin(k*math.tau/N)]) for k in range(N)])
fs.append(tuple(range(N-1,-1,-1)))
for j in range(len(prof)-1):
 for k in range(N):q=(k+1)%N;fs.append((j*N+k,j*N+q,(j+1)*N+q,(j+1)*N+k))
fs.append(tuple((len(prof)-1)*N+k for k in range(N)))
ob=mesh('Ducha baño mono',vs,fs,'stainless','GROUND_FLOOR')
import bmesh
bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(ob.data);bm.free()
for f in ob.data.polygons:f.use_smooth=len(f.vertices)==4
mat=bpy.data.materials.get('FIT95 | boquillas silicona') or bpy.data.materials.new('FIT95 | boquillas silicona');mat.use_nodes=True;b=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');b.inputs['Base Color'].default_value=(.12,.13,.12,1);b.inputs['Roughness'].default_value=.65;M['nozzles']=mat
num=0
for r,n in [(0,1),(.024,10),(.046,18),(.068,26),(.086,34)]:
 for k in range(n):
  a=k*math.tau/n+r*7;x=cx+r*math.cos(a);z=cz+r*math.sin(a)
  o=cyl('Ducha baño mono | boquilla %02d'%num,[x,2.3099,z],[x,2.312,z],.0014,'nozzles','GROUND_FLOOR');num+=1
cyl('Ducha baño mono | conexión vertical',[cx,2.322,cz],[cx,2.370,cz],.007,'stainless','GROUND_FLOOR')
ob['P_clearance_above_floor_m']=2.10;ob['P_product']='Rociador genérico plano Ø200x12 mm con boquillas; producto comercial pendiente de seleccionar.'
c=bpy.data.objects['REV | Baño mono'];c.location=cv([19.74,1.72,4.92]);c.rotation_euler=(cv([21.30,1.43,4.90])-c.location).to_track_quat('-Z','Y').to_euler();c.data.lens=18;c['presentation_frame']=150;c.data.clip_start=.035
report={'head_body_diameter_m':.200,'head_body_thickness_m':.012,'body_low_face':2.310,'nozzle_low_face':2.3099,'floor':.21,'minimum_clearance_m':2.0999,'nozzles':num,'mount_center_source':[21.35,2.370,4.60],'column_mixer_wall_fixings':'unchanged','proposal':'Generic product visualization; no hydraulic or manufacturer certification'}
S['r6k_shower_head']=json.dumps(report);json.dump(report,open(R+'/review95/r6k_shower_head.json','w'),indent=2);bpy.context.view_layer.update();print('SHOWER_HEAD_READY_NO_SAVE',num)
