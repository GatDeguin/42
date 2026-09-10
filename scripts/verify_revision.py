import bpy,os,sys,json,math,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'review');sys.path.insert(0,os.path.join(ROOT,'scripts'));S=bpy.context.scene
D=json.load(open(os.path.join(ROOT,'source','scene.json'),encoding='utf8'));ROUTE=json.load(open(os.path.join(ROOT,'output','tour_route.json'),encoding='utf8'))['shots']
def cv(p):return Vector((p[0],-p[2],p[1]))
def bounds(o):
 p=np.array([o.matrix_world@Vector(v) for v in o.bound_box]);return p.min(0),p.max(0)
def bvh(o):
 dg=bpy.context.evaluated_depsgraph_get();e=o.evaluated_get(dg);me=e.to_mesh();tree=BVHTree.FromPolygons([o.matrix_world@v.co for v in me.vertices],[list(p.vertices) for p in me.polygons]);e.to_mesh_clear();return tree
S.frame_set(1);bpy.context.view_layer.update()
O={i:o for i,o in enumerate(S.objects) if ' | banda antideslizante' not in o.name}
rigs={o.name.split(' | ',1)[1]:o for o in S.objects if o.name.startswith('DOOR | ')}
from validate_scene import validate
report=validate({'S':S,'DATA':D,'OBJS':O,'RIGS':rigs,'CAM':{o.name:o for o in S.objects if o.type=='CAMERA'},'TOUR':bpy.data.objects['TOUR | Recorrido virtual'],'ROUTE':ROUTE,'cv':cv,'corrections':json.loads(S['corrections'])})
checks=[]
def ck(n,p,m=None):checks.append({'name':n,'pass':bool(p),'measured':m})
S.frame_set(150);bpy.context.view_layer.update()
# Reproduce evaluated mesh tests for all moving assemblies across27poses.
exec(compile(open(os.path.join(ROOT,'scripts','verify_coordination.py'),encoding='utf8').read(),'verify_coordination.py','exec'),{})
coord=json.load(open(os.path.join(OUT,'coordinated_mesh_checks.json'),encoding='utf8'))
ck('All movable door meshes avoid walls across27sampledposes (evaluated BVH)',not coord['all_door_leaf_wall_intersections'],coord['all_door_leaf_wall_intersections'])
ck('Extraction pipes avoid evaluated enclosure and structural meshes',not coord['pipe_structure_intersections'],coord['pipe_structure_intersections'])
primary={k:[o for o in e.children if o.type=='MESH'] for k,e in rigs.items()}
# Panel meshes no longer intersect; their AABBs may overlap because of the cut shapes.
S.frame_set(1);bpy.context.view_layer.update()
ac=[o for o in S.objects if o.name.startswith(('Bafle cielorraso estudio','Cloud estudio'))]
over=[]
for i,a in enumerate(ac):
 ba=bvh(a)
 for b in ac[i+1:]:
  p0,p1=bounds(a);q0,q1=bounds(b)
  if np.all(np.minimum(p1,q1)-np.maximum(p0,q0)>.001):
   intersect=ba.overlap(bvh(b))
   if intersect:over.append([a.name,b.name,len(intersect)])
ck('Acoustic meshes do not intersect',not over,over)
# Real pipe triangles are checked against sanitary fixtures, worktops and wardrobe/bed.
pipes=[o for o in S.objects if o.name.startswith('Extracción ') and o.type=='MESH']
fixtures=[o for o in S.objects if o.type=='MESH' and any(t in o.name.lower() for t in ['bañera','inodoro','bidet','placard','cocina lineal','mesada baño','panel acústico lateral'])]
bad=[]
for pipe in pipes:
 pa,pb=bounds(pipe);bp=bvh(pipe)
 for f in fixtures:
  a,b=bounds(f)
  if np.all(np.minimum(pb,b)-np.maximum(pa,a)>.001):
   pairs=bp.overlap(bvh(f))
   if pairs:bad.append([pipe.name,f.name,len(pairs)])
ck('Extraction pipes avoid sanitary fixtures and kitchen/wardrobe meshes',not bad,bad)
# Roof and ceiling clearances, both user-defined interior heights.
levels={}
for name,floor in [('Cielorraso estudio | cota inferior 6.45m',3.25),('Cielorraso vivienda | 2.60m sobre piso general',3.25),('Cielorraso baño | 2.60m sobre porcelanato',3.30)]:
 lo,hi=bounds(bpy.data.objects[name]);levels[name]={'floor':floor,'underside':float(lo[2]),'clear':float(lo[2]-floor)}
ck('Studio3.20m / dwelling and bathroom2.60m clear',abs(levels['Cielorraso estudio | cota inferior 6.45m']['clear']-3.2)<.002 and all(abs(v['clear']-2.6)<.002 for k,v in levels.items() if 'estudio' not in k),levels)
rf=bpy.data.objects['Cubierta pendiente Cedro Misionero'];rr=bpy.data.objects['Cubierta pendiente pileta']
ck('Exterior front studio roof stands0.60m above dwelling module',abs(rf.location.z-rr.location.z-.6)<.01,{'front_center':rf.location.z,'rear_center':rr.location.z,'difference':rf.location.z-rr.location.z})
# Camera supplemental origins and source camera retention.
cameras=[]
for key,spec in D['views'].items():
 o=bpy.data.objects['CAM | '+spec['label']];cameras.append({'name':o.name,'error_m':(o.location-cv(spec['p'])).length,'lens_error_mm':abs(o.data.lens-spec['f'])})
ck('All HTML fixed cameras retained',all(c['error_m']<.001 and c['lens_error_mm']<.001 for c in cameras),cameras)
images=[im for im in bpy.data.images if im.source=='FILE' and im.type!='RENDER_RESULT'];ck('All textures and reference images packed',all(im.packed_file for im in images),len(images))
ck('Video generation explicitly paused',S.get('video_render_requires_explicit_approval') is True)
report['checks']+=checks;report['passed']=all(c['pass'] for c in report['checks']);report['review_state']='After three construction/spatial/appearance passes; pending independent critic.';report['continuous_tour_frames']=4206;report['objects']=len(S.objects)
json.dump(report,open(os.path.join(ROOT,'output','validation.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
json.dump({'checks':checks,'bounds':[{'name':o.name,'lo':bounds(o)[0].tolist(),'hi':bounds(o)[1].tolist()} for o in S.objects if o.type=='MESH' and (o in pipes or 'cabio' in o.name or 'cielorraso' in o.name.lower() or 'Patinillo' in o.name or 'Cubierta' in o.name)],'tested_moving_meshes':{k:[o.name for o in v] for k,v in primary.items()}},open(os.path.join(OUT,'revision_checks.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
print('REVISION_CHECKS',report['passed'],'FAILURES',[c for c in report['checks'] if not c['pass']],flush=True)
