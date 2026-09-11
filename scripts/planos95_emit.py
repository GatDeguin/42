"""Emit a coherent architectural set from one frozen model (PDF/SVG/DXF).
Run: python scripts/planos95_emit.py --model output/MODEL.blend --out planos95/EMISSION --expected-sha SHA
"""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parent.parent
p=argparse.ArgumentParser();p.add_argument('--model',required=True);p.add_argument('--out',required=True);p.add_argument('--expected-sha');p.add_argument('--status',default='EN REVISION / MODELO COORDINADO');p.add_argument('--reuse-geometry',action='store_true');a=p.parse_args()
model=(ROOT/a.model).resolve();out=(ROOT/a.out).resolve();sha=hashlib.sha256(model.read_bytes()).hexdigest()
if a.expected_sha and a.expected_sha.lower()!=sha:raise RuntimeError('Frozen input SHA mismatch')
if ROOT not in out.parents:raise ValueError('Output must remain in project workspace')
def run(script,*args):
 print('PLANOS95',script,flush=True);subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],cwd=ROOT,check=True)
build=['--model',model,'--out',out,'--status',a.status]
if a.reuse_geometry:build.append('--reuse-geometry')
run('planos95_build.py',*build)
run('planos95_details_build.py','--geometry',out/'geometry.json','--out',out/'details','--bearing-details',ROOT/'review95/bearing_details_3c.json')
run('planos95_verify.py','--out',out)
if json.loads((out/'geometry.json').read_text('utf8')).get('scene_metadata',{}).get('r7_vent_details'):run('planos99_document_audit.py','--out',out)
run('planos95_package.py','--out',out,'--details',out/'details')
assert hashlib.sha256(model.read_bytes()).hexdigest()==sha,'Source modified while emitting'
report=json.loads((out/'package_validation.json').read_text(encoding='utf8'));print(json.dumps({'model':str(model),'sha256':sha,'complete_pdf':str(out/'Casa_de_Campo_Planos_Completos_95_A2.pdf'),'checks':report},ensure_ascii=False,indent=2))
