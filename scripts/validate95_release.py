"""Validate one public candidate: geometry, doors, plans, photographs and source hashes."""
from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parents[1];D=R/'docs'
def j(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
model=R/'output/Casa_de_Campo_95_R6K.blend';s=sha(model)
dim=j(D/'preview95/dimension-verification.json');plans=j(D/'planos/manifest.json');pics=j(D/'renders/manifest.json');doors=j(R/'review95/r6k_furniture_door_checks.json')
checks={
'glb_dimensions_match_source':dim['pass'] and dim['sourceSHA256']==s,
'glb_bytes_match_checked_export':dim['glbSHA256']==sha(D/'preview95/assets/house.glb'),
'glb_under_github_single_file_limit':(D/'preview95/assets/house.glb').stat().st_size<100*1024**2,
'plans_share_model':plans['model_sha256']==s,
'photographs_share_model':pics['source_sha256']==s and len(pics['images'])==19,
'door_sweeps_share_model':doors['sha256']==s and doors['all_pass'],
'original_model_unchanged':sha(R/'output/Casa_de_Campo_Final.blend')=='58223d78f71dc0c1d4f33034aaaf0be96a1bd420f72f2231468003e942c2bbfe',
'photos_match_manifest':all(sha(D/'renders'/i['file'])==i['sha256'] for i in pics['images']),
'public_pdf_present':(D/'planos/Casa_de_Campo_Planos_A2.pdf').stat().st_size>100000,
'editable_plans_present':(D/'planos/Casa_de_Campo_Planos_Editables.zip').stat().st_size>100000,
'root_uses_candidate': 'preview95/' in (D/'index.html').read_text(encoding='utf8')
}
report={'version':'R6K','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'model_sha256':s,'glb_sha256':dim['glbSHA256'],'pdf_sha256':sha(D/'planos/Casa_de_Campo_Planos_A2.pdf'),'status':'EN REVISION · aprobación integral9.5 pendiente','video':'PAUSADO HASTA APROBACION EXPLICITA','checks':checks,'all_pass':all(checks.values()),'doors':13,'still_images':19,'known_pending':['Pool water volume extends approximately114mm into basin bottom; correction pending, recorded in A08.','Independent global9.5/photographic approval pending.'],'limits':'Digital geometry and publication checks, not structural, hydraulic, acoustic or municipal certification.'}
(D/'release.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2));assert report['all_pass'],'Public release validation failed'
