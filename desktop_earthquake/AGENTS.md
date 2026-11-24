# Project Layout

This project is a Python Tkinter desktop app. Keep the application in `gui.py` and project documentation in the top-level files:

- `AGENTS.md` for project layout, working rules, and a concise change log.
- `prompts.md` for requests and their outcomes.
- `index.html` for a lightweight project landing page and run instructions.
- `spec.md` for the app's requirements and behavior.
- `00_planning/` for plans, sketches, and design decisions.
- `01_data/` for source data and sample inputs.
- `02_validation/` for test cases, hand calculations, and validation results.
- `03_output/` for screenshots and exported results.

Add a README to each project folder describing what belongs there.

## Project Status

`gui.py` contains the initial Tkinter desktop implementation of the Earthquake Shaker workflow. Its response calculation is a simplified educational estimate; consult `spec.md` for the broader target requirements.

## Working Rules

- Keep the specification synchronized with agreed requirements.
- After each request, update `prompts.md` with what was asked, changed, and whether it worked.
- After meaningful project or folder changes, add a dated entry to this file's change log.
- Keep implementation changes in `gui.py` unless the specification calls for additional source files.

## Change Log

- 2026-11-24: Corrected `00_planning/README.md` to name the Earthquake Shaker project.
- 2026-11-24: Added New/Open/Save/Save As project-file workflow with JSON `.eqs` files, unsaved-change prompts, and active project title state.
- 2026-11-24: Recorded expected-versus-actual validation review; Python syntax compilation passed, while most behavioral cases remain partial or unimplemented.
- 2026-11-24: Changed shake animation to lateral story drift and added a falling-apart effect for placed components at high input motion.
- 2026-11-24: Reworked grid placement to show Point A and a live Point B preview; made floors, joints, and endpoint rules functional.
- 2026-11-24: Replaced the starter window with a Tkinter tower editor, ground-motion controls, shake-test animation, result/cost panel, and save/compare/export workflow.
- 2026-11-24: Clarified the Tkinter desktop target and desktop-window behavior in the specification; no application code changed.
- 2026-11-24: Added the standard project documentation and numbered folders for planning, data, validation, and output.
- 2026-11-24: Specified a native Tkinter desktop port of the Earthquake Shaker, using its source specification and web app as references.
