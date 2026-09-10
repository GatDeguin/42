from pathlib import Path
p=Path(r'D:\2026\42\scripts\correcciones95_dimensiones_r6.py');s=p.read_text(encoding='utf8')
tag="S['r6h_dimensional_corrections']=json.dumps(report,ensure_ascii=False);"
insert="""# Remove low duplicate shower head; preserve the assembled replacement fixture.
remove('Ducha baño vivienda')
bpy.data.objects['Bañera vivienda']['fixture_classification']='Bañera compacta/asiento 1.25x0.74m; producto a seleccionar. No inmersión adulta extendida.'
# Physical freeboard: wave crest100mm below basin wall cap+0.070, not above it.
water=bpy.data.objects['Agua de pileta'];wa,wb=bounds(water);map_h(water,float(wa[2]),-.030)
water['design_water_crest_y']=-.030;water['freeboard_to_basin_cap_m']=.100
report['pool']={'basin_cap':.070,'water_crest':-.030,'freeboard_m':.100,'status':'P cota operativa de agua; filtración/skimmer/equipos requieren proyecto hidráulico.'}
report['bath_compact']='1.25x0.74m compact/asiento, producto a seleccionar'
"""
s=s.replace(tag,insert+tag);p.write_text(s,encoding='utf8')
