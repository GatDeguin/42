import bpy,os,runpy,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.argv=[sys.argv[0]]
for name in ['correcciones95_acabados_r5.py','correcciones95_productos_r5.py','correcciones95_apoyos_muebles_r6.py','correcciones95_mono_r6.py','correcciones95_guardados_r6.py']:
 print('INTEGRATING',name,flush=True);runpy.run_path(os.path.join(ROOT,'scripts',name),run_name='__main__')
print('R6C_INTEGRATED',bpy.data.filepath,flush=True)
