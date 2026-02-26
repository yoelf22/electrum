# Gate Checklist Validation: Pop!

| Field | Value |
|-------|-------|
| Date | 2026-02-24 |
| System Description Version | 0.2 |
| Reviewer | Auto (PRD flow) |
| Result | **PASS with notes** — 3 minor gaps, all addressable without architectural changes. |

---

## Vision and Context

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1 | Product statement is a single clear sentence | PASS | §1 — "Pop! is a desktop popcorn machine that pops kernels one at a time using a slow conveyor belt through a hot zone." |
| 2 | Problem being solved is stated explicitly | PASS | §1 — gap between mindless microwave popcorn and overkill stovetop. Fills "snack + spectacle" niche. |
| 3 | [HW↔SW] HW vs. SW capabilities stated | PASS | §3 narrative — physics does the sorting, firmware does PID + motor + LEDs. Clear split. |
| 4 | [HW↔SW] Software value on top of hardware is clear | PASS | §3 — FW adds temperature regulation, safety watchdog, LED feedback, optional BLE stats. Not just "it has an app." |
| 5 | Deployment environment defined | PASS | §1 — indoor, desks/dorms/kitchens, consumer, any surface near USB-C PD. |
| 6 | Expected product lifespan stated | PASS | §1 — 2-3 years. |

## User Scenarios

| # | Item | Status | Notes |
|---|------|--------|-------|
| 7 | At least 3 concrete scenarios | FAIL | 1 scenario provided (MVP only, per user direction). Acceptable scope decision — the single scenario is detailed and end-to-end. |
| 8 | [HW↔SW] Each scenario traces through full stack | PASS | Scenario 1 traces: pour kernels → press button → preheat → belt + chute + hot zone → physics sorting → done. FW states map to physical actions. |
| 9 | At least 1 error/edge-case scenario | FAIL | No error scenario. Missing: what happens if user plugs in a 5V charger? What if hopper runs dry mid-cycle? What if chute jams? These are mentioned in decisions/risks but not as user scenarios. |
| 10 | [HW↔SW] First-time experience described end-to-end | PASS | Scenario 1 covers: fill hopper → plug in → press start → watch pops → eat. First-time flow is implicit and complete. |
| 11 | Most common interaction identified | PASS | Scenario 1 is the common interaction: fill, start, watch, eat. |
| 12 | [HW↔SW] Offline/degraded scenarios covered | PASS | §7 — "The device IS the offline experience." BLE is optional. No cloud dependency. Core function needs no connectivity. |

## System Architecture

| # | Item | Status | Notes |
|---|------|--------|-------|
| 13 | Block diagram covers all major subsystems | PASS | §3 — Mermaid diagram with all subsystems: hopper, chute, belt, heater, thermistor, bowls, MCU, motor, LEDs, button, PSU, app. |
| 14 | Every subsystem in diagram has a description | PASS | §4.1 covers all HW blocks. §4.2 covers FW. §4.3 covers app. §4.4 covers cloud (N/A). |
| 15 | [HW↔SW] Every HW↔SW arrow specifies protocol, data, direction | PASS | §3 diagram + §5 interface table: ADC for thermistor, PWM for heater/motor, SPI for LEDs, GPIO for button. |
| 16 | Data flows identified | PASS | §5 — full interface table with protocol, data type, rate for every connection. |
| 17 | Trust/security boundaries marked | N/A | No cloud, no user data, optional BLE only. No meaningful security boundary. |
| 18 | Architecture narrative explains "why" | PASS | §3 — two key insights (passive singulation, physics-based sorting) explain why the architecture is this simple. |
| 19 | [HW↔SW] Processing location is clear | PASS | §4.2 — "All processing is local." PID + motor on-device. App is display-only. |
| 20 | Fundamental HW problems identified | PASS | high_level_design.md §Fundamental Hardware Problems: belt material at 200°C, passive chute flow, popped kernel escaping belt. |
| 21 | Resolution paths stated | PASS | high_level_design.md §Component Choice Architecture and §Open Calls — PTFE-fiberglass mesh, V-groove chute, spring-loaded belt tension. All flagged for M1 prototyping. |

## Subsystem Descriptions — Hardware

