import fs from 'node:fs';
import {NodeIO} from '@gltf-transform/core';
import {ALL_EXTENSIONS} from '@gltf-transform/extensions';
import {dedup,prune,weld,meshopt} from '@gltf-transform/functions';
import {MeshoptEncoder,MeshoptDecoder} from 'meshoptimizer';
await MeshoptEncoder.ready;
const io=new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({'meshopt.encoder':MeshoptEncoder,'meshopt.decoder':MeshoptDecoder});
const document=await io.read('web-tools/.cache/house-raw.glb');
let grassBefore=0,grassAfter=0;
for(const node of document.getRoot().listNodes()){
 if(!(node.getExtras().label||node.getName()).startsWith('Césped botánico'))continue;
 const mesh=node.getMesh();if(!mesh)continue;
 for(const p of mesh.listPrimitives()){
  const ia=p.getIndices();if(!ia)continue;const indices=ia.getArray(),n=p.getAttribute('POSITION').getCount();
  const parent=Int32Array.from({length:n},(_,i)=>i);
  function find(i){while(parent[i]!==i){parent[i]=parent[parent[i]];i=parent[i];}return i;}
  for(let i=0;i<indices.length;i+=3){const r=find(indices[i]);parent[find(indices[i+1])]=r;parent[find(indices[i+2])]=r;}
  const components=new Map();let count=0;const kept=[];
  for(let i=0;i<indices.length;i+=3){const r=find(indices[i]);if(!components.has(r))components.set(r,count++);if(components.get(r)%4===0)kept.push(indices[i],indices[i+1],indices[i+2]);}
  const remap=new Map();for(const v of kept)if(!remap.has(v))remap.set(v,remap.size);
  for(const semantic of p.listSemantics()){
   const old=p.getAttribute(semantic),arr=old.getArray(),size=old.getElementSize(),a=new arr.constructor(remap.size*size);
   for(const [from,to] of remap)for(let k=0;k<size;k++)a[to*size+k]=arr[from*size+k];
   p.setAttribute(semantic,document.createAccessor().setType(old.getType()).setArray(a).setNormalized(old.getNormalized()).setBuffer(old.getBuffer()));
  }
  p.setIndices(document.createAccessor().setType('SCALAR').setArray(Uint32Array.from(kept,v=>remap.get(v))).setBuffer(ia.getBuffer()));
  grassBefore+=indices.length/3;grassAfter+=kept.length/3;
 }
}
console.log('GRASS_TUFT_LOD',grassBefore,grassAfter);
await document.transform(dedup(),prune(),weld(),meshopt({encoder:MeshoptEncoder,level:'high'}));
await io.write('docs/assets/house.glb',document);
const info=JSON.parse(fs.readFileSync('docs/assets/model-info.json','utf8'));
info.stats.downloadBytes=fs.statSync('docs/assets/house.glb').size;info.stats.webNodes=document.getRoot().listNodes().length;info.stats.grassTrianglesBefore=grassBefore;info.stats.grassTrianglesAfter=grassAfter;
fs.writeFileSync('docs/assets/model-info.json',JSON.stringify(info,null,2));
console.log('OPTIMIZED_GLB',info.stats);
