### Minimal Metronome — High-Level System Design

**Date:** 2026-02-22 | **Author:** | **Status:** Draft

#### What It Is

A pocket-sized, battery-powered metronome that produces a precise audible click and visual beat indicator, controlled by a rotary encoder on the device and optionally configured via a BLE companion app. Built for practicing musicians who want a physical tempo reference with zero phone dependency for basic use, plus app-based features like time-signature presets, accent patterns, and practice session logging.

#### Block Diagram

```
  ┌──────────────────────────────────────────────────────────┐
  │                    Minimal Metronome                      │
  │                                                          │
  │  ┌──────────────┐          ┌────────────────────┐        │
  │  │Rotary encoder│──GPIO───→│  MCU (nRF52832)    │        │
  │  │+ push button │          │                    │        │
  │  └──────────────┘          │  Timing engine,    │        │
  │                            │  BLE stack,        │        │
  │  ┌──────────────┐          │  audio synthesis,  │        │
  │  │ 4× RGB LEDs  │←─GPIO───│  UI state machine  │        │
  │  │ (beat ring)  │          │                    │        │
  │  └──────────────┘          └──┬─────────┬───────┘        │
  │                               │ I2S/PWM  │ BLE           │
  │  ┌──────────────┐          ┌──▼──────┐   │               │
  │  │ LiPo 500mAh  │          │Class-D  │   │               │
  │  │ + USB-C chg  │          │amp +    │   │               │
  │  └──────────────┘          │speaker  │   │               │
  │                            └─────────┘   │               │
  └──────────────────────────────┼───────────┘               │
                                 │                           │
                    BLE GATT     │                           │
                                 ▼                           │
                        ┌──────────────┐   HTTPS   ┌────────┐
                        │ Companion    │←─────────→│ Cloud  │
                        │ App (mobile) │           │ (OTA)  │
                        └──────────────┘           └────────┘
```

#### Subsystems

| Subsystem | Purpose | Domain |
|-----------|---------|--------|
| MCU + firmware (nRF52832) | Hardware-timer–driven beat generation, audio synthesis, BLE stack, rotary encoder input, LED driving, power management | FW |
| Audio output (class-D amp + 15mm speaker) | Produce sharp, clean click at usable volume (75+ dB at 30cm) with accent differentiation | HW+FW |
| Beat indicator (4× RGB LEDs) | Show current beat position in measure — downbeat accent color, subdivisions optional | HW+FW |
| Rotary encoder + push button | Tempo adjustment (rotate), start/stop (press), tap tempo (double-press) | HW |
| Power (3.7V 500mAh LiPo + USB-C charging) | 10+ hours continuous use, charge via USB-C | HW |
| Companion app (iOS/Android) | Time signature config, accent patterns, preset management, practice session logging, OTA delivery | SW |
| Cloud backend | Firmware image hosting, optional practice log sync | Cloud |

#### Key Interfaces

| From → To | What Crosses | Protocol / Medium |
|-----------|-------------|-------------------|
| Rotary encoder → MCU | Quadrature pulses (CW/CCW) + button press | GPIO with hardware debounce (RC filter) |
| MCU → Class-D amp → Speaker | Audio samples (click waveform) | PWM at 32kHz or I2S, amplified to 0.5W |
| MCU → LEDs | Beat position, color, brightness | GPIO (direct drive or shift register) |
| MCU ↔ App | Tempo, time sig, accent pattern, playback state, presets, FW images | BLE 5.0 GATT (custom service) |
| App ↔ Cloud | FW binaries, practice logs | HTTPS/REST |

#### Constraints

| Constraint | Value | Why It Matters |
|-----------|-------|----------------|
| Timing jitter | < 100 µs beat-to-beat | Musicians perceive jitter above ~0.5 ms; 100 µs gives 5× margin. Eliminates software-loop timing — must use hardware timer + ISR. |
| Battery life | > 10 hours continuous at moderate volume | A full day of practice sessions on one charge. Drives speaker efficiency and amplifier choice. |
| BOM cost | < $12 at 5k units | Retail target $35–45. Allows quality speaker and proper amp but constrains display options. |
| Size | < 70 × 70 × 25 mm | Must sit on a music stand or fit in a gig bag pocket. |
| Audio latency | < 1 ms from timer event to sound | Click must feel "on the beat" — no perceptible delay between LED flash and audio click. |

