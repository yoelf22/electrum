# Gate Checklist Validation: Shusher

| Field | Value |
|-------|-------|
| Date | 2026-02-23 |
| System Description Version | 0.1 |
| Reviewer | Auto (Electrum flow) |
| Result | **PASS with notes** — see gaps below |

---

## Vision and Context

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1 | Product statement is a single clear sentence | PASS | §1 — clear statement with target user, category, benefit, and differentiator |
| 2 | Problem being solved is stated explicitly | PASS | §1 — loud talkers/speakerphone abusers in shared spaces, no passive way to signal |
| 3 | [HW↔SW] HW vs. SW capabilities stated | PASS | §3 — hardware captures and emits audio; firmware runs detection/classification; app adds configuration |
| 4 | [HW↔SW] Software value on top of hardware is clear | PASS | FW provides the intelligence (level analysis, trigger logic, ambient adaptation). App adds personalization (sensitivity, shush style, event log). Without FW, it's just two mics and a speaker. |
| 5 | Deployment environment defined | PASS | §1 — indoor, public shared spaces, consumer, no installation |
| 6 | Expected product lifespan stated | PASS | §1 — 2-3 years |

## User Scenarios

| # | Item | Status | Notes |
|---|------|--------|-------|
| 7 | At least 3 concrete scenarios | PASS | 5 scenarios provided |
| 8 | [HW↔SW] Each scenario traces through full stack | PASS | Scenario 1: loud speech → front mic → firmware trigger → shush playback → speaker → target hears it. Scenario 3 traces unboxing → button → haptic → LED → active. |
| 9 | At least 1 error/edge-case scenario | PASS | Scenario 4 (barista false trigger) and Scenario 5 (low battery) |
| 10 | [HW↔SW] First-time experience described end-to-end | PASS | Scenario 3 — unbox → button press → haptic confirm → aim → working in 10 seconds |
| 11 | Most common interaction identified | PASS | Scenario 1 — place on table, aim, activate, forget |
| 12 | [HW↔SW] Offline/degraded scenarios covered | PASS | §4.3 — device works fully standalone without app. §7 — "the device IS the offline experience." BLE is optional. |

## System Architecture

| # | Item | Status | Notes |
|---|------|--------|-------|
| 13 | Block diagram covers all major subsystems | PASS | §3 — Mermaid diagram with 8 device blocks + app |
| 14 | Every subsystem in diagram has a description | PASS | §4.1 (HW), §4.2 (FW), §4.3 (App), §4.4 (Cloud — minimal) |
| 15 | [HW↔SW] Every HW↔SW arrow specifies protocol, data, direction | PASS | §3 diagram labels + §5 interface tables |
| 16 | Data flows identified | PASS | §5 — full internal and external interface tables with protocol, data, rate |
| 17 | Trust/security boundaries marked | FAIL | No explicit trust boundary discussion. The device-to-app BLE connection is a trust boundary. The audio privacy guarantee ("no audio leaves the device") is stated but not formally modeled as a security boundary. |
| 18 | Architecture narrative explains "why" | PASS | §3 — explains two-mic differential approach, why processing is local, why BLE is optional |
| 19 | [HW↔SW] Processing location is clear | PASS | §4.2 — all audio analysis on-device, core 0. BLE/app logic on core 1. No cloud processing. |
| 20 | Fundamental HW problems identified | PASS | High-level design identifies cardioid porting, speaker directivity, and volume-at-distance as fundamental |
| 21 | Resolution paths stated | PASS | Each has a resolution direction (acoustic porting, waveguide, volume calibration) flagged for prototyping |

## Subsystem Descriptions — Hardware

| # | Item | Status | Notes |
|---|------|--------|-------|
| 22 | MCU selected with rationale | PASS | §4.1 — ESP32-S3, selected for DSP + PDM + BLE integration at $2.50 |
| 23 | Dominant tradeoff axis per component identified | PASS | High-level design component choice architecture table covers MCU, mics, speaker, battery |
| 24 | Tradeoff conflicts surfaced | PASS | §8 — ESP32-S3 power vs. cost (higher draw than nRF5340 but half the price), waveguide vs. enclosure complexity |
| 25 | All sensors listed with interface, rate, specs | PASS | §4.1 — two MEMS mics with PDM interface, 16 kHz sample rate, SNR specs |
| 26 | Actuators and physical UI listed | PASS | §4.1 — speaker, LRA haptic, button, RGB LED (bottom-facing, normally off) |
| 27 | PCB strategy described | PASS | §4.1 — 55mm round, 4-layer, component placement, antenna keep-out, acoustic isolation notes |
| 28 | [HW↔SW] Test points and debug interfaces documented | PASS | §5 — SWD pads (Tag-Connect footprint), noted as factory-access only |

