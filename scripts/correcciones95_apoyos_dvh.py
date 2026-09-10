"""P localized rebates and3mm EPDM bearing for fixed DVH windows. Loaded scene; NO SAVE.
Only support/abutment meshes are cut; frame/glass/UV/13rigs preserved.
"""
import bpy,bmesh,json,ast,hashlib
from pathlib import Path
from array import array
from mathutils import Vector
ROOT=Path(__file__).resolve().parent.parent;S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
COL=bpy.data.collections.get('95 | Apoyos DVH')
if COL:raise RuntimeError('DVH bearing patch already applied')
COL=bpy.data.collections.new('95 | Apoyos DVH');S.collection.children.link(COL)
M={m.get('source_material_key'):m for m in bpy.data.materials if m.get('source_material_key')}
for m in bpy.data.materials:
 if m.name.startswith(('MAT95 | ','SL95 | ','FIT95 | ')):M[m.name.split(' | ',1)[1]]=m
for nd in ast.parse((ROOT/'scripts/correcciones95_corredizas_r5.py').read_text(encoding='utf8')).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['mat','cv','src','bounds','overlap','box','boolean','sig']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
def mesh_sig(o):
 a=array('f',[0])*(len(o.data.vertices)*3);o.data.vertices.foreach_get('co',a);b=array('i',[0])*len(o.data.loops);o.data.loops.foreach_get('vertex_index',b);h=hashlib.sha256(a.tobytes()+b.tobytes())
 for uv in o.data.uv_layers:
  a=array('f',[0])*(len(uv.data)*2);uv.data.foreach_get('uv',a);h.update(a.tobytes())
 return h.hexdigest()
F=[('E','Ventana DVH estudio',['Estudio antepecho ventana','Estudio dintel ventana','Estudio lateral frente','Estudio paño entre ventana y puerta','Vierteaguas DVH estudio']),('D','Puerta ventana dormitorio',['Dormitorio antepecho lateral','Dormitorio dintel lateral','Paño lateral medio vivienda','Vivienda lateral junto estudio'])]
host_names={p+' alféizar' for i,p,ns in F}|{n for i,p,ns in F for n in ns};unchanged={o.name:mesh_sig(o) for o in S.objects if o.type=='MESH' and o.name not in host_names};rigs=[o for o in S.objects if o.name.startswith('DOOR |')];before_rig={o.name:sig(o) for o in rigs};report={'source_loaded':bpy.data.filepath,'status':'P local hidden rebates; no change to frame/glass/sourceopening envelopes; capacity and weathering require project','families':[]}
for ident,prefix,ns in F:
 sill=bpy.data.objects[prefix+' alféizar'];sb=bounds(sill);lower=bpy.data.objects[prefix+' marco inferior'];lb=bounds(lower);seatbase=lb['y'][0]-.003;z=[max(sb['z'][0],lb['z'][0]),min(sb['z'][1],lb['z'][1])];x=lb['x']
 # Intersect proposed seat/lips with the ORIGINAL sill before removing itslocalvolume.
 pieces=[]
 for label,xx,yy in [('asiento alféizar EPDM3',x,[seatbase,lb['y'][0]]),('junta labio exterior1',[x[0]-.001,x[0]],[seatbase,sb['y'][1]]),('junta labio interior1',[x[1],x[1]+.001],[seatbase,sb['y'][1]])]:
  ob=box('GL95 | '+ident+' '+label,{'x':xx,'y':yy,'z':z},'rubber95');boolean(ob,sill,'INTERSECT');pieces.append(ob)
 hosts=[bpy.data.objects[n] for n in ns+[sill.name]];ops=[]
 # Each rebate follows one existingmember/pane; no fullopening box is removed.
 parts=[o for o in S.objects if o.type=='MESH' and o.name.startswith(prefix+' ') and (' marco ' in o.name or 'vidrio' in o.name.lower())]
 for ob in parts:
  b=bounds(ob);tol=.003 if 'vidrio' in ob.name.lower() else .001;cbox={k:[vv[0]-tol,vv[1]+tol] for k,vv in b.items()}
  if ob==lower:cbox['y'][0]=seatbase
  cutter=box('TEMP reserva '+ob.name,cbox,'blackMetal');done=[]
  for host in hosts:
   if overlap(bounds(host),cbox):boolean(host,cutter);done.append(host.name)
  bpy.data.objects.remove(cutter,do_unlink=True);ops.append({'member':ob.name,'reservation_source_m':cbox,'hosts':done})
 # ExistingGL95 glazingseals remain; the two newlips close the sill clearance.
 bpy.context.view_layer.update();after=bounds(sill);err=max(abs(sb[k][j]-after[k][j]) for k in 'xyz' for j in [0,1]);assert err<1e-5,(sill.name,err)
 report['families'].append({'id':ident,'prefix':prefix,'sill':sill.name,'frame_bottom_m':lb['y'][0],'original_sill_top_m':sb['y'][1],'old_overlap_mm':(sb['y'][1]-lb['y'][0])*1000,'rebate_bottom_m':seatbase,'seat_thickness_mm':3,'clearance_lip_mm':1,'sill_outer_envelope_error_m':err,'seat_common_footprint_source_m':{'x':x,'z':z},'new_pieces':[o.name for o in pieces],'reservations':ops})
assert all(mesh_sig(bpy.data.objects[n])==v for n,v in unchanged.items()),'Non-host geometry or UV changed'
assert before_rig=={o.name:sig(o) for o in rigs},'Rig changed';assert len(rigs)==13
report.update(non_host_meshes_and_uv_preserved=True,rig_definitions_preserved=True,rig_count=13)
S['dv_h_fixed_bearings_r6k']=json.dumps(report,ensure_ascii=False)
(ROOT/'review95/apoyos_dvh_r6k_details.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print('DVH_BEARINGS_PATCHED_NO_SAVE',json.dumps(report,ensure_ascii=False),flush=True)
