"""Build a still gallery from a frozen, source-verified render manifest."""
import argparse,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--source',default='review99/r7_final/stills');ap.add_argument('--out',default='docs/renders99');ap.add_argument('--expected-sha',required=True);ap.add_argument('--revision',default='R7D');ap.add_argument('--count',type=int,default=25);args=ap.parse_args()
assert re.fullmatch(r'R[0-9]+[A-Z]?',args.revision) and args.count>0
src=(ROOT/args.source).resolve();out=(ROOT/args.out).resolve();assert out.is_relative_to(ROOT/'docs')
manifest=json.loads((src/'manifest.json').read_text(encoding='utf8'))
assert manifest['sourceSHA256']==args.expected_sha
assert hashlib.sha256(Path(manifest['source']).read_bytes()).hexdigest()==args.expected_sha
assert len(manifest['images'])==args.count and len({r['key'] for r in manifest['images']})==args.count
for row in manifest['images']:assert hashlib.sha256((src/row['file']).read_bytes()).hexdigest()==row['sha256'],row['key']
code=(ROOT/'scripts/publish95_gallery.py').read_text(encoding='utf-8-sig')
code=code.replace("src=ROOT/'review95/r6k_stills';out=ROOT/'docs/renders'",'src=SOURCE_DIR;out=DEST_DIR')
code=code.replace("assert len(r['images'])==19",f"assert len(r['images'])=={args.count}")
code=code.replace("r['source_model']","Path(r['source']).name").replace("r['source_sha256']","r['sourceSHA256']")
code=code.replace('R6K',args.revision).replace('19 imágenes',f'{args.count} imágenes').replace('9,5','9,9').replace('Fotografías del modelo','Imágenes del modelo').replace('../planos/','../avance-r8/planos/' if args.revision=='R8' else '../planos99/')
# Keep replaced image URLs separate from earlier cached revisions.
code=code.replace("x['file']", "(x['file']+'?v='+x['sha256'][:16])")
if args.revision=='R8':
 code=code.replace('En revisión · aprobación global 9,9 pendiente','R8 · 26 imágenes publicadas')

exec(compile(code,str(ROOT/'scripts/publish95_gallery.py'),'exec'),dict(__file__=str(ROOT/'scripts/publish95_gallery.py'),__name__='__main__',SOURCE_DIR=src,DEST_DIR=out))
