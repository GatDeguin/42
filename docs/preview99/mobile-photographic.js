import * as THREE from 'three';
import {RGBELoader,RectAreaLightUniformsLib} from './vendor/photographic-runtime.js';

// Bounded raster pipeline: no BVH, screen-space buffers or geometry expansion.
export async function createPhotographicPipeline({renderer,scene,camera,controls,status}){
 const [optics,hdr]=await Promise.all([fetch('./assets/optics.json',{cache:'no-store'}).then(r=>r.json()),new RGBELoader().setDataType(THREE.HalfFloatType).loadAsync('./assets/mobile/sunset-512.hdr')]);
 hdr.mapping=THREE.EquirectangularReflectionMapping;scene.environment=scene.background=hdr;
 scene.environmentIntensity=scene.backgroundIntensity=optics.environment?.strength??.5;
 scene.environmentRotation.y=scene.backgroundRotation.y=optics.environment?.threeEnvironmentRotationY??Math.PI/4;
 renderer.toneMappingExposure=2**(optics.environment?.exposureEV??0);
 RectAreaLightUniformsLib.init();const locals=[];
 for(const s of optics.lights){
  let l;const color=new THREE.Color().setRGB(...s.color);
  if(s.type==='SUN'){
   l=new THREE.DirectionalLight(color,s.energy);l.position.fromArray(s.position);l.target.position.copy(l.position).add(new THREE.Vector3(...s.direction).multiplyScalar(50));scene.add(l.target);l.castShadow=true;l.shadow.mapSize.set(1024,1024);Object.assign(l.shadow.camera,{left:-34,right:34,top:34,bottom:-34,near:.1,far:160});l.shadow.bias=-.00008;l.shadow.normalBias=.009;
  }else if(s.type==='AREA'){
   const w=Math.max(.03,s.size||.2),h=['RECTANGLE','ELLIPSE'].includes(s.shape)?Math.max(.03,s.sizeY||w):w;l=new THREE.RectAreaLight(color,s.energy/(Math.PI*w*h),w,h);l.position.fromArray(s.position);l.quaternion.fromArray(s.quaternion);locals.push(l);
  }else{l=new THREE.PointLight(color,s.energy/(4*Math.PI),0,2);l.position.fromArray(s.position);locals.push(l);}
  scene.add(l);
 }
 const chooseLights=()=>{const nearest=new Set([...locals].sort((a,b)=>{const score=l=>l.position.distanceToSquared(camera.position)+(Math.abs(l.position.y-camera.position.y)>2?80:0);return score(a)-score(b)}).slice(0,4));for(const l of locals)l.visible=nearest.has(l);};
 controls.addEventListener('change',chooseLights);chooseLights();const materialCache=new Map();
 const metrics={profile:'mobile',sourceLights:optics.lights.length,rasterLocalLightLimit:4,geometryExpansion:false,enabled:false};
 return {
  textures:{},verifySource(sha){if(optics.sourceSHA256!==sha)throw new Error('Optics source mismatch');},
  prepareMesh(o){
   const convert=old=>{if(materialCache.has(old.uuid))return materialCache.get(old.uuid);const m=old.clone(),key=old.name.split('|').at(-1).trim();
    if(['glass','glassInner','water'].includes(key)){m.transparent=true;m.opacity=key==='water'?.62:.15;m.depthWrite=false;if('transmission' in m)m.transmission=0;m.roughness=key==='water'?.12:.08;}
    for(const prop of ['map','normalMap','roughnessMap','metalnessMap'])if(m[prop])m[prop].anisotropy=2;
    materialCache.set(old.uuid,m);return m;};o.material=Array.isArray(o.material)?o.material.map(convert):convert(o.material);
  },
  async warmup(){chooseLights();await renderer.compileAsync(scene,camera);},
  completeSetup(){renderer.shadowMap.autoUpdate=false;renderer.shadowMap.needsUpdate=true;status.textContent='Iluminación optimizada para móvil';},
  invalidate(geometry){if(geometry)renderer.shadowMap.needsUpdate=true;},setEnabled(){},setContact(){},resize(){},get enabled(){return false;},get metrics(){return metrics;},
  render(now,{moving}){if(moving)renderer.shadowMap.needsUpdate=true;renderer.info.reset();renderer.info.autoReset=false;renderer.render(scene,camera);}
 };
}
