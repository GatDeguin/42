import bpy,bmesh,json,ast
from pathlib import Path
from mathutils import Vector
S=bpy.context.scene;S.frame_set(1);bpy.context.view_layer.update()
for node in ast.parse(Path('scripts/planos95_juntas_check.py').read_text(encoding='utf-8-sig')).body:
 if isinstance(node,ast.FunctionDef):exec(compile(ast.Module(body=[node],type_ignores=[]),'<check>','exec'))
pairs=[('Ventana DVH estudio marco inferior','Estudio antepecho ventana'),('Ventana DVH estudio Vidrio interior','Estudio antepecho ventana'),('Ventana DVH estudio marco inferior','Vierteaguas DVH estudio'),('Puerta ventana dormitorio marco inferior','Dormitorio antepecho lateral'),('Puerta ventana dormitorio Vidrio interior','Dormitorio antepecho lateral'),('Puerta ventana dormitorio marco fondo','Paño lateral medio vivienda'),('Ventana DVH estudio marco frente','Estudio lateral frente'),('Ventana DVH estudio marco fondo','Estudio paño entre ventana y puerta')]
r=[]
for an,bn in pairs:
 a,b=bpy.data.objects[an],bpy.data.objects[bn];v=vol(a,b) if overlap(bounds(a),bounds(b)) else 0;r.append({'a':an,'b':bn,'volume_m3':v});print(r[-1],flush=True)
Path('review95/dvh_adjacent_r6j.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
