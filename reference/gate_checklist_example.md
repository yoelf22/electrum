# Gate Checklist Validation: AquaChill

| Field | Value |
|-------|-------|
| Date | 2026-02-24 |
| System Description Version | 0.1 |
| Reviewer | Auto (example) |
| Result | **PASS with notes** — 1 gap (food-grade material documentation), all applicable items covered. |

---

## Vision and Context

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1 | Product statement is a single clear sentence | PASS | §1 — "a countertop water chiller that cools tap water from 20°C to 4°C in under 90 seconds…" |
| 2 | Problem being solved is stated explicitly | PASS | §1 — fridge pitchers are slow, floor coolers are bulky |
| 3 | [HW↔SW] HW vs. SW capabilities stated | PASS | §3 narrative — compressor + tank + sensors are HW; PID control, BLE, filter tracking are FW; temp display + settings are app |
| 4 | [HW↔SW] Software value on top of hardware is clear | PASS | FW adds PID control (vs. simple thermostat), BLE enables app setpoint changes + filter tracking — not just passthrough |
| 5 | Deployment environment defined | PASS | §1 — indoor, kitchen countertop / office break room, consumer, self-installed |
| 6 | Expected product lifespan stated | PASS | §1 — 3–5 years |

## User Scenarios

| # | Item | Status | Notes |
|---|------|--------|-------|
| 7 | At least 3 concrete scenarios | PASS | 5 scenarios provided |
| 8 | [HW↔SW] Each scenario traces through full stack | PASS | Scenario 2: water poured → NTC detects temp rise → PID starts compressor → PWM ramps → tank reaches setpoint → compressor stops. Scenario 3 includes BLE pairing flow. |
| 9 | At least 1 error/edge-case scenario | PASS | Scenario 5 — thermistor failure, safe mode |
| 10 | [HW↔SW] First-time experience described end-to-end | PASS | Scenario 3 — unboxing → plug in → self-test → first chill → app pairing |
| 11 | Most common interaction identified | PASS | Scenario 1 — push lever, pour cold water |
| 12 | [HW↔SW] Offline/degraded scenarios covered | PASS | §7 — device fully functional without app; app shows stale data when disconnected |

## System Architecture

| # | Item | Status | Notes |
|---|------|--------|-------|
| 13 | Block diagram covers all major subsystems | PASS | §3 — Mermaid diagram with all components |
| 14 | Every subsystem in diagram has a description | PASS | §4.1 (HW), §4.2 (FW), §4.3 (App), §4.4 (Cloud — N/A, justified) |
| 15 | [HW↔SW] Every HW↔SW arrow specifies protocol, data, direction | PASS | §3 diagram labels + §5 interface table |
| 16 | Data flows identified | PASS | §5 — full interface table with protocol, data, rate |
| 17 | Trust/security boundaries marked | PASS | §7 — BLE Secure Connections with passkey pairing, AES-CCM encryption |
| 18 | Architecture narrative explains "why" | PASS | §3 — explains PID approach, why BLE not Wi-Fi, why no cloud |
| 19 | [HW↔SW] Processing location is clear | PASS | §4.2 — "All processing is local" — PID on MCU, display in app |
| 20 | Fundamental HW problems identified | PASS | High-level design doc — thermal rejection, noise, BLE antenna near metal |
| 21 | Resolution paths stated | PASS | Each has a stated approach (variable-speed for noise, antenna placement for BLE) |

## Subsystem Descriptions — Hardware

| # | Item | Status | Notes |
|---|------|--------|-------|
| 22 | MCU selected with rationale | PASS | §4.1 — nRF52832, BLE reliability over ESP32 cost savings |
| 23 | Dominant tradeoff axis per component identified | PASS | High-level design component choice architecture table covers all major components |
| 24 | Tradeoff conflicts surfaced | PASS | §8 — nRF52 vs. ESP32 (reliability vs. cost), variable vs. on/off compressor (noise vs. cost + complexity) |
| 25 | All sensors listed with interface, rate, specs | PASS | §4.1 sensor table — NTC ×2 + flow sensor with full specs |
| 26 | Actuators and physical UI listed | PASS | §4.1 — compressor, fan, LEDs, button, dispense valve |
| 27 | PCB strategy described | PASS | §4.1 — 4-layer, 60×40mm, layer stack, component placement, antenna keep-out |
| 28 | [HW↔SW] Test points and debug interfaces documented | PASS | §4.1 — SWD header, §5 physical connectors — Tag-Connect for production |

## Subsystem Descriptions — Firmware

