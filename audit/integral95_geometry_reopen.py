import bpy,json,hashlib,re,math,os
from mathutils import Vector
root=r'D:\2026\42';scene=bpy.context.scene;scene.frame_set(1);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
def box(o):
 e=o.evaluated_get(dg);m=e.to_mesh();v=[o.matrix_world@a.co for a in m.vertices];e.to_mesh_clear();return {'min':[min(p[k] for p in v) for k in range(3)],'max':[max(p[k] for p in v) for k in range(3)]}
keep=[]
for o in scene.objects:
 if o.type=='MESH' and (re.fullmatch(r'Peldaño exterior \d+',o.name) or any(w in o.name.lower() for w in ['bajada','canaleta','cielorraso','umbral puerta estudio','descanso escalera','piso estudio','piso vivienda','piso baño vivienda','zapata','fundaci','desag','replanteo','membrana','baranda escalera pasamanos'])):
  keep.append({'name':o.name,'box':box(o)})
steps=sorted([x for x in keep if re.fullmatch(r'Peldaño exterior \d+',x['name'])],key=lambda x:x['box']['max'][2])
rise=[b['box']['max'][2]-a['box']['max'][2] for a,b in zip(steps,steps[1:])]
going=[abs((b['box']['min'][1]+b['box']['max'][1]-a['box']['min'][1]-a['box']['max'][1])/2) for a,b in zip(steps,steps[1:])]
result={'file':bpy.data.filepath,'sha256':hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),'objects':keep,'stair':{'count':len(steps),'rises':rise,'goings':going,'first_tread_top':steps[0]['box']['max'][2],'last_tread_top':steps[-1]['box']['max'][2],'slope_deg':math.degrees(math.atan(sum(rise)/sum(going)))}}
json.dump(result,open(os.path.join(root,'audit','integral95_geometry_reopen.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
for name in ['independent_checks_03','door_fixtures_03','acoustic_ceiling_03']:
 path=os.path.join(root,'audit',name+'.py')
 text=open(path,encoding='utf8').read().replace(name+'.json','integral95_'+name+'.json')
 exec(compile(text,path,'exec'),{})
print('INTEGRAL95_GEOMETRY_REOPEN_COMPLETE',flush=True)
