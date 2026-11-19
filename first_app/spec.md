
# Beam Designer

## Purpose
A beam design tool for engineers and students. The user sets up a beam,
places loads on it, and picks a steel or lumber section. The app shows the
shear, moment, and deflection diagrams and checks whether the beam is
strong and stiff enough, updating instantly as anything changes.

## Users
A civil engineering student checking a homework beam, or an engineer
sizing a floor beam or deck joist.

## Inputs

| Input | Units | Range | Default | Control |
|---|---|---|---|---|
| Support type | None | Simply supported or Cantilever (fixed at the left end) | Simply supported | Segmented control or radio buttons |
| Span | ft | 4–40 ft | 20 ft | Slider and synchronized editable number box |
| Point-load magnitude | kips, downward positive | 0–100 kips | 10 kips | Editable number box |
| Point-load position | ft | 0–span | Midspan (span / 2) | Editable number box and draggable beam arrow |
| Uniform-load magnitude | kips/ft, downward positive | 0–10 kips/ft | 1 kip/ft | Editable number box |
| Uniform-load start | ft | 0–span, start <= end | 0 ft | Editable number box |
| Uniform-load end | ft | 0–span, end >= start | Span | Editable number box |
| Material | None | Steel or Douglas Fir-Larch No. 2 lumber | Steel | Dropdown |
| Section | None | Sections in the selected material | W12x26 for steel; 2x10 for lumber | Dropdown |
| Deflection limit | None | L/240 or L/360 | L/360 | Segmented control or radio buttons |

- The app opens with one uniform load over the full span.
- Loads appear in a list panel where each row can be edited or removed.
- "Add point load" creates a point load at midspan (or at the free end for
  a cantilever) with the 10-kip default magnitude.
- "Add uniform load" creates a uniformly distributed load from 0 ft to the
  full span with the 1-kip/ft default magnitude.
- Point-load positions snap to increments of 0.25 ft when dragged.
- Loads that extend past the beam end are cut off at the end.
- Zero-magnitude loads are allowed. A zero-length uniform load is allowed
  while editing but produces no load.
- Invalid, blank, or nonnumeric input values must be rejected with a clear
  error; calculated results must not be shown until the input is valid.

The available sections are:

  Steel W-shapes (E = 29,000 ksi, allowable bending stress Fb = 30 ksi):

  | Section | Ix (in^4) | Sx (in^3) | Weight (lb/ft) |
  |---------|-----------|-----------|----------------|
  | W8x10   | 30.8      | 7.81      | 10 |
  | W10x12  | 53.8      | 10.9      | 12 |
  | W12x26  | 204       | 33.4      | 26 |
  | W14x22  | 199       | 29.0      | 22 |
  | W16x26  | 301       | 38.4      | 26 |
  | W18x35  | 510       | 57.6      | 35 |
  | W21x44  | 843       | 81.6      | 44 |
  | W24x55  | 1350      | 114       | 55 |

  Douglas Fir-Larch No. 2 lumber (E = 1,600 ksi, Fb = 0.900 ksi):

  | Section | Ix (in^4) | Sx (in^3) |
  |---------|-----------|-----------|
  | 2x8     | 47.63     | 13.14     |
  | 2x10    | 98.93     | 21.39     |
  | 2x12    | 177.98    | 31.64     |
- Self-weight is ignored.

## Calculations

### Sign convention and units
- Use downward-positive point-load and uniform-load magnitudes.
- For shear and moment diagrams, take positive shear and positive moment
  as shown by the standard simply supported and cantilever sign
  conventions. Beam position `x` is measured in feet from the left end.
- Use kips for forces, kip/ft for uniform loads, feet for beam position and
  span, kip-ft for moment, ksi for stress and modulus, `in^4` for `Ix`,
  `in^3` for `Sx`, and inches for deflection.
- For deflection calculations, convert beam position and span to inches:
  `x_in = x_ft × 12`, `L_in = L_ft × 12`. Convert moment from kip-ft to
  kip-in with `M_in = M_ft × 12`.
- `E` is the modulus of elasticity from the selected material:
  29,000 ksi for steel or 1,600 ksi for Douglas Fir-Larch No. 2 lumber.
