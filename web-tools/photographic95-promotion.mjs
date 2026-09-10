import {addDoorPartViewer} from './photographic95-door-viewer.mjs';
import fs from 'node:fs';import path from 'node:path';import {pathToFileURL} from 'node:url';
export function preparePromotion(out){
 let html=fs.readFileSync(path.join(out,'index.html'),'utf8'),js=fs.readFileSync(path.join(out,'viewer.js'),'utf8');
 if(!html.includes('href="../renders/"'))html=html.replace('<a href="../planos/">Planos ↗</a>','<a href="../planos/">Planos ↗</a><a href="../renders/">Renders ↗</a>');
 if(!html.includes('id="source-glb"'))html=html.replace('<a class="source-link" href="./README.md"', '<a id="source-glb" class="source-link" href="./assets/house.glb" download>Descargar modelo 3D · GLB ↧</a>\n<a id="source-blend" class="source-link" href="#" hidden>Descargar fuente Blender ↧</a>\n<a class="source-link" href="./README.md"');
 if(!html.includes('href="./controles.html"'))html=html.replace('<a id="source-glb"', '<a class="source-link" href="./controles.html" target="_blank" rel="noopener">Cómo recorrer la casa ↗</a>\n<a id="source-glb"');
 if(!html.includes('data-view="bathDining"'))html=html.replace('<button data-view="acceso"><span>10</span>Acceso</button>', '<button data-view="acceso"><span>10</span>Acceso</button><button data-view="bathDining" hidden><span>11</span>Baño/comedor</button>');
 if(!js.includes('camera-optics.js'))js="import {fitAuthoredCamera} from './camera-optics.js';\n"+js;
 if(!js.includes('metadata.viewerViews'))js=js.replace('  woodSurfaces=await fetch(',`  for(const binding of metadata.viewerViews||[]){
   const authored=metadata.cameras.find(c=>c.name===binding.camera);if(!authored)throw new Error('Missing authored camera: '+binding.camera);
   presets[binding.key]={label:binding.label,p:authored.position,t:authored.target,f:authored.fov,frustum:authored.frustum,presentationFrame:authored.presentationFrame};const button=document.querySelector('[data-view="'+binding.key+'"]');if(button)button.hidden=false;
  }
  if(metadata.downloads?.blender&&/^https?:\\/\\//.test(metadata.downloads.blender)){const link=$('source-blend');if(link){link.href=metadata.downloads.blender;link.hidden=false;}}
  woodSurfaces=await fetch(`);
 // Also upgrade a prototype already generated before camera optics were available.
 js=js.replace('f:authored.fov};','f:authored.fov,frustum:authored.frustum,presentationFrame:authored.presentationFrame};');
 if(!js.includes('if(v.presentationFrame!=null)'))js=js.replace(" if(key==='vestidor')setAllDoors(0);", " if(v.presentationFrame!=null)setAllDoors(v.presentationFrame>=105?1:0);\n else if(key==='vestidor')setAllDoors(0);");
 if(!js.includes('fitAuthoredCamera(camera,v)'))js=js.replace(' const endP=new THREE.Vector3(...v.p)', ' fitAuthoredCamera(camera,v);\n const targetFov=v.frustum?camera.fov:v.f;\n const endP=new THREE.Vector3(...v.p)').replace('camera.fov=v.f;', 'camera.fov=targetFov;').replace('endF:v.f}', 'endF:targetFov}');
 if(!js.includes('fitAuthoredCamera(camera,presets[currentView])'))js=js.replace('camera.aspect=w/h;camera.updateProjectionMatrix();', 'camera.aspect=w/h;fitAuthoredCamera(camera,presets[currentView]);camera.updateProjectionMatrix();');
 js=js.replace(" if(['exterior','pb','pa','pileta','huerta','acceso'].includes(key))endP", " if(!v.frustum&&['exterior','pb','pa','pileta','huerta','acceso'].includes(key))endP");
 if(!js.includes('get presets()'))js=js.replace('selectView,setAllDoors,get photo()', 'selectView,setAllDoors,get presets(){return presets;},get photo()');
 js=addDoorPartViewer(js);
 fs.writeFileSync(path.join(out,'index.html'),html);fs.writeFileSync(path.join(out,'viewer.js'),js);
 const cssPath=path.join(out,'viewer.css');let css=fs.readFileSync(cssPath,'utf8');if(!css.includes('.source-link[hidden]'))fs.appendFileSync(cssPath,'\n.source-link[hidden],.room-grid button[hidden]{display:none}\n');
 if(!css.includes('mobile-gallery-links'))fs.appendFileSync(cssPath,'\n/* mobile-gallery-links */\n@media(max-width:760px){.header-right{gap:10px}.header-right a[href*="github.com"]{display:none}}\n');
 let draft=html.replace('<meta charset="utf-8">',`<meta charset="utf-8"><base id="candidate-base" href="./preview95/"><script>if(location.pathname.endsWith('/preview95/root-index-candidate.html'))document.getElementById('candidate-base').href='./';</script>`);
 draft=draft.replace('class="brand" href="./"','class="brand" href="../"').replace('<span class="live">Prueba de iluminación</span>','').replace('</header>','<p class="review-state" role="status">En revisión · aprobación 9,5 pendiente</p></header>');
 draft=draft.replace('</head>',`<style>header{height:104px;padding-bottom:28px}.review-state{position:absolute;left:28px;bottom:7px;margin:0;font-size:12px;line-height:18px;color:#775135;letter-spacing:.1px}main,aside{top:104px}@media(max-width:760px){header{height:94px;padding-bottom:28px}.review-state{left:16px;font-size:11px}main,aside{top:94px}}</style></head>`);
 draft=draft.replace('<title>Casa de campo · Visor arquitectónico</title>','<title>Casa de campo · Modelo en revisión</title>');fs.writeFileSync(path.join(out,'root-index-candidate.html'),draft);
}
if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href){preparePromotion(path.resolve(import.meta.dirname,'../docs/preview95'));console.log('ROOT_INDEX_CANDIDATE_READY; production root untouched');}
