# Earthquake Shaker

## Purpose
Create a native Python desktop application using Tkinter. Users build a model tower with columns, beams, braces, and floor masses, then shake it using simulated earthquake ground motion. The app measures movement based on ground-motion frequency and amplitude, shows results and piece costs with a total cost and strength score, and saves and compares multiple tower designs against the same or different ground motions. The desktop app is a reimplementation of the Earthquake Shaker described by the source project specification; it does not depend on a browser or web application runtime.

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
- Peak ground acceleration in g or ft/s². PGA and displacement amplitude shall be separate display/control modes; in sine-PGA mode, equivalent displacement shall be calculated, and in sine-displacement mode, PGA shall be calculated.
- Ground-motion direction and phase offset for X, Y, or both directions.
- Motion duration in seconds.
- Acceleration-time-history input: upload or paste time and acceleration values in CSV format.
- Equivalent sinusoidal ground motion inputs: frequency, peak amplitude, phase angle, duration, and cycles.
- Optional frequency sweep: starting frequency, ending frequency, sweep duration, and sweep direction.
- The app shall display the active frequency, amplitude, acceleration, and elapsed time while the simulation runs.
- Time step, using a default of 0.01 s and bounded to preserve a usable simulation.
- Damping ratio as a percent of critical damping.
- Soil or site factor, entered as a dimensionless multiplier or preset: stiff 0.85, medium 1.00, or soft 1.20. The multiplier is applied only to the generated ground acceleration; it shall not change uploaded records unless the user explicitly enables scaling.
- Optional recorded motion file in CSV format with time and acceleration columns.

### Analysis and simulation controls
- Start, pause, resume, reset, and step-by-forward-frame buttons.
- Playback speed, such as 0.25x to 5x.
- Show deformation, floor movement, member forces, or acceleration overlays.
- Directional and global result scale for viewing displacement without changing calculated values.
- Structural idealization: 2D frame with lumped floor masses. The 2D frame shall be the initial and default model.
- The 2D shear-building model and 3D visual/analysis options may be deferred to later releases.
- Maximum simulation duration: 1 to 10 seconds, default 10 seconds, plus stopping conditions such as drift limit or member failure.

### Strength, cost, and scoring
- Default preset costs for every material, member, joint, and floor component shall come from the app's cost library.
- User-entered cost overrides shall be optional and shall be advanced inputs, not required for normal use.
- Labor, connection, and foundation cost multipliers shall have defaults and may be edited as advanced inputs.
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

### Project files
- Provide File menu commands for New, Open, Save, and Save As, with keyboard shortcuts for common actions.
- Store the active tower geometry, placed components, material preset, ground-motion profile and settings, and saved design versions in a portable project file.
- Opening an unsupported or malformed project shall show an understandable error and leave the current project unchanged.
- Prompt to save unsaved edits before opening another project, starting a new project, or closing the application.
- Show the active project name in the window title and indicate unsaved changes.

## Calculations
### Calculation scope and sign conventions
- The initial physics model shall be a two-dimensional, lumped-mass, multi-degree-of-freedom shear and bending frame in the selected X or Y direction.
- Gravity is positive downward for weight and mass calculations. Horizontal ground acceleration is positive in the selected positive X or Y direction.
- Floor displacement `u_i`, floor velocity `v_i`, floor acceleration `a_i`, and base acceleration `ag(t)` use feet or inches consistently throughout each calculation.
- The first version shall use feet, seconds, kips, kip-feet, pounds per cubic foot, and g for display. Internal calculations shall use one consistent unit system, preferably feet and kips or inches and kips, and convert only at input/output boundaries.
- All coordinates, floor masses, member properties, joints, and costs shall remain in memory as the user edits the model.
- The physics engine shall advance all degrees of freedom using the same time step and shall expose both the analytical equations and the sampled frame for student/engineering review.

### Floor masses and gravity loads
- `A_floor,i = sum of the usable floor area on story i` in square feet.
- Floor slab weight is `W_slab,i = A_floor,i × t_slab,i × gamma_slab,i / 144`, where slab thickness is in inches and unit weight is in pcf. The result is pounds or can be divided by 1000 for kips.
- Steel deck or timber slab weight is `W_slab,i = A_floor,i × w_slab,i`, where `w_slab,i` is psf.
- Superimposed dead load is `W_dead,i = A_floor,i × w_dead,i`.
- Live load is `W_live,i = A_floor,i × w_live,i × L`, where `L` is the live-load participation factor for earthquake mass, bounded from 0 to 1 and clearly identified as an input or standard simplification.
- Wall, partition, and equipment mass is `W_misc,i = sum of all assigned loads on floor i`.
- Effective floor weight is `W_i = W_slab,i + W_dead,i + W_live,i + W_misc,i`.
- Lumped floor mass is `m_i = W_i / g`, where `g = 32.174 ft/s²` for US units. Display mass in kip-sec²/ft or pounds-sec²/in as appropriate.
- Every concentrated floor mass is added to the story mass at its entered location.
- Base mass is excluded from the floor response. Foundation and soil-structure interaction may be enabled only as a future model option.

### Member section properties
- Axial area is `A = A_custom` or is calculated from the selected member section.
- Moment of inertia is `I = I_custom` or is calculated from member dimensions.
- Section modulus is `S = I/c`, where `c` is distance from the neutral axis to the extreme fiber.
- Member weight is `W_member = rho × L_member × A_member` using consistent length and area units.
- Column, beam, and brace quantities are summed once; repeated identical pieces in matching bays count by placement quantity.
- Elastic modulus `E` is selected from the material library: steel, concrete, timber, masonry, or custom material.
- For composite members, the initial model shall use an equivalent axial area and equivalent flexural stiffness `EI` documented beside the result.

