"""Replace24 legacy solid-metal glazing strips; P mounting detail, retainglass/rigs/envelopes."""
import bpy,json,sys,argparse,hashlib,ast,bmesh
from array import array
from pathlib import Path
from mathutils import Vector
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--report',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();root=Path(__file__).resolve().parent.parent;source=Path(bpy.data.filepath)
COL=bpy.data.collections.new('95 | Juntas DVH propuestas');S.collection.children.link(COL)
M={m.get('source_material_key'):m for m in bpy.data.materials if m.get('source_material_key')}
for m in bpy.data.materials:
 if m.name.startswith(('MAT95 | ','SL95 | ')):M[m.name.split(' | ',1)[1]]=m
for node in ast.parse((root/'scripts/correcciones95_corredizas_r5.py').read_text(encoding='utf8')).body:
 if isinstance(node,ast.FunctionDef):exec(compile(ast.Module(body=[node],type_ignores=[]),'<helper>','exec'))
def gb(n,t,u,h,f,key='rubber95',parent=None):return box('GL95 | '+f['id']+' '+n,globox(t,u,h,f['axis']),key,parent)
def geometry_sig(o):
 a=array('f',[0])*(len(o.data.vertices)*3);o.data.vertices.foreach_get('co',a);b=array('i',[0])*len(o.data.loops);o.data.loops.foreach_get('vertex_index',b);return hashlib.sha256(a.tobytes()+b.tobytes()).hexdigest()
F=[('ML','Puerta doble mono izquierda','x'),('MR','Puerta doble mono derecha','x'),('D','Puerta ventana dormitorio','z'),('L','Corrediza lateral A','z'),('LF','Corrediza lateral B','z'),('E','Ventana DVH estudio','z')]
legacy=[o for o in S.objects if o.type=='MESH' and any(o.name.startswith(p+' Burlete ') for i,p,a in F)]
assert len(legacy)==24,len(legacy)
modified=[o for o in S.objects if o.type=='MESH' and any(o.name.startswith(p+' marco ') for i,p,a in F if i not in ('L','LF'))]
allowed={o.name for o in legacy+modified};unchanged={o.name:geometry_sig(o) for o in S.objects if o.type=='MESH' and o.name not in allowed}
rigs=[o for o in S.objects if o.name.startswith('DOOR |')];rig_before={r.name:sig(r) for r in rigs};outer={o.name:bounds(o) for o in modified};glass_original={o.name:geometry_sig(o) for o in S.objects if o.type=='MESH' and any(o.name.startswith(p) for i,p,a in F) and 'vidrio' in o.name.lower()}
removed=[o.name for o in legacy]
for o in legacy:bpy.data.objects.remove(o,do_unlink=True)
reports=[];operations=[]
for ident,prefix,axis in F:
 f={'id':ident,'axis':axis};cross='z' if axis=='x' else 'x';glasses=[o for o in S.objects if o.type=='MESH' and o.name.startswith(prefix+' ') and 'vidrio' in o.name.lower()];glasses.sort(key=lambda o:bounds(o)[cross][0]);assert len(glasses)==2
 bs=[bounds(o) for o in glasses];parent=glasses[0].parent;frames=[o.name for o in modified if o.name.startswith(prefix+' ')];report={'family':ident,'prefix':prefix,'panes':[{'name':g.name,'bounds_source_m':b} for g,b in zip(glasses,bs)],'rig':parent.name if parent else None,'air_gap_mm':(bs[1][cross][0]-bs[0][cross][1])*1000}
 if ident in ('L','LF'):
  report['action']='Removed legacy4; preserved existing SL95 pane gaskets, glass pockets, setting blocks and DVH perimeter spacer.';reports.append(report);continue
 print('GL95 family',ident,flush=True)
 # One common39mm glazing cavity removes the metal web previously bridgingthe17mm airspace.
 t=[min(b[axis][0] for b in bs)-.002,max(b[axis][1] for b in bs)+.002];u=[bs[0][cross][0]-.002,bs[1][cross][1]+.002];h=[min(b['y'][0] for b in bs)-.006,max(b['y'][1] for b in bs)+.002]
 reserve(frames,globox(t,u,h,axis),ident+' alojamiento DVH39mm con apoyo6mm')
 # Separateperpane thin resilient seals, neither solidmetal nor volumeinside glass.
 for gi,(g,b) in enumerate(zip(glasses,bs),1):
  gt=b[axis];gu=b[cross];gh=b['y']
  for face,uu in [('exterior',[gu[0]-.002,gu[0]]),('interior',[gu[1],gu[1]+.002])]:
   for edge,hh in [('base',[gh[0],gh[0]+.012]),('cabeza',[gh[1]-.012,gh[1]])]:gb(f'junta vidrio{gi} {face} {edge}',gt,uu,hh,f,parent=parent)
   for edge,tt in [('inicio',[gt[0],gt[0]+.012]),('fin',[gt[1]-.012,gt[1]])]:gb(f'junta vidrio{gi} {face} {edge}',tt,uu,[gh[0]+.012,gh[1]-.012],f,parent=parent)
  for j,frac in enumerate([.25,.75],1):
   ct=gt[0]+frac*(gt[1]-gt[0]);gb(f'taco vidrio{gi}-{j}100x6',[ct-.05,ct+.05],gu,[gh[0]-.006,gh[0]],f,parent=parent)
   # Inner pane inherited higherbottom: fitted bearing6mm plus rigidshim down to common seat.
   if gh[0]-.006>h[0]+1e-6:gb(f'calzo apoyo vidrio{gi}-{j}',[ct-.05,ct+.05],gu,[h[0],gh[0]-.006],f,'polymer',parent)
 # Perimeterjoint betweeninner faces of bothpanes; trim existing2mm face strips,
 # so central13mm secondaryseal and two2mm lips form17mm withoutdouble volume.
 tt=[max(b[axis][0] for b in bs),min(b[axis][1] for b in bs)];hh=[max(b['y'][0] for b in bs),min(b['y'][1] for b in bs)];gap=[bs[0][cross][1]+.002,bs[1][cross][0]-.002]
 for edge,hb in [('base',[hh[0],hh[0]+.006]),('cabeza',[hh[1]-.006,hh[1]])]:gb('sellador cámara '+edge,tt,gap,hb,f,parent=parent)
 for edge,tb in [('inicio',[tt[0],tt[0]+.006]),('fin',[tt[1]-.006,tt[1]])]:gb('sellador cámara '+edge,tb,gap,[hh[0]+.006,hh[1]-.006],f,parent=parent)
 report.update(action='Glazing pocket in originalmembers;2mm face gaskets eachpane;6mmdeep peripheral cavityseal;2x100mm settingblocks per glass.',pocket_source_m=globox(t,u,h,axis),face_gasket_thickness_mm=2,face_gasket_bite_mm=12,setting_block_height_mm=6,spacer_peripheral_depth_mm=6,modified_frames=frames);reports.append(report)
