import fs from 'node:fs';
let f='web-tools/photographic95-build.mjs',s=fs.readFileSync(f,'utf8');
s=s.replace("js=js.replace('let renderer, scene, camera, controls,','let photo, renderer, scene, camera, controls,');", "js=js.replace('let renderer, scene, camera, controls,','let photo, renderer, scene, camera, controls,');\njs=js.replace(\"const webTextures={}\",\"const assetRoot=new URLSearchParams(location.search).has('candidate')?'./assets/':'../assets/';\\nconst webTextures={}\");\njs=js.replace(\"fetch('../assets/model-info.json')\",\"fetch(assetRoot+'model-info.json')\");\njs=js.replace(\"fetch('../assets/textures/wood-surfaces.json')\",\"fetch(assetRoot+'textures/wood-surfaces.json')\");\njs=js.replace(\"loader.loadAsync('../assets/house.glb',\",\"loader.loadAsync(assetRoot+'house.glb',\");");
fs.writeFileSync(f,s);
fs.copyFileSync('docs/preview95/assets/optics.json','docs/preview95/assets/optics-original.json');
f='docs/preview95/photographic.js';s=fs.readFileSync(f,'utf8').replace("fetch('./assets/optics.json')", "fetch(new URLSearchParams(location.search).has('candidate')?'./assets/optics.json':'./assets/optics-original.json')");fs.writeFileSync(f,s);
f='scripts/web95_optics_export.py';s=fs.readFileSync(f,'utf8');
s=s.replace("    export_path=os.path.join(ROOT,'scripts','export_web_model.py')",`    # Convert evaluated FONT/CURVE objects only in this unsaved export process.
    depsgraph=bpy.context.evaluated_depsgraph_get()
    for obj in list(scene.objects):
        if obj.type not in ('FONT','CURVE') or obj.hide_render: continue
        mesh=bpy.data.meshes.new_from_object(obj.evaluated_get(depsgraph),preserve_all_data_layers=True,depsgraph=depsgraph)
        copy=bpy.data.objects.new(obj.name+' | web mesh',mesh)
        copy.matrix_world=obj.matrix_world.copy()
        for col in obj.users_collection: col.objects.link(copy)
    export_path=os.path.join(ROOT,'scripts','export_web_model.py')`);
s=s.replace("    exec(compile(code,export_path,'exec')",`    # New authored leaf units must not be torn apart by the legacy generic decimator.
    code=code.replace("elif len(o.data.vertices)>50000 and", "elif not o.name.startswith('MAT95 |') and len(o.data.vertices)>50000 and")
    exec(compile(code,export_path,'exec')`);
fs.writeFileSync(f,s);
