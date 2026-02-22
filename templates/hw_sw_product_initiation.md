# Workflow: From Idea to System Description to PRD for Software-Augmented Hardware

## Overview

This workflow is for products where physical hardware and software (firmware, companion apps, cloud services) must be designed together. The key challenge: hardware and software have different iteration speeds, different risk profiles, and different teams — but they share interfaces, constraints, and a single user experience.

Four phases:

1. **Explore** — Map the hardware/software boundary and identify knowledge gaps
2. **High-Level Design** — Produce a single-page system overview: subsystems, interfaces, constraints, and hard problems
3. **Describe** — Write the full system description iteratively, hardware and software in lockstep
4. **Gate** — Validate completeness across both domains, then feed into PRD

The high-level design (`hw_sw_high_level.md`) is a single-page document that captures the major subsystems, their connections, and the hardest problems — without elaboration. It serves as an executive summary or a standalone artifact for early alignment. The full system description builds on it with detailed subsystem specifications, interface contracts, and power/connectivity architecture.

```
Concept / Idea (physical product + software capabilities)
    ↓
[Explore] Research comparable products, map HW/SW boundary, identify gaps
    ↓
[High-Level Design] Single-page overview — blocks, interfaces, constraints, hard problems
    ↓
[Describe] Full System Description (this toolkit)
    ↓
[Gate] Completeness checklist + cross-discipline review
    ↓
PRD (formal requirements — split into HW, FW, SW, and integration tracks)
```

---

## Phase 1: Explore (1-3 days)

**Goal:** Understand the product well enough to draw the hardware/software boundary and start the system description.

**Steps:**
1. Start with whatever you have — a sketch, a conversation, a feature list, a competitor product.
2. **Identify what is hardware vs. software vs. shared.** For each product capability, ask:
   - Does this require a physical component (sensor, actuator, antenna, battery)?
   - Does this require firmware running on embedded hardware?
   - Does this require a companion app, cloud service, or OTA update mechanism?
   - Where does the logic live — on-device, on-phone, or in the cloud?
3. Review `skills_map.md`. For each of the 16 skill areas, ask: "Is this relevant to my product?" For relevant areas where you feel weak, note them — you'll need specialist input later. Pay special attention to areas that span the HW/SW boundary (connectivity, power management, sensor fusion).
4. Research:
   - Look at comparable products (teardowns on iFixit, product pages, FCC filings)
   - Scan relevant datasheets for key components (MCU, sensors, connectivity modules)
   - Review SDK/API documentation for any platforms you plan to build on (e.g., BLE stacks, cloud IoT platforms, mobile frameworks)
   - Check regulatory requirements for your target markets (FCC, CE, UL — hardware constraints that shape software decisions)
5. Make rough notes. No structure needed yet — just capture what you learn.

**Output:** Rough notes, a preliminary HW/SW boundary sketch, a list of knowledge gaps, and confidence that you understand the product concept well enough to describe it architecturally.

---

## Phase 2: High-Level Design (half day to 1 day)

**Goal:** Produce a single-page system overview that captures the major pieces, how they connect, and what's hard — before investing days in the full system description.

**Process:** Follow `hw_sw_high_level.md`. It contains the template and process guidance.

**What you produce:**
- A 2-3 sentence product description
- A block diagram with 4-8 blocks (hardware, firmware, app, cloud) and labeled arrows
- A subsystem table — name and one-line purpose only, no elaboration
- Key interfaces with protocols
- 3-6 hard constraints that eliminate design options
- The 3 hardest problems
- Fundamental hardware problems — the physics, geometry, or environment problems that must be solvable for the product to exist. These are distinct from the "hardest problems" (which include software and integration). If a fundamental hardware problem is unsolvable, the product is dead regardless of how good the software is.
- Component choice architecture — for each major component (MCU, sensors, actuators, power source), identify which tradeoff axis dominates (physical constraint, performance, availability, cost, or firmware complexity) and where axes conflict. You're not picking part numbers yet — you're surfacing the tradeoffs that will drive selection in Phase 3.
- 2-4 open decisions that block detailed design

**Why this step matters:**
- Forces early clarity on the HW/SW boundary before you're deep in details
- Gives executives and partners something to react to in 5 minutes
- Acts as a sanity check — if the high-level design doesn't hold together, the details won't either
- Becomes the executive summary of the full system description

**When to skip:** Only if you've built this exact type of product before and the architecture is obvious. Even then, the single page is useful for alignment.

**Output:** A single-page high-level system design, reviewed by at least one hardware and one software person.

---

## Phase 3: Describe (3-10 days)

**Goal:** Write a complete system description that covers hardware, firmware, software, and — most importantly — their interfaces.

**Setup:**
1. Copy `templates/system_description_template.md` to your project folder
2. Rename it: `system_description_[product_name].md`
3. Fill in the meta section (version, date, author)

**Recommended section order:**

Work through sections in this order. Each section builds on the previous ones:

