# System Description: Consumable Electric Toothbrush

| Field | Value |
|-------|-------|
| Version | 0.1 |
| Date | 2026-02-24 |
| Author | Electrum workflow |
| Status | Draft |
| Related docs | explore_notes.md, high_level_design.md, component_arrangement.md |

---

## 1. Product Vision and Context

**Product statement:**
For cost-conscious consumers, the Consumable Electric Toothbrush is a disposable vibrating toothbrush that works until its battery dies — then you throw it away and open a new one. Unlike the Oral-B Pulsar ($8–12, non-replaceable battery, pretends to be reusable), it is honestly designed as a consumable from day one, at a fraction of the price ($3–5 retail).

**Problem:**
The Oral-B Pulsar dominates the "disposable electric toothbrush" category at $8–12 retail. It uses a non-replaceable AA battery and a sealed housing — when the battery dies, the user discards the whole unit. But the price and marketing position it as semi-permanent, creating dissonance when it dies. A purpose-built consumable at $3–5 with ~90 days of runtime would undercut the Pulsar on price while being transparent about its disposable nature.

**Deployment context:**
- Environment: Indoor — bathroom, hotel, travel
- Setting: Home, travel, hospitality
- User type: Consumer — mass market
- Installation: None — open package, remove any battery seal tab, press button, brush
- Expected lifespan: ~90 days (350 min motor runtime at 2×/day, 2 min/session)

---

## 2. User Scenarios

### Scenario 1: Daily Brushing
**Persona:** Sarah, 28, budget-conscious, uses manual toothbrushes but wants an upgrade.
**Situation:** Morning routine, standing at the bathroom sink.
**Action:** Picks up the toothbrush, applies toothpaste, presses the button. Motor vibrates. Brushes for ~2 minutes. Presses button again to stop. Rinses brush under tap water.
**Outcome:** Clean teeth with powered vibration. Brush goes back in the cup holder. No charging cradle, no app, no thinking.

### Scenario 2: First Use — Unboxing
**Persona:** Any buyer.
**Situation:** Purchased a single brush in blister pack from a drugstore shelf.
**Action:** Opens blister. Picks up brush. Presses button. Brush vibrates immediately — the alkaline battery is pre-installed and has years of shelf life. Starts brushing.
**Outcome:** Zero setup. No pull-tabs, no charging, no pairing. Working electric toothbrush in under 5 seconds from opening the package.

### Scenario 3: End of Life
**Persona:** Sarah, ~3 months later.
**Situation:** Presses the button. Motor barely vibrates or doesn't start — the alkaline cell has dropped below the motor's stall voltage.
**Action:** Sarah recognizes the brush is done. Discards it in household waste. Opens a new one from a multi-pack she bought.
**Outcome:** Clear, unambiguous end-of-life signal (motor stops). No gradual degradation anxiety. No "is the battery low or is it broken?" confusion — it either vibrates or it doesn't.

### Scenario 4: Travel Use
**Persona:** Mike, 40, business traveler.
**Situation:** Packing for a 5-day trip. Doesn't want to bring a charger for his Oral-B iO.
**Action:** Grabs a consumable brush and throws it in his toiletry bag. Uses it during the trip. Discards it at the hotel on departure or brings it home.
**Outcome:** No charger, no charging case, no worry about battery dying mid-trip. Lighter packing.

### Scenario 5: Left On Accidentally
**Persona:** Sarah's child, 6 years old.
**Situation:** Finishes brushing but forgets to press the button to turn off. Motor keeps running.
**Action:** Motor runs until parent notices the buzzing and turns it off. If no one notices for hours, the battery drains faster than normal.
**Outcome:** Shortened battery life but no safety hazard. No overheating (motor draws <100 mA at 1.5V = <150 mW — negligible thermal load). Worst case: brush lasts 2 months instead of 3.

---

## 3. System Architecture

