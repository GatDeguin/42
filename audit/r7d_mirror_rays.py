"""Mirror ray direction diagnostic; analytical specular rays, no renderer or source save."""
exec(compile((__import__('pathlib').Path(r'D:\2026\42')/'audit/r7d_mirror_probe.py').read_text(encoding='utf-8'),'mirror_inventory','exec'))
samples=[]
for name,cam in [('Espejo baño pileta','REV | Baño quincho'),('Espejo baño suite','LUZ99 | Bano suite humano'),('Espejo baño mono','REV | Baño mono sanitarios')]:
 item=next(q for q in items if q['name']==name);camera=bpy.data.objects[cam].matrix_world.translation
 for face in item['evaluated_faces']:
  vs=[Vector(p) for p in face['vertices']];gn=Vector(face['geometric_normal'])
  if len(vs)!=3 or gn.dot(camera-sum(vs,Vector())/3)<=0:continue
  ns=[Vector(n) for n in face['corners']]
  for weights in [(1/3,1/3,1/3),(.8,.1,.1),(.1,.8,.1),(.1,.1,.8),(.45,.45,.1),(.1,.45,.45),(.45,.1,.45)]:
   p=sum((v*w for v,w in zip(vs,weights)),Vector());sn=sum((n*w for n,w in zip(ns,weights)),Vector()).normalized();inc=(p-camera).normalized()
   ideal=(inc-2*inc.dot(gn)*gn).normalized();actual=(inc-2*inc.dot(sn)*sn).normalized()
   targets={}
   for label,d in [('plane',ideal),('interpolatedNormal',actual)]:
    hit,loc,n,idx,obj,matrix=S.ray_cast(DG,p+d*.0005,d,distance=30)
    targets[label]=dict(hit=hit,object=obj.name if obj else None,position=list(loc) if hit else None)
   samples.append(dict(mirror=name,camera=cam,face=face['index'],barycentric=weights,normalDeviationDegrees=math.degrees(gn.angle(sn)),reflectedRayDeviationDegrees=math.degrees(ideal.angle(actual)),targets=targets))
report['reflectionSamples']=samples
report['scope']='Ideal first-bounce reflection direction using geometric face normal compared with the interpolated custom corner normal; material roughness not sampled. This is not a substitute render or proof that all reflected wall UVs are correct.'
(R/'audit/r7d_preliminary/mirror_rays.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
for n in ['Espejo baño pileta','Espejo baño suite','Espejo baño mono']:
 a=[q for q in samples if q['mirror']==n];print('RAYS',n,len(a),'maxDeg',max(q['reflectedRayDeviationDegrees'] for q in a))
print('MIRROR_RAYS_DONE',flush=True)
