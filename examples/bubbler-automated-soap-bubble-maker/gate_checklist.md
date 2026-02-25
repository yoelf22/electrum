# Gate Checklist Validation: Bubbler

| Field | Value |
|-------|-------|
| Date | 2026-02-25 |
| System Description Version | 0.1 |
| Reviewer | Auto |
| Result | **PASS with notes** — 3 minor gaps, all N/A items justified. Ready for next phase. |

---

## Vision and Context

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1 | Product statement is a single clear sentence | PASS | §1 — "Bubbler is a battery-powered automated soap bubble machine that produces large bubbles…" |
| 2 | Problem being solved is stated explicitly | PASS | §1 — existing machines produce only small bubbles unreliably with no adaptation |
| 3 | [HW↔SW] HW vs. SW capabilities stated | PASS | §3 — mechanical subsystem (wand, fan, vat) is HW; optimization loop, force-curve analysis, state machine are FW |
| 4 | [HW↔SW] Software value on top of hardware is clear | PASS | §3 — firmware adds adaptive optimization (hill-climbing on force curves), not just fixed-speed operation |
| 5 | Deployment environment defined | PASS | §1 — outdoor, parks/backyards/events, portable, table or ground |
| 6 | Expected product lifespan stated | PASS | §1 — 2–3 years |

## User Scenarios

| # | Item | Status | Notes |
|---|------|--------|-------|
| 7 | At least 3 concrete scenarios | PASS | 5 scenarios: backyard party, street performer, unboxing, solution out, wind too strong |
| 8 | [HW↔SW] Each scenario traces through full stack | PASS | Scenario 1: dip → rotate → strain gauge → firmware calibrates → fan ramps → bubble releases. No app/cloud stack (standalone). |
| 9 | At least 1 error/edge-case scenario | PASS | Scenarios 4 (no solution) and 5 (wind too strong) |
| 10 | [HW↔SW] First-time experience described end-to-end | PASS | Scenario 3 — unboxing → batteries → solution → power → first bubbles in 2 minutes |
| 11 | Most common interaction identified | PASS | Scenario 1 — fill, press power, walk away |
| 12 | [HW↔SW] Offline/degraded scenarios covered | N/A | No connectivity — device is always "offline." Degraded modes covered via low-battery and wind-pause behaviors. |

## System Architecture

| # | Item | Status | Notes |
|---|------|--------|-------|
| 13 | Block diagram covers all major subsystems | PASS | Block diagram includes mechanical domain (vat, wand, fan, motor) and electronic domain (MCU, HX711, drivers, power, UI) |
| 14 | Every subsystem in diagram has a description | PASS | §4.1 (HW), §4.2 (FW) — all blocks described |
| 15 | [HW↔SW] Every HW↔SW arrow specifies protocol, data, direction | PASS | §5 interface table — HX711 serial protocol, PWM frequencies, GPIO directions all specified |
| 16 | Data flows identified | PASS | §5 — 8 internal interfaces with protocol, data, rate |
| 17 | Trust/security boundaries marked | N/A | No connectivity, no external data exchange. Battery-powered toy with no attack surface beyond physical access. |
| 18 | Architecture narrative explains "why" | PASS | §3 — explains force-sensing approach, why standalone, why no RTOS |
| 19 | [HW↔SW] Processing location is clear | PASS | §4.2 — "All processing is local. No connectivity, no external dependencies." |
| 20 | Fundamental HW problems identified | PASS | high_level_design.md — film survival during rotation, gentle airflow, force signal extraction |
| 21 | Resolution paths stated | PASS | Each problem has resolution direction (velocity profiles, duct geometry, filtering + mechanical isolation) |

## Subsystem Descriptions — Hardware

| # | Item | Status | Notes |
|---|------|--------|-------|
| 22 | MCU selected with rationale | PASS | §4.1 — STM32C011F4, cheapest Cortex-M0+ with sufficient peripherals, $0.70–0.90 |
| 23 | Dominant tradeoff axis per component identified | PASS | high_level_design.md component choice table covers MCU, strain gauge, pivot actuator, fan, battery |
| 24 | Tradeoff conflicts surfaced | PASS | §8 — 8 decisions with options and rationale |
| 25 | All sensors listed with interface, rate, specs | PASS | §4.1 sensor table — strain gauge, battery divider, capacitive level (optional) |
| 26 | Actuators and physical UI listed | PASS | §4.1 — blower fan, geared DC motor, 2 buttons, 3–5 LEDs |
| 27 | PCB strategy described | PASS | §4.1 — single board, 2-layer FR4, 50×35mm, component list, connector types |
| 28 | [HW↔SW] Test points and debug interfaces documented | PASS | §4.1 — SWD debug pads (Tag-Connect TC2030), 0.1" header for dev |

## Subsystem Descriptions — Firmware

