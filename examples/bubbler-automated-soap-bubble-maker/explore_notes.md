# Exploration Notes — Bubbler

## Product Summary

An automated large-bubble machine that produces soap bubbles up to ~500mm diameter and actively optimizes bubble size and stability using force-sensing feedback. A single large loop (~160mm opening) dips horizontally into an open vat of soap solution, rotates to vertical, and a gentle fan inflates the film into a large bubble. A strain gauge on the wand arm tracks the inflation curve in real time — firmware adjusts fan speed, dip duration, and blow ramp rate to maximize successful large bubbles. Consumer product, outdoor/portable, battery-powered, targeting sub-$50 retail at 10k+ unit volumes.

## Product Classification

**Electromechanical.** The product moves air (fan/blower at low speed for gentle inflation), rotates a mechanical wand arm (dip-and-present mechanism), and uses closed-loop sensor feedback to optimize the process. Two motors, an open liquid vat, and a force-sensing feedback loop.

## HW/SW Boundary Analysis

| Domain | Hardware | Firmware | Software (App) |
|--------|----------|----------|-----------------|
| Bubble production | Fan motor (low-speed blower), wand arm with loop, pivot motor/actuator | Fan PWM ramp control, wand dip/rotate timing | N/A |
| Auto-optimization | Strain gauge or load cell on wand arm pivot, HX711 ADC | Inflation curve analysis: slope = growth rate, peak = size, sudden drop = pop vs. clean detach. Adaptive control adjusts fan ramp, dip time, pause-before-blow. | Optional — display optimization stats, let user set target bubble size |
| Solution management | Open vat (user fills manually), no pump or wick | Optionally sense solution level (capacitive) | Low-solution alert |
| User interface | Power button, mode dial or buttons, LEDs | Mode state machine, LED feedback | Optional BLE companion app |
| Power | LiPo or 4×AA, motor drivers | Battery monitoring, motor power management | Battery status |

**Primary sensing approach: Force on the wand arm.**

At 500mm bubble scale, the forces on the wand arm during inflation are significant and measurable:
- **Film weight + drainage:** A large soap film (~0.8 m² surface area, 1–4 µm thick) weighs 0.8–3.2g. Solution drains to the bottom, concentrating weight.
- **Aerodynamic drag:** As the bubble inflates to 500mm, its cross-section catches the gentle airflow. Even at low fan speed, this adds measurable force.
- **Total force on wand arm:** Estimated 50–200 mN (5–20 grams-force), building over several seconds.
- **A cheap strain gauge ($0.30) + instrumentation amplifier or HX711 ($0.50 at volume)** on the wand arm pivot can track the full inflation curve.

**Why force sensing beats other options at this scale:**
- **IR break-beam** would need components spanning the 160mm loop opening, and can't track the bubble as it inflates 250mm+ beyond the loop. Bulky and gives only binary "present/absent."
- **Pressure sensing** in the duct is overwhelmed by outdoor wind.
- **Motor current sensing** signal is too small relative to baseline motor draw.
- **Force sensing** is fully internal (no external protrusions), compact (embedded in pivot), gives a continuous inflation curve over seconds, and distinguishes pop (abrupt drop mid-rise) from clean detach (smooth peak then gradual drop).

**The firmware optimization objective function:**
- Maximize: successful detach rate (bubbles that inflate to target size and release cleanly)
- Minimize: premature pops (film burst during inflation)
- The force curve signature tells the firmware everything: inflation rate (fan too fast?), final size (fan too slow?), failure mode (pop = too aggressive, slow drain = dip too brief).

## Physical Architecture

### Physical Function
Inflates large soap bubbles (~500mm diameter) by gently blowing air through a soap-film-coated loop. The loop dips horizontally into an open vat of soap solution, soaks to build a thick film, then rotates 90° to vertical and presents the film to a slow, directed airstream.

