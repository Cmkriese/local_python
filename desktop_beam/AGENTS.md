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

`gui.py` is still a minimal Tkinter starter window. The project specification calls for a native desktop reimplementation of the Earthquake Shaker described in `../earthquake_shaker/spec.md`; the conversion has not yet been implemented.

## Working Rules

- Keep the specification synchronized with agreed requirements.
- After each request, update `prompts.md` with what was asked, changed, and whether it worked.
- After meaningful project or folder changes, add a dated entry to this file's change log.
- Keep implementation changes in `gui.py` unless the specification calls for additional source files.

## Change Log

- 2026-11-24: Added the standard project documentation and numbered folders for planning, data, validation, and output.
- 2026-11-24: Specified a native Tkinter desktop port of the Earthquake Shaker, using its source specification and web app as references.
