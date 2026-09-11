"""Read-only geometry/component regressions on explicitly identified final R8 source."""
import bpy,json,hashlib,sys,time
from pathlib import Path
R=Path(r'D:/2026/42');a=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
expected=a[a.index('--expected-sha')+1];source=Path(bpy.data.filepath);OUT=R/'review99/r8_integrated';OUT.mkdir(parents=True,exist_ok=True)
assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
jobs={
 'geometry':('verify99_frozen_geometry.py','review99/r7d_integrated/frozen_geometry_checks.json','review99/r8_integrated/frozen_geometry_checks.json'),
 'sanitary':('verify99_sanitary_frozen.py','review99/r7d_integrated/sanitary_checks.json','review99/r8_integrated/sanitary_checks.json'),
 'san8':('check99_san_mecanica_r8.py',None,'review99/r8_integrated/san8/validation.json'),
 'san8_continuous':('proof99_san_mecanica_r8.py',None,'review99/r8_integrated/san8/continuous_and_sections.json'),
 'wet':('planos99_wet_check.py','review99/wet_check_r7.json','review99/r8_integrated/wet_check.json'),
 'vent':('planos99_vent_check.py','review99/vent_check_r7.json','review99/r8_integrated/vent_check.json'),
 'vent_self':('planos99_vent_self_check.py','review99/vent_self_check_r7.json','review99/r8_integrated/vent_self_check.json'),
 'door_hands':('validate99_door_hands.py','review99/door_hands/validation.json','review99/r8_integrated/door_hands_check.json')}
selected=a[a.index('--only')+1].split(',') if '--only' in a else list(jobs);assert all(k in jobs for k in selected);rows=[]
for key in selected:
 script,old,new=jobs[key];bpy.ops.wm.open_mainfile(filepath=str(source));p=R/'scripts'/script;code=p.read_text(encoding='utf-8-sig')
 if old:assert old in code;code=code.replace(old,new)
 if key=='sanitary':
  code=code.replace("o.name.startswith('SAN99 |')", "o.name.startswith(('SAN99 |','SAN8 |'))")
  code=code.replace("assert len(objects)==78", "assert len(objects)==234")
  code=code.replace("o.name.startswith('SAN99 | '+label+' ')", "o.name.startswith(('SAN99 | '+label+' ','SAN8 | '+label+' '))")
 if key in ['san8','san8_continuous']:
  code=code.replace("OUT=R/'review99/r8_san'", "OUT=R/'review99/r8_integrated/san8'")
  (OUT/'san8').mkdir(exist_ok=True)
 if key=='san8':
  oldsha="SHA='9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e'";assert oldsha in code;code=code.replace(oldsha,'SHA='+repr(expected))
  gate="if report['pass'] and not quick:";assert code.count(gate)==1;code=code.replace(gate,"if False: # Read-only final-source regression; no preview save")
 started=time.time();exec(compile(code,str(p),'exec'),dict(__name__='__main__',__file__=str(p)))
 q=json.loads((R/new).read_text(encoding='utf-8-sig'));passed=q.get('pass',q.get('passed'));sha=q.get('sha256',q.get('sourceSHA256',q.get('source_sha256',q.get('preview_sha256'))));assert sha==expected,(key,sha);assert passed,(key,new)
 assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
 rows.append({'key':key,'report':new,'sourceSHA256':expected,'scriptSHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'adaptedCodeSHA256':hashlib.sha256(code.encode()).hexdigest(),'seconds':time.time()-started,'passed':True,'adaptation':('R8 sanitary family includes42 retained plus192 new parts in environment, topology and footprint tests; tolerance unchanged.' if key=='sanitary' else 'Output paths/source guard only; SAN8 preview-save branch disabled. Measurement geometry and tolerances unchanged.')})
 (OUT/('regressions_'+'-'.join(selected)+'.json')).write_text(json.dumps({'source':str(source),'sourceSHA256':expected,'checks':rows,'passed':len(rows)==len(selected),'videoRendered':False},ensure_ascii=False,indent=2),'utf8')
 print('R8_COMPONENT_PASS',key,round(rows[-1]['seconds'],1),flush=True)
