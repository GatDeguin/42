import bpy,os,json
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);dep=bpy.context.evaluated_depsgraph_get()
p=Vector((16.5,-16.5,.07));hits=[]
for i in range(10):
 hit,loc,n,idx,obj,mat=S.ray_cast(dep,p,Vector((0,0,-1)),distance=5)
 if not hit:break
 hits.append([obj.name,list(loc)]);p=loc-Vector((0,0,.002))
print('POOL_SUBSURFACE_RAY',hits,flush=True)
