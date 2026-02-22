# Product Requirements Document: Chair Balancing Act (Continuous Escalation Model)

| Field | Value |
|-------|-------|
| Version | 0.1 |
| Date | 2026-02-20 |
| Author | |
| Status | Draft |
| Source | system_description_chair_balancing_act.md v0.1 |
| Gate result | PASS (gate_checklist_chair_balancing_act.md) |

---

## 1. Product Summary

A clip-on tilt sensor for fixed-leg chairs (school, dining) that produces a continuously escalating audio tone when a chair leaves static balance. All legs down = silence; any leg lifts = pleasant low tone that rises proportionally with tilt, reaching maximum alarm just before the fall point. Standalone device — no app, no cloud, no connectivity. Target: parents and teachers of habitual chair tilters. Retail $15-25.

---

## 2. Requirement Tracks

This product has two development tracks. No app or cloud track — the device is fully standalone.

| Track | Scope |
|-------|-------|
| **HW** | PCB, enclosure, sensors, actuators, power, mechanical mounting |
| **FW** | Bare-metal firmware on ATtiny1616 — tilt detection, filtering, audio triggering, power management |
| **Integration** | Requirements that span both tracks and must be verified end-to-end |

---

## 3. Hardware Requirements

### 3.1 Electrical

| ID | Requirement | Priority | Acceptance Criteria | Source |
|----|------------|----------|-------------------|--------|
| HW-E-01 | MCU shall be ATtiny1616 (or pin-compatible ATtiny3216 fallback) | Must | Part number verified on BOM; UPDI programming succeeds | §4.1 |
| HW-E-02 | Accelerometer shall be a 3-axis MEMS device with programmable threshold interrupt and I2C interface | Must | LIS2DH12 or equivalent; interrupt fires within 100ms of threshold crossing; I2C read completes at 400 kHz | §4.1 |
| HW-E-03 | Class-D amplifier shall amplify MCU PWM output to drive piezo speaker; shall have a shutdown pin for power control | Must | Amp produces audible tone from MCU PWM input; draws <0.1 µA in shutdown | §4.1, §8 D3 |
| HW-E-04 | Piezo speaker shall produce ≥75 dB SPL at 10 cm | Must | Measured with SPL meter during functional test | §4.1 |
| HW-E-05 | All components shall operate on 2.0-3.6V direct from CR2450 (no voltage regulator) | Must | Device functions correctly at 2.0V (end-of-life cell) and 3.3V (fresh cell) | §5 |
| HW-E-06 | Total sleep current (all components) shall be ≤2 µA | Must | Measured at battery terminal with device in sleep state for >10s | §6 |
| HW-E-07 | PCB shall provide UPDI test pads (VCC, UPDI, GND) accessible via pogo-pin jig | Must | Factory programming jig connects and programs firmware in <10s | §4.1 |
| HW-E-08 | PCB shall provide I2C test points and power rail test points | Should | Accessible with scope probe for debugging | §4.1 |

### 3.2 Mechanical

| ID | Requirement | Priority | Acceptance Criteria | Source |
|----|------------|----------|-------------------|--------|
| HW-M-01 | Enclosure maximum dimensions: 35mm diameter × 10mm height | Must | Measured with calipers | §4.1 |
| HW-M-02 | Total weight (assembled, with battery): ≤18g | Must | Measured on scale | §4.1 |
| HW-M-03 | Enclosure material: ABS injection-molded | Must | Material cert from supplier | §4.1 |
| HW-M-04 | Battery compartment shall use twist-lock cover for CR2450 replacement without tools | Must | User can swap battery in <30s; cover reseats securely | §4.1, §2 S4 |
| HW-M-05 | Enclosure shall have ≥5 edge slots for piezo sound output | Must | Audio is audible at ≥70 dB at 10cm through enclosure | §4.1 |
| HW-M-06 | Mounting: adhesive pad on bottom face (3M Command-strip style), removable and repositionable | Must | Pad holds device under chair seat for ≥3 months under daily use; removes cleanly | §4.1 |
| HW-M-07 | Device shall survive drop from 1.5m onto hard floor without functional damage | Must | 5 consecutive drops from 1.5m, device functions normally after | §9 |
| HW-M-08 | Tactile button shall be accessible from under the chair without removing the device | Must | User can press button by reaching under seat | §4.1 |

