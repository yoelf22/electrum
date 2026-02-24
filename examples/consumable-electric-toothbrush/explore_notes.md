# Exploration Notes

## Product Summary

A consumable electric toothbrush targeting the consumer market at sub-$5 retail and 100k+ unit volumes. The brush uses a vibration motor to drive bristle oscillation and runs until its non-rechargeable battery is depleted — then the user discards it and opens a new one. No wireless connectivity, no display, no app. The design goal is the simplest possible electric toothbrush: battery + switch + motor + sealed plastic handle. Target battery life is ~350 minutes of motor runtime with a flat discharge curve and sudden cutoff (no gradual fade).

## Product Classification

**Electromechanical.** The product is a motor in a sealed plastic tube. The core function is mechanical: vibration motor oscillates bristles to clean teeth. The enclosure is the structure. The product operates in a wet oral environment. With NFC removed, there is no software layer — the "electronics" may reduce to a switch, a MOSFET, and possibly a simple timer circuit (555 or RC) for a 2-minute auto-shutoff. No MCU is required unless a timer or usage indicator is added.

**Note on software augmentation:** With NFC removed, this product has no software component. The electromechanical workflow phases (physical architecture, component arrangement, structural design) remain fully applicable. Firmware/app/cloud sections will be marked N/A.

## HW/SW Boundary Analysis

| Domain | Hardware | Firmware | Software |
|--------|----------|----------|----------|
| Brushing action | Vibration motor, battery, switch | N/A | N/A |
| Timer (optional) | 555 timer IC or RC delay circuit | N/A | N/A |
| Power | Primary cell (non-toxic chemistry) | N/A | N/A |
| User feedback | Motor vibration = "on" feedback | N/A | N/A |
| Water protection | Sealed enclosure, ultrasonic welding | N/A | N/A |

**There is no HW/SW boundary.** This is a purely electrical/mechanical product. All "intelligence" is in passive analog circuits.

## Physical Architecture

### Physical Function
Vibrates the brush head via an eccentric rotating mass (ERM) motor to produce oscillating bristle motion at ~150–200 Hz. The vibration mechanically disrupts dental plaque and drives toothpaste slurry between teeth. The motor runs at a fixed speed — no variable modes, no pulsing patterns (those would require an MCU).

### Mechanical Subsystem
- **Motor:** Miniature cylindrical ERM motor (~6mm × 12mm) with eccentric mass. Proven at 1.5V single-cell operation (Oral-B Pulsar reference). At volume, $0.08–0.15.
- **Transmission:** Motor connects to one half of a **split bristle head** — the moving half oscillates relative to the fixed half, concentrating vibration at the bristles rather than shaking the entire handle. This is the Oral-B Pulsar architecture.
- **Bristle head:** Split-head design. Bristles are **insert-molded** during the first injection shot (inserted into the mold cavity, plastic injected around the bristle bases), then **trimmed** to profile after demolding. One half of the head is rigidly connected to the handle body; the other half is mechanically coupled to the motor shaft/eccentric, allowing it to oscillate.

### Structure and Load Paths
- **Dual-injection (overmolded) construction:**
  - **First shot:** Rigid PP or ABS main body — forms the structural handle, bristle head halves, motor pocket, and battery tube. Bristles are insert-molded in this shot.
  - **Assembly phase:** Motor, wiring, switch, and battery inserted into the rigid body.
  - **Second shot:** Soft TPE (thermoplastic elastomer) overmolded onto the assembly — seals all penetrations, provides grip texture, and encapsulates the electronics.
- Motor reaction forces (vibration) absorbed by the rigid first-shot body and the user's grip.
- Battery held in a molded tube within the handle, closed by a **screw cap with O-ring** at the base (allows factory battery insertion after molding).
- No separate chassis — the first-shot rigid body IS the structure.

### Working Media and Interfaces
- **Wet environment:** Water, toothpaste (mildly abrasive), saliva. Exposed to tap water rinse after each use.
- **Sealing target:** IPX5 (splashing water from all directions). Not designed for prolonged submersion.
- **Sealing method:** Dual-injection overmolding. The TPE second shot seals around all component interfaces — no separate gaskets or adhesive needed for the main body. The bristle bases are sealed by the first injection shot (insert molding).
- **Battery compartment:** Screw cap with O-ring at the handle base. This is the only user-accessible seal point (for factory battery insertion; not intended for user replacement on a consumable product, but the O-ring provides reliable sealing).
- **Split head hinge/joint:** The moving half of the bristle head pivots relative to the fixed half. The joint between them is a potential ingress point — the TPE overmold must seal this interface while still allowing oscillation. Oral-B Pulsar solves this with a flexible TPE boot around the joint.

### Physical-Electronic Interface
- **Motor drive:** Direct battery → latching push-button → motor. No MOSFET, no IC.
- **Power button:** Latching push-on/push-off mechanism. Sealed by the TPE overmold layer.
- **Motor-to-head coupling:** Motor shaft/eccentric connects mechanically to the moving half of the split bristle head via a rigid plastic linkage molded into the first shot.
- **No sensors, no feedback loops, no encoders.** The motor is uncontrolled open-loop.

## Battery Chemistry — RESOLVED

**Requirements:** ~350 min motor runtime, months-long shelf life once opened, non-toxic, sudden depletion, low cost.

**Decision: Alkaline cell.** Shelf-stable for 5–10 years sealed, months of active life once in use. The discharge curve slopes gradually, but for a motor load this produces *functionally sudden* depletion: the motor runs at full strength down to ~1.1V, then rapidly weakens below the stall threshold. From the user's perspective, it works one day and doesn't the next.

