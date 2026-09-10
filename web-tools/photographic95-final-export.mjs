import fs from 'node:fs';const f='scripts/web95_optics_export.py';let s=fs.readFileSync(f,'utf8');
s=s.replace("out = os.path.join(ROOT,'docs','preview95','assets','optics.json')",`world=scene.world
nodes=world.node_tree.nodes if world and world.use_nodes else []
bg=next((n for n in nodes if n.type=='BACKGROUND'),None)
env=next((n for n in nodes if n.type=='TEX_ENVIRONMENT'),None)
mapping=next((n for n in nodes if n.type=='MAPPING'),None)
rotation_z=float(mapping.inputs['Rotation'].default_value[2]) if mapping else 0
optical_world=dict(type='HDR' if env else 'procedural',strength=float(bg.inputs['Strength'].default_value) if bg else 1,rotationZ=rotation_z,threeEnvironmentRotationY=-rotation_z,exposureEV=float(scene.view_settings.exposure),look=scene.view_settings.look)
out = os.path.join(ROOT,'docs','preview95','assets','optics.json')`);
s=s.replace('lights=lights, materials=materials, units=', 'lights=lights, materials=materials, environment=optical_world, units=');
s=s.replace('    assignments={} ', '    assignments={} ');
s=s.replace('    # Convert evaluated FONT/CURVE',`    # Keep complete five-vertex/four-triangle folded leaves. Preserve colour and normals.
    import numpy as np
    leaf_cache={};leaf_lod=[]
    for obj in list(scene.objects):
        if obj.type!='MESH' or obj.hide_render or not obj.name.startswith('MAT95 | árbol ') or 'hojas' not in obj.name: continue
        tree=int(obj.name.split('árbol ')[1].split()[0]);old=obj.data
        assert len(old.vertices)%5==0 and len(old.polygons)==len(old.vertices)//5*4, 'Unknown leaf topology: '+obj.name
        count=len(old.vertices)//5;target=min(count,18000 if tree<6 else 4000)
        key=(old.name,target)
        if key not in leaf_cache:
            if target==count: leaf_cache[key]=old
            else:
                verts=np.empty(len(old.vertices)*3,dtype=np.float32);old.vertices.foreach_get('co',verts);verts=verts.reshape(-1,3)
                faces=np.empty(len(old.loops),dtype=np.int32);old.loops.foreach_get('vertex_index',faces);faces=faces.reshape(-1,3)
                assert np.all(faces//5==(np.arange(count).repeat(4))[:,None]), 'Leaf components mixed: '+obj.name
                leaves=np.linspace(0,count-1,target,dtype=np.int32);vi=(leaves[:,None]*5+np.arange(5)).reshape(-1);fi=(leaves[:,None]*4+np.arange(4)).reshape(-1)
                remap=np.full(len(old.vertices),-1,dtype=np.int32);remap[vi]=np.arange(len(vi))
                new=bpy.data.meshes.new(old.name+' WEB '+str(target)+' whole leaves');new.from_pydata(verts[vi].tolist(),[],remap[faces[fi]].tolist())
                for mat in old.materials:new.materials.append(mat)
                for poly in new.polygons:poly.use_smooth=True
                for attr in old.color_attributes:
                    if attr.domain!='POINT':continue
                    color=np.empty(len(old.vertices)*4,dtype=np.float32);attr.data.foreach_get('color',color)
                    ca=new.color_attributes.new(name=attr.name,type='FLOAT_COLOR',domain='POINT');ca.data.foreach_set('color',color.reshape(-1,4)[vi].reshape(-1))
                new.update();leaf_cache[key]=new
        obj.data=leaf_cache[key];leaf_lod.append(dict(name=obj.name,sourceLeaves=count,webLeaves=target,completeUnits=True,vertexColour='botanical_tint'))
    with open(os.path.join(ROOT,'docs','preview95','assets','leaf-lod.json'),'w',encoding='utf8') as f:json.dump(leaf_lod,f,ensure_ascii=False,indent=2)
    # Convert evaluated FONT/CURVE`);
s=s.replace('    # New authored leaf units',`    code=code.replace(" cache[old.name]=m;return m", " if 'leaf95' in old.name:\\n  attr=m.node_tree.nodes.new('ShaderNodeVertexColor');attr.layer_name='botanical_tint';m.node_tree.links.new(attr.outputs['Color'],bs.inputs['Base Color'])\\n cache[old.name]=m;return m")
    # New authored leaf units`);
fs.writeFileSync(f,s);
const p='docs/preview95/photographic.js';s=fs.readFileSync(p,'utf8');s=s.replace('scene.environmentRotation.y=scene.backgroundRotation.y=Math.PI/4;',`scene.environmentRotation.y=scene.backgroundRotation.y=Math.PI/4;
 if(optics.environment?.type==='HDR'){
  scene.environmentIntensity=scene.backgroundIntensity=optics.environment.strength;
  scene.environmentRotation.y=scene.backgroundRotation.y=optics.environment.threeEnvironmentRotationY;
  renderer.toneMappingExposure=Math.pow(2,optics.environment.exposureEV);
 }`);fs.writeFileSync(p,s);
