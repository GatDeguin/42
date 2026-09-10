"""Fine real-scale mineral finishes and neutral detailed kitchen appliances."""
import bpy,os,math,json,ast,numpy as np
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
M={m['source_material_key']:m for m in bpy.data.materials if 'source_material_key' in m};COL={c.name:c for c in bpy.data.collections}
for m in bpy.data.materials:
 if m.name.startswith('MAT95 | '):M[m.name.split(' | ',1)[1]]=m
def cv(p):return Vector((p[0],-p[2],p[1]))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_textiles.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['bounds','deform','map_h','mineral']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<helper>','exec'))
for nd in ast.parse(open(os.path.join(ROOT,'scripts','correcciones95_materialidad.py'),encoding='utf8').read()).body:
 if isinstance(nd,ast.FunctionDef) and nd.name in ['box','cyl','mesh','curve']:exec(compile(ast.Module(body=[nd],type_ignores=[]),'<fast>','exec'))
mineral('concreteDark',(.20,.195,.18),.75,.00024,380)
mineral('concrete',(.47,.46,.425),.62,.00016,520)
def mat(key,color,rough,metal=0):
 m=bpy.data.materials.new('FIT95 | '+key);m.use_nodes=True;bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal;M[key]=m;return m,bs
m,bs=mat('vidrio vitrocerámico',(.009,.012,.013),.105);bs.inputs['Coat Weight'].default_value=.35
mat('serigrafía tenue',(.24,.25,.24),.40)
mat('epdm juntas',(.008,.010,.011),.82)
m,bs=mat('vidrio ahumado horno',(.011,.014,.017),.16);bs.inputs['Coat Weight'].default_value=.28
m,bs=mat('acero cepillado electrodomésticos',(.50,.51,.515),.31,1);bs.inputs['Anisotropic'].default_value=.34
# Quiet submillimetric steel texture rather than wavy normal distortion.
n=m.node_tree.nodes;l=m.node_tree.links;tc=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(1,1,420);l.new(tc.outputs['Generated'],mapping.inputs[0]);noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=8;l.new(mapping.outputs[0],noise.inputs[0]);bum=n.new('ShaderNodeBump');bum.inputs['Distance'].default_value=.000007;bum.inputs['Strength'].default_value=.12;l.new(noise.outputs['Fac'],bum.inputs['Height']);l.new(bum.outputs[0],bs.inputs['Normal'])
def assign(o,key):
 o.data=o.data.copy();o.data.materials.clear();o.data.materials.append(M[key])
def remove(prefix):
 for o in list(S.objects):
  if o.name.startswith(prefix):bpy.data.objects.remove(o,do_unlink=True)
# Induction hob: black glass with printed rings and touch-control marks, not solid metal discs.
assign(bpy.data.objects['Anafe cocina'],'vidrio vitrocerámico');remove('Inductor cocina ')
for x in [21.27,21.53]:
 for z in [10.20,10.43]:
  pts=[[x+.087*math.cos(k*math.tau/96),4.17525,z+.087*math.sin(k*math.tau/96)] for k in range(97)]
  curve('FIT95 | aro serigrafiado inducción',pts,.00050,'serigrafía tenue','INTERIORS')
for z in [10.15,10.25,10.35,10.45]:
 box('FIT95 | control táctil inducción',[21.15,4.1753,z],[.012,.0003,.0012],'serigrafía tenue','INTERIORS',0)
box('FIT95 | control encendido inducción',[21.15,4.1753,10.52],[.012,.0003,.010],'serigrafía tenue','INTERIORS',.002)
# Oven: inset glass, perimeter seal, control fascia, readable handle mounts and ventilation gaps.
assign(bpy.data.objects['Horno cocina vidrio'],'vidrio ahumado horno')
assign(bpy.data.objects['Horno cocina tirador'],'acero cepillado electrodomésticos')
for z in [10.068,10.572]:box('FIT95 | junta horno vertical',[21.072,3.70,z],[.002,.488,.004],'epdm juntas','INTERIORS',.0005)
for h in [3.452,3.946]:box('FIT95 | junta horno horizontal',[21.072,h,10.32],[.002,.004,.508],'epdm juntas','INTERIORS',.0005)
box('FIT95 | panel mandos horno',[21.068,3.860,10.32],[.008,.048,.486],'acero cepillado electrodomésticos','INTERIORS',.001)
for z in [10.17,10.47]:
 cyl('FIT95 | mando horno',[21.062,3.862,z],[21.049,3.862,z],.014,'blackMetal','INTERIORS')
 box('FIT95 | indicador mando',[21.0485,3.870,z],[.0008,.007,.0012],'serigrafía tenue','INTERIORS',0)