### Mechanical Subsystem
- **Blower fan:** Low-speed fan or ducted blower (60–80mm). Must produce gentle, laminar-ish airflow — NOT high-velocity turbulent air. Large bubbles need very low airflow velocity (~0.5–2 m/s at the loop). A large slow fan is better than a small fast one. Variable speed via PWM.
- **Wand arm with loop:** A rigid arm (~200mm) with a ~160mm diameter loop at the end. The arm pivots at its base — horizontal position for dipping, vertical position for blowing. A geared DC motor or servo drives the pivot. The rotation must be smooth and controlled — a jerk or vibration during rotation will break the film.
- **Open vat:** A wide, shallow trough the user fills with soap solution. The loop submerges fully when horizontal. No pumps, no wicks, no sealed reservoir. The vat must be wide enough for the loop (~180mm minimum internal width) and deep enough for full submersion (~20–30mm depth). Removable or integrated with a pour spout for filling.
- **Cam or linkage (optional):** If a single motor drives both the dip/rotate and presents to the fan, a cam profile could sequence: dip → soak → rotate → blow → rotate back → dip. But a separate servo for the arm is simpler and allows firmware to control timing independently.

### Structure and Load Paths
- Injection-molded plastic shell, unified structure/enclosure.
- The product has a roughly upright form factor: vat at the bottom, fan at the back, wand arm pivoting from the middle, loop extends above/in front.
- Fan mounts in a molded duct in the rear, aimed forward at the vertical loop position.
- Wand arm pivot mounts mid-body. Motor or servo below the pivot, inside the dry zone.
- Vat sits in the base — open top, removable or integrated.
- Battery compartment in the base or rear, sealed from the wet zone.
- The wand arm is the main dynamic load — small forces (< 1N), low speed. No structural concerns beyond keeping the pivot smooth and the arm stiff enough not to flex excessively (which would corrupt the strain gauge signal).

### Working Media and Interfaces
- **Air:** Ambient, drawn from rear, directed gently forward through a duct/nozzle. Low velocity. No pressurization.
- **Soap solution:** Aqueous with surfactant + glycerin/polymer additives for large-bubble stability. Open vat — user fills it. Solution contacts the vat, wand arm lower section, and loop. Materials: PP or ABS (soap-resistant). The open vat means **transport leakage** is the user's problem — provide a snap-on lid for the vat.
- **Outdoor exposure:** Splashes from bubbles, rain, sun. Electronics must be isolated from the wet zone (vat and wand area). IPX4 for the electronics enclosure. The vat and wand arm can be fully wet — they're just plastic.

### Physical-Electronic Interface
- **Fan motor driver:** MCU PWM → MOSFET → fan motor. Gentle ramp control (not on/off — gradual spin-up to avoid bursting the film with an air blast).
- **Wand arm motor/servo:** MCU PWM → servo or MCU PWM → H-bridge → geared DC motor. Position control for dip (horizontal) → present (vertical) → return.
- **Strain gauge on wand arm:** Strain gauge bonded to wand arm near pivot → instrumentation amp or HX711 ADC → MCU. Sampled at ~10–50 Hz (bubble inflation takes seconds). Gives continuous force curve.
- **Solution level sensor (optional):** Capacitive sense on vat wall. Simple threshold: solution present / low.
- **Battery voltage:** ADC channel for fuel gauge.

## Relevant Skill Areas

