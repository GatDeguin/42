import fs from 'node:fs';const file='docs/preview95/photographic.js';let s=fs.readFileSync(file,'utf8');
s=s.replace('async warmup(){const begin=performance.now();rasterSubset();try{await renderer.compileAsync(scene,camera);}finally{restoreLights();}metrics.rasterCompileMs=performance.now()-begin;}',`async warmup(){
   const begin=performance.now(),visible=new THREE.Group(),empty=new THREE.Scene(),planes=renderer.clippingPlanes;
   scene.updateMatrixWorld(true);scene.traverseVisible(o=>{if(o.isMesh)visible.add(o.clone(false));});
   rasterSubset();
   try{
    for(const clipping of [[],[new THREE.Plane(new THREE.Vector3(0,-1,0),4.5)]]){
     renderer.clippingPlanes=clipping;renderer.render(empty,camera);
     await renderer.compileAsync(visible,camera,scene);
    }
   }finally{renderer.clippingPlanes=planes;renderer.render(empty,camera);restoreLights();}
   metrics.rasterCompileMs=performance.now()-begin;metrics.precompiledMeshes=visible.children.length;
  }`);
fs.writeFileSync(file,s);