## Subsystem Descriptions — Firmware

| # | Item | Status | Notes |
|---|------|--------|-------|
| 29 | OS/framework chosen with rationale | PASS | §4.2 — ESP-IDF with FreeRTOS, justified by audio peripheral support and dual-core task separation |
| 30 | Major modules listed with responsibilities | PASS | §4.2 — 9 modules with inputs/outputs table |
| 31 | [HW↔SW] HAL boundaries defined | FAIL | Not explicitly addressed. ESP-IDF provides HAL layers for I2S, GPIO, ADC, but the system description doesn't state which firmware modules talk to hardware directly vs. through ESP-IDF abstractions. Minor for this product but a gap. |
| 32 | [HW↔SW] OTA update strategy defined | PASS | §4.2 — A/B partitions, BLE delivery via app, automatic rollback, RSA-3072 signing |
| 33 | [HW↔SW] On-device vs. cloud processing boundary | PASS | §4.2 — "All audio analysis runs on-device. No audio data leaves the device — ever." |
| 34 | [HW↔SW] FW versioning scheme defined | FAIL | Not addressed. Needed for OTA (app must know current version to offer updates) and manufacturing traceability. |

## Subsystem Descriptions — Companion App

| # | Item | Status | Notes |
|---|------|--------|-------|
| 35 | Platform and framework chosen | PASS | §4.3 — Flutter, iOS + Android |
| 36 | Core screens and flows listed | PASS | §4.3 — 5 screens described |
| 37 | [HW↔SW] Device communication protocol defined | PASS | §4.3 — GATT service table with 6 characteristics, purpose, and direction |
| 38 | [HW↔SW] App behavior when device disconnected | FAIL | Not specified. What does the app show when BLE connection drops? Does it cache last-known settings? Does it notify the user? |
| 39 | [HW↔SW] Pairing and authentication flow documented | PASS | §7 — 5-step pairing flow from both perspectives |
| 40 | App store requirements and constraints noted | FAIL | Not addressed. iOS background BLE limits (the app can't maintain a persistent connection when backgrounded), Android battery optimization (BLE scanning restrictions), and permission requirements (Bluetooth, location for BLE scanning on Android) are not discussed. |

## Subsystem Descriptions — Cloud / Backend

| # | Item | Status | Notes |
|---|------|--------|-------|
| 41 | Platform/infrastructure chosen | PASS | §4.4 — static HTTPS endpoint (S3/GitHub Releases) for firmware hosting. No backend. |
| 42 | [HW↔SW] Device provisioning approach defined | N/A | No cloud registration. Devices are standalone. BLE pairing is local. |
| 43 | Data model documented | N/A | No cloud data. No telemetry. Explicitly stated. |
| 44 | [HW↔SW] Device management capabilities | N/A | No fleet management. Individual consumer devices. OTA is app-mediated, not cloud-orchestrated. |
| 45 | [HW↔SW] Device-to-cloud authentication | N/A | No device-to-cloud connection. |

## Interfaces

| # | Item | Status | Notes |
|---|------|--------|-------|
| 46 | Every internal bus/connection listed | PASS | §5 — 9 internal interfaces documented |
| 47 | Every external interface listed | PASS | §5 — BLE, acoustic output, USB-C charging |
| 48 | Physical connectors documented | PASS | §5 — USB-C (charge only), SWD pads |
| 49 | No subsystem is an island | PASS | All blocks connected in diagram and tables |
| 50 | Protocol specified for each interface | PASS | §5 — PDM, I2S, GPIO, ADC, BLE GATT, USB power |
| 51 | [HW↔SW] HW↔FW interfaces specify signal-level details | PASS | §5 — PDM clock/data, I2S BCLK/LRCLK/DIN, GPIO active-low with pull-up, ADC resolution |
| 52 | [HW↔SW] FW↔App interfaces specified | PASS | §4.3 — GATT service table with characteristics and directions |
| 53 | [HW↔SW] App↔Cloud interfaces specified | N/A | No app-to-cloud connection for device operation. Firmware download is a static HTTPS fetch — no API. |
| 54 | [HW↔SW] Data format transformations documented | PASS | §4.2 — PDM → PCM → bandpass filter → RMS → dB comparison → trigger. Full pipeline documented. |

## Power Architecture

| # | Item | Status | Notes |
|---|------|--------|-------|
| 55 | Power source and capacity specified | PASS | §6 — LiPo 1200 mAh, 3.7V nominal |
| 56 | Power states defined with transition triggers | PASS | §6 — state diagram with Off, Active (listening), Active (shushing), Standby |
| 57 | Power budget table for primary mode | PASS | §6 — per-component breakdowns for listening, shushing, and standby |
| 58 | Target battery life stated | PASS | §6 — ~3 days at 4hr/day, ~5.5 days at 2hr/day |
| 59 | Back-of-envelope calculation done | PASS | §6 — daily charge breakdown with usage profile |
| 60 | Charging method specified | PASS | §6 — USB-C, MCP73831, 500 mA, ~2.5 hours |
| 61 | [HW↔SW] FW role in power management defined | PASS | §4.2 — power manager module controls active/standby transitions, battery monitoring via ADC |
| 62 | [HW↔SW] Radio duty cycle and impact on app responsiveness | FAIL | BLE advertising interval stated (1s in active, 2s in standby) but impact on app connection time and responsiveness of GATT notifications not discussed. |

## Connectivity

| # | Item | Status | Notes |
|---|------|--------|-------|
| 63 | Primary connectivity technology chosen with rationale | PASS | §7 — BLE 5.0, justified by low power + phone universality |
| 64 | Protocol stack documented | PASS | §7 — physical through application layer table |
| 65 | Data transmission frequency, payload, daily volume | PASS | §7 — event-driven, 32 bytes/event, <1 KB/day |
| 66 | [HW↔SW] Provisioning/pairing flow described | PASS | §7 — 5-step flow |
| 67 | [HW↔SW] Offline behavior defined for every layer | PASS | §7 — device works standalone, app uses last-stored config |
| 68 | [HW↔SW] Connection recovery specified | FAIL | Not addressed. What happens if BLE drops during an OTA transfer? During a config write? Does the device re-advertise? Does the app auto-reconnect? Chunked OTA needs resume-from-last-chunk capability. |

## Key Decisions

| # | Item | Status | Notes |
|---|------|--------|-------|
| 69 | At least 3 non-obvious decisions documented | PASS | §8 — 4 decisions with full structure |
| 70 | Options considered, chosen approach, rationale | PASS | Every decision follows the template |
| 71 | Consequences and risks stated | PASS | Every decision includes both |
| 72 | 3 decisions that would force redesign if reversed | PASS | Decision 1 (two-mic vs. array — changes PCB and DSP), Decision 2 (ESP32-S3 — changes entire platform), Decision 4 (waveguide — changes enclosure mold) |
| 73 | [HW↔SW] HW/SW tradeoff decisions explicit | PASS | Decision 3 — pre-recorded vs. synthesized shush is a storage-vs-DSP tradeoff |

## Constraints

| # | Item | Status | Notes |
|---|------|--------|-------|
| 74 | Required certifications listed | PASS | §9 — FCC, CE/RED, IC, Bluetooth SIG, RoHS |
| 75 | Operating environment defined | PASS | §9 — 0-45°C, indoor, 1m drop |
| 76 | Target BOM cost stated | PASS | §9 — <$18 at 1k, <$14 at 5k, with full BOM breakdown |
| 77 | Target production volume stated | PASS | §9 — 2,000-10,000 units/year |
| 78 | Key schedule milestones listed | PASS | §9 — M1 through M5-6 |
| 79 | Third-party dependencies identified | PASS | §9 — sound recordings, acoustic simulation, ESP-IDF, Flutter BLE plugin |
| 80 | [HW↔SW] App store constraints | FAIL | Same as item #40. iOS background BLE and Android permissions not discussed. |
| 81 | [HW↔SW] Manufacturing test requirements | PASS | §9 — functional test (audio path loopback), BLE test, battery check, SWD programming, acoustic calibration |

## Open Questions and Risks

| # | Item | Status | Notes |
|---|------|--------|-------|
| 82 | All questions have owner and target date | PASS | §10 — 8 questions with owners and milestone targets |
| 83 | High-impact risks have mitigation plans | PASS | §10 — H-impact items (cardioid porting, false positives, waveguide) have resolution paths or prototyping flags |
| 84 | No question open >2 weeks without progress | PASS | Fresh document — all newly opened |
| 85 | [HW↔SW] Cross-domain risks flagged | PASS | §10 #1 (HW enclosure porting determines FW detection quality), #5 (ESP32 BLE+audio coexistence is HW/FW integration risk) |

## Overall Quality

| # | Item | Status | Notes |
|---|------|--------|-------|
| 86 | No section is placeholder-only | PASS | Every section has real content |
| 87 | Consistent terminology | PASS | Glossary defines 9 key terms including "plausible deniability" |
| 88 | Diagrams match text | PASS | Mermaid diagram matches interface tables |
| 89 | [HW↔SW] Cross-domain consistency check | PASS | Power budget matches ESP32-S3 specs, GATT characteristics match firmware modules, BOM matches component selections, flash size (8 MB) accommodates firmware + 20 shush samples |
| 90 | [HW↔SW] Cross-domain review | N/A | Auto-generated — needs human review |
| 91 | Open questions resolved or carried as TBDs | PASS | §10 — all carried as open with owners |

---

## Summary

| Category | PASS | N/A | FAIL | Total |
|----------|-----:|----:|-----:|------:|
| Vision and Context | 6 | 0 | 0 | 6 |
| User Scenarios | 6 | 0 | 0 | 6 |
| System Architecture | 8 | 0 | 1 | 9 |
| Hardware | 7 | 0 | 0 | 7 |
| Firmware | 4 | 0 | 2 | 6 |
| Companion App | 3 | 0 | 2 | 5 |
| Cloud / Backend | 1 | 4 | 0 | 5 |
| Interfaces | 8 | 1 | 0 | 9 |
| Power Architecture | 7 | 0 | 1 | 8 |
| Connectivity | 4 | 0 | 1 | 5 |
| Key Decisions | 5 | 0 | 0 | 5 |
| Constraints | 6 | 0 | 1 | 7 |
| Open Questions | 4 | 0 | 0 | 4 |
| Overall Quality | 5 | 1 | 0 | 6 |
| **Total** | **74** | **6** | **8** | **88** |

*Note: 2 checklist items collapsed (app items 35-40 evaluated as 5, cloud items 41-45 evaluated as 5).*

### FAIL Items

1. **#17 — Trust/security boundaries not marked.** Add a brief section to the architecture identifying the BLE link as a trust boundary and formalizing the audio privacy guarantee (no raw audio stored or transmitted, only dB levels over BLE).

2. **#31 — HAL boundaries not defined.** Add a note to §4.2 stating that firmware modules use ESP-IDF's I2S driver, GPIO driver, and ADC driver as the HAL — no direct register access.

3. **#34 — FW versioning scheme missing.** Define a semantic versioning scheme (MAJOR.MINOR.PATCH) stored in firmware image header, exposed via a BLE GATT characteristic, and logged during factory test.

4. **#38 — App behavior when device disconnected not specified.** Define: app shows "Disconnected" state, retains last-known settings, attempts auto-reconnect for 30 seconds, then falls back to manual reconnect. Cached settings are editable and pushed on reconnection.

5. **#40 / #80 — App store constraints not addressed.** Add a section covering: iOS background BLE (app loses active BLE connection when backgrounded — real-time level meter stops, but bonded reconnection works on foreground resume), Android location permission for BLE scanning, notification permissions for shush event alerts.

6. **#62 — BLE advertising impact on app responsiveness not discussed.** Add: at 1s advertising interval, initial connection takes 1-3 seconds. GATT notifications for level updates are near-instant once connected. OTA throughput is ~20 KB/s over BLE, firmware image (~1.5 MB) takes ~75 seconds.

7. **#68 — BLE connection recovery not specified.** Add: device re-advertises immediately on disconnect. App auto-reconnects using bonded identity. OTA transfer uses sequence-numbered chunks with CRC — resumes from last acknowledged chunk on reconnection.

### Gate Decision

**PASS with 8 FAIL items.** All FAILs are documentation gaps, not design flaws. The core product architecture is sound. The gaps are concentrated in BLE/app edge cases (disconnection, recovery, platform constraints) and firmware documentation details (versioning, HAL). None require architectural changes — they're additions to the existing system description.

**Recommendation:** Address FAIL items in the next revision before proceeding to detailed firmware development. The hardware design, audio pipeline, and core detection logic can proceed to prototyping now.
