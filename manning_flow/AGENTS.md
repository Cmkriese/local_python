# Project Layout
This repository is a single-file web app. Keep project files in the following locations:

- `index.html` at the top level for GitHub Pages. All app HTML, CSS, and JavaScript belong in this file.
- `AGENTS.md`, `spec.md`, and `prompts.md` at the top level.
- `00_planning/` for notes and sketches.
- `01_data/` for data files.
- `02_validation/` for hand calculations and test cases.
- `03_output/` for screenshots and exported results.
- `manning.py` may remain as the calculation or reference script.

Save every new file in the folder that best matches its purpose. Do not scatter project files into unrelated existing folders or create additional folders without a documented reason.

# Project Status

This project is a Manning flow web app. Detailed requirements and implementation decisions should be maintained in `spec.md`.

## Change log

- 2026-11-20: Set up the top-level project files and numbered folder layout.
- 2026-11-20: Added `manning_flow(n, A, R, S)` to `manning.py` for Manning open-channel flow calculations in cubic feet per second.
- 2026-11-20: Validated `manning_flow(n, A, R, S)` with four representative roughness, area, hydraulic-radius, and slope combinations; all cases matched exactly.
- 2026-11-20: Added the unit-input validation case of `n=1`, `A=1 ft²`, `R=1 ft`, and `S=1 ft/ft`, producing `1.490000 cfs`.
- 2026-11-20: Added the `n=2`, `A=1 ft²`, `R=1 ft`, and `S=1 ft/ft` validation case, producing `0.745000 cfs`.

## Working rules

- After each request, update `prompts.md` with what was asked, what changed, and whether it worked.
- After each meaningful requirement or folder change, add a short entry to the change log in `AGENTS.md` and keep the change log in chronological order.
- Save every new file in the folder that best matches its purpose.
- Keep `spec.md` as the detailed source of truth and `AGENTS.md` as the concise implementation and change-summary source.
- Do not build or modify the app implementation unless explicitly asked to implement it.
