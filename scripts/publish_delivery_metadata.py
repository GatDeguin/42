from pathlib import Path
import json,re,hashlib
root=Path(r'D:\2026\42')
p=root/'README.md';s=p.read_text(encoding='utf8').replace('**Estado:** tercera auditoría independiente en cierre; las revisiones anteriores obtuvieron 6/10 y 7/10.','**Estado:** tercera auditoría independiente aprobada con **8,0/10**, tras las evaluaciones de 6/10 y 7/10. [Dictamen final](audit/critica_iteracion_03.md).')
s=s.replace('Los nombres Revision y los archivos de las primeras iteraciones locales son versiones anteriores; la entrega vigente es Final.','La escena vigente es Casa_de_Campo_Final.blend; el render vigente conserva el nombre Casa_de_Campo_Atardecer_Revision.png. Los archivos de las primeras iteraciones se mantienen como registro.')
p.write_text(s,encoding='utf8')
p=root/'output/validation.json';v=json.loads(p.read_text(encoding='utf8'));v['review_state']='Independent architecture review03:8.0/10; frozen final model inspected from disk. Video remains paused.';v['independent_review']={'score':8.0,'report':'audit/critica_iteracion_03.md','model':'output/Casa_de_Campo_Final.blend','model_sha256':'58223d78f71dc0c1d4f33034aaaf0be96a1bd420f72f2231468003e942c2bbfe'};p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
for fn in ['audit/respuesta_constructor_02.md','docs/DECISIONES.md']:
 p=root/fn;s=p.read_text(encoding='utf8');s=re.sub(r'(?<=\d)(?=[A-Za-zÁÉÍÓÚÑáéíóúñ])',' ',s);s=re.sub(r'(?<=[a-záéíóúñ])(?=\d)',' ',s);p.write_text(s,encoding='utf8')
p=root/'.gitignore';s=p.read_text(encoding='utf8')+'\n!audit/final_reopen_checks_03.log\n';p.write_text(s,encoding='utf8')
files=['output/Casa_de_Campo_Final.blend','output/Casa_de_Campo_Atardecer_Revision.png','output/tour_route.json','output/validation.json','review/saved_route_final.json','audit/critica_iteracion_03.md']
manifest={'version':'architectural-review-03','critic_score':8.0,'video':'paused-pending-explicit-approval','files':[]}
for fn in files:
 p=root/fn;manifest['files'].append({'path':fn,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(root/'output/delivery_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print('DELIVERY_METADATA_UPDATED')
