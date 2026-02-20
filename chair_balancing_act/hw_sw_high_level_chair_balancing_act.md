### Chair Balancing Act — High-Level System Design

**Date:** 2026-02-20 | **Author:** | **Status:** Draft

#### What It Is

A clip-on device that plays escalating audio feedback when a chair tilts. A small MCU reads an accelerometer, filters out fidgeting, maps sustained tilt to audio zones, and triggers sound clips on a playback IC. Balanced = silence. Tilting = sounds. More tilt = louder, more urgent, or funnier. Part safety device, part office prank.

#### Block Diagram

```
  ┌──────────────────────────────────────────────┐
  │            Chair Balancing Act               │
  │                                              │
  │  ┌──────────────┐      ┌───────────────┐     │
  │  │Accelerometer │─I2C─→│  MCU          │     │
  │  └──────────────┘      │  Tilt filter, │     │
  │                        │  zone mapping,│     │
  │  ┌──────────┐          │  calibration  │     │
  │  │ Button   │───GPIO──→│               │     │
  │  │ On/Mode  │          └───────┬───────┘     │
  │  └──────────┘                  │ GPIO        │
  │                                ▼             │
  │  ┌──────────┐         ┌──────────────┐       │
  │  │ Coin cell│         │ Audio        │       │
  │  │ or LiPo  │         │ playback IC  │       │
  │  └──────────┘         │ + speaker    │       │
  │                       └──────────────┘       │
  └──────────────────────────────────────────────┘
```

#### Subsystems

| Subsystem | Purpose | Domain |
|-----------|---------|--------|
| Accelerometer | Measure tilt angle on pitch and roll axes | HW |
| MCU + firmware | Read accelerometer, filter transients from sustained tilt, map angle to audio zone, auto-calibrate baseline on power-up | FW |
| Audio playback IC + speaker | Store sound clips in flash, play the clip the MCU selects for the current tilt zone | HW |
| Power (CR2450 coin cell) | Run the device for months — MCU sleeps between accelerometer wake interrupts, user-replaceable cell | HW |
| Button | On/off, mode cycle (serious / comedic / stealth) | HW |

#### Key Interfaces

| From → To | What Crosses | Protocol / Medium |
|-----------|-------------|-------------------|
| Accelerometer → MCU | Tilt data + wake interrupt | I2C + GPIO interrupt |
| MCU → Audio playback IC | Clip selection trigger (which zone, which mode) | GPIO lines |
| Audio IC → Speaker | Amplified audio signal | Direct drive or class-D amp |
| Button → MCU | Mode select, power toggle | GPIO |

#### Attachment

This device is for **fixed-leg chairs only** — school chairs, dining chairs. Not office swivel chairs, not rocking chairs. Fixed legs make the tilt signal clean: the whole chair tilts as one rigid body, and the accelerometer reads it directly.

**Mount:** Under-seat adhesive pad (3M Command-strip style). Flat, rigid coupling. Speaker fires through enclosure edge slots. Button accessible by reaching under. The flat underside of fixed-leg chairs is consistent and predictable — no need to accommodate pedestal bases, 5-star casters, or recline mechanisms.

#### Power Source

**Baseline: coin cell or small LiPo**

| Option | Capacity | Life estimate (8 hrs/day) | Pros | Cons |
|--------|----------|--------------------------|------|------|
| CR2032 coin cell | 220 mAh | ~2-4 weeks (if MCU+accel draw <50µA avg, audio bursts rare) | No charging, cheapest, smallest, user-replaceable | Limited current for speaker bursts (~20mA peak), may brown out during loud clips |
| CR2450 coin cell | 600 mAh | ~6-10 weeks | Same as CR2032 but more headroom | Slightly larger, still current-limited |
| Small LiPo (100-200 mAh) | 100-200 mAh | ~2-6 weeks | Higher burst current for speaker, rechargeable via USB-C | Adds USB-C port, charge IC, cost, and "another thing to charge" |

**Energy harvesting discussion: can chair movement charge the battery?**