#### Three Hardest Problems

1. **Sub-100 µs timing jitter under BLE load:** The nRF52 SoftDevice (BLE stack) uses high-priority interrupts that can preempt application code. The beat-generation timer ISR must coexist with BLE radio events without jitter. This requires careful interrupt priority assignment — beat timer at highest app priority — and may need radio event scheduling coordination. Must be measured with an oscilloscope on a prototype.

2. **Click sound quality that musicians will accept:** Phone metronome apps sound fine through phone speakers; a tiny 15mm speaker in a small enclosure must produce a click that is sharp, loud enough (75+ dB at 30cm), and non-fatiguing over hours. The click waveform, speaker selection, enclosure acoustic port design, and amplifier headroom all interact. Needs real-world listening tests with musicians.

3. **BLE configuration without disrupting timing:** Receiving and applying configuration changes (tempo, time signature, accent pattern) from the app over BLE while the metronome is running must not cause audible glitches. Configuration changes must be double-buffered — written to a shadow copy and applied at the next measure boundary or beat boundary.

#### Fundamental Hardware Problems

| Problem | Why It's Fundamental |
|---------|---------------------|
| Producing a clean, loud click from a 15mm speaker in a compact enclosure | The speaker and its acoustic environment ARE the product's primary output. If the click sounds bad or is too quiet, nothing else matters. Speaker size, enclosure volume, port tuning, and amplifier power are all coupled. |
| Hardware timer resolution sufficient for < 100 µs jitter | The product's core promise is timing precision. The MCU's timer peripheral must support interrupt latency well under 100 µs even during BLE radio activity. If the silicon can't deliver this, the product fails. |
| Fitting speaker + battery + PCB + encoder in a 70×70×25 mm enclosure | The speaker needs acoustic volume, the battery needs capacity (500 mAh), the encoder needs shaft height. These compete for space inside a compact enclosure. If they don't fit, either the form factor or the feature set must change. |

#### Component Choice Architecture

| Component | Dominant Axis | Key Tension | Resolution Direction |
|-----------|--------------|-------------|---------------------|
| MCU (nRF52832) | Firmware complexity | An STM32L4 + separate BLE module is cheaper but doubles firmware integration effort; the nRF52 integrates BLE with mature SDK and proven audio paths | Pay the ~$1 premium for nRF52 — saves months of BLE stack integration and gives proven timer + radio coexistence |
| Speaker | Physical constraint vs. performance | A 20mm speaker is louder and fuller but 5mm taller; a 13mm × 2.5mm micro speaker fits but needs careful acoustic porting | Start with 15mm, 3.5mm-tall micro speaker (e.g., CUI CMS-151135-078SP); test SPL in enclosure prototype |
| Amplifier | Cost vs. performance | A discrete class-D (MAX98357, ~$1) gives I2S input and 3.2W; an integrated PAM8302 ($0.60) is simpler but only 2.5W mono analog input | PAM8302 for V1 — analog PWM input from MCU, 2.5W is enough for a 15mm speaker, simpler BOM |
| Battery | Physical constraint | A 500mAh LiPo gives 10+ hours but is 30×20×4mm; a 300mAh fits easier but drops to ~6 hours | 500mAh — battery life is a key differentiator over phone apps that drain the phone |
| Rotary encoder | Cost vs. UX | A $0.30 mechanical encoder has tactile detents (good for BPM steps); a $2 optical encoder is smoother but overkill | Mechanical encoder with 20 detents/revolution — cheap, tactile, musicians like clicky feedback |

#### Open Calls

| Decision | Options | Deadline |
|----------|---------|----------|
| Haptic motor inclusion | Include LRA for silent practice mode (+$1.50 BOM, adds use case) vs. omit for V1 (simpler, cheaper) | Before schematic |
| Display | No display (LEDs + app only) vs. small 0.91" OLED for BPM readout (+$2 BOM, reduces app dependency) | Before schematic |
| Click waveform source | Pure firmware synthesis (PWM waveform table) vs. stored PCM samples in flash (richer sound, uses ~100KB flash) | Before firmware architecture |
| App platform | Native iOS + Android vs. cross-platform (Flutter/React Native) vs. web BLE app | Before app development |
