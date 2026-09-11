"""List the exact R7D plan publication files; does not stage or commit."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=lambda folder:sorted(p.relative_to(R).as_posix() for p in (R/folder).rglob('*') if p.is_file())
published=files('docs/planos99')
generators=[
 'scripts/planos95_build.py','scripts/planos95_details_build.py','scripts/planos95_emit.py','scripts/planos95_extract.py',
 'scripts/planos95_package.py','scripts/planos95_publish.py','scripts/planos95_verify.py','scripts/planos95_publication.css',
 'scripts/planos99_detail_views.py','scripts/planos99_document_audit.py','scripts/planos99_service_access_probe.py',
 'scripts/planos99_publication_scope.py','web-tools/planos99-publication-qa.mjs']
inputs=['review95/bearing_details_3c.json']
evidence=files('review99/planos99_publication')+['review99/service_access_r7d.json']
selfoutputs=['review99/planos99_publication_files.json','review99/planos99_stage_paths.txt']
paths=sorted(set(published+generators+inputs+evidence+selfoutputs))
for n in paths:
 if n not in selfoutputs:assert (R/n).is_file(),n
report={'model':'output/Casa_de_Campo_99_R7D.blend','model_sha256':'9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e',
'purpose':'Curated plan publication only. No staging, commit or push performed.',
'published_files':published,'generator_files':generators,'additional_required_input_files':inputs,'evidence_files':evidence,'stage_paths':paths,
'existing_inputs_unchanged':['source/scene.json','scripts/planos95_juntas_check.py','output/Casa_de_Campo_99_R7D.blend'],
'excluded_from_this_scope':['docs/planos/ (R6K unchanged)','docs/index.html and viewer files (parent-owned)','docs/renders99/ (parent-owned)','planos95/r7d_candidate/ (duplicate local emission, regenerable from source)','Other agents files and intermediate Blender models','planos95/_vendor/ and runtime dependencies'],
'records':[{'path':n,'bytes':(R/n).stat().st_size,'sha256':sha(R/n)} for n in paths if n not in selfoutputs]}
(R/selfoutputs[0]).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf8')
(R/selfoutputs[1]).write_text('\n'.join(paths)+'\n','utf8')
print(json.dumps({'files':len(paths),'published':len(published),'generators':len(generators),'inputs':len(inputs),'evidence':len(evidence),'list':selfoutputs[1]},indent=2))
