# R8 mobile loading repair

Reported device: iPhone 15 Pro Max. Symptom: loading restarts before the model opens. A physical device crash log was not available, so a process-memory termination is a strongly supported explanation, not a directly observed OS diagnosis.

The previous mobile check only emulated a screen and touch on a desktop computer. It did not establish that the full asset fit a phone memory budget.

Baseline: 208,958,850 bytes downloaded for the model, 204,282,656 bytes of decoded compressed geometry, approximately 926,056,448 bytes of RGBA textures with mipmaps, and 44,061,880 triangles across scene instances. Landscape accounts for 42,510,648 triangles. The original preparation also expanded indexed geometry into non-indexed floats and retained copies for picking.

Fix: choose a separate mobile package before loading on phones, tablets (including landscape/iPad desktop UA), coarse-pointer devices and devices reporting at most 4 GB memory. Mobile download including its small HDR and finish maps is 17,005,021 bytes. Model geometry expands to 22,308,856 bytes; source scene has 2,104,998 triangles; model texture estimate is 83,615,744 bytes. Indexed batching is preserved. The mobile raster pipeline has four nearby local lights, a 512 px HDR and 1024 px sun shadow. It avoids path-tracing BVH, full-size photographic replacement maps, screen-space postprocessing and physical transmission buffers. Glass/water use inexpensive transparency; the full photographic images and desktop model remain available.

All 5,618 scene nodes, transforms, metadata and hierarchy are preserved. Decoded vertex attributes and oriented triangle sets outside vegetation match the original exactly, including furniture, terrain, door mechanisms and all 13 door rigs. Only vegetation geometry and image resolution use lower-detail derivatives.

The budget test failed on the original asset and passed on the mobile asset. Browser checks passed for iPhone 15 Pro Max and iPad landscape profiles in desktop Chrome with a 256 MiB V8 old-space limit. This is not an emulation of total iPhone RAM or Safari. They verify actual light-resource selection, controls, doors, cuts, no WebGL context losses and runtime geometry/texture budgets. Actual phone confirmation remains necessary. A separate existing desktop/mobile load regression also passed.

Reproduce from the repository root with node web-tools/r8-mobile-build.mjs, node web-tools/r8-mobile-budget.mjs, node web-tools/r8-mobile-geometry.mjs and node web-tools/r8-mobile-browser.mjs (serve docs on localhost:8420). No Blender model, plans, stills or videos were altered.