```
                    Consumable Electric Toothbrush
                    ═══════════════════════════════

    ┌──────────┐     ┌──────────────┐     ┌──────────────┐
    │ AAA      │────→│ Latching     │────→│ Cylindrical  │
    │ Alkaline │ DC  │ Push-Button  │ DC  │ ERM Motor    │
    │ 1.5V     │     │ Switch       │     │ ⌀6×12mm      │
    └──────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                                           ┌──────┴───────┐
                                           │ Eccentric    │
                                           │ Mass         │
                                           └──────┬───────┘
                                                  │ linkage arm
                                           ┌──────┴───────┐
                                           │ Split Bristle │
                                           │ Head (moving  │
                                           │ half oscillates)│
                                           └──────────────┘

    Signal path: Battery ──DC──→ Switch ──DC──→ Motor
    Force path:  Motor ──rotation──→ Eccentric ──vibration──→ Linkage ──oscillation──→ Bristles
    Seal zones:  [1] Bristle insert-mold  [2] TPE overmold  [3] Head joint boot  [4] O-ring cap
```

**Architecture narrative:**

This is a purely electrical/mechanical product with no microcontroller, no firmware, and no wireless connectivity. The entire electrical system is a series circuit: alkaline cell → latching switch → ERM motor. There is no PCB.

The mechanical system converts the motor's rotary eccentric vibration into oscillating bristle motion via a rigid plastic linkage arm connecting the motor's eccentric mass to the moving half of a split bristle head. The fixed half of the head is rigidly part of the handle body; the moving half pivots at a living hinge or pin joint, oscillating ~1–2mm at the motor's rotation frequency (~150–200 Hz).

Water protection is achieved through four seal zones: (1) insert-molded bristle bases sealed in the 1st injection shot, (2) TPE overmold encapsulating the body and sealing all through-wall penetrations, (3) a TPE boot sealing the dynamic head joint while allowing oscillation, and (4) a threaded battery cap with O-ring at the handle base.

---

## 4. Subsystem Descriptions

### 4.1 Hardware Subsystem

**MCU / SoC:** N/A — no microcontroller. No PCB. All "logic" is mechanical (latching switch).

**Sensors:** None.

**Actuators:**

| Actuator | Function | Interface | Key Spec |
|----------|----------|-----------|----------|
| Cylindrical ERM motor | Vibrate bristle head for dental cleaning | Direct DC from battery via switch, 2 solder joints | Rated voltage 1.5V (range 1.0–1.8V), current 60–100 mA, vibration amplitude ≥0.8G at shaft, ⌀6mm × 12mm, eccentric mass pressed on shaft |

Candidate motors (COTS, Alibaba/motor catalog):
- **JMM-1406** (Jinlong Machinery): ⌀6mm × 14mm cylindrical ERM, rated 1.5V, 80 mA, 10,000 RPM, $0.10–0.15 at 10k+ qty
- **FM-1406** (Fulling Motor): ⌀6mm × 12mm, rated 1.5V, 65 mA, 12,000 RPM, $0.08–0.12 at 10k+ qty

Both are commodity motors available from multiple Shenzhen suppliers. The key spec to validate on samples: vibration amplitude at 1.1V (end-of-life battery voltage). If vibration is too weak below 1.2V, the motor must be specified for a lower minimum operating voltage.

**Physical UI elements:**
- Buttons: 1× latching push-button (push-on / push-off). COTS 6mm × 6mm through-hole or SMD pushbutton with built-in latching mechanism. Sealed by TPE overmold membrane.
- LEDs: None.
- Display: None.
- Other: None.

Candidate switch:
- **Standard 6×6mm latching push-button** (various suppliers): Self-latching alternate-action mechanism. Push once = circuit closed (motor on). Push again = circuit open (motor off). $0.02–0.04 at 10k+ qty. Rated 50mA @ 12V DC — adequate for 80–100 mA motor current at 1.5V.

**PCB strategy:** No PCB. Point-to-point wiring:
- Wire 1: Battery positive terminal → switch terminal 1 (soldered or crimped)
- Wire 2: Switch terminal 2 → motor terminal 1 (soldered)
- Motor terminal 2 → battery negative spring contact (via wire or direct spring-to-tab contact)

Total: 2 wires (~30 AWG stranded, silicone-insulated), 3–4 solder joints. Assembly time: ~10 seconds per unit with jig-assisted manual soldering or automated wire bonding.

### 4.2 Firmware Subsystem

**N/A.** No microcontroller, no firmware, no software of any kind. The product is purely electromechanical.

### 4.3 Mobile / Companion App Subsystem

**N/A.** No app. No wireless connectivity.

### 4.4 Cloud / Backend Subsystem

**N/A.** No cloud. No accounts. No data.