### 3.3 PCB

| ID | Requirement | Priority | Acceptance Criteria | Source |
|----|------------|----------|-------------------|--------|
| HW-P-01 | PCB: dual-sided, 2-layer FR4, ≤30×25mm | Must | Gerber review + manufactured board measurement | §4.1 |
| HW-P-02 | Top side: CR2450 holder + tactile button | Must | Layout review | §4.1 |
| HW-P-03 | Bottom side: MCU, accelerometer, audio IC, passives | Must | Layout review | §4.1 |
| HW-P-04 | Piezo disc mounted inside enclosure wall, soldered to PCB edge pads | Must | Piezo survives 1.5m drop test and produces rated SPL | §4.1 |

---

## 4. Firmware Requirements

### 4.1 Core Behavior

| ID | Requirement | Priority | Acceptance Criteria | Source |
|----|------------|----------|-------------------|--------|
| FW-C-01 | FW shall wake from deep sleep on accelerometer threshold interrupt (departure from static balance) | Must | MCU wakes within 10ms of interrupt assertion; measured on scope | §3, §4.2 |
| FW-C-02 | FW shall read 3-axis acceleration via I2C at 10-25 Hz and compute tilt angle (pitch/roll) using atan2 | Must | Computed angle matches reference inclinometer within ±2° | §4.2 |
| FW-C-03 | FW shall apply a time filter: ignore tilt departures shorter than 300ms (transient rejection) | Must | Sitting down hard (< 300ms transient) produces no audio; sustained tilt >300ms engages tone | §4.2, §2 S5 |
| FW-C-04 | FW shall implement a dead-band of ~2° around the calibration baseline; tilt within the dead-band = static balance = silent | Must | Device remains silent when tilted <2° from baseline; tone begins at >2° sustained for >300ms | §4.2 |
| FW-C-05 | FW shall generate a continuous tone via PWM whose pitch and volume scale proportionally with tilt angle: pleasant low tone at first departure from static balance, rising continuously to maximum alarm near the fall point | Must | Tone pitch and volume increase monotonically with tilt angle; verified by sweeping tilt from 0° to 25° and recording audio | §4.2 |
| FW-C-06 | FW shall update the tone output in real-time as tilt angle changes (latency from angle change to tone change < 100ms) | Must | Tilting the chair faster or slower produces a correspondingly faster or slower tone change; no perceptible lag | §4.2 |
| FW-C-07 | FW shall fade tone to silence and return MCU to deep sleep when chair returns to static balance (all legs down, within dead-band for >300ms) | Must | Sleep current returns to ≤2 µA within 2s of chair settling; tone fades rather than cuts abruptly | §4.2, §6 |

### 4.2 Modes and Escalation Curves

| ID | Requirement | Priority | Acceptance Criteria | Source |
|----|------------|----------|-------------------|--------|
| FW-M-01 | FW shall support 3 tone modes, each with a distinct escalation curve: serious (clean rising tone), comedic (warbling, pitch bends, character), stealth (low max volume, subtle) | Must | Each mode produces audibly distinct tone character when tilt-tested | §4.2 |
| FW-M-02 | Short button press shall cycle modes: serious → comedic → stealth → off → serious | Must | Each press advances to the next mode; verified by tilt-triggering after each press | §4.2 |
| FW-M-03 | Current mode shall persist in EEPROM across power cycles | Must | Remove and reinsert battery; device resumes in last-set mode | §4.2 |
| FW-M-04 | Each mode's escalation curve shall map the full tilt range (dead-band to fall point) to a distinct pitch/volume/timbre trajectory | Must | Sweeping tilt from 0° to 25° in each mode produces a smooth, mode-appropriate escalation; no jumps or plateaus | §4.2 |

