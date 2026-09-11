import fs from 'node:fs';import assert from 'node:assert/strict';import {chromium} from 'playwright';
const base=process.env.PHOTO99_DOCS_URL||'http://127.0.0.1:8420/';
const out=process.env.PHOTO99_DOCS_QA_OUT||'review99/github_r8_progress/local-ui';fs.mkdirSync(out,{recursive:true});
const manifest=await(await fetch(base+'avance-r8/manifest.json')).json();
const report={url:base,sourceSHA256:manifest.sourceSHA256,errors:[],pages:[],videoRendered:false,scope:'Publication layout, images, source identity and links; no architectural score.'};
const b=await chromium.launch({channel:'chrome',headless:true});
try {
 for(const [key,w,h,mobile] of [['desktop',1440,1000,false],['mobile',390,844,true]]) {
  const p=await b.newPage({viewport:{width:w,height:h},isMobile:mobile,hasTouch:mobile});p.on('pageerror',e=>report.errors.push(String(e)));p.on('response',r=>{if(r.status()>=400)report.errors.push(r.status()+' '+r.url())});
  await p.goto(base+'avance-r8/',{waitUntil:'networkidle'});
  await p.evaluate(async()=>{const imgs=[...document.querySelectorAll('img[src]')];imgs.forEach(i=>i.loading='eager');await Promise.all(imgs.map(i=>i.decode()))});
  const row=await p.evaluate(()=>({title:document.title,width:innerWidth,scrollWidth:document.documentElement.scrollWidth,images:[...document.querySelectorAll('img[src]')].map(i=>({src:i.getAttribute('src'),width:i.naturalWidth,height:i.naturalHeight})),links:[...document.querySelectorAll('a[href]')].map(a=>({text:a.textContent.trim(),href:a.href})),text:document.body.innerText}));
  assert(row.scrollWidth<=row.width);assert.equal(row.images.length,4);assert(row.images.every(i=>i.width>=1800&&i.height>=1350));assert(row.text.includes(manifest.sourceSHA256));assert(row.text.includes('R8 todavía no tiene una calificación integral'));assert(row.text.includes('Video pausado'));
  if(!mobile)for(const link of row.links.filter(x=>x.href.startsWith(base)&&!new URL(x.href).hash)){const response=await p.request.head(link.href);assert(response.ok(),link.href)}
  for(const q of manifest.images){assert(row.images.some(i=>i.src===q.publicFile));const data=Buffer.from(await(await fetch(base+'avance-r8/'+q.publicFile)).arrayBuffer());const crypto=await import('node:crypto');assert.equal(crypto.createHash('sha256').update(data).digest('hex'),q.publicSHA256)}
  delete row.text;await p.screenshot({path:out+'/avance-r8-'+key+'.jpg',quality:88,fullPage:true});report.pages.push({viewport:key,...row});await p.close();
 }
 assert.deepEqual(report.errors,[]);report.passed=true;
}catch(e){report.passed=false;report.failure=e.stack;throw e}finally{fs.writeFileSync(out+'/report.json',JSON.stringify(report,null,2));console.log('R8_PROGRESS_QA',JSON.stringify({passed:report.passed,errors:report.errors,failure:report.failure}));await b.close()}