### Beam and column stiffness
- Axial member stiffness is `k_axial = E A / L`.
- Flexural stiffness scale is `k_bending = E I / L³`.
- Beam stiffness matrix terms use classical Euler-Bernoulli 2D frame stiffness with axial and bending degrees of freedom at each end.
- Axial deformation is `delta_axial = N L / (E A)`.
- Elastic beam bending displacement is estimated from the member end forces and exact beam-end stiffness rather than by treating the beam as an isolated pin-ended member.
- Joint rotational stiffness `K_rj` is placed in series with or added to the member-end rotational stiffness according to the selected semirigid joint model:
  `K_eff = (K_member K_rj) / (K_member + K_rj)`.
- If a joint is pinned, its rotational stiffness and moment capacity are set to zero. If fixed, its full elastic and nonlinear moment capacity is controlled by the entered joint strength.
- Column effective length is `K_eff_length L`, using an editable effective-length factor from 0.5 to 2.0. The default is 1.0.

### Brace stiffness and buckling
- Brace axial stiffness is `k_brace = E A / L`, with tension-only behavior optionally selected by the user.
- Euler buckling load is `P_e = π² E I / (K_eff_length L)²`.
- Compression capacity is limited by member yield and buckling:
  `P_cap = min(fy A, P_e)`.
- Brace force in a 2D brace is `F_brace = k_brace (u_endpoint1 - u_endpoint2)`.
- Components in global X and Y are `Fx = F_brace dx/L` and `Fy = F_brace dy/L`.
- If the brace is in tension, a positive axial force is allowed. If compression exceeds `P_cap`, mark compression yielded/buckled and reduce brace stiffness using a nonlinear factor:
  `E_eff = E × r_buckling`, where `r_buckling` is from 0.05 to 1.0.

### Global stiffness and damping
- Each member produces a 6 × 6 local frame stiffness matrix for the initial 2D model and is transformed to global coordinates.
- Assemble the full stiffness matrix:
  `K = sum(Tᵀ k T)`.
- Assemble the diagonal or lumped floor mass matrix `M`.
- Apply Rayleigh damping:
  `C = alpha M + beta K`.
- The default damping ratio shall be `ζ = 5%` of critical damping. For the initial 2D model, choose `alpha` and `beta` so the selected or default damping ratio is achieved in the first two modes.
- The damping-ratio input shall accept 0% to 30%. For a constant target ratio in modes 1 and 2, solve the two Rayleigh equations:
  `ζ_i = alpha/(2 omega_i) + beta omega_i/2`.
- Calculate the first two natural frequencies and periods from
  `(K - omega²M)phi = 0`.
- Circular frequency is `omega_n = sqrt(lambda_n)`, frequency is `f_n = omega_n / (2 pi)`, and period is `T_n = 1/f_n`.
- Damping ratio for mode `n` is `ζ_n = (alpha/(2 omega_n) + beta omega_n/2)`.
- Modal mass participation of each floor is reported for X and Y motion.
- Resonance risk is increased when the ground-motion frequency is within 20% of a building natural frequency.

### Base ground motion
- A sine ground acceleration is
  `ag(t) = PGA × sin(2 pi f t + phi)` for the selected direction.
- A sine displacement amplitude `A_motion` may be converted to acceleration amplitude by
  `a0 = A_motion (2 pi f)²`.
- If the ground-motion control is in PGA mode, the app shall calculate and display the equivalent displacement:
  `A_motion = PGA × g / (2 pi f)²`.
- If the control is in displacement-amplitude mode, the app shall calculate and display equivalent PGA:
  `PGA = A_motion × (2 pi f)² / g`.
- The app shall never combine a separately entered amplitude and PGA by adding or multiplying both fields. It shall use the active control mode and convert the paired value.
- Uploaded acceleration-time history values are interpolated at each numerical time step.
- A frequency sweep uses `f(t) = f_start + (f_end - f_start)t/T_sweep`.
- The ground velocity and displacement shall be generated or integrated from acceleration with a baseline correction. The table motion in the physics model uses `ag(t)` plus the selected soil factor.
- For bidirectional motion, calculate X and Y ground accelerations independently and combine the joint/member response with the selected phase and square-root-sum-of-squares peak display.

### Earthquake equation of motion
- For relative floor displacement `u(t)`:
  `M u¨ + C u˙ + K u = -M r ag(t) + F_nonlinear(t)`.
- `r` is the influence vector indicating the direction of base acceleration.
- Absolute floor acceleration is `a_abs,i = u¨_i + ag(t)`.
- Ground acceleration shall be applied to all masses, while local member damping and nonlinear joint forces shall act on relative motion.
- P-delta effects may be included using an approximate geometric stiffness:
  `K_geo = sum(N_member/L × transform terms)`.
- Effective stiffness is `K_eff = K - K_geo`.
- The 2D model shall not continue after geometric instability or stiffness singularity except to mark collapse.

### Numerical time integration
- The default time step is `dt = 0.01 s`, bounded by `dt <= 0.1/f_max`.
- Use Newmark-beta integration with `beta = 1/4` and `gamma = 1/2` for constant-average acceleration.
- At each step calculate:
  `u_{n+1} = u_n + dt v_n + dt²((1/2-beta)a_n + beta a_{n+1})`
  and
  `v_{n+1} = v_n + dt((1-gamma)a_n + gamma a_{n+1})`.
