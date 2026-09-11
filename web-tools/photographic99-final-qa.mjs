import {chromium} from 'playwright';
import fs from 'node:fs';import assert from 'node:assert/strict';import crypto from 'node:crypto';
const root='docs/preview99',out='review99/r7_web_final';fs.mkdirSync(out,{recursive:true});
const url=process.env.PHOTO99_URL||'http://127.0.0.1:8420/preview99/?gi=1&denoise=1';
const info=JSON.parse(fs.readFileSync(root+'/assets/model-info.json','utf8'));
const hash=path=>crypto.createHash('sha256').update(fs.readFileSync(path)).digest('hex');
const report={created:new Date().toISOString(),url,sourceSHA:info.stats.source_sha256,sourceModel:info.stats.source_model,glbSHA256:hash(root+'/assets/house.glb'),entrypoint:info.assets?.model||'house.glb',entrypointSHA256:hash(root+'/assets/'+(info.assets?.model||'house.glb')),resourceManifestSHA256:hash(root+'/assets/web-package.json'),errors:[],views:[],screenshots:[],videoRendered:false,scope:'Raster navigation, source-matched lighting, responsive authored cameras and controls. Photographic judgement belongs to independent critic.',mobileScope:'Desktop Chrome portrait viewport and touch emulation; no physical phone result claimed.'};
const browser=await chromium.launch({channel:'chrome',headless:true,args:['--enable-webgl','--ignore-gpu-blocklist']});
function watch(p){p.on('pageerror',e=>report.errors.push(e.stack));p.on('console',m=>{if(m.type()==='error')report.errors.push(m.text())});p.on('response',r=>{if(r.status()>=400)report.errors.push(r.status()+' '+r.url())})}
async function ready(p){await p.waitForFunction(()=>window.__viewer?.ready||document.querySelector('#error:not([hidden])'),null,{timeout:240000});assert(await p.evaluate(()=>!!window.__viewer?.ready),await p.locator('#error-detail').textContent())}
async function shot(p,key){await p.screenshot({path:out+'/'+key+'.jpg',quality:92});report.screenshots.push(key+'.jpg')}
const frames=a=>{a=a.slice(-100).sort((x,y)=>x-y);return{count:a.length,medianMs:a[Math.floor(a.length*.5)],p95Ms:a[Math.floor(a.length*.95)]}};
try{
 const p=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});watch(p);
 let t=performance.now();await p.goto(url,{waitUntil:'domcontentloaded'});await ready(p);report.coldReadyMs=performance.now()-t;await p.waitForTimeout(1400);
 report.desktop=await p.evaluate(()=>{const gl=__viewer.renderer.getContext(),ext=gl.getExtension('WEBGL_debug_renderer_info');return {stats:__viewer.stats,metrics:__viewer.photo.metrics,gpu:ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):null,userAgent:navigator.userAgent,memory:performance.memory?{usedJSHeap:performance.memory.usedJSHeapSize,totalJSHeap:performance.memory.totalJSHeapSize}:null}});
 assert.equal(report.desktop.stats.sourceSHA,report.sourceSHA);assert.equal(report.desktop.stats.doors,13);report.desktop.frameTimes=frames(report.desktop.metrics.frameIntervals);
 assert(report.desktop.metrics.bake,'Source-matched diffuse atlas not active');assert.deepEqual(report.desktop.metrics.bake.unmatchedSurfaces,[]);
 assert.equal(report.desktop.metrics.bake.surfaces,report.desktop.metrics.bake.appliedSurfaces);
 const keys=await p.evaluate(()=>Array.from(__viewer.doors.keys()));assert(keys.includes('bedroomDining')&&keys.includes('bathroomMono')&&!keys.includes('suiteEntry'));
 for(const key of ['exterior','pb','pa','estudio','quincho','cocina','dormitorio','vestidor','bano','mono','bathDining','pileta','huerta','acceso','banoMono','bedroomDining']){
  assert(await p.evaluate(k=>!!__viewer.presets[k],key),'Missing view '+key);await p.evaluate(k=>__viewer.selectView(k,true),key);await p.waitForTimeout(1100);
  const view=await p.evaluate(()=>({position:__viewer.camera.position.toArray(),target:__viewer.controls.target.toArray(),label:document.getElementById('view-name').textContent,fov:__viewer.camera.fov}));
  report.views.push({key,...view});await shot(p,key);
 }
 await p.evaluate(()=>__viewer.selectView('exterior',true));await p.waitForTimeout(600);
 const rect=await p.locator('#scene').boundingBox(),before=await p.evaluate(()=>__viewer.camera.position.toArray());
 await p.mouse.move(rect.x+rect.width*.5,rect.y+rect.height*.5);await p.mouse.down();await p.mouse.move(rect.x+rect.width*.6,rect.y+rect.height*.54,{steps:20});await p.mouse.up();await p.waitForTimeout(550);
 const after=await p.evaluate(()=>__viewer.camera.position.toArray());report.orbitDistance=Math.hypot(...after.map((v,i)=>v-before[i]));assert(report.orbitDistance>.05);
 report.doors=[];
 for(const state of [1,0]){
  await p.evaluate(v=>__viewer.setAllDoors(v),state);
  await p.waitForFunction(v=>Array.from(__viewer.doors.values()).every(d=>Math.abs(d.value-v)<.0001),state,{timeout:15000});
  const rows=await p.evaluate(v=>Array.from(__viewer.doors.values(),d=>({key:d.spec.key,positionError:d.node.position.distanceTo(v?d.openP:d.closedP),angleError:d.node.quaternion.angleTo(v?d.openQ:d.closedQ),parts:(d.parts||[]).map(a=>({name:a.node.userData.label,positionError:a.node.position.distanceTo(v?a.openP:a.closedP),angleError:a.node.quaternion.angleTo(v?a.openQ:a.closedQ)}))})),state);
  assert(rows.every(d=>d.positionError<.002&&d.angleError<.002&&d.parts.every(a=>a.positionError<.002&&a.angleError<.002)));report.doors.push({state,rows});
 }
 await p.check('#cut-enabled');await p.locator('#cut').fill('4.5');await p.locator('#cut').dispatchEvent('input');assert.equal(await p.evaluate(()=>__viewer.renderer.clippingPlanes[0].constant),4.5);
 await p.uncheck('#roof');await p.uncheck('#vegetation');await shot(p,'cut-controls');await p.check('#roof');await p.check('#vegetation');await p.uncheck('#cut-enabled');
 await p.evaluate(()=>__viewer.selectView('exterior',true));await p.waitForTimeout(700);
 for(const [x,y] of [[.6,.4],[.5,.5],[.4,.55],[.6,.6]]){await p.mouse.click(rect.x+rect.width*x,rect.y+rect.height*y);if(await p.evaluate(()=>!document.getElementById('selection').hidden))break}
 report.selection=await p.evaluate(()=>({visible:!document.getElementById('selection').hidden,label:document.getElementById('object-name').textContent}));assert(report.selection.visible);
 t=performance.now();await p.reload({waitUntil:'domcontentloaded'});await ready(p);report.cachedReadyMs=performance.now()-t;
 await p.close();
 const m=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});watch(m);await m.goto(url);await ready(m);await m.waitForTimeout(1000);
 report.mobile={views:[]};
 for(const key of ['exterior','estudio','dormitorio','vestidor']){
  await m.evaluate(k=>__viewer.selectView(k,true),key);await m.waitForTimeout(1000);
  const row=await m.evaluate(k=>({key:k,actual:__viewer.camera.position.toArray(),expected:__viewer.presets[k].portrait.p,sourceCamera:__viewer.presets[k].portrait.sourceCamera,width:innerWidth,scrollWidth:document.body.scrollWidth}),key);
  assert(Math.hypot(...row.actual.map((v,i)=>v-row.expected[i]))<.001);assert(row.scrollWidth<=row.width);report.mobile.views.push(row);await shot(m,'mobile-'+key);
 }
 await m.click('#menu');await shot(m,'mobile-menu');await m.click('[data-view="banoMono"]');await m.waitForTimeout(1200);await shot(m,'mobile-banoMono');
 assert.equal(await m.evaluate(()=>document.body.classList.contains('menu-open')),false);
 assert.deepEqual(report.errors,[]);report.pass=true;
}catch(e){report.pass=false;report.failure=e.stack;throw e}finally{fs.writeFileSync(out+'/report.json',JSON.stringify(report,null,2));console.log('R7_WEB_QA',JSON.stringify({pass:report.pass,source:report.sourceSHA,coldReadyMs:report.coldReadyMs,cachedReadyMs:report.cachedReadyMs,errors:report.errors}));await browser.close()}
