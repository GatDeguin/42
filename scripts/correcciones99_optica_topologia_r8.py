"""R8 limited topology and mirror-normal repair. No scene save or render in apply()."""
from pathlib import Path
import bpy,bmesh,math,json,hashlib
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
TOPO=['WET99 | PB membrana continua2','WET99 | PB adhesivo4','Vestidor cierre al estar paño A']
MIRRORS=['Espejo baño pileta','Espejo baño suite']
def geometry_signature(o):
 return dict(matrix=[list(r) for r in o.matrix_world],vertices=[list(v.co) for v in o.data.vertices],faces=[list(p.vertices) for p in o.data.polygons],materials=[m.name for m in o.data.materials])
def topology():
 rows=[]
 for name in TOPO:
  o=bpy.data.objects[name];assert not o.modifiers
  before=[o.matrix_world@v.co for v in o.data.vertices];bm=bmesh.new();bm.from_mesh(o.data);edges=[e for e in bm.edges if e.is_boundary];count=len(edges);newarea=0
  if count and name.startswith('WET99'):
   assert count==3,(name,count)
   newfaces=bmesh.ops.holes_fill(bm,edges=edges,sides=3)['faces'];newarea=sum(f.calc_area() for f in newfaces)
   assert newarea<1e-8,(name,newarea)
   for f in newfaces:f.material_index=0
  elif count:
   bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
  bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.normal_update();bad=sum(not e.is_manifold for e in bm.edges)
  assert bad==0,(name,bad)
  volume=bm.calc_volume(signed=True);assert volume>0,(name,volume)
  bm.to_mesh(o.data);bm.free();o.data.update()
  after=[o.matrix_world@v.co for v in o.data.vertices]
  # Exact geometric positions may merge duplicate seam vertices; no macroscopic face moves.
  delta=max(min((p-q).length for q in before) for p in after);assert delta<=1.1e-6,(name,delta)
  o['revision99_r8_topology']='Closed submicrometre degeneracy or coincident seam; physical extent retained'
  rows.append(dict(object=name,boundaryBefore=count,nonmanifoldAfter=bad,maxVertexDisplacementM=delta,filledAreaM2=newarea,positiveVolumeM3=volume))
 return rows

def optical():
 rows=[]
 for name in MIRRORS:
  o=bpy.data.objects[name];assert not o.modifiers
  before=geometry_signature(o);m=o.data;normals=[list(n.vector) for n in m.corner_normals];indices=[];before_deviation=[]
  for p in m.polygons:
   if p.area<.025:continue
   indices.append(p.index)
   before_deviation.extend(math.degrees(p.normal.angle(Vector(normals[k]))) for k in p.loop_indices)
   p.use_smooth=False
   for k in p.loop_indices:normals[k]=list(p.normal)
  assert len(indices)>=2
  m.normals_split_custom_set(normals);m.update()
  after_deviation=[math.degrees(m.polygons[i].normal.angle(m.corner_normals[k].vector)) for i in indices for k in m.polygons[i].loop_indices]
  assert max(after_deviation)<.02,(name,after_deviation)
  assert before==geometry_signature(o),'Optical repair changed physical geometry'
  # Identical geometric/shading normals must give identical reflected directions.
  reflection_error=0
  for i in indices:
   p=m.polygons[i]
   for direction in [Vector((.2,-.8,-.3)).normalized(),Vector((-.7,.3,.2)).normalized(),Vector((.5,.6,-.4)).normalized()]:
    ideal=direction.reflect(p.normal)
    for k in p.loop_indices:reflection_error=max(reflection_error,(ideal-direction.reflect(m.corner_normals[k].vector)).length)
  assert reflection_error<1e-6,(name,reflection_error)
  o['revision99_r8_optics']='Planar optical-face normals; beveled edge geometry and normals retained'
  rows.append(dict(object=name,opticalFaceIndices=indices,maxCornerDeviationBeforeDeg=max(before_deviation),maxCornerDeviationAfterDeg=max(after_deviation),maxReflectedVectorError=reflection_error,physicalGeometryUnchanged=True))
 return rows

def apply():
 report=dict(topology=topology(),mirrors=optical(),scope='Three mesh closures and two planar optical mirrors only',videoRendered=False)
 bpy.context.view_layer.update();return report

if __name__=='__main__':
 source=Path(bpy.data.filepath);sha=hashlib.sha256(source.read_bytes()).hexdigest();assert sha=='9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e'
 a=apply();one={n:geometry_signature(bpy.data.objects[n]) for n in TOPO+MIRRORS};b=apply();two={n:geometry_signature(bpy.data.objects[n]) for n in TOPO+MIRRORS};assert one==two
 out=R/'review99/r8_optics';out.mkdir(exist_ok=True);a.update(sourceSHA256=sha,idempotent=True,reapplication=b)
 bpy.context.preferences.filepaths.save_version=0;dest=R/'output/Casa_de_Campo_99_R8_optics_preview.blend';bpy.ops.wm.save_as_mainfile(filepath=str(dest),compress=True);a['outputSHA256']=hashlib.sha256(dest.read_bytes()).hexdigest();assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
 (out/'patch_checks.json').write_text(json.dumps(a,indent=2,ensure_ascii=False),encoding='utf-8');print('R8_OPTICS_TOPOLOGY_PASS',json.dumps(a,ensure_ascii=True),flush=True)