### 4.5 Mechanical Subsystem

This is the core of the product. The mechanical design determines cleaning effectiveness, water resistance, durability, and manufacturing cost.

#### 4.5.1 Split Bristle Head

The brush head is split longitudinally into two halves:
- **Fixed half:** Rigidly part of the PP handle body (1st injection). Contains ~15–20 bristle tufts insert-molded into the head surface.
- **Moving half:** A separate PP piece that pivots relative to the fixed half. Contains ~15–20 bristle tufts insert-molded. Connected to the motor via the linkage arm.

**Pivot mechanism:** Living hinge molded into the 1st injection shot. The hinge is a thin PP section (~0.3mm) connecting the two halves, allowing ~1–2mm of oscillation at the bristle tips. PP is well-suited for living hinges (excellent fatigue life — hundreds of millions of cycles).

Alternative: Pin pivot with a molded-in ⌀1mm PP pin. Stronger but adds mold complexity (side action or assembly step). Living hinge is preferred for single-piece moldability.

**Bristle specification:**
- Material: Nylon PA-612 (standard oral care grade, soft to medium stiffness)
- Tuft diameter: ~1.5mm (standard)
- Tuft count: ~35 total (17–18 per half)
- Bristle length: ~10mm exposed above head surface
- Bristle end rounding: chemically rounded tips (standard post-mold process)
- Insert molding: bristle tufts are placed in the mold cavity before the 1st injection shot. PP flows around the bristle bases, mechanically locking and sealing them.

#### 4.5.2 Motor-to-Head Linkage

A rigid PP arm (~15mm long, ~2mm × 3mm cross-section) connects the motor's eccentric mass to the moving head half. The arm is molded as part of the moving head half in the 1st injection shot, extending down through the neck into the motor pocket area.

The arm has a socket or clip feature at its lower end that engages the motor's eccentric mass or a stub on the motor shaft. When the motor spins, the eccentric creates a radial force oscillation that the arm converts to linear oscillation at the bristle head (the arm constrains the motion to one axis via the living hinge pivot).

#### 4.5.3 Motor Mounting

The motor press-fits into a cylindrical pocket molded into the PP body (1st shot). Pocket inner diameter: ⌀6.1mm (motor OD is ⌀6.0mm ± 0.05mm). Pocket depth: 12.5mm. The motor is retained by friction fit plus the TPE overmold encapsulating the pocket area.

Motor leads (2 wires, ~20mm pigtail) exit the pocket toward the switch mounting area.

### 4.6 Structural Design

#### Construction Method: Dual-Injection Overmolding

**1st shot (rigid PP):**
- Material: Polypropylene, injection-molding grade (e.g., Braskem CP 442XP or equivalent)
  - PP is chosen over ABS for: lower cost ($0.80/kg vs $1.50/kg), FDA food-contact compliance (21 CFR 177.1520), excellent living hinge fatigue life, good chemical resistance to toothpaste, and strong TPE adhesion in overmolding
- Forms: Handle tube, battery cradle, motor pocket, bristle head (both halves), living hinge, linkage arm, switch pocket, battery cap thread receiver
- Bristles insert-molded in this shot
- Wall thickness: 1.5–2.0mm throughout
- Mold: Single-cavity steel mold with side actions for the bristle head undercuts. Estimated mold cost: $8k–12k.

**Assembly phase (between 1st and 2nd shot):**
- Insert motor into pocket (press-fit, automated pick-and-place)
- Insert switch into pocket
- Route and solder wires (battery contact → switch → motor)
- Place battery spring contact at base end

**2nd shot (TPE overmold):**
- Material: TPE (thermoplastic elastomer), e.g., Kraiburg TPC or Teknor Apex Monprene, Shore A 50–60
  - Must be PP-compatible for chemical bond during overmolding (no adhesive needed)
- Forms: Grip texture on handle (thumb pads, finger ridges), button membrane (~1mm thick over switch), head joint boot (seals the living hinge area while allowing oscillation), cosmetic surface finish on non-grip areas
- Wall thickness: 0.5mm (thin seal areas) to 1.5mm (grip zones)
- Mold: Separate mold that receives the assembled 1st-shot part. Estimated mold cost: $10k–15k (more complex due to the assembled components inside).

