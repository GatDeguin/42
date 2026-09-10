import fs from 'node:fs';import crypto from 'node:crypto';import sharp from 'sharp';
const dir='docs/preview95/assets/oak-veneer-01',N=2048;const read=async f=>(await sharp(dir+'/'+f).removeAlpha().raw().toBuffer({resolveWithObject:true})).data;
const diffuse=await read('oak_veneer_01_diff_2k.png'),rough=await read('oak_veneer_01_rough_2k.png'),normal=await read('oak_veneer_01_nor_gl_2k.png');
const toLinear=x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4},toSRGB=x=>Math.round(255*(x<=.0031308?12.92*x:1.055*x**(1/2.4)-.055));
const means=[0,0,0];for(let i=0;i<diffuse.length;i++)means[i%3]+=toLinear(diffuse[i])/(N*N);const target=[.295,.174,.087].map(v=>v*1.08),factors=target.map((v,k)=>v/means[k]);const adjusted=Buffer.alloc(diffuse.length);for(let i=0;i<diffuse.length;i++)adjusted[i]=toSRGB(Math.min(1,toLinear(diffuse[i])*factors[i%3]));
await sharp(adjusted,{raw:{width:N,height:N,channels:3}}).jpeg({quality:95,chromaSubsampling:'4:4:4'}).toFile(dir+'/oak-calibrated-diffuse-2k.jpg');
const grainFloor=Buffer.alloc(N*N*3),roughFloor=Buffer.alloc(N*N*3),normalFloor=Buffer.alloc(N*N*3);
const fract=x=>x-Math.floor(x),random=(r,k,s)=>fract(Math.sin(r*127.1+k*311.7+s*74.7)*43758.5453123);
for(let y=0;y<N;y++)for(let x=0;x<N;x++){
 const cross=(x+.5)/N*1.44,long=(1-(y+.5)/N)*2.8,row=Math.floor(cross/.18),stagger=(row%2)*.7,segment=Math.floor((long+stagger)/1.4);
 const u=fract((cross% .18)/1.83+random(row,segment,1)),v=fract(((long+stagger)%1.4)/1.83+random(row,segment,2));const sx=Math.min(N-1,Math.floor(u*N)),sy=Math.min(N-1,Math.floor((1-v)*N)),from=(sy*N+sx)*3,to=(y*N+x)*3;
 const joint=cross% .18<.0015||(long+stagger)%1.4<.0015;
 for(let k=0;k<3;k++){grainFloor[to+k]=joint?toSRGB(toLinear(adjusted[from+k])*.32):adjusted[from+k];roughFloor[to+k]=joint?220:rough[from+k];normalFloor[to+k]=joint?(k===2?255:128):normal[from+k];}
}
await Promise.all([sharp(grainFloor,{raw:{width:N,height:N,channels:3}}).jpeg({quality:95,chromaSubsampling:'4:4:4'}).toFile(dir+'/oak-parquet-diffuse-2k.jpg'),sharp(roughFloor,{raw:{width:N,height:N,channels:3}}).png({compressionLevel:9}).toFile(dir+'/oak-parquet-roughness-2k.png'),sharp(normalFloor,{raw:{width:N,height:N,channels:3}}).png({compressionLevel:9}).toFile(dir+'/oak-parquet-normalGL-2k.png')]);
const files=['oak-calibrated-diffuse-2k.jpg','oak-parquet-diffuse-2k.jpg','oak-parquet-roughness-2k.png','oak-parquet-normalGL-2k.png'].map(file=>{const b=fs.readFileSync(dir+'/'+file);return{file,bytes:b.length,SHA256:crypto.createHash('sha256').update(b).digest('hex')}});
const result={sourceAsset:'oak_veneer_01',originalLinearMean:means,calibrationFactors:factors,calibratedLinearTarget:target,clearBaseFactor:[1/1.08,1/1.08,1/1.08,1],darkBaseFactor:[.1175/target[0],.063/target[1],.0305/target[2],1],parquetTileMetres:[1.44,2.8],parquetBoardsMetres:[.18,1.4],parquetJointMetres:.0015,notes:'Derived from the photographed asset, with per-channel linear colour calibration to existing light/dark timber means. Parquet rearranges photographic crops into existing board dimensions; joins remain material-only. No geometry changes.',files};fs.writeFileSync(dir+'/derived-provenance.json',JSON.stringify(result,null,2));console.log(result);
