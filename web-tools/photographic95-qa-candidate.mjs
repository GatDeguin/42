import fs from 'node:fs';const f='web-tools/photographic95-qa.mjs';let s=fs.readFileSync(f,'utf8');
s=s.replace("const report={created:","const baseURL=new URL(process.env.PHOTO95_URL||'http://127.0.0.1:8420/preview95/'),candidate=baseURL.searchParams.has('candidate'),capturePrefix=candidate?'candidate-':'';baseURL.searchParams.set('mode','raster');\nconst report={sourceURL:baseURL.href,created:");
s=s.replace("'docs/preview95/screenshots/'+name", "'docs/preview95/screenshots/'+capturePrefix+name");
s=s.replace("'http://127.0.0.1:8420/preview95/?mode=raster'",'baseURL.href');
s=s.replace("'http://127.0.0.1:8420/preview95/'",'baseURL.href');
// Restore the literal default URL above after replacing usages.
s=s.replace("process.env.PHOTO95_URL||baseURL.href", "process.env.PHOTO95_URL||'http://127.0.0.1:8420/preview95/'");
s=s.replace('i<40','i<64');
s=s.replace("fs.writeFileSync('docs/preview95/benchmarks.json'", "fs.writeFileSync('docs/preview95/'+(candidate?'benchmarks-candidate.json':'benchmarks.json')");
s=s.replace("report.pathExterior=await page.evaluate(()=>__viewer.photo.metrics);await shot", "report.pathExterior=await page.evaluate(()=>__viewer.photo.metrics);if(report.pathExterior.error||report.pathExterior.samples<32)throw new Error('Path trace failed to converge: '+JSON.stringify(report.pathExterior));await shot");
fs.writeFileSync(f,s);
const b='web-tools/photographic95-build.mjs';s=fs.readFileSync(b,'utf8');s=s.replace("js=js.replace('selectView,setAllDoors,get camera()'", "js=js.replace('downloadBytes:metadata.stats.downloadBytes','sourceModel:metadata.stats.source_model,sourceSHA:metadata.stats.source_sha256,downloadBytes:metadata.stats.downloadBytes');\njs=js.replace('selectView,setAllDoors,get camera()'");fs.writeFileSync(b,s);