**Battery cap (separate molded part):**
- Material: PP, same grade as main body
- Threaded (M12 × 1.0 or custom 3-start coarse thread for fast factory assembly)
- O-ring groove on outer diameter
- Mold: Simple single-cavity mold, ~$2k

#### Load Analysis

| Load Case | Source | Magnitude | Structural Response |
|-----------|--------|-----------|-------------------|
| Motor vibration | Eccentric mass at 150–200 Hz | ~0.1N radial force | Absorbed by PP body wall. Negligible stress. |
| User grip | Hand squeeze during brushing | ~5–10N | PP wall + TPE grip distributes load. No stress concentration. |
| Bristle contact | Brushing pressure on teeth | ~2–4N applied at bristle tips | Reacted through head halves → living hinge → handle body. PP handle is rigid enough at 1.5mm wall. |
| Drop (1.5m to tile floor) | Accidental drop | Impact, ~3–5G | PP is impact-resistant. TPE overmold absorbs shock at edges. No cracking expected for typical drops. |

No vibration isolation needed — the motor is small (<1W), forces are minimal, and the product life is 90 days.

### 4.7 Physical Interfaces (Seals)

Four seal zones protect the internal components:

| Seal Zone | Type | Method | Critical Spec |
|-----------|------|--------|---------------|
| **1. Bristle bases** | Static | Insert-molding — PP flows around nylon bristle tufts during 1st injection | Mold temp 220–240°C, injection pressure must fully encapsulate each tuft base. Zero air gaps. QC: visual inspection + water immersion test on samples. |
| **2. Body overmold** | Static | TPE chemically bonds to PP during 2nd injection | PP surface must be clean and warm (residual from 1st shot or preheated). Bond strength ≥ 2 N/mm peel. Covers: switch pocket, motor pocket, wire channels, handle seam. |
| **3. Head joint boot** | Dynamic | TPE boot molded over the living hinge area, thin enough to flex (~0.8mm) | Must survive ~500k flex cycles (350 min × 10,000 RPM / 60 = ~58M shaft rotations, but the boot flexes at a lower frequency, ~200 Hz × 350 min × 60s = ~4.2M cycles). TPE Shore A 50, fatigue-rated. |
| **4. Battery cap** | Static, removable | Threaded PP cap compresses O-ring against molded seat in handle base | O-ring: NBR (nitrile), AS568-012 or similar (ID ~9mm, CS ~1.8mm). Compression 15–25%. Provides IPX5-level seal. Cap torque: hand-tight (~0.2 N·m). |

### 4.8 Control Loops

**N/A for electronic control loops.** There is no feedback, no sensing, no closed-loop control.

The motor runs open-loop at whatever speed the battery voltage supports. As the battery depletes over weeks of use:
- Fresh cell (1.6V): Motor runs at full speed, strong vibration
- Mid-life (1.3V): Slightly reduced speed, vibration still effective
- End-of-life (1.1V): Motor approaches stall, vibration weakens
- Below 1.0V: Motor stalls, brush stops working → user discards

This is a feature, not a bug: the sudden stall provides a clear end-of-life signal.

---

## 5. Interfaces

### Internal Interfaces (within device)

| Interface | From | To | Protocol | Data | Rate | Notes |
|-----------|------|----|----------|------|------|-------|
| Power | AAA cell (+) | Switch terminal 1 | DC via wire | 1.5V, 0–100 mA | Continuous when on | 30 AWG stranded, silicone insulated |
| Power | Switch terminal 2 | Motor terminal (+) | DC via wire | 1.5V, 60–100 mA | Continuous when on | 30 AWG stranded, soldered |
| Power | Motor terminal (−) | AAA cell (−) via spring | DC via spring contact | Return path | Continuous when on | Phosphor bronze spring, spot-welded or crimped |
| Mechanical | Motor eccentric | Linkage arm (socket) | Mechanical coupling | Rotary → oscillating force | 150–200 Hz | Press-fit or clip engagement |
| Mechanical | Linkage arm | Moving head half | Integral (molded as one piece) | Oscillating force | 150–200 Hz | PP living hinge pivot |

### External Interfaces (device to outside world)