### 4.3 Calibration

| ID | Requirement | Priority | Acceptance Criteria | Source |
|----|------------|----------|-------------------|--------|
| FW-CAL-01 | On power-up, FW shall sample accelerometer for 2s and set the average as baseline "level" | Must | Device mounted at 5° from true level correctly treats 5° as baseline zero; tilt zones measured from this baseline | §4.2 |
| FW-CAL-02 | Long button press (3s) shall trigger re-calibration (resample baseline) | Must | After long-press on a tilted surface, tilt zones re-center on the new orientation | §4.2 |
| FW-CAL-03 | Calibration baseline shall persist in EEPROM | Should | Battery swap preserves last calibration (no re-calibration needed unless chair changes) | §4.2 |
| FW-CAL-04 | Boot-to-ready time shall be <3 seconds | Must | Timed from button press (power on) to first chime (ready) | §4.2 |

### 4.4 Power Management

| ID | Requirement | Priority | Acceptance Criteria | Source |
|----|------------|----------|-------------------|--------|
| FW-PM-01 | MCU shall enter power-down mode (deep sleep) when no tilt event is active | Must | Measured sleep current ≤0.1 µA at MCU pins | §6 |
| FW-PM-02 | FW shall monitor battery voltage via internal ADC periodically (e.g., once per tilt event) | Must | Low-battery flag set when VCC < 2.4V | §4.2 |
| FW-PM-03 | When low-battery flag is set, FW shall play a distinctive low-battery chirp on next tilt event | Must | Chirp is audibly distinct from all tilt-zone sounds | §2 S4, §4.2 |
| FW-PM-04 | Battery life shall be ≥6 months at 20 tilt events/day usage profile | Must | Calculated from measured sleep current + measured per-event charge; verified with long-duration test (or accelerated) | §6 |

### 4.5 Versioning

| ID | Requirement | Priority | Acceptance Criteria | Source |
|----|------------|----------|-------------------|--------|
| FW-V-01 | FW shall embed a version identifier (MAJOR.MINOR, 2 bytes) readable via UPDI during factory test | Should | Test jig reads and logs FW version for each unit | Gate checklist gap |

---

## 5. Integration Requirements

These requirements span HW and FW and must be verified on assembled units.

| ID | Requirement | Priority | Acceptance Criteria | Source |
|----|------------|----------|-------------------|--------|
| INT-01 | Accelerometer wake interrupt shall wake MCU from deep sleep and result in audible tone onset within 500ms of threshold crossing | Must | End-to-end timing: interrupt asserted → tone audible < 500ms; measured on scope + microphone | §3, §4.2 |
| INT-02 | Device shall produce no audio when subjected to transient motion (sitting down, bumping table) lasting <300ms | Must | Test with 10 simulated sit-downs; zero false triggers | §2 S5, §4.2 |
| INT-03 | Device shall produce a continuously escalating tone when chair is tilted from static to dynamic balance, with tone intensity proportional to tilt angle | Must | Test on 3 different chair types; slow tilt sweep produces smooth escalation; no jumps or dead spots | §4.2 |
| INT-04 | Device shall correctly cycle through modes and produce mode-appropriate tone character | Must | Cycle all 4 states (3 modes + off); tilt in each mode; verify distinct escalation curves | §4.2 |
| INT-05 | Device shall auto-calibrate on power-up and correctly detect departure from static balance relative to mounting surface (not absolute gravity) | Must | Mount on chair with 3° leg unevenness; verify tone starts only when chair actually tilts from its resting position | §4.2 |
| INT-06 | Battery replacement shall not require recalibration | Should | Swap battery; tilt immediately after; verify correct zone detection without long-press recalibration | §2 S4, FW-CAL-03 |
| INT-07 | Device shall function correctly at 0°C and 50°C | Must | Functional test in thermal chamber at both extremes | §9 |
| INT-08 | Device shall function correctly at VCC = 2.0V (depleted cell) and VCC = 3.3V (fresh cell) | Must | Full functional test at both voltage levels (use bench supply) | HW-E-05 |
| INT-09 | Factory test jig shall program FW via UPDI, run functional test (tilt → continuous tone plays and scales), and log results in <30s per unit | Should | Timed end-to-end on 10 consecutive units | §9 |

