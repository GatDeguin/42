"""Curate only R7D publication files; never stage unrelated active plan work."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];paths=set()
def add(p):
 p=R/p if isinstance(p,str) else p
 assert p.is_file(),p
 paths.add(p.relative_to(R).as_posix())
for p in ['.gitattributes','README.md','docs/index.html','docs/avance-r7/index.html','output/Casa_de_Campo_99_R7D.blend','output/Casa_de_Campo_99_R7D.glb','scripts/publish99_r7d_progress.py','scripts/curate99_r7d_publication.py','scripts/verify99_r7d_live.py']:add(p)
for p in (R/'docs/avance-r7').glob('*-r7d.jpg'):add(p)
for p in (R/'docs/preview99').iterdir():
 if p.is_file():add(p)
a=R/'docs/preview99/assets';package=json.loads((a/'web-package.json').read_text(encoding='utf-8-sig'))
for item in package['files']:add(a/item['uri'])
for name in ['belfast_sunset_2k.hdr','botanical-lod.json','leaf-lod.json','material-profiles.json','model-info.json','optics-original.json','optics.json','source-envelopes.json','texture-recoding.json','tree-small-02-provenance.json','view-bindings.json','web-package.json']:add(a/name)
for d in ['docs/preview99/assets/textures','docs/preview99/vendor','source/photographic99_pavimento','source/photographic99_luz']:
 for p in (R/d).rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts:add(p)
for d in ['docs/preview99/assets/oak-veneer-01','docs/preview99/assets/red-bricks-04']:
 for p in (R/d).glob('*.json'):add(p)
for p in ['source/assets/brown_mud/provenance.json','source/assets/terlenka/provenance.json']:add(p)
for p in (R/'scripts').glob('correcciones99_*.py'):add(p)
for name in ['integrate99_r7d.py','finish99_metadata.py','sync99_scene_variants.py','verify99_frozen_geometry.py','verify99_integrated_components.py','verify99_sanitary_frozen.py','validate99_door_hands.py','planos99_wet_check.py','planos99_vent_check.py','planos99_vent_self_check.py','planos95_juntas_check.py','preview99_sanitarios_pavimento.py','web99_export.py','web99_adapt_export.py','make99_pavimento_pbr.py','render99_final_stills.py','contacts99_final_stills.py','publish99_gallery.py']:add('scripts/'+name)
for name in ['progress99-r7d-page-qa.mjs','photographic99-optimize.mjs','photographic99-door-parts.mjs','photographic99-package.mjs','photographic99-package-verify.mjs','photographic99-dimensions-verify.mjs','photographic99-checkpoint-ui.mjs','photographic99-final-qa.mjs']:add('web-tools/'+name)
for name in ['integration_manifest','frozen_geometry_checks','component_regressions','sanitary_checks','wet_check','vent_check','vent_self_check','door_hands_check','tour_in_memory']:add('review99/r7d_integrated/'+name+'.json')
for p in (R/'review99/github_r7d_progress').glob('*.json'):add(p)
add('review99/github_r7d_progress/static-ui/page-qa.json');add('review99/github_r7d_progress/README.md');add('review99/github_r7d_progress/local-ui/report.json')
for p in ['audit/r7_progress_three_passes.md','audit/r7_review_requirements.md']:add(p)
add('audit/critica_constructiva_preliminar_r7d.md')
for p in (R/'audit/r7d_preliminary').glob('*.json'):add(p)
rows=[]
for rel in sorted(paths):
 p=R/rel;size=p.stat().st_size
 if size>=100*1024*1024:assert rel.startswith('output/') and p.suffix in ['.blend','.glb'],rel
 rows.append(dict(path=rel,bytes=size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
report=dict(files=rows,totalBytes=sum(x['bytes'] for x in rows),count=len(rows),sourceSHA256=package['sourceSHA256'],note='File list excludes old prototypes, GI under construction, incomplete R7 gallery/plans and unrelated working-tree edits.')
(R/'review99/r7d_publication_files.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('CURATED_R7D_PUBLICATION',len(rows),report['totalBytes'])
