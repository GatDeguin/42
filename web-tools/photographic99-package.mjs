// Split the optimized glTF into independent resources below GitHub's per-file limit.
// Geometry and texture bytes retain their existing precision. No simplification/recoding.
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import assert from 'node:assert/strict';
import {NodeIO} from '@gltf-transform/core';import {ALL_EXTENSIONS} from '@gltf-transform/extensions';import {MeshoptEncoder,MeshoptDecoder} from 'meshoptimizer';
await Promise.all([MeshoptEncoder.ready,MeshoptDecoder.ready]);
const dir='docs/preview99/assets/',input=dir+'house.glb',entry='house.gltf',hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const info=JSON.parse(fs.readFileSync(dir+'model-info.json'));
const io=new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({'meshopt.encoder':MeshoptEncoder,'meshopt.decoder':MeshoptDecoder});
const doc=await io.read(input),textureChecks=[];
for(const [i,b] of doc.getRoot().listBuffers().entries())b.setURI('geometry-'+i+'.bin');
for(const t of doc.getRoot().listTextures()){
 const bytes=Buffer.from(t.getImage()),sha=hash(bytes),ext={'image/png':'png','image/jpeg':'jpg','image/webp':'webp'}[t.getMimeType()];assert(ext,t.getMimeType());
 const uri='textures99/'+sha+'.'+ext;t.setURI(uri);textureChecks.push({name:t.getName(),uri,sha256:sha,bytes:bytes.length});
}
await io.write(dir+entry,doc);
const json=JSON.parse(fs.readFileSync(dir+entry));fs.writeFileSync(dir+entry,JSON.stringify(json));
for(const b of json.buffers)assert(b.uri||b.extensions?.EXT_meshopt_compression?.fallback===true,'Unresolved buffer URI');
const uris=[entry,...json.buffers.filter(b=>b.uri).map(b=>b.uri),...json.images.map(i=>i.uri)];assert(uris.every(u=>u&&!u.includes('..')&&!u.includes(':')));
const files=[...new Set(uris)].map(uri=>{const b=fs.readFileSync(dir+uri);assert(b.length<100*1024*1024,uri);return{uri,bytes:b.length,sha256:hash(b)}});
for(const t of textureChecks){const f=files.find(f=>f.uri===t.uri);assert.equal(f.sha256,t.sha256);assert.equal(f.bytes,t.bytes)}
const report={sourceSHA256:info.stats.source_sha256,sourceModel:info.stats.source_model,entrypoint:entry,originalGLBSHA256:hash(fs.readFileSync(input)),originalGLBBytes:fs.statSync(input).size,files,totalBytes:files.reduce((s,f)=>s+f.bytes,0),maxFileBytes:Math.max(...files.map(f=>f.bytes)),textureBytesPreserved:true,textureChecks,geometryValidationPending:true,scope:'Resource packaging only. Validate decoded source dimensions separately; the standalone GLB is not a Pages asset.'};
info.assets={...(info.assets||{}),model:entry};info.webPackage={entrypoint:entry,sourceSHA256:report.sourceSHA256,manifest:'web-package.json',totalBytes:report.totalBytes};info.stats.standaloneGLBBytes=report.originalGLBBytes;info.stats.downloadBytes=report.totalBytes;
info.downloads={...(info.downloads||{}),glb:process.env.PHOTO99_GLB_DOWNLOAD_URL||null};
fs.writeFileSync(dir+'web-package.json',JSON.stringify(report,null,2));fs.writeFileSync(dir+'model-info.json',JSON.stringify(info,null,2));
console.log('WEB_PACKAGE_READY',JSON.stringify({files:files.length,totalBytes:report.totalBytes,maxFileBytes:report.maxFileBytes,sourceSHA256:report.sourceSHA256}));