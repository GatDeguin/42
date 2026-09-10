import bpy,runpy
runpy.run_path('scripts/correcciones95_apoyos_dvh.py',run_name='__main__')
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=r'D:\2026\42\output\Casa_de_Campo_95_R6K_DVH_preview.blend',compress=True)