1. **Sensors & Actuators (#10)** — Core differentiator. Strain gauge integration, signal conditioning for a small force signal in a vibrating, outdoor environment.
2. **Embedded Software & Firmware (#5)** — The optimization loop. Analyzing the force curve in real time, classifying outcomes (success/pop/no-film), adjusting parameters adaptively.
3. **Mechanical & Industrial Design (#4)** — The dip-rotate-blow mechanism. Smooth wand arm motion, open vat design, wet/dry zone separation, airflow duct for gentle laminar flow.
4. **Power Management (#9)** — Two motors + MCU + strain gauge amp. Battery-powered outdoor product.
5. **Cost & BOM Awareness (#15)** — Sub-$50 retail. The strain gauge + amp adds ~$1–2 to BOM vs. a dumb bubble machine. Must justify with clearly better performance.
6. **Manufacturing (#14)** — Strain gauge bonding to the wand arm is a manual or semi-automated step. Calibration at factory (zero the strain gauge with no load).

## Key Unknowns and Questions

1. **Strain gauge signal quality.** Can a cheap strain gauge on the wand arm reliably distinguish pop vs. clean detach vs. no-film in an outdoor environment with motor vibration? Needs prototype validation. Filtering at 10–50 Hz sampling should reject motor vibration (which is higher frequency).
2. **Optimal airflow profile for large bubbles.** How should the fan ramp up? Linear? Exponential? Start very slow and accelerate as the bubble grows? This is what the optimization loop must learn.
3. **Wand arm rotation speed and profile.** Too fast = film breaks during rotation. Too slow = film drains before reaching the fan. What's the sweet spot? Does it depend on solution chemistry?
4. **Solution chemistry sensitivity.** How much does the optimal fan/timing profile change when the user mixes their own solution vs. using a supplied concentrate? Can the firmware adapt automatically, or does it need a "solution type" setting?
5. **Battery life target.** Fan motor (~0.5–1W) + servo (~0.5W intermittent) + MCU + strain gauge amp (~0.1W). Total ~1–2W average. 4×AA (9 Wh) → 4.5–9 hours. LiPo 3S 2200mAh (24 Wh) → 12–24 hours. What's the target?
6. **App or standalone?** The optimization works standalone. A BLE app could show the inflation curve in real time (satisfying to watch), let the user set target bubble size, and log performance over time. Worth the ~$1–2 BLE cost?
7. **Vat size and portability.** A 180mm+ wide vat is large. Can it detach from the machine body for easy filling and transport? Should the machine fold or disassemble?

## Initial Risk Areas

| Risk | Severity | Likelihood | Notes |
|------|----------|------------|-------|
| Strain gauge signal too noisy outdoors | High | Medium | Motor vibration + wind. Mitigation: low-pass filter (inflation is slow, ~0.5 Hz signal), mechanical vibration isolation at pivot. Needs prototype. |
| Large soap films pop before inflation starts | High | Medium | Film drainage is the enemy. Mitigation: minimize time between dip and blow, optimize dip duration for thick film, gentle fan ramp. |
| Wand arm rotation breaks film | High | Medium | Jerky motion = broken film. Mitigation: servo with controlled velocity profile, or geared DC motor with soft-start. |
| Product too large/awkward for portable use | Medium | Medium | 160mm loop + vat + fan = product footprint maybe 200×200×250mm. Acceptable for "outdoor portable" but not pocket-sized. |
| Optimization doesn't noticeably outperform fixed settings | Medium | Medium | If a fixed fan speed and timing works 80% of the time, the adaptive loop only adds 20% improvement. Is that worth the sensor cost? |
| BOM exceeds $15 target | Medium | Low | MCU ($1) + strain gauge + amp ($1.50) + fan motor ($1.50) + servo ($2) + battery holder ($0.50) + shell ($2) + PCBA ($1.50) + misc ($1.50) ≈ $12. Tight but feasible. |

## Suggested Focus for High-Level Design

1. **Wand arm mechanism:** Single servo or geared motor for dip-rotate? Cam-driven or independently controlled? This is the core mechanical design.
2. **Airflow design:** Duct geometry for gentle, directed airflow at the loop position. Fan selection (size, type, speed range).
3. **Force sensing integration:** Where exactly on the wand arm? How to mount the strain gauge? What signal conditioning? Factory calibration procedure.
4. **Control loop architecture:** What parameters does firmware control (fan speed ramp, dip duration, soak time, rotate speed, blow duration)? What does the force curve tell it? What's the adaptation algorithm (PID? lookup table? gradient descent on success rate)?
5. **Wet/dry boundary:** Where does the wet zone end and the dry zone (electronics) begin? The wand arm crosses this boundary — its pivot shaft penetrates from wet to dry.