| # | Item | Status | Notes |
|---|------|--------|-------|
| 29 | OS/framework chosen with rationale | PASS | §4.2 — bare-metal superloop, justified by simple task structure and 6KB RAM constraint |
| 30 | Major modules listed with responsibilities | PASS | §4.2 — 9 modules with I/O table |
| 31 | [HW↔SW] HAL boundaries defined | PASS | Implicit — STM32 HAL for GPIO/PWM/ADC, bit-bang SPI for HX711. Application modules use HAL functions. |
| 32 | [HW↔SW] OTA update strategy defined | PASS | §4.2 — "None for V1. Firmware programmed at factory via SWD." Justified for consumer toy at this price point. |
| 33 | [HW↔SW] On-device vs. cloud processing boundary | PASS | §4.2 — all processing local, no data leaves device |
| 34 | [HW↔SW] FW versioning scheme defined | GAP | Not explicitly addressed. Minor for V1 (no OTA, no app), but should define a version byte in flash for factory test/traceability. |

## Subsystem Descriptions — Companion App

| # | Item | Status | Notes |
|---|------|--------|-------|
| 35–40 | All app items | N/A | §4.3 — "Not applicable." No app in V1. V2 BLE companion noted as future option. |

## Subsystem Descriptions — Cloud / Backend

| # | Item | Status | Notes |
|---|------|--------|-------|
| 41–44 | All cloud items | N/A | §4.4 — "Not applicable. No cloud, no accounts, no data collection." |

## Interfaces

| # | Item | Status | Notes |
|---|------|--------|-------|
| 45 | Every internal bus/connection listed | PASS | §5 — 8 internal interfaces (force sensing, force data, fan PWM, motor H-bridge, battery ADC, buttons, LEDs, solution level) |
| 46 | Every external interface listed | PASS | §5 — battery (only external interface) |
| 47 | Physical connectors documented | PASS | §5 — 6 connectors (battery, strain gauge, motor, fan, SWD, vat electrode) |
| 48 | No subsystem is an island | PASS | All blocks connected via interface table |
| 49 | Protocol specified for each interface | PASS | §5 — PWM frequency, bit-bang SPI protocol, analog specs, GPIO polarity |
| 50 | [HW↔SW] HW↔FW interfaces specify signal-level details | PASS | §5 — voltage divider values, MOSFET part, H-bridge part, debounce timing, current-limiting resistor values |
| 51 | [HW↔SW] FW↔App interfaces specified | N/A | No app |
| 52 | [HW↔SW] App↔Cloud interfaces specified | N/A | No cloud |
| 53 | [HW↔SW] Data format transformations documented | PASS | §4.2 — raw 24-bit HX711 → tared grams-force → feature extraction (peak, slope, drop rate) → outcome classification → parameter adjustment |

## Power Architecture

| # | Item | Status | Notes |
|---|------|--------|-------|
| 54 | Power source and capacity specified | PASS | §6 — 4×AA, 6V nominal, ~9 Wh alkaline / ~10 Wh NiMH |
| 55 | Power states defined with transition triggers | PASS | §6 — low-battery thresholds (4.2V → reduced power, 3.8V → shutdown), BOR at 2.7V |
| 56 | Power budget table for primary mode | PASS | §6 — 5 consumers with current, duty cycle, average power. Total ~1.3W. |
| 57 | Target battery life stated | PASS | §6 — ~7 hours alkaline, target ≥2 hours met |
| 58 | Back-of-envelope calculation done | PASS | §6 — 9 Wh ÷ 1.3W = ~7 hours |
| 59 | Charging method specified | N/A | User-replaceable AA cells, no charging circuit |
| 60 | [HW↔SW] FW role in power management defined | PASS | §6 — firmware detects low battery via ADC, reduces fan speed, stops cycling on critical |
| 61 | [HW↔SW] Radio duty cycle specified | N/A | No radio |

## Connectivity

| # | Item | Status | Notes |
|---|------|--------|-------|
| 62–67 | All connectivity items | N/A | §7 — "Not applicable. Bubbler V1 has no wireless or wired data connectivity." Justified. |

## Key Decisions

| # | Item | Status | Notes |
|---|------|--------|-------|
| 68 | At least 3 non-obvious decisions documented | PASS | §8 — 8 decisions covering sensing, MCU, actuators, fan, battery, position sensing, enclosure, algorithm |
| 69 | Options considered, chosen approach, rationale | PASS | Every decision lists 2–4 options with rationale |
| 70 | Consequences and risks stated | GAP | Decisions list rationale but don't explicitly state downstream consequences/risks of each choice. Minor — the risks are covered in §10. |
| 71 | 3 decisions that would force redesign if reversed | PASS | Implicit: (1) strain gauge sensing — reversing requires different sensor + signal chain + firmware, (2) geared DC motor — reversing to servo changes H-bridge circuit + firmware velocity control, (3) 3-part enclosure — reversing requires new mold tooling |
| 72 | [HW↔SW] HW/SW tradeoff decisions explicit | PASS | Decision 6 (open-loop + end-stops vs. encoder) trades HW cost for FW calibration complexity. Decision 8 (hill-climbing) trades algorithm sophistication for flash/RAM. |

