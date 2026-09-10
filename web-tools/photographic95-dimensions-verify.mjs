import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';
import {NodeIO} from '@gltf-transform/core';import {ALL_EXTENSIONS} from '@gltf-transform/extensions';import {MeshoptDecoder} from 'meshoptimizer';
await MeshoptDecoder.ready;
const dir=process.env.PHOTO95_ASSET_DIR||'docs/preview95/assets/',reference=JSON.parse(fs.readFileSync(dir+'source-envelopes.json')),info=JSON.parse(fs.readFileSync(dir+'model-info.json'));
assert.equal(reference.sourceSHA256,info.stats.source_sha256,'Source bounds and GLB differ');assert.equal(reference.sourceMetresPerUnit,1);assert.equal(info.stats.positionQuantizationBits,16,'Audit tolerance requires declared 16-bit positions');
const io=new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({'meshopt.decoder':MeshoptDecoder}),doc=await io.read(dir+'house.glb');
const nodes=doc.getRoot().listNodes(),labels=new Map();for(const n of nodes){const label=n.getExtras().label||n.getName();if(labels.has(label)&&n.getMesh())throw new Error('Ambiguous source label '+label);if(label)labels.set(label,n);}
function envelope(node){
 const min=[Infinity,Infinity,Infinity],max=[-Infinity,-Infinity,-Infinity],tol=[.00002,.00002,.00002];let count=0,quantized=false;const stack=[node];
 while(stack.length){const n=stack.pop(),mesh=n.getMesh();stack.push(...n.listChildren());if(!mesh)continue;const m=n.getWorldMatrix();
 for(const p of mesh.listPrimitives()){
  const a=p.getAttribute('POSITION'),v=[0,0,0];quantized ||= a.getNormalized();
  // getElement decodes normalized attributes. getArray alone would create giant bounds.
  for(let i=0;i<a.getCount();i++){
   a.getElement(i,v);for(let j=0;j<3;j++){const x=m[j]*v[0]+m[4+j]*v[1]+m[8+j]*v[2]+m[12+j];min[j]=Math.min(min[j],x);max[j]=Math.max(max[j],x);}count++;
  }
  if(a.getNormalized()){
   assert.equal(a.getComponentType(),5122,'Unexpected position quantization component');
   for(let j=0;j<3;j++)tol[j]=Math.max(tol[j],(Math.abs(m[j])+Math.abs(m[4+j])+Math.abs(m[8+j]))/32767+.00002);
  }
 }
 }
 assert(count>0,'No geometry below '+node.getName());return {min,max,toleranceMetres:tol,vertices:count,normalizedPositions:quantized};
}
function setDoors(state){for(const d of info.doors){const n=labels.get(d.name);assert(n,'Door rig absent '+d.name);const p=d[state];n.setTranslation(p.position).setRotation(p.quaternion).setScale(p.scale);for(const part of d.parts||[]){const child=labels.get(part.label),q=part[state];assert(child,'Door child absent '+part.label);child.setTranslation(q.position).setRotation(q.quaternion).setScale(q.scale);}}}
const rows=[],failures=[],missing=[];let maximumError=0,maximumTolerance=0;
for(const state of ['closed','open']){
 setDoors(state);
 for(const r of reference.rows){
  if(state==='open'&&!r.door)continue;const n=labels.get(r.webLabel);if(!n){missing.push(r.webLabel);continue;}
  const expected=r[state],actual=envelope(n),errors=expected.min.map((v,i)=>Math.max(Math.abs(v-actual.min[i]),Math.abs(expected.max[i]-actual.max[i]))),pass=errors.every((e,i)=>e<=actual.toleranceMetres[i]);
  maximumError=Math.max(maximumError,...errors);maximumTolerance=Math.max(maximumTolerance,...actual.toleranceMetres);
  const row={name:r.sourceName,state,door:r.door,expected,actual,errorMetres:errors,pass};rows.push(row);if(!pass)failures.push(row);
 }
}
setDoors('closed');
const report={source:reference.source,sourceSHA256:reference.sourceSHA256,glbSHA256:crypto.createHash('sha256').update(fs.readFileSync(dir+'house.glb')).digest('hex'),created:new Date().toISOString(),pass:missing.length===0&&failures.length===0,sourceMetresPerUnit:1,webMetresPerUnit:1,doors:info.doors.length,sourceObjects:reference.rows.length,comparisons:rows.length,maximumErrorMetres:maximumError,maximumToleranceMetres:maximumTolerance,quantizationBits:16,tolerance:'One signed 16-bit normalized quantization step transformed into world metres per axis, plus 0.02 mm for float export. Bounds use decoded normalized attributes.',omitted:reference.omitted,vegetationLOD:reference.vegetationLOD,missing:[...new Set(missing)],failures,rows,measurementNote:reference.measurementNote,unitSource:'https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#coordinate-system-and-units'};
fs.writeFileSync('docs/preview95/dimension-verification.json',JSON.stringify(report,null,2));console.log('METRE_ENVELOPE_QA',JSON.stringify({pass:report.pass,sourceObjects:report.sourceObjects,comparisons:report.comparisons,maximumError,maximumTolerance,failures:failures.slice(0,5),missing:report.missing.slice(0,20)}));assert(report.pass,'GLB source envelopes differ; see dimension-verification.json');
