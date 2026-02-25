### Bubbler — High-Level System Design

**Date:** 2026-02-25 | **Author:** Electrum workflow | **Status:** Draft

#### What It Is

A battery-powered outdoor machine that produces large soap bubbles (up to ~500mm diameter) by dipping a 160mm loop into an open vat, rotating it to vertical, and gently inflating the film with a slow fan. A strain gauge on the wand arm pivot tracks the inflation curve in real time — firmware adjusts fan speed, dip duration, and blow ramp to maximize successful large bubbles and resist light wind (up to 4 kph). Standalone operation, physical controls only, targeting sub-$50 retail at 10k+ units.

#### Block Diagram

![Block Diagram](block_diagram.png)

#### Subsystems

| Subsystem | Purpose | Domain |
|-----------|---------|--------|
| Blower fan (60–80mm ducted) | Produce gentle, directed airflow (~0.5–2 m/s) to inflate the soap film into a large bubble | HW — Mechanical |
| Wand arm + 160mm loop | Dip horizontally into vat, rotate 90° to vertical, present soap film to airflow | HW — Mechanical |
| Pivot motor (geared DC or servo) | Drive wand arm rotation with smooth, controlled velocity profile | HW — Mechanical |
| Open vat | Hold soap solution; loop submerges fully when horizontal (~180mm wide, ~25mm deep) | HW — Mechanical |
| Strain gauge + HX711 ADC | Measure force on wand arm during inflation (50–200 mN range, 10–50 Hz sample rate) | HW — Sensing |
| MCU + firmware | Run optimization control loop, classify bubble outcomes, manage dip-rotate-blow state machine, drive motors | FW |
| Fan motor driver (MOSFET) | PWM-controlled gentle ramp of fan speed — no sudden air blasts | HW — Electronic |
| Pivot driver (H-bridge or servo PWM) | Position control for wand arm: horizontal ↔ vertical with soft-start/stop | HW — Electronic |
| Battery + regulator | 4×AA (6V nominal) or LiPo pack; 3.3V regulated rail for MCU and ADC | HW — Power |
| User controls (button, mode dial, LEDs) | Power on/off, mode selection (e.g., continuous / single / demo), status feedback | HW — UI |

#### Key Interfaces

| From → To | What Crosses | Protocol / Medium |
|-----------|-------------|-------------------|
| Strain gauge → HX711 | Analog differential voltage (µV–mV range) | Wheatstone bridge excitation, differential input |
| HX711 → MCU | Digitized force readings (24-bit) | Serial clock + data (DOUT/SCK), polled at 10–80 Hz |
| MCU → Fan MOSFET | Fan speed command | PWM (25 kHz), soft ramp in firmware |
| MCU → Pivot driver | Arm position / velocity command | PWM (servo) or PWM + DIR (H-bridge with encoder or timed open-loop) |
| MCU → LEDs | Status: idle / running / optimizing / low battery / error | GPIO (3–5 lines) |
| Mode dial / buttons → MCU | User mode selection, power | GPIO with debounce in firmware |
| Battery → regulators → all | Power rails: V_bat (4.5–6V AA or 7.4–11.1V LiPo), 3.3V logic | Linear or buck regulator |

#### Constraints

| Constraint | Value | Why It Matters |
|-----------|-------|----------------|
| BOM cost | < $15 at 10k units ($50 retail) | Rules out precision load cells, BLE modules, custom motors. Every dollar counts. |
| Battery life | ≥ 2 hours continuous operation | Average draw ~1.5W (fan ~0.8W, servo ~0.5W intermittent, MCU+sensing ~0.1W). 4×AA (≈9 Wh) gives ~4–6 hrs. LiPo 2S 2200mAh (≈16 Wh) gives ~8–10 hrs. |
| Wind resistance | Operate in side wind up to 4 kph | Fan must compensate — firmware detects wind via asymmetric force signatures and increases airflow. Duct geometry should partially shield the loop. |
| Outdoor / splash exposure | IPX4 for electronics enclosure | Open vat + bubble splashback. Electronics must be sealed from wet zone. Motors and wand arm can be wet. |
| Noise | Not a primary concern (outdoor use) | Fan and servo noise acceptable outdoors. No acoustic constraints. |
| Size | Footprint ≤ 250×250mm, height ≤ 300mm | Must be portable — carried to a park. Includes vat width (≥180mm for loop). |

#### Fundamental Hardware Problems

