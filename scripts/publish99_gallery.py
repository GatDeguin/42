"""Prepare a source-verified R7 still gallery in isolation from the published R6K gallery."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--source',default='review99/r7_final/stills');ap.add_argument('--out',default='docs/renders99');ap.add_argument('--expected-sha',required=True);args=ap.parse_args()
src=(ROOT/args.source).resolve();out=(ROOT/args.out).resolve();assert out.is_relative_to(ROOT/'docs')
manifest=json.loads((src/'manifest.json').read_text(encoding='utf8'))
assert manifest['sourceSHA256']==args.expected_sha
assert hashlib.sha256(Path(manifest['source']).read_bytes()).hexdigest()==args.expected_sha
assert len(manifest['images'])==25 and len({r['key'] for r in manifest['images']})==25
for row in manifest['images']:
 assert hashlib.sha256((src/row['file']).read_bytes()).hexdigest()==row['sha256'],row['key']
code=(ROOT/'scripts/publish95_gallery.py').read_text(encoding='utf-8-sig')
code=code.replace("src=ROOT/'review95/r6k_stills';out=ROOT/'docs/renders'",'src=SOURCE_DIR;out=DEST_DIR')
code=code.replace("assert len(r['images'])==19","assert len(r['images'])==25")
code=code.replace("r['source_model']","Path(r['source']).name").replace("r['source_sha256']","r['sourceSHA256']")
code=code.replace('R6K','R7').replace('19 imágenes','25 imágenes').replace('9,5','9,9').replace('Fotografías del modelo','Imágenes del modelo')
# The gallery may be reviewed before it replaces the public R6K bundle.
code=code.replace('<p>Imágenes calculadas desde el modelo arquitectónico R7.','<p>Imágenes calculadas desde el modelo arquitectónico R7 en revisión. La nota integral y el hiperrealismo fotográfico exigido siguen pendientes. El visor principal y los planos indican su propia revisión. ')
exec(compile(code,str(ROOT/'scripts/publish95_gallery.py'),'exec'),dict(__file__=str(ROOT/'scripts/publish95_gallery.py'),__name__='__main__',SOURCE_DIR=src,DEST_DIR=out))