import {chromium} from 'playwright';
import fs from 'node:fs';
const browser=await chromium.launch({channel:'chrome',headless:true,args:['--enable-webgl','--ignore-gpu-blocklist']});
const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(r.status()+' '+r.url());});
await page.goto((process.env.VIEWER_URL||'http://127.0.0.1:8420/'),{waitUntil:'networkidle'});await page.waitForFunction(()=>window.__viewer?.ready);await page.waitForTimeout(1200);
const report={errors,views:[],doors:[],desktop:await page.evaluate(()=>({width:innerWidth,scroll:document.body.scrollWidth,stats:__viewer.stats}))};
for(const key of ['exterior','pb','pa','estudio','quincho','cocina','dormitorio','vestidor','bano','pileta','huerta']){
 await page.click('[data-view="'+key+'"]');await page.waitForTimeout(1500);await page.screenshot({path:'review/web_'+key+'.png'});
 report.views.push(await page.evaluate(()=>({name:document.getElementById('view-name').textContent,cut:document.getElementById('cut-enabled').checked,stats:__viewer.stats})));
}
await page.evaluate(()=>__viewer.selectView('exterior'));await page.waitForTimeout(1300);
await page.evaluate(()=>__viewer.setAllDoors(1));await page.waitForTimeout(1400);
report.doors=await page.evaluate(()=>Array.from(__viewer.doors.values(),d=>({key:d.spec.key,error:d.node.position.distanceTo(d.openP),angleError:d.node.quaternion.angleTo(d.openQ)})));
await page.screenshot({path:'review/web_doors_open.png'});
await page.check('#cut-enabled');await page.locator('#cut').fill('4.5');await page.locator('#cut').dispatchEvent('input');report.cut=await page.evaluate(()=>__viewer.renderer.clippingPlanes[0].constant);
await page.uncheck('#roof');await page.uncheck('#vegetation');await page.screenshot({path:'review/web_cut.png'});
const mobile=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});mobile.on('pageerror',e=>errors.push('mobile: '+e.message));await mobile.goto((process.env.VIEWER_URL||'http://127.0.0.1:8420/'),{waitUntil:'networkidle'});await mobile.waitForFunction(()=>window.__viewer?.ready);await mobile.waitForTimeout(1500);await mobile.screenshot({path:'review/web_mobile.png'});
await mobile.click('#menu');await mobile.waitForTimeout(300);await mobile.screenshot({path:'review/web_mobile_menu.png'});await mobile.click('[data-view="estudio"]');await mobile.waitForTimeout(1500);
report.mobile=await mobile.evaluate(()=>({width:innerWidth,scroll:document.body.scrollWidth,menuOpen:document.body.classList.contains('menu-open'),view:document.getElementById('view-name').textContent,stats:__viewer.stats}));
await mobile.screenshot({path:'review/web_mobile_studio.png'});
fs.writeFileSync('review/web_qa.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report));await browser.close();
