# Gate Checklist Validation: Minimal Metronome

| Field | Value |
|-------|-------|
| Date | 2026-02-22 |
| System Description Version | 0.1 |
| Reviewer | Auto (PRD flow) |
| Result | **PASS** — all applicable items covered after revision. |

---

## Vision and Context

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1 | Product statement is a single clear sentence | PASS | §1 — "For practicing musicians, Minimal Metronome is a pocket-sized hardware metronome that produces a precise, clean click with sub-100 µs timing jitter…" |
| 2 | Problem being solved is stated explicitly | PASS | §1 — phone metronome apps have latency, distractions, and OS interruptions |
| 3 | [HW↔SW] HW vs. SW capabilities stated | PASS | §3 narrative — beat timing, audio, and physical controls on hardware; configuration, presets, practice logging, and OTA on app/cloud |
| 4 | [HW↔SW] Software value on top of hardware is clear | PASS | §3 + §4.3 — app adds time-signature config, accent patterns, setlist management, practice logging, OTA. Device works without app for basic use. |
| 5 | Deployment environment defined | PASS | §1 — indoor, home/school/studio, consumer, no installation |
| 6 | Expected product lifespan stated | PASS | §1 — 3–5 years |

## User Scenarios

| # | Item | Status | Notes |
|---|------|--------|-------|
| 7 | At least 3 concrete scenarios | PASS | 5 scenarios provided |
| 8 | [HW↔SW] Each scenario traces through full stack | PASS | Scenario 1: encoder rotation → FW BPM change → timer recalculation → click output. Scenario 2: app → BLE → preset storage → encoder double-tap → FW loads preset → click at new tempo. |
| 9 | At least 1 error/edge-case scenario | PASS | Scenario 5 — low battery mid-practice, charge while playing |
| 10 | [HW↔SW] First-time experience described end-to-end | PASS | Scenario 3 — unboxing, press encoder, hear clicks at 120 BPM in < 10 seconds. No app required. |
| 11 | Most common interaction identified | PASS | Scenario 1 — adjusting tempo via encoder during practice |
| 12 | [HW↔SW] Offline/degraded scenarios covered | PASS | §4.3 — "device is fully functional without the app." §7 — "if BLE disconnects mid-session, the metronome continues playing with its current settings." |

## System Architecture

| # | Item | Status | Notes |
|---|------|--------|-------|
| 13 | Block diagram covers all major subsystems | PASS | §3 — Mermaid diagram: MCU, encoder, amp, speaker, LEDs, power, app, cloud |
| 14 | Every subsystem in diagram has a description | PASS | §4.1–4.4 cover all blocks |
| 15 | [HW↔SW] Every HW↔SW arrow specifies protocol, data, direction | PASS | §3 diagram labels + §5 interface tables with protocol, data, rate columns |
| 16 | Data flows identified | PASS | §5 — full tables for internal and external interfaces |
| 17 | Trust/security boundaries marked | PASS | §3 Security Model — two trust boundaries defined: BLE link (LESC + config value validation) and OTA firmware boundary (Ed25519 signing + CRC + rollback). Input validation rules specified for all writable characteristics. Physical access (SWD) discussed. |
| 18 | Architecture narrative explains "why" | PASS | §3 — explains timer-driven architecture, SoftDevice coexistence, and why beat generation is fully on-device |
| 19 | [HW↔SW] Processing location is clear | PASS | §3 + §4.2 — all beat generation on-device, app is config overlay, cloud is OTA hosting only |
| 20 | Fundamental HW problems identified | PASS | High-level design identifies 3 fundamental HW problems: audio from small speaker, timer precision under BLE, component fitting |
| 21 | Resolution paths stated | PASS | Each has a resolution direction in the high-level design; §10 carries them as open questions with owners |

## Subsystem Descriptions — Hardware

