import bpy,json
r=[]
for o in bpy.context.scene.objects:
 if o.type=='LIGHT':r.append({'name':o.name,'type':o.data.type,'energy':o.data.energy,'p':[round(x,3) for x in o.location],'color':list(o.data.color)})
print(json.dumps(r,ensure_ascii=False))
print('EMITTERS',json.dumps([o.name for o in bpy.context.scene.objects if o.type=='MESH' and any(m and m.get('source_material_key')=='warmLight' for m in o.data.materials)],ensure_ascii=False))
