"""Read-only evaluated Blender geometry for planos95_build.py. Source axes X,Z,H."""
import bpy,sys,json,os,hashlib
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:];out=args[0]
s=bpy.context.scene;s.frame_set(150);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
objects=[]
for o in s.objects:
 if o.type!='MESH' or o.hide_render:continue
 cs=[c.name for c in o.users_collection]
 bb=[o.matrix_world@Vector(c) for c in o.bound_box]
 lo=[min(p[i] for p in bb) for i in range(3)];hi=[max(p[i] for p in bb) for i in range(3)]
 rec={'name':o.name,'collections':cs,'lo':[lo[0],-hi[1],lo[2]],'hi':[hi[0],-lo[1],hi[2]],'materials':[m.name for m in o.data.materials if m]}
 n=o.name.lower()
 if o.name.startswith('BOT95') or 'REFERENCE' in cs or 'LANDSCAPE' in cs or hi[0]<-1 or lo[0]>23 or hi[1]<-21 or lo[1]>2 or any(k in n for k in ['cielo ','entorno exterior','césped','terreno','calle cedro']):
  objects.append(rec);continue
 eo=o.evaluated_get(dg);me=eo.to_mesh()
 if len(me.vertices)<20000:
  rec['v']=[[round(v,6) for v in (p.x,-p.y,p.z)] for p in [o.matrix_world@v.co for v in me.vertices]]
  rec['f']=[list(p.vertices) for p in me.polygons]
 eo.to_mesh_clear();objects.append(rec)
os.makedirs(os.path.dirname(out),exist_ok=True)
json.dump({'model':bpy.data.filepath,'sha256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),'frame':150,'axes':'source X, source Z, Blender height','objects':objects},open(out,'w',encoding='utf8'),ensure_ascii=False,separators=(',',':'))
print('PLANOS95_EXTRACT',len(objects),out,flush=True)
