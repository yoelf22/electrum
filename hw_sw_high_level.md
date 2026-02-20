# High-Level System Design for Software-Augmented Hardware

## Purpose

This document produces a **single-page system overview** that sits between the initial concept and the detailed system description. It answers: "What are the major pieces, how do they connect, and what are the hard problems?" — and stops there.

Use it as:
- **An executive summary** attached to the front of the full system description
- **A standalone artifact** for early stakeholder alignment, funding conversations, or partner discussions
- **A gate** before investing days in the detailed system description — if the high-level design doesn't hold together, the details won't either

```
Concept / Idea
    ↓
[Explore] Research, map HW/SW boundary, identify gaps
    ↓
[High-Level Design] ← THIS STEP (single page)
    ↓
[Describe] Full System Description (detailed toolkit)
    ↓
[Gate] Completeness checklist + cross-discipline review
    ↓
PRD
```

---

## Process (half day to 1 day)

**Input:** Rough notes from the Explore phase — you understand the product concept, have researched comparable products, and have a preliminary sense of the HW/SW boundary.

**Steps:**
1. Fill in the template below. Every field should fit in 1-3 lines. If you need more, you're going too deep.
2. Draw the block diagram. Keep it to 4-8 blocks. If you have more, you're at the wrong abstraction level.
3. List the 3 hardest problems. If you can't identify them, you haven't explored enough — go back.
4. Get 30 minutes of feedback from one hardware person and one software person. Adjust.

**Output:** A single-page document (the filled template below) that a new team member, an executive, or a partner can read in 5 minutes and understand what you're building.

**Rule of thumb:** If any section takes more than 15 minutes to write, you're either over-detailing (save it for the full system description) or under-prepared (go back to Explore).

---

## Template

---

### [Product Name] — High-Level System Design

**Date:** YYYY-MM-DD | **Author:** | **Status:** Draft / Reviewed

#### What It Is

