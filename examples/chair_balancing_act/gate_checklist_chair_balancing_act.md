# Gate Checklist Validation: Chair Balancing Act

| Field | Value |
|-------|-------|
| Date | 2026-02-20 |
| System Description Version | 0.1 |
| Reviewer | Auto (PRD flow) |
| Result | **PASS with notes** — all applicable items covered; N/A items are justified scope decisions. Updated for continuous escalation model. |

---

## Vision and Context

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1 | Product statement is a single clear sentence | PASS | §1 — "a clip-on tilt sensor that plays escalating audio feedback…" |
| 2 | Problem being solved is stated explicitly | PASS | §1 — chair tilting safety + parental nagging |
| 3 | [HW↔SW] HW vs. SW capabilities stated | PASS | §3 narrative — accelerometer + MCU + audio IC, all on-device |
| 4 | [HW↔SW] Software value on top of hardware is clear | PASS | FW adds filtering, zone mapping, calibration, mode management — not just passthrough |
| 5 | Deployment environment defined | PASS | §1 — indoor, home/school, consumer, self-installed |
| 6 | Expected product lifespan stated | PASS | §1 — 1-2 years, novelty product |

## User Scenarios

| # | Item | Status | Notes |
|---|------|--------|-------|
| 7 | At least 3 concrete scenarios | PASS | 5 scenarios provided |
| 8 | [HW↔SW] Each scenario traces through full stack | PASS | Physical tilt → accel interrupt → FW filter → continuous tone generation via PWM → amp → speaker. No app/cloud layers (N/A). |
| 9 | At least 1 error/edge-case scenario | PASS | Scenario 5 — false trigger on sitting down |
| 10 | [HW↔SW] First-time experience described end-to-end | PASS | Scenario 3 — unboxing to attached in 60 seconds |
| 11 | Most common interaction identified | PASS | Implicit in Scenario 1 — tilt → sound → lean forward |
| 12 | [HW↔SW] Offline/degraded scenarios covered | N/A | No connectivity — device is always "offline." Battery replacement scenario (§2.4) covers the only degraded mode. |

## System Architecture

| # | Item | Status | Notes |
|---|------|--------|-------|
| 13 | Block diagram covers all major subsystems | PASS | §3 — Mermaid diagram with all 5 components |
| 14 | Every subsystem in diagram has a description | PASS | §4.1 (HW), §4.2 (FW), §4.3 (App — N/A), §4.4 (Cloud — N/A) |
| 15 | [HW↔SW] Every HW↔SW arrow specifies protocol, data, direction | PASS | §3 diagram labels + §5 interface table |
| 16 | Data flows identified | PASS | §5 — full interface table with protocol, data, rate |
| 17 | Trust/security boundaries marked | N/A | No connectivity, no external interfaces, no user data. No meaningful security boundary exists. |
| 18 | Architecture narrative explains "why" | PASS | §3 — explains the interrupt-driven sleep/wake approach and why no connectivity |
| 19 | [HW↔SW] Processing location is clear | PASS | §4.2 — "All processing is local" |
| 20 | Fundamental HW problems identified | PASS | Covered in hw_sw_high_level_chair_balancing_act.md (referenced doc) |
| 21 | Resolution paths stated | PASS | High-level doc has resolution directions for each |

## Subsystem Descriptions — Hardware

| # | Item | Status | Notes |
|---|------|--------|-------|
| 22 | MCU selected with rationale | PASS | §4.1 — ATtiny1616, cost-driven, with STM32L0 fallback |
| 23 | Dominant tradeoff axis per component identified | PASS | §8 decisions cover all major components; high-level doc has full component choice architecture |
| 24 | Tradeoff conflicts surfaced | PASS | §8 — piezo vs. dynamic speaker (size vs. sound quality), ATtiny vs. nRF52 (cost vs. BLE path) |
| 25 | All sensors listed with interface, rate, specs | PASS | §4.1 sensor table |
| 26 | Actuators and physical UI listed | PASS | §4.1 — piezo, button, no LEDs/display (justified) |
| 27 | PCB strategy described | PASS | §4.1 — dual-sided, 30×25mm, 2-layer FR4, component placement detailed |
| 28 | [HW↔SW] Test points and debug interfaces documented | PASS | §4.1 — UPDI programming pads, I2C test points, power rails |

