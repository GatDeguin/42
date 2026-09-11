"""Prepared R7 edited camera route. No rendering and no save by apply()."""
import bpy,json,os,math,ast,hashlib,numpy as np
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def cv(p):return Vector((p[0],-p[2],p[1]))
for node in ast.parse(open(os.path.join(ROOT,'scripts','iteration2_pass2.py'),encoding='utf8').read()).body:
    if isinstance(node,ast.FunctionDef) and node.name=='interp':exec(compile(ast.Module(body=[node],type_ignores=[]),'<route interpolation>','exec'))
def apply():
    S=bpy.context.scene;S.frame_set(1)
    route=json.load(open(os.path.join(ROOT,'review95','r6_tour_route.json'),encoding='utf8'))
    shots=route['shots'];changes=[]
    def change(number,points,targets,seconds=None):
        shot=shots[number-1];changes.append(dict(shot=shot['title'],oldPoints=shot['points'],newPoints=points))
        shot['points']=points;shot['targets']=targets;shot['knot_times']=list(np.linspace(0,1,len(points)))
        if seconds:shot['seconds']=seconds
    change(2,[[12.1,1.71,7.3],[12.3,1.74,8.5],[14.8,1.83,8.60],[16.1,1.86,8.60],[18.0,1.86,7.0]],[[17.8,1.45,9],[18,1.5,8.8],[20.7,1.5,8.9],[20.7,1.5,8.5],[18,1.5,4.3]])
    change(10,[[17.10,4.90,9.45],[17.10,4.90,8.55],[17.10,4.90,7.68],[18.28,4.90,7.68],[18.28,4.90,8.20]],
        [[16.25,4.30,7.45],[15.2,4.2,7.4],[18.6,4.5,7.68],[18.52,4.5,6.55],[18.52,4.4,6.45]])
    change(3,[[18,1.86,7],[18,1.86,5.15],[18.12,1.86,3.70],[18.12,1.86,2.0],[18.12,1.86,.80],[20.0,1.86,.80]],
        [[17.2,1.4,4.5],[16.4,1.3,3.9],[15.2,1.4,4.0],[20.2,1.4,.8],[20.5,1.4,.85],[21.3,1.2,1.15]],seconds=10)
    cam=bpy.data.objects['TOUR | Recorrido virtual'];target=bpy.data.objects['TOUR | Punto de mirada']
    cam.animation_data_clear();cam.data.animation_data_clear();target.animation_data_clear();cam.rotation_mode='QUATERNION'
    S.timeline_markers.clear();frame=1;previous=None
    for shot in shots:
        count=round(shot['seconds']*route['fps']);shot['start']=frame;shot['end']=frame+count-1
        times=shot.get('knot_times',list(np.linspace(0,1,len(shot['points']))));samples=[]
        S.timeline_markers.new(shot['title'],frame=frame)
        path=bpy.data.objects.get('PATH | '+shot['title'])
        if path:
            path.data.splines.clear();sp=path.data.splines.new('POLY');sp.points.add(len(shot['points'])-1)
            for point,pos in zip(sp.points,shot['points']):point.co=(*cv(pos),1)
        for j in range(count):
            u=j/(count-1);p=interp(shot['points'],u,times);t=interp(shot['targets'],u,times);q=(cv(t)-cv(p)).to_track_quat('-Z','Y')
            if previous is not None and previous.dot(q)<0:q.negate()
            previous=q.copy();cam.location=cv(p);cam.rotation_quaternion=q
            cam.keyframe_insert('location',frame=frame);cam.keyframe_insert('rotation_quaternion',frame=frame)
            cam.data.lens=shot['lens'];cam.data.keyframe_insert('lens',frame=frame)
            target.location=cv(t);target.keyframe_insert('location',frame=frame);samples.append(p);frame+=1
        shot['samples']=samples
    for ob in [cam,cam.data,target]:
        for layer in ob.animation_data.action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for fcurve in bag.fcurves:
                        for k in fcurve.keyframe_points:k.interpolation='LINEAR'
    S.frame_end=frame-1;route.update(frames=frame-1,video_status='PAUSED_PENDING_EXPLICIT_USER_APPROVAL',revision='R7 direct bedroom access and frontage mono bathroom',changes=changes)
    route['checksPending']='Final integrated source; actual door timeline, clear eye and torso paths.'
    json.dump(route,open(os.path.join(ROOT,'review99','tour_route.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
    S['video_render_requires_explicit_approval']=True;S['tour_route_requires_revalidation_after_layout']=True
    S['r7_tour_prepared']=True;S.frame_set(1)
    return route
def verify(route,output,applied_in_memory=True):
    S=bpy.context.scene;before=S.frame_current;rows=[];raysCount=0;camera_errors=[];camera=bpy.data.objects['TOUR | Recorrido virtual']
    for shot in route['shots']:
        hits={};tested=[]
        for j in sorted(set(range(0,len(shot['samples']),6))|{len(shot['samples'])-1}):
            frame=shot['start']+j;S.frame_set(frame);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
            eye=camera.matrix_world.translation.copy();position_error=(eye-cv(shot['samples'][j])).length
            if position_error>.0001:camera_errors.append(dict(frame=frame,error_m=position_error))
            rays=[(eye,Vector((0,0,-1)),1.35,'below')]
            for k in range(12):
                a=k*math.tau/12;direction=Vector((math.cos(a),math.sin(a),0))
                rays.extend([(eye-Vector((0,0,.60)),direction,.20,'torso'),(eye,direction,.12,'eye')])
            for origin,direction,dist,kind in rays:
                hit,pt,n,idx,obj,matrix=S.ray_cast(dg,origin,direction,distance=dist);raysCount+=1
                if hit:hits.setdefault((obj.name,kind),[]).append(frame)
            tested.append(frame)
        rows.append(dict(title=shot['title'],testedFrames=tested,hits=[dict(object=name,kind=kind,frames=frames) for (name,kind),frames in hits.items()]))
    S.frame_set(before)
    report=dict(model=bpy.data.filepath,sourceFileSHA256=hashlib.sha256(open(bpy.data.filepath,'rb').read()).hexdigest(),routeAppliedInMemory=applied_in_memory,cameraPositionErrors=camera_errors,routeRevision=route['revision'],videoRendered=False,method='Actual animated door pose at sampled route frame. 200 mm radial torso,120 mm eye clearance,1.35 m ray below eye. All scene-raycast meshes retained; not a human accessibility certification.',rays=raysCount,shots=rows,passed=not camera_errors and all(not row['hits'] for row in rows))
    json.dump(report,open(output,'w',encoding='utf8'),ensure_ascii=False,indent=2)
    print('R7_ROUTE_QA',json.dumps({k:report[k] for k in ['passed','rays','shots']},ensure_ascii=True),flush=True)
    return report
if __name__=='__main__':
    route=apply();verify(route,os.path.join(ROOT,'review99','tour_checks_layout.json'))
