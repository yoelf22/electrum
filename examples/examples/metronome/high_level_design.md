### Haptic Metronome Bracelet — High-Level System Design

**Date:** 2026-02-22 | **Author:** | **Status:** Draft

#### What It Is

A wrist-worn bracelet that delivers precise vibrotactile beat pulses to a musician's wrist, configured entirely from a BLE companion app. Tap the bracelet to start, double-tap to stop. No audible output — the beat is private, silent, and felt through the skin. Built for practice, rehearsal, and live performance where audible metronomes are impractical or distracting.

#### Block Diagram

```
  ┌──────────────────────────────────────────────────────┐
  │              Haptic Metronome Bracelet                │
  │                                                      │
  │  ┌──────────────┐          ┌──────────────────┐      │
  │  │Accelerometer │──I2C────→│  MCU (nRF52832)  │      │
  │  │ LIS2DH12     │  + INT   │                  │      │
  │  └──────────────┘          │  Timing engine,  │      │
  │                            │  BLE stack,      │      │
  │  ┌──────────┐              │  gesture detect, │      │
  │  │ 1× LED   │←───GPIO────│  haptic control  │      │
  │  │ (sanity) │              │                  │      │
  │  └──────────┘              └──┬───────────────┘      │
  │                               │ PWM                  │
  │  ┌──────────────┐          ┌──▼──────────┐           │
  │  │ LiPo 150mAh  │          │ Haptic      │           │
  │  │ + USB-C chg   │          │ driver IC   │           │
  │  └──────────────┘          │ + LRA motor │           │
  │                            └─────────────┘           │
  └──────────────────────────────┬───────────────────────┘
                                 │
                    BLE GATT     │
                                 ▼
                        ┌──────────────┐   HTTPS   ┌────────┐
                        │ Companion    │←─────────→│ Cloud  │
                        │ App (mobile) │           │ (OTA)  │
                        └──────────────┘           └────────┘
```

#### Subsystems

| Subsystem | Purpose | Domain |
|-----------|---------|--------|
| MCU + firmware (nRF52832) | Hardware-timer–driven beat generation, haptic pulse shaping, BLE stack, accelerometer gesture detection, LED control, power management | FW |
| Haptic output (DRV2605L driver + LRA motor) | Deliver crisp vibrotactile pulses to the wrist — accented beats stronger/longer, normal beats lighter | HW+FW |
| Accelerometer (LIS2DH12) | Detect tap (start) and double-tap (stop) gestures; reject playing motion | HW+FW |
| Sanity LED (1× green) | Flash on beat for first 4–8 bars after start, then off | HW |
| Power (3.7V 150mAh LiPo + USB-C charging) | 8+ hours continuous use, charge via USB-C | HW |
| Wristband + pod enclosure | Comfortable band, rigid pod housing electronics, motor in firm skin contact | Mech |
| Companion app (iOS/Android) | All configuration: BPM, time signature, accent patterns, presets, practice logging, OTA | SW |
| Cloud backend | Firmware image hosting | Cloud |

#### Key Interfaces

| From → To | What Crosses | Protocol / Medium |
|-----------|-------------|-------------------|
| Accelerometer → MCU | Tap/double-tap interrupt + raw acceleration | I2C (400 kHz) + GPIO interrupt |
| MCU → Haptic driver → LRA | Pulse trigger + waveform selection | I2C (DRV2605L) or PWM |
| MCU → LED | Beat flash (first few bars only) | GPIO direct drive |
| MCU ↔ App | BPM, time sig, accent pattern, playback state, presets, FW images | BLE 5.0 GATT |
| App ↔ Cloud | FW binaries | HTTPS/REST |

#### Constraints

| Constraint | Value | Why It Matters |
|-----------|-------|----------------|
| Timing jitter | < 100 µs beat-to-beat | Musicians perceive jitter above ~0.5 ms. Hardware timer + ISR mandatory. |
| Haptic pulse rise time | < 10 ms | Beat must feel crisp, not mushy. Rules out ERM motors at high tempos. Requires LRA. |
| Battery life | > 8 hours continuous at 120 BPM | Full day of rehearsals on one charge. Constrains motor drive current and pulse duration. |
| Pod dimensions | < 35 × 25 × 10 mm | Must sit comfortably on the wrist without interfering with playing. Constrains PCB, battery, and motor. |
| Pod weight | < 20g (pod only, excluding band) | Heavier pods shift during playing and cause discomfort. |
| Sweat resistance | IPX4 minimum | Musicians sweat. Pod and band must handle splash/sweat without failure. |
| BOM cost | < $15 at 5k units | Retail target $45–60. Wearable BOM is tighter than a desktop device. |