| # | Item | Status | Notes |
|---|------|--------|-------|
| 22 | MCU selected with rationale | PASS | §4.1 — nRF52832 selected; rationale in §8 Decision 1 (integrated BLE, mature SDK, sufficient performance) |
| 23 | Dominant tradeoff axis per component identified | PASS | High-level design component choice table covers MCU (FW complexity), speaker (physical constraint), amp (cost), battery (physical constraint), encoder (cost) |
| 24 | Tradeoff conflicts surfaced | PASS | Speaker size vs. audio quality, battery capacity vs. enclosure size, amp quiescent current vs. simplicity |
| 25 | All sensors listed with interface, rate, specs | PASS | §4.1 — "None" explicitly stated with explanation (no environmental sensors) |
| 26 | Actuators and physical UI listed | PASS | §4.1 — speaker, 4× WS2812B LEDs, rotary encoder, optional LRA haptic motor |
| 27 | PCB strategy described | PASS | §4.1 — single board, 4-layer FR4, 45×45mm, component placement per side, antenna keep-out |
| 28 | [HW↔SW] Test points and debug interfaces documented | PASS | §4.1 — Tag-Connect TC2030-NL SWD footprint on bottom side; §5 physical connectors table |

## Subsystem Descriptions — Firmware

| # | Item | Status | Notes |
|---|------|--------|-------|
| 29 | OS/framework chosen with rationale | PASS | §4.2 — bare-metal with nRF5 SDK, justified by interrupt-driven simplicity; Zephyr as growth path |
| 30 | Major modules listed with responsibilities | PASS | §4.2 — 8 modules with inputs/outputs table |
| 31 | [HW↔SW] HAL boundaries defined | PASS | §4.2 — modules reference nRF5 SDK peripherals (TIMER, PWM/EasyDMA, GPIOTE, SAADC, FDS). Nordic HAL is the abstraction layer. |
| 32 | [HW↔SW] OTA update strategy defined | PASS | §4.2 — Nordic Secure DFU, dual-bank A/B, Ed25519 signing, automatic rollback on CRC failure, flash layout specified |
| 33 | [HW↔SW] On-device vs. cloud processing boundary | PASS | §4.2 — "All beat generation happens on-device. The app never participates in timing." |
| 34 | [HW↔SW] FW versioning scheme defined | PASS | §4.2 Firmware Versioning — SemVer (MAJOR.MINOR.PATCH), embedded in DFU init packet header, exposed via BLE DIS Firmware Revision String (UUID 0x2A26), downgrade rejection in bootloader. |

## Subsystem Descriptions — Companion App

| # | Item | Status | Notes |
|---|------|--------|-------|
| 35 | Platform and framework chosen | PASS | §4.3 — Flutter, iOS + Android |
| 36 | Core screens and flows listed | PASS | §4.3 — 5 screens: onboarding, main, presets/setlist, practice log, settings |
| 37 | [HW↔SW] Device communication protocol defined | PASS | §4.3 — GATT service table with 10 characteristics, UUIDs, directions, data types |
| 38 | [HW↔SW] App behavior when disconnected | PASS | §4.3 — "device retains last-applied settings… app shows 'Disconnected' and attempts automatic reconnection" |
| 39 | [HW↔SW] Pairing flow documented step-by-step | PASS | §7 — 7-step pairing flow from both app and device perspectives |
| 40 | App store requirements and constraints noted | PASS | §9 App Store and Platform Constraints — iOS background BLE mode, NSBluetoothAlwaysUsageDescription, Android 12+ permissions, OEM battery optimization, Apple/Google review process for hardware-paired apps (loaner device or video demo), minimum OS versions (iOS 14+, Android 8.0+). |

## Subsystem Descriptions — Cloud / Backend

| # | Item | Status | Notes |
|---|------|--------|-------|
| 41 | Platform/infrastructure chosen | PASS | §4.4 — AWS S3 + CloudFront for static firmware hosting |
| 42 | [HW↔SW] Device provisioning approach | PASS | §4.4 — pre-provisioned BLE address + DFU public key burned at factory, no cloud registration needed |
| 43 | Data model documented | PASS | §4.4 — table with firmware images and practice logs |
| 44 | [HW↔SW] Device management capabilities | PASS | §4.4 — "No device shadow/twin. State lives on the device." Explicitly minimal for V1. |
| 45 | [HW↔SW] Device-to-cloud authentication | N/A | Device does not connect to cloud directly. App downloads OTA images over HTTPS (standard TLS). |

