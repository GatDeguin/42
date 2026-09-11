"""Prepare an explicit, byte-identified publication inventory. Does not stage or push."""
from pathlib import Path
import json,hashlib,ast
R=Path(__file__).resolve().parents[1];OUT=R/'review99/github_r8_progress';OUT.mkdir(exist_ok=True,parents=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=set('''.gitattributes README.md docs/index.html docs/preview99/index.html docs/avance-r7/index.html output/Casa_de_Campo_99_R8.blend audit/r8_three_passes.md scripts/integrate99_r8.py scripts/integrate99_r8a.py scripts/finish99_metadata_r8.py scripts/correcciones99_agua_optica_r8.py scripts/correcciones99_camara_pileta_r8.py scripts/correcciones99_cesped_r8.py scripts/correcciones99_optica_topologia_r8.py scripts/correcciones99_san_mecanica_r8.py scripts/correcciones99_tapizados_r8.py scripts/correcciones99_textiles_botanica_r8.py scripts/correcciones99_uso_r8.py scripts/correcciones99_uv_madera_r8.py scripts/check99_san_mecanica_r8.py scripts/proof99_san_mecanica_r8.py scripts/check99_cesped_r8.py scripts/check99_r8_pool_camera.py scripts/check99_r8_textile_reapply.py scripts/rebuild99_duvet_r8.py scripts/render99_final_stills.py scripts/verify99_r8_components.py scripts/publish99_r8_checkpoint.py scripts/prepare99_r8_publication.py scripts/verify99_r8_publication_live.py web-tools/r8-progress-qa.mjs scripts/assets/r8/blanket-drape-cache.json review99/r8_checkpoint/visual_review.json review99/r8_checkpoint/stills/manifest.json'''.split())
files.update((R/'review99/r8_publisher/stable_source_paths.txt').read_text('utf8').splitlines())
for pattern in ['docs/avance-r8/**/*','review99/r8_integrated/*.json','review99/r8_integrated/san8/*.json','source/assets/grass_bermuda_01/**/*']:
 files.update(p.relative_to(R).as_posix() for p in R.glob(pattern) if p.is_file())
for folder,names in {
 'source/assets/terlenka':['terlenka_diff_2k.png','terlenka_nor_gl_2k.png','terlenka_rough_2k.png'],
 'source/photographic99_grass_r8':['atlas_manifest.json','lot_color.jpg','lot_normal.png','lot_rough.png','bermuda_source_normal_2k.png','bermuda_source_rough_2k.png','provenance.json'],
 'review99/r8_san':['REVISION_MECANICA_SAN8.md','validation.json','continuous_and_sections.json','construction.json','secciones_mecanismo.svg'],
 'review99/r8_cesped':['REVISION_CESPED_R8.md','delivery.json','validation.json','roughness_only_proof.json'],
 'review99/r8_uso':['README.md','use_validation.json','scope_validation.json','dimension_validation.json'],
 'review99/r8_visual':['pool_visual_review.json','pool_water_render.json','pool_camera.json','textiles_idempotence.json','upholstery_checks.json'],
 'review99/r8_optics':['patch_checks.json','wood_uv_checks.json'],
 'review99/github_r8_progress':['README.md','local-ui/report.json'],
 'review99/r8_publisher':['stable_source_paths.txt','handoff_manifest.json']
}.items():files.update(folder+'/'+name for name in names)
files={f.strip().replace(chr(92),'/') for f in files if f.strip()}
files={f for f in files if not ('/regressions_' in f and not json.loads((R/f).read_text('utf8')).get('passed'))}
assert all((R/f).is_file() for f in files),[f for f in files if not (R/f).is_file()]
assert not any(f.endswith(('.log','.npy','.blend1')) for f in files)
assert not any('preview99/photographic.js' in f or 'preview99/assets' in f for f in files)
for f in files:
 if f.endswith('.py'):ast.parse((R/f).read_text(encoding='utf-8-sig'))
manifest=json.loads((R/'docs/avance-r8/manifest.json').read_text('utf8'))
assert sha(R/'output/Casa_de_Campo_99_R8.blend')==manifest['sourceSHA256']
rows=[dict(path=f,bytes=(R/f).stat().st_size,sha256=sha(R/f)) for f in sorted(files)]
report=dict(scope='R8 integrated Blender, four images,35 coordinated plans and explicitly identified evidence. Does not promote R8 web runtime or claim independent9.9 approval.',sourceSHA256=manifest['sourceSHA256'],files=rows,fileCount=len(rows),bytes=sum(r['bytes'] for r in rows),videoRendered=False)
path=OUT/'publication_inventory.json';path.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8');files.add(path.relative_to(R).as_posix())
(OUT/'stage_paths.bin').write_bytes(b'\0'.join(f.encode('utf8') for f in sorted(files))+b'\0')
print(json.dumps(dict(fileCount=len(files),bytes=report['bytes'],sourceSHA256=report['sourceSHA256']),indent=2))
