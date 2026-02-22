# Exploration Notes: Haptic Metronome Bracelet

## Product Summary

A wrist-worn vibrotactile metronome that delivers precise beat pulses through a haptic motor against the skin. Musicians set BPM and time signature from a companion app, then tap the bracelet to start and double-tap to stop. No audible output — the beat is felt, not heard. A single LED provides a brief visual sanity check during the first few bars, then goes dark.

## HW/SW Boundary Analysis

### Must be physical hardware
- **Haptic motor (LRA or ERM)** — the primary beat output. Must deliver a crisp, distinct tap percievable on the wrist at tempo, with enough sharpness to distinguish accented beats from normal beats.
- **Accelerometer** — detects tap (start) and double-tap (stop) gestures on the bracelet. Also enables potential future features (conducting gestures, tap-tempo).
- **Battery** — small LiPo in a wristband form factor. Target: 8+ hours of continuous haptic pulses on a single charge.
- **Single LED** — sanity-check indicator. Flashes on beat for the first 4–8 bars after starting, then turns off to avoid visual distraction.
- **Wristband / enclosure** — comfortable for long practice sessions, secure enough not to shift during playing. The haptic motor must be in firm skin contact for the vibration to be felt clearly.

### Firmware responsibilities
- **Precision timing engine** — hardware timer–driven beat generation with < 100 µs jitter. Identical requirement to an audible metronome.
- **Haptic driver control** — driving the LRA/ERM with shaped pulses. Accented beats get a stronger/longer pulse; normal beats get a lighter tap. Subdivisions could use a different vibration pattern.
- **Accelerometer gesture detection** — tap detection (start) and double-tap detection (stop). Must reject normal playing motion (bowing, guitar strumming, piano arm movement) while reliably detecting deliberate wrist taps.
- **LED control** — flash on beat for first N bars, then off.
- **BLE communication** — receive BPM, time signature, accent pattern, and presets from the app. Send playback state and battery level back.
- **Power management** — sleep when stopped, wake on tap gesture or BLE command.

### Companion app responsibilities (primary control interface)
- **All configuration** — BPM setting, time signature, accent patterns, subdivision modes. The bracelet has no physical controls for these.
- **Start/stop** — redundant to tap/double-tap; also controllable from the app.
- **Preset / setlist management** — songs with tempo and time-signature presets, pushed to device.
- **Visual beat display** — real-time beat indicator on screen, BPM readout, time signature display.
- **Practice session tracking** — log tempo, duration, patterns.
- **OTA firmware updates.**

### Cloud (minimal / optional)
- Firmware image hosting for OTA.
- Optional practice log backup.

## Relevant Skill Areas

| # | Skill Area | Relevance | Why |
|---|-----------|-----------|-----|
| 1 | Systems Architecture | **High** | The bracelet is a thin actuator; the app is the brain. Defining this split cleanly is key. |
| 5 | Embedded Software & Firmware | **High** | Timing precision, haptic waveform shaping, and accelerometer gesture detection are all firmware problems. |
| 10 | Sensors & Actuators | **High** | Haptic motor selection (LRA vs. ERM), accelerometer for tap detection — these ARE the product. |
| 9 | Power Management | **High** | Small battery in a wristband; haptic motor is the primary power consumer. Every milliamp matters. |
| 4 | Mechanical & Industrial Design | **High** | Wristband comfort, motor placement for skin contact, waterproofing for sweat, clasp design. This is now a wearable — mechanicals are harder than a box on a shelf. |
| 3 | Electrical & Electronic HW | **High** | MCU selection, haptic driver IC, accelerometer, tiny PCB in a wristband form factor. |
| 6 | Connectivity & Protocols | **Medium** | BLE for app pairing. The app is now the primary UI, so BLE reliability matters more than in the tabletop version. |
| 7 | Companion App Architecture | **High** | The app IS the control interface. It must be responsive, reliable, and handle the full configuration surface. Elevated from medium. |
| 13 | User Interaction (Physical + Digital) | **High** | Tap/double-tap gesture is the only physical interaction. Must be reliable. App UX for real-time tempo changes during performance matters. |
| 12 | Regulatory & Compliance | **Medium** | FCC/CE for BLE. Skin contact raises material safety questions (nickel, allergens). |
| 15 | Cost & BOM Awareness | **Medium** | Wearable BOM is tighter — small battery, flex PCB, band material all add cost. |
| 2 | Requirements Thinking | **High** | The wearable form factor introduces new constraints: comfort, sweat resistance, gesture reliability during playing. |
| 16 | Testing & Validation | **High** | Must validate that haptic pulses are perceptible at tempo across wrist sizes, playing styles, and motor types. |
| 8 | Cloud & Backend | **Low** | Same as before — OTA hosting only. |
| 11 | Security | **Low** | Same — signed OTA, BLE bonding. |
| 14 | Manufacturing & Provisioning | **Medium** | Wearable assembly is more complex than a box (band attachment, flex PCB, small enclosure). |

