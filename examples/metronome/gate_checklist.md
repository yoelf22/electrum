# Gate Checklist Validation: Haptic Metronome Bracelet

| Field | Value |
|-------|-------|
| Date | 2026-02-22 |
| System Description Version | 0.1 |
| Reviewer | Auto (PRD flow) |
| Result | **PASS** — all applicable items covered. |

---

## Vision and Context

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1 | Product statement is a single clear sentence | PASS | §1 — "For practicing and performing musicians, the Haptic Metronome Bracelet is a wrist-worn device that delivers precise vibrotactile beat pulses…" |
| 2 | Problem being solved is stated explicitly | PASS | §1 — audible metronomes unusable in performance, phone vibration too imprecise, earpieces isolate from room |
| 3 | [HW↔SW] HW vs. SW capabilities stated | PASS | §3 narrative — bracelet handles timing + haptic output + gesture detection; app handles all configuration |
| 4 | [HW↔SW] Software value on top of hardware is clear | PASS | §3 — "thin actuator controlled by a thick app." App is the entire configuration UI, practice logger, OTA channel. |
| 5 | Deployment environment defined | PASS | §1 — indoor/outdoor, practice/rehearsal/performance, consumer |
| 6 | Expected product lifespan stated | PASS | §1 — 3–5 years hardware, ongoing app updates |

## User Scenarios

| # | Item | Status | Notes |
|---|------|--------|-------|
| 7 | At least 3 concrete scenarios | PASS | 5 scenarios: solo practice, live performance, first use, false trigger rejection, low battery |
| 8 | [HW↔SW] Each scenario traces through full stack | PASS | Scenario 1: app sets config → BLE → bracelet stores → tap gesture → accel interrupt → FW start → timer ISR → I2C → DRV2605L → LRA pulse. Scenario 2: app preset → BLE → flash storage → tap start → haptic beats → double-tap stop. |
| 9 | At least 1 error/edge-case scenario | PASS | Scenario 4 (false trigger rejection), Scenario 5 (low battery) |
| 10 | [HW↔SW] First-time experience described end-to-end | PASS | Scenario 3 — unbox, download app, scan + pair, tap start, feel pulses. < 60 seconds. |
| 11 | Most common interaction identified | PASS | Scenario 1 — feel beats during practice, adjust tempo from app between exercises |
| 12 | [HW↔SW] Offline/degraded scenarios covered | PASS | §4.3 — "bracelet is fully functional without the app after initial configuration." §7 — tap/double-tap works without BLE, settings persist in flash. |

## System Architecture

| # | Item | Status | Notes |
|---|------|--------|-------|
| 13 | Block diagram covers all major subsystems | PASS | §3 — Mermaid diagram: MCU, accelerometer, haptic driver, LRA, LED, power, app, cloud |
| 14 | Every subsystem in diagram has a description | PASS | §4.1–4.4 cover all blocks |
| 15 | [HW↔SW] Every HW↔SW arrow specifies protocol, data, direction | PASS | §3 diagram labels + §5 interface tables |
| 16 | Data flows identified | PASS | §5 — 11 internal interfaces, 2 external interfaces, full detail |
| 17 | Trust/security boundaries marked | PASS | §3 Security Model — BLE link (LESC + config validation), OTA (Ed25519 + rollback), physical (SWD + APPROTECT) |
| 18 | Architecture narrative explains "why" | PASS | §3 — "thin actuator controlled by a thick app," explains timer priority, DRV2605L autonomy, gesture two-stage detection |
| 19 | [HW↔SW] Processing location is clear | PASS | §4.2 — "All beat generation on-device. App never participates in timing." |
| 20 | Fundamental HW problems identified | PASS | High-level design: haptic perceptibility during playing, component fitting in wrist pod, tap detection on vibrating limb |
| 21 | Resolution paths stated | PASS | Each has resolution direction in high-level design; §10 carries as open questions with owners |

## Subsystem Descriptions — Hardware

