import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import sharp from 'sharp';
const assets='docs/preview99/assets',info=JSON.parse(fs.readFileSync(assets+'/model-info.json'));
const entry=process.argv[2]||info.assets?.mobile?.model||info.assets.model,dir=path.dirname(path.join(assets,entry));
const g=JSON.parse(fs.readFileSync(path.join(assets,entry))),tri=m=>m.primitives.reduce((s,p)=>s+g.accessors[p.indices??p.attributes.POSITION].count/3,0);
let textureBytes=0,maxTexture=0;for(const image of g.images){const m=await sharp(path.join(dir,image.uri)).metadata();textureBytes+=m.width*m.height*4*4/3;maxTexture=Math.max(maxTexture,m.width,m.height);}
const files=[entry,...g.buffers.filter(b=>b.uri).map(b=>path.relative(assets,path.join(dir,b.uri))),...g.images.map(i=>path.relative(assets,path.join(dir,i.uri)))];
const bytes=[...new Set(files)].reduce((s,p)=>s+fs.statSync(path.join(assets,p)).size,0);
const sceneTriangles=g.nodes.reduce((s,n)=>s+(n.mesh==null?0:tri(g.meshes[n.mesh])),0);
const decodedBytes=g.bufferViews.filter(v=>v.extensions?.EXT_meshopt_compression).reduce((s,v)=>s+v.byteLength,0);
const report={entry,bytes,sceneTriangles,textureBytes:Math.round(textureBytes),maxTexture,decodedBytes};
fs.mkdirSync('review99/r8_mobile',{recursive:true});fs.writeFileSync('review99/r8_mobile/budget-'+(entry.includes('mobile')?'mobile':'baseline')+'.json',JSON.stringify(report,null,2));console.log(report);
assert(bytes<=30*1024*1024,'Mobile model exceeds 30 MiB download budget');assert(sceneTriangles<=3_000_000,'Mobile scene exceeds 3 million triangles');assert(textureBytes<=85*1024*1024,'Mobile textures exceed 85 MiB RGBA/mipmap budget');assert(maxTexture<=512,'Mobile model contains textures larger than 512px');assert(decodedBytes<=64*1024*1024,'Mobile compressed geometry expands beyond 64 MiB');