| Interface | From | To | Protocol | Data | Notes |
|-----------|------|----|----------|------|-------|
| User → Switch | Finger press | Latching button (through TPE membrane) | Mechanical | On/off toggle | ~3N actuation force through 1mm TPE |
| Bristles → Teeth | Moving + fixed bristle tufts | User's teeth and gums | Mechanical contact | Oscillating cleaning force, ~1–2mm amplitude | Wet environment with toothpaste |
| Water → Seals | Tap water rinse | All four seal zones | Fluid pressure | IPX5 (splashing) | Post-brushing rinse, occasional full rinse under tap |

### Physical Connectors

| Connector | Purpose | Type | Notes |
|-----------|---------|------|-------|
| Battery cap (threaded) | Factory battery insertion, seal | M12 or custom coarse-thread PP cap + NBR O-ring | Not user-serviceable — no battery replacement on a consumable product |
| None | — | — | No USB, no debug port, no charging, no external connectors |

---

## 6. Power Architecture

**Power source:**
- Type: AAA alkaline primary cell (LR03)
- Capacity: 1000–1200 mAh (typical for quality AAA alkaline)
- Nominal voltage: 1.5V (fresh), declining to ~0.9V at end of life
- Motor stall voltage: ~1.0V (below this, motor cannot start)
- Charging: N/A — non-rechargeable, disposed with the brush
- Shelf life: 5–10 years (sealed in packaging)

**Power states:**

```
              ┌─────┐
              │ Off │ ← button not pressed, circuit open
              └──┬──┘
                 │ user presses button
                 ▼
              ┌─────┐
              │ On  │ ← motor running, battery draining
              └──┬──┘
                 │ user presses button again
                 ▼
              ┌─────┐
              │ Off │
              └─────┘

No sleep states. No idle states. No MCU power management.
The switch is the entire "power management system."
```

| State | Motor | Battery Drain | Notes |
|-------|-------|---------------|-------|
| Off | Stopped | ~0 (switch open, leakage only: <1 µA) | Indefinite shelf life while off |
| On | Running at battery voltage | 60–100 mA | Draining at full rate |

**Power budget:**

| Component | Current Draw | Notes |
|-----------|------------:|-------|
| ERM motor (running) | 60–100 mA | Dominates. Only load in the circuit. |
| Switch contact resistance | <5 mΩ drop | Negligible |
| Wire resistance (total ~120mm of 30 AWG) | ~40 mΩ drop | Negligible at 100 mA |
| Spring contact resistance | <20 mΩ | Negligible |
| **Total (on)** | **60–100 mA** | |
| **Total (off)** | **<1 µA** | Switch leakage only |

**Battery life calculation:**

| Parameter | Value |
|-----------|-------|
| Cell capacity (AAA alkaline, to 1.0V cutoff) | ~1000 mAh (conservative) |
| Motor current (average) | 80 mA |
| Total runtime | 1000 ÷ 80 = **12.5 hours = 750 minutes** |
| Usage pattern | 2×/day × 2 min = 4 min/day |
| Calendar life | 750 ÷ 4 = **187 days (~6 months)** |

At 80 mA average draw, the AAA cell delivers approximately **750 minutes** of motor runtime — over 2× the 350-minute target. This surplus provides margin for:
- Longer brushing sessions (some users brush 3+ minutes)
- Forgetting to turn off occasionally
- Alkaline capacity variation between manufacturers
- Temperature effects (capacity drops ~10% at 5°C vs. 25°C)

Even in a pessimistic scenario (100 mA draw, 800 mAh capacity, 50% forgetting-to-turn-off overhead), runtime is: 800 ÷ 100 × 0.5 = 4 hours = 240 minutes. Still well within the 350-minute target if the user is somewhat attentive.

**Discharge profile at end of life:**
The alkaline cell's voltage drops gradually from 1.5V to ~1.2V over 80% of its capacity, then falls steeply to 1.0V in the final 20%. The motor runs at slightly reduced speed in the 1.2–1.1V range but still produces adequate vibration. Below 1.0V, the motor stalls abruptly. From the user's perspective: works fine → works fine → works fine → dead. Functionally sudden.

---

## 7. Connectivity Architecture

**N/A.** No wireless connectivity. No wired data connection. No protocols. This product has zero digital interfaces.

---

## 8. Key Technical Decisions and Trade-offs

