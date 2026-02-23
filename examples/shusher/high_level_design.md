### Shusher — High-Level System Design

**Date:** 2026-02-23 | **Author:** | **Status:** Draft

#### What It Is

A palm-sized, puck-shaped device you place on your café table aimed at a loud talker or speakerphone abuser. It listens continuously; when sustained loud speech from that direction exceeds the ambient baseline, it fires a brief, discreet "shhh" from a forward-facing speaker — then waits. The user aims it manually; the device does the rest. Looks like a coaster or wireless charger. No screens, no visible LEDs during normal operation. Companion app for sensitivity tuning and shush style selection.

#### Block Diagram

```
  ┌──────────────────────────────────────────────────────────┐
  │                        Shusher                           │
  │                                                          │
  │  ┌───────────────┐  I2S/PDM   ┌─────────────────────┐   │
  │  │ Directional   │──────────→│  MCU + DSP          │   │
  │  │ MEMS mic      │           │  (ESP32-S3)         │   │
  │  │ (cardioid     │           │                     │   │
  │  │  front-facing)│           │  • Noise detection  │   │
  │  └───────────────┘           │  • Speech classifier│   │
  │                              │  • Trigger logic    │   │
  │  ┌───────────────┐           │  • Shush playback   │   │
  │  │ Ambient mic   │──PDM────→│  • BLE stack        │   │
  │  │ (rear-facing) │           │  • Power mgmt       │   │
  │  └───────────────┘           └──────────┬──────────┘   │
  │                                         │ I2S           │
  │  ┌───────────────┐              ┌───────▼──────────┐   │
  │  │ LiPo battery  │              │ Class-D amp +    │   │
  │  │ 1200 mAh      │              │ front speaker    │   │
  │  │ + USB-C charge│              │ (w/ waveguide)   │   │
  │  └───────────────┘              └──────────────────┘   │
  │                                                          │
  │            BLE                                           │
  └─────────────┼────────────────────────────────────────────┘
                │
         ┌──────▼──────┐
         │ Companion   │
         │ App (phone) │
         └─────────────┘
```

#### Subsystems

| Subsystem | Purpose | Domain |
|-----------|---------|--------|
| Directional mic (front) | Capture audio from the aimed direction with cardioid pickup pattern | HW |
| Ambient mic (rear) | Capture baseline ambient noise level behind the device for comparison | HW |
| MCU + firmware (ESP32-S3) | Audio capture, front-vs-rear level comparison, speech detection, trigger decision, shush playback, BLE, power management | FW |
| Speaker + waveguide | Deliver the "shhh" sound forward toward the target, with modest directivity from a short acoustic horn/waveguide | HW |
| Class-D amplifier | Drive the speaker at controlled volume — just loud enough for the target to hear at 2–5 meters | HW |
| Battery + charging | 1200 mAh LiPo, USB-C charging, 8+ hours active listening | HW |
| Companion app | Sensitivity adjustment, shush style selection, mode presets, shush event log | SW |

#### Key Interfaces

| From → To | What Crosses | Protocol / Medium |
|-----------|-------------|-------------------|
| Front mic → MCU | Directional audio stream (16-bit, 16 kHz) | PDM or I2S |
| Rear mic → MCU | Ambient audio stream (16-bit, 16 kHz) | PDM |
| MCU → Class-D amp → Speaker | Shush audio waveform | I2S → analog → speaker |
| MCU ↔ App | Sensitivity settings, shush style, mode, event log, battery level | BLE GATT |

#### How Aiming and Detection Work

The device uses **two microphones** instead of a beamforming array:

1. **Front mic** (cardioid MEMS, forward-facing) — sensitive to sound from the aimed direction. Picks up the loud talker.
2. **Rear mic** (omnidirectional MEMS, rear-facing, possibly port-attenuated) — captures ambient café noise behind the device.

The firmware compares the two signals in real time:
- **Front level significantly above rear level + sustained for N seconds + speech-band energy detected** → trigger shush.
- **Front and rear levels similar** → general ambient noise, no trigger.
- **Rear louder than front** → noise is behind the user, ignore.

This front/rear differential approach is simple, cheap (two $0.50 MEMS mics), and avoids complex beamforming DSP. The user's manual aiming provides the spatial selectivity that would otherwise require a mic array.

#### Discretion Model

The device is designed to be socially invisible:

- **Idle state:** No LEDs, no sound, no visible indicators. Looks like a coaster or puck on the table.
- **Listening:** A single tiny LED on the underside pulses slowly — visible only if you pick the device up. Optional, can be disabled.
- **Shush fired:** The speaker produces a brief, natural-sounding "shhh" (0.5–1.5 seconds). At 2–5m distance, it's audible to the target but blends with café ambiance for everyone else. No LED flash, no mechanical sound.
- **Cooldown:** After a shush, the device waits 30–60 seconds before it can fire again. One polite nudge, not harassment.
- **Plausible deniability:** The shush sounds human. No robotic quality, no beeps, no electronic artifacts. The offender should wonder if someone nearby shushed them — not identify a gadget.

