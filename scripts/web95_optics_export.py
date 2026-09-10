"""Read-only export of authored light optics. Never saves the source blend."""
import bpy, json, os, hashlib
from mathutils import Matrix, Vector
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = Matrix(((1,0,0,0),(0,0,1,0),(0,-1,0,0),(0,0,0,1)))
scene = bpy.context.scene
source_hash_at_start=hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest()
if os.environ.get('PHOTO95_EXPECTED_SHA'):assert source_hash_at_start==os.environ['PHOTO95_EXPECTED_SHA'],'Source differs from coordinated freeze'
lights = []
for obj in scene.objects:
    if obj.type != 'LIGHT' or obj.hide_render: continue
    data = obj.data
    pos = C @ obj.matrix_world.translation
    quat = (C @ obj.matrix_world).to_quaternion()
    direction = C.to_3x3() @ (obj.matrix_world.to_quaternion() @ Vector((0,0,-1)))
    lights.append(dict(name=obj.name, type=data.type, energy=data.energy, color=list(data.color), position=list(pos), quaternion=[quat.x,quat.y,quat.z,quat.w], direction=list(direction), shape=getattr(data,'shape',None), size=getattr(data,'size',None), sizeY=getattr(data,'size_y',None), angle=getattr(data,'angle',None), radius=getattr(data,'shadow_soft_size',None)))
