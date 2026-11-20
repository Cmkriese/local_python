# Project Layout
This repository is a single-file web app. Keep project files in the following locations:

- `index.html` at the top level for GitHub Pages. All app HTML, CSS, and JavaScript belong in this file.
- `AGENTS.md`, `spec.md`, and `prompts.md` at the top level.
- `00_planning/` for notes and sketches.
- `01_data/` for data files.
- `02_validation/` for hand calculations and test cases.
- `03_output/` for screenshots and exported results.

Save every new file in the folder that best matches its purpose. Do not scatter project files into unrelated existing folders or create additional folders without a documented reason.

# Project Status

This project is a single-page Earthquake Shaker app. Detailed requirements and implementation decisions should be maintained in `spec.md`.

## Change log

- 2026-11-19: Set up the top-level project files and numbered folder layout.
- 2026-11-19: Added an abbreviated purpose statement covering tower construction, earthquake simulation, cost and strength scoring, and saved design comparison.
- 2026-11-19: Expanded the input specification with selectable joints, joint material and fastener properties, stiffness and failure strengths, and editable frequency, amplitude, direction, duration, and acceleration ground-motion inputs.
- 2026-11-19: Built Section 1 and Section 2 of `index.html`: a responsive 2D tower editor with preset pieces, grid placement, undo/redo, geometry controls, live piece counts, member properties, floor properties, and editable joint capacities.
- 2026-11-19: Built Section 3 of `index.html`: preset cost calculations, itemized member/floor/joint/foundation/labor totals, local saved tower versions, duplicate/load/delete actions, and saved-model cost comparison.
- 2026-11-19: Built Sections 4–6 of `index.html`: 1–10 second ground-motion inputs, lumped-mass structural response, natural-frequency and resonance estimates, sky-and-grass testing playback, member and joint damage reporting, 1–100 resilience scoring, and live upgrade actions.
- 2026-11-19: Improved the UI for tall towers and collapse: dynamic story scaling keeps all floors visible, columns-per-row is editable, snapped piece placement shows hover previews, stress colors members during playback, failed beams/floors fall visibly, and strong-motion tests return collapsed 1/100 reports.

## Working rules

- After each request, update `prompts.md` with what was asked, what changed, and whether it worked.
- After each meaningful requirement or folder change, add a short entry to the change log in `AGENTS.md` and keep the change log in chronological order.
- Save every new file in the folder that best matches its purpose.
- Keep `spec.md` as the detailed source of truth and `AGENTS.md` as the concise implementation and change-summary source.
- Do not build or modify the app implementation unless explicitly asked to implement it.