- Iterate within a time step if nonlinear member or joint states change.
- Recalculate member forces, joint forces, damage states, and ground-story support conditions after each accepted step.
- Stop and mark collapse if the floor drift exceeds a user-set collapse limit, a support node loses stability, or the stiffness matrix becomes singular.

### Member forces and stresses
- At each member, calculate axial force `N`, shear force `V`, and bending moment `M` from element end displacements.
- For a prismatic member:
  `sigma_axial = N/A`.
- Beam and column bending stress:
  `sigma_bending = M c/I`.
- Maximum combined axial/bending stress:
  `sigma_member = sigma_axial ± sigma_bending`.
- Steel utilization shall use `N/Ny + abs(M/My)` or an entered interaction rule, with `Ny = fy A` and `My = fy S`.
- Concrete utilization shall use an elastic axial/bending demand ratio against the selected characteristic or allowable concrete stress until a nonlinear concrete model is explicitly added.
- Timber utilization shall use combined bending and axial demand against the selected grade's bending and axial allowable stresses.
- Concrete and timber capacity rules shall use their input strength values and shall state "elastic/educational approximation" in the report because they are not a replacement for code design.
- Principal plane stress is not required in the initial 2D model, but combined bending and axial demand shall be reported for every member.
- Member strain is `epsilon = sigma/E` in the elastic range.
- Curvature is `kappa = M/EI`.
- Cross-sectional strain at extreme fiber is `epsilon_member = sigma/Es` for steel or `epsilon = delta/length` for simplified axial strain.
- Plastic or damage strain is tracked with:
  `epsilon_accum = sum(abs(epsilon - epsilon_previous))`.
- Member utilization ratio is `demand/capacity`, where capacity is the minimum of yielding, buckling, shear, or connection limits.
- Mark a member elastic, yielded, damaged, or failed when utilization crosses the entered threshold or material limit.

### Joint forces, stress, and strain
- At every joint, calculate the sum of member axial, shear, and moment demands:
  `V_joint = sum(V_member)`, `N_joint = sum(N_member)`, and `M_joint = sum(M_member)`.
- Joint shear stress is `tau_joint = V_joint/A_joint`.
- Joint axial stress is `sigma_joint = N_joint/A_joint`.
- Joint bearing stress is `sigma_bearing = demand/(bolt area × bearing factor)` or `demand/(bearing area)` for the simplified model.
- Weld stress is combined shear and tension using entered weld area and throat thickness.
- Joint moment utilization is `abs(M_joint)/M_joint_capacity`.
- Joint shear utilization is `abs(V_joint)/V_joint_capacity`.
- Joint axial utilization is `max(abs(N_joint)/N_tension_capacity, abs(N_joint)/N_compression_capacity)`.
- Governing joint utilization is the maximum of moment, shear, axial, and rotation utilization.
- Joint rotation demand is `theta_joint = abs(theta_left - theta_right)` or is directly reported from the semirigid joint rotation state.
- Rotation utilization is `theta_joint/theta_joint_limit`.
- Joint strain shall be reported only for an applicable material or fastener direction. Where it is estimated, use:
  `epsilon_joint = slip_or_axial_deformation / gauge_length`,
  or for rotation, `epsilon_joint = theta_joint × distance_from_joint_center / gauge_height`.
- A joint enters the yielded range when demand first exceeds its entered yield strength.
- A joint is damaged when demand exceeds 60% of ultimate capacity and it has residual deformation.
- A joint fails when moment, shear, axial, rotation, or fastener capacity is exceeded.
- Failed joints lose stiffness according to the selected brittle or ductile failure mode. Ductile failure retains a fraction `r_residual` of strength; brittle failure reduces strength toward zero.

### Movement and response outputs
- Floor drift is `delta_i = u_i - u_{i-1}`, and interstory drift ratio is `IDR_i = delta_i/h_i`.
- Peak floor displacement is `u_peak,i = max(abs(u_i(t)))`.
- Peak absolute floor acceleration is `a_peak,i = max(abs(u¨_i(t)+ag(t)))`.
- Maximum base shear is calculated at each time step as
  `V_base(t) = abs(sum(m_i × a_abs,i(t)))`.
- Report the positive and negative peak values and the maximum absolute base shear:
  `V_base,max = max(abs(V_base(t)))`.
- Residual displacement at the end of the simulation is `u_residual,i = u_i(T_end)`.
- Story rotation is `theta_i = (u_i-u_{i-1})/h_i`.
- Roof drift is `(u_roof-u_base)/H`.
- Total collapse or floor-contact failure occurs if any floor drift or deformation brings a floor below the ground or intersects another floor in the 2D model.
- For the screenshot validation, run a single block from height `h`, whose theoretical free-fall time is `t_f = sqrt(2h/g)`. Then use 10 cycles of the table motion and calculate measured period and amplitude from two successive extreme positions.
- Ground-motion validation shall compare the model's table period and amplitude against the entered sine frequency and displacement amplitude.

### Damage and collapse rules
- The first nonlinear model shall use simplified plastic hinges at member ends and nonlinear rotational springs at joints.
- It shall not use fiber sections, layered concrete, or full fracture mechanics in the first release.
- Plastic hinge behavior shall include yield moment, ultimate rotation, residual strength, and a residual-rotation state.
- Joint springs shall include yield force or moment, slip/rotation limit, ductile or brittle post-yield behavior, stiffness degradation, and residual deformation.
- Axial yielding and brace buckling shall remain member-level properties rather than full cross-sectional plastic-zone calculations.
- Member damage states:
  - Elastic: governing utilization `< 0.6`
  - Yielded: utilization from `0.6` to `1.0`
  - Damaged: utilization greater than `1.0` or residual deformation present
  - Failed: demand exceeds ultimate capacity, buckling limit, or assigned joint limit
