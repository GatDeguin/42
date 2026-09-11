"""Reopen the exact checkpoint and prove mesh equivalence to its checked door source."""
import bpy, json, hashlib, runpy, numpy as np
from pathlib import Path
ROOT=Path(r'D:\2026\42');OUT=ROOT/'review99/github_progress'
manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf8'))
path=Path(bpy.data.filepath);assert hashlib.sha256(path.read_bytes()).hexdigest()==manifest['outputSHA256']
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
def snapshot():
 rows={}
 for o in bpy.context.scene.objects:
  if o.type!='MESH':continue
  m=o.data;v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);f=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',f)
  rows[o.name]=dict(mesh=hashlib.sha256(v.tobytes()+f.tobytes()).hexdigest(),matrix=[round(float(v),7) for row in o.matrix_world for v in row],materials=[m.name if m else None for m in o.data.materials],modifiers=[(m.name,m.type) for m in o.modifiers],hide_render=o.hide_render)
 return rows
checkpoint=snapshot();scenes=[dict(name=s.name,objects=len(s.objects),sameObjects=set(s.objects)==set(S.objects),videoPaused=bool(s.get('video_render_requires_explicit_approval'))) for s in bpy.data.scenes]
assert all(s['sameObjects'] and s['videoPaused'] for s in scenes)
images=[im for im in bpy.data.images if im.source=='FILE'];unpacked=[im.name for im in images if not im.packed_file];assert not unpacked
rigs=sorted(o.name for o in S.objects if o.name.startswith('DOOR |'));assert len(rigs)==13 and 'DOOR | suiteEntry' not in rigs
assert all('DOOR | '+k in rigs for k in ['bedroomDining','bedroomLink','bathLink','bathDining','bathroomMono'])
route=json.loads((ROOT/'review99/tour_route.json').read_text(encoding='utf8'))
qa=runpy.run_path(str(ROOT/'scripts/correcciones99_recorrido.py'))['verify'](route,str(OUT/'tour_reopened.json'),False);assert qa['passed']
bpy.ops.wm.open_mainfile(filepath=manifest['base']);bpy.context.scene.frame_set(1);bpy.context.view_layer.update();base=snapshot()
changed=[n for n in checkpoint.keys()&base.keys() if checkpoint[n]!=base[n]]
missing=sorted(base.keys()-checkpoint.keys());added=sorted(checkpoint.keys()-base.keys())
assert not changed and not missing and not added,(changed,missing,added)
proof=ROOT/'docs/avance-r7/acceso-dormitorio.png';original=ROOT/'review99/door_hands/access_camera/preview.png'
report=dict(source=str(path),sourceSHA256=manifest['outputSHA256'],geometryComparedWith=manifest['base'],comparisonSHA256=manifest['baseSHA256'],geometryEquivalence=dict(meshes=len(checkpoint),changed=changed,missing=missing,added=added,method='Base mesh positions/topology, frame1 world matrices, material assignments, modifier names/types and render visibility. Only added camera, prepared camera route and scene memberships/metadata differ.'),scenes=scenes,packedFileImages=len(images),unpacked=unpacked,doorRigs=rigs,routePassed=True,routeRays=qa['rays'],proofImageSHA256=hashlib.sha256(proof.read_bytes()).hexdigest(),proofIdentical=proof.read_bytes()==original.read_bytes(),passed=True,videoRendered=False,scope='Checkpoint preservation and stated camera-ray controls; no global photographic/architectural approval.')
(OUT/'reopen_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print('CHECKPOINT_REOPEN_PASS',report['sourceSHA256'],len(checkpoint),flush=True)