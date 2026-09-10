"""Complete weather/glazing seals and recessed lateral pull on R5B. Geometry P."""
import bpy,json,sys,argparse,hashlib,ast
from pathlib import Path
from mathutils import Vector
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update();root=Path(__file__).resolve().parent.parent
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--report',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);base=Path(bpy.data.filepath)
COL=bpy.data.collections['95 | Corredizas propuestas'];M={m.get('source_material_key'):m for m in bpy.data.materials if m.get('source_material_key')}
for m in bpy.data.materials:
 if m.name.startswith(('MAT95 | ','SL95 | ')):M[m.name.split(' | ',1)[1]]=m
import bmesh
for node in ast.parse((root/'scripts/correcciones95_corredizas_r5.py').read_text(encoding='utf8')).body:
 if isinstance(node,ast.FunctionDef):exec(compile(ast.Module(body=[node],type_ignores=[]),'<slider helper>','exec'))
operations=[];data=json.loads((root/'review95/corredizas_r5_details.json').read_text(encoding='utf8'))
for report in data['families']:
 ident=report['family'];r=bpy.data.objects[report['rig']];axis='z' if ident=='L' else 'x';cross='x' if axis=='z' else 'z';f={'id':ident,'axis':axis};lane=report['source_lane'];t=lane[axis];u=lane[cross]
 lower=bpy.data.objects['Corrediza lateral A marco inferior' if ident=='L' else 'Hoja posterior '+ident+' | perfil móvil.001'];low=bounds(lower)
 maxcross=low[cross][1] if ident=='L' else lane[cross][1]-.003
 # Low and high brushes touch the sash, with no rigid part entering its sweep.
 for label,uu in [('frente',[u[0],low[cross][0]]),('dorso',[maxcross,u[1]])]:
  for where,hh in [('inferior',[3.226,3.236]),('superior',[5.748,5.758])]:gb('felpa pista '+label+' '+where,t,uu,hh,f,'rubber95')
 gb('burlete jamba cierre',[t[0]-.003,t[0]+.003],[u[0]+.003,u[1]-.003],[3.27,5.70],f,'rubber95')
 fixedprefix='Corrediza lateral B' if ident=='L' else 'Corrediza posterior '+ident
 fixed=[o for o in S.objects if o.type=='MESH' and o.name.startswith(fixedprefix) and 'vidrio' in o.name.lower() and o not in r.children_recursive]
 moving=[o for o in r.children_recursive if o.type=='MESH' and 'vidrio' in o.name.lower() and not o.name.startswith('SL95')]
 for gi,g in enumerate(fixed,1):
  b=bounds(g);gt=b[axis];gu=b[cross];gh=b['y']
  for label,uu in [('a',[gu[0]-.002,gu[0]]),('b',[gu[1],gu[1]+.002])]:
   for where,hh in [('base',[gh[0],gh[0]+.012]),('cabeza',[gh[1]-.012,gh[1]])]:gb(f'fijo junta vidrio{gi} '+label+where,gt,uu,hh,f,'rubber95')
   for where,tt in [('i',[gt[0],gt[0]+.010]),('f',[gt[1]-.010,gt[1]])]:gb(f'fijo junta vidrio{gi} '+label+where,tt,uu,[gh[0]+.012,gh[1]-.012],f,'rubber95')
 if ident!='L':
  bs=[bounds(g) for g in fixed];ft=min(b[axis][0] for b in bs);fu=min(b[cross][0] for b in bs)
  gb('felpa encuentro entre paños',[ft-.002,ft+.010],[u[1]-.003,fu-.008],[3.24,5.74],f,'rubber95')
 # A continuous four-sided spacer/seal ties both panes;17mm is measured clear air spacing.
 for label,panes,parent in [('móvil',moving,r),('fijo',fixed,None)]:
  if len(panes)!=2:continue
  bs=sorted([bounds(g) for g in panes],key=lambda b:b[cross][0]);gap=[bs[0][cross][1],bs[1][cross][0]];gt=[max(b[axis][0] for b in bs),min(b[axis][1] for b in bs)];gh=[max(b['y'][0] for b in bs),min(b['y'][1] for b in bs)]
  for where,hh in [('base',[gh[0],gh[0]+.006]),('cabeza',[gh[1]-.006,gh[1]])]:gb('DVH sellador espaciador '+label+' '+where,gt,gap,hh,f,'rubber95',parent)
  for where,tt in [('i',[gt[0],gt[0]+.006]),('f',[gt[1]-.006,gt[1]])]:gb('DVH sellador espaciador '+label+' '+where,tt,gap,[gh[0]+.006,gh[1]-.006],f,'rubber95',parent)
 if ident=='L':
  face=low[cross][1];tt=9.175;post='Corrediza lateral A marco frente';recess=globox([tt-.016,tt+.016],[face-.025,face+.001],[4.34,4.56],axis);reserve([post],recess,'L tirador embutido interior')
  gb('tirador embutido respaldo',[tt-.016,tt+.016],[face-.025,face-.023],[4.34,4.56],f,'blackMetal',r)
  for label,tb in [('i',[tt-.016,tt-.014]),('f',[tt+.014,tt+.016])]:gb('tirador embutido borde '+label,tb,[face-.023,face],[4.34,4.56],f,'blackMetal',r)
  for label,hh in [('i',[4.34,4.342]),('s',[4.558,4.56])]:gb('tirador embutido tapa '+label,[tt-.014,tt+.014],[face-.023,face],hh,f,'blackMetal',r)
  cylinder('SL95 | L tirador embutido agarre',xyz(tt,face-.006,4.38,axis),xyz(tt,face-.006,4.52,axis),.003,'stainless',r)
  for hh in [4.38,4.52]:cylinder('SL95 | L tirador embutido unión',xyz(tt,face-.023,hh,axis),xyz(tt,face-.006,hh,axis),.003,'stainless',r)
