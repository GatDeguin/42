import runpy,sys,os,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
steps=['scripts/correcciones95_dimensiones_r6.py','docs/preview95/stools/apply.py','scripts/correcciones95_recorrido_r6.py','scripts/correcciones95_fotografia_r6.py','scripts/correcciones95_luminarias_r6.py']
for rel in steps:
 p=os.path.join(ROOT,rel);sys.argv=[p];print('INTEGRATING',rel,flush=True);t=time.time();runpy.run_path(p,run_name='__main__');print('INTEGRATED',rel,round(time.time()-t,1),flush=True)
print('R6J_COORDINATED_CANDIDATE_READY',flush=True)