---

## 6. Priority Summary

| Priority | HW | FW | Integration | Total |
|----------|---:|---:|------------:|------:|
| Must | 16 | 17 | 7 | 40 |
| Should | 2 | 1 | 2 | 5 |
| **Total** | **18** | **18** | **9** | **45** |

---

## 7. Phasing

### V1 (MVP)

All "Must" requirements. The product ships as a standalone tilt-sensing device with continuous audio escalation, 3 tone modes, auto-calibration, CR2450 power, and adhesive mounting. 45 requirements total (40 must + 5 should — all achievable in V1).

### V2 (if market validates)

Potential additions based on customer feedback — **not committed, not designed:**

| Feature | Implication |
|---------|------------|
| Custom tone profiles via USB | Requires USB-C connector, mechanism to load escalation curve parameters. Board respin. |
| BLE + companion app | MCU changes from ATtiny to nRF52. Full board respin. App development (iOS + Android). |
| Adjustable sensitivity via app | Requires BLE. Depends on V2 BLE decision. |
| Rechargeable battery | Adds charging IC, USB-C, Li-Po cell. Enclosure grows. Full mechanical redesign. |

V2 decisions should wait for 6+ months of V1 sales data and customer feedback.

---

## 8. Traceability Matrix

| User Scenario | Key Requirements |
|---------------|-----------------|
| S1: Dinner table (tilt → rising tone → correct) | FW-C-01 through FW-C-07, INT-01, INT-03 |
| S2: Classroom (serious mode, continuous tone) | FW-M-01, FW-M-04, INT-04, HW-M-06 (adhesive repositionable) |
| S3: First use (unbox → attach → working) | FW-CAL-01, FW-CAL-04, HW-M-06, HW-M-08 |
| S4: Battery replacement | HW-M-04, FW-PM-02, FW-PM-03, INT-06 |
| S5: False trigger rejection | FW-C-03, INT-02 |

---

## 9. Open Items Carried from System Description

These items from the system description (§10) must be resolved during development. They do not block PRD approval but must be closed before production.

| # | Item | Blocks Requirements | Target |
|---|------|-------------------|--------|
| 1 | Escalation curve tuning across chair types | FW-C-05, FW-M-04 (curve shape may change) | M2 |
| 2 | Tone design for 3 modes (sound designer + FW collaboration) | FW-M-01, FW-M-04, INT-04 | M3 |
| 3 | Piezo volume validation in real environments | HW-E-04, HW-M-05 | M2 |
| 4 | False trigger testing with real users | FW-C-03, INT-02 | M2 |
| 5 | Adhesive durability testing | HW-M-06 | M3 |
| 6 | PWM audio quality — acceptable tone at low tilt? | FW-C-05, HW-E-03 | M2 |
| 7 | CPSIA/EN 71 acoustic safety for children's products | HW-E-04 | M2 |

---

## Appendix: Requirement ID Convention

| Prefix | Track |
|--------|-------|
| HW-E- | Hardware — Electrical |
| HW-M- | Hardware — Mechanical |
| HW-P- | Hardware — PCB |
| FW-C- | Firmware — Core behavior |
| FW-M- | Firmware — Modes |
| FW-CAL- | Firmware — Calibration |
| FW-PM- | Firmware — Power management |
| FW-V- | Firmware — Versioning |
| INT- | Integration (cross-track) |