- Joint damage shall use the same state thresholds and shall override the member state at its endpoints.
- A tower is collapsed when a floor contacts the ground, a support node loses stability, the stiffness matrix is singular for the active frame, or a user-set collapse threshold is exceeded.
- Partial damage may continue the simulation at reduced stiffness for an entered number of time steps or until the tower collapses.

### Earthquake magnitude and strength rating
- The app shall optionally provide an estimated magnitude-like scenario scale using user-selected earthquake size rather than pretending to calculate a seismological magnitude.
- A scenario ground motion may be mapped to a peak ground acceleration range:
  - Light: `PGA < 0.10 g`
  - Moderate: `0.10 g to 0.25 g`
  - Strong: `0.25 g to 0.50 g`
  - Severe: `0.50 g to 1.00 g`
  - Extreme: `PGA > 1.00 g`
- These ranges shall be labeled scenario classes, not official magnitude estimates.
- The entered frequency and duration shall remain visible beside the scenario class.
- If recorded acceleration data are used, classify the motion from calculated peak ground acceleration, dominant frequency, and duration.

### Piece cost and total cost
- Member cost:
  `C_member = quantity × (C_per_unit × L_member + C_fabrication)` for linear pieces.
- Section-based cost may instead use:
  `C_member = rho × A_member × L_member × C_per_weight`.
- Concrete piece cost:
  `C_concrete = volume_cubic_yards × C_per_cubic_yard`.
- Reinforcement cost:
  `C_rebar = rebar_weight × C_per_weight`.
- Joint cost:
  `C_joint = C_fasteners + C_weld_or_bolt + C_plate + C_installation`.
- Floor cost:
  `C_floor = A_floor × C_slab_per_square_foot + C_finishes`.
- Beams and columns belonging to a floor shall be counted once in the member-cost total, not added again to the floor cost.
- Total cost:
  `C_total = sum(C_column + C_beam + C_brace + C_joint + C_floor + C_foundation) × (1 + labor_fraction)`.
- Display piece cost by member, floor cost, connection cost, material cost, labor cost, and total cost.
- Cost is updated live whenever geometry, section, material, reinforcement, or quantity changes.

### Resilience score
- Calculate a 1 to 100 resilience score without using a pass/fail binary as the entire score.
- Normalize each response metric against entered or recommended limits:
  `r_drift = peak roof or interstory drift / allowable drift`
  `r_accel = peak floor acceleration / target acceleration`
  `r_residual = peak residual drift / allowable residual drift`
  `r_member = max member utilization`
  `r_joint = max joint utilization`
  `r_cost = C_total/C_budget`, with `r_cost = 1` for a cost exactly at budget.
- Collapse, floor contact, or support failure shall set the score to 1 and require a concise collapse reason.
- The design score shall use all response and cost metrics:
  `S_performance = 100 × (1 - weighted_mean(r_drift, r_accel, r_residual, r_member, r_joint, r_cost))`.
- Every metric shall be clipped at 2.0 before weighting.
- Default weights shall be drift 30%, member utilization 25%, joint utilization 20%, residual movement 10%, acceleration 10%, and cost 5%.
- `r_cost = C_total/C_budget` shall be clipped at 2.0; a design at or under budget receives no cost penalty beyond the weight of cost efficiency.
- The app shall not add a separate survivability bonus or separate over-budget multiplier, so the score formula is auditable and its component values add to one total.
- Clip the final result:
  `Score = round(clamp(S_performance, 1, 100))`.
- The score description shall be written in plain language:
  - 90 to 100: excellent control with minor or no damage
  - 75 to 89: strong performance with limited yielding or drift
  - 60 to 74: moderate performance with repairable damage
  - 40 to 59: weak performance with significant yielding or joint risk
  - 1 to 39: collapse risk or severe damage
- The app shall explain what earthquake condition the selected score was measured against.

### Interactive upgrade recommendations
- Rank the highest local utilization components rather than automatically recommending a blanket redesign.
- For each member or joint with utilization greater than 0.70, calculate at least one lower-cost option and one stronger option.
- Member upgrade options include increasing column or beam section area, moment of inertia, brace area, joint stiffness, or adding a brace/shear wall.
- Connection upgrade options include stronger plates, larger or more bolts, stronger welds, additional reinforcement, or a ductile joint.
- Additional lateral resistance shall include a base-isolation option, tuned-mass damper option, or supplemental damping only if the selected input/physics model includes it.
- Recommendation cost is `C_upgrade = sum(piece and joint replacement costs) + labor and downtime estimate`.
- The displayed improvement estimate shall compare predicted peak drift, max member utilization, max joint utilization, and 1–100 score before and after the proposed upgrade.
- Recommended changes shall not replace the user's model until accepted by a preview or apply action.
- Each recommendation shall state expected benefit, additional cost, and score increase.

### Saved comparison results
- Store the complete calculation inputs and output summary for each saved tower version.
- Comparison metrics shall include peak floor displacement, interstory drift, peak acceleration, max member stress, max member strain, max joint stress, max joint strain, residual displacement, base shear, member failure count, joint failure count, total cost, and score.
- Select two or more saved designs and calculate relative improvement:
  `Improvement = New score - Saved score` and
  `Cost difference = New cost - Saved cost`.
- The stronger design is the one with the higher score under the same ground-motion record or scenario.