### Decision 1: No MCU — Pure Electromechanical
- **Options considered:** (A) No MCU, direct battery-switch-motor circuit. (B) Tiny MCU (Padauk PMS150C, $0.03) for 2-minute timer auto-shutoff. (C) MCU + NFC for usage tracking (original concept).
- **Chosen:** A — No MCU
- **Rationale:** The user explicitly chose a simple on/off button with no timer. Removing the MCU eliminates: a PCB (~$0.15), the IC ($0.03–0.08), passive components (~$0.02), programming step in manufacturing (~$0.05 amortized), and a failure mode. Total savings: ~$0.25–0.30 per unit. For a $3–5 retail product, this is 5–10% of BOM.
- **Consequences:** No timer, no usage tracking, no end-of-life warning. The motor stopping IS the end-of-life signal.
- **Risks:** Users who want a 2-minute timer won't get one. Mitigation: this is a budget product — users who want smart features buy a Sonicare.

### Decision 2: AAA Battery Over AAAA
- **Options considered:** (A) AAA — 10.5mm dia, 1000+ mAh, universally available, $0.05–0.08 at volume. (B) AAAA — 8.3mm dia, 500–600 mAh, less common, $0.08–0.12.
- **Chosen:** A — AAA
- **Rationale:** 2× the capacity (750+ min vs ~375 min runtime), cheaper, available from any battery supplier worldwide with no sourcing risk. The handle diameter penalty (15–16mm vs ~14mm) is acceptable — the Oral-B Pulsar uses an AA cell and is ~18mm at the grip.
- **Consequences:** Handle is slightly thicker than a manual toothbrush (~12mm) but thinner than the Pulsar. Runtime far exceeds the 350-min target.
- **Risks:** None significant. AAA is the safe choice.

### Decision 3: Dual-Injection Overmolding Over Ultrasonic Welding
- **Options considered:** (A) Two-piece shell + ultrasonic welding (cheaper tooling, ~$5k). (B) Dual-injection overmolding (more expensive tooling, ~$20k, better sealing).
- **Chosen:** B — Dual-injection overmolding
- **Rationale:** Overmolding seals the entire assembly in one step (TPE chemically bonds to PP) and simultaneously provides the grip texture, button membrane, and head joint boot. Ultrasonic welding only seals the shell halves — the button, bristle head, and joint would still need separate seals (gaskets, adhesive), adding parts and assembly steps that offset the tooling savings.
- **Consequences:** Higher tooling investment ($18k–25k total for both molds + cap mold). Per-unit cost is competitive at 10k+ volume because the sealing, grip, and cosmetic surface are all achieved in one manufacturing step.
- **Risks:** Mold amortization. At 10k units, tooling adds $1.80–2.50/unit. At 50k, it drops to $0.36–0.50. Need volume commitment to make the economics work.

### Decision 4: PP Over ABS for Rigid Body
- **Options considered:** (A) Polypropylene (PP). (B) ABS. (C) PP body + ABS head.
- **Chosen:** A — PP throughout
- **Rationale:** PP is cheaper ($0.80/kg vs $1.50/kg), FDA food-contact compliant (21 CFR 177.1520), has excellent living hinge fatigue life (10M+ cycles — critical for the split head pivot), good chemical resistance to toothpaste, and bonds reliably with TPE in overmolding. ABS is stiffer and has a better surface finish, but the living hinge would fatigue-crack in ABS within weeks.
- **Consequences:** Slightly lower surface finish (PP has a waxy surface). Mitigated by the TPE overmold covering most visible areas.
- **Risks:** None. PP is the industry standard for toothbrush handles.

---

## 9. Constraints

### Regulatory
- **US:** No FCC certification needed (no intentional or unintentional radiator — no electronics). UL or ETL listing not required for a battery-powered product under 20V with no charging circuit, but retailer may require it. Battery cell must comply with DOT transport regulations (alkaline AAA exempt from UN38.3 testing).
- **EU:** CE marking required. Applicable directives: General Product Safety Directive (2001/95/EC), Battery Directive (2006/66/EC for disposal labeling), REACH (chemical substances), RoHS (lead-free).
- **Material safety:** All oral-contact materials (PP, TPE, nylon bristles) must comply with FDA 21 CFR (US) and EU Regulation 10/2011 (food-contact plastics). Certificates of compliance required from resin suppliers.
- **Bristle standard:** ISO 20126 (manual toothbrushes) — covers bristle end rounding, tuft retention, and overall construction. Though technically a powered brush, the same physical safety standards apply.
- **Battery marking:** IEC 60086-1 compliance for alkaline cells. Disposal symbol required on packaging (WEEE for EU, state-specific for US).
- **Target markets:** US, EU, UK, Canada

