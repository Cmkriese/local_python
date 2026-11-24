# Desktop Earthquake Shaker

## Platform

The app is a native Python desktop app built with Tkinter and launched with `python gui.py`.

This project ports the Earthquake Shaker defined in [`../earthquake_shaker/spec.md`](../earthquake_shaker/spec.md). Its current reference implementation is [`../earthquake_shaker/index.html`](../earthquake_shaker/index.html), a browser-based app rather than a Python app. Recreate its behavior with native Tkinter widgets and canvas rendering; do not embed the web app in a browser control or change the source project.

## Purpose

Recreate the Earthquake Shaker as a desktop app. Users build a model tower with columns, beams, braces, joints, and floor masses, test it with simulated earthquake ground motion, inspect movement and structural response, review cost and resilience results, and save and compare designs. Preserve the behaviors and engineering assumptions in the source specification while adapting the interface to a desktop window.

## Inputs

Implement the building geometry, structure layout, member and joint properties, floor masses, material choices, ground-motion profiles, simulation controls, cost and scoring settings, and saved-version controls specified in the source specification.

## Calculations

Use the source specification as the detailed authority for structural calculations, ground-motion simulation, damage and collapse behavior, cost calculations, scoring, and design comparisons. Preserve its units, sign conventions, validation rules, and documented limitations.

## Outputs

Provide desktop equivalents of the source app's tower editor and simulation, movement and response visualizations, member and joint results, cost breakdown, resilience score, damage report, recommendations, and saved-design comparisons.

## Look and feel

Use a resizable desktop layout with native Tkinter controls and a canvas for the editable tower and simulation visuals. Adapt browser-based interactions to mouse and keyboard input, retain clear labels and units, and keep invalid or incomplete inputs from displaying stale results.

## Validation

Meet the acceptance cases and interface checks in the source specification's Validation section. Verify that the desktop app produces consistent results for the same tower and ground-motion inputs, and that saving, loading, and comparing designs preserve their data.

## Out of scope

Do not create a second browser implementation or modify the original Earthquake Shaker project. As in the source specification, the app is an educational simulator and does not provide real-earthquake prediction, code certification, or signed engineering design.

## Implementation Steps

1. Replace the starter window in `gui.py` with the native tower editor and desktop layout.
2. Port model editing, component properties, and validation behavior from the source app.
3. Implement the source specification's structural response, damage, cost, and scoring calculations.
4. Add simulation playback, result views, recommendations, and saved-design comparison.
5. Run the source specification's validation cases against the desktop implementation.