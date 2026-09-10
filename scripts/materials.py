import bpy, math, os
def create_materials(data,root,anchor):
 mats={}
 for key,d in data['materials'].items():
  m=bpy.data.materials.new(d['name']+' | '+key);m.use_nodes=True
  n=m.node_tree.nodes;l=m.node_tree.links;n.clear()
  out=n.new('ShaderNodeOutputMaterial');out.location=(950,80)
  bs=n.new('ShaderNodeBsdfPrincipled');bs.location=(630,80);l.new(bs.outputs['BSDF'],out.inputs['Surface'])
  col=d.get('color',[1,1,1]);bs.inputs['Base Color'].default_value=(*col,1)
  bs.inputs['Roughness'].default_value=d.get('roughness',.5);bs.inputs['Metallic'].default_value=d.get('metalness',0)
  bs.inputs['Coat Weight'].default_value=d.get('clearcoat',0);bs.inputs['Coat Roughness'].default_value=.28
  bs.inputs['Sheen Weight'].default_value=d.get('sheen',0)
  bs.inputs['Anisotropic'].default_value=d.get('anisotropy',0)
  bs.inputs['IOR'].default_value=d.get('ior',1.5)
  m.diffuse_color=(*col,1);m['source_material_key']=key;m['source_descriptor']=str(d)
  if key in ('glass','glassInner'):
   bs.inputs['Base Color'].default_value=(.96,.985,.98,1);bs.inputs['Transmission Weight'].default_value=1
   bs.inputs['Roughness'].default_value=.022;bs.inputs['IOR'].default_value=1.52;bs.inputs['Metallic'].default_value=0
  elif key=='water':
   bs.inputs['Base Color'].default_value=(.92,.985,.985,1);bs.inputs['Transmission Weight'].default_value=1;bs.inputs['IOR'].default_value=1.333;bs.inputs['Roughness'].default_value=.035
   tc=n.new('ShaderNodeTexCoord');tc.object=anchor;noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=7.5;noise.inputs['Detail'].default_value=2;noise.inputs['Roughness'].default_value=.6
   l.new(tc.outputs['Object'],noise.inputs['Vector']);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.23;bump.inputs['Distance'].default_value=.036;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],bs.inputs['Normal'])
   vol=n.new('ShaderNodeVolumeAbsorption');vol.inputs['Color'].default_value=(.24,.74,.79,1);vol.inputs['Density'].default_value=.10;l.new(vol.outputs[0],out.inputs['Volume'])
  elif key=='mirror':
   bs.inputs['Base Color'].default_value=(.91,.94,.95,1);bs.inputs['Metallic'].default_value=1;bs.inputs['Roughness'].default_value=.025;bs.inputs['Transmission Weight'].default_value=0
  elif key=='warmLight':
   bs.inputs['Base Color'].default_value=(1,.62,.27,1);bs.inputs['Emission Color'].default_value=(1,.62,.27,1);bs.inputs['Emission Strength'].default_value=3.5
  elif key in ('screen','studioDisplay'):
   bs.inputs['Base Color'].default_value=(.006,.015,.023,1);bs.inputs['Roughness'].default_value=.2;bs.inputs['Metallic'].default_value=.08
   bs.inputs['Emission Color'].default_value=(.015,.04,.065,1);bs.inputs['Emission Strength'].default_value=.25
  elif key not in ('skyHdri','contactShadow'):
   tex=d.get('texture','white');p=data['profiles'].get(tex,data['profiles']['white'])
   tc=n.new('ShaderNodeTexCoord');tc.location=(-900,100);tc.object=anchor
   vec=n.new('ShaderNodeVectorMath');vec.operation='MULTIPLY';vec.location=(-720,100)
   tx,ty=p['tile'];vec.inputs[1].default_value=(1/tx,1/tx,1/ty)
   l.new(tc.outputs['Object'],vec.inputs[0])
   def image(kind):
    fp=os.path.join(root,'source','textures',tex+'_'+kind+'.png')
    if not os.path.exists(fp):return None
    im=n.new('ShaderNodeTexImage');im.image=bpy.data.images.load(fp,check_existing=True)
    im.image.colorspace_settings.name='sRGB' if kind=='albedo' else 'Non-Color'
    im.projection='BOX';im.projection_blend=.12;im.interpolation='Linear';im.location=(-480,100 if kind=='albedo' else -180)
    l.new(vec.outputs[0],im.inputs['Vector']);return im
   albedo=image('albedo');surface=image('surface')
   if albedo:
    mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*col,1);mix.location=(0,180);l.new(albedo.outputs['Color'],mix.inputs[1]);l.new(mix.outputs[0],bs.inputs['Base Color'])
    if key in ('leaf','blade'):
     attr=n.new('ShaderNodeVertexColor');attr.layer_name='leaf_tint';attr.location=(-120,420)
     tint=n.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=.6;l.new(mix.outputs[0],tint.inputs[1]);l.new(attr.outputs['Color'],tint.inputs[2]);l.new(tint.outputs[0],bs.inputs['Base Color'])
     bs.inputs['Subsurface Weight'].default_value=.06
     trans=n.new('ShaderNodeBsdfTranslucent');l.new(tint.outputs[0],trans.inputs[0])
     leafmix=n.new('ShaderNodeMixShader');leafmix.inputs[0].default_value=.14;l.new(bs.outputs[0],leafmix.inputs[1]);l.new(trans.outputs[0],leafmix.inputs[2]);l.new(leafmix.outputs[0],out.inputs['Surface'])
   if surface:
    sep=n.new('ShaderNodeSeparateColor');sep.location=(-180,-180);l.new(surface.outputs['Color'],sep.inputs['Color'])
    l.new(sep.outputs['Green'],bs.inputs['Roughness'])
    bump=n.new('ShaderNodeBump');bump.location=(340,-100);bump.inputs['Strength'].default_value=.6;bump.inputs['Distance'].default_value=p['h']*255/80
    l.new(sep.outputs['Blue'],bump.inputs['Height']);l.new(bump.outputs['Normal'],bs.inputs['Normal'])
  mats[key]=m
 # Restrained emissive instrument displays; all actual geometry remains editable.
 for key,color,energy in [('meterCyan',(.08,.52,.62),1.2),('meterAmber',(.9,.28,.035),1.3),('meterGreen',(.2,.65,.12),1.1),('embers',(.75,.09,.008),3)]:
  m=bpy.data.materials.new(key);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Emission Color'].default_value=(*color,1);bs.inputs['Emission Strength'].default_value=energy;mats[key]=m
 return mats