# Rounded hollow elbow: a sphere closes the outer corner, with a matching inner sphere.
# Straight bore extensions alone would perforate the back of a square tube intersection.
def sphere(n,point,r):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=r,location=cv(point));o=bpy.context.object;o.name=n
 for col in list(o.users_collection):col.objects.unlink(o)
 COL.objects.link(o);o.data.materials.append(mat('stainless'));return o
for report in data['families']:
 ident=report['family'];axis='z' if ident=='L' else 'x';top=report['rolling_height_m']-.002+.001
 for j,d in enumerate(report['drains'],1):
  for o in list(COL.objects):
   if o.name.startswith('SL95 | '+ident+f' drenaje{j} '):bpy.data.objects.remove(o,do_unlink=True)
  b=d['start'];end=d['outlet'];a=[b[0],top,b[2]]
  cutter=sphere('TMP elbow reservation',b,.008);done=[]
  for o in list(S.objects):
   if o.type!='MESH' or o==cutter or o.parent or o.name.startswith(('BOT95','TMP')):continue
   if overlap(bounds(o),bounds(cutter)):boolean(o,cutter);done.append(o.name)
  bpy.data.objects.remove(cutter,do_unlink=True);operations.append({'reservation':ident+f' elbow{j}','center':b,'diameter_mm':16,'objects':done})
  tube=cylinder('SL95 | '+ident+f' drenaje{j} Ø14 interior10',a,b,.007);arm=cylinder('TMP arm',b,end,.007);boolean(tube,arm,'UNION');bpy.data.objects.remove(arm,do_unlink=True)
  outer=sphere('TMP outer elbow',b,.007);boolean(tube,outer,'UNION');bpy.data.objects.remove(outer,do_unlink=True)
  # Only free mouths extend the bore; inside ends terminate at elbow center.
  av,bv,ev=cv(a),cv(b),cv(end);c=cylinder('TMP bore',src(av+(av-bv).normalized()*.002),b,.005);boolean(tube,c);bpy.data.objects.remove(c,do_unlink=True)
  c=cylinder('TMP bore',b,src(ev+(ev-bv).normalized()*.002),.005);boolean(tube,c);bpy.data.objects.remove(c,do_unlink=True)
  inner=sphere('TMP inner elbow',b,.005);boolean(tube,inner);bpy.data.objects.remove(inner,do_unlink=True)
  d['elbow']='continuous spherical outer14/inner10; open mouths; no crossed blind caps'
S['sliding_windows_r5_seals']='P: EPDM perimeter glazing seals, measured17mm DVH spacer, guide brushes, meeting brush and recessed interior lateral pull.'
S.frame_set(1);bpy.context.view_layer.update();out=Path(args.out).resolve();bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
data['model']=str(out);data['sha256']=hashlib.sha256(out.read_bytes()).hexdigest();data['reservations']+=operations;data['seal_completion']='2mm glass perimeter seals; guide and meeting brushes;17mm measured DVH spacer;25mm deep recessed lateral pull';data['model_before_seal_completion']=str(base)
Path(args.report).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');print('SL95_FINAL_SEALS',data['sha256'],flush=True)