### Environmental
- Operating temperature: 5°C to 40°C (bathroom temperatures)
- Storage temperature: -10°C to 50°C (warehouse, retail shelf, car glovebox)
- Ingress protection: IPX5 (protected against water jets from any direction)
- Humidity: 30–95% RH non-condensing (bathroom environment)
- Drop: 1.5m to hard surface without loss of function (standard consumer product drop test)

### Cost

| Item | Target | Notes |
|------|-------:|-------|
| BOM (at 10k units) | <$1.50 | Excluding tooling amortization |
| BOM (at 50k units) | <$1.20 | Volume pricing on motor, battery, resin |
| Tooling (total, one-time) | $20k–27k | 1st shot mold + 2nd shot mold + cap mold |
| Tooling amortized (at 50k units) | $0.40–0.54 /unit | |
| Total COGS at 50k | ~$1.60–1.74 | BOM + amortized tooling |
| Retail price target | $3–5 | 2–3× COGS depending on distribution channel |

**BOM estimate (at 10k units):**

| Component | Est. Cost | Supplier Type |
|-----------|----------:|---------------|
| AAA alkaline cell | $0.06 | Battery distributor |
| Cylindrical ERM motor (⌀6×12mm, 1.5V) | $0.12 | Shenzhen motor supplier |
| Latching push-button switch (6×6mm) | $0.03 | Electronics component supplier |
| Wire (30 AWG, 2× ~60mm lengths) | $0.01 | Wire supplier |
| Spring contact (phosphor bronze) | $0.02 | Stamping supplier |
| Contact plate (brass or phosphor bronze) | $0.01 | Stamping supplier |
| O-ring (NBR, AS568-012) | $0.01 | Seal supplier |
| PP resin (~12g main body + cap) | $0.02 | Resin distributor |
| TPE resin (~5g overmold) | $0.02 | Resin distributor |
| Nylon bristles (PA-612, ~35 tufts) | $0.03 | Bristle supplier |
| Solder + flux | $0.01 | — |
| **Component BOM** | **~$0.34** | |
| Injection molding (2 shots + cap) | $0.25 | Contract manufacturer |
| Assembly (motor insert, wiring, soldering, battery insertion, cap closing) | $0.35 | Manual with jig assistance |
| QC / inspection (sample basis) | $0.05 | Inline |
| Packaging (blister pack + card) | $0.15 | Packaging supplier |
| **Total COGS** | **~$1.14** | At 10k units, excl. tooling |

### Manufacturing
- Target annual volume: 10k (year 1), 50k+ (year 2)
- Assembly process:
  1. 1st injection shot: PP body with insert-molded bristles (cycle time ~25s)
  2. Bristle trimming and end-rounding (automated, ~5s/unit)
  3. Component insertion: motor press-fit into pocket, switch into pocket (automated or semi-automated, ~8s)
  4. Wiring: solder battery contact → switch → motor (jig-assisted manual or automated, ~12s)
  5. Battery spring insertion at base (press-fit, ~3s)
  6. 2nd injection shot: TPE overmold over assembled part (cycle time ~20s)
  7. Battery insertion: drop AAA cell into tube from base (automated, ~3s)
  8. Battery cap + O-ring assembly: thread cap into base (automated torque driver, ~4s)
  9. Functional test: press button, verify motor runs, press again, verify stop (~5s)
  10. Packaging: insert into blister, heat-seal card (~8s)

  **Total line time per unit: ~90–100 seconds** (with parallel stations for injection molding)

- Tooling: 3 steel molds (1st shot PP, 2nd shot TPE, battery cap). Single-cavity initially, multi-cavity at 50k+ volume.
- Factory yield target: ≥97% (primary reject: bristle seal defects, motor DOA, wiring open)
- Test: 100% functional test (motor runs when button pressed). Sample-basis water immersion test (1 per 100 units, submerge in 10cm water for 30 min, verify motor still runs).

