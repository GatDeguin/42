from pathlib import Path
p=Path(r'D:\2026\42\scripts\correcciones95_apoyos.py')
s=p.read_text(encoding='utf-8')
def replace(a,b):
 global s
 if a not in s: raise RuntimeError('Missing patch: '+a[:70])
 s=s.replace(a,b)
replace("# Cradle joints bear through explicit4mm pads, with return legs tied into the façade.", "# Cradle pads follow the actual 0.5% gutter underside at every support vertex.")
replace("  box('FIX95 | calzo soporte canaleta 4mm',[x,h+.002,z],[.024,.004,.16],'blackMetal',bev=0)\n  front='frontal' in o.name;zz=.004 if front else 11.996;top=6.982 if front else 6.382", """  front='frontal' in o.name
  gutter=bpy.data.objects['PL95 | canaleta '+('frontal' if front else 'posterior')+' abierta']
  outlet,low,_=json.loads(gutter['outlet_source']);fall=float(gutter['fall_percent'])/100
  thickness=low+abs(x-outlet)*fall-h
  assert thickness>0
  pad=box('FIX95 | calzo soporte canaleta ajustado',[x,h+thickness/2,z],[.024,thickness,.16],'blackMetal',bev=0)
  inv=pad.matrix_world.inverted()
  for v in pad.data.vertices:
   w=pad.matrix_world@v.co
   if w.z>h+thickness/2:w.z=low+abs(w.x-outlet)*fall
   v.co=inv@w
  pad['bearing_bottom']=float(h);pad['centre_thickness']=float(thickness)
  zz=.004 if front else 11.996;top=6.982 if front else 6.382""")
replace("floors=[geom(o) for o in S.objects if o.name.startswith('AC95 | acabado ') and o.type=='MESH']", """# Measure structural support from the actual meshes, including the +3.20/+3.21 joint.
slabs=[bpy.data.objects[n] for n in ['Descanso escalera','Balcón lateral','Balcón posterior']]
slab_trees=[(o.name,geom(o)) for o in slabs]
def support(x,z):
 hits=[]
 for name,tree in slab_trees:
  p=tree.ray_cast(cv([x,3.23,z]),Vector((0,0,-1)),.25)[0]
  if p is not None:hits.append((float(p.z),name))
 assert hits, ('No concrete under anchor',x,z)
 return max(hits)
basecoat=box('AC95 | capa base adherida balcón lateral 10mm',[13.5,3.205,9.0],[1.0,.010,6.0],'concrete','UPPER_FLOOR',bev=0)
basecoat['construction_role']='P: 10mm bonded leveling mortar between existing concrete +3.20 and finish base +3.21'
floors=[geom(o) for o in S.objects if o.name.startswith('AC95 | acabado ') and o.type=='MESH']""")
replace(" side=o.name.startswith('Baranda lateral');substrate=3.20 if side and z<6 else 3.21"," side=o.name.startswith('Baranda lateral')")
replace("v.name.startswith('AC95 | acabado ') and v.type=='MESH'","v.name.startswith(('AC95 | acabado ','AC95 | capa base adherida ')) and v.type=='MESH'")
replace(" grout('FIX95 | grout hasta sustrato '+o.name,x0+.002,x1-.002,max(z0+.002,5.001),z1-.002,3.254,substrate)", """ # Start inside concrete and subtract the three actual slabs: this also creates
 # the 10mm bottom step at rear joint instead of leaving floating grout.
 g=grout('FIX95 | grout hasta sustrato '+o.name,x0+.002,x1-.002,max(z0+.002,5.001),z1-.002,3.254,3.195)
 bpy.context.view_layer.update()
 for slab in slabs:
  ga,gb=bounds(g);sa,sb=bounds(slab)
  if np.all(np.minimum(gb,sb)-np.maximum(ga,sa)>.00001):cut(g,slab)""")
replace(" substrate=3.20 if side and z<6 else 3.21\n for xx in xs:"," anchors=[]\n for xx in xs:")
replace("  for zz in zs:\n   cyl('FIX95 | vástago", "  for zz in zs:\n   substrate,support_name=support(xx,zz)\n   anchors.append({'x':float(xx),'z':float(zz),'substrate_top':substrate,'concrete_object':support_name,'anchor_bottom':substrate-.10,'embedment_m':.10})\n   cyl('FIX95 | vástago")
replace("'substrate_top':substrate,'anchor_bottom':substrate-.10,'status':","'individual_anchors':anchors,'substrate_top_min':min(v['substrate_top'] for v in anchors),'substrate_top_max':max(v['substrate_top'] for v in anchors),'status':")
replace("95 / pass3b independent bearing corrections","95 / pass3c measured concrete bearings")
replace("'4mm gutter cradle pads and façade return fixings'","'Gutter pads conform to actual underside at each end' ")
replace("'Balcony plates anchor inside concrete and bear through fitted grout'","'68 anchors have 100mm proposed embedment measured from actual concrete; grout conforms across stepped joint; 10mm leveling base closes lateral finish gap'")
replace("'bearing_details.json'","'bearing_details_3c.json'")
replace("Casa_de_Campo_95_Pass3b.blend","Casa_de_Campo_95_Pass3c.blend")
replace("PASS3B_SAVED_NO_VIDEO","PASS3C_SAVED_NO_VIDEO")
Path(r'D:\2026\42\scripts\correcciones95_apoyos_c.py').write_text(s,encoding='utf-8')