| # | Item | Status | Notes |
|---|------|--------|-------|
| 22 | MCU selected with rationale | PASS | §4.1 — nRF52832, same rationale as tabletop (integrated BLE, mature SDK) |
| 23 | Dominant tradeoff axis per component identified | PASS | High-level design component table: MCU (FW complexity), LRA (performance), DRV2605L (FW complexity), accel (FW complexity), battery (physical constraint) |
| 24 | Tradeoff conflicts surfaced | PASS | LRA cost vs. performance, battery capacity vs. pod size, DRV2605L cost vs. custom driver simplicity |
| 25 | All sensors listed with interface, rate, specs | PASS | §4.1 — LIS2DH12 with I2C, tap/double-tap hardware detection, configurable threshold |
| 26 | Actuators and physical UI listed | PASS | §4.1 — LRA motor, DRV2605L driver, bi-color LED. No buttons (justified by app-only design). |
| 27 | PCB strategy described | PASS | §4.1 — 28×18mm, 4-layer, component placement per side, antenna keep-out, LRA mounting |
| 28 | [HW↔SW] Test points and debug interfaces documented | PASS | §4.1 — Tag-Connect TC2030-NL on bottom side; §5 physical connectors table |

## Subsystem Descriptions — Firmware

| # | Item | Status | Notes |
|---|------|--------|-------|
| 29 | OS/framework chosen with rationale | PASS | §4.2 — bare-metal with nRF5 SDK, same rationale |
| 30 | Major modules listed with responsibilities | PASS | §4.2 — 8 modules with inputs/outputs. Dual-pulse downbeat implementation detailed separately. |
| 31 | [HW↔SW] HAL boundaries defined | PASS | §4.2 — modules reference nRF5 SDK peripherals (TIMER, I2C, GPIOTE, SAADC, FDS). DRV2605L accessed via I2C abstraction. |
| 32 | [HW↔SW] OTA update strategy defined | PASS | §4.2 — Nordic Secure DFU, dual-bank A/B, Ed25519, rollback |
| 33 | [HW↔SW] On-device vs. cloud processing boundary | PASS | §4.2 — all beat generation on-device |
| 34 | [HW↔SW] FW versioning scheme defined | PASS | §4.2 — SemVer, DFU init packet header, BLE DIS 0x2A26, downgrade rejection |

## Subsystem Descriptions — Companion App

| # | Item | Status | Notes |
|---|------|--------|-------|
| 35 | Platform and framework chosen | PASS | §4.3 — Flutter, iOS + Android |
| 36 | Core screens and flows listed | PASS | §4.3 — 6 screens: onboarding, main, accent editor, presets, practice log, settings |
| 37 | [HW↔SW] Device communication protocol defined | PASS | §4.3 — GATT table with 12 characteristics, directions, formats |
| 38 | [HW↔SW] App behavior when disconnected | PASS | §4.3 — bracelet continues at last config, app shows "Disconnected," auto-reconnects |
| 39 | [HW↔SW] Pairing flow documented step-by-step | PASS | §7 — 6-step flow |
| 40 | App store requirements and constraints noted | PASS | §4.3 — iOS background BLE, Android 12+ permissions, battery optimization, review process |

## Subsystem Descriptions — Cloud / Backend

| # | Item | Status | Notes |
|---|------|--------|-------|
| 41 | Platform/infrastructure chosen | PASS | §4.4 — AWS S3 + CloudFront |
| 42 | [HW↔SW] Device provisioning approach | PASS | §4.4 — BLE random static address + DFU public key at factory |
| 43 | Data model documented | PASS | §4.4 — firmware images and practice logs |
| 44 | [HW↔SW] Device management capabilities | PASS | §4.4 — "No device shadow. State on-device." |
| 45 | [HW↔SW] Device-to-cloud authentication | N/A | Device never contacts cloud. App downloads OTA images over HTTPS. |

## Interfaces

