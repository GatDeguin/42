// Mobile derivatives preserve every architectural mesh, transform and door hierarchy.
import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';import sharp from 'sharp';
import {NodeIO} from '@gltf-transform/core';import {ALL_EXTENSIONS,EXTTextureWebP} from '@gltf-transform/extensions';
import {prune,simplifyPrimitive} from '@gltf-transform/functions';import {MeshoptEncoder,MeshoptDecoder,MeshoptSimplifier} from 'meshoptimizer';
import {RGBELoader} from 'three/examples/jsm/loaders/RGBELoader.js';import {FloatType} from 'three';
await Promise.all([MeshoptEncoder.ready,MeshoptDecoder.ready,MeshoptSimplifier.ready]);
const root='docs/preview99/assets/',dest=root+'mobile/',hash=b=>crypto.createHash('sha256').update(b).digest('hex');fs.mkdirSync(dest+'textures',{recursive:true});
const io=new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({'meshopt.encoder':MeshoptEncoder,'meshopt.decoder':MeshoptDecoder});
const info=JSON.parse(fs.readFileSync(root+'model-info.json')),doc=await io.read(root+'house.gltf');
const isVegetation=n=>n.getExtras().category==='LANDSCAPE'&&/^(BOT95 \||Césped botánico|R8B \| Huerta|Paisaje \| pradera)/.test(n.getExtras().label||n.getName());
const nodes=doc.getRoot().listNodes(),protectedMeshes=new Set(nodes.filter(n=>!isVegetation(n)).map(n=>n.getMesh()).filter(Boolean));
const protectedDigest=mesh=>hash(Buffer.concat(mesh.listPrimitives().flatMap(p=>[p.getIndices(),...p.listAttributes()].filter(Boolean).map(a=>Buffer.from(a.getArray().buffer,a.getArray().byteOffset,a.getArray().byteLength)))));
const protectedBefore=new Map([...protectedMeshes].map(m=>[m,protectedDigest(m)]));const changes=[];const visited=new Set();
for(const node of nodes){
 const mesh=node.getMesh();if(!mesh||!isVegetation(node)||protectedMeshes.has(mesh)||visited.has(mesh))continue;visited.add(mesh);
 for(const p of mesh.listPrimitives()){
  const ia=p.getIndices();if(!ia||ia.getCount()<600)continue;
  const before=ia.getCount()/3,target=Math.max(64,Math.floor(before*.012)),indices=ia.getArray(),positions=p.getAttribute('POSITION'),parent=Int32Array.from({length:positions.getCount()},(_,i)=>i);
  function find(i){while(parent[i]!==i){parent[i]=parent[parent[i]];i=parent[i];}return i;}
  for(let i=0;i<indices.length;i+=3){const r=find(indices[i]);parent[find(indices[i+1])]=r;parent[find(indices[i+2])]=r;}
  const components=new Map();for(let i=0;i<indices.length;i+=3){const r=find(indices[i]);if(!components.has(r))components.set(r,[]);components.get(r).push(indices[i],indices[i+1],indices[i+2]);}
  if(components.size>12){
   // Whole disconnected leaves/tufts are sampled evenly; never discard random faces.
   const all=[...components.values()],keepCount=Math.max(8,Math.min(all.length,Math.ceil(all.length*target/before))),kept=[];
   for(let i=0;i<keepCount;i++)kept.push(...all[Math.floor((i+.5)*all.length/keepCount)]);
   const remap=new Map();for(const v of kept)if(!remap.has(v))remap.set(v,remap.size);
   for(const semantic of p.listSemantics()){
    const old=p.getAttribute(semantic),arr=old.getArray(),size=old.getElementSize(),a=new arr.constructor(remap.size*size);
    for(const [from,to] of remap)for(let k=0;k<size;k++)a[to*size+k]=arr[from*size+k];
    p.setAttribute(semantic,doc.createAccessor().setType(old.getType()).setArray(a).setNormalized(old.getNormalized()).setBuffer(old.getBuffer()));
   }
   p.setIndices(doc.createAccessor().setType('SCALAR').setArray(Uint32Array.from(kept,v=>remap.get(v))).setBuffer(ia.getBuffer()));
  }
  const current=p.getIndices().getCount()/3;
  if(current>target*1.1)simplifyPrimitive(p,{simplifier:MeshoptSimplifier,ratio:Math.min(1,target/current),error:.025,lockBorder:false});
  changes.push({name:node.getExtras().label||node.getName(),before,after:p.getIndices().getCount()/3});
 }
}
for(const [m,digest] of protectedBefore)assert.equal(protectedDigest(m),digest,'Architectural geometry changed');
console.log('MOBILE_LANDSCAPE_LOD',changes.length);
doc.createExtension(EXTTextureWebP).setRequired(true);
for(const t of doc.getRoot().listTextures()){
 const b=await sharp(Buffer.from(t.getImage())).resize({width:512,height:512,fit:'inside',withoutEnlargement:true}).webp({quality:86,alphaQuality:95,effort:4}).toBuffer();
 t.setImage(b).setMimeType('image/webp').setURI('textures/'+hash(b)+'.webp');
}
await doc.transform(prune({keepLeaves:true,keepAttributes:true}));
for(const [i,b] of doc.getRoot().listBuffers().entries())b.setURI('geometry-'+i+'.bin');
await io.write(dest+'house.gltf',doc);
const g=JSON.parse(fs.readFileSync(dest+'house.gltf'));for(const b of g.buffers.filter(b=>b.uri)){const bytes=fs.readFileSync(dest+b.uri),uri='geometry-'+hash(bytes)+'.bin';fs.writeFileSync(dest+uri,bytes);b.uri=uri;}fs.writeFileSync(dest+'house.gltf',JSON.stringify(g));
// Smaller copies of the eight wood/finish maps restored by the runtime.
for(const name of ['fabric','paver','poolTile','cement','brick','oak','walnut','parquet'])await sharp('docs/assets/textures/'+name+'_albedo.png').resize({width:256,height:256,fit:'inside',withoutEnlargement:true}).webp({quality:86}).toFile(dest+name+'_albedo.webp');
// Downsample the authored sunset in linear HDR; retain the source lighting direction.
const hdrBytes=fs.readFileSync(root+'belfast_sunset_2k.hdr'),hdr=new RGBELoader().setDataType(FloatType).parse(hdrBytes.buffer.slice(hdrBytes.byteOffset,hdrBytes.byteOffset+hdrBytes.byteLength));
const width=512,height=256,parts=[Buffer.from('#?RADIANCE\nFORMAT=32-bit_rle_rgbe\n\n-Y '+height+' +X '+width+'\n')];
for(let y=0;y<height;y++){
 const row=Buffer.alloc(width*4);
 for(let x=0;x<width;x++){
  const c=[0,0,0];let samples=0;
  for(let sy=Math.floor(y*hdr.height/height);sy<Math.floor((y+1)*hdr.height/height);sy++)for(let sx=Math.floor(x*hdr.width/width);sx<Math.floor((x+1)*hdr.width/width);sx++){for(let k=0;k<3;k++)c[k]+=hdr.data[(sy*hdr.width+sx)*4+k];samples++;}
  for(let k=0;k<3;k++)c[k]/=samples;const max=Math.max(...c),e=max>1e-32?Math.floor(Math.log2(max))+1:0,scale=max>1e-32?256/2**e:0;
  for(let k=0;k<3;k++)row[k*width+x]=Math.min(255,Math.floor(c[k]*scale));row[3*width+x]=scale?e+128:0;
 }
 parts.push(Buffer.from([2,2,width>>8,width&255]));for(let k=0;k<4;k++)for(let x=0;x<width;x+=128){const n=Math.min(128,width-x);parts.push(Buffer.from([n]),row.subarray(k*width+x,k*width+x+n));}
}
fs.writeFileSync(dest+'sunset-512.hdr',Buffer.concat(parts));
const uris=['house.gltf',...g.buffers.filter(b=>b.uri).map(b=>b.uri),...g.images.map(i=>i.uri),'sunset-512.hdr',...['fabric','paver','poolTile','cement','brick','oak','walnut','parquet'].map(n=>n+'_albedo.webp')];
const files=[...new Set(uris)].map(uri=>{const b=fs.readFileSync(dest+uri);return {uri,bytes:b.length,sha256:hash(b)}});
const report={sourceSHA256:info.stats.source_sha256,revision:'R8-mobile-1',entrypoint:'house.gltf',files,totalBytes:files.reduce((s,f)=>s+f.bytes,0),architecturalMeshesUnchanged:protectedMeshes.size,nodesPreserved:nodes.length,landscape:changes};
fs.writeFileSync(dest+'manifest.json',JSON.stringify(report,null,2));
info.assets.mobile={model:'mobile/house.gltf',manifest:'mobile/manifest.json',downloadBytes:report.totalBytes,sourceSHA256:info.stats.source_sha256};fs.writeFileSync(root+'model-info.json',JSON.stringify(info,null,2));
console.log('MOBILE_PACKAGE_READY',JSON.stringify({bytes:report.totalBytes,architecturalMeshesUnchanged:protectedMeshes.size,nodes:nodes.length}));
