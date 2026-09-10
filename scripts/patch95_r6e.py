from pathlib import Path
p=Path(r'D:\2026\42\scripts\correcciones95_ensambles_r6.py')
s=p.read_text(encoding='utf8')
tag='# One replacement top with one hole, correctly positioned between cabinet partitions.'
s=s.replace(tag,"# Retire eight old solid metal strips superseded by manufactured SL95 seals.\nfor side in ['A','B']:\n for part in ['superior','inferior','izquierdo','derecho']:remove('Corrediza posterior '+side+' Burlete '+part)\n"+tag)
p.write_text(s,encoding='utf8')
