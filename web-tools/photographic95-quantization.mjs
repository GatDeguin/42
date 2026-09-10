import fs from 'node:fs';const file='docs/preview95/photographic.js';let s=fs.readFileSync(file,'utf8');
s=s.replace('textures,prepareMesh(o){o.material=Array.isArray(o.material)?o.material.map(material):material(o.material);}',`textures,prepareMesh(o){
   o.material=Array.isArray(o.material)?o.material.map(material):material(o.material);
   // GLB meshopt/quantization is legal for raster. Path tracing merges CPU attributes,
   // so dynamic meshes must be decoded exactly as the static batching path already does.
   if(o.userData.dynamic||Array.isArray(o.material)){
    const geometry=o.geometry.clone();
    for(const [name,a] of Object.entries(geometry.attributes)){
     const values=new Float32Array(a.count*a.itemSize);
     for(let i=0;i<a.count;i++)for(let k=0;k<a.itemSize;k++)values[i*a.itemSize+k]=a.getComponent(i,k);
     geometry.setAttribute(name,new THREE.Float32BufferAttribute(values,a.itemSize));
    }
    o.geometry=geometry;
   }
  }`);
s=s.replace('   await pathTracer.setSceneAsync(scene,camera);',`   await pathTracer.setSceneAsync(scene,camera);
   const expected=new THREE.Box3();scene.traverseVisible(o=>{if(o.isMesh){o.geometry.computeBoundingBox();expected.union(o.geometry.boundingBox.clone().applyMatrix4(o.matrixWorld));}});
   const actual=new THREE.Box3().setFromBufferAttribute(pathTracer._generator.geometry.attributes.position);
   metrics.geometryBounds={expected:{min:expected.min.toArray(),max:expected.max.toArray()},actual:{min:actual.min.toArray(),max:actual.max.toArray()}};
   if(!expected.clone().expandByScalar(.05).containsBox(actual))throw new Error('BVH geometry exceeds visible scene bounds; refusing an invalid light solution.');`);
fs.writeFileSync(file,s);
