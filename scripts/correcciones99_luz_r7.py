"""R7 pass 3: manufactured optical finishes, physical luminaire sampling and cameras.
Apply on a copy of the coordinated candidate, never on the frozen R6K.
No rendering, animations, video, external publishing, or structural edits.
All distances are metres. Blender coordinates are (source X, -source Z, height).
"""
import bpy, json, os, sys, math, hashlib
import numpy as np
from mathutils import Vector, Matrix

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,'review99','lighting')
TEX=os.path.join(ROOT,'source','photographic99_luz')
PREFIX='LUZ99 | '
S=bpy.context.scene

def bounds(o):
    pts=[o.matrix_world@Vector(p) for p in o.bound_box]
    return Vector([min(p[i] for p in pts) for i in range(3)]),Vector([max(p[i] for p in pts) for i in range(3)])

def material(name,color,roughness,metal=0,period=.05,grain=0):
    full=PREFIX+name
    m=bpy.data.materials.get(full) or bpy.data.materials.new(full)
    m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;n.clear()
    bs=n.new('ShaderNodeBsdfPrincipled');out=n.new('ShaderNodeOutputMaterial');l.new(bs.outputs['BSDF'],out.inputs['Surface'])
    bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=roughness;bs.inputs['Metallic'].default_value=metal
    m.diffuse_color=(*color,1);m['photographic99']=True;m['texture_period_m']=period
    m['finish99']='Manufactured generic finish; no product certification or artificial dirt.'
    if grain:
        N=512;rng=np.random.default_rng(99013+int(roughness*100))
        noise=rng.normal(0,1,(N,N))
        # Periodic grain; weak 4-neighbour filter removes isolated, sparkle-like pixels.
        noise=(noise*2+np.roll(noise,1,0)+np.roll(noise,-1,0)+np.roll(noise,1,1)+np.roll(noise,-1,1))/6
        noise/=max(float(noise.std()),.00001)
        rough=np.clip(roughness+noise*.006,0,1)
        arr=np.ones((N,N,4),dtype=np.float32);arr[:,:,:3]=rough[:,:,None]
        im=write_image(name+'_rough',arr)
        tex=n.new('ShaderNodeTexImage');tex.image=im;tex.interpolation='Linear';l.new(tex.outputs['Color'],bs.inputs['Roughness'])
        # Height amplitude is physically declared; normal map, not a displacement that changes dimensions.
        height=noise*grain;dx=(np.roll(height,-1,1)-np.roll(height,1,1))/(2*period/N)
        dy=(np.roll(height,-1,0)-np.roll(height,1,0))/(2*period/N)
        vec=np.dstack([-dx,-dy,np.ones_like(dx)]);vec/=np.linalg.norm(vec,axis=2)[:,:,None]
        arr[:,:,:3]=vec*.5+.5;im=write_image(name+'_normal',arr)
        tex=n.new('ShaderNodeTexImage');tex.image=im;normal=n.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=1
        l.new(tex.outputs['Color'],normal.inputs['Color']);l.new(normal.outputs['Normal'],bs.inputs['Normal'])
        m['surface_rms_m']=grain
    return m

def write_image(name,arr):
    safe=''.join(c if c.isalnum() or c in '-_' else '_' for c in name)
    path=os.path.join(TEX,safe+'.png')
    im=bpy.data.images.get('PHOTO99_luz_'+safe)
    if im:bpy.data.images.remove(im)
    im=bpy.data.images.new('PHOTO99_luz_'+safe,width=arr.shape[1],height=arr.shape[0],alpha=True)
    im.colorspace_settings.name='Non-Color';im.pixels.foreach_set(arr.astype(np.float32).ravel())
    im.file_format='PNG';im.filepath_raw=path;im.save();im.pack()
    return im