### Schedule
- Key milestones: Motor sample evaluation (M1), Mold design (M1–M2), 1st shot sampling (M3), Overmold sampling (M4), Assembly trial (M5), Functional testing + water ingress validation (M5–M6), Regulatory material certificates (M4), Pilot production run (M7), Mass production (M8)
- Hard deadlines: None identified
- Certification: CE marking (self-declaration for low-voltage battery product, no test lab needed). Material safety certificates from suppliers (2–4 weeks to obtain).

### Dependencies
- Motor supplier: Shenzhen-based, minimum order 5k–10k units, 4–6 week lead time
- Battery supplier: Standard AAA alkaline, universally available, 2-week lead time
- Mold maker: Shenzhen-based tooling shop, 4–6 weeks for molds
- PP + TPE resin: standard grades from major distributors (Braskem, Kraiburg), 1–2 week lead time
- Bristle supplier: PA-612 nylon bristle tufts, cut to length, 2–4 week lead time from specialty oral-care supplier (e.g., DuPont Filaments, Perlon)

---

## 10. Open Questions and Risks

| # | Question / Risk | Category | Impact | Owner | Target Date | Status |
|---|----------------|----------|--------|-------|-------------|--------|
| 1 | Motor vibration at end-of-life voltage (1.0–1.1V): does the selected motor still produce perceptible bristle vibration at 1.1V? Must test on samples. | Technical | H | Mech Lead | M1 | Open |
| 2 | Living hinge fatigue life: PP living hinge must survive ~4M flex cycles (350 min × 200 Hz × 60s). Standard PP hinges survive 1M+ easily, but validate with the specific geometry and TPE boot loading. | Technical | M | Mech Lead | M4 | Open |
| 3 | Insert-molded bristle seal quality: consistent seal around ~35 bristle tufts at production speed. Need to establish process window (injection temp, pressure, hold time) and QC sampling rate. | Manufacturing | H | Mfg Lead | M3 | Open |
| 4 | TPE-to-PP bond strength at head boot: the boot is thin (~0.8mm) and flexes constantly. Bond delamination = water ingress. Need peel test data from overmold trials. | Technical | H | Materials Lead | M4 | Open |
| 5 | Latching switch reliability in wet environment: the switch is sealed by the TPE membrane, but can moisture creep through the button actuation area over 90 days? Need accelerated life test (elevated humidity + temperature + cyclic button pressing). | Technical | M | Test Lead | M5 | Open |
| 6 | Retail channel acceptance at $3–5: will drugstore/grocery buyers stock a "disposable electric toothbrush" at this price point alongside $8–12 Oral-B Pulsar? Needs retail buyer conversations. | Market | H | Sales Lead | M2 | Open |
| 7 | Multi-cavity mold economics: at what annual volume does it make sense to invest in 4-cavity or 8-cavity molds (reducing per-unit molding cost but increasing tooling investment 3–4×)? | Cost | M | Mfg Lead | M6 | Open |

---

## Appendix

### Glossary

| Term | Definition |
|------|-----------|
| ERM | Eccentric Rotating Mass — a motor with an off-center weight that creates vibration when it spins |
| Living hinge | A thin, flexible section of plastic (typically PP) connecting two rigid parts, designed to flex repeatedly without breaking |
| TPE | Thermoplastic Elastomer — a rubber-like plastic that can be injection-molded and bonds to PP during overmolding |
| Insert molding | Placing a component (bristles) into a mold cavity before injecting plastic, so the plastic encapsulates and locks the component in place |
| Overmolding | A two-shot injection process where a second material (TPE) is molded over a first (PP), creating a multi-material part |
| IPX5 | Ingress protection rating: protected against water jets (6.3mm nozzle, 12.5 L/min, 3 min) from any direction |
| COGS | Cost of Goods Sold — total manufacturing cost per unit including materials, labor, and amortized tooling |

### Reference Documents

| Document | Location | Relevance |
|----------|----------|-----------|
| ISO 20126:2012 | ISO | Dentistry — manual toothbrush construction and safety requirements |
| FDA 21 CFR 177.1520 | FDA.gov | Olefin polymers (PP) for food-contact use |
| EU Regulation 10/2011 | EUR-Lex | Plastic materials intended to come into contact with food |
| IEC 60086-1 | IEC | Primary batteries — general requirements and test methods |
| Battery Directive 2006/66/EC | EUR-Lex | EU battery disposal and labeling requirements |

### Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-02-24 | Electrum workflow | Initial draft |
