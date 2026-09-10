import {chromium} from 'playwright';import fs from 'node:fs';
const browser=await chromium.launch({channel:'chrome',headless:true,args:['--enable-webgl','--ignore-gpu-blocklist']});
try{const page=await browser.newPage({viewport:{width:960,height:680}});page.on('pageerror',e=>console.log('ERROR',e.message));
await page.goto('http://127.0.0.1:8420/preview95/?mode=raster');await page.waitForFunction(()=>window.__viewer?.ready,null,{timeout:120000});await page.evaluate(()=>{__viewer.selectView('estudio',true);__viewer.photo.setEnabled(true);__viewer.photo.pathTracer.renderScale=.4;__viewer.photo.pathTracer.minSamples=1;});
for(let i=0;i<30;i++){await page.waitForTimeout(3000);const state=await page.evaluate(()=>({samples:__viewer.photo.samples,compile:__viewer.photo.pathTracer.isCompiling}));console.log('STATE',i,state);if(state.samples>=32)break;}
await page.screenshot({path:'docs/preview95/screenshots/debug-filtered.jpg',quality:72});
console.log('PARAMS',await page.evaluate(()=>({camera:__viewer.camera.position.toArray(),target:__viewer.controls.target.toArray(),builds:__viewer.photo.metrics.builds,bounds:__viewer.photo.metrics.geometryBounds,lights:__viewer.photo.pathTracer._pathTracer.material.lights.count})));
await page.evaluate(()=>{__viewer.photo.pathTracer.renderToCanvasCallback=(target,r,quad)=>{const old=r.autoClear;r.autoClear=false;quad.render(r);r.autoClear=old;};});await page.waitForTimeout(1000);await page.screenshot({path:'docs/preview95/screenshots/debug-raw.jpg',quality:72});
await page.evaluate(()=>{__viewer.photo.pathTracer.updateCamera();});await page.waitForTimeout(3000);await page.screenshot({path:'docs/preview95/screenshots/debug-camera.jpg',quality:72});
}finally{await browser.close();}


