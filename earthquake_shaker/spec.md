# Earthquake Shaker

## Purpose
Build a model tower with columns, beams, braces, and floor masses, then shake it using simulated earthquake ground motion. The app will measure movement based on ground-motion frequency and amplitude, show results and piece costs with a total cost and strength score, and save and compare multiple tower designs against the same or different ground motions.

## Inputs
### Building geometry
- Number of floors, editable whole number from 1 to 30, default 5.
- Floor height, feet, from 8 to 30 ft, default 10 ft.
- Plan width and plan depth, feet, using length and width boxes or click-and-drag bay boundaries.
- Number of bays in the X and Y directions, editable whole numbers from 1 to 20.
- Bay spacing, feet, in X and Y directions, default 15 ft.
- Floor area per floor, square feet, calculated from plan width and depth and displayed as editable reference data.
- Building shape: rectangle, custom floor plan, or future irregular shape; the initial control is a dropdown.
- Story mass location and slab type: floor area, slab thickness, and optional floor-material selections.

### Structure layout
- Placement mode: column, beam, brace, wall, floor, or select/delete.
- Grid snap and rotation controls for consistent member placement.
- Member endpoint selection: click two grid nodes for beams and braces, or two points on a vertical line for columns.
- Bay and story occupancy: select one bay/story at a time or apply a piece to multiple matching locations.
- Optional premanufactured library of ready-to-place pieces with preview, base size, material, mass, cost, and strength properties.
- Manual custom-piece inputs: length or span, cross-section dimensions, material, grade or strength, and member type.
- Member start and end coordinates, displayed as reference values while editing.
- Add, copy, move, rotate, delete, and undo/redo controls for all placed pieces.

### Columns
- Column material dropdown: steel, reinforced concrete, timber, or masonry.
- Column section type: rectangular, circular, wide-flange, tube, or custom.
- Column size: width, depth, diameter, wall thickness, or cross-section area as applicable.
- Concrete column input: concrete compressive strength in psi, reinforcement area in square inches, reinforcing steel yield strength in psi, and concrete volume or weight per member.
- Steel column input: nominal yield strength in ksi, section modulus, moment of inertia, cross-sectional area, and member weight.
- Timber column input: grade, species, allowable stress, modulus of elasticity, cross-sectional dimensions, and member weight.
- Column length, number of stories continued, and connection type.
- Column cost per piece, cost per foot, cost per cubic yard of concrete, or cost per pound/ton of steel.

### Beams
- Beam material dropdown: steel, reinforced concrete, prestressed concrete, timber, or composite.
- Beam section type: rectangular, I-shaped, channel, tube, timber, or custom.
- Beam dimensions: width, depth, flange/thickness, cross-sectional area, moment of inertia, and section modulus.
- Material strength inputs: concrete or timber compressive/bending strength and steel yield strength in psi or ksi.
- Reinforcement inputs for concrete beams: reinforcing area, bar size, number of bars, cover, and yield strength.
- Beam span and tributary width, which determine gravity and lateral load assignment.
- Beam connection type: pinned or fixed for simplified analysis.
- Beam cost per piece or per unit length.

### Joints and connections
- Every beam-column, beam-brace, column-brace, wall, and floor connection is modeled as a selectable joint at a structural node.
- Joint type: pinned, semirigid, fixed, welded, bolted, grout/reinforced, or custom.
- Joint strength inputs: moment capacity, axial tension capacity, axial compression capacity, shear capacity, and rotation or slip limit.
- Joint material and fastener inputs: plate or weld size, bolt diameter and number, anchor or dowel count, concrete embedment length, reinforcement grade, and reinforcement area.
- Joint stiffness inputs: rotational stiffness, translational stiffness, and damping ratio.
- Joint ductility and failure inputs: yield deformation, ultimate deformation, post-yield strength, brittle or ductile failure mode, and maximum allowable rotation or displacement.
- Joint cost per connection, installation cost, and failure/repair cost.
- Visual joint indicators show intact, yielded, damaged, or failed status during the simulation.
- Joint strength and stiffness override member strength locally when a connection is weaker than the attached member.
- Enable individual joint editing and a preset library of common pinned, bolted, welded, and reinforced-concrete joint configurations.
- The simulation shall stop propagating load through a failed joint according to its failure mode and update member forces and tower stability in real time.

