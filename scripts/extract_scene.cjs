const fs=require('fs'),vm=require('vm'),zlib=require('zlib'),path=require('path');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'source');
const source=fs.readFileSync(path.join(OUT,'original.html'),'utf8').match(/<script id="engineSource"[^>]*>([\s\S]*?)<\/script>/)[1];
fs.writeFileSync(path.join(OUT,'engine.js'),source);
const noop=()=>{};
const gl=new Proxy({getExtension:()=>null,getParameter:()=>8192,getShaderParameter:()=>true,getProgramParameter:()=>true,getShaderInfoLog:()=>'',getProgramInfoLog:()=>'',getError:()=>0}, {get(t,k){if(k in t)return t[k];if(/^[A-Z0-9_]+$/.test(k))return k;return ()=>({});}});
const ctx=new Proxy({getImageData:(x,y,w,h)=>({data:new Uint8ClampedArray(w*h*4)}),createImageData:(w,h)=>({data:new Uint8ClampedArray(w*h*4)}),measureText:()=>({width:100})},{get:(t,k)=>k in t?t[k]:()=>({addColorStop:noop}),set:(t,k,v)=>(t[k]=v,true)});
const element=()=>new Proxy({style:{},classList:{add:noop,remove:noop,toggle:noop,contains:()=>false},children:[{},{}],dataset:{},getContext:k=>k==='webgl2'?gl:ctx,addEventListener:noop,querySelector:()=>element(),querySelectorAll:()=>[],getBoundingClientRect:()=>({width:1600,height:1000,left:0,top:0}),appendChild:noop,setAttribute:noop},{get:(t,k)=>k in t?t[k]:noop});
const document={getElementById:()=>element(),createElement:()=>element(),body:element(),addEventListener:noop,querySelector:()=>element(),querySelectorAll:()=>[],hidden:false};
const sandbox={console,document,navigator:{maxTouchPoints:0},matchMedia:()=>({matches:false,addEventListener:noop}),performance:{now:()=>0},requestAnimationFrame:noop,setTimeout:noop,clearTimeout:noop,Blob:class{},URL:{createObjectURL:()=>'',revokeObjectURL:noop},Image:class{},devicePixelRatio:1,innerWidth:1600,innerHeight:1000};
sandbox.window=sandbox;sandbox.addEventListener=noop;sandbox.localStorage={getItem:()=>null,setItem:noop};sandbox.ArchStudio={onReady:noop,fail:noop};
vm.createContext(sandbox);
vm.runInContext(source.replace(/init\(\)\.catch\(function\(error\)[^\n]*/,''),sandbox,{timeout:10000,filename:'engine.js'});
vm.runInContext("uploadPixels=function(data,size,srgb){return {data:Array.from(data),size,srgb};}; configureLighting(); configurePhysicalMaterials();",sandbox);
console.log('Generating original matched PBR textures...');
vm.runInContext('buildTextures(); buildScene();',sandbox,{timeout:180000});
const exportScene=()=>{
 const geos=[],gm=new Map(),mid=new Map(Object.entries(materials).map(([k,v])=>[v,k]));
 const meshIds=new Map(scene.meshes.map((m,i)=>[m,i]));
 const arr=a=>a?Array.from(a):null;
 const meshes=scene.meshes.map((m,i)=>{
  if(!gm.has(m.geometry)){gm.set(m.geometry,geos.length);const c=m.geometry.cpu;geos.push({positions:arr(c.positions),normals:arr(c.normals),uvs:arr(c.uvs),indices:arr(c.indices)});}
  const userData={};for(const [k,v] of Object.entries(m.userData)){if(k==='linkedMeshes')userData[k]=v.map(x=>meshIds.get(x)).filter(x=>x!==undefined);else if(typeof v!=='object'||Array.isArray(v)||ArrayBuffer.isView(v))userData[k]=ArrayBuffer.isView(v)?arr(v):v;}
  return {id:i,name:m.name,geometry:gm.get(m.geometry),material:mid.get(m.material),layer:m.layer,position:arr(m.position),scale:arr(m.scale),rotation:arr(m.rotation),matrix:arr(m.model),visible:m.visible,userData,instances:arr(m.instanceCPU),vegetation:m.vegetation||0};
 });
 const doors={};for(const [k,v] of Object.entries(scene.doors))doors[k]=v.map(m=>meshIds.get(m)).filter(x=>x!==undefined);
 return JSON.stringify({config:CONFIG,materials,profiles:materialProfiles,geometries:geos,meshes,doors,doorSpecs:ARCH_DOORS,views:ARCH_VIEWS,colliders:scene.colliders,checks:architectureChecks(),textures:textures,surfaces:surfaceTextures,normals:normalTextures},(k,v)=>ArrayBuffer.isView(v)?Array.from(v):v);
};
const data=JSON.parse(vm.runInContext('('+exportScene.toString()+')()',sandbox,{timeout:180000}));
const textures=data.textures,surfaces=data.surfaces,normals=data.normals;delete data.textures;delete data.surfaces;delete data.normals;
fs.writeFileSync(path.join(OUT,'scene.json'),JSON.stringify(data));
const table=Array.from({length:256},(_,n)=>{for(let k=0;k<8;k++)n=n&1?0xedb88320^(n>>>1):n>>>1;return n>>>0;});
function crc(buf){let c=0xffffffff;for(const b of buf)c=table[(c^b)&255]^(c>>>8);return (c^0xffffffff)>>>0;}
function chunk(type,buf){const t=Buffer.from(type),n=Buffer.alloc(4),c=Buffer.alloc(4);n.writeUInt32BE(buf.length);c.writeUInt32BE(crc(Buffer.concat([t,buf])));return Buffer.concat([n,t,buf,c]);}
function png(file,t){const s=t.size,h=Buffer.alloc(13);h.writeUInt32BE(s,0);h.writeUInt32BE(s,4);h[8]=8;h[9]=6;const raw=Buffer.alloc((s*4+1)*s),pixels=Buffer.from(t.data);
for(let y=0;y<s;y++)pixels.copy(raw,y*(s*4+1)+1,y*s*4,(y+1)*s*4);
fs.writeFileSync(file,Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),chunk('IHDR',h),chunk('IDAT',zlib.deflateSync(raw)),chunk('IEND',Buffer.alloc(0))]));}
fs.mkdirSync(path.join(OUT,'textures'),{recursive:true});
for(const [kind,group] of Object.entries({albedo:textures,surface:surfaces,normal:normals}))for(const [name,t] of Object.entries(group))if(t.data)png(path.join(OUT,'textures',name+'_'+kind+'.png'),t);
fs.writeFileSync(path.join(OUT,'inventory.txt'),data.meshes.map(m=>m.id+'\t'+m.layer+'\t'+m.name+'\t'+m.material+'\t'+m.position.join(',')+'\t'+m.scale.join(',')).join('\n'));
console.log(JSON.stringify({meshes:data.meshes.length,geometries:data.geometries.length,instances:data.meshes.reduce((a,m)=>a+(m.instances?.length||0)/16,0),doors:data.doors,checks:data.checks},null,2));