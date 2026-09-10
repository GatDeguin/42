"""Independent measurements of candidate95; never saves or changes the blend file."""
import bpy,os,json,math,hashlib,sys,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
def cv(p):return Vector((p[0],-p[2],p[1]))
def geometry(o):
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=e.to_mesh()
 p=[e.matrix_world@v.co for v in me.vertices];f=[list(v.vertices) for v in me.polygons]
 e.to_mesh_clear()
 if not p:return None
 a=np.array(p);return (a.min(0),a.max(0),BVHTree.FromPolygons(p,f))
def intersect(a,b):
 if a is None or b is None:return 0
 if not np.all(np.minimum(a[1],b[1])-np.maximum(a[0],b[0])>.0005):return 0
 return len(a[2].overlap(b[2]))
def bbox(o):
 a=np.array([o.matrix_world@Vector(v) for v in o.bound_box]);return a.min(0),a.max(0)
checks=[]
def check(name,passed,data):checks.append({'name':name,'pass':bool(passed),'measured':data})
treads=sorted([o for o in S.objects if o.name.startswith('Peldaño exterior ') and '|' not in o.name],key=lambda o:bbox(o)[1][2])
tops=[float(bbox(o)[1][2]) for o in treads]
risers=np.diff([.06]+tops)
check('18 risers equal from +0.06 to +3.25',len(tops)==18 and max(abs(risers-(3.25-.06)/18))<.0001,{'tops':tops,'risers':list(risers),'going':3.8/18,'slope_deg':math.degrees(math.atan((3.25-.06)/3.8))})
a,b=bbox(bpy.data.objects['AC95 | acabado descanso al umbral'])
check('Landing highest finish matches studio threshold',abs(b[2]-3.25)<.0001,{'landing_bounds':[list(a),list(b)]})
for ceiling,floor,h in [('Cielorraso estudio | cota inferior 6.45m',3.25,3.2),('Cielorraso vivienda | 2.60m sobre piso general',3.25,2.6),('Cielorraso baño | 2.60m sobre porcelanato',3.25 if 'bath_dining_layout95' in S else 3.3,2.6)]:
 a,b=bbox(bpy.data.objects[ceiling]);check(ceiling,abs(a[2]-floor-h)<.0001,{'underside':float(a[2]),'clear':float(a[2]-floor)})
new=[o for o in S.objects if o.type=='MESH' and o.name.startswith(('PL95 |','AC95 |','FIX95 |'))]
ng={o.name:geometry(o) for o in new}
for name,z,low,outlet in [('PL95 | canaleta frontal abierta',-.08,6.895,13.8),('PL95 | canaleta posterior abierta',12.08,6.295,21.78)]:
 ob=bpy.data.objects[name];g=ng[name];results=[]
 for x in [14.5,17.,20.,21.5]:
  bottom=low+abs(x-outlet)*.005+.0012
  hit,normal,index,dist=g[2].ray_cast(cv([x,bottom+.20,z]),Vector((0,0,-1)),.25)
  results.append({'x':x,'expected_bottom':bottom,'first_surface':float(hit.z) if hit else None,'pass':hit is not None and abs(hit.z-bottom)<.00015})
 check(name+' open receiving channel',all(r['pass'] for r in results),results)
 # Direct vertical opening at the drain, through both the gutter bottom and downpipe throat.
 hit,_,_,dist=g[2].ray_cast(cv([outlet,low+.03,z]),Vector((0,0,-1)),.08)
 check(name+' outlet open',hit is None,{'hit':list(hit) if hit else None})
for nm,a,b in [
 ('T main', [12.96,-.49353,.7],[12.60,-.55,.7]),
 ('T branch', [12.96,-.49353,.7],[12.60,-.55,.7])]:
 obname='PL95 | colector enterrado de jardín' if 'main' in nm else 'PL95 | enlace cámara frontal'
 start,end=cv(a),cv(b);vec=end-start;hit,_,_,dist=ng[obname][2].ray_cast(start,vec.normalized(),vec.length-.0001)
 check(nm+' unobstructed centerline at junction',hit is None,{'hit':list(hit) if hit else None})
# New collectors vs real structural and enclosure meshes. Intended sleeves/chamber connectors are excluded here.
tokens=['muro','tabique','medianera','fachada','losa','cielorraso','cabio','correa','viga','pilar','columna','cimiento','zapata','cubierta pendiente','balcón posterior','recrecido']
targets=[o for o in S.objects if o.type=='MESH' and not o.hide_render and not o.parent and not o.name.startswith(('PL95 |','AC95 |','FIX95 |')) and any(t in o.name.lower() for t in tokens)]
tg={o.name:geometry(o) for o in targets}
pipes=[o for o in new if any(v in o.name for v in ['bajada frontal continua','bajada posterior continua','colector enterrado','enlace cámara'])]
hits=[]
for p in pipes:
 for o in targets:
  n=intersect(ng[p.name],tg[o.name])
  if n:hits.append({'new':p.name,'other':o.name,'face_pairs':n})
check('Downpipes/collector versus structure and enclosure',not hits,hits)
# Check the genuine new geometry against moving leaves, handles, rollers; final known driver states included.
dh=[]
rigs=[o for o in S.objects if o.name.startswith('DOOR | ')]
for fr in sorted(set(list(range(1,151,5))+[105,150])):
 S.frame_set(fr);bpy.context.view_layer.update()
 for rig in rigs:
  for o in rig.children_recursive:
   if o.type!='MESH':continue
   go=geometry(o)
   for n in new:
    count=intersect(go,ng[n.name])
    if count:dh.append({'frame':fr,'rig':rig.name,'part':o.name,'new':n.name,'face_pairs':count})
check('Every moving door part versus new construction',not dh,dh)
S.frame_set(1)
source=os.path.join(ROOT,'output','Casa_de_Campo_Final.blend')
sourcehash=hashlib.sha256(open(source,'rb').read()).hexdigest()
check('Audited source remains unchanged',sourcehash=='58223d78f71dc0c1d4f33034aaaf0be96a1bd420f72f2231468003e942c2bbfe',sourcehash)
result={'model':bpy.data.filepath,'sha256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),'checks':checks,'all_pass':all(c['pass'] for c in checks),'scope':'Geometric coordination only. No structural capacity, hydraulic sizing, acoustical performance or municipal compliance certification.'}
outname=sys.argv[sys.argv.index('--out')+1] if '--out' in sys.argv else 'construccion_checks.json'
json.dump(result,open(os.path.join(ROOT,'review95',outname),'w',encoding='utf8'),ensure_ascii=False,indent=2,default=lambda o:o.item() if hasattr(o,'item') else str(o))
print(json.dumps({'all_pass':result['all_pass'],'checks':[(c['name'],c['pass']) for c in checks],'structure_hits':hits,'door_hits_count':len(dh),'door_hits_sample':dh[:15]},ensure_ascii=False),flush=True)
