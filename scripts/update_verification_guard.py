from pathlib import Path
root=Path(r'D:\2026\42')
p=root/'scripts/verify_revision.py';s=p.read_text(encoding='utf8')
a=s.index('# Sweep tests');b=s.index('# Panel meshes')
s=s[:a]+'''# Reproduce evaluated mesh tests for all moving assemblies across27poses.
exec(compile(open(os.path.join(ROOT,'scripts','verify_coordination.py'),encoding='utf8').read(),'verify_coordination.py','exec'),{})
coord=json.load(open(os.path.join(OUT,'coordinated_mesh_checks.json'),encoding='utf8'))
ck('All movable door meshes avoid walls across27sampledposes (evaluated BVH)',not coord['all_door_leaf_wall_intersections'],coord['all_door_leaf_wall_intersections'])
ck('Extraction pipes avoid evaluated enclosure and structural meshes',not coord['pipe_structure_intersections'],coord['pipe_structure_intersections'])
primary={k:[o for o in e.children if o.type=='MESH'] for k,e in rigs.items()}
''' +s[b:]
s=s.replace("me=o.data;return BVHTree.FromPolygons([o.matrix_world@v.co for v in me.vertices],[list(p.vertices) for p in me.polygons])","dg=bpy.context.evaluated_depsgraph_get();e=o.evaluated_get(dg);me=e.to_mesh();tree=BVHTree.FromPolygons([o.matrix_world@v.co for v in me.vertices],[list(p.vertices) for p in me.polygons]);e.to_mesh_clear();return tree")
s=s.replace("'door_primary':","'tested_moving_meshes':")
p.write_text(s,encoding='utf8')
p=root/'scripts/render.py';s=p.read_text(encoding='utf8');s=s.replace("if mode=='hero':","if mode=='tour' and S.get('video_render_requires_explicit_approval',True):\n raise RuntimeError('Video rendering paused by owner. Explicit approval is required before changing this project flag.')\nif mode=='hero':");p.write_text(s,encoding='utf8')
p=root/'scripts/encode_video.py';s=p.read_text(encoding='utf8');s=s.replace("import os,json,sys,subprocess","import os,json,sys,subprocess\nraise SystemExit('Video encoding paused by owner. Resume this pipeline only after explicit approval.')");p.write_text(s,encoding='utf8')
p=root/'.gitignore';s=p.read_text(encoding='utf8')+'\n*.blend@\nreview/*.log\nreview/pass2_*.png\noutput/Casa_de_Campo.blend\noutput/control_*.png\noutput/Casa_de_Campo_Atardecer.png\n';p.write_text(s,encoding='utf8')