### Braces and lateral systems
- Brace type: X, K, V, inverted-V, single diagonal, shear wall, or custom.
- Brace material, section size, cross-sectional area, modulus of elasticity, yield strength, and buckling length.
- Brace direction, bay location, story location, and connection type.
- Shear-wall option: wall area, wall thickness, material, reinforcement, and in-plane strength.

### Floors and masses
- Floor area in square feet per floor, editable if the plan is irregular.
- Floor slab type: reinforced concrete, steel deck, timber, or custom.
- Concrete quantity in cubic feet or cubic yards, slab thickness in inches, and unit weight in pcf.
- Steel deck or timber floor thickness and unit weight.
- Superimposed dead load in psf.
- Occupancy/live load in psf, with a simple custom distributed load option.
- Nonstructural and equipment mass in pounds or kips, with location by floor.
- Total floor mass, calculated and displayed from area, floor weight, and live-load participation.
- Partition or wall load in psf, including location or floor assignment.

### Materials library
- Select from default material presets and create only user-defined values within the custom-material option.
- Steel presets: yield strength, modulus of elasticity, density, allowable deformation, and cost.
- Concrete presets: compressive strength, modulus of elasticity, density, and cost per cubic yard.
- Timber presets: species/grade, bending strength, modulus of elasticity, density, and cost.
- Reinforcement steel presets: yield strength, density, and cost.
- Masonry presets: compressive strength, density, modulus of elasticity, and cost.
- Material-strength factors or design reductions, if a simplified strength check is selected.

### Earthquake ground motion
- Ground-motion profile: sine, pulse, white noise, or uploaded ground acceleration data.
- Dominant frequency in Hz, editable by number box or slider, with an optional frequency range and sweep rate.
- Motion amplitude in displacement units, acceleration units, or percent of peak ground acceleration.
- Peak ground acceleration in g or ft/s2, kept independent from amplitude for acceleration-based ground motions.
- Ground-motion direction and phase offset for X, Y, or both directions.
- Motion duration in seconds.
- Acceleration-time-history input: upload or paste time and acceleration values in CSV format.
- Equivalent sinusoidal ground motion inputs: frequency, peak amplitude, phase angle, duration, and cycles.
- Optional frequency sweep: starting frequency, ending frequency, sweep duration, and sweep direction.
- The app shall display the active frequency, amplitude, acceleration, and elapsed time while the simulation runs.
- Time step, using a default of 0.01 s and bounded to preserve a usable simulation.
- Damping ratio as a percent of critical damping.
- Soil or site factor, such as stiff, medium, or soft soil.
- Optional recorded motion file in CSV format with time and acceleration columns.

### Analysis and simulation controls
- Start, pause, resume, reset, and step-by-forward-frame buttons.
- Playback speed, such as 0.25x to 5x.
- Show deformation, floor movement, member forces, or acceleration overlays.
- Directional and global result scale for viewing displacement without changing calculated values.
- Structural idealization: 2D frame, 2D shear building, or future 3D model; the initial app will clearly state the selected idealization.
- Maximum simulation duration and stopping conditions, such as drift limit or member failure.

### Strength, cost, and scoring
- Structural cost inputs for every material, member, and floor component.
- Labor, connection, and foundation cost multipliers, with defaults and editable values.
- Strength score weights: maximum floor drift, peak acceleration, residual displacement, member failure count, cost efficiency, and weight.
- Target drift, allowable displacement, or code-style drift limit.
- Budget limit and cost-per-square-foot display.
- Automatic comparison ranking against saved tower versions.

### Saved versions and comparison
- Save tower name and optional notes.
- Save button to store geometry, member placement, materials, floor masses, costs, earthquake settings, and results.
- Version list with thumbnail, ground-motion settings, peak displacement, peak acceleration, total cost, strength score, and pass/fail status.
- Duplicate, rename, overwrite, export, and delete saved versions.
- Select at least two saved versions to compare displacement curves, peak values, costs, and scores.

## Calculations
The equations, rules, or logic the app uses, written out. Define every variable and its units.

## Outputs
What the app shows: numbers (with units), tables, plots, diagrams,
colors, animations.

## Look and feel
How the app looks and is laid out, what it shows when it first opens,
and how it works on a phone.

## Validation
At least one test case you have worked by hand: the exact inputs,
and the outputs the app must produce.

## Out of scope
Things the app will NOT do, so the agent doesn't add them.