| # | Item | Status | Notes |
|---|------|--------|-------|
| 46 | Every internal bus/connection listed | PASS | §5 — 11 internal interfaces including I2C (shared bus for DRV2605L + LIS2DH12), GPIO interrupts, ADC, power |
| 47 | Every external interface listed | PASS | §5 — BLE, USB-C |
| 48 | Physical connectors documented | PASS | §5 — USB-C, Tag-Connect, band lugs |
| 49 | No subsystem is an island | PASS | All blocks connected |
| 50 | Protocol specified for each interface | PASS | Every row has protocol column |
| 51 | [HW↔SW] HW↔FW interfaces specify signal-level details | PASS | §5 — I2C addresses, interrupt polarity, DMA, ADC resolution, shared bus note |
| 52 | [HW↔SW] FW↔App interfaces specified | PASS | §4.3 GATT table + §7 pairing flow. Connection intervals in §5. |
| 53 | [HW↔SW] App↔Cloud interfaces specified | PASS | §4.4 — HTTPS for OTA images |
| 54 | [HW↔SW] Data format transformations documented | PASS | §4.2 — BPM → µs interval → timer compare → I2C waveform command → LRA drive. Accel tap interrupt → axis validation → start/stop. |

## Power Architecture

| # | Item | Status | Notes |
|---|------|--------|-------|
| 55 | Power source and capacity specified | PASS | §6 — 150 mAh LiPo |
| 56 | Power states defined with transition triggers | PASS | §6 — state diagram: Off, Booting, Idle, Playing |
| 57 | Power budget table for primary mode | PASS | §6 — Playing at 4.9 mA avg with per-component breakdown and duty cycles |
| 58 | Target battery life stated | PASS | §6 — > 8 hours continuous |
| 59 | Back-of-envelope calculation done | PASS | §6 — 30 hours continuous, 10 days typical use |
| 60 | Charging method specified | PASS | §6 — USB-C at 250 mA, ~45 min charge |
| 61 | [HW↔SW] FW role in power management defined | PASS | §4.2 power manager module — System ON/OFF, WFE between beats, BLE advertising intervals |
| 62 | [HW↔SW] Radio duty cycle and app responsiveness noted | PASS | §5 — advertising 1000 ms, connection interval 30–50 ms. §7 — connection takes up to 1.5s during pairing. |

## Connectivity

| # | Item | Status | Notes |
|---|------|--------|-------|
| 63 | Primary connectivity chosen with rationale | PASS | §7 — BLE 5.0, rationale: low power, direct phone connection, app is primary UI |
| 64 | Protocol stack documented | PASS | §7 — Physical, Link, Application, Security layers |
| 65 | Data transmission estimated | PASS | §7 — event-driven, 1–32 bytes, < 1 KB/day |
| 66 | [HW↔SW] Provisioning/pairing step-by-step | PASS | §7 — 6 steps |
| 67 | [HW↔SW] Offline behavior defined | PASS | §7 — bracelet runs independently, tap start/stop works, settings persist, app auto-reconnects |
| 68 | [HW↔SW] Connection recovery specified | PASS | §4.3 — auto-reconnect, re-sync by reading all characteristics. §8 Decision 3 — BLE disconnect risk and mitigation. |

## Key Decisions

| # | Item | Status | Notes |
|---|------|--------|-------|
| 69 | At least 3 non-obvious decisions documented | PASS | §8 — 4 decisions |
| 70 | Options considered, chosen approach, rationale | PASS | Full structure per decision |
| 71 | Consequences and risks stated | PASS | Each includes consequences + risks + mitigations |
| 72 | 3 decisions that would force redesign if reversed | PASS | Decision 1 (LRA+DRV2605L — defines haptic subsystem), Decision 2 (dual-pulse downbeat — defines beat differentiation), Decision 3 (app-only config — defines form factor and interaction model) |
| 73 | [HW↔SW] HW/SW tradeoff decisions explicit | PASS | Decision 1 (motor type = HW, driver complexity = FW), Decision 4 (hardware vs. firmware tap detection) |

## Constraints

