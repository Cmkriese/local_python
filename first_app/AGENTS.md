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

This project is a single-page Beam Designer for simply supported and cantilever beams. The app must allow point loads and uniform loads, calculate reactions, shear, moment, and deflection, check bending and deflection, compare beam sections, and show aligned diagrams and live results.

The detailed requirements are maintained in `spec.md`. Keep this file synchronized with major requirement decisions and folder changes.

## Current specification

- `Inputs`: Defines support type, span, point loads, uniform loads, material, section, and deflection limit. It includes units, ranges, defaults, controls, load behavior, and invalid-input rules.
- `Calculations`: Defines sign conventions, units, reactions, load superposition, shear and moment, deflection integration, bending and deflection checks, section selection, extrema, and display precision.
- `Outputs`: Defines the beam drawing, aligned diagrams, pointer readouts, bending and deflection cards, passing-section recommendations, no-passing-section fallback behavior, invalid state, and immediate live updates.
- `Look and feel`: Requires a clean light design with a blue accent, square/minimal cards and controls, generous spacing, desktop side-by-side layout, and mobile stacking in the order inputs, beam, diagrams, checks. Controls use 44 px touch targets; live updates include subtle transitions for diagram redraws. Keyboard use and visible focus are required.
- `Validation`: Defines hand-calculation acceptance cases for simple uniform loading, an off-center point load, a cantilever end load, and a lumber joist, plus interaction and invalid-input checks.

## Change log

- 2026-11-19: Set up the top-level project files and numbered folders.
- 2026-11-19: Defined the complete Inputs requirements and section tables.
- 2026-11-19: Expanded Calculations with units, sign conventions, reactions, superposition, shear and moment, deflection, checks, extrema, and precision.
- 2026-11-19: Expanded Outputs with beam and diagram labeling, pointer behavior, cards, recommendations, invalid state, and live updates.
- 2026-11-19: Refined Look and feel requirements for visual style, layout, mobile behavior, motion, and accessibility.
- 2026-11-19: Refined Validation with hand-calculation results and acceptance checks.
- 2026-11-19: Built Stage 1 as a static, single-file Beam Designer mockup in `index.html` with placeholder outputs and no calculations.
- 2026-11-19: Built Stage 2 input and validation behavior in `index.html`, including synchronized spans, load controls, material-section switching, and invalid-output hiding.
- 2026-11-19: Built Stages 3 through 6 in `index.html`, including live beam drawing, draggable loads, reactions, analytical diagrams, numerical deflection, design checks, recommendations, linked pointer readouts, and responsive polish.
- 2026-11-19: Ran the validation cases in-browser and fixed the recommendation button, material/section switching guard, and blank-span validation message.
- 2026-11-19: Expanded the specification for beam deformation and along-the-beam stress visualization, using the calculated deflection curve and a green-to-red local bending-stress gradient.
- 2026-11-19: Added the beam deformation and stress visualization to `index.html`; the beam now follows the calculated deflection and is colored continuously from green at low local moment to red at maximum local moment.
- 2026-11-19: Browser-checked the new beam visualization; the default case rendered 204 colored beam segments and the “green low / red max” stress legend.

## Working rules

- After each request, update `prompts.md` with what was asked, what changed, and whether it worked.
- After each meaningful requirement or folder change, add a short entry to the change log in `AGENTS.md` and keep the change log in chronological order.
- Save every new file in the folder that best matches its purpose.
- Keep `spec.md` as the detailed source of truth and `AGENTS.md` as the concise implementation and change-summary source.
- Do not build or modify the app implementation unless explicitly asked to implement it.