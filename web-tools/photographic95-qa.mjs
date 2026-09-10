import {chromium} from 'playwright';import fs from 'node:fs';
const summarize=a=>{const x=a.slice().sort((a,b)=>a-b);return {count:x.length,median:x[Math.floor(x.length*.5)],p95:x[Math.floor(x.length*.95)],max:x.at(-1)}};
const browser=await chromium.launch({channel:'chrome',headless:true,args:['--enable-webgl','--ignore-gpu-blocklist']});
const baseURL=new URL(process.env.PHOTO95_URL||'http://127.0.0.1:8420/preview95/'),candidate=baseURL.searchParams.has('candidate'),capturePrefix=candidate?'candidate-':'';baseURL.searchParams.set('mode','raster');
const report={sourceURL:baseURL.href,created:new Date().toISOString(),errors:[],views:[],notes:['Static screenshots only. No video. Desktop mobile emulation is not a physical mobile-device benchmark.']};
const shot=async(page,name)=>{await page.screenshot({path:'docs/preview95/screenshots/'+capturePrefix+name+'.png'});await page.screenshot({path:'docs/preview95/screenshots/'+capturePrefix+name+'.jpg',quality:72})};
try{
 const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});
 page.on('pageerror',e=>{report.errors.push(e.stack);console.log('ERROR',e.message)});page.on('console',m=>{if(m.type()==='error'){report.errors.push(m.text());console.log('CONSOLE',m.text().slice(0,800))}});page.on('response',r=>{if(r.status()>=400)report.errors.push(r.status()+' '+r.url())});
 const start=Date.now();await page.goto(baseURL.href,{waitUntil:'domcontentloaded'});await page.waitForFunction(()=>window.__viewer?.ready,null,{timeout:180000});report.readyMs=Date.now()-start;console.log('READY',report.readyMs);
 await page.waitForTimeout(2000);await shot(page,'raster-exterior');
 report.initial=await page.evaluate(()=>{const gl=__viewer.renderer.getContext(),ext=gl.getExtension('WEBGL_debug_renderer_info');return{stats:__viewer.stats,metrics:__viewer.photo.metrics,renderer:ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):null,threeRevision:__viewer.renderer.constructor.name}});
 for(const view of ['estudio','cocina','dormitorio','bano','bathDining','vestidor','quincho','pileta','pb','pa','huerta','mono','acceso']){
  await page.evaluate(v=>__viewer.selectView(v,true),view);await page.waitForTimeout(1600);report.views.push(await page.evaluate(()=>({name:document.getElementById('view-name').textContent,cut:__viewer.renderer.clippingPlanes.map(p=>p.constant),stats:__viewer.stats,intervals:__viewer.photo.metrics.frameIntervals.slice(-60)})));
  if(['estudio','cocina','bano','bathDining','vestidor','quincho','dormitorio','mono','pileta','pb'].includes(view))await shot(page,'raster-'+view);
  console.log('VIEW',view);
 }
 await page.evaluate(()=>__viewer.selectView('exterior',true));await page.waitForTimeout(1200);
 const r=await page.locator('#scene').boundingBox();await page.mouse.move(r.x+r.width*.54,r.y+r.height*.5);await page.mouse.down();await page.mouse.move(r.x+r.width*.59,r.y+r.height*.52,{steps:24});await page.mouse.up();await page.waitForTimeout(900);report.orbit=await page.evaluate(()=>({camera:__viewer.camera.position.toArray(),stats:__viewer.stats}));
 await page.evaluate(()=>__viewer.selectView('exterior',true));await page.waitForTimeout(900);
 let pathStart=Date.now();await page.evaluate(()=>__viewer.photo.setEnabled(true));
 for(let i=0;i<64;i++){await page.waitForTimeout(5000);const state=await page.evaluate(()=>({samples:__viewer.photo.samples,building:__viewer.photo.building,compiling:__viewer.photo.pathTracer?.isCompiling,error:__viewer.photo.metrics.error}));console.log('PATH',i,JSON.stringify(state));if(state.samples>=192||state.error)break;}
 report.pathExteriorMs=Date.now()-pathStart;report.pathExterior=await page.evaluate(()=>__viewer.photo.metrics);if(report.pathExterior.error||report.pathExterior.samples<32)throw new Error('Path trace failed to converge: '+JSON.stringify(report.pathExterior));await shot(page,'path-exterior-192');
 // Geometry mutation must invalidate accumulation and rebuild for all thirteen doors.
 const before=await page.evaluate(()=>__viewer.photo.metrics.builds.length);const doorsStart=Date.now();await page.evaluate(()=>__viewer.setAllDoors(1));await page.waitForTimeout(1800);await page.waitForFunction(()=>Array.from(__viewer.doors.values()).every(d=>d.node.position.distanceTo(d.openP)<.002&&d.node.quaternion.angleTo(d.openQ)<.002),null,{timeout:30000});
 report.doors=await page.evaluate(()=>Array.from(__viewer.doors.values(),d=>({key:d.spec.key,positionError:d.node.position.distanceTo(d.openP),angleError:d.node.quaternion.angleTo(d.openQ)})));
 if(report.doors.length!==13||report.doors.some(d=>d.positionError>.01||d.angleError>.01))throw new Error('Door endpoint validation failed');
 await page.waitForFunction(n=>!__viewer.photo.building&&__viewer.photo.metrics.builds.length>n&&__viewer.photo.samples>2,before,{timeout:90000});
 report.doorUpdateMs=Date.now()-doorsStart;report.afterDoor=await page.evaluate(()=>__viewer.photo.metrics);console.log('DOORS',report.doorUpdateMs,report.afterDoor.builds.length);
 // Cut and selection remain immediate raster operations, not stale path-traced geometry.
 await page.check('#cut-enabled');await page.locator('#cut').fill('4.5');await page.locator('#cut').dispatchEvent('input');await page.waitForTimeout(250);report.cut=await page.evaluate(()=>({plane:__viewer.renderer.clippingPlanes[0].constant,status:document.getElementById('photo-status').textContent}));
 await page.uncheck('#roof');await page.uncheck('#vegetation');await shot(page,'cut-without-roof');
 await page.check('#roof');await page.check('#vegetation');await page.evaluate(()=>{__viewer.photo.setEnabled(false);__viewer.selectView('estudio',true);});await page.waitForTimeout(1700);await shot(page,'raster-estudio-doors-open');await page.evaluate(()=>__viewer.photo.setEnabled(true));
 for(let i=0;i<24;i++){await page.waitForTimeout(5000);const samples=await page.evaluate(()=>__viewer.photo.samples);console.log('STUDIO',i,samples);if(samples>=128)break;}
 report.pathStudio=await page.evaluate(()=>__viewer.photo.metrics);if(report.pathStudio.error||report.pathStudio.samples<32)throw new Error('Studio path did not converge');await shot(page,'path-estudio-128');
 await page.evaluate(()=>__viewer.photo.setEnabled(false));await page.evaluate(()=>__viewer.selectView('exterior',true));await page.waitForTimeout(900);
 await page.mouse.click(r.x+r.width*.60,r.y+r.height*.40);await page.waitForTimeout(100);report.selection=await page.evaluate(()=>({visible:!document.getElementById('selection').hidden,name:document.getElementById('object-name').textContent}));
 await page.close();
 const phone=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});phone.on('pageerror',e=>report.errors.push('mobile '+e.message));
 await phone.goto(baseURL.href,{waitUntil:'domcontentloaded'});await phone.waitForFunction(()=>window.__viewer?.ready,null,{timeout:180000});await phone.waitForTimeout(1200);await shot(phone,'mobile-exterior');await phone.click('#menu');await shot(phone,'mobile-menu');await phone.click('[data-view="estudio"]');await phone.waitForTimeout(1700);await shot(phone,'mobile-estudio');
 report.mobile=await phone.evaluate(()=>({width:innerWidth,scroll:document.body.scrollWidth,view:document.getElementById('view-name').textContent,menuOpen:document.body.classList.contains('menu-open'),stats:__viewer.stats,metrics:__viewer.photo.metrics}));
 if(report.errors.length)throw new Error('Browser errors recorded');if(report.mobile.scroll>report.mobile.width)throw new Error('Mobile horizontal overflow');if(!report.selection.visible)throw new Error('Selection did not resolve');
 report.initial.frames=summarize(report.initial.metrics.frameIntervals.slice(-100));for(const v of report.views){v.frames=summarize(v.intervals);delete v.intervals;}report.pathExterior.frames=summarize(report.pathExterior.frameIntervals.slice(-300));
 fs.writeFileSync('docs/preview95/'+(candidate?'benchmarks-candidate.json':'benchmarks.json'),JSON.stringify(report,null,2));console.log('FINAL',JSON.stringify({errors:report.errors,readyMs:report.readyMs,frames:report.initial.frames,pathMs:report.pathExteriorMs,pathSamples:report.pathExterior.samples,doorUpdateMs:report.doorUpdateMs,selection:report.selection,mobile:{width:report.mobile.width,scroll:report.mobile.scroll}}));
}catch(error){report.failure=error.stack||error.message;fs.writeFileSync('docs/preview95/'+(candidate?'benchmarks-candidate.json':'benchmarks.json'),JSON.stringify(report,null,2));throw error;}finally{await browser.close();}
