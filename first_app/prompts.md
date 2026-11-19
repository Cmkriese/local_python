# Prompts

## 2026-11-19

- **Asked:** Set up the top-level and numbered folder layout in the `first_app` folder.
- **Changed:** Added `index.html`, `spec.md`, `prompts.md`, project layout guidance in `AGENTS.md`, and README files for the planning, data, validation, and output folders.
- **Worked:** Yes.

- **Asked:** Make `AGENTS.md` describe the project changes and require it to remain updated.
- **Changed:** Added a project status summary, concise change log, and working rules for future updates to `AGENTS.md` and `prompts.md`.
- **Worked:** Yes.

- **Asked:** Build Stage 1 of the app as a static mockup in `index.html`.
- **Changed:** Replaced the empty page with a responsive Beam Designer layout showing all inputs, beam and load placeholders, shear, moment, deflection, check cards, and section recommendation. Added only mockup UI interactions and synchronized span controls.
- **Worked:** Yes.

- **Asked:** Build Stage 2 of the app with working inputs and validation.
- **Changed:** Added synchronized span controls, support and deflection selections, material-dependent section lists, point and uniform load editing, range and consistency validation, and invalid-state hiding for calculated outputs. Kept beam calculations and drawing updates out of this stage.
- **Worked:** Yes.

- **Asked:** Build Stages 3 through 6 in the index folder.
- **Changed:** Replaced output placeholders with live SVG beam and diagram rendering, equilibrium reactions, load superposition, shear and moment sampling, inch-based deflection integration, bending and deflection checks, section recommendations, draggable point loads, linked pointer readouts, extrema labels, adaptive scales, and live responsive updates.
- **Worked:** JavaScript syntax tooling was unavailable in the environment; the implementation was checked with diff validation and targeted source inspection.

- **Asked:** Add the beam-deformation and stress-gradient requirements to the bottom of the specification.
- **Changed:** Added requirements for a visibly deflected beam with exaggerated display scaling, downward-positive deflection, and a continuous green-to-red local bending-stress color gradient keyed to maximum absolute moment. Updated the project change log.
- **Worked:** Yes.

- **Asked:** Implement the new beam-deformation and stress-gradient specification in the index.
- **Changed:** Replaced the straight beam stroke with sampled, downward-positive deflection geometry and a continuous green-to-yellow-to-red local bending-stress gradient. Added an in-drawing stress legend and retained the horizontal beam scale and supports.
- **Worked:** Browser validation remains to be rechecked after reload.

- **Asked:** Publish the repository as a GitHub Pages site with a public URL.
- **Changed:** Added a root `index.html` redirect to `first_app/` and prepared the master branch for GitHub Pages publication.
- **Worked:** Pending GitHub Pages configuration and deployment.
