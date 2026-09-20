import fs from 'node:fs';import assert from 'node:assert/strict';import {chromium} from 'playwright';
const out='review99/r8_mobile_trees';fs.mkdirSync(out,{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true});
try{
 const page=await browser.newPage();await page.route('**/__tree_test__',r=>r.fulfill({contentType:'text/html',body:'<script type="importmap">{"imports":{"three":"/vendor/three.module.js","three/addons/":"/vendor/addons/"}}</script>'}));await page.goto('http://127.0.0.1:8420/__tree_test__');
 const result=await page.evaluate(async()=>{
  const T=await import('three'),{GLTFLoader}=await import('three/addons/loaders/GLTFLoader.js'),{MeshoptDecoder}=await import('three/addons/libs/meshopt_decoder.module.js');
  const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder),models=[];
  for(const name of ['reference','candidate']){const g=await loader.loadAsync('/preview99/assets/mobile-test/'+name+'.glb?v='+Date.now());g.scene.traverse(o=>{if(o.isMesh){const old=o.material;o.material=new T.MeshBasicMaterial({map:old.map,alphaTest:old.alphaTest,side:T.DoubleSide});}});models.push(g.scene);}
  const renderer=new T.WebGLRenderer({alpha:true,antialias:false,preserveDrawingBuffer:true});renderer.setSize(512,512);renderer.setClearColor(0,0);const target=new T.WebGLRenderTarget(512,512),box=new T.Box3().setFromObject(models[0]),center=box.getCenter(new T.Vector3()),size=box.getSize(new T.Vector3()),s=Math.max(...size.toArray())*.55,camera=new T.OrthographicCamera(-s,s,s,-s,.01,1000),rows=[];
  for(const [view,p,up] of [['front',[0,0,20],[0,1,0]],['side',[20,0,0],[0,1,0]],['top',[0,20,0],[0,0,-1]]]){
   camera.position.copy(center).add(new T.Vector3(...p));camera.up.fromArray(up);camera.lookAt(center);camera.updateMatrixWorld();const masks=[],images=[];
   for(const model of models){const scene=new T.Scene();scene.add(model);renderer.setRenderTarget(target);renderer.render(scene,camera);const data=new Uint8Array(512*512*4);renderer.readRenderTargetPixels(target,0,0,512,512,data);masks.push(Uint8Array.from({length:512*512},(_,i)=>data[i*4+3]>127?1:0));renderer.setRenderTarget(null);renderer.render(scene,camera);images.push(renderer.domElement.toDataURL());}
   let reference=0,candidate=0,intersection=0,union=0;for(let i=0;i<masks[0].length;i++){reference+=masks[0][i];candidate+=masks[1][i];intersection+=masks[0][i]&&masks[1][i];union+=masks[0][i]||masks[1][i];}
   rows.push({view,reference,candidate,coverage:intersection/reference,iou:intersection/union,images});
  }
  return rows;
 });
 for(const row of result){for(const [i,data] of row.images.entries())fs.writeFileSync(out+'/'+row.view+'-'+(i?'candidate':'reference')+'.png',Buffer.from(data.split(',')[1],'base64'));delete row.images;}
 fs.writeFileSync(out+'/canopy-coverage.json',JSON.stringify(result,null,2));console.log(result);
 for(const row of result){assert(row.coverage>=.72,'Tree canopy coverage below72% from '+row.view);assert(row.iou>=.58,'Tree silhouette differs excessively from '+row.view);}
}finally{await browser.close();}
