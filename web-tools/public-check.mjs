import {chromium} from 'playwright';import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';import {execFileSync} from 'node:child_process';
const url=process.env.VIEWER_URL||'https://gatdeguin.github.io/42/';
fs.mkdirSync('web-tools/.cache',{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true,args:['--enable-webgl','--ignore-gpu-blocklist']});
const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];
page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(r.status()+' '+r.url());});
const start=Date.now();const response=await page.goto(url,{waitUntil:'networkidle'});assert.equal(response.status(),200);await page.waitForFunction(()=>window.__viewer?.ready,{},{timeout:60000});
const readyMS=Date.now()-start;
await page.waitForTimeout(1400);await page.screenshot({path:'web-tools/.cache/public-desktop.png'});
await page.click('[data-view="pb"]');await page.locator('#cut').fill('4.5');await page.locator('#cut').dispatchEvent('input');
assert.equal(await page.locator('#view-name').textContent(),'Planta baja · corte a 4,50 m');
await page.evaluate(()=>__viewer.setAllDoors(1));await page.waitForTimeout(1500);
const doors=await page.evaluate(()=>Array.from(__viewer.doors.values(),d=>({key:d.spec.key,error:d.node.position.distanceTo(d.openP),angleError:d.node.quaternion.angleTo(d.openQ)})));assert.equal(doors.length,12);assert(doors.every(d=>d.error<.0001&&d.angleError<.0001));
await page.setViewportSize({width:390,height:844});await page.click('#home');await page.waitForTimeout(1400);await page.screenshot({path:'web-tools/.cache/public-mobile.png'});
await page.click('#menu');await page.waitForTimeout(300);await page.click('[data-view="estudio"]');await page.waitForTimeout(1400);
const mobile=await page.evaluate(()=>({width:innerWidth,scroll:document.body.scrollWidth,title:document.querySelector('#view-name').textContent,menuOpen:document.body.classList.contains('menu-open')}));assert.equal(mobile.width,mobile.scroll);assert.equal(mobile.title,'Estudio de grabación');assert.equal(mobile.menuOpen,false);
const assets={};for(const file of ['index.html','viewer.js','viewer.css','assets/house.glb','assets/textures/parquet_albedo.png']){
 const response=await page.request.get(new URL(file,url).href);assert.equal(response.status(),200);const body=await response.body(),hash=crypto.createHash('sha256').update(body).digest('hex'),expected=crypto.createHash('sha256').update(execFileSync('git',['show','HEAD:docs/'+file],{maxBuffer:20*1024*1024})).digest('hex');assert.equal(hash,expected);assets[file]={bytes:body.length,sha256:hash};
}
const report={url,verifiedAt:new Date().toISOString(),http:response.status(),readyMS,errors,mobile,doors,assets,stats:await page.evaluate(()=>__viewer.stats)};
assert.deepEqual(errors,[]);fs.writeFileSync('web-tools/.cache/public-check.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));await browser.close();
