import bpy,json
s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update()
for name in ['Puerta acceso estudio','Puerta doble mono izquierda vidrio','Corrediza posterior A vidrio','Corrediza posterior A Vidrio interior','Corrediza lateral A vidrio']:
 o=bpy.data.objects.get(name)
 print(name,'LOCATION',list(o.location),'WORLD',list(o.matrix_world.translation),'SCALE',list(o.scale),'PARENT',o.parent.name if o.parent else None,'PARENTWORLD',list(o.parent.matrix_world.translation) if o.parent else None)
