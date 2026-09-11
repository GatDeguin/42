"""Authored metric ceramic PBR maps:300mm module,3.5mm grout,0.6mm recess."""
from pathlib import Path
import numpy as np,json,hashlib
from PIL import Image
OUT=Path(r'D:\2026\42\source\photographic99_pavimento');OUT.mkdir(exist_ok=True)
N=2048;period=1.2;pitch=.3;grout=.0035;bevel=.0008;rng=np.random.default_rng(991042)
x=(np.arange(N,dtype=np.float32)+.5)*period/N;y=x.copy();X,Y=np.meshgrid(x,y)
dx=np.minimum(X%pitch,pitch-X%pitch);dy=np.minimum(Y%pitch,pitch-Y%pitch);dist=np.minimum(dx,dy)
f=np.clip((dist-grout/2)/bevel,0,1);f=f*f*(3-2*f)
noise=np.zeros((N,N),np.float32)
for scale,amp,count in [(4,.0018,8),(14,.0012,10),(53,.0007,12),(181,.0004,16)]:
 for j in range(count):
  kx=int(rng.integers(1,scale+1));ky=int(rng.integers(1,scale+1));phase=rng.uniform(0,2*np.pi)
  noise+=amp/np.sqrt(count)*np.cos(2*np.pi*(kx*X+ky*Y)/period+phase)
tile_variation=rng.uniform(-.006,.006,(4,4)).astype(np.float32)[np.floor(Y/pitch).astype(int),np.floor(X/pitch).astype(int)]
base=np.array([.665,.642,.586],np.float32)[None,None,:]+(noise+tile_variation)[...,None]
grout_col=np.array([.48,.475,.445],np.float32)[None,None,:]
linear=grout_col*(1-f[...,None])+base*f[...,None]
srgb=np.where(linear<=.0031308,linear*12.92,1.055*linear**(1/2.4)-.055)
Image.fromarray(np.clip(srgb*255+.5,0,255).astype(np.uint8),'RGB').save(OUT/'tile300_basecolor.png',optimize=True)
rough=np.clip(.66*(1-f)+(.275+noise*7)*f,0,1)
Image.fromarray((rough*255+.5).astype(np.uint8),'L').save(OUT/'tile300_roughness.png',optimize=True)
height=-.0006*(1-f)+noise*.0015*f
gy,gx=np.gradient(height,period/N,period/N);norm=np.stack([-gx,gy,np.ones_like(gx)],axis=-1);norm/=np.linalg.norm(norm,axis=-1,keepdims=True)
Image.fromarray(np.clip((norm*.5+.5)*255+.5,0,255).astype(np.uint8),'RGB').save(OUT/'tile300_normal.png',optimize=True)
report={'author':'Procedural dimensional ceramic maps authored for this project; not a vendor product','resolution':[N,N],'period_m':period,'module_m':pitch,'grout_width_m':grout,'edge_transition_m':bevel,'grout_recess_m':.0006,'normal_convention':'OpenGL tangent; image-down derivative converted to UV-up','color_encoding':'sRGB basecolor; linear roughness/normal','files':{}}
for p in OUT.glob('*.png'):report['files'][p.name]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(OUT/'material.json').write_text(json.dumps(report,indent=2),'utf8');print(json.dumps(report,indent=2))