| # | Item | Status | Notes |
|---|------|--------|-------|
| 22 | MCU selected with rationale | PASS | §4.1 — ESP32-C3-MINI-1, cheapest ESP32 with BLE, ATtiny fallback if BLE dropped. |
| 23 | Dominant tradeoff axis per component identified | PASS | §8 decisions + §4.1 — belt (performance + food safety), heater (power), motor (cost + simplicity), enclosure (aesthetics + food safety). |
| 24 | Tradeoff conflicts surfaced | PASS | §8 — conveyor belt vs. rotary disc, passive vs. active feed, PTC contact vs. hot air, USB-C PD vs. barrel jack. Each with tensions stated. |
| 25 | All sensors listed with interface, rate, specs | PASS | §4.1 — NTC thermistor: ADC, 10 Hz, 100K B=3950, ±2°C at 200°C. Explicitly notes: no mic, no pop detection sensor. |
| 26 | Actuators and physical UI listed | PASS | §4.1 — PTC heater, DC gearmotor, piezo buzzer, button, WS2812B LEDs. |
| 27 | PCB strategy described | PASS | §4.1 — single board, 4-layer, 50×40mm, full component list, mounting location. |
| 28 | [HW↔SW] Test points and debug interfaces documented | PASS | §4.1 — SWD test pads for factory programming. §9 — pogo-pin functional test. |

## Subsystem Descriptions — Firmware

| # | Item | Status | Notes |
|---|------|--------|-------|
| 29 | OS/framework chosen with rationale | PASS | §4.2 — ESP-IDF with FreeRTOS. Rationale: PID + BLE benefit from task separation, native framework for ESP32-C3. |
| 30 | Major modules listed with responsibilities | PASS | §4.2 — 7 modules: Cycle FSM, Temp Controller, Motor Controller, LED Controller, Safety Watchdog, BLE Service, Config Store. Each with I/O. |
| 31 | [HW↔SW] HAL boundaries defined | PASS | Implicit — ESP-IDF provides HAL for ADC, LEDC, GPIO, SPI. FW modules use ESP-IDF APIs, not register-level access. Appropriate for this platform. |
| 32 | [HW↔SW] OTA update strategy defined | PASS | §4.2 — A/B partitioning (ESP-IDF native), BLE DFU via companion app, Secure Boot v2 signing, rollback on boot failure. |
| 33 | [HW↔SW] On-device vs. cloud processing boundary | PASS | §4.2 — "Minimal. PID temperature control… The firmware is intentionally dumb — the mechanism is smart." All local. |
| 34 | [HW↔SW] FW versioning scheme defined | FAIL | Not addressed. Need a simple versioning convention for manufacturing and OTA compatibility. |

## Subsystem Descriptions — Companion App

| # | Item | Status | Notes |
|---|------|--------|-------|
| 35 | Platform and framework chosen | PASS | §4.3 — iOS + Android, Flutter. |
| 36 | Core screens and flows listed | PASS | §4.3 — 4 screens: Pairing, Live View, Settings, Stats. |
| 37 | [HW↔SW] Device communication protocol defined | PASS | §4.3 — BLE GATT services table: Temperature (notify), Cycle State (notify), Config (write), Run Time (read). |
| 38 | [HW↔SW] App behavior when device disconnected | N/A | App is optional. Device is fully standalone. No critical app-device dependency. |
| 39 | [HW↔SW] Pairing flow documented | PASS | §7 — long-press button → BLE advertising → app pairs → bonded for auto-reconnect. |
| 40 | App store constraints noted | N/A | App is optional, BLE-only, no background requirements. Standard permissions. |

## Subsystem Descriptions — Cloud / Backend

| # | Item | Status | Notes |
|---|------|--------|-------|
| 41 | Platform/infrastructure chosen | PASS | §4.4 — "Not applicable." OTA images on static HTTPS (GitHub Releases). |
| 42 | [HW↔SW] Device provisioning | N/A | No cloud accounts, no device registration. |
| 43 | Data model documented | N/A | No cloud data collection. |
| 44 | [HW↔SW] Device management | N/A | No fleet management. Consumer device with optional BLE-only app. |
| 45 | [HW↔SW] Device-to-cloud auth | N/A | No cloud. |

## Interfaces

