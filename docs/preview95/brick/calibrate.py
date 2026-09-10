"""Apply calibrated Red Bricks 04 to the loaded scene. Never saves a .blend.
Works with source brick/brickDark or already photographic masonry; wood and all geometry remain unchanged.
"""
import bpy,os,sys,json,hashlib,numpy as np
BASE=os.path.dirname(__file__);OUT=os.path.join(BASE,'calibrated');os.makedirs(OUT,exist_ok=True);ASSET=os.path.abspath(os.path.join(BASE,'..','assets','red-bricks-04'));S=bpy.context.scene
has_original=any(o.type=='MESH' and not o.hide_render and any(s.material and s.material.get('source_material_key') in ['brick','brickDark'] for s in o.material_slots) for o in S.objects)
if has_original:
 path=os.path.join(BASE,'apply.py');code=open(path,encoding='utf8').read();code=code.replace('OUT=os.path.dirname(__file__);ASSET=',"OUT=os.path.join(os.path.dirname(__file__),'calibrated');ASSET=")
 saved_argv=sys.argv[:];sys.argv=[sys.argv[0]]
 try:exec(compile(code,path,'exec'),{'__file__':path,'__name__':'__main__'})
 finally:sys.argv=saved_argv
materials={s.material for o in S.objects if o.type=='MESH' and not o.hide_render for s in o.material_slots if s.material and s.material.get('photographic_masonry')};assert materials,'No photographic masonry found'
image=bpy.data.images.load(os.path.join(ASSET,'red_bricks_04_calibrated_diffuse_2k.png'),check_existing=True);image.colorspace_settings.name='sRGB';report=[]
for mat in materials:
 bs=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');assert bs.inputs['Emission Strength'].default_value==0,'Masonry must not emit light'
 tex=[n for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.image and ('_diff_' in n.image.name or 'calibrated_diffuse' in n.image.name)];assert len(tex)==1,'Expected one albedo image: '+mat.name
 tex[0].image=image;mat['albedo_calibration']='linear RGB: 0.82*Cphoto + 0.18*[0.36,0.17,0.09]';mat['albedo_calibration_asset']='red_bricks_04_calibrated_diffuse_2k.png';mat['review_status']='CALIBRATED_PREVIEW';report.append(mat.name)
result=dict(source=bpy.data.filepath,sourceSHA256=hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),materials=report,count=len(report),geometryChanged=False,secondaryUVChanged=False,emissionUsed=False,woodChanged=False,savedBlend=False,provenance=os.path.join(ASSET,'calibration-provenance.json'));json.dump(result,open(OUT+'/application-report-calibrated.json','w',encoding='utf8'),ensure_ascii=False,indent=2);print('BRICK_CALIBRATED_IN_MEMORY',len(report),'NO_BLEND_SAVED',flush=True)