## Key Unknowns and Questions

1. **Haptic motor type** — LRA (Linear Resonant Actuator) gives crisper taps with faster rise time (~5 ms) but needs a tuned driver (DRV2605 or similar). ERM (Eccentric Rotating Mass) is cheaper but has slower rise/stop time (~20–50 ms), making beats feel mushy at high tempos. LRA is almost certainly the right choice, but needs validation at 200+ BPM.
2. **Haptic perceptibility during playing** — When a guitarist is strumming, a violinist is bowing, or a pianist is playing expressively, arm motion is significant. Can the wrist-worn haptic pulse still be felt? This is the fundamental product risk.
3. **Tap/double-tap reliability** — The accelerometer must distinguish a deliberate tap on the bracelet from playing motions. A strumming guitarist's wrist experiences repeated moderate-g transients. False starts and missed stops would be infuriating.
4. **Wristband design** — Rigid pod on a flexible band (like a fitness tracker)? Fully flexible (like a fabric strap with embedded electronics)? The motor needs firm skin contact, which argues for a rigid pod with a sprung or contoured contact surface.
5. **Downbeat differentiation via haptics** — Can musicians reliably distinguish beat 1 from other beats purely through vibration? Amplitude alone is hard to distinguish on a vibrating limb. Proposed approach: a **dual-pulse** pattern for beat 1 (two short taps ~40 ms apart — a "da-dum") vs. a single pulse for other beats. Pattern-based distinction is more perceptible than intensity-based. Needs user testing at tempo.
6. **Battery life in wristband form factor** — A wristband can fit ~100–200 mAh. An LRA draws ~50–100 mA per pulse. At 120 BPM (2 pulses/s, ~20 ms each), average current is ~2 mA from the motor alone. 200 mAh / ~5 mA total ≈ 40 hours. Likely fine, but needs validation.
7. **Sweat and water resistance** — Musicians sweat during performance. IP rating? At minimum, sweat-resistant (IPX4 splash-proof).

## Initial Risk Areas

| Risk | Severity | Notes |
|------|----------|-------|
| **Haptic perceptibility during active playing** | High | The product fails if the musician can't feel the beat while playing. Strumming guitarists and bowing string players have the most arm motion among target users. Must prototype and test with real musicians on real instruments. |
| **Tap gesture false triggers** | Medium | Accelerometer must reject playing motion. A strumming guitarist's wrist sees moderate repeated transients. The tap detection algorithm must use a distinctive gesture signature (sharp fingertip tap on the pod) that differs from playing motion patterns. |
| **Timing jitter** | High | Same as audible metronome — < 100 µs. The haptic driver adds its own latency (LRA rise time ~5 ms). Consistent latency is acceptable (musicians adapt); variable latency (jitter) is not. |
| **Comfort for long sessions** | Medium | Wristband must be comfortable for 2+ hour practice sessions. Weight, band material, pod size, and clasp type all matter. Must not interfere with playing technique. |
| **Downbeat distinction via haptics** | Medium | If musicians can't tell beat 1 from beats 2–3–4 by feel alone, the product is a simple click track with no musical utility beyond steady pulse. Dual-pulse pattern for beat 1 is the proposed mitigation — needs prototype validation. |
| **BLE reliability as primary control** | Medium | The app is now the only way to change BPM and meter. If BLE drops, the musician is stuck at the current setting until reconnection. The device should continue playing the last-set config independently. |

## Suggested Focus for High-Level Design

1. **Haptic motor selection and driving** — LRA vs. ERM, driver IC, pulse shaping for accent differentiation. This is the core product decision.
2. **Accelerometer gesture detection** — Tap/double-tap algorithm that works during active playing. May need instrument-specific profiles or a distinctive gesture.
3. **Wristband form factor** — Pod size, band attachment, motor skin contact, comfort.
4. **Power budget** — Small battery, haptic pulses as primary consumer. Target 8+ hours.
5. **BLE GATT profile** — Same characteristics as before, but now BLE is the primary control channel, not a convenience overlay.
