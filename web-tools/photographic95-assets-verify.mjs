import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';
import {NodeIO} from '@gltf-transform/core';import {ALL_EXTENSIONS} from '@gltf-transform/extensions';import {MeshoptDecoder} from 'meshoptimizer';
await MeshoptDecoder.ready;
const dir='docs/preview95/assets/',info=JSON.parse(fs.readFileSync(dir+'model-info.json')),optics=JSON.parse(fs.readFileSync(dir+'optics.json')),lod=JSON.parse(fs.readFileSync(dir+'botanical-lod.json'));
const sha=crypto.createHash('sha256').update(fs.readFileSync(optics.source)).digest('hex');assert.equal(sha,info.stats.source_sha256,'Source Blender changed after export');assert.equal(info.doors.length,13);assert.equal(optics.lights.length,33);assert.equal(lod.length,70);assert(lod.every(o=>o.completeUnits&&o.components.find(c=>c.material.includes('leaves')).webComponents>=4000));assert(lod.filter(o=>o.lod==='foreground').every(o=>o.components.find(c=>c.material.includes('leaves')).webComponents>=16000));
const io=new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({'meshopt.decoder':MeshoptDecoder});const doc=await io.read(dir+'house.glb');
assert.equal(doc.getRoot().listScenes().length,1,'Export should contain only the active architectural scene');
const bath=info.doors.find(d=>d.key==='bathDining');assert(bath,'Missing new dining bathroom door');assert(Math.abs((bath.open.position[0]-bath.closed.position[0])-1.02)<.002,'Bathroom sliding distance differs from source');
const authoredMinerals=optics.materials.filter(m=>m.proceduralFinish);
for(const key of ['whitePlaster','cement','concreteDark']){
 const spec=authoredMinerals.find(m=>m.key===key);assert(spec,'Missing authored mineral '+key);
 const mat=doc.getRoot().listMaterials().find(m=>m.getName().split('|').at(-1).trim()===key);assert(mat,'Missing exported mineral '+key);
 assert(Math.abs(mat.getRoughnessFactor()-spec.roughness)<1e-5,'Roughness mismatch '+key);
 const color=mat.getBaseColorFactor();assert(spec.color.every((v,i)=>Math.abs(v-color[i])<1e-5),'Authored mean colour mismatch '+key);
 assert(!mat.getBaseColorTexture(),'Obsolete macrotexture reintroduced '+key);
}
const trees=[],converted=[],meshes=new Set();let triangles=0;
for(const n of doc.getRoot().listNodes()){
 const name=n.getExtras().label||n.getName(),mesh=n.getMesh();if(!mesh)continue;
 for(const p of mesh.listPrimitives())triangles+=(p.getIndices()?.getCount()||p.getAttribute('POSITION').getCount())/3;
 if(name.startsWith('BOT95 | árbol ')){
  assert(mesh.listPrimitives().every(p=>p.getAttribute('TEXCOORD_0')&&p.getAttribute('NORMAL')),'Missing botanical UV or normals '+name);meshes.add(mesh);
  trees.push({name,primitives:mesh.listPrimitives().map(p=>({triangles:p.getIndices().getCount()/3,attributes:p.listSemantics(),material:p.getMaterial()?.getName()}))});
 }
 if(name.includes(' | web mesh'))converted.push(name);
}
assert.equal(trees.length,70);assert(meshes.size<=2,'Botanical sharing lost');assert(converted.length>20,'Expected converted lettering and curves');
const materials=doc.getRoot().listMaterials().filter(m=>m.getName().includes('tree_small_02')).map(m=>({name:m.getName(),alpha:m.getAlphaMode(),baseTexture:!!m.getBaseColorTexture(),normalTexture:!!m.getNormalTexture(),roughnessTexture:!!m.getMetallicRoughnessTexture(),baseUV:m.getBaseColorTextureInfo()?.getTexCoord(),normalUV:m.getNormalTextureInfo()?.getTexCoord(),roughnessUV:m.getMetallicRoughnessTextureInfo()?.getTexCoord()}));
assert.equal(materials.length,3);assert(materials.every(m=>m.baseTexture&&m.normalTexture&&m.roughnessTexture&&m.baseUV===0&&m.normalUV===0&&m.roughnessUV===0));assert.equal(materials.find(m=>m.name.includes('leaves')).alpha,'MASK');
const photographicWood=doc.getRoot().listMaterials().filter(m=>m.getName().startsWith('PHOTO95 | oak_veneer_01')).map(m=>({name:m.getName(),base:m.getBaseColorFactor(),maps:[m.getBaseColorTexture(),m.getNormalTexture(),m.getMetallicRoughnessTexture()].map(t=>({name:t?.getName(),size:t?.getSize()})),uv:[m.getBaseColorTextureInfo()?.getTexCoord(),m.getNormalTextureInfo()?.getTexCoord(),m.getMetallicRoughnessTextureInfo()?.getTexCoord()]}));
assert(photographicWood.length>=4,'Photographic wood missing');assert(photographicWood.every(m=>m.maps.every(t=>t.size?.[0]===2048)&&m.uv.every(u=>u===0)),'Wood PBR or UV0 lost');
const photographicMasonry=doc.getRoot().listMaterials().filter(m=>m.getName().startsWith('PHOTO95 | red_bricks_04')).map(m=>({name:m.getName(),base:m.getBaseColorFactor(),normalScale:m.getNormalScale(),emissive:m.getEmissiveFactor(),maps:[m.getBaseColorTexture(),m.getNormalTexture(),m.getMetallicRoughnessTexture()].map(t=>({name:t?.getName(),size:t?.getSize()})),uv:[m.getBaseColorTextureInfo()?.getTexCoord(),m.getNormalTextureInfo()?.getTexCoord(),m.getMetallicRoughnessTextureInfo()?.getTexCoord()]}));
assert(photographicMasonry.length>=2,'Photographic masonry missing');assert(photographicMasonry.every(m=>m.maps.every(t=>t.size?.[0]===2048)&&m.maps[0].name?.includes('calibrated')&&m.uv.every(u=>u===0)&&m.emissive.every(v=>v===0)),'Calibrated masonry PBR, UV0 or non-emission lost');
assert(info.viewerViews.some(v=>v.key==='mono'&&v.camera==='REV | Mono distribución'),'Revised mono view missing');assert(info.viewerViews.some(v=>v.key==='bathDining'),'Dining bathroom view missing');assert(info.cameras.find(c=>c.name==='REV | Vestidor circulación').presentationFrame===1,'Vestidor camera frame must be closed');
const wardrobeGarments=doc.getRoot().listNodes().filter(n=>(n.getExtras().label||n.getName()).includes('Vestidor prenda ')&&n.getMesh()).map(n=>n.getExtras().label||n.getName());assert.equal(wardrobeGarments.filter(n=>n.includes('cloth body')).length,7,'Wardrobe garment replacement absent');assert.equal(wardrobeGarments.filter(n=>n.includes('hanger hook')).length,7,'Wardrobe hangers absent');
const garmentMaterials=doc.getRoot().listMaterials().filter(m=>m.getName().startsWith('GAR95 | woven garment'));assert.equal(garmentMaterials.length,7);assert(garmentMaterials.every(m=>m.getNormalTexture()&&m.getNormalTextureInfo().getTexCoord()===0),'Garment normal/UV lost');
const textureFootprint=doc.getRoot().listTextures().map(t=>({name:t.getName(),mime:t.getMimeType(),bytes:t.getImage()?.byteLength||0,size:t.getSize()})).sort((a,b)=>b.bytes-a.bytes);
const result={wardrobeGarments,photographicWood,photographicMasonry,sceneCount:doc.getRoot().listScenes().length,authoredMinerals,textureFootprint,created:new Date().toISOString(),source:optics.source,sha,sourceVerified:true,bytes:fs.statSync(dir+'house.glb').size,doors:info.doors.length,lights:optics.lights.length,environment:optics.environment,triangles,treeObjects:trees.length,sharedTreeMeshes:meshes.size,treeLOD:lod,treeAttributes:trees,convertedObjects:converted,botanicalMaterials:materials,uvNote:'Original UVMap preserved for trunk/leaves; original UV_map_01 copied to UV0 on branch faces with its authored (3,0.6) transform, to support the path tracer single UV channel.'};
fs.writeFileSync('docs/preview95/asset-verification.json',JSON.stringify(result,null,2));console.log('ASSET_VERIFIED',JSON.stringify({sha,triangles,trees:trees.length,sharedTreeMeshes:meshes.size,converted:converted.length,bytes:result.bytes,doors:13,lights:optics.lights.length,environment:optics.environment,materials}));
