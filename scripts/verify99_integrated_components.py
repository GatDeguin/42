"""Read-only component regressions from one frozen R7D source; never save or render."""
import bpy,json,hashlib,sys,time
from pathlib import Path
R=Path(r'D:\2026\42');OUT=R/'review99/r7d_integrated';OUT.mkdir(exist_ok=True)
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
expected=args[args.index('--expected-sha')+1];source=Path(bpy.data.filepath)
assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
jobs=[('sanitary','verify99_sanitary_frozen.py','review99/r7d_integrated/sanitary_checks.json','review99/r7d_integrated/sanitary_checks.json'),('wet','planos99_wet_check.py','review99/wet_check_r7.json','review99/r7d_integrated/wet_check.json'),('vent','planos99_vent_check.py','review99/vent_check_r7.json','review99/r7d_integrated/vent_check.json'),('vent_self','planos99_vent_self_check.py','review99/vent_self_check_r7.json','review99/r7d_integrated/vent_self_check.json'),('door_hands','validate99_door_hands.py','review99/door_hands/validation.json','review99/r7d_integrated/door_hands_check.json')]
if '--only' in args:
 selected=args[args.index('--only')+1].split(',');jobs=[j for j in jobs if j[0] in selected]
rows=[]
for key,script,old,new in jobs:
 bpy.ops.wm.open_mainfile(filepath=str(source));code=(R/'scripts'/script).read_text(encoding='utf-8-sig')
 assert old in code,(key,old);code=code.replace(old,new)
 started=time.time();exec(compile(code,str(R/'scripts'/script),'exec'),dict(__name__='__main__',__file__=str(R/'scripts'/script)))
 result=json.loads((R/new).read_text(encoding='utf8'));passed=result.get('pass',result.get('passed'));sha=result.get('sha256',result.get('sourceSHA256'))
 assert sha==expected,(key,sha);assert passed,(key,new)
 rows.append(dict(key=key,report=new,scriptSHA256=hashlib.sha256((R/'scripts'/script).read_bytes()).hexdigest(),seconds=time.time()-started,passed=True))
 assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
(OUT/'component_regressions.json').write_text(json.dumps(dict(source=str(source),sourceSHA256=expected,checks=rows,passed=True,videoRendered=False),ensure_ascii=False,indent=2),encoding='utf8')
print('R7_COMPONENT_REGRESSIONS_PASS',[r['key'] for r in rows],flush=True)