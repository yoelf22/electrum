# Component Arrangement — Bubbler

## Component Inventory

1. **Wand loop** — 160mm Ø, flexible (bends flat against vat bottom during dip), attached to wand arm
2. **Wand arm** — ≤30mm rigid rod, connects loop to rotating shaft
3. **Rotating shaft** — ~180mm span across vat width, axis sits above vat rim +5mm clearance, ~175° rotation range (90° upright to 265° dip), shaft on right side next to air duct protrusion
4. **Open vat** — oval, 200mm × 170mm internal, 20mm deep, removable shallow tray
5. **Blower fan** — centrifugal/radial, ~40×40×10mm, flat profile, optimized for pressure
6. **Air duct (L-bent horn)** — vertical segment from fan, 90° bend to horizontal exit; round outlet Ø40mm, concentric with and flush to upright loop
7. **Geared DC motor** — small (~15×10×8mm) with high-ratio gear train (~100:1), drives shaft rotation
8. **Strain gauge** — ~10×5mm foil gauge bonded near shaft bearing/pivot
9. **HX711 ADC** — integrated on main PCBA
10. **Main PCBA** — ~50×35mm; MCU (Cortex-M0), HX711, MOSFET fan driver, H-bridge pivot driver, voltage regulator
11. **Battery holder (4×AA)** — ~58×58×15mm (2×2 flat), near base level inside U-rim tall side, aligned with long edge
12. **User controls** — power button + mode selection, style TBD
13. **Status LEDs** — 3–5× 3mm LEDs
14. **Enclosure: Base** — flat plate, footprint ~215×206mm, with 4× leveling rubber feet
15. **Enclosure: Inverse-U rim** — asymmetric: tall on one long side (~80mm+ above vat rim, houses duct + PCBA + battery; motor + fan mounted on rim, wired to PCBA), minimal elsewhere (~15mm, holds shaft bearings)
16. **Enclosure: Vat** — shallow oval tray (200×170mm internal, 20mm deep), sits on top of base within U-rim

## Selected Views

- **Side cross-section** (looking along the 200mm long axis): Loop and wand arm appear edge-on as a vertical line in blow position. Shows the tapered protrusion on the right side (wide at base, narrows to duct exit + 10mm radial clearance). Shaft pivot on the right, arm rotates 175° from 90° (upright, blow) to 265° (down-left, dip into vat). Reveals the asymmetric U-rim profile and internal component stacking (battery near base, PCBA above, motor at shaft height, fan near top).
- **Front view** (looking along the airflow axis, into the loop): Shows the concentric alignment of the Ø40mm duct exit inside the 160mm loop. Shows the shaft spanning the vat width with bearings at both ends.

## Arrangement Diagram

![Arrangement](arrangement_options.png)

## Arrangement Rationale

| Placement | Reason |
|-----------|--------|
| Vat on top, open | Gravity keeps solution in place; easy to fill and inspect level; loop dips down into it naturally |
| Shaft axis just above vat rim | Minimal clearance allows the arm to swing freely between dip (into vat) and blow (above vat) positions without the shaft interfering with the vat walls |
| Loop above vat in blow position | Bubbles inflate upward and outward, away from the machine — no interference with structure |
| Flexible loop | Bends flat against vat bottom during dip for maximum film coverage and thick coating; springs back to circular when upright |
| Battery near base, aligned with long edge | Low center of gravity for stability; long-edge alignment fits 2×2 AA holder within rim depth |
| PCBA aligned with long edge above battery | Short wire runs to battery below and connectors to motor/fan mounted on rim above |
| Motor + fan mounted on rim, wired to PCBA | Mechanical components fixed to structural rim; electrical connection via JST cables to PCBA — separates mechanical mounting from electronics |
| Tapered protrusion (tall side) | Tapers from full base width at bottom to 60mm (duct Ø40mm + 10mm clearance each side) at duct exit — houses battery, PCBA, motor, and fan while minimizing visual bulk at the top |
| L-bent air horn | Allows a flat centrifugal fan (horizontal) to deliver air horizontally through the vertical loop; the 90° bend fits within the U-rim structure; round exit disperses air evenly |
| Duct exit concentric with loop | Air passes through the center of the soap film, inflating it symmetrically into a sphere |
| Motor on shaft end inside U-rim | Protected from splashes; gear train provides slow, smooth rotation; shaft transmits torque across vat width |
| Strain gauge near shaft bearing | Picks up torsional/bending force from wand arm during inflation; close to pivot = maximum signal; inside dry zone |

## Spatial Constraints Identified

- **Shaft bearing alignment:** Both bearings must be coaxial across ~180mm span. U-rim mounting points must maintain alignment after assembly.
- **Duct exit alignment:** The Ø40mm duct exit must be centered on the loop center when the arm is in blow position. Positional tolerance ±5mm.
- **Vat clearance for loop rotation:** The vat's 200mm long axis accommodates 5mm + 30mm (arm) + 160mm (loop) + 5mm = 200mm exactly. No excess — tight fit ensures compact product.
- **Wet/dry boundary:** The shaft penetrates from the wet zone (vat) into the dry zone (U-rim). Shaft seal or labyrinth required at both bearing points.
- **Fan intake:** The centrifugal fan needs an air intake on the U-rim exterior. Must be positioned to avoid drawing in soap spray.

## Key Dimensions

| Dimension | Value |
|-----------|-------|
| Overall footprint | ~215 × 206mm |
| Overall height (to loop top) | ~250mm (base to top of upright loop) |
| U-rim tall side height | ~80mm above vat rim |
| U-rim minimal height | ~15mm above vat rim |
| Vat internal | 200 × 170mm oval, 20mm deep |
| Loop diameter | 160mm |
| Wand arm length | 30mm |
| Shaft span | ~180mm |
| Base width (short axis) | ~206mm (vat 176mm + motor 15mm + clearances 15mm) |
| Duct exit diameter | 40mm |
| Rubber leveling feet | 4×, adjustable or press-fit, on base corners |