## Subsystem Descriptions — Firmware

| # | Item | Status | Notes |
|---|------|--------|-------|
| 29 | OS/framework chosen with rationale | PASS | §4.2 — bare-metal, justified by simplicity and power |
| 30 | Major modules listed with responsibilities | PASS | §4.2 — 8 modules with I/O table (tone generator + escalation curves replace zone mapper + audio trigger) |
| 31 | [HW↔SW] HAL boundaries defined | PASS | Implicit — bare-metal on ATtiny, FW talks directly to I2C registers and GPIO. Acceptable for this complexity level. |
| 32 | [HW↔SW] OTA update strategy defined | PASS | §4.2 — "None. No wireless connectivity." Explicitly accepts the risk. |
| 33 | [HW↔SW] On-device vs. cloud processing boundary | PASS | §4.2 — "All processing is local." |
| 34 | [HW↔SW] FW versioning scheme defined | GAP | Not addressed. Minor for a no-connectivity product, but useful for manufacturing traceability. |

## Subsystem Descriptions — Companion App

| # | Item | Status | Notes |
|---|------|--------|-------|
| 35-40 | All app items | N/A | §4.3 — "Not applicable." Justified: zero-setup simplicity is the product's appeal. |

## Subsystem Descriptions — Cloud / Backend

| # | Item | Status | Notes |
|---|------|--------|-------|
| 41-44 | All cloud items | N/A | §4.4 — "Not applicable." No data collection, no accounts. |

## Interfaces

| # | Item | Status | Notes |
|---|------|--------|-------|
| 45 | Every internal bus/connection listed | PASS | §5 — I2C, GPIO (interrupt, trigger, button), power rail |
| 46 | Every external interface listed | PASS | §5 — audio output only |
| 47 | Physical connectors documented | PASS | §5 — battery compartment, UPDI header, adhesive pad |
| 48 | No subsystem is an island | PASS | All blocks connected in diagram and interface table |
| 49 | Protocol specified for each interface | PASS | §5 table includes protocol column |
| 50 | [HW↔SW] HW↔FW interfaces specify signal-level details | PASS | §5 — interrupt polarity, I2C speed, pull-up strategy |
| 51 | [HW↔SW] FW↔App interfaces specified | N/A | No app |
| 52 | [HW↔SW] App↔Cloud interfaces specified | N/A | No cloud |
| 53 | [HW↔SW] Data format transformations documented | PASS | §4.2 — raw XYZ → atan2 → angle → filtered angle → dead-band check → escalation curve → PWM frequency + duty cycle |

## Power Architecture

| # | Item | Status | Notes |
|---|------|--------|-------|
| 54 | Power source and capacity specified | PASS | §6 — CR2450, 600 mAh |
| 55 | Power states defined with transition triggers | PASS | §6 — state diagram with 4 states + Off |
| 56 | Power budget table for primary mode | PASS | §6 — sleeping + active budgets with per-component breakdowns |
| 57 | Target battery life stated | PASS | §6 — ~9 months typical, >2 months target |
| 58 | Back-of-envelope calculation done | PASS | §6 — full calculation with daily charge breakdown |
| 59 | Charging method specified | PASS | §6 — "Not rechargeable. User replaces cell." |
| 60 | [HW↔SW] FW role in power management defined | PASS | §6 + §4.2 — sleep manager module, FW controls MCU sleep/wake |
| 61 | [HW↔SW] Radio duty cycle specified | N/A | No radio |

## Connectivity

| # | Item | Status | Notes |
|---|------|--------|-------|
| 62-67 | All connectivity items | N/A | §7 — "Not applicable." |

## Key Decisions

| # | Item | Status | Notes |
|---|------|--------|-------|
| 68 | At least 3 non-obvious decisions documented | PASS | §8 — 4 decisions, each with options/rationale/consequences/risks |
| 69 | Options considered, chosen approach, rationale | PASS | Every decision has this structure |
| 70 | Consequences and risks stated | PASS | Every decision includes both |
| 71 | 3 decisions that would force redesign if reversed | PASS | Decisions 1 (no wireless), 2 (MCU choice), 3 (separate audio IC) — reversing any requires board respin |
| 72 | [HW↔SW] HW/SW tradeoff decisions explicit | PASS | Decision 3 explicitly: audio in dedicated IC vs. MCU-generated |