materials=[]
for mat in bpy.data.materials:
    if not mat.use_nodes: continue
    bs=next((n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
    if not bs: continue
    color=list(bs.inputs['Base Color'].default_value)
    ramp=next((link.from_node for link in bs.inputs['Base Color'].links if link.from_node.type=='VALTORGB'),None)
    finish=None
    if mat.get('finish_scale_m') is not None and ramp:
        colors=[list(e.color) for e in ramp.color_ramp.elements]
        color=[sum(c[k] for c in colors)/len(colors) for k in range(4)]
        bump=next((n for n in mat.node_tree.nodes if n.type=='BUMP'),None)
        finish=dict(scaleMetres=float(mat['finish_scale_m']),albedoVariationPercent=float(mat.get('albedo_variation_percent',0)),albedoRange=colors,bumpDistance=float(bump.inputs['Distance'].default_value) if bump else 0,bumpStrength=float(bump.inputs['Strength'].default_value) if bump else 0)
    materials.append(dict(name=mat.name,key=mat.get('source_material_key',''), color=color,proceduralFinish=finish,roughness=bs.inputs['Roughness'].default_value, metalness=bs.inputs['Metallic'].default_value,ior=bs.inputs['IOR'].default_value, transmission=bs.inputs['Transmission Weight'].default_value, textures=[n.image.filepath for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]))
world=scene.world
nodes=world.node_tree.nodes if world and world.use_nodes else []
bg=next((n for n in nodes if n.type=='BACKGROUND'),None)
env=next((n for n in nodes if n.type=='TEX_ENVIRONMENT'),None)
mapping=next((n for n in nodes if n.type=='MAPPING'),None)
rotation_z=float(mapping.inputs['Rotation'].default_value[2]) if mapping else 0
optical_world=dict(type='HDR' if env else 'procedural',strength=float(bg.inputs['Strength'].default_value) if bg else 1,rotationZ=rotation_z,threeEnvironmentRotationY=-rotation_z,exposureEV=float(scene.view_settings.exposure),look=scene.view_settings.look)
out = os.path.join(ROOT,'docs','preview95','assets','optics.json')
with open(out,'w',encoding='utf8') as f:
    json.dump(dict(source=bpy.data.filepath, scene=scene.name, axes='Three Y up, from Blender (X,Z,-Y)',lights=lights, materials=materials, environment=optical_world, units='Blender radiant watts; preview photometric scale is calibrated, not a lux certification'),f,ensure_ascii=False,indent=2)
print('OPTICS_EXPORT',len(lights),out,flush=True)

# Optional candidate export, isolated from production. Invoke after the parent saves its new blend.
import sys
if '--candidate' in sys.argv:
    import runpy
    measurement=runpy.run_path(os.path.join(ROOT,'docs','preview95','source-envelopes.py'))
    measurement['measure_source'](os.path.join(ROOT,'docs','preview95','assets','source-envelopes.json'))
    assignments={}
    for obj in scene.objects:
        if obj.type!='MESH': continue
        for slot in obj.material_slots:
            mat=slot.material
            if mat and mat.name.startswith(('Roble aceitado','Nogal mate')):
                tail=mat.name.split('|')[1].strip()
                assignments[obj.name]=dict(wood='oak' if mat.name.startswith('Roble') else 'walnut',axis=int(tail[0]),floor='parquet' in tail)
    with open(os.path.join(ROOT,'docs','preview95','assets','textures','wood-surfaces.json'),'w',encoding='utf8') as f:
        json.dump(assignments,f,ensure_ascii=False)
    # Photo-textured botanical asset: preserve complete connected units, both UV layers,
    # material assignments and shared meshes. No source asset or blend is saved.
    botanical=[o for o in scene.objects if o.type=='MESH' and not o.hide_render and o.name.startswith('BOT95 | árbol ')]
    botanical_lod=[]
    if botanical:
        import numpy as np
        import bmesh
        original=botanical[0].data
        assert all(o.data==original for o in botanical),'Expected one shared source tree mesh'
        parent=np.arange(len(original.vertices),dtype=np.int32)
        def find_root(x):
            while parent[x]!=x:parent[x]=parent[parent[x]];x=int(parent[x])
            return x
        edges=np.empty(len(original.edges)*2,dtype=np.int32);original.edges.foreach_get('vertices',edges)
        for a,b in edges.reshape(-1,2):parent[find_root(a)]=find_root(b)
        roots=np.array([find_root(i) for i in range(len(parent))],dtype=np.int32)
        material_index=np.zeros(len(parent),dtype=np.int32)
        for poly in original.polygons:
            for v in poly.vertices:material_index[v]=poly.material_index
        components={}
        for i,mat in enumerate(original.materials):components[i]=np.unique(roots[material_index==i])
        botanical_cache={}
        for foreground in [True,False]:
            kept=[];details=[]
            for i,mat in enumerate(original.materials):
                ids=components[i]
                target=min(len(ids),20000 if foreground else 4000) if 'leaves' in mat.name else (max(1,int(len(ids)*(.5 if foreground else .15))) if 'branches' in mat.name else len(ids))
                keep=ids[np.linspace(0,len(ids)-1,target,dtype=np.int32)];kept.extend(keep.tolist())
                details.append(dict(material=mat.name,sourceComponents=len(ids),webComponents=target))
            keep_vertex=np.isin(roots,np.array(kept,dtype=np.int32))
            bm=bmesh.new();bm.from_mesh(original);bm.verts.ensure_lookup_table()
            bmesh.ops.delete(bm,geom=[v for v in bm.verts if not keep_vertex[v.index]],context='VERTS')
            mesh=bpy.data.meshes.new('TreeSmall02 WEB '+('foreground' if foreground else 'background'));bm.to_mesh(mesh);bm.free()
            for mat in original.materials:mesh.materials.append(mat)
            # glTF and the path tracer share UV0. Remap branch faces from their original
            # UV_map_01 into UVMap; retain the authored (3,.6) texture transform.
            uv0=mesh.uv_layers.get('UVMap');uv1=mesh.uv_layers.get('UV_map_01')
            assert uv0 and uv1,'Missing photographic tree UV layers'
            u0=np.empty(len(mesh.loops)*2,dtype=np.float32);u1=np.empty_like(u0)
            uv0.data.foreach_get('uv',u0);uv1.data.foreach_get('uv',u1)
            mask=np.zeros(len(mesh.loops),dtype=bool)
            for poly in mesh.polygons:
                if 'branches' in original.materials[poly.material_index].name:mask[poly.loop_start:poly.loop_start+poly.loop_total]=True
            u0=u0.reshape(-1,2);u0[mask]=u1.reshape(-1,2)[mask];uv0.data.foreach_set('uv',u0.reshape(-1))
            mesh.update();botanical_cache[foreground]=(mesh,details)
        for obj in botanical:
            tree=int(obj.name.split('árbol ')[1]);foreground=tree<6
            obj.data,details=botanical_cache[foreground]
            botanical_lod.append(dict(name=obj.name,lod='foreground' if foreground else 'background',components=details,vertices=len(obj.data.vertices),sourceVertices=len(original.vertices),completeUnits=True,uvLayers=[u.name for u in obj.data.uv_layers]))
        def botanical_material(old):
            if old.name.startswith('WEB | '):return old
            name='WEB | '+old.name
            if bpy.data.materials.get(name):return bpy.data.materials[name]
            mat=bpy.data.materials.new(name);mat.use_nodes=True;nodes=mat.node_tree.nodes;links=mat.node_tree.links
            bs=next(n for n in nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(1,1,1,1);bs.inputs['Roughness'].default_value=1
            uv=nodes.new('ShaderNodeUVMap');uv.uv_map='UVMap'
            vector=uv.outputs['UV']
            if 'branches' in old.name:
                mapping=nodes.new('ShaderNodeMapping');mapping.inputs['Scale'].default_value=(3,.6,1);links.new(vector,mapping.inputs['Vector']);vector=mapping.outputs['Vector']
            images=[n.image for n in old.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]
            for kind,target in [('diff','Base Color'),('rough','Roughness'),('nor','Normal'),('alpha','Alpha')]:
                image=next((im for im in images if '_'+kind in im.name),None)
                if not image:continue
                tex=nodes.new('ShaderNodeTexImage');tex.image=image;links.new(vector,tex.inputs['Vector'])
                if kind=='nor':
                    normal=nodes.new('ShaderNodeNormalMap');normal.uv_map=uv.uv_map;links.new(tex.outputs['Color'],normal.inputs['Color']);links.new(normal.outputs['Normal'],bs.inputs[target])
                else:links.new(tex.outputs['Color'],bs.inputs[target])
            mat.use_backface_culling=False;mat['asset_source']='https://polyhaven.com/a/tree_small_02';mat['asset_license']='CC0'
            return mat
        for mesh,details in botanical_cache.values():
            for i,mat in enumerate(list(mesh.materials)):mesh.materials[i]=botanical_material(mat)
        with open(os.path.join(ROOT,'docs','preview95','assets','botanical-lod.json'),'w',encoding='utf8') as f:json.dump(botanical_lod,f,ensure_ascii=False,indent=2)
        print('BOTANICAL_LOD_COMPLETE',len(botanical),[(k,len(v[0].vertices),len(v[0].polygons)) for k,v in botanical_cache.items()],flush=True)

    # Keep complete five-vertex/four-triangle folded leaves. Preserve colour and normals.
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
    # Convert evaluated FONT/CURVE objects only in this unsaved export process.
    depsgraph=bpy.context.evaluated_depsgraph_get()
    for obj in list(scene.objects):
        if obj.type not in ('FONT','CURVE') or obj.hide_render: continue
        mesh=bpy.data.meshes.new_from_object(obj.evaluated_get(depsgraph),preserve_all_data_layers=True,depsgraph=depsgraph)
        copy=bpy.data.objects.new(obj.name+' | web mesh',mesh)
        copy.matrix_world=obj.matrix_world.copy()
        for col in obj.users_collection: col.objects.link(copy)
    export_path=os.path.join(ROOT,'scripts','export_web_model.py')
    with open(export_path,encoding='utf-8-sig') as f: code=f.read()
    code=code.replace("OUT=os.path.join(ROOT,'docs','assets')","OUT=os.path.join(ROOT,'docs','preview95','assets')")
    code=code.replace("os.path.join(ROOT,'web-tools','.cache','house-raw.glb')","os.path.join(ROOT,'web-tools','.cache','photographic95','house-raw.glb')")
    code=code.replace("'source_model':'Casa_de_Campo_Final.blend'","'source_model':os.path.basename(bpy.data.filepath)")
    code=code.replace("bs=m.node_tree.nodes.get('Principled BSDF')", "bs=next((node for node in m.node_tree.nodes if node.type=='BSDF_PRINCIPLED'),None) or m.node_tree.nodes.new('ShaderNodeBsdfPrincipled')")
    code=code.replace(" cache[old.name]=m;return m", " if 'leaf95' in old.name:\n  attr=m.node_tree.nodes.new('ShaderNodeVertexColor');attr.layer_name='botanical_tint';m.node_tree.links.new(attr.outputs['Color'],bs.inputs['Base Color'])\n cache[old.name]=m;return m")
    code=code.replace("use_selection=True,export_apply=True", "use_selection=True,use_active_scene=True,export_apply=True")
    # Preserve the authored mineral mean and roughness in the standalone glTF as well.
    code=code.replace(" bs.inputs['Base Color'].default_value=color;", " if old.get('finish_scale_m') is not None:\n  ramp=next((link.from_node for link in src.inputs['Base Color'].links if link.from_node.type=='VALTORGB'),None) if src else None\n  if ramp:color=tuple(sum(e.color[k] for e in ramp.color_ramp.elements)/len(ramp.color_ramp.elements) for k in range(4))\n bs.inputs['Base Color'].default_value=color;")
    # New authored leaf units must not be torn apart by the legacy generic decimator.
    code=code.replace("elif len(o.data.vertices)>50000 and", "elif not o.name.startswith('MAT95 |') and len(o.data.vertices)>50000 and")
    # Botanical assets retain author UVs and shared data; avoid the generic adaptation.
    code=code.replace(" o.data=o.data.copy()", " if not o.name.startswith('BOT95 |'):o.data=o.data.copy()")
    code=code.replace("  for poly in o.data.polygons:", "  for poly in ([] if o.name.startswith('BOT95 |') else o.data.polygons):")
    code=code.replace(" if old.name in cache:return cache[old.name]", " if 'tree_small_02' in old.name:return old\n if old.name in cache:return cache[old.name]")
    code=code.replace("elif not o.name.startswith('MAT95 |')", "elif not o.name.startswith(('MAT95 |','BOT95 |'))")
    # Photographic oak already has metric UV0 and export-compatible PBR nodes.
    code=code.replace(" if old.name in cache:return cache[old.name]", " if old.get('photographic_wood') or old.get('photographic_masonry') or old.get('photographic_garment'):return old\n if old.name in cache:return cache[old.name]")
    code=code.replace("for poly in ([] if o.name.startswith('BOT95 |') else o.data.polygons):", "for poly in ([] if o.name.startswith('BOT95 |') or any(slot.material and (slot.material.get('photographic_wood') or slot.material.get('photographic_masonry') or slot.material.get('photographic_garment')) for slot in o.material_slots) else o.data.polygons):")
    exec(compile(code,export_path,'exec'),dict(__file__=export_path,__name__='__main__'))


if '--candidate' in sys.argv:
    binding_path=os.path.join(ROOT,'docs','preview95','assets','view-bindings.json')
    if os.path.isfile(binding_path):
        bindings=json.load(open(binding_path,encoding='utf8'))
        info_path=os.path.join(ROOT,'docs','preview95','assets','model-info.json')
        info=json.load(open(info_path,encoding='utf8'))
        import runpy
        optics_module=runpy.run_path(os.path.join(ROOT,'docs','preview95','camera-optics.py'))
        info['cameras']=optics_module['camera_optics'](scene)
        info['cameraOpticsBasis']='Blender Camera.view_frame(scene), near-normalized frustum; viewer contains full source frame at any aspect'
        for view in bindings.get('views',[]):
            assert any(c['name']==view['camera'] for c in info['cameras']),'Requested viewer camera is absent: '+view['camera']
        info['viewerViews']=bindings.get('views',[])
        info['downloads']={'blender':bindings.get('blenderDownloadURL')}
        info['gi']={'enabled':False,'reason':'No source-matched GI approved for this publication'}
        with open(info_path,'w',encoding='utf8') as f:json.dump(info,f,ensure_ascii=False,indent=2)

assert hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest()==source_hash_at_start,'Source changed during read-only export'
