import fs from 'node:fs';import assert from 'node:assert/strict';import {chromium} from 'playwright';
const out='review99/r7d_deliverables_qa';fs.mkdirSync(out,{recursive:true});
const SHA='9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e';
const report={sourceSHA256:SHA,errors:[],pages:[],videoRendered:false,scope:'Document/gallery image loading, responsive layout, links and image dialog. Independent architectural and photographic approval is separate.'};
const b=await chromium.launch({channel:'chrome',headless:true});
try{
 for(const [key,w,h,mobile] of [['desktop',1440,1000,false],['mobile',390,844,true]]){
  const p=await b.newPage({viewport:{width:w,height:h},isMobile:mobile,hasTouch:mobile});p.on('pageerror',e=>report.errors.push(String(e)));p.on('response',r=>{if(r.status()>=400)report.errors.push(r.status()+' '+r.url())});
  for(const section of ['renders99','planos99']){
   await p.goto('http://127.0.0.1:8420/'+section+'/',{waitUntil:'networkidle'});
   await p.evaluate(async()=>{const imgs=[...document.querySelectorAll('img[src]')];imgs.forEach(i=>i.loading='eager');await Promise.all(imgs.map(i=>i.decode()))});
   const row=await p.evaluate(()=>({title:document.title,width:innerWidth,scrollWidth:document.documentElement.scrollWidth,images:[...document.querySelectorAll('img[src]')].map(i=>({src:i.getAttribute('src'),width:i.naturalWidth,height:i.naturalHeight})),links:[...document.querySelectorAll('a[href]')].map(a=>({text:a.textContent.trim(),href:a.href}))}));
   assert(row.scrollWidth<=row.width);assert.equal(row.images.length,section==='renders99'?25:33);assert(row.images.every(i=>i.width>0&&i.height>0));
   if(section==='renders99'){
    assert(await p.locator('body').innerText().then(t=>t.includes(SHA)));await p.locator('figure>a').first().click();assert(await p.locator('dialog').evaluate(d=>d.open));await p.locator('dialog button').click();assert(!(await p.locator('dialog').evaluate(d=>d.open)));
   }
   if(!mobile)for(const link of row.links.filter(x=>x.href.startsWith('http://127.0.0.1:8420/')&&!new URL(x.href).hash)){const response=await p.request.head(link.href);assert(response.ok(),link.href)}
   await p.screenshot({path:out+'/'+section+'-'+key+'.jpg',quality:87});report.pages.push({section,viewport:key,...row});
  }
  await p.close();
 }
 assert.deepEqual(report.errors,[]);report.passed=true;
}catch(e){report.passed=false;report.failure=e.stack;throw e}finally{fs.writeFileSync(out+'/report.json',JSON.stringify(report,null,2));console.log('R7D_DELIVERABLES_QA',JSON.stringify({passed:report.passed,errors:report.errors,failure:report.failure}));await b.close()}
