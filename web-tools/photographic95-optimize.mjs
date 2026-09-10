import {addDoorPartMotion} from './photographic95-door-parts.mjs';
import fs from 'node:fs';
import sharp from 'sharp';
import {NodeIO} from '@gltf-transform/core';
import {ALL_EXTENSIONS} from '@gltf-transform/extensions';
import {dedup,prune,weld,meshopt} from '@gltf-transform/functions';
import {MeshoptEncoder,MeshoptDecoder} from 'meshoptimizer';
await MeshoptEncoder.ready;
const io=new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({'meshopt.encoder':MeshoptEncoder,'meshopt.decoder':MeshoptDecoder});
const document=await io.read('web-tools/.cache/photographic95/house-raw.glb');
for(const m of document.getRoot().listMaterials())if(m.getName().includes('tree_small_02_leaves'))m.setAlphaMode('MASK').setAlphaCutoff(.4).setDoubleSided(true);
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
await document.transform(dedup(),prune(),weld(),meshopt({encoder:MeshoptEncoder,level:'high',quantizePosition:16}));
const textureRecodes=[];
await Promise.all(document.getRoot().listTextures().map(async t=>{
 const input=t.getImage();if(t.getMimeType()!=='image/png'||input.byteLength<8000000)return;
 const original=Buffer.from(input),metadata=await sharp(original).metadata();if(metadata.depth!=='ushort')return;
 const output=await sharp(original).png({compressionLevel:9}).toBuffer();
 const [before,after]=await Promise.all([sharp(original).raw().toBuffer(),sharp(output).raw().toBuffer()]);
 if(!before.equals(after))throw new Error('Texture recode changed decoded 8-bit pixels: '+t.getName());
 if(output.byteLength<original.byteLength){t.setImage(output);textureRecodes.push({name:t.getName(),before:original.byteLength,after:output.byteLength,width:metadata.width,height:metadata.height,decoded8bitPixelEquality:true});}
}));
fs.writeFileSync('docs/preview95/assets/texture-recoding.json',JSON.stringify(textureRecodes,null,2));
console.log('TEXTURE_RECODE',textureRecodes);
await io.write('docs/preview95/assets/house.glb',document);
const info=JSON.parse(fs.readFileSync('docs/preview95/assets/model-info.json','utf8'));
addDoorPartMotion(document,info);
info.gi={enabled:false,reason:'No source-matched GI approved for this publication'};info.stats.positionQuantizationBits=16;info.stats.sceneCount=document.getRoot().listScenes().length;info.stats.downloadBytes=fs.statSync('docs/preview95/assets/house.glb').size;info.stats.webNodes=document.getRoot().listNodes().length;info.stats.grassTrianglesBefore=grassBefore;info.stats.grassTrianglesAfter=grassAfter;
fs.writeFileSync('docs/preview95/assets/model-info.json',JSON.stringify(info,null,2));
console.log('OPTIMIZED_GLB',info.stats);

