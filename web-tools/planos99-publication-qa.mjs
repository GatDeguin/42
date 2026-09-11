import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
const root=path.resolve('docs');
const out=path.resolve('review99/planos99_publication');fs.mkdirSync(out,{recursive:true});
const types={'.html':'text/html; charset=utf-8','.svg':'image/svg+xml','.json':'application/json','.pdf':'application/pdf','.css':'text/css','.csv':'text/csv','.zip':'application/zip'};
const server=http.createServer((req,res)=>{let p=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(p!==root&&!p.startsWith(root+path.sep)){res.writeHead(403);return res.end();}if(fs.existsSync(p)&&fs.statSync(p).isDirectory())p=path.join(p,'index.html');if(!fs.existsSync(p)){res.writeHead(404);return res.end();}res.writeHead(200,{'Content-Type':types[path.extname(p)]||'application/octet-stream'});fs.createReadStream(p).pipe(res);});
await new Promise(r=>server.listen(0,'127.0.0.1',r));const port=server.address().port;
const browser=await chromium.launch({channel:'chrome',headless:true,args:['--disable-gpu']});const results=[];
try {
 for(const [name,width,height] of [['desktop',1440,1000],['mobile',390,844]]){
  const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${port}/planos99/`,{waitUntil:'networkidle'});
  await page.locator('img').evaluateAll(imgs=>imgs.forEach(im=>im.loading='eager'));
  await page.waitForFunction(()=>[...document.images].every(im=>im.complete&&im.naturalWidth>0));
  const metrics=await page.evaluate(()=>({title:document.title,cards:document.querySelectorAll('article').length,images:[...document.images].map(i=>({src:i.getAttribute('src'),ok:i.complete&&i.naturalWidth>0})),width:innerWidth,scrollWidth:document.documentElement.scrollWidth,links:[...document.querySelectorAll('a')].map(a=>a.getAttribute('href')),body:document.body.innerText}));
  const hrefs=[...new Set(metrics.links.filter(h=>h&&!h.startsWith('http')&&!h.startsWith('#')))];const responses=[];
  for(const href of hrefs){const response=await page.request.get(new URL(href,page.url()).href);responses.push({href,status:response.status(),bytes:(await response.body()).byteLength});}
  await page.screenshot({path:path.join(out,`${name}-top.png`)});
  await page.locator('footer').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,`${name}-footer.png`)});
  const row={name,cards:metrics.cards,all_images_loaded:metrics.images.every(i=>i.ok),no_horizontal_overflow:metrics.scrollWidth<=metrics.width,all_links_ok:responses.every(r=>r.status===200&&r.bytes>0),links:responses,errors,revision:metrics.title.includes('R7D'),status:metrics.body.includes('9,9/10'),gallery_linked:metrics.links.includes('../renders99/'),viewer:metrics.links.includes('../')};
  row.pass=row.cards===33&&row.all_images_loaded&&row.no_horizontal_overflow&&row.all_links_ok&&row.errors.length===0&&row.revision&&row.status&&row.gallery_linked&&row.viewer;results.push(row);await page.close();
 }
 const report={status:results.every(r=>r.pass)?'PASS':'FAIL',model_sha256:'9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e',surfaces:results};fs.writeFileSync(path.join(out,'browser_validation.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({status:report.status,surfaces:results.map(r=>({name:r.name,cards:r.cards,pass:r.pass,links:r.links.length,overflow:!r.no_horizontal_overflow,errors:r.errors}))},null,2));if(report.status!=='PASS')process.exitCode=1;
} finally {await browser.close();await new Promise(r=>server.close(r));}
