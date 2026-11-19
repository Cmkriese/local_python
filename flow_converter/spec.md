# Specification
# Your App's Name

## Purpose
Calculate the volume of concrete needed for a rectangular slab from its length,
width, and thickness.

## Inputs
The app accepts the following user inputs:

| Input | Units | Reasonable range | Default | Control |
|---|---|---:|---:|---|
| Slab length | Its selected unit | 1–100 ft equivalent | 20 ft | Slider plus number box |
| Slab width | Its selected unit | 1–100 ft equivalent | 10 ft | Slider plus number box |
| Slab thickness | Its selected unit | 0.01–10 ft equivalent | 0.33 ft (4 in) | Number box |
| Length unit | `ft`, `in`, `m`, or `cm` | One option | `ft` | Dropdown |
| Width unit | `ft`, `in`, `m`, or `cm` | One option | `ft` | Dropdown |
| Thickness unit | `ft`, `in`, `m`, or `cm` | One option | `ft` | Dropdown |
| Waste factor | Percent | 0–20% | 10% | Slider |
| Concrete price | USD per cubic yard | $0–$500 per cubic yard | $175 per cubic yard | Number box |

Length, width, and thickness are entered as single numeric values using their
own selected units. Length and width can be adjusted with sliders and
fine-tuned in editable number boxes. Their values should update live as the
sliders move, with keyboard arrow support for accessible adjustments. The
dimension ranges are evaluated after conversion to feet so that the same
physical limits apply regardless of the selected unit. The waste factor
increases the concrete quantity used for the cost estimate.

## Calculations
### Unit conversion

Convert each entered dimension to feet using its selected unit:

- 1 ft = 12 in
- 1 m = 3.28084 ft
- 1 cm = 0.0328084 ft

### Base volume

Calculate the slab volume in cubic feet:

`V_base_ft3 = length_ft × width_ft × thickness_ft`

### Cubic-yard conversion

Convert the base volume to cubic yards:

`V_base_yd3 = V_base_ft3 ÷ 27`

### Waste-adjusted quantity

Convert the waste percentage to a decimal and add it to the base quantity:

`V_waste_yd3 = V_base_yd3 × (1 + waste_percent ÷ 100)`

Round the waste-adjusted quantity upward to the nearest quarter cubic yard:

`V_order_yd3 = ceil(V_waste_yd3 × 4) ÷ 4`

### Estimated cost

Multiply the rounded-up order quantity by the entered concrete price:

`cost = V_order_yd3 × price_per_cubic_yard`

Keep full precision during calculations and display volume and cost rounded to
two decimal places, except that the order quantity is displayed to the nearest
quarter cubic yard. Dimensions and concrete price must be greater than zero.
The waste factor may be between 0% and 20%. Reject invalid inputs with a clear
message instead of calculating.

## Outputs
The app presents each result in a clear, visually engaging layout:

- **Estimated cost:** Displayed as the largest and most prominent result, in
  dollars with two decimal places. The price per cubic yard and rounded order
  quantity appear nearby as supporting information.
- **Concrete quantity:** Display the final order quantity in cubic yards,
  rounded upward to the nearest 0.25 cubic yard.
- **Volume breakdown:** Show the base volume in cubic feet and cubic yards, and
  the waste-adjusted volume in cubic yards, rounded to two decimal places.
- **3D slab diagram:** Show a clean, responsive rectangular-prism model labeled
  with the slab's length, width, and thickness. The model updates when the
  dimensions change and uses the selected dimension units.
- **Input summary:** Show the selected dimensions, their units, waste factor, and
  concrete price per cubic yard.
- **Validation messages:** Clearly identify blank, nonnumeric, out-of-range, or
  otherwise invalid inputs instead of displaying calculated results.

The final cost uses the rounded-up order quantity multiplied by the concrete
price per cubic yard.

## Look and feel
The page title at the top is **Concrete Slab Calculator**. A clear instruction
under the title reads **Enter dimensions here**.

The inputs are organized in a logical vertical order:

1. Length
2. Width
3. Thickness
4. Length unit
5. Width unit
6. Thickness unit
7. Waste factor
8. Concrete price per cubic yard

The results appear below the input area. The 3D slab diagram appears below the
results. On mobile screens, the title, inputs, results, and diagram stack
vertically in the same order so that no horizontal scrolling is required.

## Validation
### Rectangular slab unit-conversion test

Inputs:

- Length: 1 ft
- Width: 2 ft
- Thickness: 6 in
- Waste factor: 0%
- Concrete price: $175 per cubic yard

Hand calculation:

- Convert thickness: 6 in = 0.5 ft
- Base volume: `1 ft × 2 ft × 0.5 ft = 1 ft³`
- Base volume in cubic yards: `1 ÷ 27 = 0.037037... yd³`
- Waste-adjusted volume: `0.037037... yd³`
- Order quantity rounded upward to the nearest 0.25 yd³: `0.25 yd³`
- Estimated cost: `0.25 × $175 = $43.75`

Expected displayed results:

- Base volume: `1.00 ft³` and `0.04 yd³`
- Waste-adjusted volume: `0.04 yd³`
- Order quantity: `0.25 yd³`
- Estimated cost: `$43.75`

## Out of scope
The app will not calculate concrete for slabs that are not rectangular.
It will not allow users to select, change, or otherwise modify the type or mix
of concrete.