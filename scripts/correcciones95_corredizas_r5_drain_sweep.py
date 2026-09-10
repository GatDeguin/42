"""Replace six slider drains with explicit watertight swept tube walls. No Boolean tube joins."""
import bpy,json,sys,argparse,hashlib,ast,math,bmesh
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parent.parent;S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();source=Path(bpy.data.filepath)
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--report',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);COL=bpy.data.collections['95 | Corredizas propuestas'];M={m.get('source_material_key'):m for m in bpy.data.materials if m.get('source_material_key')}
for m in bpy.data.materials:
 if m.name.startswith(('MAT95 | ','SL95 | ')):M[m.name.split(' | ',1)[1]]=m
for node in ast.parse((root/'scripts/correcciones95_corredizas_r5.py').read_text(encoding='utf8')).body:
 if isinstance(node,ast.FunctionDef):exec(compile(ast.Module(body=[node],type_ignores=[]),'<slider helper>','exec'))
data=json.loads((root/'review95/corredizas_r5_details_complete.json').read_text(encoding='utf8'));ops=[]
def sweep(name,centers,tangents,normal,outer,inner):
 vertices=[];faces=[];N=32;nr=2 if inner else 1
 for c,t in zip(centers,tangents):
  side=t.cross(normal).normalized()
  for radius in ([outer,inner] if inner else [outer]):
   for j in range(N):vertices.append(cv(c+radius*(normal*math.cos(2*math.pi*j/N)+side*math.sin(2*math.pi*j/N))))
 stride=N*nr
 for i in range(len(centers)-1):
  for layer in range(nr):
   for j in range(N):
    p=i*stride+layer*N+j;q=i*stride+layer*N+(j+1)%N;faces.append((p,q,q+stride,p+stride) if layer==0 else (p,p+stride,q+stride,q))
 for end in [0,len(centers)-1]:
  b=end*stride
  if inner:
   for j in range(N):faces.append((b+j,b+(j+1)%N,b+N+(j+1)%N,b+N+j))
  else:faces.append(tuple(b+j for j in range(N)))
 me=bpy.data.meshes.new(name);me.from_pydata(vertices,[],faces);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();o=bpy.data.objects.new(name,me);COL.objects.link(o);o.data.materials.append(mat('stainless'));o['detail_status']='P / propuesta; tubo hueco barrido radio12mm sin cálculo';return o
for f in data['families']:
 for j,d in enumerate(f['drains'],1):
  name='SL95 | '+f['family']+f' drenaje{j} Ø14 interior10'
  for o in list(COL.objects):
   if o.name.startswith('SL95 | '+f['family']+f' drenaje{j} '):bpy.data.objects.remove(o,do_unlink=True)
  sharp=Vector(d['start']);end=Vector(d['outlet']);a=sharp.copy();a.y=f['rolling_height_m']-.002+.001;out=end-sharp;out.y=0;out.normalize();up=Vector((0,1,0));normal=out.cross(up).normalized();beta=math.atan(.02);R=.012;advance=R*math.tan((math.pi/2-beta)/2);center=sharp+up*advance+out*R;A=sharp+up*advance
  cs=[a,A];ts=[-up,-up]
  for k in range(1,17):
   angle=math.pi+(math.pi/2-beta)*k/16;cs.append(center+R*(out*math.cos(angle)+up*math.sin(angle)));ts.append(-out*math.sin(angle)+up*math.cos(angle))
  cs.append(end);ts.append((end-sharp).normalized())
  cutter=sweep('TMP swept drain reserve',cs,ts,normal,.008,0);done=[]
  for o in list(S.objects):
   if o.type!='MESH' or o==cutter or o.parent or o.name.startswith(('BOT95','TMP')):continue
   if overlap(bounds(o),bounds(cutter)):boolean(o,cutter);done.append(o.name)
  bpy.data.objects.remove(cutter,do_unlink=True);tube=sweep(name,cs,ts,normal,.007,.005)
  midangle=math.pi+(math.pi/2-beta)/2;mid=center+R*(out*math.cos(midangle)+up*math.sin(midangle));tangent=-out*math.sin(midangle)+up*math.cos(midangle)
  d.update(elbow='explicit hollow swept mesh, bend radius12mm,32 sides/16 bend segments',bend_radius_m=R,bend_midpoint=list(mid),bend_tangent=list(tangent),bend_plane_normal=list(normal),mouth_top=list(a));ops.append({'drain':name,'reservation':'swept outerØ16','objects':done})
S['sliding_drain_r6']='P six explicit hollow swept tubesØ14/10;16-segment R12 bends; no Boolean tube unions; structural coordination pending.'
out=Path(args.out).resolve();bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True);data['model']=str(out);data['sha256']=hashlib.sha256(out.read_bytes()).hexdigest();data['source_before_swept_drains']=str(source);data['drain_sweep_reservations']=ops;Path(args.report).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');print('SWEPT_DRAINS_SAVED',data['sha256'],flush=True)
