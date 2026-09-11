/** Verify either33 or35 published sheets against its manifest, using CPU Chromium. */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
const args=process.argv.slice(2),get=(key,fallback)=>args.includes(key)?args[args.indexOf(key)+1]:fallback;
const root=process.cwd(),publication=path.resolve(get('--publication','planos95/r8_publication_preview'));
const out=path.resolve(get('--out','review99/r8_publisher/browser'));fs.mkdirSync(out,{recursive:true});
const manifest=JSON.parse(fs.readFileSync(path.join(publication,'manifest.json'),'utf8'));
if(!publication.startsWith(root+path.sep)||!out.startsWith(root+path.sep))throw Error('Workspace paths required');
const prefix='/'+path.relative(root,publication).split(path.sep).join('/')+'/';
const types={'.html':'text/html; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.json':'application/json','.pdf':'application/pdf','.css':'text/css','.csv':'text/csv','.zip':'application/zip','.md':'text/plain; charset=utf-8'};
const server=http.createServer((req,res)=>{let p=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(p!==root&&!p.startsWith(root+path.sep)){res.writeHead(403);return res.end();}if(fs.existsSync(p)&&fs.statSync(p).isDirectory())p=path.join(p,'index.html');if(!fs.existsSync(p)){res.writeHead(404);return res.end();}res.writeHead(200,{'Content-Type':types[path.extname(p)]||'application/octet-stream'});fs.createReadStream(p).pipe(res);});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({channel:'chrome',headless:true,args:['--disable-gpu']});const results=[];
try{
 for(const [name,width,height] of [['desktop',1440,1000],['mobile',390,844]]){
  const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}${prefix}`,{waitUntil:'networkidle'});
  await page.locator('img').evaluateAll(imgs=>imgs.forEach(im=>im.loading='eager'));
  await page.waitForFunction(()=>[...document.images].every(im=>im.complete&&im.naturalWidth>0));
  const m=await page.evaluate(()=>({title:document.title,cards:document.querySelectorAll('article').length,images:[...document.images].map(i=>({src:i.getAttribute('src'),ok:i.complete&&i.naturalWidth>0,width:i.naturalWidth})),width:innerWidth,scrollWidth:document.documentElement.scrollWidth,links:[...document.querySelectorAll('a')].map(a=>a.getAttribute('href')),body:document.body.innerText}));
  const responses=[];
  for(const href of [...new Set(m.links.filter(h=>h&&!h.startsWith('http')&&!h.startsWith('#')))]){const r=await page.request.get(new URL(href,page.url()).href);responses.push({href,status:r.status(),bytes:(await r.body()).byteLength});}
  await page.screenshot({path:path.join(out,name+'-top.png')});
  await page.locator('footer').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,name+'-footer.png')});
  const row={name,cards:m.cards,images:m.images,all_images_loaded:m.images.every(i=>i.ok),no_horizontal_overflow:m.scrollWidth<=m.width,all_links_ok:responses.every(r=>r.status===200&&r.bytes>0),links:responses,errors,revision:m.title.includes(manifest.revision),status:m.body.includes('9,9/10'),preview:manifest.preview?m.body.includes('Prueba local del generador'):true,navigation:['back','viewer','gallery'].every(k=>!manifest.navigation[k]||m.links.includes(manifest.navigation[k]))};
  row.pass=row.cards===manifest.pages&&row.images.length===manifest.pages&&row.all_images_loaded&&row.no_horizontal_overflow&&row.all_links_ok&&!errors.length&&row.revision&&row.status&&row.preview&&row.navigation;results.push(row);await page.close();
 }
 const report={status:results.every(r=>r.pass)?'PASS':'FAIL',model_sha256:manifest.model_sha256,publication:path.relative(root,publication),pages:manifest.pages,renderer:'Chrome headless --disable-gpu',surfaces:results};fs.writeFileSync(path.join(out,'browser_validation.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({status:report.status,surfaces:results.map(r=>({name:r.name,cards:r.cards,pass:r.pass,links:r.links.length,overflow:!r.no_horizontal_overflow,errors:r.errors}))},null,2));if(report.status!=='PASS')process.exitCode=1;
}finally{await browser.close();await new Promise(r=>server.close(r));}
