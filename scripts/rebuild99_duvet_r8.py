"""R8 CPU duvet drape: single continuous head edge, exact fixed mattress collider."""
import bpy,math,time,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];out=R/'scripts/assets/r8';out.mkdir(parents=True,exist_ok=True);start=time.perf_counter();original=bpy.context.scene;original.frame_set(1);bpy.context.view_layer.update()
source=Path(bpy.data.filepath);sha=hashlib.sha256(source.read_bytes()).hexdigest();assert sha=='9cf1a0e2f1b1a6063a28942623f20bc25b1b1ef423471a284b052ed7acffc54e'
mattress=bpy.data.objects['Cama dormitorio colchón'];dg=bpy.context.evaluated_depsgraph_get();data=bpy.data.meshes.new_from_object(mattress.evaluated_get(dg),depsgraph=dg)
s=bpy.data.scenes.new('R8 duvet CPU drape laboratory');bpy.context.window.scene=s;s.render.threads_mode='FIXED';s.render.threads=4
c=bpy.data.objects.new('Exact unchanged mattress collider',data);s.collection.objects.link(c);c.matrix_world=mattress.matrix_world.copy();c.modifiers.new('Cloth collider','COLLISION');c.collision.thickness_outer=.0012;c.collision.cloth_friction=12
N,M=100,74;verts=[];faces=[]
for j in range(M+1):
 v=j/M
 for i in range(N+1):
  u=i/N;x=14.79+2.06*u;y=-8.29+1.34*v
  z=3.92+.009*math.sin(9*u+3*v)+.006*math.sin(7*v-2*u)
  # Place one continuous head seam; the old manually looped strip is removed.
  y+=.010*math.sin(u*5)*v**5
  if j==M and 10<=i<=90:z=3.8585
  verts.append((x,y,z))
for j in range(M):
 for i in range(N):
  a=j*(N+1)+i;faces.append((a,a+1,a+N+2,a+N+1))
me=bpy.data.meshes.new('Continuous duvet base grid');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Duvet gravity drape',me);s.collection.objects.link(o)
vg=o.vertex_groups.new(name='Placed continuous head edge');vg.add([M*(N+1)+i for i in range(10,91)],1,'REPLACE')
cloth=o.modifiers.new('Gravity and bending stiffness','CLOTH');q=cloth.settings;q.vertex_group_mass=vg.name;q.quality=10;q.mass=.38;q.air_damping=3;q.tension_stiffness=35;q.compression_stiffness=35;q.shear_stiffness=12;q.bending_stiffness=1.2;q.tension_damping=14;q.compression_damping=14;q.shear_damping=12;q.bending_damping=2
co=cloth.collision_settings;co.use_self_collision=True;co.self_distance_min=.006;co.distance_min=.0012;co.collision_quality=6
frames=100;cloth.point_cache.frame_start=1;cloth.point_cache.frame_end=frames
for frame in range(1,frames+1):
 s.frame_set(frame);ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());ev.to_mesh();ev.to_mesh_clear()
 if frame%10==0:print('R8_DUVET_FRAME',frame,round(time.perf_counter()-start,1),flush=True)
ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();report=dict(vertices=[list(v.co) for v in me.vertices],faces=faces,grid=[N,M],frames=frames,seconds=time.perf_counter()-start,method='Blender Cloth CPU, exact mattress collider; continuous placed head seam, gravity-set side/foot overhangs, no folded strip',sourceSHA256=sha,settings=dict(mass_parameter=.38,quality=10,bending_stiffness=1.2,self_distance_m=.006,object_distance_m=.0012));ev.to_mesh_clear()
(out/'blanket-drape-cache.json').write_text(json.dumps(report,separators=(',',':')),encoding='utf-8');assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
bpy.context.window.scene=original
for ob in list(s.objects):bpy.data.objects.remove(ob,do_unlink=True)
bpy.data.scenes.remove(s);print('R8_DUVET_CACHE_DONE',report['seconds'],flush=True)
