// Fit the entire authored Blender camera frame; extra viewport area extends the view.
export function fitAuthoredCamera(camera, preset) {
 if (!preset.frustum) {camera.clearViewOffset();return;}
 const {left,right,bottom,top}=preset.frustum;
 const sourceHalfW=(right-left)/2,sourceHalfH=(top-bottom)/2;
 const halfH=Math.max(sourceHalfH,sourceHalfW/camera.aspect),halfW=halfH*camera.aspect;
 camera.fov=2*Math.atan(halfH)*180/Math.PI;
 camera.setViewOffset(2*halfW,2*halfH,(left+right)/2,-(bottom+top)/2,2*halfW,2*halfH);
}
