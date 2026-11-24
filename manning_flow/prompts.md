# Prompts

## 2026-11-20

- **Asked:** Set up the `manning_flow` folder using the same top-level and numbered-folder layout as the previous app folders.
- **Changed:** Added `index.html`, `spec.md`, `prompts.md`, project layout guidance in `AGENTS.md`, and README files for planning, data, validation, and output. Preserved `manning.py`.
- **Worked:** Yes.

- **Asked:** Add the Manning flow function to `manning.py`.
- **Changed:** Added `manning_flow(n, A, R, S)` using Manning's equation with US customary units and flow returned in cubic feet per second.
- **Worked:** Yes.

- **Asked:** Run `manning_flow(n, A, R, S)` with multiple variable combinations and provide expected versus actual results.
- **Changed:** Ran four representative cases for roughness, area, hydraulic radius, and slope; every actual result matched the Manning equation result with zero numerical difference.
- **Worked:** Yes.

- **Asked:** Add the unit-input Manning result to the validation cases.
- **Changed:** Added `n=1`, `A=1`, `R=1`, and `S=1`, with an expected and actual flow of `1.490000 cfs`.
- **Worked:** Yes.

- **Asked:** Calculate and add the Manning result for `n=2`, `A=1`, `R=1`, and `S=1`.
- **Changed:** Added the case with expected and actual flow of `0.745000 cfs`.
- **Worked:** Yes.
