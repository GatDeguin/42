import {chromium} from 'playwright';import fs from 'node:fs/promises';
const browser=await chromium.launch({channel:'chrome',headless:true});const page=await browser.newPage({viewport:{width:1440,height:1000}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));const r=await page.goto('http://127.0.0.1:8420/planos/',{waitUntil:'networkidle'});
const sheets=await page.locator('article').count();const widths=await page.evaluate(()=>({body:document.body.scrollWidth,viewport:innerWidth}));
const links=await page.locator('a[href$=".pdf"],a[href$=".zip"],article nav a').evaluateAll(es=>es.map(e=>e.href));
const statuses=[];for(const url of links){const r=await page.request.get(url);statuses.push({url,status:r.status(),size:(await r.body()).length});}
await page.screenshot({path:'review95/planos_desktop.png',fullPage:false});await page.setViewportSize({width:390,height:844});await page.screenshot({path:'review95/planos_mobile.png',fullPage:false});
const mobile=await page.evaluate(()=>({body:document.body.scrollWidth,viewport:innerWidth}));const result={status:r.status(),sheets,errors,widths,mobile,downloads:statuses,pass:r.status()===200&&sheets===19&&!errors.length&&widths.body===widths.viewport&&mobile.body===mobile.viewport&&statuses.every(s=>s.status===200&&s.size>0)};
await fs.writeFile('review95/planos_browser_checks.json',JSON.stringify(result,null,2));console.log(JSON.stringify({pass:result.pass,sheets,downloads:statuses.length,errors,mobile}));await browser.close();