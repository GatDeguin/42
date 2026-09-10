from pathlib import Path
p=Path(r'D:\2026\42\scripts\verificar95_recorrido_cuerpo.py');s=p.read_text(encoding='utf8').replace("import bpy,json,math,os,hashlib","import bpy,json,math,os,hashlib,sys")
s=s.replace("r=json.load(open(os.path.join(ROOT,'output','tour_route.json'),encoding='utf8'))","r=json.load(open(os.path.join(ROOT,'review95','r6_tour_route.json') if '--r6' in sys.argv else os.path.join(ROOT,'output','tour_route.json'),encoding='utf8'))")
s=s.replace("'r6_route_body_checks.json'","'r6f_route_body_checks.json' if '--r6' in sys.argv else 'r6_route_body_checks.json'")
p.write_text(s,encoding='utf8')
