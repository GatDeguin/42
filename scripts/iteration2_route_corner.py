import bpy,os,json,ast,numpy as np
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'output');S=bpy.context.scene
def cv(p):return Vector((p[0],-p[2],p[1]))
R=json.load(open(os.path.join(OUT,'tour_route.json'),encoding='utf8'));shots=R['shots'];s=shots[3]
s['points'][3]=[20.7,1.86,12.8];s['targets'][3]=[21.25,1.35,10.8];s['seconds']=10;s['knot_times']=[0,.25,.52,.8,1]
# Reuse only route keyframing, without repeating prior geometry changes.
source=open(os.path.join(ROOT,'scripts','iteration2_pass2.py'),encoding='utf8').read();source=source[source.index('# Piecewise Hermite'):];exec(compile(source,'route_final','exec'))
print('FINAL_ROUTE_CORNER_FIXED',flush=True)
