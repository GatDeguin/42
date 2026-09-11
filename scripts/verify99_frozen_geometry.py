"""Read-only checks on the frozen integrated candidate; no source save or render."""
import bpy,bmesh,ast,os,json,hashlib,re,math
from pathlib import Path
from array import array
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
ROOT=Path(r'D:\2026\42');S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
# Reuse explicit geometric measurement routines, never the construction script body.
tree_ast=ast.parse((ROOT/'scripts/correcciones99_constructivas_r7.py').read_text(encoding='utf8'))
for n in tree_ast.body:
 if isinstance(n,ast.FunctionDef):exec(compile(ast.Module(body=[n],type_ignores=[]),'<water measurement routines>','exec'))
checks=[]
def ck(name,passed,measured=None):checks.append(dict(name=name,passed=bool(passed),measured=measured))
water=bpy.data.objects['Agua de pileta']
solids=[o for o in S.objects if o.type=='MESH' and o.name.startswith(('Fondo de pileta','Borde pileta','Escalón pileta','Playa húmeda','Nariz playa húmeda','Junta borde pileta','Banda húmeda'))]
assert len(solids)==14
intersections=[dict(solid=o.name,volume_m3=intersection(water,o)) for o in solids]
contacts=pair_contacts(water,solids);metrics=mesh_metrics(water);wb=bounds(water)
ck('Water confined to the 14 basin solids',all(r['volume_m3']<1e-8 for r in intersections),intersections)
ck('Water contact at 72 sampled basin stations',len(contacts)==72 and all(r['pass'] for r in contacts),contacts)
ck('Water is one closed positive volume',metrics['non_manifold_edges']==0 and metrics['connected_components']==1 and metrics['volume_m3']>0,metrics)
pool=bounds(bpy.data.objects['Fondo de pileta'])
ck('Nominal basin 7 x 3 metres',abs(pool['x'][1]-pool['x'][0]-7)<1e-5 and abs(pool['z'][1]-pool['z'][0]-3)<1e-5,pool)
ck('Water surface and basin bottom',abs(wb['y'][1]+.030)<1e-6 and abs(wb['y'][0]+1.390)<1e-6,wb)
datums={}
for label,ceiling,floor in [
 ('studio','Cielorraso estudio | cota inferior 6.45m',3.25),
 ('dwelling','Cielorraso vivienda | 2.60m sobre piso general',3.25),
 ('bathroom','Cielorraso baño | 2.60m sobre porcelanato',bounds(bpy.data.objects['Piso baño vivienda'])['y'][1])]:
 underside=bounds(bpy.data.objects[ceiling])['y'][0];datums[label]=dict(floor=floor,ceiling=underside,clear=underside-floor)
ck('Owner clear heights 3.20 and 2.60 metres',abs(datums['studio']['clear']-3.2)<1e-5 and all(abs(datums[k]['clear']-2.6)<1e-5 for k in ['dwelling','bathroom']),datums)
vents=[o for o in S.objects if o.type=='MESH' and o.name.startswith('VENT99 |')]
vh=min(bounds(o)['y'][0] for o in vents)
ck('New studio ventilation preserves clear height',vh>=6.452,dict(minHeight=vh,clearFromFinishedFloor=vh-3.25))
steps=[o for o in S.objects if re.fullmatch(r'Peldaño exterior [0-9]+',o.name)]
step_rows=[dict(name=o.name,bounds=bounds(o)) for o in sorted(steps,key=lambda o:int(o.name.rsplit(' ',1)[1]))]
ck('18 exterior timber steps, each 1 metre wide',len(steps)==18 and all(abs(r['bounds']['x'][1]-r['bounds']['x'][0]-1)<1e-5 for r in step_rows),step_rows)
landing=bounds(bpy.data.objects['Descanso escalera']);ck('Structural landing 1 x 1 metres',abs(landing['x'][1]-landing['x'][0]-1)<1e-5 and abs(landing['z'][1]-landing['z'][0]-1)<1e-5,landing)
rigs=[o.name for o in S.objects if o.name.startswith('DOOR |')]
ck('Corrected access graph keeps 13 door rigs',len(rigs)==13 and 'DOOR | suiteEntry' not in rigs and all('DOOR | '+k in rigs for k in ['bedroomDining','bedroomLink','bathLink','bathDining','bathroomMono']),rigs)
ck('Metric scale1',S.unit_settings.system=='METRIC' and abs(S.unit_settings.scale_length-1)<1e-8)
files=[im for im in bpy.data.images if im.source=='FILE' and im.type!='RENDER_RESULT'];unpacked=[im.name for im in files if not im.packed_file]
ck('All file-based images packed',not unpacked,dict(count=len(files),unpacked=unpacked))
ck('Scene variants share current geometry',all(set(sc.objects)==set(S.objects) for sc in bpy.data.scenes),[dict(name=sc.name,objects=len(sc.objects)) for sc in bpy.data.scenes])
ck('Video paused in every scene',all(sc.get('video_render_requires_explicit_approval') for sc in bpy.data.scenes))
report=dict(source=bpy.data.filepath,sourceSHA256=hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),checks=checks,passed=all(c['passed'] for c in checks),scope='Dimensional/mesh regression of stated controls. Not structural, statutory, acoustic or hydraulic certification; independent aesthetic audit pending.',videoRendered=False)
out=ROOT/'review99/r7d_integrated/frozen_geometry_checks.json';out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
print('R7_FROZEN_GEOMETRY',report['passed'],[c['name'] for c in checks if not c['passed']],flush=True)
assert report['passed'],'Frozen source checks failed; inspect report'