Assuming motor draws **60–100 mA at 1.5V**:

| Cell | Dimensions | Capacity | Est. Runtime @80mA | Cost @100k | Fit |
|------|-----------|----------|---------------------|------------|-----|
| **AAAA (LR61)** | 8.3mm × 42mm | 500–600 mAh | **375–450 min** | $0.06–0.12 | Slim handle, hits 350-min target |
| AAA (LR03) | 10.5mm × 44mm | 1000–1200 mAh | 750–900 min | $0.05–0.10 | Slightly thicker, 2× overshoot on runtime |
| AA (LR6) | 14.5mm × 50mm | 2500–2800 mAh | 1875–2100 min | $0.06–0.10 | Chunky handle, massive overkill |

**Best candidate: AAAA (LR61).** 8.3mm diameter fits a slim toothbrush handle (~12–14mm OD with shell). ~500 mAh capacity delivers ~375 min at 80 mA — right at target. Alkaline chemistry (zinc-manganese dioxide) is non-toxic. Shelf life 3+ years.

**Fallback: AAA.** If a AAAA cell is harder to source at volume or costs more, AAA is universally available and cheaper, at the cost of a thicker handle (needs ~15–17mm OD). Runtime overshoots to ~900 min but that just means the brush lasts longer — not a problem for a consumable.

## Timer — RESOLVED

**No timer.** Simple momentary push-button: press to turn on, press again to turn off. No 555 circuit, no auto-shutoff. If the user forgets to turn off, the battery drains — acceptable for a consumable product. Eliminates the only remaining IC from the BOM.

## Relevant Skill Areas

From the 16 skills map areas, ranked by importance:

1. **Cost & BOM Awareness (#15)** — DOMINANT. Sub-$5 retail implies ~$0.80–1.50 BOM target. Every fraction of a cent matters.
2. **Mechanical & Industrial Design (#4)** — The product IS the mechanical design: handle ergonomics, bristle tufting, motor pocket, battery cradle, ultrasonic weld line, button seal, water resistance.
3. **Manufacturing & Provisioning (#14)** — High-volume automated assembly. Cycle time per unit directly affects cost. Ultrasonic welding, motor insertion, battery insertion, bristle tufting.
4. **Sensors & Actuators (#10)** — Motor selection at extreme cost targets: vibration amplitude, current draw, voltage match to battery chemistry.
5. **Power Management (#9)** — Battery sizing for 350-min target. No active power management — just matching cell capacity to motor draw.
6. **Regulatory & Compliance (#12)** — No RF (NFC removed), so no FCC/CE radio testing. Still needs: CE marking (general product safety), RoHS, material safety for oral use (FDA food-contact or equivalent), battery transport (UN38.3 exemption for small cells), WEEE (disposal).

**Not relevant:** Electrical HW (#3, no PCB needed in simplest design), Embedded SW (#5), Connectivity (#6), Companion App (#7), Cloud (#8), Security (#11), User Interaction (#13, single button only), Testing (#16, simplified — no firmware to test).

## Key Unknowns and Questions

1. **AAAA vs. AAA cell.** AAAA gives a slimmer handle but is less commonly sourced at volume. AAA is ubiquitous and cheaper but makes the handle thicker. Needs supplier quotes.
2. **Handle form factor.** The TPE overmold enables ergonomic shaping (soft-touch grip zones) at low marginal cost. How much contouring vs. simple cylindrical?
3. **Overmold tooling investment.** Dual-injection molds cost $15k–25k vs. $3k–8k for single-shot. What minimum order quantity justifies this?
4. **Battery cap design.** Screw cap with O-ring (proven, reliable) vs. press-fit cap with interference seal (cheaper, less reliable). Which approach?
5. **Split head pivot mechanism.** How is the moving bristle half coupled to the motor? The pivot point geometry, range of motion, and TPE boot seal all affect cleaning effectiveness and durability.

## Initial Risk Areas

| Risk | Severity | Likelihood | Notes |
|------|----------|------------|-------|
| Overmolding tooling cost | High | Medium | Dual-injection molds are 2–3× the cost of single-shot molds ($15k–25k). Amortization needs high volume to stay under BOM target. |
| Split head joint seal durability | Medium | Medium | The TPE boot around the oscillating joint degrades with daily wet use over ~90 days. Must validate. |
| User forgets to turn off → premature battery drain | Medium | High | No auto-shutoff; mitigated by packaging instructions and handle feel (vibration is obvious) |
| BOM exceeds target at initial volumes | Medium | Medium | Overmolding + O-ring cap + insert-molded bristles adds process cost. Need 100k+ to amortize tooling. |
| AAAA cell sourcing at volume | Medium | Medium | Less common than AAA; may need to fall back to AAA (thicker handle) |

## Suggested Focus for High-Level Design

1. **Motor-battery pairing.** Identify a specific 1.5V-rated ERM motor and confirm vibration amplitude is adequate for bristle cleaning at the alkaline cell's end-of-life voltage (~1.1V).
2. **BOM bill-up.** List every physical component with cost estimate. Target: $0.30–0.60 total BOM for the simplest possible design (no PCB, no IC).
3. **Sealing strategy.** Three ingress points: shell ultrasonic weld, bristle head penetration, power button. Define the approach and cost for each.
4. **Handle geometry.** Cylindrical vs. contoured, driven by battery cell choice (AAAA vs. AAA) and ergonomic minimums.
5. **Switch mechanism.** Latching push-button vs. slide switch — trade-off between water sealing and UX.