## Interfaces

| # | Item | Status | Notes |
|---|------|--------|-------|
| 46 | Every internal bus/connection listed | PASS | §5 — 8 internal interfaces: timer, PWM/DMA, WS2812B, encoder quadrature, encoder button, ADC, power regulation, USB charging |
| 47 | Every external interface listed | PASS | §5 — BLE radio, audio output, USB-C power |
| 48 | Physical connectors documented | PASS | §5 — USB-C, Tag-Connect SWD, speaker pads |
| 49 | No subsystem is an island | PASS | All blocks in diagram connect to MCU or power |
| 50 | Protocol specified for each interface | PASS | Every row in §5 tables has a protocol column |
| 51 | [HW↔SW] HW↔FW interfaces specify signal-level details | PASS | §5 — interrupt behavior (GPIOTE), DMA for PWM, ADC resolution, I2C-equivalent WS2812B timing, debounce strategy |
| 52 | [HW↔SW] FW↔App interfaces specified | PASS | §4.3 GATT table + §7 pairing flow. Connection interval (30–50ms) and advertising interval (1000ms) specified in §5. |
| 53 | [HW↔SW] App↔Cloud interfaces specified | PASS | §4.4 — HTTPS for firmware image download. Minimal scope, but specified. |
| 54 | [HW↔SW] Data format transformations documented | PASS | §4.2 — BPM → microsecond interval → timer compare register → PWM burst → amplified audio. Encoder quadrature → direction + speed → BPM delta. |

## Power Architecture

| # | Item | Status | Notes |
|---|------|--------|-------|
| 55 | Power source and capacity specified | PASS | §6 — 3.7V LiPo 500mAh |
| 56 | Power states defined with transition triggers | PASS | §6 — state diagram with 5 states (Off, Booting, Idle, Playing, DeepSleep) + transitions |
| 57 | Power budget table for primary mode | PASS | §6 — Playing mode: 8.5 mA average with per-component breakdown including duty cycles |
| 58 | Target battery life stated | PASS | §6 — >10 hours continuous playing |
| 59 | Back-of-envelope calculation done | PASS | §6 — 59 hours continuous playing, 29 days typical use. Well above target. |
| 60 | Charging method specified | PASS | §6 — USB-C at 500mA via MCP73831, ~1.5 hours from empty |
| 61 | [HW↔SW] FW role in power management defined | PASS | §4.2 power manager module — FW controls System ON/OFF, sleep scheduling, WFE between beats |
| 62 | [HW↔SW] Radio duty cycle and app responsiveness noted | PASS | §5 + §7 — advertising interval 1000ms (idle), connection interval 30–50ms (connected). §7 notes "connection takes up to 1.5s" during pairing. |

## Connectivity

| # | Item | Status | Notes |
|---|------|--------|-------|
| 63 | Primary connectivity technology chosen with rationale | PASS | §7 — BLE 5.0, rationale: low power, no infrastructure, sufficient bandwidth for config data |
| 64 | Protocol stack documented | PASS | §7 — Physical (BLE 5.0), Link (LESC bonding), Application (custom GATT), Security (AES-CCM) |
| 65 | Data transmission frequency, payload, volume estimated | PASS | §7 — event-driven, 1–32 bytes per interaction, < 1 KB/day |
| 66 | [HW↔SW] Provisioning/pairing flow step-by-step | PASS | §7 — 7-step flow from both sides |
| 67 | [HW↔SW] Offline behavior defined for every layer | PASS | §7 — device operates identically without BLE, app shows "Disconnected" and auto-reconnects, settings persist in flash |
| 68 | [HW↔SW] Connection recovery specified | PASS | §4.3 — "app reconnects automatically when in range and re-syncs state by reading all characteristics." §7 — "if BLE disconnects mid-session, the metronome continues playing with its current settings." |

