# Prompts

## 2026-11-19

- **Asked:** Set up the `earthquake_shaker` folder using the same top-level and numbered-folder layout as the previous app folders.
- **Changed:** Added `index.html`, `spec.md`, `prompts.md`, project layout guidance in `AGENTS.md`, and README files for planning, data, validation, and output.
- **Worked:** Yes.

- **Asked:** Add an abbreviated purpose for the Earthquake Shaker app to the specification.
- **Changed:** Updated `spec.md` to describe building a tower with columns, beams, braces, and masses; shaking it with frequency- and amplitude-based ground motion; displaying movement, piece costs, total cost, and strength score; and saving and comparing designs.
- **Worked:** Yes.

- **Asked:** Add joint strengths and earthquake frequency/amplitude ground-motion inputs.
- **Changed:** Added joint types, moment/shear/axial capacities, stiffness, ductility, failure modes, connection costs, and failure visualization inputs. Expanded ground motion with frequency, amplitude, PGA, phase, duration, sweep, direction, and acceleration-time-history controls.
- **Worked:** Yes.

- **Asked:** Build Section 2 in `index.html`.
- **Changed:** Expanded the tower editor with editable member sections and materials, custom width/depth/strength fields, floor area/thickness/material/mass fields, joint type and moment/shear/axial/rotation-strength fields, and live piece-count cards.
- **Worked:** Browser-tested selection and live geometry rebuilding; member, floor, joint, and bay-controls rendered and updated correctly.

- **Asked:** Build Section 3 in `index.html`.
- **Changed:** Added preset pricing and live itemized cost totals, a Save Tower control, browser-local saved tower storage, load/duplicate/delete actions, and a two-tower cost comparison check.
- **Worked:** Browser-tested cost reporting, saving two towers, duplicating a tower, and comparing saved costs.

- **Asked:** Build Sections 4, 5, and 6 in `index.html`.
- **Changed:** Added ground-motion controls and an educational 2D lumped-mass response engine, short sky-and-grass testing playback, natural-frequency and resonance output, member and joint stress/damage tables, 1–100 resilience scoring, and brace/member upgrade actions.
- **Worked:** Browser-tested a 1-second 4x simulation, report generation, resonance and movement output, member/joint tables, and immediate brace-upgrade recalculation.

- **Asked:** Fix tall-tower visibility, piece placement, column count, stress colors, collapse, and upgrade usability.
- **Changed:** Added dynamic floor spacing for 10-story visibility, an editable columns-per-row control, snap hover previews for placed beams/braces/columns, live red/yellow/green member stress, collapsed-floor/member visual fall behavior, and failed-tower reporting.
- **Worked:** Browser-tested F10 visibility and a 2 g high-motion run that produced collapse at 18.4% drift with failed member and joint states.
