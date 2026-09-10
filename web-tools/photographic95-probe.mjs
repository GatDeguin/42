import {chromium} from 'playwright';import fs from 'node:fs';
const browser=await chromium.launch({channel:'chrome',headless:true,args:['--enable-webgl','--ignore-gpu-blocklist']});
const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});
const errors=[],logs=[];page.on('pageerror',e=>{errors.push(e.stack);console.log('ERROR',e.message)});page.on('console',m=>{if(m.type()==='error'){errors.push(m.text());console.log('CONSOLE',m.text().slice(0,800));}});page.on('response',r=>{if(r.status()>=400){errors.push(r.status()+' '+r.url());console.log('HTTP',r.status(),r.url())}});
const started=Date.now();await page.goto('http://127.0.0.1:8420/preview95/?mode=raster',{waitUntil:'domcontentloaded'});await page.waitForFunction(()=>window.__viewer?.ready,null,{timeout:180000});console.log('READY',Date.now()-started);await page.waitForTimeout(2500);
await page.screenshot({path:'docs/preview95/screenshots/raster-exterior.png'});await page.screenshot({path:'docs/preview95/screenshots/raster-exterior.jpg',quality:70});
const report={errors,loadMs:Date.now()-started,raster:await page.evaluate(()=>({stats:__viewer.stats,optics:__viewer.photo.metrics,hardware:(()=>{const gl=__viewer.renderer.getContext(),ext=gl.getExtension('WEBGL_debug_renderer_info');return ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):null;})()}))};
console.log('RASTER',JSON.stringify({...report.raster,optics:{...report.raster.optics,frameIntervals:undefined}}));
await page.evaluate(()=>__viewer.photo.setEnabled(true));
for(let n=0;n<18;n++){await page.waitForTimeout(6000);const state=await page.evaluate(()=>({samples:__viewer.photo.samples,compiling:__viewer.photo.pathTracer?.isCompiling,building:__viewer.photo.building,error:__viewer.photo.metrics.error,builds:__viewer.photo.metrics.builds}));console.log('PATH',n,JSON.stringify(state));if(state.samples>=12||state.error)break;}
await page.screenshot({path:'docs/preview95/screenshots/path-exterior.png'});report.path=await page.evaluate(()=>__viewer.photo.metrics);
fs.writeFileSync('docs/preview95/probe.json',JSON.stringify(report,null,2));await browser.close();


