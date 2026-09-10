import {chromium} from '../web-tools/node_modules/playwright/index.mjs';import fs from 'node:fs';
const b=await chromium.launch({channel:'chrome',headless:true,args:['--enable-webgl','--ignore-gpu-blocklist']});const p=await b.newPage({viewport:{width:1440,height:1000}});
await p.goto('https://gatdeguin.github.io/42/',{waitUntil:'networkidle'});await p.waitForFunction(()=>window.__viewer?.ready);
const report=await p.evaluate(()=>{
 const materials=new Map();for(const o of __viewer.originals){for(const m of (Array.isArray(o.material)?o.material:[o.material])){
 if(!materials.has(m.uuid))materials.set(m.uuid,{name:m.name,type:m.type,objects:0,maps:{color:!!m.map,normal:!!m.normalMap,bump:!!m.bumpMap,roughness:!!m.roughnessMap,metalness:!!m.metalnessMap,ao:!!m.aoMap,light:!!m.lightMap,emissive:!!m.emissiveMap},roughness:m.roughness,metalness:m.metalness,transparent:m.transparent,opacity:m.opacity,transmission:m.transmission||0});
 materials.get(m.uuid).objects++;
 }}
 const rows=Array.from(materials.values());return {url:location.href,stats:__viewer.stats,materials:rows,coverage:Object.fromEntries(['color','normal','bump','roughness','ao','light'].map(k=>[k,rows.filter(m=>m.maps[k]).length]))};
});
fs.writeFileSync('audit/integral95_web_materials.json',JSON.stringify(report,null,2));console.log(JSON.stringify({materials:report.materials.length,coverage:report.coverage,stats:report.stats}));await b.close();
