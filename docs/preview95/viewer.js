import {fitAuthoredCamera} from './camera-optics.js';
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/addons/libs/meshopt_decoder.module.js';
import {createPhotographicPipeline} from './photographic.js';
import {mergeGeometries} from 'three/addons/utils/BufferGeometryUtils.js';

const $=id=>document.getElementById(id), viewport=$('viewport'), canvas=$('scene');
const mobile=matchMedia('(max-width:760px)').matches, reduced=matchMedia('(prefers-reduced-motion:reduce)').matches;
let photo, renderer, scene, camera, controls, model, metadata, selected=null, selectionBox=null, cameraMove=null, ready=false, currentView='exterior';
const assetRoot=new URLSearchParams(location.search).has('previous')?'../assets/':'./assets/';
const webTextures={},woodMaterials=new Map();let woodSurfaces={};const doors=new Map(), originals=[], batches=[], pickable=[], raycaster=new THREE.Raycaster(), pointer=new THREE.Vector2();
const categoryNames={SITE:'Terreno y perímetro',GROUND_FLOOR:'Planta baja',UPPER_FLOOR:'Planta alta',STUDIO:'Estudio',QUINCHO:'Quincho',ROOF:'Cubierta',CONSTRUCTION:'Construcción',INTERIORS:'Interior',LANDSCAPE:'Paisajismo',POOL:'Pileta',STAIR:'Escalera',DOORS:'Carpintería',VENTILATION:'Extracción'};
const presets={
 exterior:{label:'Casa y paisaje',p:[4.8,10.5,28.3],t:[14,2.5,10],f:46},
 pb:{label:'Planta baja',p:[14,19,23],t:[15,0,7],f:43,cut:2.8},
 pa:{label:'Planta alta',p:[16,20,22],t:[17.5,3.2,6],f:43,cut:5.6},
 estudio:{label:'Estudio de grabación',p:[20.2,4.98,5.28],t:[17.2,4.5,2.6],f:75},
 quincho:{label:'Quincho y línea de fuego',p:[15.0,1.92,11.4],t:[20.9,1.77,8.25],f:74},
 cocina:{label:'Cocina y comedor',p:[15.05,4.93,11.46],t:[20.7,4.36,9.97],f:70},
 dormitorio:{label:'Dormitorio',p:[17.25,4.82,7.68],t:[15.1,4.15,7.45],f:79},
 vestidor:{label:'Vestidor pasante',p:[18.55,4.85,8.75],t:[18.55,4.22,6.40],f:85},
 bano:{label:'Baño de la vivienda',p:[19.84,4.9,8.55],t:[20.8,4.23,6.72],f:83},
 pileta:{label:'Pileta y jardín',p:[9.7,5.8,23.1],t:[17.5,.6,16.4],f:47},
 mono:{label:'Monoambiente de planta baja',p:[18.4,1.86,5.36],t:[16.85,1.25,2.4],f:76},acceso:{label:'Fachada y acceso',p:[8.5,3.5,-6],t:[15,2.5,3],f:58},huerta:{label:'Huerta y acceso',p:[.1,4.5,1.3],t:[4.65,.45,5.5],f:58}
};
function fail(error){
 console.error(error);$('loading').classList.add('done');$('error').hidden=false;$('status').textContent='No disponible';
 $('error-detail').textContent=error?.message?.includes('WebGL')?'Tu navegador no pudo iniciar WebGL. Prueba con Chrome, Edge o Safari actualizado y aceleración gráfica activada.':'No se pudo descargar o preparar el modelo. Comprueba la conexión y vuelve a cargar.';
}
function doorAncestor(o){while(o){if(o.userData.doorKey)return o;o=o.parent;}return null;}
function metaOf(o){let p=o;while(p){if(p.userData.label)return p.userData;p=p.parent;}return o.userData;}
function setVisibility(){
 photo?.invalidate(true);
 for(const b of batches)b.visible=(!$('roof').checked?!b.userData.roofPart:true)&&($('vegetation').checked||b.userData.category!=='LANDSCAPE');
 for(const o of originals)if(o.userData.dynamic||o.userData.sharedAsset)o.visible=(!$('roof').checked?!o.userData.roofPart:true)&&($('vegetation').checked||o.userData.category!=='LANDSCAPE');
 if(selectionBox)selectionBox.visible=false;
}
function updateViewLabel(){
 const cut=$('cut-enabled').checked?' · corte a '+(+$('cut').value).toFixed(2).replace('.',',')+' m':'';
 $('view-name').textContent=presets[currentView].label+cut;
}
function setCut(){
 photo?.invalidate(false);
 const enabled=$('cut-enabled').checked,value=+$('cut').value;
 $('cut-options').hidden=!enabled;$('cut-value').textContent=value.toFixed(2).replace('.',',')+' m';
 updateViewLabel();
 renderer.clippingPlanes=enabled?[new THREE.Plane(new THREE.Vector3(0,-1,0),value)]:[];
 clearSelection();
}
function setDoor(key,value){
 const d=doors.get(key);if(!d)return;d.target=value;photo?.invalidate(true);
 if(reduced)d.value=value;
 updateDoorButton();updateDoorStatus();
}
function updateDoorStatus(){
 const values=Array.from(doors.values(),d=>d.target),value=values[0]||0;
 const mixed=values.some(v=>Math.abs(v-value)>.001);
 $('door-value').textContent=mixed?'Personalizadas':value===0?'Cerradas':value===1?'Abiertas':Math.round(value*100)+' %';
 if(!mixed)$('doors').value=Math.round(value*100);
}
function setAllDoors(value){
 for(const key of doors.keys())setDoor(key,value);
 $('doors').value=Math.round(value*100);$('door-value').textContent=value===0?'Cerradas':value===1?'Abiertas':Math.round(value*100)+' %';
}
function updateDoorButton(){
 const rig=selected&&doorAncestor(selected);$('toggle-door').hidden=!rig;
 if(rig){const d=doors.get(rig.userData.doorKey);$('toggle-door').textContent=d.target>.5?'Cerrar esta puerta':'Abrir esta puerta';}
}
function selectView(key,instant=false){
 if(!ready)return;
 const v=presets[key];if(!v)return;currentView=key;
 document.querySelectorAll('[data-view]').forEach(b=>b.classList.toggle('active',b.dataset.view===key));$('view-name').textContent=v.label;
 $('cut-enabled').checked=!!v.cut;if(v.cut)$('cut').value=v.cut;setCut();
 if(v.presentationFrame!=null)setAllDoors(v.presentationFrame>=105?1:0);
 else if(key==='vestidor')setAllDoors(0);
 else if(!['exterior','pb','pa','pileta','huerta','acceso'].includes(key))setAllDoors(1);
 else if(key==='exterior')setAllDoors(0);
 fitAuthoredCamera(camera,v);
 const targetFov=v.frustum?camera.fov:v.f;
 const endP=new THREE.Vector3(...v.p),endT=new THREE.Vector3(...v.t);
 if(!v.frustum&&['exterior','pb','pa','pileta','huerta','acceso'].includes(key))endP.sub(endT).multiplyScalar(Math.max(1,1.10/camera.aspect)).add(endT);
 if(instant||reduced){camera.position.copy(endP);controls.target.copy(endT);camera.fov=targetFov;camera.updateProjectionMatrix();controls.update();cameraMove=null;}
 else cameraMove={start:performance.now(),p:camera.position.clone(),t:controls.target.clone(),f:camera.fov,endP,endT,endF:targetFov};
 clearSelection();document.body.classList.remove('menu-open');$('menu').setAttribute('aria-expanded','false');
}
function clearSelection(){photo?.invalidate(false);selected=null;$('selection').hidden=true;if(selectionBox){scene.remove(selectionBox);selectionBox.dispose();selectionBox=null;}}
function choose(o){
 clearSelection();selected=o;photo?.invalidate(false);const d=metaOf(o);$('selection').hidden=false;$('object-name').textContent=d.label||o.name||'Elemento arquitectónico';
 const box=new THREE.Box3().setFromObject(o),size=box.getSize(new THREE.Vector3());$('object-meta').textContent=(categoryNames[d.category]||'Elemento')+' · '+[size.x,size.z,size.y].map(x=>x.toFixed(2).replace('.',',')).join(' × ')+' m';
 selectionBox=new THREE.Box3Helper(box,0xd28b52);selectionBox.material.depthTest=false;selectionBox.renderOrder=5;scene.add(selectionBox);updateDoorButton();
}
function pick(event){
 if(!ready)return;
 const rect=canvas.getBoundingClientRect();pointer.set((event.clientX-rect.left)/rect.width*2-1,-(event.clientY-rect.top)/rect.height*2+1);raycaster.setFromCamera(pointer,camera);
 model.updateMatrixWorld(true);
 const valid=pickable.filter(o=>($('roof').checked||!o.userData.roofPart)&&($('vegetation').checked||o.userData.category!=='LANDSCAPE'));
 const hit=raycaster.intersectObjects(valid,false).find(h=>!$('cut-enabled').checked||h.point.y<=+$('cut').value);
 if(hit)choose(hit.object);else clearSelection();
}
function restoreWood(o,data){
 const profile=woodSurfaces[data.label];
 if(!profile||Array.isArray(o.material))return;
 const kind=profile.floor?'parquet':profile.wood;
 if(!woodMaterials.has(kind)){
  const m=o.material.clone();m.name='WEB | '+kind+' · madera original';m.map=webTextures[kind];m.color.setRGB(1,1,1);m.roughness=.43;m.bumpMap=m.map;m.bumpScale=profile.floor?.0006:.0002;m.needsUpdate=true;woodMaterials.set(kind,m);
 }
 o.material=woodMaterials.get(kind);

 const geometry=o.geometry.clone(),p=geometry.attributes.position,n=geometry.attributes.normal,uv=new Float32Array(p.count*2),normalMatrix=new THREE.Matrix3().getNormalMatrix(o.matrixWorld);
 const point=new THREE.Vector3(),normal=new THREE.Vector3();
 for(let i=0;i<p.count;i++){
  point.fromBufferAttribute(p,i).applyMatrix4(o.matrixWorld);normal.fromBufferAttribute(n,i).applyMatrix3(normalMatrix).normalize();
  const xyz=[point.x,-point.z,point.y],norm=[normal.x,-normal.z,normal.y],axis=profile.axis;
  const across=[0,1,2].filter(k=>k!==axis).sort((a,b)=>Math.abs(norm[a])-Math.abs(norm[b]))[0];
  uv[i*2]=profile.floor?xyz[0]*.70:xyz[across]/1.4;uv[i*2+1]=profile.floor?xyz[1]*.70:xyz[axis]/1.4;
 }
 geometry.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));o.geometry=geometry;
}
function setupBatching(root){
 root.updateMatrixWorld(true);const bins=new Map();
 root.traverse(o=>{
  if(!o.isMesh)return;const data=metaOf(o);o.userData={...data,...o.userData};
  restoreWood(o,data);
  const sharedAsset=(data.label||'').startsWith('BOT95 |');o.userData.sharedAsset=sharedAsset;const dynamic=!!doorAncestor(o);o.userData.dynamic=dynamic;originals.push(o);pickable.push(o);
  const materials=Array.isArray(o.material)?o.material:[o.material];
  for(const m of materials){
   if(m.map){m.map.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());m.map.needsUpdate=true;}
   m.envMapIntensity=.40;for(const [key,texture] of Object.entries(webTextures)){if(m.name.endsWith('| '+key)){m.map=texture;m.needsUpdate=true;}}if(m.name.includes('Césped fino')){m.vertexColors=false;m.color.setRGB(.075,.14,.038);m.needsUpdate=true;}if(m.name.endsWith('| brick'))m.color.setRGB(.75,.65,.54);
   if(m.transparent){m.depthWrite=false;o.castShadow=false;}
   if((m.name.includes('Follaje')||m.name.includes('Corteza'))&&m.vertexColors){m.vertexColors=false;m.needsUpdate=true;}
  }
  photo.prepareMesh(o);
  o.castShadow=sharedAsset||(!materials.some(m=>m.transparent)&&data.category!=='LANDSCAPE');o.receiveShadow=true;
  if(dynamic||sharedAsset||Array.isArray(o.material)){o.visible=true;return;}
  const signature=Object.keys(o.geometry.attributes).sort().join(',');const key=[o.material.uuid,data.category,!!data.roofPart,signature].join('|');
  if(!bins.has(key))bins.set(key,[]);bins.get(key).push(o);o.visible=false;
 });
 for(const members of bins.values()){
  const first=members[0],geos=[];
  for(const o of members){
   let g=o.geometry.clone();if(g.index)g=g.toNonIndexed();for(const [name,a] of Object.entries(g.attributes)){const array=new Float32Array(a.count*a.itemSize);for(let i=0;i<a.count;i++)for(let k=0;k<a.itemSize;k++)array[i*a.itemSize+k]=a.getComponent(i,k);g.setAttribute(name,new THREE.Float32BufferAttribute(array,a.itemSize));}g.applyMatrix4(o.matrixWorld);geos.push(g);
  }
  const geometry=mergeGeometries(geos,false);
  if(!geometry){for(const o of members){o.visible=true;o.userData.dynamic=true;}continue;}
  geometry.computeBoundingSphere();const mesh=new THREE.Mesh(geometry,first.material);mesh.userData={category:first.userData.category,roofPart:first.userData.roofPart};mesh.castShadow=first.castShadow;mesh.receiveShadow=true;scene.add(mesh);batches.push(mesh);
  for(const g of geos)g.dispose();
 }
 setVisibility();
}
async function start(){
 try{
  renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:false,powerPreference:'high-performance'});
  renderer.setPixelRatio(Math.min(devicePixelRatio,mobile?1.5:2));renderer.setClearColor(0xe8ede8);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.AgXToneMapping;renderer.toneMappingExposure=1.0;
  renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
  scene=new THREE.Scene();scene.background=new THREE.Color(0xe8ede8);
  camera=new THREE.PerspectiveCamera(46,1,.035,5000);camera.position.set(...presets.exterior.p);
  controls=new OrbitControls(camera,canvas);controls.target.set(...presets.exterior.t);controls.enableDamping=true;controls.dampingFactor=.10;controls.minDistance=.18;controls.maxDistance=95;controls.maxPolarAngle=Math.PI*.495;controls.screenSpacePanning=true;controls.rotateSpeed=.55;controls.panSpeed=.6;
  controls.addEventListener('start',()=>{cameraMove=null;});
  photo=await createPhotographicPipeline({THREE,renderer,scene,camera,controls,viewport,mobile,status:$('photo-status')});
  const ground=new THREE.Mesh(photo.groundGeometry(),new THREE.MeshStandardMaterial({color:0xffffff,roughness:1,map:photo.textures.outerGrass.albedo,normalMap:photo.textures.outerGrass.normal,normalScale:new THREE.Vector2(.25,.25)}));ground.material.map=ground.material.map.clone();ground.material.map.repeat.set(.25,.25);ground.material.normalMap=ground.material.normalMap.clone();ground.material.normalMap.repeat.set(.25,.25);ground.rotation.x=-Math.PI/2;ground.position.set(0,-.20,0);ground.receiveShadow=true;scene.add(ground);
  new ResizeObserver(()=>{const w=viewport.clientWidth,h=viewport.clientHeight;renderer.setSize(w,h,false);photo?.resize(w,h);const oldPortrait=camera.aspect<1;camera.aspect=w/h;fitAuthoredCamera(camera,presets[currentView]);camera.updateProjectionMatrix();if(ready&&oldPortrait!==(camera.aspect<1))selectView(currentView,true);}).observe(viewport);
  metadata=await fetch(assetRoot+'model-info.json').then(r=>{if(!r.ok)throw new Error('metadata download failed');return r.json();});
  for(const binding of metadata.viewerViews||[]){
   const authored=metadata.cameras.find(c=>c.name===binding.camera);if(!authored)throw new Error('Missing authored camera: '+binding.camera);
   presets[binding.key]={label:binding.label,p:authored.position,t:authored.target,f:authored.fov,frustum:authored.frustum,presentationFrame:authored.presentationFrame};const button=document.querySelector('[data-view="'+binding.key+'"]');if(button)button.hidden=false;
  }
  if(metadata.downloads?.blender&&/^https?:\/\//.test(metadata.downloads.blender)){const link=$('source-blend');if(link){link.href=metadata.downloads.blender;link.hidden=false;}}
  woodSurfaces=await fetch(assetRoot+'textures/wood-surfaces.json').then(r=>r.json());
  const texLoader=new THREE.TextureLoader();await Promise.all(Object.entries({fabric:'fabric',paver:'paver',poolBasin:'poolTile',road:'cement',terracotta:'brick',oak:'oak',walnut:'walnut',parquet:'parquet'}).map(async([key,file])=>{const t=await texLoader.loadAsync('../assets/textures/'+file+'_albedo.png');t.colorSpace=THREE.SRGBColorSpace;t.flipY=false;t.wrapS=t.wrapT=THREE.RepeatWrapping;t.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());if(key==='parquet')t.repeat.set(1/(.70*2.8),1/(.70*1.44));webTextures[key]=t;}));const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);if(metadata.gi?.enabled&&new URLSearchParams(location.search).has('gi'))await photo.loadBake(loader);
  const gltf=await loader.loadAsync(assetRoot+'house.glb',e=>{const total=e.total||metadata.stats.downloadBytes;const progress=Math.min(95,e.loaded/total*95);$('progress').style.width=progress+'%';$('loading-text').textContent='Descargando modelo · '+Math.round(progress)+' %';});
  model=gltf.scene;scene.add(model);$('loading-text').textContent='Preparando materiales e interacción…';
  const sourceNodes=new Map();model.traverse(o=>sourceNodes.set(o.userData.label||o.name,o));
  model.traverse(o=>{if(o.userData.doorKey){const spec=metadata.doors.find(d=>d.key===o.userData.doorKey);if(spec)doors.set(spec.key,{node:o,spec,value:0,target:0,closedP:new THREE.Vector3(...spec.closed.position),openP:new THREE.Vector3(...spec.open.position),closedQ:new THREE.Quaternion(...spec.closed.quaternion),openQ:new THREE.Quaternion(...spec.open.quaternion),parts:(spec.parts||[]).map(part=>({node:sourceNodes.get(part.label),closedP:new THREE.Vector3(...part.closed.position),openP:new THREE.Vector3(...part.open.position),closedQ:new THREE.Quaternion(...part.closed.quaternion),openQ:new THREE.Quaternion(...part.open.quaternion),closedS:new THREE.Vector3(...part.closed.scale),openS:new THREE.Vector3(...part.open.scale)}))});}});
  for(const d of doors.values())for(const part of d.parts||[])if(!part.node)throw new Error('Missing animated door child');
  await new Promise(resolve=>requestAnimationFrame(resolve));
  setupBatching(model);await photo.warmup();photo.completeSetup();ready=true;selectView('exterior',true);$('progress').style.width='100%';$('status').textContent='Modelo listo';$('status-dot').classList.add('ready');$('loading').classList.add('done');
  window.__viewer={get ready(){return ready;},get stats(){return {drawCalls:renderer.info.render.calls,triangles:renderer.info.render.triangles,doors:doors.size,meshes:originals.length,sourceModel:metadata.stats.source_model,sourceSHA:metadata.stats.source_sha256,downloadBytes:metadata.stats.downloadBytes};},selectView,setAllDoors,get presets(){return presets;},get photo(){return photo;},get scene(){return scene;},get controls(){return controls;},get camera(){return camera;},get doors(){return doors;},get renderer(){return renderer;},get originals(){return originals;},pick};
  animate();
 }catch(error){fail(error);}
}
let previous=performance.now();
function animate(now=performance.now()){
 requestAnimationFrame(animate);if(document.hidden)return;
 const dt=Math.min((now-previous)/1000,.05);previous=now;
 if(cameraMove){const a=cameraMove,u=Math.min(1,(now-a.start)/1100),t=u*u*(3-2*u);camera.position.lerpVectors(a.p,a.endP,t);controls.target.lerpVectors(a.t,a.endT,t);camera.fov=THREE.MathUtils.lerp(a.f,a.endF,t);camera.updateProjectionMatrix();if(u===1)cameraMove=null;}
 for(const d of doors.values()){
  d.value=THREE.MathUtils.damp(d.value,d.target,9,dt);d.node.position.lerpVectors(d.closedP,d.openP,d.value);d.node.quaternion.slerpQuaternions(d.closedQ,d.openQ,d.value);
  for(const p of d.parts||[]){if(!p.node)continue;p.node.position.lerpVectors(p.closedP,p.openP,d.value);p.node.quaternion.slerpQuaternions(p.closedQ,p.openQ,d.value);p.node.scale.lerpVectors(p.closedS,p.openS,d.value);}
 }
 if(selectionBox&&selected){selectionBox.box.setFromObject(selected);selectionBox.updateMatrixWorld(true);}
 controls.update();photo.render(now,{moving:!!cameraMove||Array.from(doors.values()).some(d=>Math.abs(d.value-d.target)>.0001),cut:$('cut-enabled').checked,selected:!!selected});
}
document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>selectView(b.dataset.view)));
$('roof').addEventListener('change',setVisibility);$('vegetation').addEventListener('change',setVisibility);
$('cut-enabled').addEventListener('change',()=>ready&&setCut());$('cut').addEventListener('input',()=>ready&&setCut());
$('doors').addEventListener('input',e=>setAllDoors(e.target.value/100));
$('home').addEventListener('click',()=>selectView('exterior'));
for(const [id,factor] of [['zoom-in',.8],['zoom-out',1.25]])$(id).addEventListener('click',()=>{if(!ready)return;cameraMove=null;camera.position.sub(controls.target).multiplyScalar(factor).add(controls.target);controls.update();});
$('clear-selection').addEventListener('click',clearSelection);
$('toggle-door').addEventListener('click',()=>{const rig=selected&&doorAncestor(selected);if(rig){const d=doors.get(rig.userData.doorKey);setDoor(rig.userData.doorKey,d.target>.5?0:1);}});
$('menu').addEventListener('click',()=>{const open=document.body.classList.toggle('menu-open');$('menu').setAttribute('aria-expanded',String(open));});
$('fullscreen').addEventListener('click',async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else if(viewport.requestFullscreen)await viewport.requestFullscreen();}catch{ $('status').textContent='Pantalla completa no disponible';}});
let down=null;
canvas.addEventListener('pointerdown',e=>{down={x:e.clientX,y:e.clientY};});
canvas.addEventListener('pointerup',e=>{if(down&&Math.hypot(e.clientX-down.x,e.clientY-down.y)<5&&e.button===0)pick(e);down=null;});
canvas.addEventListener('keydown',e=>{if(e.key==='Escape')clearSelection();if(e.key==='Home')selectView('exterior');if(e.key==='+'||e.key==='=')$('zoom-in').click();if(e.key==='-')$('zoom-out').click();});
canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();fail(new Error('WebGL context lost'));});
$('photo-mode').addEventListener('change',e=>photo.setEnabled(e.target.checked));
$('contact-mode').addEventListener('change',e=>photo.setContact(e.target.checked));
start();