| # | Item | Status | Notes |
|---|------|--------|-------|
| 29 | OS/framework chosen with rationale | PASS | §4.2 — Zephyr RTOS, justified by concurrent PID + BLE tasks |
| 30 | Major modules listed with responsibilities | PASS | §4.2 — 10 modules with I/O table |
| 31 | [HW↔SW] HAL boundaries defined | PASS | Implicit — Zephyr HAL + Nordic SoftDevice provide the HW abstraction. Application code uses Zephyr ADC/GPIO/PWM APIs. |
| 32 | [HW↔SW] OTA update strategy defined | PASS | §4.2 — BLE DFU via MCUboot, dual-bank, Ed25519 signing, auto rollback |
| 33 | [HW↔SW] On-device vs. cloud processing boundary | PASS | §4.2 — "All processing is local. No raw sensor data leaves the device." |
| 34 | [HW↔SW] FW versioning scheme defined | PASS | Implicit in MCUboot — firmware image header contains version. App reads via BLE device info service. |

## Subsystem Descriptions — Companion App

| # | Item | Status | Notes |
|---|------|--------|-------|
| 35 | Platform and framework chosen | PASS | §4.3 — React Native + react-native-ble-plx, iOS + Android |
| 36 | Core screens and flows listed | PASS | §4.3 — 5 screens with descriptions |
| 37 | [HW↔SW] Device communication protocol defined | PASS | §4.3 — GATT service UUID, 4 characteristics with UUIDs, data formats, directions |
| 38 | [HW↔SW] App behavior when device disconnected | PASS | §4.3 — cached last-known state, "Disconnected" banner, auto-reconnect |
| 39 | [HW↔SW] Pairing flow documented | PASS | §7 — 4-step pairing flow from both device and app perspective |
| 40 | App store constraints noted | GAP | Not addressed. iOS background BLE execution limits and Android battery optimization are mentioned in Decision 4 risks but not formally documented as constraints. Minor — add a line to §9. |

## Subsystem Descriptions — Cloud / Backend

| # | Item | Status | Notes |
|---|------|--------|-------|
| 41–44 | All cloud items | N/A | §4.4 — "Not applicable for V1." Justified: no cloud backend, BLE-only direct communication. V2 path noted. |

## Interfaces

| # | Item | Status | Notes |
|---|------|--------|-------|
| 45 | Every internal bus/connection listed | PASS | §5 — ADC, GPIO, PWM, power rails — 10 interfaces detailed |
| 46 | Every external interface listed | PASS | §5 — BLE, mains power |
| 47 | Physical connectors documented | PASS | §5 — barrel jack, SWD, JST connectors, filter bay |
| 48 | No subsystem is an island | PASS | All blocks connected in diagram and interface table |
| 49 | Protocol specified for each interface | PASS | §5 table includes protocol column for every entry |
| 50 | [HW↔SW] HW↔FW interfaces specify signal-level details | PASS | §5 — ADC voltage divider values, PWM frequency, GPIO pin numbers, interrupt polarity |
| 51 | [HW↔SW] FW↔App interfaces specified | PASS | §4.3 + §7 — GATT characteristics, notification rates, data formats |
| 52 | [HW↔SW] App↔Cloud interfaces specified | N/A | No cloud |
| 53 | [HW↔SW] Data format transformations documented | PASS | §4.2 — raw ADC → Steinhart-Hart → °C → PID → PWM duty. §4.3 — int16 at 0.1°C resolution over BLE. |

## Power Architecture

| # | Item | Status | Notes |
|---|------|--------|-------|
| 54 | Power source and capacity specified | PASS | §6 — 24V/3A external adapter, mains-powered |
| 55 | Power states defined with transition triggers | PASS | §6 — state diagram with 5 states |
| 56 | Power budget table for primary mode | PASS | §6 — idle + cooling budgets with per-component breakdowns |
| 57 | Target battery life stated | N/A | Mains-powered — energy cost estimated instead ($0.68/year) |
| 58 | Back-of-envelope calculation done | PASS | §6 — 12.4 Wh/day, 4.5 kWh/year calculation |
| 59 | Charging method specified | N/A | Mains-powered |
| 60 | [HW↔SW] FW role in power management defined | PASS | §4.2 — compressor manager controls on/off/speed, safety monitor can kill compressor |
| 61 | [HW↔SW] Radio duty cycle specified | PASS | §5 — BLE advertising at 500ms (idle), 100ms (first 30s); notification at 1 Hz |

## Connectivity

| # | Item | Status | Notes |
|---|------|--------|-------|
| 62 | Primary connectivity technology chosen with rationale | PASS | §7 — BLE 5.0, justified vs. Wi-Fi |
| 63 | Protocol stack documented | PASS | §7 — physical through application layer |
| 64 | Data transmission frequency, payload, volume | PASS | §7 — 1 Hz notify, 2–4 bytes, ~170 KB/day max |
| 65 | [HW↔SW] Provisioning/pairing flow | PASS | §7 — 4-step flow from both sides |
| 66 | [HW↔SW] Offline behavior defined | PASS | §7 — device fully standalone; app caches + reconnects |
| 67 | [HW↔SW] Connection recovery specified | PASS | §4.3 — auto-reconnect when in range; §7 — bond stored for automatic reconnection |

## Key Decisions

