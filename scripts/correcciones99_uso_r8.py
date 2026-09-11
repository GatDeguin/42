"""R8 use correction: MIDI tray/support and two island dining places.
apply() is idempotent; no save/render. --preview saves a separate source-derived file.
Dimensions/proposals do not certify product ergonomics or load capacity.
"""
import bpy,bmesh,json,math
from mathutils import Vector
PREFIX='USO99 | '
KEY='r8_uso_details'
def sb(o):
 p=[o.matrix_world@Vector(v) for v in o.bound_box];return {'x':[min(q.x for q in p),max(q.x for q in p)],'h':[min(q.z for q in p),max(q.z for q in p)],'z':[min(-q.y for q in p),max(-q.y for q in p)]}
def apply():
 S=bpy.context.scene
 if KEY in S:return json.loads(S[KEY])
 assert 'r7_layout' in S and 'door_hands99_v1' in S,'Requires integrated R7 layout/hands'
 S.frame_set(1);bpy.context.view_layer.update();old={};changed=[];created=[]
 C=bpy.data.collections.new('99 | Uso R8 P');S.collection.children.link(C)
 mats={}
 for key,c,r,met in [('steel',(.055,.065,.066,1),.3,.8),('tray',(.075,.08,.08,1),.42,.05),('rubber',(.025,.029,.025,1),.65,0)]:
  m=bpy.data.materials.new('USO99 | '+key);m.diffuse_color=c;m.use_nodes=True;m.node_tree.nodes.clear();bs=m.node_tree.nodes.new('ShaderNodeBsdfPrincipled');out=m.node_tree.nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(bs.outputs['BSDF'],out.inputs['Surface']);bs.inputs['Base Color'].default_value=c;bs.inputs['Roughness'].default_value=r;bs.inputs['Metallic'].default_value=met;mats[key]=m
 def mesh(n,v,f,k,zone):
  me=bpy.data.meshes.new(PREFIX+n);me.from_pydata([(x,-z,h) for x,h,z in v],[],f);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();o=bpy.data.objects.new(PREFIX+n,me);C.objects.link(o)
  col=bpy.data.collections.get(zone)
  if col:col.objects.link(o)
  o.data.materials.append(mats[k]);o['detail_status']='P / dimensions and contacts; product, connections and load capacity require project';created.append(o.name);return o
 def box(n,x,h,z,k='steel',zone='STUDIO'):
  return mesh(n,[(xx,hh,zz) for hh in h for zz in z for xx in x],[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)],k,zone)
 def tube(n,a,b,w,t,k='steel',zone='STUDIO'):
  # Rectangular hollow section, outer dimensions w x t, wall2mm, end annuli.
  av,bv=Vector(a),Vector(b);axis=(bv-av).normalized();u=axis.cross(Vector((0,1,0)))
  if u.length<.1:u=axis.cross(Vector((1,0,0)))
  u.normalize();v=axis.cross(u).normalized();pts=[]
  for pos in [av,bv]:
   for ww,tt in [(w,t),(w-.004,t-.004)]:
    for xx,yy in [(-1,-1),(1,-1),(1,1),(-1,1)]:pts.append(tuple(pos+u*xx*ww/2+v*yy*tt/2))
  faces=[]
  for i in range(4):
   j=(i+1)%4;faces.extend([(i,j,j+8,i+8),(i+4,i+12,j+12,j+4),(i,i+4,j+4,j),(i+8,j+8,j+12,i+12)])
  return mesh(n,pts,faces,k,zone)
 def touch(o):
  if o.name not in old:old[o.name]=sb(o);changed.append(o.name)
 def remap(o,axis,lo,hi):
  touch(o);bpy.context.view_layer.update();pts=[o.matrix_world@v.co for v in o.data.vertices];vals=[(p.x,p.z,-p.y)[axis] for p in pts];mn,mx=min(vals),max(vals);inv=o.matrix_world.inverted();o.data=o.data.copy()
  for v,p,t in zip(o.data.vertices,pts,vals):
   val=lo+(t-mn)/(mx-mn)*(hi-lo)
   if axis==0:p.x=val
   elif axis==1:p.z=val
   else:p.y=-val
   v.co=inv@p
  o.data.update()
 def move(o,dx=0,dh=0,dz=0):touch(o);o.location+=Vector((dx,-dz,dh))
 def difference(o,c):
  touch(o);bpy.context.view_layer.update();bpy.context.view_layer.objects.active=o;m=o.modifiers.new('R8 local clearance','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=c;bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(c,do_unlink=True)
 # Island: unchanged work edge/counter/floor, shallower cabinet and steel end frames.
 family=[o for o in S.objects if o.type=='MESH' and o.name.startswith('Isla cocina mono base |')]
 for o in family:
  n=o.name
  if n.endswith('fondo'):remap(o,2,3.720,3.738)
  elif n.endswith('piso') or 'costilla' in n:remap(o,2,3.738,3.960)
  elif 'travesaño' in n:
   if sb(o)['z'][0]<3.8:remap(o,2,3.738,3.778)
   else:remap(o,2,3.910,3.925)
  elif 'zócalo' in n:remap(o,2,3.780,3.900)
 for p,dx in [('Taburete isla mono A |',.030),('Taburete isla mono B |',-.090)]:
  for o in list(S.objects):
   if o.name.startswith(p):move(o,dx=dx)
  bpy.context.view_layer.update();cx=16.350 if ' A |' in p else 17.290
  for o in list(S.objects):
   if not o.name.startswith(p) or 'asiento 30' in o.name:continue
   b=sb(o)
   if ' X ' in o.name:remap(o,0,cx-.1525,cx+.1525)
   else:move(o,dx=(-.0175 if sum(b['x'])/2<cx else .0175))
 # Two end portals outside the610mm wide knee zones, continuous20mm-high rails.
 for k,x in enumerate([15.985,17.655]):
  for j,z in enumerate([3.365,3.940]):
   box(f'isla apoyo elastomerico {k}{j}',[x-.020,x+.020],[.210,.215],[z-.020,z+.020],'rubber','GROUND_FLOOR')
   tube(f'isla montante {k}{j}',(x,.215,z),(x,1.052,z),.025,.025,zone='GROUND_FLOOR')
  tube(f'isla larguero extremo {k}',(x,1.062,3.3525),(x,1.062,3.9525),.025,.020,zone='GROUND_FLOOR')
 for j,z in enumerate([3.365,3.940]):
  tube(f'isla travesano superior {j}',(15.9975,1.062,z),(17.6425,1.062,z),.025,.020,zone='GROUND_FLOOR')
  box(f'isla asiento elastomerico tapa {j}',[15.9725,17.6675],[1.072,1.075],[z-.0125,z+.0125],'rubber','GROUND_FLOOR')
 #2mm installation gap around new rear metal rail in the three timber ribs.
 for o in family:
  if 'costilla' in o.name:
   cutter=box('temporary island steel pocket',[15.999,17.641],[1.050,1.076],[3.9255,3.9545],zone='GROUND_FLOOR');cn=cutter.name;difference(o,cutter)
   if cn in created:created.remove(cn)
 # MIDI compact400mm body, input plane750mm above finished floor, original1080mm width.
 body=S.objects['Controlador estudio'];remap(body,0,18.510,18.910)
 midinames=[]
 for o in list(S.objects):
  if o.name=='Controlador estudio' or o.name.startswith(('MAT95 | tecla natural','MAT95 | tecla sostenido','MAT95 | pad MIDI','MAT95 | pantalla controlador','MAT95 | encoder maestro')):
   midinames.append(o.name);move(o,dh=-.1095)
   if o.name.startswith('MAT95 | pad MIDI'):
    x=sb(o)['x'];cx=sum(x)/2;dx=(18.560 if cx<18.34 else 18.635)-cx;move(o,dx=dx,dh=-.0015)
   elif o.name.startswith('MAT95 | pantalla controlador'):remap(o,0,18.530,18.620);remap(o,2,3.120,3.300);move(o,dh=-.0015)
   elif o.name.startswith('MAT95 | encoder maestro'):move(o,dx=.125,dh=-.002)
 # Actual tray entirely below new enclosure; local notch leaves mixing surface intact.
 cutter=box('temporary console recess',[18.475,18.956],[3.740,4.200],[2.385,3.615])
 cname=cutter.name;difference(S.objects['Consola estudio'],cutter)
 if cname in created:created.remove(cname)
 # Root steel passes below retained mixing top through two local underside pockets.
 for z in [2.430,3.570]:
  cutter=box('temporary console underside pocket',[18.205,18.478],[3.740,3.922],[z-.035,z+.035])
  cname=cutter.name;difference(S.objects['Consola estudio'],cutter)
  if cname in created:created.remove(cname)
 box('MIDI bandeja18',[18.490,18.940],[3.915,3.933],[2.405,3.595],'tray')
 for k,z in enumerate([2.430,3.570]):
  box(f'MIDI placa asiento base {k}',[18.220,18.520],[3.863,3.867],[z-.030,z+.030])
  #3mm proposed fillet welds physically join each root plate to existing steel base.
  for side in [-1,1]:
   edge=z+side*.030;tri=[(3.863,edge),(3.866,edge),(3.863,edge+side*.003)]
   vv=[(x,h,zz) for x in [18.225,18.515] for h,zz in tri]
   mesh(f'MIDI soldadura base {k} {side}',vv,[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],'steel','STUDIO')
  box(f'MIDI calce8 {k}',[18.240,18.500],[3.867,3.875],[z-.015,z+.015])
  tube(f'MIDI brazo40x30 {k}',(18.220,3.895,z),(18.940,3.895,z),.030,.040)
  # A welded root plate and arm are a proposed steel connection, not a calculated joint.
  for j,x in enumerate([18.245,18.490]):box(f'MIDI cordon soldadura {k}{j}',[x-.008,x+.008],[3.867,3.875],[z+.014,z+.019])
 for k,x in enumerate([18.550,18.870]):
  for j,z in enumerate([2.500,3.500]):box(f'MIDI apoyo elastomerico {k}{j}',[x-.025,x+.025],[3.933,3.936],[z-.025,z+.025],'rubber')
 # Discrete enclosure stops touch side walls; tray remains horizontally supported.
 for k,z in enumerate([2.455,3.545]):box(f'MIDI tope lateral {k}',[18.570,18.650],[3.933,3.947],[z-.005,z+.005],'rubber')
 bpy.context.view_layer.update()
 result={'version':3,'status':'P / first correction pass; independent assessment pending','changed_objects':changed,'created_objects':created,'before_bounds_source':old,'after_bounds_source':{n:sb(S.objects[n]) for n in changed+created if n in S.objects},'island':{'counter_mm':[1720,680,35],'counter_height_m':.900,'seat_height_m':.650,'knee_depth_m':.400,'knee_zone_width_m':.610,'seat_centres_source':[[16.350,.860,3.050],[17.290,.860,3.050]],'cabinet_internal_depth_m':.222,'stool_front_leg_clearance_m':.305,'stool_frame_outer_width_m':.375,'support':'steel end portals and hollow25x20mm perimeter beams, elastomer3mm against concrete top; sizing and fastening pending'},'midi':{'body_mm':[400,1080,55],'white_key_height_m':.750,'black_key_height_m':.7625,'seat_height_m':.470,'tray_underside_height_m':.665,'primary_use':'keys; relaxed elbow trial atseat+280mm','support':'two40x30x2mm cantilever arms on existing steel base, rootplate4+spacer8 and3mm proposed fillets to existing steel base; tray18+fourpad3mm; weld/strength selection pending','controller_family':midinames},'limits':['Body/seat/hand envelopes are declared trial geometry, not anthropometric percentiles.','Structural capacity, vibration, welds and furniture anchorage need professional/product selection.','Original architectural floors, openings, SAN99, C2/C3 and doors unchanged.']}
 S[KEY]=json.dumps(result,ensure_ascii=False);return result
if __name__=='__main__':
 import sys,hashlib
 from pathlib import Path
 a=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
 r=apply()
 if '--preview' in a:
  R=Path(__file__).resolve().parent.parent;out=R/'output/Casa_de_Campo_99_R8_uso_preview.blend';bpy.ops.wm.save_as_mainfile(filepath=str(out));d=R/'review99/r8_uso';d.mkdir(parents=True,exist_ok=True);r.update(model=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest());(d/'details.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),'utf8');print(json.dumps({'model':str(out),'sha256':r['sha256'],'changed':len(r['changed_objects']),'created':len(r['created_objects'])}),flush=True)