## Constraints

| # | Item | Status | Notes |
|---|------|--------|-------|
| 73 | Required certifications listed | PASS | §9 — CE, FCC Part 15, RoHS |
| 74 | Operating environment defined | PASS | §9 — 0-50°C, indoor, 1.5m drop |
| 75 | Target BOM cost stated | PASS | §9 — <$8 at 1k, <$5.50 at 10k, with full BOM breakdown |
| 76 | Target production volume stated | PASS | §9 — 5,000-20,000 units/year |
| 77 | Key schedule milestones listed | PASS | §9 — M1 through M5 |
| 78 | Third-party dependencies identified | PASS | §9 — sound designer, enclosure tooling |
| 79 | [HW↔SW] App store constraints | N/A | No app |
| 80 | [HW↔SW] Manufacturing test requirements | PASS | §9 — functional test, UPDI jig, audio IC programming |

## Open Questions and Risks

| # | Item | Status | Notes |
|---|------|--------|-------|
| 81 | All questions have owner and target date | PASS | §10 — 7 questions, each with owner and milestone target |
| 82 | High-impact risks have mitigation plans | PASS | §10 — H-impact items (threshold tuning, audio design) have mitigation approaches |
| 83 | No question open >2 weeks without progress | PASS | Fresh document — all newly opened |
| 84 | [HW↔SW] Cross-domain risks flagged | PASS | §10 #1 (FW threshold tuning depends on HW chair testing), #4 (FW filter depends on real-world accelerometer behavior) |

## Overall Quality

| # | Item | Status | Notes |
|---|------|--------|-------|
| 85 | No section is placeholder-only | PASS | Every section has real content |
| 86 | Consistent terminology | PASS | Glossary in Appendix defines key terms |
| 87 | Diagrams match text | PASS | Mermaid diagram matches §5 interface table |
| 88 | [HW↔SW] Cross-domain consistency check | PASS | Power budget matches component specs, FW modules match HW interfaces, BOM matches component choices |
| 89 | [HW↔SW] Cross-domain review | N/A | Auto-generated — needs human review |
| 90 | Open questions resolved or carried as TBDs | PASS | §10 — all carried as open with owners |

---

## Summary

| Category | Pass | N/A | Gap | Total |
|----------|-----:|----:|----:|------:|
| Vision and Context | 6 | 0 | 0 | 6 |
| User Scenarios | 5 | 1 | 0 | 6 |
| System Architecture | 8 | 1 | 0 | 9 |
| Hardware | 7 | 0 | 0 | 7 |
| Firmware | 5 | 0 | 1 | 6 |
| Companion App | 0 | 6 | 0 | 6 |
| Cloud / Backend | 0 | 4 | 0 | 4 |
| Interfaces | 7 | 2 | 0 | 9 |
| Power Architecture | 7 | 1 | 0 | 8 |
| Connectivity | 0 | 6 | 0 | 6 |
| Key Decisions | 5 | 0 | 0 | 5 |
| Constraints | 7 | 1 | 0 | 8 |
| Open Questions | 4 | 0 | 0 | 4 |
| Overall Quality | 5 | 1 | 0 | 6 |
| **Total** | **66** | **23** | **1** | **90** |

### Gaps to Address

1. **FW versioning scheme** (item #34): Add a simple versioning convention for manufacturing traceability. Recommendation: embed a version byte in the ATtiny EEPROM or flash header (e.g., `MAJOR.MINOR` as two bytes), readable via UPDI during factory test.

### N/A Justification

23 items are N/A — all related to Companion App (6), Cloud (4), Connectivity (6), and specific HW↔SW boundary items that only apply to connected products (7). This is a deliberate, documented scope decision (§4.3, §4.4, §7, §8 Decision 1). The product is standalone by design.

### Gate Decision

**PASS** — proceed to PRD generation. The single gap (FW versioning) is minor and can be resolved during PRD writing.
