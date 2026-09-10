import fs from 'node:fs';import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..'),three=path.join(import.meta.dirname,'node_modules','three');
const copy=(from,to)=>{fs.mkdirSync(path.dirname(to),{recursive:true});fs.copyFileSync(from,to);};
for(const file of ['three.module.js','three.core.js'])copy(path.join(three,'build',file),path.join(root,'docs','vendor',file));
copy(path.join(three,'LICENSE'),path.join(root,'docs','vendor','THREE-LICENSE.txt'));
for(const file of ['controls/OrbitControls.js','loaders/GLTFLoader.js','utils/BufferGeometryUtils.js','environments/RoomEnvironment.js','libs/meshopt_decoder.module.js'])copy(path.join(three,'examples','jsm',file),path.join(root,'docs','vendor','addons',file));
for(const name of ['fabric','paver','poolTile','cement','brick'])copy(path.join(root,'source','textures',name+'_albedo.png'),path.join(root,'docs','assets','textures',name+'_albedo.png'));
console.log('Local Three.js runtime and source maps copied.');
