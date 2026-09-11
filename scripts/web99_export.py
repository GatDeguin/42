"""Read-only R7 web export preserving full botanical canopy. Uses the audited export pipeline."""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source=os.path.join(ROOT,'scripts','web95_optics_export.py')
code=open(source,encoding='utf-8-sig').read()
code=code.replace("'preview95'","'preview99'").replace("'photographic95'","'photographic99'")
# Keep every leaf and every branch. Shared geometry is deduplicated on export.
old="target=min(len(ids),20000 if foreground else 4000) if 'leaves' in mat.name else (max(1,int(len(ids)*(.5 if foreground else .15))) if 'branches' in mat.name else len(ids))"
assert old in code
code=code.replace(old,"target=len(ids)")
code=code.replace("lod='foreground' if foreground else 'background'","lod='full_canopy_no_components_removed'")
# New R7 material families provide metric UV0 and exportable PBR nodes.
code=code.replace("old.get('photographic_garment')","old.get('photographic_garment') or old.get('photographic99')")
code=code.replace("slot.material.get('photographic_garment')","slot.material.get('photographic_garment') or slot.material.get('photographic99')")
# Derive optical water depth from the actual evaluated basin volume.
water_code="""water_obj=bpy.data.objects.get('Agua de pileta')
optical_water=None
if water_obj:
    ev=water_obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    heights=[(ev.matrix_world@Vector(v)).z for v in ev.bound_box]
    optical_water=dict(maxDepthMetres=max(heights)-min(heights),surfaceHeight=max(heights),bottomHeight=min(heights),scope='Maximum source water depth; raster uses a constant optical thickness.')
"""
code=code.replace("out = os.path.join(ROOT,'docs','preview99','assets','optics.json')",water_code+"\nout = os.path.join(ROOT,'docs','preview99','assets','optics.json')")
code=code.replace("dict(source=bpy.data.filepath, scene=scene.name,","dict(source=bpy.data.filepath, sourceSHA256=source_hash_at_start, water=optical_water, scene=scene.name,")
# Adapt the nested legacy exporter without changing the frozen R6K scripts.
nested="    exec(compile(code,export_path,'exec'),dict(__file__=export_path,__name__='__main__'))"
assert nested in code
code=code.replace(nested,"    import runpy\n    code=runpy.run_path(os.path.join(ROOT,'scripts','web99_adapt_export.py'))['adapt'](code)\n"+nested)
exec(compile(code,source,'exec'),dict(__file__=source,__name__='__main__'))