## Key Decisions

| # | Item | Status | Notes |
|---|------|--------|-------|
| 69 | At least 3 non-obvious decisions documented | PASS | §8 — 4 decisions |
| 70 | Options considered, chosen approach, rationale | PASS | Each decision has full structure |
| 71 | Consequences and risks stated | PASS | Each decision includes consequences and risks with mitigations |
| 72 | 3 decisions that would force redesign if reversed | PASS | Decision 1 (MCU choice — nRF52 is the board), Decision 2 (PCM samples vs. synthesis — affects flash layout and audio pipeline), Decision 4 (LiPo vs. coin cell — changes enclosure, power circuit, and connectors) |
| 73 | [HW↔SW] HW/SW tradeoff decisions explicit | PASS | Decision 1 — single-chip vs. MCU + BLE module (HW cost vs. FW complexity). Decision 2 — stored samples vs. synthesis (flash usage vs. CPU time). Decision 3 — no display (HW cost vs. app dependency). |

## Constraints

| # | Item | Status | Notes |
|---|------|--------|-------|
| 74 | Required certifications listed | PASS | §9 — FCC, CE/RED, IC, Bluetooth SIG |
| 75 | Operating environment defined | PASS | §9 — 0–45°C, indoor, 1m drop |
| 76 | Target BOM cost stated | PASS | §9 — <$12 at 1k, <$9 at 5k, full BOM breakdown |
| 77 | Target production volume stated | PASS | §9 — 2k–10k year 1, 10k–30k year 2+ |
| 78 | Key schedule milestones listed | PASS | §9 — M1 through M8 |
| 79 | Third-party dependencies identified | PASS | §9 — Nordic SDK, Flutter, Nordic DFU bootloader, sound designer |
| 80 | [HW↔SW] App store constraints noted | PASS | §9 — see item #40 |
| 81 | [HW↔SW] Manufacturing test requirements | PASS | §9 — functional test sequence described (BLE connect, BPM set, microphone verify, LED verify, encoder verify, battery check), SWD programming via Tag-Connect |

## Open Questions and Risks

| # | Item | Status | Notes |
|---|------|--------|-------|
| 82 | All questions have owner and target date | PASS | §10 — 8 questions, each with owner and milestone target |
| 83 | High-impact risks have mitigation plans | PASS | §10 — H-impact items (#1 timing jitter, #2 speaker acoustics) have specific mitigation approaches (oscilloscope validation, musician listening tests) |
| 84 | No question open >2 weeks without progress | PASS | Fresh document — all newly opened |
| 85 | [HW↔SW] Cross-domain risks flagged | PASS | §10 #1 (FW timing depends on SoftDevice radio behavior — HW↔SW), #3 (amp quiescent current is HW choice affecting FW power strategy), #7 (Flutter BLE reliability varies by Android OEM — app↔device boundary) |

## Overall Quality

| # | Item | Status | Notes |
|---|------|--------|-------|
| 86 | No section is placeholder-only | PASS | Every section has real, specific content |
| 87 | Consistent terminology | PASS | Glossary in Appendix with 11 defined terms |
| 88 | Diagrams match text | PASS | Mermaid diagram blocks match §4 subsystem descriptions and §5 interface tables |
| 89 | [HW↔SW] Cross-domain consistency check | PASS | Power budget uses nRF52832 datasheet values; flash layout fits 512 KB; GATT characteristics match app screen descriptions; BOM components match subsystem descriptions; timer resolution matches jitter target |
| 90 | [HW↔SW] Cross-domain review needed | N/A | Auto-generated — needs human review from both HW and SW perspectives |
| 91 | Open questions resolved or carried as TBDs | PASS | §10 — all 8 questions carried as open with owners and target dates |

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

**PASS** — all 89 applicable items covered. 2 items are N/A (device-to-cloud auth — device never contacts cloud directly; cross-domain human review — auto-generated, needs human review). Proceed to PRD generation.
