from pathlib import Path
p=Path(r'D:\2026\42\scripts\correcciones95_apoyos_c.py');s=p.read_text(encoding='utf-8')
old="basecoat['construction_role']='P: 10mm bonded leveling mortar between existing concrete +3.20 and finish base +3.21'"
new=old+"""
# Continue the exact finish reservation down through the leveling layer.
c=box('Temporal reserva base guía lateral',[13.91,3.205,10.36],[.29,.05,2.66],col='REFERENCE',bev=0)
bpy.context.view_layer.update();cut(basecoat,c);bpy.data.objects.remove(c,do_unlink=True)
"""
assert old in s
s=s.replace(old,new).replace('Pass3c.blend','Pass3d.blend').replace('pass3c measured','pass3d measured').replace('bearing_details_3c.json','bearing_details_3d.json').replace('PASS3C_SAVED','PASS3D_SAVED')
Path(r'D:\2026\42\scripts\correcciones95_apoyos_d.py').write_text(s,encoding='utf-8')