bpy.context.view_layer.update();checks=[]
for n,b in outer.items():
 now=bounds(bpy.data.objects[n]);err=max(abs(now[k][i]-b[k][i]) for k in 'xyz' for i in [0,1]);checks.append({'name':n,'outer_envelope_error_m':err});assert err<2e-5,(n,err)
assert all(geometry_sig(bpy.data.objects[n])==v for n,v in unchanged.items()),'Outside scope mesh changed'
assert all(geometry_sig(bpy.data.objects[n])==v for n,v in glass_original.items()),'Glass changed'
assert {r.name:sig(r) for r in rigs}==rig_before,'Rig changed'
# Run showerheightpatchwithout saving a secondintermediate file.
_argv=sys.argv;sys.argv=['shower integration'];exec(compile((root/'scripts/correcciones95_rociador_r6.py').read_text(encoding='utf-8-sig'),'<shower height>','exec'));sys.argv=_argv;shower_report=dict(report)
S['glazing_r6g']='P: replacement of24solidmetal strips by measured EPDM glazing interfaces; no product certification or weather test.'
S.frame_set(1);bpy.context.view_layer.update();out=Path(args.out).resolve();bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
report={'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'model':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'removed_legacy':removed,'shower_clearance':shower_report,'families':reports,'reservations':operations,'outer_bounds_checks':checks,'original_glass_preserved':True,'all_meshes_outside_glazing_and_named_shower_patch_preserved':True,'rig_definitions_preserved':True,'rig_count':len(rigs),'limitations':['P geometric assembly; proprietary profile design, drainage and manufacturer system selection remain unverified.','No acoustic, thermal, mechanical or watertightness certification.']}
Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print('GL95_COMPLETE',report['sha256'],flush=True)