## Outputs
### Resilience score summary
- The primary result shall be a large 1–100 resilience score, the exact score condition, and the scenario used to calculate it.
- The app shall show a plain-language score description: 90–100 excellent, 75–89 strong, 60–74 moderate, 40–59 weak, and 1–39 severe damage or collapse risk.
- The score panel shall list its major components: drift score, acceleration score, residual-movement score, member utilization score, joint utilization score, and cost score.
- A compact breakdown shall show the contribution and penalty of each component rather than only a final number.
- The explanation shall state whether the tower survived, yielded, became damaged, failed partially, or collapsed.
- The output shall identify the governing weakness, such as excessive drift, weak joint moment capacity, member buckling, resonance, residual displacement, or cost overrun.
- If no failure occurs, the app shall state which limit was closest to being exceeded and by how much.
- If the design collapses, the app shall show the first collapse event, elapsed time, affected floor or joint, and the failure mode.

### Ground-motion and resonance summary
- The output shall display active or uploaded ground motion, peak ground acceleration in g and ft/s², dominant frequency in Hz, motion amplitude, duration, and direction.
- The app shall display the measured or uploaded table motion period and amplitude alongside the entered values.
- A response-spectrum or frequency-sweep panel shall show peak floor displacement and peak floor acceleration across frequencies.
- The app shall identify natural frequencies and periods for the selected tower modes.
- Resonance shall be marked when a ground-motion frequency is within 20% of a calculated natural frequency.
- The output shall report the critical frequency, critical amplitude or PGA, peak amplification factor, and estimated displacement at resonance.
- When a frequency sweep is used, the app shall mark the frequency with the highest roof displacement and the frequency with the highest member or joint utilization.
- The app shall state whether the risk is base motion resonance, floor resonance, or both.
- A resonance safety bar or line shall show safe, caution, and resonance-risk frequency bands.

### Building movement output
- The main animation shall show the base motion and simulated tower movement with an exaggerated displacement scale that is clearly labeled.
- The animation shall display the current elapsed time, floor displacement, floor acceleration, story drift, and ground acceleration.
- Each floor shall have a selectable marker showing absolute displacement, relative displacement, velocity, and acceleration.
- The app shall display peak roof displacement, peak floor displacement for every story, maximum interstory drift, maximum drift ratio, and residual displacement.
- Direction-specific outputs shall be reported for X and Y motion when bidirectional input is used.
- Maximum base shear and base overturning demand shall be shown with units.
- A displacement-time graph shall show ground motion and selected floor motion on the same or aligned time axes.
- An acceleration-time graph shall show ground acceleration and selected floor absolute acceleration.
- A drift-time graph shall show the maximum interstory drift and compare it with the entered allowable and collapse limits.
- The final state shall show remaining movement, floor contact or separation, and residual lean or deformation.

### Member strength table
- A table shall list every column, beam, and brace by ID, floor/story, bay, member type, material, section, length, and cost.
- The table shall show axial force, shear force, bending moment, axial stress, bending stress, combined stress, strain, curvature, and buckling utilization.
- Stress and strain values shall include maximum absolute demand and the time or simulation frame at which it occurred.
- Utilization shall be shown as a percentage or ratio for strength, buckling, drift, and connection demand.
- The table shall include member damage state: elastic, yielded, damaged, or failed.
- The table shall highlight the highest-utilization members and identify the governing limit for each.
- Sorting shall be available by utilization, stress, strain, displacement, cost, and damage state.
- Selecting a table row shall highlight the corresponding member in the model and show its end forces and stress state.
- The table shall include an expandable detail view with `N`, `V`, `M`, `A`, `I`, `S`, `E`, yield stress, buckling capacity, and utilization.
- Units shall remain visible in every table header and remain consistent across results.

### Joint strength table
- A table shall list every joint by ID, node location, story, connected member IDs, and connection type.
- The table shall show moment demand/capacity, shear demand/capacity, axial tension and compression demand/capacity, and governing utilization.
- The table shall show joint rotation, slip or displacement, joint stress, joint strain, bolt/weld/rebar demand, and residual deformation.
- The table shall include joint damage state: intact, yielded, damaged, or failed.
- Brittle versus ductile failure mode, residual strength, and stiffness retained after damage shall be displayed.
- Selecting a joint row shall highlight the joint in the animated model and show the forces in each attached member.
- The output shall identify joints that are predicted to yield or fail earlier than the members they connect.
- Fastener or weld capacity shall be reported separately when those controls are entered.

### Stress and strain visualization
- Members and joints shall use a continuous performance color scale:
  - blue or green for low utilization
  - yellow for caution
  - orange for yielding or repairable damage
  - red for high utilization or failure
- The beam/column member colors shall represent maximum combined stress or governing utilization, not just deformation.
- Joint colors shall represent joint utilization and damage state independently from the connected members.
- The model shall provide toggles for stress, strain, utilization, damage, displacement, acceleration, and forces.
- The deformation view shall clearly label any displacement exaggeration and shall not alter actual output values.
- Failure animation shall show yielded or failed members and joints, residual lean, and floor contact or separation.

### Cost and efficiency output
- The cost summary shall show the price of every individual column, beam, brace, and floor member.
- The cost summary shall show the price of every individual joint, including fasteners, plates, welds, reinforcement, and installation when entered.
- The cost summary shall show the price of every floor, including slab, beam, and assigned member costs.
- The cost detail shall show the unit cost and quantity used to calculate each member, joint, and floor price.
- The cost table shall provide expandable member and joint groups and allow sorting from lowest to highest cost or highest to lowest cost.
- The primary total cost shall separate structure, joints, floors, foundation, materials, fabrication, labor, and contingency.
- The app shall display the exact formula-derived total and format the final value as US dollars.
- The output shall display member, floor, foundation, joint, material, fabrication, labor, and total cost.
- The cost panel shall show cost per square foot and cost as a percentage of the entered budget.
- The app shall show remaining budget or over-budget amount.
- Every saved and compared tower shall retain the cost and score measured during the selected simulation.
- The app shall show whether reducing cost introduced new risk and whether extra cost produced a meaningful resilience improvement.

