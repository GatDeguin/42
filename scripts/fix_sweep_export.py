from pathlib import Path
p=Path(r'D:\2026\42\scripts\extract_door_sweeps.py');s=p.read_text(encoding='utf8')
s=s.replace("data['door_primary'].items()","data['tested_moving_meshes'].items()")
s=s.replace("o=bpy.data.objects[objects[0]];rig=", "parts=[bpy.data.objects[n] for n in objects];o=parts[0];rig=")
s=s.replace("pts=[o.matrix_world@Vector(v) for v in o.bound_box]","pts=[ob.matrix_world@Vector(v) for ob in parts for v in ob.bound_box]")
p.write_text(s,encoding='utf8')