- `Ix` and `Sx` are the selected-section properties in `in^4` and `in^3`.
  Bending and flexural rigidity use `E × Ix`; `Ix` is also written `I`
  below.

### Reactions and load superposition
- Calculate all reactions by static equilibrium:
  sum of vertical forces equals zero and sum of moments about the left
  end equals zero.
- For a simply supported beam, use `RA` and `RB` for the left and right
  vertical reactions. For a cantilever fixed at the left end, use `Ay`
  and `MA` for the vertical reaction and fixed-end moment.
- Calculate reactions for every point and uniform load using superposition.
  Treat a point load of magnitude `P` at position `a` and a uniform load
  of magnitude `w` from position `c` to position `d` as independent
  contributions, in their original units.
- For a simply supported beam with a point load `P` at `a`:
  `RA = P(L - a)/L`
  and
  `RB = Pa/L`.
- For a uniformly distributed load `w` from `c` to `d`, with `d <= L`:
  `W = w(d - c)`; the resultant acts at `(c + d)/2`.
- A uniform load that extends outside the beam is clipped first so that
  `c = max(0, c)` and `d = min(L, d)`. If `d <= c`, it contributes
  neither force nor moment.
- Sum the contributions from all loads to obtain the final reactions.
- Ignore load direction reversal or negative load magnitude; all load
  magnitudes are limited to nonnegative, downward-positive values.

### Shear and moment
- Build `V(x)` and `M(x)` analytically by superposition.
- For a point load `P` at position `a`, add `-P` to the shear when crossing
  `x = a`. The moment contribution at position `x` is:
  `P(x - a)` for `x >= a`, and zero for `x < a`, using the appropriate
  simply supported or cantilever integration constant.
- For a uniform load `w` from `c` to `d`, add its loaded length
  `w × min(d - c, max(0, x - c))` to the shear when moving from left to
  right, with sign and integration constants determined from the support
  reactions. The moment contribution is found by integrating the shear
  over `x`.
- Include the exact reaction contribution and exact load-start, load-end,
  and point-load locations in all shear and moment calculations.
- Report shear and moment at every 1-ft sample and, in addition, at exactly
  every support location, load point, uniform-load start/end, and any
  calculated maximum or minimum location. Add fine samples or interpolate
  only enough to locate maxima accurately.
- `V_max_abs = max(|V(x)|)` over the beam, and `M_max_abs = max(|M(x)|)`.
  Also retain `V_max`, `V_min`, `M_max`, and `M_min` for diagram labels.

### Deflection
- Find deflection `y(x)` by integrating moment divided by flexural rigidity:
  `EI × y''(x) = M(x)`.
- Carry out the integration in inch units. Use `EI = E × I`, with `E`
  in ksi and `I` in `in^4`, so `EI` is in kip-in^2.
- For a simply supported beam, apply `y(0) = 0` and
  `y(L_in) = 0`.
- For a cantilever fixed at the left end, apply `y(0) = 0` and
  `y'(0) = 0`. The right end is free.
- Determine `y(x)` through exact analytical integration of the superposed
  load and reaction moments, or through an equivalent numerical method
  with boundary conditions applied exactly. Downward deflection is positive.
- Include every 1-ft sample and every support, load point, load start/end,
  and calculated slope-zero location where the deflection is found.
- `y_max_abs = max(|y(x)|)`, and retain the signed maximum and minimum
  values with their locations. Report deflection in inches.

### Design checks
- Bending stress is:
  `fb = |M_max_abs| × 12 / Sx`,
  where `M_max_abs` is in kip-ft and `Sx` is in `in^3`. The result is in ksi.
- The bending check passes if `fb <= Fb`, where `Fb` is 30 ksi for steel
  or 0.900 ksi for Douglas Fir-Larch No. 2 lumber.
- The deflection check passes if
  `y_max_abs <= L_in/240` or `y_max_abs <= L_in/360`, according to the
  selected deflection limit.
- The lightest passing section is found from the sections in the selected
  material. For steel, choose the passing section with the lowest weight
  in lb/ft; if two have the same weight, choose the one with the larger
  `Ix`. For lumber, choose the first passing section in the table order.
- A section passes only if both its bending and deflection checks pass.