Piezoelectric or electromagnetic harvesting from chair rocking is appealing on paper — the product is literally about chair movement. In practice:

- **Available energy is tiny.** A chair tilting back 15° and returning generates roughly 1-10 mJ per cycle (depending on harvester mass and travel). At 20 tilts per hour, that's 20-200 mJ/hr = 5-55 µW average.
- **The device needs ~50-100 µW average** (accelerometer + MCU sleeping, occasional audio bursts). So harvesting could in theory approach break-even on sensing alone, but not cover audio playback spikes (speaker draws 10-50 mW during clips).
- **Harvester adds volume and cost.** A piezo disc or small electromagnetic harvester + rectifier + storage cap adds $1-3 BOM, 5-10g, and mechanical complexity. For a <$8 BOM target, that's significant.
- **The pitch is fun** ("powered by your bad posture") but the math is marginal.

**Verdict:** Not for V1. A CR2450 coin cell is the simplest path — months of life, user-replaceable, no charging. If a V2 moves to LiPo for other reasons (louder speaker, more modes), harvesting could supplement charging as a marketing feature, but it won't replace it.

#### Constraints

| Constraint | Value | Why It Matters |
|-----------|-------|----------------|
| BOM cost | <$8 at 1k units | Gift/novelty price — retail $15-25 |
| Battery life | >2 months on CR2450 | Forget-and-use — no charging, just replace the coin cell |
| Latency | Tilt-to-sound <100ms | Comedy timing — the sound must feel coupled to the physical tilt |
| Size/weight | ~32 mm round × 10 mm tall, ~15g | AirTag-sized — see dimension estimate below |

#### Dimension Estimate

**PCB — dual-sided, 30 × 25 mm:**

| Side | Components |
|------|-----------|
| Top | CR2450 holder (25 mm dia, 5.4 mm tall including cell), button |
| Bottom | MCU (QFN 4×4), accelerometer (LGA 2×2), audio IC (QFP/QFN 5×5), passives |

The coin cell holder defines the PCB width (25 mm). The remaining 5 mm of length accommodates the button and edge-fire speaker pads.

**Speaker:** 13 mm × 2.5 mm piezo disc, mounted inside the enclosure wall, firing through side slots.

**Enclosure:**

| Dimension | Value |
|-----------|-------|
| Diameter / shape | ~32 mm round (or 35 × 28 mm oval) — coin cell sets the minimum |
| Height | ~10 mm (5.4 mm cell + 1.5 mm PCB/components + 1 mm clearance + 2 mm walls) |
| Weight | ~15g (PCB+components ~5g, coin cell ~6g, speaker ~1.5g, enclosure ~2.5g) |

About the size of an AirTag. Mounts flat and hidden under a chair seat.

#### Three Hardest Problems

1. **Getting the thresholds right for different chairs:** Office chairs, dining chairs, and classroom chairs have different resting angles and tilt ranges. Fixed thresholds may be too sensitive on one chair and dead on another. May need a brief calibration step (hold button for 3s = "this is level") or self-calibrating baseline on power-up.

2. **Filtering fidgeting from tilting:** Sitting down, crossing legs, and leaning to grab something all move the accelerometer. The device must only trigger on sustained tilt, not transient motion — a short time-delay or low-pass filter on the interrupt, but without adding enough latency to kill the comedy timing.

3. **Making it actually funny:** The audio clips and their escalation curve are the product. Hardware is trivial — the sound design and tilt-to-sound mapping are what make it a good gift or a returned one. Needs real-world playtesting, not just engineering.

#### Open Calls

| Decision | Options | Deadline |
|----------|---------|----------|
| MCU selection | ATtiny (cheapest, bare-metal) vs. STM32L0 (more GPIO, low power) vs. nRF52 (overkill now, but BLE-ready if app added later) | Before schematic |
| Audio content | Pre-loaded fixed set vs. USB-swappable clips vs. multiple built-in modes | Before audio IC selection |
| Attachment | Under-seat adhesive (primary) + chair-leg clamp accessory — needs prototype testing on 5+ chair types | Before enclosure design |
