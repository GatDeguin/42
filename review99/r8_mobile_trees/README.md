# R8 mobile: restore visible trees

The owner confirmed that loading completes on iPhone 15 Pro Max, then reported nearly invisible trees. The first mobile reducer sampled disconnected components indiscriminately. It removed most branches and leaves, leaving only 3.4–3.9% of the source tree silhouette visible.

Trees now have a separate LOD policy: trunk and branches are simplified without sampling away branch components; leaf cards are sampled at 2.5% and expanded about their own centers to preserve canopy coverage at mobile screen sizes. This is a mobile representation of the source tree, with coarser leaves. The full desktop geometry is unchanged.

A rendered silhouette regression failed on the old package, then passed with source coverage of 75.6% front, 78.7% side and 78.7% top. IoU is 62.4%, 65.9% and 68.6%, respectively. Reference and candidate images use the same camera and alpha-tested source materials.

Mobile package including small HDR/finish maps: 17,477,303 bytes. Geometry: 2,937,858 scene triangles and 23,156,728 decoded buffer bytes. Texture estimate remains 83,615,744 bytes. The existing 30 MiB download, 3 million triangle, 85 MiB texture and 64 MiB decoded geometry budgets pass. Nonvegetation geometry, all scene transforms, hierarchy and 13 doors remain unchanged.

The model URL now includes its mobile revision, so an unchanged Blender SHA cannot reuse an earlier mobile geometry cache. Architectural renders, plans, Blender and video status are unaffected.

Checks: node web-tools/r8-mobile-tree-fixtures.mjs, node web-tools/r8-mobile-tree-coverage.mjs, node web-tools/r8-mobile-budget.mjs, node web-tools/r8-mobile-geometry.mjs, node web-tools/r8-mobile-browser.mjs. Local docs server is required on port8420. Fixtures in docs/preview99/assets/mobile-test are temporary and are not published. Browser tests use Chrome desktop emulation, not a physical iPhone or Safari.
