import fs from 'node:fs';import sharp from 'sharp';import {Document,NodeIO} from '@gltf-transform/core';import {ALL_EXTENSIONS} from '@gltf-transform/extensions';import {copyToDocument} from '@gltf-transform/functions';import {MeshoptEncoder,MeshoptDecoder} from 'meshoptimizer';
await Promise.all([MeshoptEncoder.ready,MeshoptDecoder.ready]);const io=new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({'meshopt.encoder':MeshoptEncoder,'meshopt.decoder':MeshoptDecoder});
const dest='docs/preview99/assets/mobile-test/';fs.mkdirSync(dest,{recursive:true});
for(const [name,path] of [['reference','house.gltf'],['candidate','mobile/house.gltf']]){
 const source=await io.read('docs/preview99/assets/'+path),doc=new Document(),node=source.getRoot().listNodes().find(n=>n.getExtras().label==='BOT95 | árbol 00');
 for(const ext of source.getRoot().listExtensionsUsed())doc.createExtension(ext.constructor).setRequired(ext.isRequired());
 const copy=copyToDocument(doc,source,[node]).get(node);doc.createScene().addChild(copy);
 for(const t of doc.getRoot().listTextures())t.setImage(await sharp(Buffer.from(t.getImage())).resize({width:512,height:512,fit:'inside',withoutEnlargement:true}).png().toBuffer()).setMimeType('image/png');
 await io.write(dest+name+'.glb',doc);
}