### Upgrade recommendations panel
- Recommendations shall be sorted by predicted score improvement per dollar.
- Each recommendation shall identify the exact member or joint, the issue found, the proposed change, additional cost, and estimated 1–100 score change.
- The panel shall include at least one lower-cost option and one stronger option for the governing weakness.
- Member upgrades shall include section increase, stronger material, brace addition, brace-section increase, shear wall, or base/floor lateral connection change.
- Joint upgrades shall include larger or more fasteners, stronger plate or weld, added reinforcement, and ductile/semi-rigid connection improvements.
- The app shall distinguish stiffness-only changes from strength-and-stiffness changes.
- Every recommendation shall be previewable in the model before it is applied.
- Applying a preview shall recalculate drift, acceleration, member utilization, joint utilization, total cost, and score immediately.
- The app shall warn if an upgrade reduces cost efficiency or merely shifts damage to a weaker member or joint.

### Damage and collapse report
- The damage report shall list the first yielded member, first yielded joint, first failed member, first failed joint, and first floor to exceed the drift limit.
- The report shall include elapsed time and ground-motion state at each event.
- A collapse report shall identify the collapse mechanism and affected components.
- Partial-damage simulations shall show residual deformation and estimate which components require repair or replacement.
- The app shall identify if the tower can resist more motion, equal motion, or less motion after its member and joint states are considered.

### Saved and comparative outputs
- The saved-version panel shall show thumbnail, tower name, notes, ground-motion settings, peak displacement, peak acceleration, peak drift, max member/joint utilization, cost, damage count, and score.
- Saved versions shall include an exact copy of geometry, piece sizes, materials, joints, floor masses, earthquake inputs, and result summary.
- Side-by-side or overlaid comparison shall include score, cost, peak displacement, peak acceleration, peak drift, base shear, member failures, joint failures, and resonance frequency.
- Comparison graphs shall overlay displacement-time, acceleration-time, and drift-time curves for selected towers.
- The app shall show score improvement and cost difference for each paired comparison.
- The stronger design shall be reported for the exact ground motion tested, not presented as universally stronger.

### Live, accessibility, and export outputs
- Results shall update live for valid model changes and shall not keep stale values after an input change.
- Invalid or incomplete inputs shall hide calculated results and show a clear validation message instead.
- Headings, table data, color indicators, and failure states shall have text labels and accessible equivalents.
- The app shall provide an export or copy action for the score summary, member table, joint table, cost, and recommendations.
- Full precision shall be retained in calculations, while display values shall use appropriate units and readable significant figures.

