"""Read-only island use-envelope intersections on R7D; no source save."""
exec(compile((__import__('pathlib').Path(r'D:\2026\42')/'audit/r7d_island_probe.py').read_text(encoding='utf-8'),'island_inventory','exec'))
def create_box(name,x,h,z):
 v=[(xx,-zz,hh) for xx,zz,hh in [(x[0],z[0],h[0]),(x[1],z[0],h[0]),(x[1],z[1],h[0]),(x[0],z[1],h[0]),(x[0],z[0],h[1]),(x[1],z[0],h[1]),(x[1],z[1],h[1]),(x[0],z[1],h[1])]]
 f=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
 m=bpy.data.meshes.new(name);m.from_pydata(v,[],f);m.update();o=bpy.data.objects.new(name,m);S.collection.objects.link(o);return o
def intersection_box(o,x,h,z):
 test=create_box('AUDIT KNEE TEMP',x,h,z); v,f=geometry(o);m=bpy.data.meshes.new('AUDIT TARGET TEMP');m.from_pydata(v,[],f);m.update();target=bpy.data.objects.new('AUDIT TARGET TEMP',m);S.collection.objects.link(target)
 try:
  mod=test.modifiers.new('Exact directed intersection','BOOLEAN');mod.operation='INTERSECT';mod.solver='EXACT';mod.object=target;DG.update();e=test.evaluated_get(DG);em=e.to_mesh();bm=bmesh.new();bm.from_mesh(em);volume=abs(bm.calc_volume(signed=True));bm.free();e.to_mesh_clear();return volume
 finally:
  for q in [test,target]:qm=q.data;bpy.data.objects.remove(q,do_unlink=True);bpy.data.meshes.remove(qm)
def run_envelope(label,seat,x,h,z):
 checks=[]
 for obj in island:
  b=bounds(obj)
  if all(min(pair[1],b[k][1])-max(pair[0],b[k][0])>1e-7 for k,pair in [('x',x),('h',h),('z',z)]):
   v=intersection_box(obj,x,h,z)
   if v>1e-10:checks.append(dict(object=obj.name,volume_m3=v))
 return dict(label=label,seat=seat.name,envelope={'x':x,'h':h,'z':z},intersections=checks)
tests=[]
for seat in seats:
 sb=bounds(seat);xc=sum(sb['x'])/2;zc=sum(sb['z'])/2;sh=sb['h'][1]
 tests.append(run_envelope('NKBA-inspired width/depth reserve with auditor selected vertical band',seat,[xc-.305,xc+.305],[sh+.04,sh+.16],[tb['z'][0],tb['z'][0]+.381]))
 for depth in [.5,.55,.6]:
  for side in [-1,1]:
   tests.append(run_envelope('Declared knee proxy; hip-to-forward-bound='+str(depth)+'m, side='+str(side),seat,[xc+side*.10-.06,xc+side*.10+.06],[sh+.04,sh+.16],[zc+.19,zc+depth]))
report['useEnvelopes']=tests
report['proxyLimitations']='Two 120mm wide envelopes at X +/-100mm, H seat+40..160mm, front of seat to hip+500/550/600mm. These are explicit geometric sensitivity scenarios, not anthropometric percentiles or a complete seated person. NKBA depth/width reference does not prescribe the chosen vertical band.'
report['mirrorInventory']=[entry(o) for o in S.objects if o.type=='MESH' and ('espejo' in o.name.lower() or ('baño quincho' in o.name.lower() and 'pared' in o.name.lower()))]
(OUT/'island_use_envelopes.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('ENVELOPE_DONE',len(tests),sum(bool(t['intersections']) for t in tests),flush=True)
for t in tests: print(t['seat'],t['label'],[(q['object'],round(q['volume_m3']*1e6,3)) for q in t['intersections']])
for m in report['mirrorInventory']:print('MIRROR',m)