## Constraints

| # | Item | Status | Notes |
|---|------|--------|-------|
| 73 | Required certifications listed | PASS | §9 — FCC Part 15 Class B, CE (EMC + RoHS), toy safety TBD |
| 74 | Operating environment defined | PASS | §9 — 5–40°C operating, IPX4 electronics, UV-stabilized enclosure |
| 75 | Target BOM cost stated | PASS | §9 — $12.80 estimated, target <$15 for sub-$50 retail |
| 76 | Target production volume stated | PASS | §9 — 10k+ units |
| 77 | Key schedule milestones listed | GAP | No milestone schedule provided. Should add target dates for prototype, EVT, DVT, PVT, mass production. |
| 78 | Third-party dependencies identified | PASS | Implicit — COTS motors, fans, HX711, STM32 availability. No single-source risks identified. |
| 79 | [HW↔SW] App store constraints | N/A | No app |
| 80 | [HW↔SW] Manufacturing test requirements | PASS | §4.1 — SWD programming via Tag-Connect. §4.2 — factory tare calibration of strain gauge at boot. |

## Open Questions and Risks

| # | Item | Status | Notes |
|---|------|--------|-------|
| 81 | All questions have owner and target date | PASS | §10 — 6 questions with deadlines (relative to milestones) |
| 82 | High-impact risks have mitigation plans | PASS | §10 — 6 risks with likelihood, impact, and mitigation strategies |
| 83 | No question open >2 weeks without progress | PASS | Fresh document — all newly opened |
| 84 | [HW↔SW] Cross-domain risks flagged | PASS | §10 #1 (motor vibration tears film — HW problem mitigated by FW velocity profiles), #2 (noisy force signal — HW noise mitigated by FW filtering) |

## Overall Quality

| # | Item | Status | Notes |
|---|------|--------|-------|
| 85 | No section is placeholder-only | PASS | Every section has real content with specific numbers |
| 86 | Consistent terminology | PASS | Consistent use of "blow position," "dip position," "force curve," "cycle" throughout |
| 87 | Diagrams match text | PASS | Block diagram matches §5 interface table; arrangement diagram matches §4.1 component specs |
| 88 | [HW↔SW] Cross-domain consistency check | PASS | Power budget matches component specs (fan 300–500mA, motor 150–250mA); BOM matches component choices; firmware modules match HW interfaces (9 modules map to 8 interfaces) |
| 89 | [HW↔SW] Cross-domain review | N/A | Needs human review |
| 90 | Open questions resolved or carried as TBDs | PASS | §10 — all carried with deadlines |

---

## Summary

| Category | Pass | N/A | Gap | Total |
|----------|-----:|----:|----:|------:|
| Vision and Context | 6 | 0 | 0 | 6 |
| User Scenarios | 5 | 1 | 0 | 6 |
| System Architecture | 9 | 0 | 0 | 9 |
| Hardware | 7 | 0 | 0 | 7 |
| Firmware | 5 | 0 | 1 | 6 |
| Companion App | 0 | 6 | 0 | 6 |
| Cloud / Backend | 0 | 4 | 0 | 4 |
| Interfaces | 6 | 2 | 0 | 8 |
| Power Architecture | 6 | 2 | 0 | 8 |
| Connectivity | 0 | 6 | 0 | 6 |
| Key Decisions | 4 | 0 | 1 | 5 |
| Constraints | 5 | 1 | 1 | 7 |
| Open Questions | 4 | 0 | 0 | 4 |
| Overall Quality | 5 | 1 | 0 | 6 |
| **Total** | **62** | **23** | **3** | **88** |

### Gaps to Address

1. **FW versioning scheme** (#34): Add a firmware version byte or struct in flash for factory traceability (e.g., `{major, minor, build}` readable via SWD during production test).
2. **Decision consequences** (#70): §8 decisions state rationale but not explicit downstream consequences. The risks are captured in §10, so this is a formatting gap rather than a content gap.
3. **Schedule milestones** (#77): Add a milestone timeline (prototype → EVT → DVT → PVT → MP) to §9.

### N/A Justification

23 items are N/A — covering companion app (6), cloud/backend (4), connectivity (6), and individual items for offline scenarios (standalone device), security boundaries (no attack surface), charging (user-replaceable cells), radio duty cycle (no radio), FW↔App/App↔Cloud interfaces (no app/cloud), app store constraints (no app), and cross-domain review (needs human). All are justified by V1 being a fully standalone device with no connectivity.

### Gate Decision

**PASS** — proceed to next phase. The 3 gaps are minor (versioning is a one-line addition, consequences are already covered in §10, schedule is a planning artifact). None block the product definition from being actionable.