### Output extrema and precision
- The beam drawing reaction labels use the final vertical reactions and
  fixed-end moment. Draw downward loads with downward arrows.
- The shear diagram reports `V_max_abs` and the moment diagram reports
  `M_max_abs`. The deflected shape reports `y_max_abs` and its location.
- The hover calculation uses the final `V(x)`, `M(x)`, and `y(x)` at the
  selected beam position from the same analytical or numerical solution.
- Keep full precision in calculations. Display shear and moment to three
  significant figures, deflection and limits to three decimal places,
  stress to two decimal places, and section properties in the table format.

## Outputs
- **Beam drawing:** Show the beam span, simply supported or fixed supports,
  all point and uniform loads, and the final reactions. Point loads appear
  as single downward arrows labeled with their magnitude in kips and
  position in ft. Uniform loads appear as a row of downward arrows labeled
  with their magnitude in kips/ft and their start and end positions in ft.
  Show reaction magnitude and direction: left and right vertical reactions
  for a simply supported beam, or vertical reaction and fixed-end moment
  for a cantilever. Reaction values are displayed to two decimal places.
- **Aligned diagrams:** Stack the shear, moment, and deflected-shape
  diagrams below the beam drawing. Use the same horizontal x scale in ft
  for the beam and all three diagrams, with beam position values increasing
  from left to right. Use an adaptive y scale for each diagram; each scale
  starts at or includes zero and is sized to contain the full signed curve.
- **Shear diagram:** Fill the area under the curve and label the positive
  maximum, negative minimum, and absolute maximum with each location in ft.
  Units are kips.
- **Moment diagram:** Fill the area under the curve and label the positive
  maximum, negative minimum, and absolute maximum with each location in ft.
  Units are kip-ft.
- **Deflected-shape diagram:** Fill the area under the curve and label the
  positive maximum, negative minimum, and absolute maximum with each location
  in ft. Units are inches. Draw downward deflection as positive, and use an
  adaptive scale sized to contain the complete deflected shape. The drawing
  may exaggerate deflection visually, but must clearly state or distinguish
  that the vertical scale is not the same as the horizontal scale.
- **Pointer readout:** Moving the pointer over the beam drawing or any diagram
  places the same vertical guide at that x position across the beam and all
  three diagrams. Display `x` in ft and the corresponding `V` in kips,
  `M` in kip-ft, and `y` in inches. Hide the pointer readout when the pointer
  leaves the linked drawing and diagram area.
- **Bending check card:** Display the actual bending stress `fb` in ksi, the
  allowable stress `Fb` in ksi, the utilization ratio `fb/Fb`, a utilization
  bar, and `PASS` or `FAIL`. Use green below 70% utilization, amber from 70%
  through 100%, and red above 100%. Hovering over the card explains the
  formula `fb = |M|max × 12 / Sx`.
- **Deflection check card:** Display the actual maximum absolute deflection
  in inches, the selected allowable deflection `L/240` or `L/360` in inches,
  the utilization ratio `actual/allowable`, a utilization bar, and `PASS` or
  `FAIL`. Use the same green, amber, and red utilization thresholds and
  hovering behavior. Hovering over the card explains the formula used and the
  selected deflection limit.
- **Section recommendation:** When one or more sections pass both checks,
  list the lightest passing section and provide a button to apply it as the
  selected section. For steel, choose the lowest-weight passing section,
  breaking ties by larger `Ix`; for lumber, choose the first passing section
  in table order.
- **Fallback recommendation:** When no section in the selected material
  passes, state clearly that no section passes and show the section with the
  lowest governing utilization ratio. The governing ratio is
  `max(fb/Fb, y_max_abs/allowable deflection)`. The section with the lowest
  governing ratio is the closest section. Do not present it as a passing
  section.
- **Invalid state:** If any input is invalid, blank, or nonnumeric, hide all
  beam and diagram results, hide both check cards, and show a clear validation
  message instead. Do not keep or mark stale calculated results.
- **Live updates:** Recalculate and update every valid output immediately
  whenever any input changes. Do not require an Apply button or a debounce.

## Look and feel
- Opens with an example already loaded (20 ft simply supported W12x26
  with a 1 kip/ft uniform load over the full span), so it is useful the
  moment it opens.
