import bpy,bmesh,json
from mathutils import Vector
dg=bpy.context.evaluated_depsgraph_get();out=[]
for o in bpy.context.scene.objects:
 if o.type!='MESH' or not any(w in o.name for w in ['Canaleta','Bajada']):continue
 e=o.evaluated_get(dg);m=e.to_mesh();bm=bmesh.new();bm.from_mesh(m);bm.transform(o.matrix_world)
 ps=[v.co.copy() for v in bm.verts];mi=[min(p[k] for p in ps) for k in range(3)];ma=[max(p[k] for p in ps) for k in range(3)];bbox=(ma[0]-mi[0])*(ma[1]-mi[1])*(ma[2]-mi[2]);vol=abs(bm.calc_volume(signed=True))
 origin=Vector(((mi[0]+ma[0])/2,(mi[1]+ma[1])/2,ma[2]+.2));local=o.matrix_world.inverted()@origin;direct=o.matrix_world.inverted().to_3x3()@Vector((0,0,-1));hit,point,normal,idx=o.ray_cast(local,direct)
 out.append({'name':o.name,'min':mi,'max':ma,'volume_m3':vol,'bbox_volume_m3':bbox,'solid_fraction':vol/bbox if bbox else None,'top_center_hit':list(o.matrix_world@point) if hit else None})
 bm.free();e.to_mesh_clear()
json.dump(out,open(r'D:\2026\42\audit\integral95_rainwater_meshes.json','w',encoding='utf8'),ensure_ascii=False,indent=2)
print(json.dumps(out,ensure_ascii=False))