## Look and feel
- The app shall open as a clean engineering simulator with a left model/tool panel, a central tower and ground-motion canvas, and a right properties/results panel.
- The initial view shall show a simple preset tower and a short setup hint rather than an empty workspace.
- The main model shall support an interactive 2D frame view and an optional 3D isometric-style visual view.
- The 2D view shall be the default editing and physics mode. The 3D isometric view shall be a visual projection of the 2D frame and floor data only; it shall not create a separate 3D analysis model or 3D physics equations.
- Rotating or tilting the 3D view shall not change physics inputs or calculated response.
- The workspace shall use a visible grid, floor lines, bay labels, story height, and ground line.
- Columns shall appear vertically, beams horizontally, braces diagonally, floors as slabs, joints as selectable nodes, and floor masses as clearly marked blocks or labels.
- Users shall place pieces by selecting a piece from a visual library and clicking or dragging it onto an allowed grid position.
- The piece library shall offer clear premade choices for common columns, beams, braces, floors, and joints.
- Grid snapping, copy, move, rotate, delete, undo, and redo controls shall be easy to reach above or beside the model.
- Clicking a placed piece shall open a compact properties panel with section type, dimensions, length, thickness, material, and damage state.
- Material choices shall use dropdown menus with short visual descriptions or small diagrams.
- Length, thickness, floor count, bay count, and ground-motion values shall use labeled number boxes or sliders with units shown beside the control.
- Beam and column dimensions shall use short preset dropdowns when appropriate and a custom option for advanced values.
- Floor thickness and floor material shall be adjustable in the floor properties panel or from a floor-level selector.
- Adding a floor shall create and select a new story; removing a floor shall remove only that story after a clear confirmation.
- The left panel shall focus only on building pieces and materials. The right panel shall focus on selected-piece properties or the live simulation results.
- The ground-motion control shall use a compact panel with an earthquake profile, frequency, amplitude/PGA, duration, direction, and damping.
- Ground-motion inputs shall include a short description or tooltip explaining where the value goes and what it changes.
- Frequency shall have a slider and number box with Hz. Amplitude/PGA shall show units and a readable equivalent, such as inches or g.
- Playback controls shall include a prominent circular or square Play button, Pause, Reset, and animation speed controls.
- Pressing Play shall lock or clearly indicate editing changes and begin shaking the ground and tower in real time.
- The simulator shall use the active ground motion to move the tower smoothly while preserving the actual calculated displacement values.
- Optional fast-forward controls shall allow the user to reach high-frequency or long-duration motion quickly.
- The simulation shall display a horizontal ground line that moves with the base motion and a small elapsed-time and ground-motion readout.
- Members that remain elastic shall display in neutral or cool colors. Yielded members may be yellow or orange, and failed members red.
- Joints shall have distinct selectable indicators with intact, yielded, damaged, and failed states.
- When a member or joint breaks, it shall separate, bend, or lose stiffness visually while remaining identifiable.
- Collapse view shall show falling floors, reduced-support positions, and floor contact while clearly labeling the cause of failure.
- The app shall provide a replay control and a timeline slider for inspecting peak movement and failure moments.
- A stress, strain, utilization, displacement, acceleration, or damage overlay selector shall switch the model visualization.
- Displacement exaggeration shall be obvious but shall not change the exact values in readouts or tables.
- Live result badges shall show the current floor displacement, maximum member utilization, maximum joint utilization, and simulation status.
- The app shall keep cost hidden from the editing screen except for the piece library preview and shall not require the user to enter cost values.
- Cost, recommendations, score, detailed table, and saved comparison results shall appear after or beside simulation in a report panel.
- The base interface shall use light, neutral colors with a restrained structural accent color and clear red, orange, yellow, green, and gray state colors.
- Buttons, tabs, dropdowns, inputs, and model handles shall be usable with a mouse and keyboard, with visible keyboard focus.
- Loading, simulation, and reset actions shall provide immediate but unobtrusive status feedback.
- The desktop window shall arrange editing tools, the model view, and results so the tower remains visible while editing.
- The main window shall support resizing; panels and controls shall adapt to available desktop space without hiding essential model or simulation controls.
- Dialog boxes shall confirm deletion, collapse reset, tower reset, and saved-model overwrite actions.
- The app shall preserve valid model edits while changing views and shall not require a rebuild button or page refresh.
- When Play is pressed, the editor panel shall transition into a full-screen or nearly full-screen testing-zone screen.
- The testing zone shall show only the model tower and essential testing information against a clear sky and grassy outdoor background.
- Each simulation run shall be short and complete within 10 seconds of simulation time.
- At the end of playback, the testing zone shall automatically return to the tower editor rather than remain on the animation screen indefinitely.
- A final report summary may appear briefly before or alongside the return transition, but the user shall return to the editable tower as the default behavior.
- The returned editor shall preserve every placed member, joint, floor, material, dimension, and ground-motion setting from the tested tower.
- The same damaged tower state shall remain visible as a visual reference during rebuilding, but damage colors or animation frames shall not be mistaken for newly edited geometry.
- The user shall be able to change an existing member, joint, brace, floor, or material directly after the test without rebuilding the tower from scratch.
- After a test, the app shall offer Clear Damage Reference, Restore Undamaged Geometry, Apply Upgrade, and Save Tower actions in the editor.
- Replay shall remain available from the final test result and shall test the current tower again without closing or resetting the editor history.
- The surrounding area shall remain visually uncluttered: no building tools or editing panels should appear over the model during playback.
- The sky shall have subtle color, cloud, sun, or atmospheric depth, while the ground shall be a clear green test area with a defined shake table or base line.
- The tower shall appear from the exact placed member, floor, brace, joint, and material configuration created in the editor.
- The base shall visibly move horizontally with the selected ground motion while the building moves relative to it.
- A low, simple shake-table platform or labeled base line may be shown, but it shall not add visual clutter or unrelated buildings.
- The testing-zone view shall keep a small time, ground acceleration, displacement, and simulation-status overlay.
- A compact lower playback bar shall include Play/Pause, Replay, timeline, elapsed time, playback speed, camera view, and Exit Simulation.
- The testing zone shall hide editing-only controls while playing and shall show a clear Exit Simulation or Stop button.
- Before Play begins, the app shall show a short launch view with tower preview, entered frequency, amplitude/PGA, duration, and direction.
- During normal playback, the camera shall follow the tower gently while keeping the full building and ground line visible.
- The camera shall switch automatically or manually between full-building, story-close-up, joint-detail, and ground-detail views.
- Damage and collapse shall remain visible in the testing-zone scene with bending, separation, floor contact, falling floors, and residual lean.
- The sky and grass shall remain stationary unless a slow, subtle camera or ground-shake effect is intentionally used.
- At the end of playback, the tower shall hold its residual position briefly for inspection.
- The testing zone shall then leave the full-screen testing view and return to the editable tower workspace with an open result summary.
- Replay shall remain available in the editor for retesting the unchanged tower.

## Validation
- Validation shall use a small set of fast, repeatable tests. No test should require more than 10 simulated seconds or complex manual setup.

### Quick physics baseline: falling block
- Test setup: place one block on the ground with no tower members or external horizontal motion.
- Inputs: block height from the ground `h = 4 ft`.
- Use gravity `g = 32.174 ft/s²`.
- Check that the calculated free-fall time is
  `t_f = sqrt(2h/g) = about 0.50 s`.
- Run the simulation and confirm that the measured fall time is within 10% of the calculated value.
- Confirm that the block stops at ground contact and does not pass through the floor.

### Quick shake baseline: 10-cycle sine motion
- Test setup: use a simple platform or a one-story model with a total floor mass of 1 kip-sec²/ft and one horizontal spring.
- Inputs: sine frequency `f = 1 Hz`, peak amplitude `A = 1 ft`, duration `10 s`, and zero initial displacement and velocity.
- Confirm the table completes 10 cycles and the measured period is approximately `1.00 s`.
- Measure from one positive extreme to the next positive extreme; the time between successive extremes shall be within 5% of `1/f`.
- Confirm the peak base displacement is approximately `1 ft` within 5%.
- Confirm the base motion is back-and-forth, not a one-direction push.

