import * as THREE from 'three';
import {WebGLPathTracer,DenoiseMaterial,FullScreenQuad,GenerateMeshBVHWorker,RGBELoader,RectAreaLightUniformsLib,EffectComposer,RenderPass,GTAOPass,OutputPass} from './vendor/photographic-runtime.js';

export async function createPhotographicPipeline({renderer,scene,camera,controls,viewport,mobile,status}) {
 const start=performance.now(), textureLoader=new THREE.TextureLoader();
 const [optics,source,hdr]=await Promise.all([
  fetch(new URLSearchParams(location.search).has('previous')?'./assets/optics-original.json':'./assets/optics.json',{cache:'no-store'}).then(r=>r.json()),fetch('./assets/material-profiles.json').then(r=>r.json()),
  new RGBELoader().setDataType(THREE.FloatType).loadAsync('./assets/belfast_sunset_2k.hdr')]);
 hdr.mapping=THREE.EquirectangularReflectionMapping;
 scene.environment=hdr;scene.background=hdr;scene.environmentIntensity=.50;scene.backgroundIntensity=.7;scene.backgroundBlurriness=.06;
 scene.environmentRotation.y=scene.backgroundRotation.y=Math.PI/4;
 if(optics.environment?.type==='HDR'){
  scene.environmentIntensity=scene.backgroundIntensity=optics.environment.strength;
  scene.environmentRotation.y=scene.backgroundRotation.y=optics.environment.threeEnvironmentRotationY;
  renderer.toneMappingExposure=Math.pow(2,optics.environment.exposureEV);
 }
 const authoredMaterials=new Map(optics.materials.filter(m=>m.key).map(m=>[m.key,m]));
 const textures={};
 await Promise.all(Object.entries(source.profiles).map(async([key,profile])=>{
  textures[key]={};
  await Promise.all(['albedo','normal','surface'].map(async(kind)=>{
   const texture=await textureLoader.loadAsync('./assets/textures/'+key+'_'+kind+'.png');
   texture.flipY=false;texture.wrapS=texture.wrapT=THREE.RepeatWrapping;
   texture.minFilter=THREE.LinearMipmapLinearFilter;texture.magFilter=THREE.LinearFilter;
   texture.colorSpace=kind==='albedo'?THREE.SRGBColorSpace:THREE.NoColorSpace;
   texture.repeat.set(1/(.7*profile.tile[0]),1/(.7*profile.tile[1]));
   texture.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());textures[key][kind]=texture;
  }));
 }));
 // Analytic normal field, in metres. This changes only surface optics, not architecture.
 const resolution=256, waveData=new Uint8Array(resolution*resolution*4);
 for(let y=0;y<resolution;y++)for(let x=0;x<resolution;x++){
  const u=x/resolution*Math.PI*2,v=y/resolution*Math.PI*2;
  const dx=.16*Math.cos(u*3+v*2)+.055*Math.cos(u*7-v*5),dy=.12*Math.cos(u*3+v*2)-.045*Math.cos(u*7-v*5);
  const normal=new THREE.Vector3(-dx,-dy,1).normalize(),i=(y*resolution+x)*4;
  waveData[i]=(normal.x*.5+.5)*255;waveData[i+1]=(normal.y*.5+.5)*255;waveData[i+2]=(normal.z*.5+.5)*255;waveData[i+3]=255;
 }
 const wave=new THREE.DataTexture(waveData,resolution,resolution);wave.wrapS=wave.wrapT=THREE.RepeatWrapping;wave.magFilter=THREE.LinearFilter;wave.minFilter=THREE.LinearMipmapLinearFilter;wave.generateMipmaps=true;wave.repeat.set(1.8,1.8);wave.needsUpdate=true;
 RectAreaLightUniformsLib.init();
 const lights=[];
 for(const spec of optics.lights){
  const color=new THREE.Color().setRGB(...spec.color),p=new THREE.Vector3(...spec.position);let light;
  if(spec.type==='SUN'){
   light=new THREE.DirectionalLight(color,spec.energy);light.position.copy(p);
   light.target.position.copy(p).add(new THREE.Vector3(...spec.direction).multiplyScalar(50));scene.add(light.target);
   light.castShadow=true;light.shadow.mapSize.set(mobile?2048:4096,mobile?2048:4096);
   Object.assign(light.shadow.camera,{left:-34,right:34,top:34,bottom:-34,near:.1,far:160});
   light.shadow.bias=-.00008;light.shadow.normalBias=.009;light.shadow.radius=2.2;
  } else if(spec.type==='AREA'){
   const w=Math.max(.03,spec.size||.2),h=spec.shape==='RECTANGLE'||spec.shape==='ELLIPSE'?Math.max(.03,spec.sizeY||w):w;
   // Radiant power / emitting area / pi. Global scale 1 preserves the authored energy ratios.
   light=new THREE.RectAreaLight(color,spec.energy/(Math.PI*w*h),w,h);light.position.copy(p);light.quaternion.fromArray(spec.quaternion);
  } else {
   light=new THREE.PointLight(color,spec.energy/(4*Math.PI),0,2);light.position.copy(p);light.radius=spec.radius||.08;
  }
  light.name=spec.name;light.userData.source=spec;lights.push(light);scene.add(light);
 }
 const materialCache=new Map(),decodedGeometries=new Map(),bakedSurfaces=new Map(),bakedMaterials=new Map(),appliedBakedSurfaces=new Set();
 const bakedUVTextures=new Map();
 function bakeTextureUV0(texture){if(!texture||texture.channel===0)return texture;if(!bakedUVTextures.has(texture.uuid)){const copy=texture.clone();copy.channel=0;copy.needsUpdate=true;bakedUVTextures.set(texture.uuid,copy);}return bakedUVTextures.get(texture.uuid);}
 let bakedTexture=null,bakeReport=null;
 function material(old){
  if(materialCache.has(old.uuid))return materialCache.get(old.uuid);
  const key=old.name.split('|').at(-1).trim();
  const physical=['glass','glassInner','water','fabric','clothWhite','acoustic'].includes(key);
  const m=physical?new THREE.MeshPhysicalMaterial():old.clone();
  if(physical){THREE.MeshStandardMaterial.prototype.copy.call(m,old);m.defines={STANDARD:'',PHYSICAL:''};}
  m.name=old.name+' · óptica R8';m.envMapIntensity=1;
  const definition=source.materials[key];
  const kind=definition?.texture||(key.includes('madera original')?'wood':null);
  const maps=textures[kind];
  if(maps){
   if(!key.includes('madera original')){m.map=maps.albedo;m.color.setRGB(...(definition?.color||[1,1,1]));}
   m.normalMap=maps.normal;m.normalScale.set(.65,.65);m.roughnessMap=maps.surface;m.roughness=1;m.bumpMap=null;
   if(['fabric','acoustic','clothWhite'].includes(kind)){m.sheen=.35;m.sheenRoughness=.85;m.sheenColor.setRGB(.3,.28,.25);}
  }
  const authored=authoredMaterials.get(key);
  if(authored?.proceduralFinish){
   // The source now uses subtle procedural minerals, not the older cloud-textured maps.
   // Preserve its linear mean and measured roughness; submillimetre bump is below this LOD.
   m.map=null;m.normalMap=null;m.roughnessMap=null;m.bumpMap=null;
   m.color.setRGB(...authored.color.slice(0,3));m.roughness=authored.roughness;m.metalness=authored.metalness;
   m.userData.authoredFinish=authored.proceduralFinish;
  }
  if(['glass','glassInner','water'].includes(key)){
   m.transparent=false;m.opacity=1;m.depthWrite=true;m.metalness=0;m.transmission=1;m.ior=key==='water'?1.333:1.52;
   m.thickness=key==='water'?(optics.water?.maxDepthMetres??1.45):.012;m.attenuationColor.setRGB(...(key==='water'?[.24,.74,.79]:[.93,.975,.96]));
   m.attenuationDistance=key==='water'?12:14;m.color.setRGB(.98,.995,.995);m.roughness=key==='water'?.035:.022;
   m.side=THREE.DoubleSide;m.map=null;m.roughnessMap=null;m.normalMap=key==='water'?wave:null;
   if(key==='water'){const strength=.35*(optics.water?.bumpDistanceRatio??1);m.normalScale.set(strength,strength);}
  }
  if(key==='mirror'){m.color.setRGB(.91,.94,.95);m.metalness=1;m.roughness=.025;}
  m.needsUpdate=true;materialCache.set(old.uuid,m);return m;
 }
 const composer=new EffectComposer(renderer,new THREE.WebGLRenderTarget(1,1,{type:THREE.HalfFloatType,samples:mobile?0:2}));
 composer.addPass(new RenderPass(scene,camera));
 const gtao=new GTAOPass(scene,camera,viewport.clientWidth,viewport.clientHeight);
 gtao.updateGtaoMaterial({radius:.26,thickness:1,distanceExponent:1.3,distanceFallOff:1,scale:1,samples:12,screenSpaceRadius:false});
 gtao.blendIntensity=.65;
 const baseOverride=gtao._overrideVisibility.bind(gtao);
 gtao._overrideVisibility=()=>{baseOverride();scene.traverseVisible(o=>{if(o.isMesh&&(Array.isArray(o.material)?o.material:[o.material]).some(m=>m.transmission>0||m.transparent)){o.visible=false;gtao._visibilityCache.push(o);}});};
 composer.addPass(gtao);composer.addPass(new OutputPass());
 const areaLights=lights.filter(l=>l.isRectAreaLight),rasterLightLimit=8;
 function rasterSubset(){
  const selected=new Set(areaLights.slice().sort((a,b)=>{const score=l=>l.position.distanceToSquared(camera.position)+(Math.abs(l.position.y-camera.position.y)>2?80:0);return score(a)-score(b);}).slice(0,rasterLightLimit));
  for(const l of areaLights)l.visible=selected.has(l);
 }
 const restoreLights=()=>{for(const l of lights)l.visible=true;};
 const raster=()=>{rasterSubset();try{composer.render();}finally{restoreLights();}};
 const denoise=new DenoiseMaterial({sigma:2,threshold:.065,kSigma:1});const denoiseQuad=new FullScreenQuad(denoise);
 let pathTracer=null,worker=null,enabled=false,contact=true,complete=false,building=false,sceneDirty=true,lastChange=performance.now(),lastFrame=performance.now(),lastStatus=0,generation=0;
 const metrics={sourceLights:lights.length,rasterAreaLightLimit:rasterLightLimit,loadMilliseconds:performance.now()-start,builds:[],frameIntervals:[],longTasks:[],error:null};
 try{new PerformanceObserver(list=>{for(const e of list.getEntries())metrics.longTasks.push({start:e.startTime,duration:e.duration});}).observe({entryTypes:['longtask']});}catch{}
 function invalidate(geometry=false){lastChange=performance.now();if(geometry){sceneDirty=true;generation++;renderer.shadowMap.needsUpdate=true;}pathTracer?.reset();}
 controls.addEventListener('change',()=>{lastChange=performance.now();pathTracer?.updateCamera();});
 async function rebuild(){
  if(building||!enabled||!complete)return;
  building=true;const version=generation,started=performance.now();status.textContent='Preparando rebotes de luz…';
  try{
   if(!pathTracer){
    pathTracer=new WebGLPathTracer(renderer);worker=new GenerateMeshBVHWorker();pathTracer.setBVHWorker(worker);
    pathTracer.bounces=6;pathTracer.transmissiveBounces=8;pathTracer.filterGlossyFactor=.5;
    pathTracer.tiles.set(3,3);pathTracer.renderScale=mobile?.6:.75;pathTracer.textureSize.set(mobile?512:1024,mobile?512:1024);
    pathTracer.minSamples=32;pathTracer.fadeDuration=350;pathTracer.renderDelay=100;pathTracer.rasterizeSceneCallback=raster;
    pathTracer.dynamicLowRes=false;
    pathTracer.renderToCanvasCallback=(target,r,quad)=>{denoise.map=target.texture;denoise.opacity=quad.material.opacity;denoise.transparent=denoise.opacity<1;denoise.blending=denoise.transparent?THREE.NormalBlending:THREE.NoBlending;const prior=r.autoClear;r.autoClear=false;denoiseQuad.render(r);r.autoClear=prior;};
   }
   await pathTracer.setSceneAsync(scene,camera);
   const expected=new THREE.Box3();scene.traverseVisible(o=>{if(o.isMesh){o.geometry.computeBoundingBox();expected.union(o.geometry.boundingBox.clone().applyMatrix4(o.matrixWorld));}});
   const actual=new THREE.Box3().setFromBufferAttribute(pathTracer._generator.geometry.attributes.position);
   metrics.geometryBounds={expected:{min:expected.min.toArray(),max:expected.max.toArray()},actual:{min:actual.min.toArray(),max:actual.max.toArray()}};
   if(!expected.clone().expandByScalar(.05).containsBox(actual))throw new Error('BVH geometry exceeds visible scene bounds; refusing an invalid light solution.');
   sceneDirty=version!==generation;metrics.builds.push({milliseconds:performance.now()-started,version,triangles:(pathTracer._generator.geometry.index?.count||pathTracer._generator.geometry.attributes.position.count)/3});
   lastChange=performance.now();
  }catch(error){metrics.error=error.stack||error.message;enabled=false;document.getElementById('photo-mode').checked=false;console.error(error);status.textContent='La luz progresiva no está disponible; navegación activa.';}
  finally{building=false;}
 }
 function setEnabled(value){enabled=value;document.getElementById('photo-mode').checked=value;invalidate(false);if(enabled&&sceneDirty&&!building)rebuild();}
 function resize(w,h){composer.setSize(w,h);gtao.setSize(Math.round(w*renderer.getPixelRatio()*.75),Math.round(h*renderer.getPixelRatio()*.75));invalidate(false);}
 resize(viewport.clientWidth,viewport.clientHeight);
 return {
  verifySource(sha){if(optics.sourceSHA256&&optics.sourceSHA256!==sha)throw new Error('Optics and model source SHA differ');},
  groundGeometry(){const shape=new THREE.Shape();shape.moveTo(-1500,-1500);shape.lineTo(1500,-1500);shape.lineTo(1500,1500);shape.lineTo(-1500,1500);shape.closePath();const hole=new THREE.Path();hole.moveTo(0,0);hole.lineTo(22,0);hole.lineTo(22,-20);hole.lineTo(0,-20);hole.closePath();shape.holes.push(hole);return new THREE.ShapeGeometry(shape);},
  async loadBake(loader){
   const [manifest,modelInfo]=await Promise.all([fetch('./gi/manifest.json').then(r=>r.json()),fetch('./assets/model-info.json').then(r=>r.json())]);
   if(manifest.sourceSHA256!==modelInfo.stats.source_sha256){metrics.bakeDisabled='Light atlas belongs to a different source SHA';return;}
   await Promise.all(manifest.regions.map(async entry=>{
    const prefix='./gi/'+entry.region+'/';
    const [gltf,texture,report]=await Promise.all([loader.loadAsync(prefix+'surfaces.glb'),new RGBELoader().setDataType(THREE.HalfFloatType).loadAsync(prefix+(new URLSearchParams(location.search).get('denoise')!=='0'?'irradiance-denoised.hdr':'irradiance.hdr')),fetch(prefix+'bake-report.json').then(r=>r.json())]);
    if(report.sourceSHA256!==manifest.sourceSHA256)throw new Error('Region light atlas source mismatch: '+entry.region);
    texture.channel=1;texture.flipY=false;texture.colorSpace=THREE.LinearSRGBColorSpace;
    gltf.scene.updateMatrixWorld(true);
    gltf.scene.traverse(o=>{if(o.isMesh)bakedSurfaces.set(o.userData.label||o.name,{object:o,texture,region:entry.region});});
   }));
   bakeReport={source:modelInfo.stats.source_model,sourceSHA256:manifest.sourceSHA256,staleSource:false,regions:manifest.regions.map(e=>e.region),scope:'Static full diffuse at closed-door pose; dynamic reflections and approximate door-motion lighting'};
   gtao.blendIntensity=.25;
  },
  textures,prepareMesh(o){
   o.material=Array.isArray(o.material)?o.material.map(material):material(o.material);
   const baked=bakedSurfaces.get(o.userData.label);
   if(baked&&!Array.isArray(o.material)){
    appliedBakedSurfaces.add(o.userData.label);
    o.geometry=baked.object.geometry.clone().applyMatrix4(new THREE.Matrix4().copy(o.matrixWorld).invert().multiply(baked.object.matrixWorld));
    if(!o.geometry.attributes.uv1)throw new Error('Missing UV2 for baked surface '+o.userData.label);
    const lightKey=o.material.uuid+'|'+baked.region;
    if(!bakedMaterials.has(lightKey)){
     const m=o.material.clone();
     for(const key of ['map','normalMap','roughnessMap','metalnessMap','aoMap','emissiveMap','bumpMap','alphaMap','clearcoatMap','clearcoatNormalMap','clearcoatRoughnessMap','sheenColorMap','sheenRoughnessMap','transmissionMap','thicknessMap','specularIntensityMap','specularColorMap'])if(m[key])m[key]=bakeTextureUV0(m[key]);
     m.lightMap=baked.texture;m.lightMapIntensity=Math.PI;
     m.onBeforeCompile=shader=>{shader.fragmentShader=shader.fragmentShader.replace('#include <lights_fragment_maps>',THREE.ShaderChunk.lights_fragment_maps.replace('iblIrradiance += getIBLIrradiance( geometryNormal );','/* Full diffuse is provided by the source-matched atlas. */'));shader.fragmentShader=shader.fragmentShader.replace('#include <lights_fragment_end>','#include <lights_fragment_end>\nreflectedLight.directDiffuse = vec3(0.0);');};
     m.customProgramCacheKey=()=> 'gi-full-diffuse-r7';m.needsUpdate=true;bakedMaterials.set(lightKey,m);
    }
    o.material=bakedMaterials.get(lightKey);
    if(o.material.normalMap){if(!o.geometry.index||!o.geometry.attributes.normal||!o.geometry.attributes.uv)throw new Error('Incomplete photographic tangent basis in GI receiver '+o.userData.label);o.geometry.computeTangents();}
   }
   // GLB meshopt/quantization is legal for raster. Path tracing merges CPU attributes,
   // so dynamic meshes must be decoded exactly as the static batching path already does.
   if(o.userData.dynamic||o.userData.sharedAsset||Array.isArray(o.material)){
    if(decodedGeometries.has(o.geometry.uuid)){o.geometry=decodedGeometries.get(o.geometry.uuid);return;}
    const sourceUUID=o.geometry.uuid;
    const geometry=o.geometry.clone();
    for(const [name,a] of Object.entries(geometry.attributes)){
     const values=new Float32Array(a.count*a.itemSize);
     for(let i=0;i<a.count;i++)for(let k=0;k<a.itemSize;k++)values[i*a.itemSize+k]=a.getComponent(i,k);
     geometry.setAttribute(name,new THREE.Float32BufferAttribute(values,a.itemSize));
    }
    decodedGeometries.set(sourceUUID,geometry);o.geometry=geometry;
   }
  },
  async warmup(){
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
  },
  completeSetup(){complete=true;renderer.shadowMap.autoUpdate=false;renderer.shadowMap.needsUpdate=true;const preference=new URLSearchParams(location.search).get('mode');setEnabled(preference==='path');},
  invalidate,setEnabled,setContact(value){contact=value;gtao.enabled=value;invalidate(false);},resize,
  get enabled(){return enabled;},get building(){return building;},get samples(){return pathTracer?.samples||0;},get pathTracer(){return pathTracer;},
  get metrics(){return {...metrics,bake:bakeReport?{surfaces:bakedSurfaces.size,appliedSurfaces:appliedBakedSurfaces.size,unmatchedSurfaces:[...bakedSurfaces.keys()].filter(k=>!appliedBakedSurfaces.has(k)),materials:bakedMaterials.size,source:bakeReport.source,sourceSHA:bakeReport.sourceSHA256,staleSource:bakeReport.staleSource}:null,compiling:pathTracer?.isCompiling||false,enabled,building,sceneDirty,samples:pathTracer?.samples||0,materials:materialCache.size,authoredProceduralFinishes:[...materialCache.values()].filter(m=>m.userData.authoredFinish).map(m=>({name:m.name,color:m.color.toArray(),roughness:m.roughness,source:m.userData.authoredFinish})),normalMaps:[...materialCache.values()].filter(m=>m.normalMap).length,roughnessMaps:[...materialCache.values()].filter(m=>m.roughnessMap).length,transmission:[...materialCache.values()].filter(m=>m.transmission>0).map(m=>({name:m.name,ior:m.ior,transmission:m.transmission,opacity:m.opacity})),contact};},
  render(now,{moving,cut,selected}){
   renderer.info.reset();renderer.info.autoReset=false;
   metrics.frameIntervals.push(now-lastFrame);if(metrics.frameIntervals.length>600)metrics.frameIntervals.shift();lastFrame=now;
   if(moving){lastChange=now;pathTracer?.reset();renderer.shadowMap.needsUpdate=true;}
   const idle=now-lastChange>650,eligible=enabled&&!cut&&!selected&&!moving&&idle;
   if(eligible&&sceneDirty&&!building)rebuild();
   if(eligible&&pathTracer&&!building&&!sceneDirty){pathTracer.renderSample();}
   else raster();
   if(now-lastStatus>600){
    lastStatus=now;
    if(metrics.error)status.textContent='Luz progresiva no disponible; navegación activa.';
    else if(cut)status.textContent='Corte arquitectónico · luz de navegación';
    else if(selected)status.textContent='Inspección de elemento · luz de navegación';
    else if(building||pathTracer?.isCompiling)status.textContent='Preparando rebotes de luz…';
    else if(eligible&&pathTracer)status.textContent='Luz progresiva · '+Math.floor(pathTracer.samples)+' muestras';
    else status.textContent=enabled?'Navegación · la luz se refina al detenerte':'Luz de navegación · contacto y materiales físicos';
    if(bakeReport)status.textContent+=bakeReport.staleSource?' · ensayo GI de fuente anterior':' · luz calculada del modelo';
    else if(metrics.bakeDisabled)status.textContent+=' · GI pendiente de actualizar';
   }
  }
 };
}

