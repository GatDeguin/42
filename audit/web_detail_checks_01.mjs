import {chromium} from '../web-tools/node_modules/playwright/index.mjs';import fs from 'node:fs';
const b=await chromium.launch({channel:'chrome',headless:true,args:['--enable-webgl','--ignore-gpu-blocklist']});const p=await b.newPage({viewport:{width:1440,height:1000}});
await p.goto('http://127.0.0.1:8420/',{waitUntil:'networkidle'});await p.waitForFunction(()=>window.__viewer?.ready);
await p.click('[data-view="pb"]');await p.waitForTimeout(1300);await p.locator('#cut').fill('4.5');await p.locator('#cut').dispatchEvent('input');
const report={cut:await p.evaluate(()=>({label:document.getElementById('view-name').textContent,output:document.getElementById('cut-value').textContent,actual:__viewer.renderer.clippingPlanes[0].constant}))};
await p.screenshot({path:'D:/2026/42/audit/web_cut_label_01.png'});
report.wood=await p.evaluate(()=>{const seen=new Set(),data=[];for(const o of __viewer.originals){const m=o.material;if(!m.name?.match(/Roble|Nogal|parquet|wood|Madera/i)||seen.has(m.uuid))continue;seen.add(m.uuid);data.push({name:m.name,map:!!m.map,normal:!!m.normalMap,roughnessMap:!!m.roughnessMap,roughness:m.roughness,color:m.color.toArray()});}return data;});
for(const key of ['mono','acceso','vestidor']){await p.click('[data-view="'+key+'"]');await p.waitForTimeout(1400);await p.screenshot({path:'D:/2026/42/audit/web_'+key+'_independent.png'});}
fs.writeFileSync('D:/2026/42/audit/web_detail_checks_01.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report));await b.close();