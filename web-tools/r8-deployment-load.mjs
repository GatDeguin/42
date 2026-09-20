import fs from 'node:fs';import assert from 'node:assert/strict';import {chromium} from 'playwright';
const base=process.env.R8_SITE_URL||'http://127.0.0.1:8420/';
const out=process.env.R8_DEPLOY_OUT||'review99/r8_final/local-load.json';
const expected='60810e1945f53b339c070c6e77635f408b99c244fc07f43a5084ebeecdde5329';
const report={url:base,scope:'Deployment load and controls only; no architectural or photographic review.',expectedSHA256:expected,errors:[],viewports:[],videoRendered:false};
const browser=await chromium.launch({channel:'chrome',headless:true,args:['--enable-webgl','--ignore-gpu-blocklist']});
try{
 const gallery=await(await fetch(base+'renders99/manifest.json')).json(),plans=await(await fetch(base+'avance-r8/planos/manifest.json')).json();
 assert.equal(gallery.sourceSHA256,expected);assert.equal(gallery.images.length,26);assert.equal(plans.model_sha256,expected);assert.equal(plans.pages,35);
 for(const [name,width,height,touch] of [['desktop',1440,1000,false],['mobile',390,844,true]]){
  const page=await browser.newPage({viewport:{width,height},isMobile:touch,hasTouch:touch});page.on('pageerror',e=>report.errors.push(String(e)));page.on('response',r=>{if(r.status()>=400)report.errors.push(r.status()+' '+r.url())});
  const start=performance.now();await page.goto(base,{waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>window.__viewer?.ready||document.querySelector('#error:not([hidden])'),null,{timeout:240000});
  assert(await page.evaluate(()=>!!window.__viewer?.ready),await page.locator('#error-detail').textContent());
  const state=await page.evaluate(()=>({stats:__viewer.stats,width:innerWidth,scrollWidth:document.documentElement.scrollWidth,doors:[...__viewer.doors.keys()],download:document.getElementById('source-glb').href}));
  assert.equal(state.stats.sourceSHA,expected);assert.equal(state.stats.doors,13);assert(!state.doors.includes('suiteEntry'));assert(state.scrollWidth<=state.width);assert(state.download.endsWith('Casa_de_Campo_99_R8.glb'));
  await page.evaluate(()=>__viewer.selectView('pileta',true));await page.waitForTimeout(300);
  for(const value of [1,0]){await page.evaluate(v=>__viewer.setAllDoors(v),value);await page.waitForFunction(v=>[...__viewer.doors.values()].every(d=>Math.abs(d.value-v)<.001),value,{timeout:20000});}
  if(touch){await page.click('#menu');await page.click('[data-view="estudio"]');await page.waitForTimeout(300);assert(!(await page.evaluate(()=>document.body.classList.contains('menu-open'))));}
  report.viewports.push({name,readyMs:performance.now()-start,...state});await page.close();
 }
 assert.deepEqual(report.errors,[]);report.passed=true;
}catch(e){report.passed=false;report.failure=e.stack;throw e}finally{fs.mkdirSync(out.slice(0,out.lastIndexOf('/')),{recursive:true});fs.writeFileSync(out,JSON.stringify(report,null,2));console.log('R8_DEPLOYMENT_LOAD',JSON.stringify({passed:report.passed,errors:report.errors,viewports:report.viewports.length}));await browser.close();}