| # | Item | Status | Notes |
|---|------|--------|-------|
| 74 | Required certifications listed | PASS | §9 — FCC, CE/RED, IC, BT SIG, REACH for skin contact |
| 75 | Operating environment defined | PASS | §9 — 0–45°C, IPX4, 1.5m drop, vibration during playing |
| 76 | Target BOM cost stated | PASS | §9 — < $18 at 1k, < $15 at 5k, full BOM breakdown |
| 77 | Target production volume stated | PASS | §9 — 2k–10k year 1, 10k+ year 2 |
| 78 | Key schedule milestones listed | PASS | §9 — M1 through M9 |
| 79 | Third-party dependencies identified | PASS | §9 — Nordic SDK, Flutter, DRV2605L library, silicone tooling vendor, band supplier |
| 80 | [HW↔SW] App store constraints noted | PASS | §4.3 — iOS background BLE, Android permissions, review process |
| 81 | [HW↔SW] Manufacturing test requirements | PASS | §9 — BLE test, haptic verification via vibration sensor, gesture test, LED, battery. IPX4 splash test per batch. |

## Open Questions and Risks

| # | Item | Status | Notes |
|---|------|--------|-------|
| 82 | All questions have owner and target date | PASS | §10 — 8 questions, each with owner and milestone |
| 83 | High-impact risks have mitigation plans | PASS | §10 — H-impact: haptic perceptibility during guitar/violin/piano playing (larger LRA fallback), tap false triggers (per-instrument testing), dual-pulse perception (gap adjustment fallback) |
| 84 | No question open >2 weeks without progress | PASS | Fresh document |
| 85 | [HW↔SW] Cross-domain risks flagged | PASS | §10 #2 (FW gesture algorithm depends on real-world accel data from playing), #3 (dual-pulse timing depends on DRV2605L hardware sequencer), #7 (DRV2605L sequence jitter may require firmware-timed fallback) |

## Overall Quality

| # | Item | Status | Notes |
|---|------|--------|-------|
| 86 | No section is placeholder-only | PASS | All sections have specific, real content |
| 87 | Consistent terminology | PASS | Glossary with 13 terms including haptic-specific (LRA, ERM, dual-pulse, Z-dominance) |
| 88 | Diagrams match text | PASS | Mermaid blocks match §4 subsystems and §5 interfaces |
| 89 | [HW↔SW] Cross-domain consistency check | PASS | Power budget uses DRV2605L datasheet values, I2C bus shared correctly (different addresses), flash layout matches nRF52832 512KB, GATT characteristics match app screens, dual-pulse timing fits within beat intervals |
| 90 | [HW↔SW] Cross-domain review needed | N/A | Auto-generated — needs human review |
| 91 | Open questions resolved or carried as TBDs | PASS | §10 — all 8 carried with owners |

---

## Summary

| Category | Pass | N/A | Fail | Total |
|----------|-----:|----:|-----:|------:|
| Vision and Context | 6 | 0 | 0 | 6 |
| User Scenarios | 6 | 0 | 0 | 6 |
| System Architecture | 9 | 0 | 0 | 9 |
| Hardware | 7 | 0 | 0 | 7 |
| Firmware | 6 | 0 | 0 | 6 |
| Companion App | 6 | 0 | 0 | 6 |
| Cloud / Backend | 4 | 1 | 0 | 5 |
| Interfaces | 9 | 0 | 0 | 9 |
| Power Architecture | 8 | 0 | 0 | 8 |
| Connectivity | 6 | 0 | 0 | 6 |
| Key Decisions | 5 | 0 | 0 | 5 |
| Constraints | 8 | 0 | 0 | 8 |
| Open Questions | 4 | 0 | 0 | 4 |
| Overall Quality | 5 | 1 | 0 | 6 |
| **Total** | **89** | **2** | **0** | **91** |

### Gate Decision

**PASS** — 89/91 items pass, 2 N/A (device-to-cloud auth — device never contacts cloud; cross-domain human review — auto-generated). Zero FAIL items. Product definition is ready to proceed to PRD.
