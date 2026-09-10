import bpy,os,json,math
from mathutils import Vector,Matrix
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m}
def cv(p):return Vector((p[0],-p[2],p[1]))
def box(name,p,dims):
 x,y,z=[v/2 for v in dims];p0=[cv([a*x,b*y,c*z]) for a,b,c in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
 f=[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)]
 me=bpy.data.meshes.new(name);me.from_pydata(p0,[],f);me.materials.append(M['blackMetal']);o=bpy.data.objects.new(name,me);o.location=cv(p);bpy.data.collections['DOORS'].objects.link(o);return o
# Track separation must include frames, not only glass surfaces.
for key in ['mono_L','mono_R']:
 o=bpy.data.objects['DOOR | '+key];o.location.y+=.10;o['track_detail']='Complete sash shifted0.10m toward monoambiente; moving frame clears partition by37.5mm.'
box('Monoambiente | carril doble superior',[18,2.64,5.78],[4.24,.045,.075])
for o in S.objects:
 if '| paño fijo' in o.name:o.location.y-=.020
side=bpy.data.objects['DOOR | balconySide'];side.location.x-=.115;side['track_detail']='Sash normal offset totals0.15m from original source; complete125mm frames pass each other with21mm clear separation.'
box('Corrediza lateral | riel de dos vías superior',[13.91,5.81,10.35],[.26,.04,2.59])
box('Corrediza lateral | umbral de dos vías',[13.91,3.21,10.35],[.26,.025,2.59])
# Source cameras stay unchanged; supplement with useful room positions and controlled poses.
def camera(name,p,t,lens,frame=150,shift=None):
 d=bpy.data.cameras.new(name);d.lens=lens;d.sensor_width=36;d.clip_start=.03;d.clip_end=10000
 o=bpy.data.objects.new(name,d);bpy.data.collections['CAMERAS'].objects.link(o);o.location=cv(p)
 if shift is not None:t=[t[0],p[1],t[2]];d.shift_y=shift
 o.rotation_euler=(cv(t)-o.location).to_track_quat('-Z','Y').to_euler();o['presentation_frame']=frame;o['supplemental_camera']=True;return o
hero=bpy.data.objects['CAM | Presentación verticales corregidas'];hero.location=cv([7.5,7.4,26.0]);hero.rotation_euler=(cv([17,7.4,9.5])-hero.location).to_track_quat('-Z','Y').to_euler();hero.data.lens=30;hero.data.shift_y=-.25
camera('REV | Dormitorio completo',[17.25,4.82,7.68],[15.1,4.15,7.45],21,150)
camera('REV | Dormitorio acceso',[14.55,4.88,8.63],[17.03,4.55,7.05],21,150)
camera('REV | Baño completo',[19.84,4.90,8.55],[20.80,4.23,6.72],18,1)
camera('REV | Baño desde acceso',[19.68,4.9,7.43],[21.1,4.25,7.1],18,150)
camera('REV | Vestidor circulación',[18.50,4.9,9.36],[18.53,4.34,6.49],20,150)
camera('REV | Estudio y cubierta',[20.2,5.02,5.28],[17.2,4.95,2.6],21,150)
camera('REV | Cocina comedor',[15.05,4.93,11.46],[20.70,4.36,9.97],24,150)
camera('REV | Quincho y extracción',[15.0,1.92,11.4],[20.90,1.77,8.25],23,150)
camera('REV | Escalera y desembarco',[9.5,3.25,.2],[13.4,2.8,3.5],30,150)
camera('REV | Cubierta escalonada',[10.2,9.0,-4.5],[18.0,6.8,5.6],33,1)
camera('REV | Portón y riel',[7.5,2.5,-3.0],[12,1.0,.3],28,150)
# Camera travel changes preserve source layout; proof of rooms uses their actual door poses.
S['review_iteration']='1 / pass2 spatial presentation'
notes=json.loads(S['corrections']);notes.append('Iteration1 pass2: mono complete sliding sashes shifted0.10m clear of wall; side sliding sash offset totals0.15m so125mm frames no longer intersect; rear fixed glass tracks receive20mm extra separation. Original opening extents retained; all normal track offsets documented.')
S['corrections']=json.dumps(notes,ensure_ascii=False)
S.camera=hero;S.frame_set(1);bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output','Casa_de_Campo.blend'),compress=True)
print('PASS2_SPATIAL_SAVED',flush=True)
# Quick visibility controls only, not a video sequence.
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='OPTIX';p.get_devices()
for d in p.devices:d.use=d.type=='OPTIX'
S.cycles.device='GPU';S.cycles.samples=32;S.cycles.denoiser='OPTIX';S.cycles.denoising_use_gpu=True;S.render.use_persistent_data=True;S.render.resolution_x=1000;S.render.resolution_y=680;S.render.resolution_percentage=100
for n,label in [('REV | Dormitorio completo','dormitorio'),('REV | Baño completo','bano'),('REV | Baño desde acceso','bano_acceso'),('REV | Cocina comedor','cocina'),('REV | Quincho y extracción','quincho')]:
 o=bpy.data.objects[n];S.camera=o;S.frame_set(o['presentation_frame']);S.render.filepath=os.path.join(ROOT,'review','pass2_'+label+'.png');bpy.ops.render.render(write_still=True)
S.frame_set(1);S.camera=hero;S.render.resolution_y=750;S.render.filepath=os.path.join(ROOT,'review','pass2_exterior.png');bpy.ops.render.render(write_still=True)
print('PASS2_VISIBILITY_RENDERED',flush=True)
