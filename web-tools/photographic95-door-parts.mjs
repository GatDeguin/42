import fs from 'node:fs';import {Matrix4} from 'three';
export function addDoorPartMotion(document,info){
 const reference=JSON.parse(fs.readFileSync('docs/preview95/assets/source-envelopes.json'));if(reference.sourceSHA256!==info.stats.source_sha256)throw new Error('Door motion reference SHA differs');
 const nodes=new Map(document.getRoot().listNodes().map(n=>[n.getExtras().label||n.getName(),n]));let count=0;
 for(const d of info.doors)d.parts=[];
 for(const row of reference.rows){
  const a=row.closed.localMatrixThree,b=row.open?.localMatrixThree;if(!a||!b||!b.some((v,i)=>Math.abs(v-a[i])>1e-5))continue;
  const node=nodes.get(row.webLabel);if(!node)throw new Error('Moving door part absent '+row.webLabel);
  const original=node.getMatrix(),closed={position:node.getTranslation(),quaternion:node.getRotation(),scale:node.getScale()};
  const matrix=new Matrix4().fromArray(b).multiply(new Matrix4().fromArray(a).invert()).multiply(new Matrix4().fromArray(original));node.setMatrix(matrix.elements);
  const open={position:node.getTranslation(),quaternion:node.getRotation(),scale:node.getScale()};node.setMatrix(original);
  info.doors.find(d=>d.name===row.door).parts.push({label:row.webLabel,closed,open});count++;
 }
 info.stats.animatedDoorParts=count;console.log('DOOR_PART_MOTION',count);return count;
}