- Clean and professional, like a commercial engineering web app: light
  background, white cards with soft shadows, one accent color, a modern
  system font, generous spacing. No clutter.
- Inputs in a panel on the left; drawing, diagrams, and checks on the
  right. On a phone, the panels stack.
- Every input has a short label with units. Hovering over a check card
  explains the formula used.

## Validation
The app will be considered complete only if all of the following hand
calculation cases pass using the specified material properties and full
precision in the calculations. Displayed values follow the rounding rules
in the Calculations section.

1. Simply supported beam with full-span uniform load:
   - Span: 20 ft
   - Section: W12x26
   - Uniform load: 1 kip/ft from 0 to 20 ft
   - Deflection limit: L/360
   - Left and right reactions: 10.00 kips each
   - Maximum absolute shear: 10 kips at 0 ft and 20 ft
   - Maximum absolute moment: 50.0 kip-ft at 10 ft
   - Bending stress: 17.96 ksi
   - Allowable bending stress: 30.0 ksi
   - Maximum deflection: 0.609 in at 10 ft
   - Deflection limit: 0.667 in
   - Both bending and deflection checks pass.

2. Simply supported beam with an off-center point load:
   - Span: 20 ft
   - Section: W12x26
   - Point load: 10 kips at 5 ft
   - Deflection limit: L/360
   - Left reaction: 7.50 kips
   - Right reaction: 2.50 kips
   - Maximum absolute moment: 37.5 kip-ft at 5 ft
   - Bending stress: 13.47 ksi
   - Allowable bending stress: 30.0 ksi
   - Maximum deflection: approximately 0.325 in at approximately 7.64 ft
   - Deflection limit: 0.667 in
   - Both bending and deflection checks pass.

3. Cantilever beam with a point load at the free end:
   - Span: 10 ft
   - Section: W12x26
   - Point load: 5 kips at 10 ft
   - Deflection limit: L/360
   - Vertical reaction: 5.00 kips upward
   - Fixed-end moment: 50.0 kip-ft
   - Maximum absolute moment: 50.0 kip-ft at the fixed end
   - Bending stress: 17.96 ksi
   - Allowable bending stress: 30.0 ksi
   - Maximum deflection: approximately 0.487 in at the free end
   - Deflection limit: 0.333 in
   - Bending passes and deflection fails.

4. Simply supported Douglas Fir-Larch No. 2 2x10 joist:
   - Span: 12 ft
   - Section: 2x10
   - Uniform load: 0.05 kip/ft over the full span
   - Deflection limit: L/360
   - Left and right reactions: 0.30 kip each
   - Maximum absolute moment: 0.90 kip-ft at 6 ft
   - Bending stress: 0.505 ksi
   - Allowable bending stress: 0.900 ksi
   - Maximum deflection: approximately 0.147 in at 6 ft
   - Deflection limit: 0.400 in
   - Both bending and deflection checks pass.

### Additional acceptance checks
- Changing the support type to cantilever updates reactions, moment,
  deflection boundary conditions, and the beam diagram immediately.
- Adding, removing, editing, or dragging a load updates all reactions,
  diagrams, cards, and recommendations.
- A point load position or uniform-load boundary outside the beam is
  clipped or rejected according to the Inputs rules.
- Invalid, blank, nonnumeric, out-of-range, or inconsistent values hide all
  calculated output and show a clear validation message.
- When no section passes, the fallback recommendation is the section with
  the lowest value of `max(fb/Fb, y_max_abs/allowable deflection)`.
- Each diagram must include the same beam span and x-axis scale.
- Pointer movement over the beam or a diagram must show the matching
  `x`, `V`, `M`, and `y` readout across the linked diagrams.

## Build stages

### Stage 1: Static page mockup
- Build the desktop and mobile layout in `index.html` only.
- Include the left input panel, right beam area, stacked diagram area,
  and check-card placeholders.
- Use the 20 ft simply supported W12x26 example as visible demo text, but
  do not implement calculations.
- Test at desktop and phone widths. Confirm the layout stacks correctly,
  controls are usable, 44 px touch targets are respected, and horizontal
  scrolling is not required.

### Stage 2: Working inputs and validation
- Add support, span, point-load, uniform-load, material, section, and
  deflection-limit controls with the specified defaults and ranges.