### Quick tower check: no member failure
- Test setup: use the default simple two-story tower with one column and one beam at each story.
- Keep the model within elastic member and joint limits for a low-motion test.
- Inputs: frequency `1 Hz`, PGA `0.10 g`, equivalent displacement amplitude calculated from the entered frequency and PGA, and duration `10 s`.
- Confirm the tower shakes visibly but no member or joint fails.
- Confirm the peak roof displacement, peak floor acceleration, and maximum member and joint utilization are displayed.
- Confirm the 1–100 score is from 75 to 100 and the report does not claim severe damage.

### Quick tower check: member failure
- Test setup: use the default simple two-story tower.
- Apply ground motion with PGA `0.75 g`, frequency `2 Hz`, equivalent displacement amplitude calculated from the entered PGA and frequency, and duration `10 s`.
- Confirm that the simulation identifies at least one yielded member or joint.
- Confirm the model changes color and the member or joint table is updated.
- Confirm that the simulation reports the elapsed time and component that governed the response.
- Confirm that a failed or buckled member remains visibly distinct from an elastic member.

### Quick tower check: joint weakness
- Test setup: use the default two-story tower with a deliberately weak joint and stronger connected members.
- Set one beam-column joint moment capacity to 50% of the default capacity.
- Apply PGA `0.50 g`, frequency `2 Hz`, equivalent displacement amplitude calculated from the entered PGA and frequency, and duration `10 s`.
- Confirm that the weak joint yields or fails before an adjacent equal-strength member.
- Confirm the joint table identifies moment, shear, or rotation as the governing limit.
- Confirm the joint remains selectable and its damage state is visible in the model.

### Quick cost check
- Test setup: use the default single-story tower.
- Add one standard column, one standard beam, one standard floor, and four standard joints.
- Confirm a price is shown for each column, beam, brace when present, floor, and joint.
- Confirm the report separately lists member, joint, floor, labor, material, and foundation cost.
- Confirm the displayed total equals the sum of itemized costs within one cent.
- Confirm changing a section or material updates the cost and total immediately.

### Quick resonance check
- Test setup: use the default one-story simple tower.
- Run a short 10 s frequency sweep from 0.5 Hz to 3.0 Hz.
- Confirm the app identifies natural frequency and period.
- Confirm peak roof displacement is marked at or near a calculated natural frequency.
- Confirm that the frequency-risk display changes between safe, caution, and resonance-risk states.
- Confirm resonance is a reported result and not hidden inside the score only.

### Score and recommendation check
- Run the no-failure and failure tests on the same tower.
- Confirm both 1–100 scores are calculated and the failure run scores lower.
- Confirm the report identifies the governing weakness.
- Confirm at least one lower-cost and one stronger upgrade recommendation are shown.
- Confirm each upgrade lists added cost, predicted benefit, and estimated score change.
- Confirm the original tower is unchanged until the user applies a preview or upgrade.

### Save-and-compare check
- Save the no-failure tower, run the failure test, and save the changed tower.
- Confirm both versions retain ground-motion inputs, geometry, costs, peak results, and score.
- Compare both versions.
- Confirm score difference and cost difference are calculated correctly.
- Confirm the comparison identifies the stronger design only for the ground motion tested.

### Interface and invalid-input checks
- Click Play with an incomplete or out-of-range frequency, amplitude, duration, or floor setup.
- Confirm that the simulation does not start and a clear validation message identifies the invalid input.
- Confirm that stale results and stale damage states are hidden after an input becomes invalid.
- Confirm that Pause freezes motion, Replay restores the initial state, Reset returns the ground and tower to rest, and Exit returns to editing.
- Confirm that Play can be used with the keyboard and that Pause, Replay, Reset, and Exit have visible focus states.
- Confirm the testing zone remains uncluttered and tower motion remains visible at common desktop window sizes.

## Out of scope
- This app does not predict or forecast real earthquake ground motion.
- It tests a tower only against ground motion entered or selected by the user, including sine motion, pulses, frequency sweeps, uploaded acceleration records, or user-entered peak acceleration.
- It does not claim that a particular building will survive a real future earthquake or provide a seismic-code or structural-engineering certification.
- It does not model future fault rupture, probabilistic seismic hazard, earthquake early warning, tsunami loading, or regional ground-motion prediction.
- It is not a substitute for geotechnical surveys, professional seismic analysis, or an engineer's signed design.

## Implementation Steps
1. **Build the Tkinter tower editor.** Create the desktop window, 2D grid, floor and story controls, member library, and click-or-drag placement for columns, beams, braces, joints, and floor masses.
2. **Add editable pieces and properties.** Provide preset materials and member sizes, custom dimensions, floor thickness and area, material dropdowns, joint strength controls, and live piece counts.
3. **Implement cost and saved models.** Assign preset piece prices, calculate itemized and total cost, and add save, duplicate, rename, delete, and compare actions for tower versions.
4. **Build the 2D structural calculation engine.** Assemble floor masses, member stiffness, joint springs, plastic hinges, damping, natural frequencies, ground acceleration, Newmark time integration, member forces, joint forces, stress, strain, and damage.
5. **Create the short simulation testing zone.** Add a 1–10 second sky-and-grass playback scene with ground motion, tower movement, member and joint damage, replay controls, and automatic return to the editable tower.
6. **Add the report and upgrade loop.** Display the 1–100 score, resonance and movement results, member and joint tables, itemized cost, damage report, and lower-cost or stronger redesign recommendations.
