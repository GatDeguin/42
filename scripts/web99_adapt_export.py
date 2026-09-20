"""R7 changes to the legacy read-only web adapter; source blend is never saved."""
def adapt(code):
    excluded="  if any(w in o.name for w in ['Entorno | terreno continuo','Paisaje | pradera de transición']):continue"
    assert excluded in code
    code=code.replace(excluded,"  # R7 exports the original terrain and its transition planting.")
    code=code.replace("('CAM | ','REV | ')","('CAM | ','REV | ','LUZ99 | ')")
    code=code.replace("elif not o.name.startswith(('MAT95 |','BOT95 |'))", "elif not o.name.startswith(('MAT95 |','BOT95 |','Paisaje | pradera de transición'))")
    code=code.replace("and len(o.data.vertices)>50000", "and not o.get('preserve_complete_leaves') and not o.get('grass8_preserve_faces_on_export') and len(o.data.vertices)>50000")
    code=code.replace(" for k in list(o.keys()):del o[k]", " preserve_full=bool(o.get('preserve_complete_leaves') or o.get('grass8_preserve_faces_on_export'))\n for k in list(o.keys()):del o[k]\n if preserve_full:o['preserveFullGeometry']=True")
    marker="stats['objects']=len(selected)"
    assert marker in code
    code=code.replace(marker,marker+"\nstats['sourceTerrain']=any(o.name=='Entorno | terreno continuo' for o in selected)\nstats['landscapeGeometry']='Full source terrain and transition meadow; no substitute flat plane.'")
    # Blender needs triangulated n-gons when exporting tangent frames for normal maps.
    # These modifiers live only in the unsaved export copy; the editable source stays intact.
    tangent_prep="""triangulated_normal_meshes=[]
for obj in selected:
 if obj.type!='MESH' or not any(m and any(m.get(tag) for tag in ['photographic99','photographic_masonry','photographic_wood','photographic_garment']) for m in obj.data.materials):continue
 ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());evaluated_mesh=ev.to_mesh();has_ngons=any(len(p.vertices)>4 for p in evaluated_mesh.polygons);ev.to_mesh_clear()
 if has_ngons:
  modifier=obj.modifiers.new('WEB99 tangent triangulation','TRIANGULATE');modifier.ngon_method='BEAUTY';modifier.min_vertices=5
  if hasattr(modifier,'keep_custom_normals'):modifier.keep_custom_normals=True
  triangulated_normal_meshes.append(obj.name)
stats['tangentTriangulationObjects']=triangulated_normal_meshes
"""
    code=code.replace("stats['objects']=len(selected)",tangent_prep+"stats['objects']=len(selected)")
    code=code.replace("export_texcoords=True,export_normals=True","export_texcoords=True,export_normals=True,export_tangents=True")
    return code
