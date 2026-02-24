# Component Arrangement — Consumable Electric Toothbrush

## Component Inventory

**Electrical:**
1. AAA alkaline cell (⌀10.5mm × 44.5mm)
2. Battery spring contact (negative terminal, base end)
3. Battery contact plate (positive terminal, top end)
4. Latching push-button switch (~6mm × 6mm)
5. Wiring — 2 wires (battery→switch, switch→motor)

**Mechanical — Drive:**
6. Cylindrical ERM motor (⌀6mm × 12mm)
7. Eccentric mass (pressed on motor shaft)
8. Linkage arm — rigid PP, motor eccentric → moving head half (~15mm)

**Mechanical — Bristle Head:**
9. Fixed bristle half (with ~15–20 tufts, insert-molded)
10. Moving bristle half (with ~15–20 tufts, insert-molded)
11. Pivot joint (living hinge or pin) between head halves

**Enclosure / Structure:**
12. Rigid PP body — 1st injection (handle tube, motor pocket, battery tube, head structure)
13. TPE overmold — 2nd injection (grip texture, button membrane, head joint boot)
14. Battery cap (threaded PP)
15. O-ring (battery cap seal)

## Selected Views

- **Longitudinal cross-section** — primary view. The toothbrush is a cylindrical object with a dominant long axis (~160mm). This view reveals the full stacking order of all internal components from base to tip.
- **Transverse cross-section at head** — secondary view. Shows the split-head mechanism and pivot relationship between fixed and moving halves.

## Arrangement Diagram

**Selected: Option A — Axial Motor**

![Arrangement cross-section](arrangement_options.png)

Motor cylinder oriented along the handle axis (left diagram). Stacking from base to tip:

```
BASE (bottom)
  │
  ├── Battery cap (threaded PP) + O-ring seal
  │
  ├── − spring contact
  │
  ├── AAA alkaline cell (⌀10.5 × 44.5mm)
  │      ← largest component, fills most of handle length
  │
  ├── + contact plate
  │
  ├── wire run (~5mm)
  │
  ├── Latching push-button switch
  │      ← positioned at thumb reach, mid-handle
  │      ← sealed by TPE overmold membrane
  │
  ├── wire run (~10mm)
  │
  ├── ERM motor (⌀6 × 12mm, axial)
  │      ← motor shaft points toward head
  │
  ├── Eccentric mass (on shaft tip)
  │
  ├── Linkage arm (~15mm rigid PP)
  │      ← connects eccentric to moving head half
  │
  ├── TPE boot (dynamic seal around head joint)
  │
  ├── Pivot (living hinge or pin)
  │
  ├── Fixed bristle half │ Moving bristle half
  │      ← split head, both with insert-molded tufts
  │
  └── Bristle tips
TIP (top)
```

## Arrangement Rationale

| Placement Decision | Reason |
|-------------------|--------|
| Battery at the base | Heaviest component low = natural balance point when held. Also allows base-access battery cap without disturbing the head-end seals. |
| Switch at mid-handle (thumb position) | Ergonomic — natural thumb resting point when gripping the handle. Between battery and motor so wiring runs are short in both directions. |
| Motor above switch, below head | Minimizes linkage length to the moving head half (~15mm). Vibration source close to where it's needed. Motor pocket sits in the neck transition zone. |
| Motor axial (shaft along handle) | Keeps the neck slim (~15mm, same as handle body). Avoids a bulge. Simpler mold geometry — the motor pocket is a straight cylindrical bore. |
| Linkage arm from eccentric to head | Converts the motor's rotary eccentric motion into oscillating motion at the split head. Short arm = efficient transfer, minimal energy loss. |
| TPE boot at head joint | Seals the dynamic pivot between fixed and moving head halves. This is the most critical seal — it must flex millions of cycles while keeping water out of the motor cavity. |
| Battery cap with O-ring at base | Only access point. Factory-sealed after battery insertion. Threaded engagement + O-ring = reliable static seal. Located at the furthest point from water exposure (base of handle, not the head). |
| Bristles insert-molded in 1st injection | Seals each tuft base during molding — no secondary sealing step needed. Both head halves get bristles in the same shot. |

## Spatial Constraints Identified

These constraints must be respected in the system description:

1. **Motor-to-head linkage clearance:** The linkage arm passes through the neck section. The PP body must have a channel or slot for the arm to oscillate within. Minimum clearance: ~1mm per side.
2. **Battery tube inner diameter:** Must be ≥10.8mm (AAA cell is 10.5mm + tolerance) for easy factory insertion. Spring contact must provide ~2mm compression for reliable electrical contact.
3. **Switch actuation through TPE:** The TPE overmold membrane must be thin enough at the button location (~1mm) to transmit finger press to the latching switch underneath, while thick enough everywhere else for grip and sealing.
4. **Motor pocket concentricity:** The motor must be centered in the handle cross-section so the eccentric doesn't hit the inner wall during rotation. With ⌀6mm motor in ~⌀13mm internal cavity, there's ~3.5mm radial clearance — adequate.
5. **TPE boot flex range:** The boot must accommodate ~1–2mm of oscillation at the head pivot without restricting motion or fatiguing. Boot wall thickness ~0.8–1.2mm, Shore A 40–50 for flexibility.
6. **Wire routing:** Two wires run from battery area through the switch to the motor. Must be routed along the inner wall of the PP body with strain relief at solder points. Total wire length ~60–70mm.
7. **O-ring groove dimensions:** Standard AS568 groove for the battery cap. O-ring ID matches cap outer thread diameter. Groove depth and width per standard for static radial seal.

## Key Dimensions

| Dimension | Value | Notes |
|-----------|-------|-------|
| Overall length | ~160mm | Battery (44.5) + switch zone (10) + motor zone (18) + linkage (15) + head (30) + transitions |
| Handle diameter (grip zone) | ~15–16mm | AAA (10.5) + PP wall (1.5×2) + TPE (0.5×2) |
| Neck diameter (motor zone) | ~15mm | Motor (6) + PP wall (1.5×2) + clearance (2×2) + TPE (0.5×2) |
| Head width | ~12mm | Standard toothbrush head width |
| Head length | ~25–30mm | Split into two ~12–15mm halves |
| Battery cap diameter | ~16mm | Matches handle base, with thread engagement |
| TPE overmold thickness | 0.5–1.5mm | Thinner at button (1mm), thicker at grip zones (1.5mm) |
