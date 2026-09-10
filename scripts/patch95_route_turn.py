from pathlib import Path
p=Path(r'D:\2026\42\scripts\correcciones95_recorrido_r6.py');s=p.read_text(encoding='utf8')
s=s.replace("[18.2,4.9,8.35],[18.2,4.9,7.68]","[18.38,4.9,8.35],[18.38,4.9,8.1],[18.28,4.9,7.68]")
s=s.replace("[18.3,4.5,6.45],[16.6,4.3,7.4]","[18.3,4.5,6.45],[18.0,4.4,7.45],[16.6,4.3,7.4]")
p.write_text(s,encoding='utf8')
