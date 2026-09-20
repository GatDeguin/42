import fs from 'node:fs';import assert from 'node:assert/strict';import {chromium,devices} from 'playwright';
const base=process.env.R8_SITE_URL||'http://127.0.0.1:8420/',out=process.env.R8_MOBILE_REPORT||'review99/r8_mobile/browser-local.json';
const report={url:base,environment:'Chrome desktop with touch/UA emulation and 256 MiB V8 old-space limit; not a physical phone',errors:[],cases:[]};
const browser=await chromium.launch({channel:'chrome',headless:true,args:['--enable-webgl','--ignore-gpu-blocklist','--js-flags=--max-old-space-size=256']});
try{
 for(const spec of [{name:'phone',...devices['iPhone 15 Pro Max']},{name:'tablet-landscape',...devices['iPad Pro 11 landscape']}]){
  const {name,defaultBrowserType,...options}=spec;const context=await browser.newContext(options),page=await context.newPage(),requests=[];let contextLost=false;
  await page.addInitScript(()=>{window.__contextLossCount=0;addEventListener('DOMContentLoaded',()=>document.querySelector('canvas')?.addEventListener('webglcontextlost',()=>window.__contextLossCount++));});
  page.on('request',r=>requests.push(r.url()));page.on('pageerror',e=>report.errors.push(String(e)));page.on('crash',()=>report.errors.push(name+' renderer crashed'));page.on('response',r=>{if(r.status()>=400)report.errors.push(r.status()+' '+r.url())});
  const start=performance.now();await page.goto(base,{waitUntil:'domcontentloaded'});await page.waitForFunction(()=>window.__viewer?.ready||document.querySelector('#error:not([hidden])'),null,{timeout:120000});
  assert(await page.evaluate(()=>!!window.__viewer?.ready),await page.locator('#error-detail').textContent());const readyMs=performance.now()-start;
  const initial=await page.evaluate(()=>({stats:__viewer.stats,ratio:__viewer.renderer.getPixelRatio(),width:innerWidth,scrollWidth:document.documentElement.scrollWidth,photo:__viewer.photo.metrics}));
  assert.equal(initial.stats.profile,'mobile');assert.equal(initial.stats.doors,13);assert(initial.stats.downloadBytes<30*1024*1024);assert(initial.ratio<=1);assert(initial.scrollWidth<=initial.width);
  assert(!requests.some(u=>/\/assets\/house\.(gltf|glb)/.test(u)),'Desktop asset downloaded on mobile');assert(!requests.some(u=>/\/photographic\.js/.test(u)),'Desktop pipeline loaded on mobile');
  for(const key of ['estudio','quincho','cocina','dormitorio','vestidor','bano','mono','pileta','pb','pa','exterior']){await page.evaluate(k=>__viewer.selectView(k,true),key);await page.waitForTimeout(180);}
  for(const value of [1,0]){await page.evaluate(v=>__viewer.setAllDoors(v),value);await page.waitForFunction(v=>[...__viewer.doors.values()].every(d=>Math.abs(d.value-v)<.001),value,{timeout:15000});}
  if(await page.locator('#menu').isVisible())await page.click('#menu');await page.click('[data-view="estudio"]');assert(!(await page.evaluate(()=>document.body.classList.contains('menu-open'))));
  const memory=await page.evaluate(()=>{const buffers=new Set(),textures=new Map();__viewer.scene.traverse(o=>{if(!o.isMesh)return;for(const a of Object.values(o.geometry.attributes))buffers.add((a.data?.array||a.array).buffer);if(o.geometry.index)buffers.add(o.geometry.index.array.buffer);for(const m of Array.isArray(o.material)?o.material:[o.material])for(const v of Object.values(m))if(v?.isTexture){const im=v.image;if(im?.width)textures.set(v.source.uuid,im.width*im.height*4*4/3);}});return{geometryArrayBytes:[...buffers].reduce((s,b)=>s+b.byteLength,0),materialTextureMipBytes:[...textures.values()].reduce((s,b)=>s+b,0),webglContextLosses:window.__contextLossCount,stats:__viewer.stats}});
  assert.equal(memory.webglContextLosses,0);assert(memory.geometryArrayBytes<128*1024*1024,'Excess runtime geometry duplication');assert(memory.materialTextureMipBytes<100*1024*1024,'Texture budget exceeded at runtime');
  if(name==='phone'){await page.evaluate(()=>__viewer.selectView('exterior',true));await page.waitForTimeout(500);await page.screenshot({path:'review99/r8_mobile/phone-exterior.png'});await page.evaluate(()=>__viewer.selectView('estudio',true));await page.waitForTimeout(500);await page.screenshot({path:'review99/r8_mobile/phone-studio.png'});}
  report.cases.push({name,readyMs,...initial,memory,requests:requests.length});console.log('MOBILE_CASE',JSON.stringify(report.cases.at(-1)));await context.close();
 }
 assert.deepEqual(report.errors,[]);report.passed=true;
}catch(e){report.passed=false;report.failure=e.stack;throw e}finally{fs.writeFileSync(out,JSON.stringify(report,null,2));await browser.close();}