def metric_uv(o,period):
    if o.type!='MESH':return
    if o.data.users>1:o.data=o.data.copy()
    uv=o.data.uv_layers.active or o.data.uv_layers.new(name='UVMap')
    uv.name='UVMap'
    m=o.matrix_world;norm=m.to_3x3().inverted_safe().transposed()
    for p in o.data.polygons:
        axis=max(range(3),key=lambda i:abs((norm@p.normal)[i]));axes=[i for i in range(3) if i!=axis]
        for li in p.loop_indices:
            v=m@o.data.vertices[o.data.loops[li].vertex_index].co
            uv.data[li].uv=(v[axes[0]]/period,v[axes[1]]/period)
    o['uv99']='World-metric tri-planar face UV; material texture period in metres.'

def assign(o,m,replace_only=None):
    if o.type not in ['MESH','CURVE','FONT']:return
    if replace_only is None:o.data.materials.clear();o.data.materials.append(m)
    else:
        for i,old in enumerate(o.data.materials):
            if old and old.name in replace_only:o.data.materials[i]=m
    if o.type=='MESH':metric_uv(o,m.get('texture_period_m',1))

def link(o,col='LUZ99_LIGHTING'):
    c=bpy.data.collections.get(col)
    if c is None:c=bpy.data.collections.new(col);S.collection.children.link(c)
    c.objects.link(o);o['photographic99_detail']=True
    return o

def box(name,p,size,mat,bevel=.001):
    x,y,z=[v/2 for v in size]
    vs=[(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)]
    fs=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    me=bpy.data.meshes.new(PREFIX+name);me.from_pydata(vs,[],fs);me.update()
    o=link(bpy.data.objects.new(PREFIX+name,me));o.location=p;assign(o,mat)
    if bevel:
        md=o.modifiers.new('Fabricated edge radius','BEVEL');md.width=bevel;md.segments=3
        md=o.modifiers.new('Weighted planar normals','WEIGHTED_NORMAL');md.keep_sharp=True
    return o

def cylinder(name,a,b,r,mat,N=32):
    a,b=Vector(a),Vector(b);t=(b-a).normalized();u=t.cross(Vector((1,0,0)) if abs(t.x)<.9 else Vector((0,1,0))).normalized();v=t.cross(u);mid=(a+b)*.5
    vs=[p-mid+r*(u*math.cos(k*math.tau/N)+v*math.sin(k*math.tau/N)) for p in [a,b] for k in range(N)]
    fs=[tuple(range(N-1,-1,-1)),tuple(range(N,2*N))]
    fs += [(k,(k+1)%N,N+(k+1)%N,N+k) for k in range(N)]
    me=bpy.data.meshes.new(PREFIX+name);me.from_pydata(vs,[],fs);me.update()
    o=link(bpy.data.objects.new(PREFIX+name,me));o.location=mid;assign(o,mat)
    for f in me.polygons:f.use_smooth=len(f.vertices)==4
    return o

def ring_x(name,x0,x1,cy,cz,outer,inner,mat):
    N=64;vs=[]
    for x,r in [(x0,outer),(x1,outer),(x1,inner),(x0,inner)]:
        vs.extend([(x,cy+r*math.sin(k*math.tau/N),cz+r*math.cos(k*math.tau/N)) for k in range(N)])
    fs=[]
    for j in range(4):
        for k in range(N):q=(k+1)%N;jj=(j+1)%4;fs.append((j*N+k,j*N+q,jj*N+q,jj*N+k))
    me=bpy.data.meshes.new(PREFIX+name);me.from_pydata(vs,[],fs);me.update()
    o=link(bpy.data.objects.new(PREFIX+name,me));assign(o,mat)
    for f in me.polygons:f.use_smooth=True
    return o

def area(name,p,target,power,size,size_y,color):
    data=bpy.data.lights.new(PREFIX+name,'AREA');data.energy=power;data.shape='RECTANGLE';data.size=size;data.size_y=size_y;data.color=color
    o=link(bpy.data.objects.new(PREFIX+name,data));o.location=p;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    o['radiometric_note']='Blender radiant power W, not electric lamp wattage. Generic dimmed design proposal.'
    return o