| # | Item | Status | Notes |
|---|------|--------|-------|
| 68 | At least 3 non-obvious decisions documented | PASS | §8 — 4 decisions |
| 69 | Options considered, chosen approach, rationale | PASS | Every decision follows the template |
| 70 | Consequences and risks stated | PASS | Every decision includes both |
| 71 | 3 decisions that would force redesign if reversed | PASS | Decisions 1 (BLE-only), 2 (nRF52832), 3 (variable-speed compressor) — reversing any requires board respin or major mechanical change |
| 72 | [HW↔SW] HW/SW tradeoff decisions explicit | PASS | Decision 3: variable-speed requires PID in firmware vs. simple on/off hysteresis. Decision 2: MCU choice directly affects BLE stack quality. |

## Constraints

| # | Item | Status | Notes |
|---|------|--------|-------|
| 73 | Required certifications listed | PASS | §9 — UL, CE, FCC, Bluetooth SIG, NSF |
| 74 | Operating environment defined | PASS | §9 — 10–38°C, indoor, IPX0 |
| 75 | Target BOM cost stated | PASS | §9 — <$65 at 5k, <$50 at 20k, with full BOM breakdown |
| 76 | Target production volume stated | PASS | §9 — 5,000 (Y1), 20,000 (Y2) |
| 77 | Key schedule milestones listed | PASS | §9 — M1 through M8 |
| 78 | Third-party dependencies identified | PASS | §9 — compressor supplier, nRF52 availability, filter cartridge, BLE library |
| 79 | [HW↔SW] App store constraints | GAP | Mentioned in passing (Decision 4 risks) but not formally documented. Should add iOS BLE background limits and Android battery optimization as explicit constraints in §9. |
| 80 | [HW↔SW] Manufacturing test requirements | PASS | §9 — functional test, leak test, hi-pot, SWD programming, filter flow test |

## Open Questions and Risks

| # | Item | Status | Notes |
|---|------|--------|-------|
| 81 | All questions have owner and target date | PASS | §10 — 7 questions, each with owner and milestone target |
| 82 | High-impact risks have mitigation plans | PASS | §10 — H-impact items (thermal performance, compressor noise, regulatory path) have mitigation approaches or explicit "needs prototype" flags |
| 83 | No question open >2 weeks without progress | PASS | Fresh document — all newly opened |
| 84 | [HW↔SW] Cross-domain risks flagged | PASS | §10 #3 (BLE antenna affected by HW enclosure design), #7 (FW PID tuning depends on thermal prototype HW) |

## Overall Quality

| # | Item | Status | Notes |
|---|------|--------|-------|
| 85 | No section is placeholder-only | PASS | Every section has real content |
| 86 | Consistent terminology | PASS | Glossary in Appendix defines key terms (PID, setpoint, duty cycle, etc.) |
| 87 | Diagrams match text | PASS | Mermaid diagram matches §5 interface table |
| 88 | [HW↔SW] Cross-domain consistency check | PASS | Power budget matches component specs; BLE characteristics match app screens; BOM matches component choices; firmware modules match HW interfaces |
| 89 | [HW↔SW] Cross-domain review | N/A | Example document — needs human review in real use |
| 90 | Open questions resolved or carried as TBDs | PASS | §10 — all carried as open with owners |

---

## Summary

| Category | Pass | N/A | Gap | Total |
|----------|-----:|----:|----:|------:|
| Vision and Context | 6 | 0 | 0 | 6 |
| User Scenarios | 6 | 0 | 0 | 6 |
| System Architecture | 9 | 0 | 0 | 9 |
| Hardware | 7 | 0 | 0 | 7 |
| Firmware | 6 | 0 | 0 | 6 |
| Companion App | 5 | 0 | 1 | 6 |
| Cloud / Backend | 0 | 4 | 0 | 4 |
| Interfaces | 7 | 1 | 0 | 8 |
| Power Architecture | 6 | 2 | 0 | 8 |
| Connectivity | 6 | 0 | 0 | 6 |
| Key Decisions | 5 | 0 | 0 | 5 |
| Constraints | 7 | 0 | 1 | 8 |
| Open Questions | 4 | 0 | 0 | 4 |
| Overall Quality | 5 | 1 | 0 | 6 |
| **Total** | **85** | **8** | **2** | **89** |

*Note: Item count is 89, not 90 — items 41–44 are grouped as one row in the Cloud section.*

### Gaps to Address

1. **App store constraints** (item #40 / #79): Add a subsection to §9 documenting iOS background BLE execution limits (Core Bluetooth background modes, ~10s execution window on wake) and Android battery optimization (Doze mode, app standby buckets). These affect filter replacement notification reliability.

### N/A Justification

8 items are N/A — 4 for Cloud/Backend (no cloud in V1, justified in §4.4), 2 for battery/charging (mains-powered), 1 for App↔Cloud interface (no cloud), 1 for cross-domain review (example document). All are deliberate scope decisions.

### Gate Decision

**PASS** — proceed to next phase. The 2 gaps (app store constraints documentation) are minor and can be addressed with a few lines added to §9.
