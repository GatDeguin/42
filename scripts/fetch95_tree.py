from pathlib import Path
import json,urllib.request,hashlib,concurrent.futures
root=Path(r'D:\2026\42');data=json.loads((root/'review95/tree_small_02_files.json').read_text(encoding='utf-8-sig'));item=data['blend']['2k']['blend'];out=root/'source/assets/tree_small_02';out.mkdir(parents=True,exist_ok=True)
jobs=[('tree_small_02_2k.blend',item)]+list(item['include'].items())
def get(pair):
 rel,info=pair;p=out/rel;p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():urllib.request.urlretrieve(info['url'],p)
 actual=hashlib.md5(p.read_bytes()).hexdigest()
 if actual!=info['md5']:raise RuntimeError('Asset checksum failed: '+rel)
 return {'file':rel,'bytes':p.stat().st_size,'md5':actual,'url':info['url']}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:results=list(ex.map(get,jobs))
manifest={'asset':'Tree Small02','creator':'Rico Cilliers','source':'https://polyhaven.com/a/tree_small_02','license':'CC0','purpose':'Architectural visualization vegetation; source tree centres and canopy envelope retained, species illustrative','files':results}
(out/'provenance.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
print('DOWNLOADED_AND_VERIFIED',len(results),sum(r['bytes'] for r in results))