| Problem | Why It's Fundamental |
|---------|---------------------|
| Keeping the soap film intact during wand rotation from horizontal to vertical | If the film breaks during rotation, no bubble is produced regardless of how good the sensing and fan control are. Film drainage during rotation thins the film; any jerk or vibration tears it. This constrains motor choice, velocity profile, and mechanical stiffness of the arm. |
| Producing gentle, directed airflow that inflates a 500mm bubble without popping it | Large soap films need very low velocity (~0.5–2 m/s), evenly distributed across the 160mm loop. Turbulence, gusts from the fan starting, or uneven flow pop the film. Fan selection, duct geometry, and PWM ramp profile are all driven by this. |
| Extracting a usable force signal from the wand arm in an outdoor vibrating system | The strain gauge must resolve 50–200 mN of slowly changing force (0.1–1 Hz inflation signal) while rejecting motor vibration (10–100 Hz), wind buffeting, and thermal drift. Signal conditioning, mechanical isolation of the gauge from vibration sources, and firmware filtering all flow from this problem. |

#### Component Choice Architecture

| Component | Dominant Axis | Key Tension | Resolution Direction |
|-----------|--------------|-------------|---------------------|
| MCU | Cost + firmware complexity | ATtiny / low-end AVR ($0.50) has limited ADC and timers for simultaneous PWM + HX711 polling. ARM Cortex-M0 ($0.80–1.20, e.g., STM32C011 or RP2040) has plenty of peripherals. | ARM Cortex-M0 — the $0.50 premium buys multiple PWM channels, DMA for HX711, and enough flash for the optimization algorithm. |
| Strain gauge + amp | Cost vs. performance | Cheap foil strain gauge ($0.30) + HX711 ($0.50) = $0.80 total, 10–80 Hz, 24-bit. A pre-packaged load cell ($2–5) is easier to integrate but heavier and more expensive. | Foil strain gauge bonded to wand arm + HX711 — lowest cost, lightest, and the wand arm IS the flexure element. Requires factory calibration (zero with no load). |
| Pivot actuator | Firmware complexity vs. cost | Hobby servo ($2) has built-in position control but limited to 180° and fixed speed profile. Geared DC motor ($1.50) + H-bridge ($0.30) needs firmware position control but allows custom velocity profiles. | Geared DC motor + H-bridge — custom velocity profile is critical for not breaking the film. Servo's fixed speed and detent torque are wrong for this application. |
| Fan / blower | Physical constraint vs. performance | Large slow fan (80mm, $1.50) produces gentler airflow but takes more space. Small fast fan (40mm, $0.80) needs a duct/diffuser to slow the air, adding complexity. | Large slow fan — the gentler the airflow, the better for large bubbles. The product is already ~200mm wide for the vat, so an 80mm fan fits. |
| Battery | Cost vs. runtime | 4×AA ($0.50 holder, user-supplied cells) is cheapest but lower energy density. LiPo 2S ($4–6) gives longer runtime but adds charging circuit cost. | 4×AA for V1 — lowest cost, user-replaceable, no charging circuit needed. Revisit LiPo for V2 if runtime is insufficient. |

#### Three Hardest Problems

1. **Film survival during rotation:** The soap film must survive the wand arm rotating from horizontal (where it picked up the film) to vertical (where the fan inflates it). This transition takes ~1–2 seconds, during which gravity drains the film and any mechanical vibration tears it. The motor velocity profile, arm stiffness, and pivot smoothness all must be tuned together — and the optimal profile depends on solution chemistry and ambient conditions.

2. **Force-curve interpretation for adaptive control:** The strain gauge gives a continuous force signal during inflation. Firmware must classify each cycle's outcome (successful detach, premature pop, no-film, partial inflation) from the force curve shape, then adjust 4+ parameters (fan ramp rate, peak fan speed, dip duration, soak time) to improve the next cycle. The adaptation algorithm must converge quickly (within 5–10 cycles) and handle changing conditions (wind, solution aging, temperature).

3. **Wind compensation at 4 kph:** A 4 kph crosswind applies ~10–30 mN of lateral force on a 500mm bubble and distorts the inflation dynamics. The force curve changes shape in wind. Firmware must detect wind presence (asymmetric force signature, faster-than-expected force rise) and compensate — likely by increasing fan speed slightly and shortening blow duration to release the bubble before wind tears it. This interacts with problem #2: the adaptation must distinguish "wind changed" from "solution degraded."

#### Open Calls

| Decision | Options | Deadline |
|----------|---------|----------|
| Wand arm position sensing | (A) Timed open-loop with end-stop switches, (B) Potentiometer on pivot shaft, (C) Encoder on motor | Before schematic — affects firmware complexity and pivot driver circuit |
| Adaptation algorithm | (A) Lookup table with hill-climbing on success rate, (B) PID on force-curve features, (C) Simple gradient descent on parameters | Before firmware architecture — determines MCU flash/RAM needs |
| Vat attachment | (A) Removable snap-in vat with lid for transport, (B) Integrated vat (simpler, but harder to fill/clean) | Before mechanical design — affects enclosure mold and user flow |
| Solution level sensing | (A) Include capacitive sensor on vat wall ($0.10 + firmware), (B) Skip — user checks visually | Before schematic — minor cost but affects BOM and UX |
