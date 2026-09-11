import bpy,runpy,json,os,hashlib,ast,numpy as np,bmesh
ROOT=r'D:\2026\42';OUT=os.path.join(ROOT,'review99','door_hands');os.makedirs(OUT,exist_ok=True);S=bpy.context.scene;S.frame_set(1)
source=bpy.data.filepath;sourceSHA=hashlib.sha256(open(source,'rb').read()).hexdigest()
driver=ast.parse(open(os.path.join(ROOT,'scripts','integrate99_r7c.py'),encoding='utf-8').read())
exec(compile(ast.Module(body=[n for n in driver.body if isinstance(n,ast.FunctionDef) and n.name=='snapshot'],type_ignores=[]),'<snapshot>','exec'),globals())
patch=runpy.run_path(os.path.join(ROOT,'scripts','correcciones99_bedroom_link.py'));scope=[o.name for o in S.objects if patch['owned_existing'](o)]
before=snapshot(True);result=patch['apply']();after=snapshot(True)
outside=[n for n in before if n not in scope and before[n]!=after.get(n)]
assert not outside,outside
first=snapshot(True);patch['apply']();second=snapshot(True);assert first==second,'Not idempotent'
normals=[]
for o in S.objects:
 if o.type!='MESH' or not (o.name in scope or o.name.startswith('HAND99 |')):continue
 bm=bmesh.new();bm.from_mesh(o.data);volume=bm.calc_volume(signed=True);bm.free()
 normals.append({'name':o.name,'matrixDet':o.matrix_world.determinant(),'signedLocalVolume':volume})
assert not [n for n in normals if n['matrixDet']<=0],normals
dest=os.path.join(ROOT,'output','Casa_de_Campo_99_R7C_hands_preview.blend');bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=dest,compress=True)
report={'source':source,'sourceSHA256':sourceSHA,'output':dest,'outputSHA256':hashlib.sha256(open(dest,'rb').read()).hexdigest(),'patch':result,'preservation':{'outside_scope_changes':outside,'existing_objects_missing':list(set(before)-set(after)),'pass':not outside and set(before)<=set(after)},'idempotence':True,'normal_orientation':normals,'status':'Proposal; pose and circulation tests pending'}
json.dump(report,open(OUT+'/proposal_manifest.json','w'),indent=2,ensure_ascii=True)
print('HANDS_PREVIEW '+json.dumps({'sha256':report['outputSHA256'],'scope':len(scope),'new':len(result['new_objects']),'outside':outside,'negative_volumes':[n['name'] for n in normals if n['signedLocalVolume']<0]}))
