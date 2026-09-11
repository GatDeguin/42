import {chromium} from 'playwright';
import fs from 'node:fs';import assert from 'node:assert/strict';
const out='review99/github_progress';fs.mkdirSync(out,{recursive:true});
const url=process.env.PROGRESS_URL||'http://127.0.0.1:8420/avance-r7/';
const report={url,errors:[],views:[],scope:'Static R7 progress page, desktop and touch viewport emulation. No claim of final R7 model viewer QA.'};
const b=await chromium.launch({channel:'chrome',headless:true});
try{for(const [key,width,height,mobile] of [['desktop',1440,1000,false],['mobile',390,844,true]]){
 const p=await b.newPage({viewport:{width,height},isMobile:mobile,hasTouch:mobile});
 p.on('pageerror',e=>report.errors.push(String(e)));p.on('response',r=>{if(r.status()>=400)report.errors.push(r.status()+' '+r.url())});
 const response=await p.goto(url,{waitUntil:'networkidle'});assert.equal(response.status(),200);
 assert((await p.locator('body').innerText()).includes('R7 aún no tiene nota ni aprobación.'));
 assert((await p.locator('body').innerText()).includes('El visor principal y los planos todavía muestran R6K.'));
 const row=await p.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,imageReady:[...document.images].every(i=>i.complete&&i.naturalWidth===1200),links:[...document.querySelectorAll('a')].map(a=>({text:a.textContent,href:a.href}))}));
 assert(row.scrollWidth<=row.width);assert(row.imageReady);report.views.push({key,...row});
 await p.screenshot({path:out+'/page-'+key+'.png',fullPage:true});await p.close();
}assert.deepEqual(report.errors,[]);report.passed=true;}catch(e){report.passed=false;report.failure=e.stack;throw e;}finally{fs.writeFileSync(out+'/page-qa.json',JSON.stringify(report,null,2));console.log(JSON.stringify({passed:report.passed,errors:report.errors}));await b.close();}