#### Constraints

| Constraint | Value | Why It Matters |
|-----------|-------|----------------|
| Battery life | >8 hours active listening | Full workday café session on a single charge |
| Size | ~70 mm diameter × 15 mm tall | Coaster-sized, fits naturally on a café table |
| Shush range | Audible at 2–5 m, not conspicuous beyond 5 m | Must reach the offender's table but not alert the whole room |
| Trigger latency | <2 seconds from onset of loud speech | Fast enough to feel responsive, slow enough to avoid triggering on brief bursts |
| False positive rate | <1 per hour in a typical café | Shushing the wrong person or the barista is a product-killing experience |
| BOM cost | <$18 at 1k units | Target retail $50–70 — niche but real product, not a gag gift |

#### Three Hardest Problems

1. **Distinguishing shush-worthy noise from normal café ambiance:** The front mic will pick up everything in that direction — the target's loud conversation, but also music, other conversations, dish clatter. The classifier must isolate sustained loud speech energy above the ambient baseline (rear mic) and hold for several seconds before triggering. Too sensitive → shushes the espresso machine. Too conservative → never fires. The threshold must adapt to each environment.

2. **Making the shush sound natural and plausibly human:** If the shush sounds electronic, robotic, or obviously from a device, the product fails socially. It needs to sound like a real person shushed — breathy, slightly variable, naturally timed. This is a sound design problem and a playback quality problem (speaker + waveguide + audio file quality). Multiple shush recordings with slight randomization on each firing.

3. **Achieving useful directivity from a small speaker:** A 70mm-wide device with a small speaker and waveguide won't produce a tight beam — maybe ±30° at speech frequencies. That's enough to make the shush louder for the target than for people at 90°, but it's not a laser. The waveguide design and speaker placement need to maximize the forward-to-side ratio within the enclosure constraints.

#### Fundamental Hardware Problems

| Problem | Why It's Fundamental |
|---------|---------------------|
| Forward directivity from a puck-sized enclosure | The shush must be louder in front than to the sides. Physics limits directivity at speech frequencies for a 70mm aperture. If the shush is equally loud in all directions, the product embarrasses the user instead of the offender. |
| Cardioid mic pickup in a small form factor | The front mic needs a cardioid pattern (sensitive to front, rejecting rear) to enable front-vs-rear comparison. MEMS mics are omnidirectional by default; cardioid behavior requires acoustic port design in the enclosure (front and rear ports with tuned delay). If the front mic can't reject rear sound, detection doesn't work. |
| Speaker volume sufficient at 3–5 m without being conspicuous at 1 m | The shush must travel across a café but not be obviously loud at the user's own table. This is a narrow dynamic range window — enough SPL for distance but within ambient levels up close. |

#### Component Choice Architecture

| Component | Dominant Axis | Key Tension | Resolution Direction |
|-----------|--------------|-------------|---------------------|
| MCU (ESP32-S3) | Firmware complexity | Needs audio DSP capability + BLE + enough RAM for dual-mic processing. ESP32-S3 has built-in DSP, 512KB SRAM, BLE 5.0. Cheaper MCUs (ESP32-C3) lack the DSP horsepower for real-time audio. | ESP32-S3 — the audio DSP requirement is non-negotiable. ~$2.50 at volume. |
| Front mic | Firmware complexity | Standard omnidirectional MEMS mic (SPH0645) is cheap ($0.50) but needs acoustic enclosure design for cardioid behavior. A true differential/cardioid MEMS mic exists but is 3x cost. | Start with standard MEMS + acoustic porting. Prototype to validate cardioid rejection ratio. |
| Speaker | Physical constraint | Larger speaker = better low-frequency response and SPL at distance. But enclosure is 70mm × 15mm. A 28mm micro speaker fits but has limited output. | 28mm dynamic micro speaker + short horn waveguide molded into the enclosure front. Optimize for 2–6 kHz (sibilant "shh" energy). |
| Battery | Physical constraint | 1200 mAh LiPo fits in the puck but adds 25g. A smaller 800 mAh cell saves 10g but cuts runtime to ~5–6 hours. | 1200 mAh — 8-hour runtime is more important than 10g weight savings. |

#### Open Calls

| Decision | Options | Deadline |
|----------|---------|----------|
| Cardioid mic implementation | Acoustic porting of standard MEMS mic vs. dedicated cardioid MEMS element | Before enclosure design — acoustic port geometry is part of the enclosure mold |
| Shush sound library | Pre-recorded human shush samples vs. synthesized sibilant noise vs. hybrid | Before firmware audio pipeline — determines storage needs and playback approach |
| Waveguide design | Molded horn in enclosure front vs. ported slot array vs. bare speaker (fallback) | Before enclosure design — integral to the mold |
| App necessity for V1 | Ship with app (more features, BLE required) vs. ship standalone with fixed defaults (simpler, cheaper, no BLE needed at all) | Before schematic — determines whether BLE radio is on the board |
