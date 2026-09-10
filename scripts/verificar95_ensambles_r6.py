import bpy,os,json,ast,numpy as np,hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
def raw(o):
 e=o.evaluated_get(dg);m=e.to_mesh();v=np.array([e.matrix_world@p.co for p in m.vertices]);f=[list(p.vertices) for p in m.polygons];e.to_mesh_clear();return v,f
def geo(v,f):return(v.min(0),v.max(0),BVHTree.FromPolygons([Vector(x) for x in v],f))
def hits(g,targets):
 rr=[]
 for n,fg in targets.items():
  d=np.minimum(g[1],fg[1])-np.maximum(g[0],fg[0])
  if min(d)>.0001:
   pp=g[2].overlap(fg[2])
   if pp:rr.append([n,len(pp)])
 return rr
r={'source':bpy.data.filepath,'sha256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest()}
targets={o.name:geo(*raw(o)) for o in S.objects if o.type=='MESH' and o.name.startswith('Bajos cocina mono')}
r['sink_carcass_hits']=hits(geo(*raw(bpy.data.objects['Bacha cocina mono'])),targets)
targets={o.name:geo(*raw(o)) for o in S.objects if o.type=='MESH' and o.name.startswith(('Mueble TV','MOB95 | canal retención TV','MOB95 | perfil soporte TV'))}
r['tv_hits']=[]
for side,d in [('izquierda',.76),('derecha',-.76)]:
 for o in [v for v in S.objects if v.type=='MESH' and (v.name in ['MOB95 | frente corredero TV '+side,'MOB95 | uñero frente TV '+side] or v.name.startswith('MOB95 | patín TV '+side))]:
  v,f=raw(o)
  for t in np.linspace(0,1,41):
   vv=v.copy();vv[:,0]+=t*d
   for n,pp in hits(geo(vv,f),targets):r['tv_hits'].append([o.name,n,float(t),pp])
r['obsolete_removed']=all(bpy.data.objects.get(n)==None for n in ['Espejo baño','Frente cocina vivienda 2']+['Frente cocina vivienda detalle '+str(i) for i in range(4)])
json.dump(r,open(r'D:\2026\42\review95\r6e_cabinet_checks.json','w'),indent=2,ensure_ascii=False)
print(json.dumps(r,ensure_ascii=False))
