"""R8 strict35-A2 emission. Read-only Blender sources; never publishes to docs.
python scripts/planos99_emit_r8.py --model output/MODEL.blend --expected-sha SHA --out planos95/EMISSION [--preview]
"""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,shutil,re,os
ROOT=Path(__file__).resolve().parent.parent
for envname in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[envname]='4'
ap=argparse.ArgumentParser();ap.add_argument('--model',required=True);ap.add_argument('--expected-sha',required=True);ap.add_argument('--out',required=True);ap.add_argument('--preview',action='store_true');ap.add_argument('--reuse-geometry',action='store_true');ap.add_argument('--use-evidence');a=ap.parse_args()
model=(ROOT/a.model).resolve();out=(ROOT/a.out).resolve();expected=a.expected_sha.lower()
if not re.fullmatch('[0-9a-f]{64}',expected):raise ValueError('Expected SHA256 must contain64 hexadecimal characters')
actual=hashlib.sha256(model.read_bytes()).hexdigest()
if actual!=expected:raise RuntimeError('R8 source SHA mismatch; no output generated')
if ROOT not in out.parents or ROOT/'docs' in out.parents:raise ValueError('Output must be an isolated local candidate outside docs')
if 'preview' in model.name.lower() and not a.preview:raise ValueError('A preview source requires --preview')
status='PREVIEW LOCAL R8 / PRUEBA DE GENERADOR / SIN APROBACION9,9' if a.preview else 'R8 EN REVISION / SIN APROBACION9,9 / SIN CALCULO DE CAPACIDAD'
def run(name,*args):
 print('R8_EMIT',name,flush=True);subprocess.run([sys.executable,str(ROOT/'scripts'/name),*map(str,args)],cwd=ROOT,check=True)
out.mkdir(parents=True,exist_ok=True);evdir=out/'use_evidence';evdir.mkdir(exist_ok=True)
if a.use_evidence:
 ev=(ROOT/a.use_evidence).resolve();q=json.loads(ev.read_text('utf8'));geo=json.loads((ev.parent/'geometry.json').read_text('utf8'))
 if q['sha256']!=expected or geo['sha256']!=expected or q['status']!='PASS':raise RuntimeError('Use evidence SHA/status mismatch')
 for src,dst in [(ev,evdir/'use_validation.json'),(ev.parent/'geometry.json',evdir/'geometry.json')]:
  if src.resolve()!=dst.resolve():shutil.copy2(src,dst)
else:
 subprocess.run([r'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-t','4','-b',str(model),'--python',str(ROOT/'scripts/planos99_uso_r8_check.py'),'--','--out',str(evdir),'--expected-sha',expected],cwd=ROOT,check=True)
q=json.loads((evdir/'use_validation.json').read_text('utf8'))
if q.get('sha256')!=expected or q.get('status')!='PASS':raise RuntimeError('Use geometry failed or does not match source; drawing generation stopped')
subprocess.run([r'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-t','4','-b',str(model),'--python',str(ROOT/'scripts/planos99_service_access_probe.py'),'--','--out',str(out/'service_access_proposal.json'),'--expected-sha',expected],cwd=ROOT,check=True)
b=['--model',model,'--out',out,'--status',status]
if a.reuse_geometry:b.append('--reuse-geometry')
run('planos95_build.py',*b)
g=json.loads((out/'geometry.json').read_text('utf8'))
if g['sha256']!=expected or not g.get('scene_metadata',{}).get('r8_uso_details'):raise RuntimeError('Source lacks R8 use correction or extraction SHA mismatch')
run('planos95_details_build.py','--geometry',out/'geometry.json','--out',out/'details','--bearing-details',ROOT/'review95/bearing_details_3c.json','--revision','R8','--status',status,'--use-evidence',evdir/'use_validation.json')
run('planos95_verify.py','--out',out);run('planos99_document_audit.py','--out',out)
base=json.loads((out/'manifest.json').read_text('utf8'));details=json.loads((out/'details/manifest.json').read_text('utf8'));ids=[s['id'] for s in base['sheets']+details['sheets']]
assert len(ids)==35 and len(set(ids))==35 and ids[-2:]==['D13','D14']
result={'revision':'R8','status':status,'preview':a.preview,'model':str(model),'source_sha256':expected,'preserved_general_sheets':len(base['sheets']),'preserved_detail_sheets':len(details['sheets'])-2,'added_sheets':['D13','D14'],'pages':35,'validation_files':['package_validation.json','dimensional_audit.json','print_validation.json','details/validation.json'],'evidence':'use_evidence/use_validation.json','source_unchanged':True,'not_published':True}
(out/'r8_emission.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf8')
run('planos95_package.py','--out',out,'--details',out/'details')
check=json.loads((out/'package_validation.json').read_text('utf8'));assert check['pages']==35
assert hashlib.sha256(model.read_bytes()).hexdigest()==expected,'Model changed during emission'
print(json.dumps(dict(result,checks=check),ensure_ascii=False,indent=2))