[2-3 sentences. What the physical product does, what the software adds, and who it's for.]

#### Block Diagram

```
[Draw 4-8 blocks maximum. Show: physical hardware, firmware, companion app, cloud/backend.
 Label every arrow with what crosses it (data type, protocol).
 Example:

  ┌─────────┐   I2C/SPI    ┌───────────┐   BLE    ┌─────────┐   HTTPS   ┌─────────┐
  │ Sensors │───────────→│ MCU + FW  │←──────→│   App   │←────────→│  Cloud  │
  └─────────┘            └───────────┘        └─────────┘          └─────────┘
       ↑                      ↑
  ┌─────────┐            ┌─────────┐
  │Actuators│            │  Power  │
  └─────────┘            └─────────┘
]
```

#### Subsystems (name and one-line purpose only)

| Subsystem | Purpose | Domain |
|-----------|---------|--------|
| _e.g., Sensor array_ | _Measure temperature and humidity at 1Hz_ | HW |
| _e.g., Main MCU + firmware_ | _Read sensors, run BLE stack, manage power states_ | FW |
| _e.g., Companion app_ | _Display data, configure device, deliver OTA updates_ | SW |
| _e.g., Cloud backend_ | _Store history, manage fleet, push alerts_ | Cloud |

Do not elaborate. One line per subsystem. Save details for the full system description.

#### Key Interfaces

| From → To | What Crosses | Protocol / Medium |
|-----------|-------------|-------------------|
| _Sensors → MCU_ | _Raw readings_ | _I2C at 100kHz_ |
| _MCU ↔ App_ | _Sensor data, config commands, FW images_ | _BLE GATT_ |
| _App ↔ Cloud_ | _Telemetry, device registration, FW binaries_ | _HTTPS/REST_ |

#### Constraints (hard limits only)

| Constraint | Value | Why It Matters |
|-----------|-------|----------------|
| _e.g., Battery life_ | _> 6 months on coin cell_ | _Drives power architecture, limits radio use_ |
| _e.g., BOM cost_ | _< $15 at 10k units_ | _Rules out cellular, limits sensor count_ |
| _e.g., Certification_ | _FCC + CE required_ | _Antenna design and FW radio parameters constrained_ |

List 3-6 constraints. Only include constraints that eliminate design options.

#### Three Hardest Problems

1. **[Problem name]:** [One sentence describing the problem and why it's hard. E.g., "Achieving 6-month battery life with BLE — the power budget allows only 4 transmissions per hour, but the user expects near-real-time data in the app."]

2. **[Problem name]:** [One sentence.]

3. **[Problem name]:** [One sentence.]

These are the problems that will dominate the detailed system description. If you solve these, the rest is execution.

#### Fundamental Hardware Problems

What physical problems must this device solve to exist? These aren't feature requests — they're physics, geometry, and environment problems that constrain every other decision.

List 2-4 problems. For each, state the problem in one sentence and why it's fundamental (not just hard).

| Problem | Why It's Fundamental |
|---------|---------------------|
| _e.g., Rejecting 20°C mains water down to 4°C in a countertop form factor_ | _Defines the thermal system — tank size, PCM mass, compressor power. Everything else fits around this._ |
| _e.g., Sensing tilt angle while mounted to a vibrating surface_ | _If the sensor can't distinguish real tilt from noise, the product doesn't work at all._ |

These are the problems that, if unsolvable, kill the product. The "Three Hardest Problems" section above may overlap — but that section includes software and integration challenges too. This section is strictly about the physics.

#### Component Choice Architecture

Hardware component selection is a multi-axis tradeoff. At the high-level stage, you don't need to pick specific part numbers — but you need to identify which axes matter most for your product and where they conflict.

**The five axes:**

| Axis | What It Means | Example Tension |
|------|--------------|-----------------|
| **Physical constraint** | Size, weight, thermal envelope, mounting geometry | A better sensor exists but it's 3x the footprint and won't fit the enclosure |
| **Performance** | Accuracy, speed, resolution, power efficiency | A higher-resolution ADC improves measurement but doubles current draw |
| **Availability** | Lead times, number of suppliers, end-of-life risk | The ideal MCU is single-sourced with 26-week lead times |
| **Cost** | Per-unit BOM cost at target volume | An integrated module saves board space but costs $4 more than discrete components |
| **Firmware complexity** | How much software effort a component demands | A raw sensor with no built-in processing needs custom firmware DSP; an integrated module with on-chip processing needs only I2C reads |

**How to use this at the high-level stage:**

For each major component (MCU, sensors, actuators, power source, connectivity module), ask:

1. **Which axis dominates?** For a coin-cell device, power efficiency probably wins every tradeoff. For a novelty product at $20 retail, cost dominates. For a medical device, performance and availability dominate.
2. **Where do axes conflict?** Flag these — they're your real decisions. "The cheapest accelerometer has no built-in filtering, so firmware must compensate" is a cost-vs-firmware-complexity tradeoff worth noting.
3. **What's non-negotiable vs. flexible?** A size constraint from the enclosure is physics — you can't negotiate with it. A cost target is a business decision — you can revisit it if the product requires it.

Fill in one row per major component:

| Component | Dominant Axis | Key Tension | Resolution Direction |
|-----------|--------------|-------------|---------------------|
| _e.g., MCU_ | _Cost_ | _Cheapest option (ATtiny) has no BLE; adding BLE later means a board respin_ | _Pick ATtiny for V1, accept no wireless. Revisit for V2._ |
| _e.g., Accelerometer_ | _Firmware complexity_ | _Cheapest part needs custom filtering in FW; $0.50 more gets on-chip motion detection_ | _Spend the $0.50 — saves weeks of firmware tuning._ |
| _e.g., Speaker_ | _Physical constraint_ | _Dynamic speaker is louder but 4mm tall; piezo is 2.5mm but tinny at low frequencies_ | _Piezo — 1.5mm height saving lets us hit 10mm enclosure target._ |

Don't over-analyze. One row, one sentence per field. The goal is to surface tradeoffs, not resolve them — resolution comes in the full system description.

#### Open Calls (decisions that block detailed design)

| Decision | Options | Deadline |
|----------|---------|----------|
| _e.g., Connectivity choice_ | _BLE vs. Wi-Fi_ | _Before system description Phase 2_ |
| _e.g., Edge vs. cloud processing_ | _On-MCU filtering vs. raw-to-cloud_ | _Before firmware architecture_ |

List only decisions that must be made before the full system description can proceed. 2-4 items maximum.

---

## What This Is NOT

- **Not a PRD.** No formal requirements, no acceptance criteria, no priority tiers.
- **Not the full system description.** No subsystem elaboration, no power budget tables, no interface specifications, no firmware module breakdowns.
- **Not a slide deck.** It's a working document. No selling, no vision statements beyond the opening sentence.

If you find yourself adding detail beyond what fits in this template, stop and move to the full system description (`templates/system_description_template.md`).