box('FIT95 | pantalla horno apagada',[21.0625,3.862,10.32],[.001,.024,.09],'vidrio ahumado horno','INTERIORS',.001)
for z in [10.15,10.49]:
 cyl('FIT95 | apoyo tirador horno',[21.074,3.90,z],[21.045,3.90,z],.0055,'acero cepillado electrodomésticos','INTERIORS')
for h in [3.478,3.486,3.494]:
 box('FIT95 | ranura ventilación horno',[21.071, h,10.32],[.002,.0016,.42],'epdm juntas','INTERIORS',.0003)
# Refrigerator retains the original footprint and usable clearances.
for name in ['Heladera','Heladera puerta superior']:assign(bpy.data.objects[name],'acero cepillado electrodomésticos')
box('Heladera puerta congelador',[21.099,3.600,11.24],[.024,.55,.67],'acero cepillado electrodomésticos','INTERIORS',.003)
for h in [3.321,3.881,5.373]:
 box('FIT95 | junta heladera horizontal',[21.1125,h,11.24],[.005,.006,.67],'epdm juntas','INTERIORS',.0005)
for z in [10.902,11.578]:
 box('FIT95 | junta heladera vertical',[21.1125,4.348,z],[.005,2.05,.006],'epdm juntas','INTERIORS',.0005)
# Upper handle held off the face on two real spacers; freezer grip is recessed at its top.
for h in [4.225,4.675]:
 cyl('FIT95 | separador tirador heladera',[21.090,h,10.98],[21.066,h,10.98],.005,'blackMetal','INTERIORS')
box('FIT95 | uñero congelador',[21.085,3.850,11.24],[.004,.015,.41],'epdm juntas','INTERIORS',.003)
for h in [3.278,3.289,3.300]:
 box('FIT95 | ventilación zócalo heladera',[21.114,h,11.24],[.003,.0025,.52],'epdm juntas','INTERIORS',.0004)
# Lower fridge in mono must start on its actual finished floor, not below the slab.
o=bpy.data.objects['Heladera mono'];map_h(o,.210,2.280)
# Exposure belongs to each architectural photograph; room lighting is still physically located.
for name in ['REV | Dormitorio completo','REV | Dormitorio acceso']:
 bpy.data.objects[name]['photographic_exposure_compensation_ev']=.35
# Imported rounded-box custom normals distorted otherwise planar appliance fronts.
# Reconstruct their exact external bounding boxes with flat faces and manufactured edge radii.
for nm,key,bevel in [('Heladera puerta superior','acero cepillado electrodomésticos',.0025),('Heladera','acero cepillado electrodomésticos',.003),('Horno cocina vidrio','vidrio ahumado horno',.001),('Anafe cocina','vidrio vitrocerámico',.0015)]:
 old=bpy.data.objects[nm];a,b=bounds(old);mid=(a+b)/2;col=old.users_collection[0].name
 obj=box(nm+' temporal',[mid[0],mid[2],-mid[1]],[b[0]-a[0],b[2]-a[2],b[1]-a[1]],key,col,bevel)
 bpy.data.objects.remove(old,do_unlink=True);obj.name=nm;obj['planar_normal_repair']='Exact bounds retained; planar faces replace distorted imported custom normals.'
S['review_iteration']='95 / R5D material scale and manufactured appliances'
S['r5d_finish_notes']='Concrete/dark concrete microfinish0.16/0.24mm,2% broad albedo range; unbranded conceptual appliances with detailed joints, controls and supports. Model dimensions remain source-derived.'
S.frame_set(1);bpy.context.view_layer.update();bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
import sys
name='Casa_de_Campo_95_R5D_preview.blend' if '--preview' in sys.argv else 'Casa_de_Campo_95_R5D.blend'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'output',name),compress=True);print('R5D_SAVED',flush=True)
