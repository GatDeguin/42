# Casa de Campo reconstruction plan

Goal: Deliver a faithful editable Blender property, fixed cameras, doors, animated tour, Cycles presentation and rendered video.
Source of truth: source/request.txt (user instructions) and the final functions in source/engine.js (architectural data).
Axis conversion: HTML (X,Y,Z) to Blender (X,-Z,Y), right handed, metres.

- [ ] Export final geometry, original PBR maps, doors, colliders and cameras.
- [ ] Build ordinary editable mesh geometry and organized named collections in a fresh background Blender scene.
- [ ] Rig doors and camera route; validate dimensions and circulation against actual meshes.
- [ ] Render and inspect exterior, interior and inspection views against the reference.
- [ ] Render real virtual tour and encode video; reopen and verify delivered blend.

Preserve explicit source coordinates. Ground reference 0; upper structural datum 3m, 0.2m slab, landing top 3.2m. No interior stairs. Source dimensions outrank illustrative reference. Document any genuine source inconsistencies and their corrections. Keep existing open Blender project untouched.