#### Three Hardest Problems

1. **Haptic perceptibility during active playing:** A strumming guitarist's wrist experiences moderate repeated transients. A violinist's bowing arm is in constant motion. A singer's wrist is relatively still but they need subtle feedback that doesn't distract from vocal technique. The LRA pulse (~1–2g peak) must be distinguishable from arm motion during playing. This requires: tight skin contact (band/pod design), short and sharp pulses (LRA with fast rise), and possibly different vibration frequency than instrument-induced vibration. If musicians can't feel the beat while playing, the product doesn't work.

2. **Tap gesture detection during playing motion:** The accelerometer sees arm motion during playing. A tap-to-start gesture must be reliably distinguished from bowing, strumming, and piano arm movement. The detection algorithm needs a distinctive signature — likely a sharp impulse perpendicular to the wrist surface (tapping the pod with a fingertip) vs. the broader, multi-axis motion of playing. False start rate must be near zero; missed tap rate must be < 5%.

3. **Downbeat differentiation through vibration alone:** Musicians need to feel beat 1 differently from beats 2–3–4 to maintain their place in the measure. The only channel is vibration intensity/duration/pattern. The proposed approach uses a **dual-pulse** for beat 1 (two short taps ~40 ms apart — a "da-dum" feel) vs. a **single pulse** for other beats. This is more perceptible than amplitude differences alone, which are hard to distinguish on a vibrating limb. The dual-pulse pattern must be validated with musicians at tempos up to 200 BPM (where inter-beat interval is 300 ms and the 40 ms double-tap must not blur into the next beat).

#### Fundamental Hardware Problems

| Problem | Why It's Fundamental |
|---------|---------------------|
| Delivering a perceptible vibrotactile pulse through the wrist during active instrument playing | This is the product's entire output modality. If the pulse can't be felt during playing, no amount of software can fix it. Depends on motor type, drive strength, skin contact pressure, and vibration frequency vs. instrument-induced noise. |
| Fitting MCU + BLE antenna + accelerometer + haptic driver + LRA motor + 150mAh battery in a wrist-wearable pod < 35×25×10 mm | The form factor is the product. Too large and it interferes with playing or looks awkward. Every component competes for space in a very small volume. |
| Reliable tap detection on a vibrating limb | The input modality (tap gesture) and the operating environment (active instrument playing) are in direct conflict. The accelerometer sees the same axis for both. Signal processing must separate them. |

#### Component Choice Architecture

| Component | Dominant Axis | Key Tension | Resolution Direction |
|-----------|--------------|-------------|---------------------|
| MCU (nRF52832) | Firmware complexity | Same as tabletop version — integrated BLE is worth the premium. No change. | nRF52832 — proven, same platform across product line |
| Haptic motor | Performance | LRA ($1.50–3.00) has 5 ms rise time but needs tuned driver; ERM ($0.30) is cheap but 20–50 ms rise makes beats mushy above 160 BPM | LRA — crisp pulses are non-negotiable for a metronome |
| Haptic driver | Firmware complexity vs. cost | DRV2605L ($1.50) has built-in waveform library and auto-resonance tracking for LRA; raw PWM drive is cheaper but needs custom tuning per motor | DRV2605L — auto-resonance saves weeks of motor-specific tuning |
| Accelerometer | Firmware complexity | LIS2DH12 ($0.80) has built-in tap/double-tap detection in hardware — offloads gesture detection from MCU | LIS2DH12 — hardware tap detection reduces FW complexity and power |
| Battery | Physical constraint | 150 mAh fits the pod; 250 mAh gives more life but adds 3 mm height and 3g weight | Start with 150 mAh, validate battery life on prototype; upgrade if needed |

#### Open Calls

| Decision | Options | Deadline |
|----------|---------|----------|
| Wristband design | Rigid pod + silicone band (watch-style) vs. rigid pod + fabric/velcro band vs. semi-flexible cuff | Before mechanical design — affects pod mounting, skin contact, comfort |
| Downbeat haptic pattern | Dual-pulse ("da-dum", ~40 ms gap) proposed for beat 1 — validate with musicians at 120–200 BPM that it's perceptible and distinct from single-pulse normal beats | Before firmware — needs user testing |
| Tap gesture algorithm | LIS2DH12 hardware tap detection vs. custom firmware algorithm with tunable thresholds per instrument | Before firmware development — hardware tap may not be configurable enough |
| LED behavior | First 4 bars only vs. first 8 bars vs. user-configurable duration vs. always-on option in app | Before firmware — minor, but affects UX |
