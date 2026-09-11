import {chromium} from 'playwright';import fs from 'node:fs';import assert from 'node:assert/strict';
const out=process.env.PHOTO99_CHECKPOINT_QA_OUT||'review99/web_checkpoint_ui';fs.mkdirSync(out,{recursive:true});
const report={sourceSHA256:process.env.PHOTO99_EXPECTED_SHA||'2fb66250a3634a3b956244220d0f52f587623c1d0b0179c9ee0a5fd0d9b2bf46',scope:'Checkpoint glTF resource loading, controls and camera bindings. GPU mode recorded separately; no photorealism approval.',errors:[],views:[]};
const software=process.env.PHOTO99_SOFTWARE==='1';report.gpuMode=software?'SwiftShader':'Chrome hardware';const b=await chromium.launch({channel:'chrome',headless:true,args:software?['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']:['--enable-webgl','--ignore-gpu-blocklist']});
try{
 const p=await b.newPage({viewport:{width:1100,height:760}});p.on('pageerror',e=>report.errors.push(String(e)));p.on('console',m=>{if(m.type()==='error')report.errors.push(m.text())});p.on('response',r=>{if(r.status()>=400)report.errors.push(r.status()+' '+r.url())});
 await p.goto(process.env.PHOTO99_URL||'http://127.0.0.1:8420/preview99/',{waitUntil:'domcontentloaded'});
 await p.waitForFunction(()=>window.__viewer?.ready||document.querySelector('#error:not([hidden])'),null,{timeout:240000});
 assert(await p.evaluate(()=>!!window.__viewer?.ready),await p.locator('#error-detail').innerText());
 report.stats=await p.evaluate(()=>__viewer.stats);assert.equal(report.stats.sourceSHA,report.sourceSHA256);assert.equal(report.stats.doors,13);
 const info=JSON.parse(fs.readFileSync('docs/preview99/assets/model-info.json','utf8'));
 if(info.downloads?.glb){assert.equal(await p.locator('#source-glb').getAttribute('href'),info.downloads.glb);assert(await p.locator('#source-glb').isVisible())}else assert(await p.locator('#source-glb').isHidden(),'Do not offer incomplete standalone glTF download');
 for(const key of ['exterior','estudio','bedroomDining','banoMono']){
  await p.evaluate(k=>__viewer.selectView(k,true),key);await p.waitForTimeout(500);
  report.views.push(await p.evaluate(k=>({key:k,label:document.getElementById('view-name').textContent,position:__viewer.camera.position.toArray(),expected:__viewer.presets[k].p}),key));
  await p.screenshot({path:out+'/'+key+'.jpg',quality:90});
 }
 assert(report.views.every(v=>Math.hypot(...v.position.map((x,i)=>x-v.expected[i]))<.0001));
 await p.evaluate(()=>__viewer.setAllDoors(1));await p.waitForFunction(()=>Array.from(__viewer.doors.values()).every(d=>d.value>.999),null,{timeout:90000});
 report.doors=await p.evaluate(()=>Array.from(__viewer.doors.values(),d=>({key:d.spec.key,positionError:d.node.position.distanceTo(d.openP),parts:d.parts.map(a=>({name:a.node.userData.label,error:a.node.position.distanceTo(a.openP)}))})));
 assert(report.doors.every(d=>d.positionError<.002&&d.parts.every(p=>p.error<.002)));
 await p.setViewportSize({width:390,height:844});await p.evaluate(()=>__viewer.selectView('dormitorio',true));await p.waitForTimeout(500);
 report.portrait=await p.evaluate(()=>({actual:__viewer.camera.position.toArray(),expected:__viewer.presets.dormitorio.portrait.p,width:innerWidth,scrollWidth:document.body.scrollWidth}));
 assert(Math.hypot(...report.portrait.actual.map((x,i)=>x-report.portrait.expected[i]))<.0001);assert(report.portrait.scrollWidth<=report.portrait.width);
 await p.screenshot({path:out+'/portrait.jpg',quality:90});assert.deepEqual(report.errors,[]);report.passed=true;
}catch(e){report.passed=false;report.failure=e.stack;throw e;}finally{fs.writeFileSync(out+'/report.json',JSON.stringify(report,null,2));console.log('CHECKPOINT_WEB_UI',JSON.stringify({passed:report.passed,errors:report.errors,failure:report.failure}));await b.close();}