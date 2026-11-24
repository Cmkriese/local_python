# Validation Review — 2026-11-24

Compared the validation cases in `spec.md` with the current `gui.py` implementation. Ran `python -m py_compile gui.py` successfully. No automated or GUI-driven validation harness exists, so behavioral outcomes below are based on code-level inspection, not a measured desktop run.

| Case | Expected result | Actual result | Status |
|---|---|---|---|
| Falling block | A 4 ft block falls in about 0.50 s, lands, and does not pass through the floor. | No falling-block input, gravity solver, or ground-contact model exists. | Not implemented |
| 10-cycle sine baseline | 1 Hz motion runs 10 cycles in 10 s, period near 1 s, peak base displacement 1 ft, with bidirectional movement. | The animation samples a 1 Hz sine for 10 s and sways laterally. It does not model a platform, spring, or 1 ft amplitude. Its reported displacement is derived from canvas pixels and is not a physical displacement. | Partial; physics assertions fail |
| Low-motion tower | Tower responds without failure; reports roof displacement, floor acceleration, member/joint utilization, and score 75–100. | Lateral sway and a score are shown, but floor acceleration and utilization are absent. Reported displacement is not calibrated; score is based on that value and may fall outside the expected range. | Partial; expected results not met reliably |
| High-motion member failure | At 0.75 g and 2 Hz, identifies yielded/failed component and shows status/table and governing time. | At PGA ≥0.70 g, a visual collapse animation starts. No component failure calculation, governing component, or member/joint result table exists. | Partial; visual effect only |
| Weak-joint failure | Half-capacity joint fails before stronger members; identifies governing joint limit and remains selectable. | Joint placement is visual only; no capacity inputs or joint failure analysis exist. | Not implemented |
| Cost check | Itemized member, joint, floor, labor, material, foundation costs sum accurately; material changes update them. | A basic estimate is displayed, but it does not price individual pieces consistently or itemize labor/foundation. The running-test estimate uses a different formula from the editor summary. | Partial; totals are not consistent |
| Resonance sweep | Identifies natural frequency/period and resonance risk during a 0.5–3 Hz sweep. | No sweep, modal analysis, natural frequency, or resonance indicator exists. | Not implemented |
| Score and recommendations | Scores failure lower, identifies governing weakness, and offers priced upgrade recommendations without changing original. | A heuristic score is shown; no upgrade recommendations, governing weakness, or preview/apply flow exists. | Partial; recommendation checks fail |
| Save and compare | Saved versions retain test results and compare score/cost differences. | Designs save geometry and motion inputs in memory. Comparison only shows story/member counts and a rough cost; results, score differences, and stronger-design ranking are absent. | Partial; comparison checks fail |
| Invalid inputs and controls | Rejects invalid inputs; pause/replay/reset/exit work; keyboard/focus behavior is accessible. | Frequency, PGA, and duration ranges are checked; pause and reset are available. Replay and exit controls, stale-result clearing on invalid edits, and explicit focus/accessibility verification are absent. | Partial |
| Desktop layout | Clean, visible testing view at common desktop sizes. | Window is resizable and canvas expands, but the testing scene is not a separate focused view and no GUI-driven size check was run. | Partial; not visually verified |

## Summary

Only Python syntax compilation passed as an executed check. The current app is an initial interactive prototype, not a pass of the full specification validation suite. The main blockers are the absent structural dynamics/failure model, nonphysical displacement reporting, lack of a falling-block baseline, and missing result/recommendation workflows.