| Order | Section | Why this order |
|------:|---------|---------------|
| 1 | Product Vision and Context | Anchor everything else — state which capabilities require hardware and which are software-delivered |
| 2 | User Scenarios | Ground the architecture in real use — trace each scenario through HW, FW, and SW layers |
| 3 | System Architecture | Draw the block diagram showing physical hardware, firmware, companion app, and cloud — iterate until it feels right |
| 4 | Connectivity Architecture | Often the pivotal choice that constrains everything else — BLE vs. Wi-Fi vs. cellular shapes power, cost, firmware complexity, and app architecture |
| 5 | Power Architecture | Second major constraint — shapes what the hardware can do, which directly limits software features (sensor polling rates, radio duty cycles, processing budgets) |
| 6 | Subsystem Descriptions | Fill in the blocks from the diagram — for each, specify what runs in hardware and what runs in software |
| 7 | Interfaces | Make every HW↔FW, FW↔App, and App↔Cloud connection explicit — protocols, data formats, update mechanisms |
| 8 | Key Decisions | Document the rationale while it is fresh — especially HW/SW tradeoffs (e.g., "edge processing vs. cloud processing" or "dedicated sensor IC vs. MCU ADC") |
| 9 | Constraints | Capture what is non-negotiable — BOM cost targets, battery life, certifications, app store requirements |
| 10 | Open Questions | Be honest about unknowns — flag cross-domain questions that need both HW and SW input to resolve |

**Tips:**

- **Work in passes.** First pass: fill every section with something, even rough notes. Second pass: add detail and diagrams. Third pass: review for consistency across sections.
- **The block diagram is the spine.** If a section doesn't connect to the block diagram, question whether it belongs. If a block on the diagram has no section, fill the gap.
- **Trace data flows end-to-end.** Pick a user scenario and follow the data from physical sensor → firmware processing → wireless transmission → app display (or the reverse for actuators). If any link in the chain is undefined, you've found a gap.
- **Make the firmware explicit.** Firmware is often the most under-specified layer. For each MCU or embedded processor, note: what RTOS or bare-metal approach, what peripherals it drives, what communication stacks it runs, and how it gets updated in the field.
- **Specify OTA update strategy early.** How firmware and app software get updated after manufacturing is a first-class architectural decision, not an afterthought.
- **Use the prompt questions.** They are in blockquotes in the template. Answer them, then delete the blockquotes when the section is complete.
- **Don't aim for perfection.** The system description is a working document. "Good enough to review" is the bar, not "complete engineering specification."
- **Flag unknowns immediately.** Add them to the Open Questions table with an owner and target date. Don't let unknowns block progress on other sections.
- **Check consistency across domains.** If the power budget says "BLE," make sure the connectivity section also says "BLE" and the app architecture assumes BLE (not Wi-Fi). If the block diagram shows 4 sensors, make sure the firmware section handles 4 sensor drivers and the app shows 4 data streams.

---

## Phase 4: Gate (1-2 days)

**Goal:** Validate the system description is complete enough to drive PRD creation — for both hardware and software tracks.

**Steps:**
1. Run through `checklist.md`. Mark every box. For unchecked items, either fill the gap or document why it's intentionally scoped out.
2. **Cross-domain review.** Get at least two reviewers:
   - Someone from hardware/electrical engineering reviewing the software assumptions
   - Someone from software/firmware reviewing the hardware assumptions
   - The most valuable feedback comes from the boundary — where one domain's assumptions affect the other
3. Resolve or explicitly flag all open questions. "TBD" is acceptable if it has an owner and a date.
4. Confirm the document is internally consistent — diagrams match text, tables match narrative, subsystem count matches the block diagram, and HW/SW interfaces are specified from both sides.
5. **Verify that every interface between hardware and software is described with enough detail** for both teams to begin independent work — signal names, protocols, data formats, timing constraints, and error handling.

**Output:** A reviewed, checked system description ready to serve as PRD input for parallel HW and SW development tracks.

---

## Converting to PRD

The system description is input to the PRD, not replaced by it. Keep both documents alive.

For software-augmented hardware, the PRD typically splits into parallel tracks that share integration requirements:

**What the PRD adds on top of the system description:**

| PRD Element | Derived From |
|-------------|-------------|
| HW requirements (electrical, mechanical, thermal) | System architecture + subsystem descriptions |
| FW requirements (drivers, RTOS tasks, communication stacks) | Subsystem descriptions + interfaces |
| App/cloud requirements (features, APIs, data models) | User scenarios + connectivity architecture |
| Integration requirements (HW↔FW↔SW end-to-end) | Interfaces + user scenarios |
| Formal requirements ("shall" statements) | System description sections 4-7 |
| Acceptance criteria per requirement | Section 15 of skills map (testing strategy) |
| Priority and phasing (MVP vs. V2) | User scenarios + constraints |
| Detailed specs (exact values, tolerances) | System description ranges and targets |
| Verification methods per requirement | Open questions and test strategy |
| Traceability matrix | User scenarios → requirements → subsystems |

**Process:**
1. Walk through each system description section
2. Extract testable requirements — tag each as HW, FW, SW, or Integration
3. Assign priority (must-have / should-have / nice-to-have)
4. Define acceptance criteria for each requirement
5. Map requirements to subsystems (traceability)
6. Identify integration test points where HW and SW requirements meet

---

## File Management

- Keep the system description as a living document alongside the PRD
- Version both in git — markdown diffs well
- When the system description changes, review the impacted PRD sections — changes to an interface often ripple into both HW and SW requirements
- Use the system description for architecture reviews; use the PRD for engineering hand-off
- Archive superseded versions rather than deleting them

---

## Quick Reference

| What | Where | When |
|------|-------|------|
| Assess your skills | `skills_map.md` | Phase 1 |
| Single-page system overview | `hw_sw_high_level.md` | Phase 2 |
| Write the full description | `templates/system_description_template.md` | Phase 3 |
| Validate completeness | `checklist.md` | Phase 4 |
| See a worked example | `examples/smart_sensor_hub.md` | Any time |