- Implement add, remove, and edit actions for loads, synchronized span
  controls, and invalid-input handling.
- Test that defaults load correctly, range and consistency errors appear,
  valid changes update state immediately, and invalid inputs hide stale
  calculated results.

### Stage 3: Beam drawing and load interaction
- Draw the beam with a shared horizontal x scale, supports, load arrows,
  reaction placeholders, and span labels.
- Add point-load dragging with 0.25 ft snapping and uniform-load editing
  with clipped boundaries.
- Test that simply supported and cantilever symbols are correct, control
  values and drawing values stay synchronized, dragging stays on the beam,
  and load changes update live.

### Stage 4: Reactions, shear, and moment
- Implement static equilibrium, point-load and uniform-load superposition,
  and analytical `V(x)` and `M(x)` sampling.
- Draw aligned shear and moment diagrams with zero baselines and positive,
  negative, and absolute extrema.
- Test the validation cases, especially 10 kips reactions, the 50.0 kip-ft
  uniform-load moment, the 37.5 kip-ft point-load moment, and the cantilever
  fixed-end moment.

### Stage 5: Deflection and design checks
- Integrate moment using inch units and the selected `E`, `Ix`, and support
  boundary conditions.
- Calculate bending stress, deflection limits, pass/fail bars, and section
  recommendations.
- Test that the 20 ft uniform-load case deflects approximately 0.609 in,
  lumber and cantilever cases pass or fail as specified, and fallback
  ranking uses the governing utilization ratio.

### Stage 6: Linked readout and prototype polish
- Add the shared pointer vertical guide and linked `x`, `V`, `M`, and `y`
  readout. Finish extrema labels, formula tooltips, visible focus states,
  adaptive diagram scales, and live transitions.
- Recheck calculations and responsive behavior after the final integration.
- Test that pointer movement stays synchronized, keyboard focus is visible,
  pass/fail colors are legible, and all validation cases work on desktop
  and mobile.

## Out of scope
- Beam geometry other than a prismatic, straight beam with the two
  support types provided.
- Continuous, indeterminate, and other beam configurations beyond
  simply supported and cantilever.
- Custom materials, custom section properties, and custom section sizes.
- Applied moments, sloping loads, impact loads, moving loads, dynamic
  loads, and seismic or wind load combinations.
- Load combinations and factored or strength-design load cases.
- Self-weight of the beam or section.
- Shear stress and shear design checks.
- Lateral-torsional buckling, local buckling, torsion, axial stress,
  and combined-stress checks.
- Bearing stress, web or flange crippling, connections, supports,
  foundations, and other structural detailing.
- Bracing, lateral stability, deflection from non-bending effects,
  and cambers.
- Composite beams, built-up sections, reinforced concrete, prestressed
  concrete, and other material systems.
- Three-dimensional models and three-dimensional frame or truss analysis.
- Saving, loading, sharing, exporting, or printing designs.

## Beam deformation and stress visualization
- When the beam has any nonzero load, the beam drawing must show the
  calculated deflected shape instead of a straight beam. When all loads
  have zero magnitude or have zero effective length, the beam remains
  straight with no calculated deflection.
- Use the same `y(x)` deflection values calculated for the deflected-shape
  diagram. Downward deflection is positive and must therefore display the
  beam downward when the load direction is downward.
- Apply a visible vertical exaggeration to the beam drawing if needed so
  the deformation is clear, but keep the horizontal span and support
  locations consistent with the beam scale. The exaggeration must not change
  the displayed deflection value in the linked pointer readout.
- Color the beam along its length to model bending stress. Calculate the
  local bending stress at each position as
  `fb(x) = |M(x)| × 12 / Sx`.
- Use a continuous green-to-red color gradient along the beam: green
  represents zero or minimum stress and red represents the maximum absolute
  moment/bending stress along the beam. Intermediate stress values use an
  intermediate green-to-yellow-to-red color progression.
- The maximum-stress location must be visually red. The beam drawing must
  update the deformed shape and stress colors immediately when span, loads,
  supports, material, or section changes.
- Keep the stress gradient visually distinct from the beam and supports, and
  add a brief legend such as “Stress: Green = low, Red = max” to the beam
  drawing or its surrounding card.