def make_camera(name,source_p,source_target,lens,aspect=(4,3),shift=0,frame=1):
    full=PREFIX+name;data=bpy.data.cameras.new(full);data.lens=lens;data.sensor_width=36;data.clip_start=.035;data.clip_end=250
    o=link(bpy.data.objects.new(full,data));o.location=(source_p[0],-source_p[2],source_p[1])
    target=Vector((source_target[0],-source_target[2],source_target[1]));o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
    data.shift_y=shift;data.dof.use_dof=False;o['presentation_frame']=frame;o['supplemental_camera']=True;o['aspect_width']=aspect[0];o['aspect_height']=aspect[1]
    o['photographic_exposure_compensation_ev']=0.;o['camera99_note']='Companion image, original CAM/REV views retained. Camera placement needs final model occlusion proof.'
    return o

def apply():
    os.makedirs(OUT,exist_ok=True);os.makedirs(TEX,exist_ok=True);S.frame_set(1);bpy.context.view_layer.update()
    # Only owned additions are rebuilt; architecture and existing rig objects are retained.
    for o in list(bpy.data.objects):
        if o.name.startswith(PREFIX):bpy.data.objects.remove(o,do_unlink=True)
    report={'source_model':bpy.data.filepath,'pass':'R7 photographic light and manufactured details','video_rendered':False,'changes':[],'lights':[],'cameras':[],'original_cameras_preserved':[]}
    report['original_cameras_preserved']=[o.name for o in S.objects if o.type=='CAMERA']
    ceramic=material('porcelana vidriada',(.76,.755,.725),.125,period=.05,grain=.000002)
    bs=next(n for n in ceramic.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    bs.inputs['IOR'].default_value=1.50;bs.inputs['Coat Weight'].default_value=.24;bs.inputs['Coat Roughness'].default_value=.065
    seat=material('asiento UF satinado',(.76,.755,.74),.245,period=.05,grain=.000003)
    chrome=material('cromado sanitario',(.56,.575,.59),.11,1,period=.05,grain=.0000008)
    powder=material('pintura equipo negro',(.021,.024,.027),.37,.05,period=.05,grain=.000007)
    silver=material('aluminio controles',(.5,.515,.53),.25,1,period=.05,grain=.000002)
    pc=material('policarbonato bisel negro',(.011,.014,.017),.29,period=.05,grain=.000002)
    opal=material('opal lineal 3500K',(.69,.66,.60),.4,period=.05)
    bs=next(n for n in opal.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Emission Color'].default_value=(1,.82,.65,1);bs.inputs['Emission Strength'].default_value=1.5
    rub=material('elastomero base sanitario',(.28,.28,.27),.7)
    optical_count=0
    for o in list(S.objects):
        if o.type!='MESH' or o.hide_render:continue
        mats=[m.name for m in o.data.materials if m]
        if 'Porcelana sanitaria | ceramic' in mats or PREFIX+'porcelana vidriada' in mats or PREFIX+'asiento UF satinado' in mats:
            assign(o,seat if 'asiento' in o.name.lower() else ceramic,replace_only=set(mats));optical_count+=1
        low=o.name.lower()
        if any(k in low for k in ['grifería','grifo','ducha |','bañera |','pulsador','válvula lavatorio','bajada lavatorio']):
            if any(m in ['Acero | stainless',PREFIX+'cromado sanitario'] for m in mats):assign(o,chrome,replace_only={'Acero | stainless',PREFIX+'cromado sanitario'});optical_count+=1
        if o.name in ['Consola estudio','Monitor izquierdo','Monitor derecho'] or o.name.startswith('MAT95 | tira canal'):
            assign(o,powder)
        if o.name.startswith('MAT95 | capuchón fader'):assign(o,silver)
    report['changes'].append({'manufactured_finish_objects':optical_count,'glaze_roughness':.125,'glaze_micro_rms_m':.000002,'pbr_maps_packed':True})
    # These local speaker flange interfaces bridge the previous 6 mm visual separation.
    for index,o in enumerate([o for o in S.objects if o.name.startswith('MAT95 | suspensión y cono monitor')]):
        lo,hi=bounds(o);cy=(lo.y+hi.y)/2;cz=(lo.z+hi.z)/2;r=(hi.z-lo.z)/2
        ring_x('brida monitor %d'%index,17.579,17.589,cy,cz,r+.007,r*.87,powder)
        for k in range(4):
            a=math.pi/4+k*math.pi/2;rr=r+.003;y=cy+rr*math.sin(a);z=cz+rr*math.cos(a)
            cylinder('tornillo monitor %d %d'%(index,k),(17.588,y,z),(17.591,y,z),.0024,silver)
            # Recessed straight slot is a black inlay within the metal head.
            box('ranura tornillo %d %d'%(index,k),(17.5911,y,z),(.0003,.0028,.00065),pc,0)
    report['changes'].append({'speaker_flange_count':4,'speaker_mounted_fasteners':16,'preserved_cabinet_envelopes':True})
    # Screen carcass and bezel: source waveforms remain visible; no image replaces scene geometry.
    screen=bpy.data.objects.get('Pantalla estudio')
    if screen:
        assign(screen,pc)
        lo,hi=bounds(screen);front=17.548
        # Narrow bezel touches source housing, outside its central display area.
        for i,z in enumerate([lo.z+.007,hi.z-.007]):
            box('bisel pantalla horizontal %d'%i,(front,-3,z),(.007,1.18,.014),pc,.001)
        for i,y in enumerate([-2.417,-3.583]):
            box('bisel pantalla vertical %d'%i,(front,y,(lo.z+hi.z)/2),(.007,.014,.666),pc,.001)
        # The old 3D bars were an illustrative display, not equipment outside its case.
        # Replace them with a project-authored interface physically mapped to the same LCD.
        for legacy in S.objects:
            if legacy.name.startswith('DAW | '):legacy.hide_render=True;legacy.hide_set(True)
        lcd=material('LCD sesion audio',(.02,.025,.03),.20,period=1)
        nn=lcd.node_tree.nodes;ll=lcd.node_tree.links;bb=next(q for q in nn if q.type=='BSDF_PRINCIPLED')
        im=bpy.data.images.load(os.path.join(TEX,'studio_session99.png'),check_existing=True);im.colorspace_settings.name='sRGB';im.pack()
        tex=nn.new('ShaderNodeTexImage');tex.image=im;ll.new(tex.outputs['Color'],bb.inputs['Base Color']);ll.new(tex.outputs['Color'],bb.inputs['Emission Color'])
        bb.inputs['Emission Strength'].default_value=.65;bb.inputs['Coat Weight'].default_value=.15;bb.inputs['Coat Roughness'].default_value=.18
        me=bpy.data.meshes.new(PREFIX+'LCD fisico');me.from_pydata([(17.552,-3.576,lo.z+.014),(17.552,-2.424,lo.z+.014),(17.552,-2.424,hi.z-.014),(17.552,-3.576,hi.z-.014)],[],[(0,1,2,3)]);me.update();me.materials.append(lcd)
        uv=me.uv_layers.new(name='UVMap')
        for data,val in zip(uv.data,[(0,0),(1,0),(1,1),(0,1)]):data.uv=val
        panel=link(bpy.data.objects.new(PREFIX+'LCD fisico',me));mw=panel.matrix_world.copy();panel.parent=screen;panel.matrix_world=mw
        lcd['interface99']='Original illustrative audio session; no external screenshot or brand.'
        # Matte black side returns no longer emit as screen glass.
        report['changes'].append({'studio_screen':'Non-emitting moulded carcass and 14 mm bezels; original illustrative 3D DAW bars retained hidden, replaced by authored LCD interface.'})
    # R7A moved the PB bathroom to Cedro; move its actual light with it and give it a ceiling fixture.
    bath_floor=bpy.data.objects.get('Piso baño mono')
    if bath_floor and -bath_floor.matrix_world.translation.y<2.0:
        housing=material('plafon aluminio blanco',(.72,.72,.69),.34,.05)
        cylinder('plafon baño PB carcasa',(20.60,-1.05,2.969),(20.60,-1.05,3.000),.132,housing,64)
        cylinder('plafon baño PB difusor',(20.60,-1.05,2.966),(20.60,-1.05,2.969),.115,opal,64)
        source=bpy.data.objects.get('Indirecta | baño mono')
        if source:
            if 'light99_pre_r7_position' not in source:
                source['light99_pre_r7_position']=list(source.matrix_world.translation)
                source['light99_pre_r7_power']=source.data.energy
            source.location=(20.60,-1.05,2.9645);source.rotation_euler=(0,0,0)
            source.data.type='AREA';source.data.shape='DISK';source.data.size=.230
            source.data.energy=12.0;source.data.color=(1,.88,.76)
            source['radiometric_note']='12 W radiant source, generic warm-white opal ceiling fixture proposal; not electric wattage or certified photometry.'
            report['changes'].append({'bathroom_PB_light':source.name,'previous_position_blender':list(source['light99_pre_r7_position']),'previous_radiant_W':source['light99_pre_r7_power'],'new_position_source':[20.60,2.9645,1.05],'radiant_W':12,'fixture_diameter_m':.264,'fixture_top_m':3.0,'diffuser_bottom_m':2.966,'status':'P: ceiling fixture outside shower footprint, physical/IP product selection pending'})

    # Rectangular sampling surfaces coincide with the actual opal diffusers.
    pairs=[
      ('LED | Luz lineal quincho','MOB95 | difusor opal Luz lineal quincho'),
      ('LED | Luz lineal estudio','MOB95 | difusor opal Luz lineal estudio'),
      ('LED | Luz lineal vivienda','MOB95 | difusor opal Luz lineal vivienda'),
      ('LED | Lámpara comedor','MOB95 | difusor opal Lámpara comedor'),
      ('LED | Lámpara lineal cocina','MOB95 | difusor opal Lámpara lineal cocina'),
      ('LED | Luz bajo alacena cocina','MOB95 | difusor opal Luz bajo alacena cocina'),
    ]
    for lname,mname in pairs:
        light=bpy.data.objects.get(lname);surface=bpy.data.objects.get(mname)
        if not light:continue
        if not surface:
            # Other revisions can supply a source emitter without MOB prefix.
            match=mname.replace('MOB95 | difusor opal ','')
            surface=bpy.data.objects.get(match)
        if surface:
            lo,hi=bounds(surface);p=(lo+hi)/2;p.z=lo.z-.0015
            light.location=p;light.rotation_euler=(0,0,0);light.data.shape='RECTANGLE';light.data.size=max(.015,hi.x-lo.x);light.data.size_y=max(.015,hi.y-lo.y)
            light.data.color=(1,.86,.73);light['source_emitter_object99']=surface.name
            # Existing powers remain unchanged for comparison; removing disk spill changes light physically.
            report['lights'].append({'name':lname,'emitter':surface.name,'power_radiant_W':light.data.energy,'size_m':[light.data.size,light.data.size_y],'position':list(light.location)})
    # Cabinet top was occluding its sole ceiling source. Reposition the complete original fitting into the aisle.
    target_z=7.08
    fitting=bpy.data.objects.get('Vestidor luz lineal')
    old_z=-float(fitting.location.y) if fitting else 6.51
    delta=target_z-old_z
    for name in ['Vestidor luz lineal','MOB95 | difusor opal Vestidor luz lineal']:
        o=bpy.data.objects.get(name)
        if o:o.location.y-=delta
    light=bpy.data.objects.get('LED | Vestidor luz lineal')
    if light:
        light.location=(18.52,-target_z,5.7245);light.rotation_euler=(0,0,0)
        light.data.shape='RECTANGLE';light.data.size=1.325;light.data.size_y=.020;light.data.energy=30;light.data.color=(1,.87,.75)
        report['lights'].append({'name':light.name,'change':'whole fitting positioned in aisle ahead of cabinet cap', 'translation_source_z_m':delta,'power_radiant_W':30,'source_Z':target_z})
    # Short fixture supports terminate at ceiling; no independent floating luminaire.
    ceiling=5.85
    for x in [17.90,19.14]:
        cylinder('suspension vestidor %.2f'%x,(x,-target_z,5.7535),(x,-target_z,ceiling),.003,pc)
        cylinder('floron vestidor %.2f'%x,(x,-target_z,ceiling-.008),(x,-target_z,ceiling),.022,pc)
    # Under-shelf lights reveal the clothing without a photographic fill light floating in space.
    for i,(x0,x1) in enumerate([(17.76,18.25),(18.31,18.78),(18.84,19.28)]):
        cx=(x0+x1)/2;width=x1-x0
        box('perfil armario %d'%i,(cx,-6.708,5.2925),(width,.024,.010),silver,.001)
        surface=box('difusor armario %d'%i,(cx,-6.708,5.2875),(width-.012,.017,.001),opal,.0003)
        light=area('LED armario %d'%i,(cx,-6.708,5.2855),(cx,-6.48,4.45),4,width-.018,.015,(1,.86,.72))
        light['source_emitter_object99']=surface.name
        report['lights'].append({'name':light.name,'power_radiant_W':4,'fixture_parent':'Vestidor estante 5.31','profile_top':5.2975,'shelf_bottom':5.2975})

    # Real scanned grass/leaf litter at the declared two metre scale.
    # A low-frequency vertex tint avoids the previous uniform distant green sheet.
    ground=material('terreno vegetal CC0',(1,1,1),.86,period=2)
    ground['asset']='Poly Haven leafy_grass';ground['asset_license']='CC0';ground['asset_author']='Charlotte Baglioni'
    ground['asset_url']='https://polyhaven.com/a/leafy_grass';ground['material_scope']='Illustrative surrounding ground only; surveyed lot levels unchanged.'
    n=ground.node_tree.nodes;l=ground.node_tree.links;bs=next(q for q in n if q.type=='BSDF_PRINCIPLED')
    prov=json.load(open(os.path.join(TEX,'leafy_grass','provenance.json'),encoding='utf8'))
    for k,socket in [('Diffuse','Base Color'),('Rough','Roughness'),('nor_gl',None)]:
        im=bpy.data.images.load(os.path.join(TEX,'leafy_grass',os.path.basename(prov['maps'][k]['path'])),check_existing=True)
        im.colorspace_settings.name='sRGB' if k=='Diffuse' else 'Non-Color';im.pack()
        tex=n.new('ShaderNodeTexImage');tex.image=im
        if k=='Diffuse':
            vc=n.new('ShaderNodeVertexColor');vc.layer_name='landscape_tint99'
            mul=n.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1
            l.new(tex.outputs['Color'],mul.inputs[1]);l.new(vc.outputs['Color'],mul.inputs[2]);l.new(mul.outputs['Color'],bs.inputs[socket])
        elif k=='nor_gl':
            normal=n.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.65
            l.new(tex.outputs['Color'],normal.inputs['Color']);l.new(normal.outputs['Normal'],bs.inputs['Normal'])
        else:l.new(tex.outputs['Color'],bs.inputs[socket])
    terrains=[bpy.data.objects.get(name) for name in ['Entorno | terreno continuo','Entorno exterior','Césped del lote']]
    for terrain in [o for o in terrains if o is not None]:
        assign(terrain,ground)
        co=terrain.data.color_attributes.get('landscape_tint99') or terrain.data.color_attributes.new(name='landscape_tint99',type='FLOAT_COLOR',domain='POINT')
        terrain.data.color_attributes.active_color_index=list(terrain.data.color_attributes).index(co)
        terrain.data.color_attributes.render_color_index=list(terrain.data.color_attributes).index(co)
        for v,d in zip(terrain.data.vertices,co.data):
            p=terrain.matrix_world@v.co
            macro=.78+.13*math.sin(p.x*.109+p.y*.041)*math.sin(p.y*.078-p.x*.029)
            tone=.5+.5*math.sin(p.x*.071-p.y*.053)
            d.color=(macro*(.93+.07*tone),macro,macro*(.88+.08*tone),1)
        # Rotate UV axes so a camera axis cannot follow a repeated two-metre tile seam.
        uv=terrain.data.uv_layers.active;a=math.radians(23)
        for d in uv.data:
            u,v=d.uv;d.uv=(math.cos(a)*u-math.sin(a)*v,math.sin(a)*u+math.cos(a)*v)
        report['changes'].append({'terrain':'CC0 leafy_grass scanned texture, 2 m repeat; existing relief and vertex positions preserved','maps':prov['maps'],'macro_tint_range':[.65,.91]})
    meadow=bpy.data.objects.get('Paisaje | pradera de transición')
    if meadow:
        # No topology changes: preserve the removed blades below bench pads.
        m=material('briznas entorno',(1,1,1),.81);nn=m.node_tree.nodes;ll=m.node_tree.links;bb=next(q for q in nn if q.type=='BSDF_PRINCIPLED')
        co=meadow.data.color_attributes.get('landscape_tint99') or meadow.data.color_attributes.new(name='landscape_tint99',type='FLOAT_COLOR',domain='POINT')
        meadow.data.color_attributes.active_color_index=list(meadow.data.color_attributes).index(co)
        meadow.data.color_attributes.render_color_index=list(meadow.data.color_attributes).index(co)
        nnc=nn.new('ShaderNodeVertexColor');nnc.layer_name='landscape_tint99';ll.new(nnc.outputs['Color'],bb.inputs['Base Color']);bb.inputs['Subsurface Weight'].default_value=.035
        for f in meadow.data.polygons:
            center=sum((meadow.data.vertices[i].co for i in f.vertices),Vector())/len(f.vertices)
            seed=abs(math.sin(center.x*12.9898+center.y*78.233))*43758.5453;seed-=int(seed)
            dry=.5+.5*math.sin(center.x*.43+center.y*.19)
            color=(.068+.035*dry,.102+.04*(1-dry),.023+.012*dry)
            for vi in f.vertices:
                v=meadow.data.vertices[vi].co;factor=.74+.4*seed+.12*max(0,v.z-center.z)/.12
                co.data[vi].color=(*(c*factor for c in color),1)
        assign(meadow,m)
        report['changes'].append({'meadow':'Existing blades and bench clearances preserved; botanical green/ochre variation in exportable vertex colour.'})

    S.view_settings.view_transform='AgX';S.view_settings.look='AgX - Medium High Contrast';S.view_settings.exposure=.35
    for name in ['REV | Vestidor circulación','CAM | Vestidor pasante']:
        cam=bpy.data.objects.get(name)
        if cam:cam['photographic_exposure_compensation_ev']=0
    # Broad, descriptive companion views; no source view is overwritten.
    specs=[
      ('Estudio amplitud',[20.55,4.85,5.63],[18.25,4.55,2.90],21,(4,3),0,150),
      ('Estudio retrato',[20.40,4.83,5.45],[18.35,4.62,3.04],22,(3,4),0,150),
      ('Dormitorio desde paso',[18.20,4.78,7.72],[15.48,4.30,7.27],24,(4,3),0,150),
      ('Dormitorio amplitud',[17.36,4.63,8.76],[15.77,4.30,7.17],19.5,(4,3),0,1),
      ('Dormitorio retrato',[17.10,4.67,8.67],[15.77,4.27,7.18],20,(3,4),0,1),
      ('Vestidor retrato',[18.52,4.75,8.43],[18.52,4.48,6.38],23,(3,4),0,1),
      ('Exterior jardin retrato',[7.10,5.5,24.00],[17.50,4.0,8.40],29,(3,4),0,1),
      ('Quincho amplitud',[13.13,1.69,11.22],[19.12,1.39,8.42],28,(4,3),0,150),
      ('Bano suite humano',[19.77,4.75,8.34],[21.02,4.10,6.95],20,(3,4),0,1),
    ]
    # Coordinate the two stable primary camera identities with the authored R7A bath relocation.
    bath_floor=bpy.data.objects.get('Piso baño mono')
    if bath_floor and -bath_floor.matrix_world.translation.y<2.0:
        specs.append(('Bano PB desde puerta',[18.82,1.65,.82],[20.50,1.15,.89],20,(4,3),0,150))
        report['relocated_primary_cameras']=[]
        for name,p,t,lens in [
            ('REV | Baño mono',[19.50,1.75,1.65],[20.77,1.05,.69],22),
            ('REV | Baño mono sanitarios',[20.62,1.80,.89],[19.82,1.10,1.41],22),
        ]:
            cam=bpy.data.objects.get(name)
            if cam:
                if 'camera99_pre_r7_matrix' not in cam:
                    cam['camera99_pre_r7_matrix']=[v for row in cam.matrix_world for v in row]
                    cam['camera99_pre_r7_lens']=cam.data.lens
                cam.location=(p[0],-p[2],p[1]);target=Vector((t[0],-t[2],t[1]))
                cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
                cam.data.lens=lens;cam.data.shift_x=0;cam.data.shift_y=0;cam.data.dof.use_dof=False
                cam['presentation_frame']=150;cam['camera99_layout_current']=True
                cam['camera99_note']='Primary camera coordinated with R7 bathroom at Cedro facade; identity retained.'
                if 'camera99_layout_obsolete' in cam:del cam['camera99_layout_obsolete']
                report['relocated_primary_cameras'].append({'name':name,'previous_matrix':list(cam['camera99_pre_r7_matrix']),'previous_lens_mm':cam['camera99_pre_r7_lens'],'source_position':p,'source_target':t,'lens_mm':lens})
    for name,p,t,lens,aspect,shift,frame in specs:
        cam=make_camera(name,p,t,lens,aspect,shift,frame)
        if name=='Dormitorio desde paso':cam['camera99_note']='Technical relationship view only; foreground door dominates. Not a photographic hero.'
        report['cameras'].append({'name':cam.name,'source_position':p,'source_target':t,'lens_mm':lens,'aspect':list(aspect),'frame':frame})
    S.cycles.max_bounces=12;S.cycles.diffuse_bounces=6;S.cycles.glossy_bounces=6;S.cycles.transmission_bounces=10;S.cycles.transparent_max_bounces=16
    S.cycles.use_denoising=True;S.cycles.denoiser='OPENIMAGEDENOISE';S.cycles.adaptive_threshold=.009;S.cycles.samples=384
    S['photographic99_light_pass']='Fixture-bound illumination; PBR manufactured finishes; original source cameras retained and companion views.'
    S['video_render_requires_explicit_approval']=True;S['review99_status']='Candidate in revision; independent 9.9 approval pending.'
    bpy.context.view_layer.update()
    report['light_count_final']=sum(o.type=='LIGHT' for o in S.objects)
    report['notes']=['No artificial camera fill lights. Existing source world and sun unchanged.','Sanitary positions and architectural envelopes unchanged.','Original CAM/REV cameras retained. Companion positions need integrated scene obstruction checks.','Neutral optical glazes, no deliberate damage or dirt. Electric lumens/photometry remain product-design proposals.','No still or video renders executed by this script.']
    json.dump(report,open(os.path.join(OUT,'r7_lighting_changes.json'),'w',encoding='utf8'),ensure_ascii=False,indent=2)
    print('PHOTO99_LIGHT_PASS',json.dumps({'optical_objects':optical_count,'light_count':report['light_count_final'],'new_cameras':len(report['cameras'])}),flush=True)
    return report

if __name__=='__main__':
    apply()
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    if '--save' in args:
        dest=args[args.index('--save')+1]
        assert os.path.abspath(dest)!=os.path.abspath(bpy.data.filepath),'Never overwrite the input candidate'
        assert os.path.basename(dest)!='Casa_de_Campo_95_R6K.blend','R6K is frozen'
        bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
        bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(dest),compress=True)
