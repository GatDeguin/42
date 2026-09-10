import fs from 'node:fs';
let f='docs/preview95/photographic.js',s=fs.readFileSync(f,'utf8');
s=s.replace('const raster=()=>composer.render();',`const areaLights=lights.filter(l=>l.isRectAreaLight),rasterLightLimit=8;
 function rasterSubset(){
  const selected=new Set(areaLights.slice().sort((a,b)=>{const score=l=>l.position.distanceToSquared(camera.position)+(Math.abs(l.position.y-camera.position.y)>2?80:0);return score(a)-score(b);}).slice(0,rasterLightLimit));
  for(const l of areaLights)l.visible=selected.has(l);
 }
 const restoreLights=()=>{for(const l of lights)l.visible=true;};
 const raster=()=>{rasterSubset();try{composer.render();}finally{restoreLights();}};`);
s=s.replace('sourceLights:lights.length,loadMilliseconds','sourceLights:lights.length,rasterAreaLightLimit:rasterLightLimit,loadMilliseconds');
s=s.replace('await renderer.compileAsync(scene,camera);metrics.rasterCompileMs', 'rasterSubset();try{await renderer.compileAsync(scene,camera);}finally{restoreLights();}metrics.rasterCompileMs');
s=s.replace(' textures,prepareMesh(o)', ` groundGeometry(){const shape=new THREE.Shape();shape.moveTo(-1500,-1500);shape.lineTo(1500,-1500);shape.lineTo(1500,1500);shape.lineTo(-1500,1500);shape.closePath();const hole=new THREE.Path();hole.moveTo(0,0);hole.lineTo(22,0);hole.lineTo(22,-20);hole.lineTo(0,-20);hole.closePath();shape.holes.push(hole);return new THREE.ShapeGeometry(shape);},
  textures,prepareMesh(o)`);
fs.writeFileSync(f,s);
f='web-tools/photographic95-build.mjs';s=fs.readFileSync(f,'utf8');
s=s.replace("'new THREE.PlaneGeometry(3000,3000)'","'photo.groundGeometry()'");
s=s.replace('ground.material.map.repeat.set(750,750);ground.rotation.x=-Math.PI/2;', 'ground.material.map.repeat.set(.25,.25);ground.material.normalMap=ground.material.normalMap.clone();ground.material.normalMap.repeat.set(.25,.25);ground.rotation.x=-Math.PI/2;');
s=s.replace("js=js.replace('color:0x8f9b79'", "js=js.replace('ground.position.set(11,-.20,10)','ground.position.set(0,-.20,0)');\njs=js.replace('color:0x8f9b79'");
fs.writeFileSync(f,s);
