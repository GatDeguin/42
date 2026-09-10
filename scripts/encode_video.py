import os,json,sys,subprocess
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'output')
sys.path.insert(0,os.path.join(ROOT,'tools'))
import imageio_ffmpeg
ff=imageio_ffmpeg.get_ffmpeg_exe()
route=json.load(open(os.path.join(OUT,'tour_route.json'),encoding='utf8'))
shots=route['shots'];clips=os.path.join(OUT,'tour_clips');os.makedirs(clips,exist_ok=True)
font='C\\:/Windows/Fonts/segoeui.ttf'
for i,s in enumerate(shots):
 textfile=os.path.join(clips,'label%02d.txt'%i)
 label=s['title'].split(' · ',1)[1]
 open(textfile,'w',encoding='utf8').write(label)
 textArg=textfile.replace('\\','/').replace(':','\\:')
 vf="drawbox=x=38:y=h-83:w=560:h=50:color=black@0.25:t=fill:enable='lt(t,2.5)',drawtext=fontfile='"+font+"':textfile='"+textArg+"':x=56:y=h-67:fontsize=21:fontcolor=white:enable='lt(t,2.5)'"
 cmd=[ff,'-y','-hide_banner','-loglevel','error','-framerate','24','-start_number',str(s['start']),'-i',os.path.join(OUT,'tour_frames','%05d.png'),'-frames:v',str(s['end']-s['start']+1),'-vf',vf,'-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',os.path.join(clips,'%02d.mp4'%i)]
 subprocess.run(cmd,check=True);print('ENCODED SHOT',i+1,flush=True)
inputs=[]
for i in range(len(shots)):inputs+=['-i',os.path.join(clips,'%02d.mp4'%i)]
chain=[];duration=shots[0]['seconds'];current='0:v'
for i in range(1,len(shots)):
 offset=duration-.5;label='x'+str(i)
 chain.append('[%s][%d:v]xfade=transition=fade:duration=0.5:offset=%.6f[%s]'%(current,i,offset,label))
 duration+=shots[i]['seconds']-.5;current=label
output=os.path.join(OUT,'Casa_de_Campo_Recorrido.mp4')
subprocess.run([ff,'-y','-hide_banner','-loglevel','error',*inputs,'-filter_complex',';'.join(chain),'-map','['+current+']','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',output],check=True)
json.dump({'file':output,'seconds':duration,'fps':24,'resolution':[1280,720],'render_engine':'Cycles/OptiX','samples':24,'shot_count':len(shots),'transition_seconds':.5,'frames_before_edit':route['frames']},open(os.path.join(OUT,'video_metadata.json'),'w'),indent=2)
print('VIDEO',output,'duration',duration,flush=True)
