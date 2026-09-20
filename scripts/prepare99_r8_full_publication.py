"""Curated complete R8 deployment inventory; ignores historical local intermediates."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1];out=R/'review99/r8_final';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
release=json.loads((out/'release.json').read_text('utf8'));assert release['stills']==26 and release['plans']==35
files=set('''.gitattributes README.md audit/r8_three_passes.md docs/index.html docs/preview99/index.html docs/preview99/README.md docs/preview99/controles.html docs/preview99/viewer.js docs/preview99/photographic.js docs/avance-r7/index.html docs/avance-r8/index.html docs/avance-r8/manifest.json output/Casa_de_Campo_99_R8.glb scripts/publish99_r8_full.py scripts/finish99_r8_site.py scripts/prepare99_r8_full_publication.py scripts/publish99_gallery.py scripts/web99_adapt_export.py web-tools/photographic99-optimize.mjs web-tools/photographic99-package.mjs web-tools/r8-deployment-load.mjs review99/r8_final/release.json review99/r8_final/stills/manifest.json'''.split())
assets=R/'docs/preview99/assets';pkg=json.loads((assets/'web-package.json').read_text('utf8'))
files.update('docs/preview99/assets/'+f['uri'] for f in pkg['files'])
for name in ['model-info.json','optics.json','source-envelopes.json','texture-recoding.json','view-bindings.json','web-package.json','botanical-lod.json','leaf-lod.json']:files.add('docs/preview99/assets/'+name)
for folder in ['docs/renders99','docs/renders-r7d','docs/avance-r8/planos']:
 files.update(p.relative_to(R).as_posix() for p in (R/folder).rglob('*') if p.is_file())
for p in (R/'review99/r8_integrated').glob('*.json'):
 if p.name.startswith('regressions_') and not json.loads(p.read_text('utf8')).get('passed'):continue
 files.add(p.relative_to(R).as_posix())
for p in (R/'review99/r8_integrated/san8').glob('*.json'):files.add(p.relative_to(R).as_posix())
if (out/'local-load.json').exists():files.add('review99/r8_final/local-load.json')
assert all((R/f).is_file() for f in files),[f for f in files if not (R/f).is_file()]
assert 'docs/preview99/assets/house.glb' not in files and 'docs/preview99/assets/geometry-0.bin' not in files
assert not any('/gi/' in f for f in files),'Do not publish old static atlases'
rows=[{'path':f,'bytes':(R/f).stat().st_size,'sha256':sha(R/f)} for f in sorted(files)]
for q in rows:assert q['bytes']<100*1024*1024 or q['path']=='output/Casa_de_Campo_99_R8.glb',q['path']
manifest={'revision':'R8','sourceSHA256':release['sourceSHA256'],'files':rows,'fileCount':len(rows),'bytes':sum(q['bytes'] for q in rows),'noNewArchitecturalReview':True,'videoRendered':False}
mp=out/'publication_inventory.json';mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),'utf8');files.add(mp.relative_to(R).as_posix())
(out/'stage_paths.bin').write_bytes(b'\0'.join(s.encode('utf8') for s in sorted(files))+b'\0');print(json.dumps({'files':len(files),'bytes':manifest['bytes']},indent=2))