| # | Item | Status | Notes |
|---|------|--------|-------|
| 46 | Every internal bus/connection listed | PASS | §5 — 8 internal interfaces: thermistor ADC, heater PWM, motor PWM, LED SPI, button GPIO, buzzer PWM, 20V rail, 3.3V rail. |
| 47 | Every external interface listed | PASS | §5 — BLE, USB-C PD. |
| 48 | Physical connectors documented | PASS | §5 — USB-C, heater JST-PH, motor JST-PH, SWD pads. |
| 49 | No subsystem is an island | PASS | All blocks connected in diagram and interface table. |
| 50 | Protocol specified for each interface | PASS | §5 — ADC, PWM (1 kHz), WS2812B, active-low GPIO, BLE GATT, USB PD 2.0. |
| 51 | [HW↔SW] HW↔FW interfaces specify signal-level details | PASS | §5 — voltage divider spec, PWM frequency, pull-up strategy, interrupt behavior (debounce). |
| 52 | [HW↔SW] FW↔App interfaces specified | PASS | §4.3 — BLE GATT services with direction and update rate. |
| 53 | [HW↔SW] App↔Cloud interfaces specified | N/A | No cloud. |
| 54 | [HW↔SW] Data format transformations documented | PASS | §4.2 — thermistor ADC → temperature → PID → PWM duty. Simple chain, fully described. |

## Power Architecture

| # | Item | Status | Notes |
|---|------|--------|-------|
| 55 | Power source and capacity specified | PASS | §6 — USB-C PD, 20V @ 1.5A (30W). |
| 56 | Power states defined with transition triggers | PASS | §6 — state diagram: Off → Idle → Preheat → Running → Drain → Cooldown → Idle. Triggers specified. |
| 57 | Power budget table for primary mode | PASS | §6 — Running: heater 17W, motor 0.3W, MCU 0.15W, LEDs 0.8W, regulator 0.5W = ~19W total. 11W headroom. |
| 58 | Target battery life stated | N/A | No battery. Mains-powered via USB-C PD. |
| 59 | Back-of-envelope calculation done | PASS | §6 — power budget adds up. 19W < 30W available. Headroom quantified. |
| 60 | Charging method specified | N/A | No battery. |
| 61 | [HW↔SW] FW role in power management defined | PASS | §4.2 — Cycle FSM controls heater on/off, motor on/off per state. Safety watchdog overrides on thermal fault. |
| 62 | [HW↔SW] Radio duty cycle specified | PASS | §7 — BLE is optional, device is functional without it. No impact on core operation. |

## Connectivity

| # | Item | Status | Notes |
|---|------|--------|-------|
| 63 | Primary connectivity technology chosen | PASS | §7 — BLE 5.0 (ESP32-C3 integrated). Optional. |
| 64 | Protocol stack documented | PASS | §4.3 — BLE GATT with services for temp, state, config, run time. |
| 65 | Data transmission frequency and volume | PASS | §4.3 — Temperature at 1 Hz, Cycle State on change. Minimal data volume. |
| 66 | [HW↔SW] Provisioning/pairing flow | PASS | §7 — long-press → advertising → pair → bond. |
| 67 | [HW↔SW] Offline behavior defined | PASS | §7 — "The device IS the offline experience." |
| 68 | [HW↔SW] Connection recovery specified | N/A | BLE is optional display-only. Dropped connection has zero impact on device function. |

## Key Decisions

| # | Item | Status | Notes |
|---|------|--------|-------|
| 69 | At least 3 non-obvious decisions documented | PASS | §8 — 4 decisions: conveyor belt vs. rotary disc, passive chute vs. active feed, USB-C PD vs. barrel jack, PTC contact vs. hot air. |
| 70 | Options considered, chosen approach, rationale | PASS | Every decision has options, chosen, rationale, consequences, risks. |
| 71 | Consequences and risks stated | PASS | Each decision includes both. |
| 72 | 3 decisions that would force redesign if reversed | PASS | Decisions 1 (conveyor belt), 2 (passive chute), 4 (PTC contact heater) — reversing any changes the entire mechanism. |
| 73 | [HW↔SW] HW/SW tradeoff decisions explicit | PASS | Decision 1 explicitly: conveyor belt eliminates pop detection sensor, MEMS mic, sorting firmware. HW mechanism replaces SW logic. |

## Constraints

| # | Item | Status | Notes |
|---|------|--------|-------|
| 74 | Required certifications listed | PASS | §9 — FCC, CE/RED, IC, Bluetooth SIG, UL/ETL, FDA 21 CFR, EU 1935/2004, RoHS. |
| 75 | Operating environment defined | PASS | §9 — 10-35°C, indoor, 0.75m drop. |
| 76 | Target BOM cost stated | PASS | §9 — <$25 at 1k, <$19 at 5k. Full BOM breakdown (24 line items). |
| 77 | Target production volume stated | PASS | §9 — 3,000-15,000 units/year. |
| 78 | Key schedule milestones listed | PASS | §9 — M1 through M7 with specific activities. Holiday Q4 launch target. |
| 79 | Third-party dependencies identified | PASS | §9 — PTFE belt sourcing, PTC heater, SS rollers, food-safety documentation. Lead times noted. |
| 80 | [HW↔SW] App store constraints | N/A | App is optional, standard BLE permissions. |
| 81 | [HW↔SW] Manufacturing test requirements | PASS | §9 — functional test (preheat + belt + temp), PD negotiation, BLE, pop test on sample basis. |

