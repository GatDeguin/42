"""R8 subtle capillary water optics; basin geometry and absorption unchanged."""
import bpy,json,math

def apply():
 S=bpy.context.scene;m=bpy.data.materials['Agua | water'];b=next(n for n in m.node_tree.nodes if n.type=='BUMP');noise=b.inputs['Height'].links[0].from_node
 assert noise.type=='TEX_NOISE' and abs(noise.inputs['Scale'].default_value-7.5)<1e-6
 assert abs(b.inputs['Strength'].default_value-.23)<1e-6
 before=b.inputs['Distance'].default_value
 assert any(abs(before-q)<1e-6 for q in [.036,.008]),before
 b.inputs['Distance'].default_value=.008
 r={'material':m.name,'scope':'Optical bump only; no vertex, volume, surface level, basin, colour, absorption or IOR changes.','bumpDistanceBefore_m':.036,'bumpDistanceAfter_m':.008,'strength':float(b.inputs['Strength'].default_value),'effectiveHeightScale_m':.008*.23,'noiseObjectScale':7.5,'reason':'The earlier optical bump distance represented8.28mm effective modulation and looked choppy in the human-height pool view. Reduce the optical height multiplier to1.84mm for subtle wind ripple; no hydraulic simulation or wave-amplitude certification.'}
 S['r8_water_optics']=json.dumps(r);return r
