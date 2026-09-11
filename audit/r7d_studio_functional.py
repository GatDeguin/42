"""Studio functional heights and knee opening, read-only."""
exec(compile((__import__('pathlib').Path(r'D:\2026\42')/'audit/r7d_studio_probe.py').read_text(encoding='utf-8'),'studio_inventory','exec'))
from mathutils import Vector
from mathutils.bvhtree import BVHTree
selected=[o for o in S.objects if o.type=='MESH' and o.name.startswith(('Consola estudio','Base consola estudio','Controlador estudio','MAT95 | tecla natural','MAT95 | tecla sostenido','MAT95 | pad MIDI','MAT95 | encoder maestro'))]
trees={}
for o in selected:
 e=o.evaluated_get(DG);m=e.to_mesh();v=[e.matrix_world@q.co for q in m.vertices];f=[list(p.vertices) for p in m.polygons];trees[o.name]=BVHTree.FromPolygons(v,f);e.to_mesh_clear()
rays=[]
for x in [18.20,18.4,18.6,18.75]:
 for z in [2.65,3,3.35]:
  hits=[]
  for name,bv in trees.items():
   p,n,idx,d=bv.ray_cast(Vector((x,-z,3.2501)),Vector((0,0,1)),1.5)
   if p is not None:hits.append({'name':name,'h':p.z})
  hits.sort(key=lambda h:h['h'])
  rays.append(dict(x=x,z=z,first=hits[0] if hits else None))
from_front=[]
for h in [3.72,3.80,3.90,3.94]:
 hits=[]
 for name,bv in trees.items():
  p,n,idx,d=bv.ray_cast(Vector((19.1,-3,h)),Vector((-1,0,0)),1.5)
  if p is not None:hits.append({'name':name,'x':p.x,'distance':d})
 hits.sort(key=lambda h:h['distance'])
 from_front.append(dict(h=h,first=hits[0] if hits else None))
report={'sha256':EXPECTED,'floor':3.25,'inventory':[entry(o) for o in selected],'underside_rays':rays,'front_depth_rays':from_front}
(R/'audit/r7d_preliminary/studio_workstation_functional.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
for prefix in ['Controlador estudio','MAT95 | tecla natural','MAT95 | tecla sostenido','MAT95 | pad MIDI','MAT95 | encoder maestro']:
 a=[q for q in report['inventory'] if q['name'].startswith(prefix)]
 if a:print(prefix,len(a),{'x':[min(q['bounds']['x'][0] for q in a),max(q['bounds']['x'][1] for q in a)],'h':[min(q['bounds']['h'][0] for q in a),max(q['bounds']['h'][1] for q in a)]})
print('KNEES',rays,'FRONT',from_front,flush=True)