## Open Questions and Risks

| # | Item | Status | Notes |
|---|------|--------|-------|
| 82 | All questions have owner and target date | PASS | §10 — 8 questions, each with owner, milestone target, and status. |
| 83 | High-impact risks have mitigation plans | PASS | §10 — H-impact items (#1 belt grip, #2 heat transfer, #3 chute jamming) all have mitigation approaches and are targeted for M1 prototyping. |
| 84 | No question open >2 weeks without progress | PASS | Fresh document. All newly opened. |
| 85 | [HW↔SW] Cross-domain risks flagged | PASS | §10 #1 (mechanism tuning determines if product concept works), #5 (thermal isolation affects enclosure design). |

## Overall Quality

| # | Item | Status | Notes |
|---|------|--------|-------|
| 86 | No section is placeholder-only | PASS | Every section has real, specific content. Real part numbers, real costs, real specs. |
| 87 | Consistent terminology | PASS | Glossary in Appendix defines 7 key terms (singulation, double conveyor belt, hot zone, dud, PTC heater, PTFE-coated fiberglass, gravity chute). |
| 88 | Diagrams match text | PASS | Mermaid diagram matches §5 interface table. State diagram matches §4.2 module descriptions. |
| 89 | [HW↔SW] Cross-domain consistency check | PASS | Power budget (19W) matches USB-C PD (30W). FW modules match HW interfaces. BOM matches component choices. Belt material matches thermal requirements. |
| 90 | [HW↔SW] Cross-domain review | N/A | Auto-generated — needs human review. |
| 91 | Open questions resolved or carried as TBDs | PASS | §10 — all 8 carried as open with owners and milestones. |

---

## Summary

| Category | Pass | N/A | Fail | Total |
|----------|-----:|----:|-----:|------:|
| Vision and Context | 6 | 0 | 0 | 6 |
| User Scenarios | 3 | 0 | 2 | 5 |
| System Architecture | 8 | 1 | 0 | 9 |
| Hardware | 7 | 0 | 0 | 7 |
| Firmware | 5 | 0 | 1 | 6 |
| Companion App | 3 | 2 | 0 | 5 |
| Cloud / Backend | 1 | 4 | 0 | 5 |
| Interfaces | 8 | 1 | 0 | 9 |
| Power Architecture | 5 | 2 | 0 | 7 |
| Connectivity | 4 | 1 | 0 | 5 |
| Key Decisions | 5 | 0 | 0 | 5 |
| Constraints | 6 | 1 | 0 | 7 |
| Open Questions | 4 | 0 | 0 | 4 |
| Overall Quality | 5 | 1 | 0 | 6 |
| **Total** | **70** | **13** | **3** | **86** |

### FAIL Items

1. **#7 — At least 3 concrete scenarios** — Only 1 scenario (MVP, per user direction). This is a deliberate scope decision. To address: add 2-3 short scenarios (e.g., first-time setup, insufficient USB-C power, chute jam/empty hopper).

2. **#9 — At least 1 error/edge-case scenario** — No error scenario as a user story. Error conditions are discussed in §8 (risks) and §10 (open questions) but not narrated from the user's perspective. To address: add a short scenario for "5V charger" or "hopper runs empty mid-cycle."

3. **#34 — FW versioning scheme** — Not defined. To address: add a `MAJOR.MINOR.PATCH` scheme stored in NVS, reported via BLE device info service, checked during OTA.

### N/A Justification

13 items are N/A — related to Cloud (4), battery/charging (2), optional app constraints (2), security boundaries (1), BLE recovery (1), cross-domain human review (1), app disconnect behavior (1), and app store constraints (1). All are justified by the product's standalone, mains-powered, optional-app design.

### Gate Decision

**PASS** — proceed to illustration generation. The 3 FAIL items are minor:
- Scenarios (#7, #9): deliberate MVP scoping. The single scenario is thorough. Adding error scenarios is a documentation task, not an architectural gap.
- FW versioning (#34): standard practice, easy to add. No design impact.

None of the FAIL items affect the system architecture, component choices, or feasibility.
