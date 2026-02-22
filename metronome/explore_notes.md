# Exploration Notes: Minimal Metronome

## Product Summary

A stripped-down, physical metronome device that produces an audible (and optionally haptic) beat at a user-set tempo. The device pairs with a companion app for advanced configuration — time signatures, accent patterns, tempo presets, and practice session tracking — while the hardware itself stays deliberately simple: a knob or buttons, a speaker/buzzer, and a visual beat indicator.

## HW/SW Boundary Analysis

### Must be physical hardware
- **Audio output** — a speaker, piezo buzzer, or similar transducer to produce the click/beat. Audio latency and jitter must be sub-millisecond; this is the core product promise.
- **Tempo control** — a rotary encoder or physical buttons for hands-free BPM adjustment during practice.
- **Visual beat indicator** — one or more LEDs (or a small display) showing the current beat position within the measure.
- **Power supply** — rechargeable LiPo or USB-C powered, depending on portability goals.
- **Enclosure** — compact, stable on a music stand or tabletop.

### Firmware responsibilities
- **Precision timing engine** — hardware timer–driven beat generation. This is the single most important firmware function. Jitter must stay under ~100 µs to be imperceptible to trained musicians.
- **Audio synthesis / playback** — driving a DAC or PWM output to produce click sounds with accent differentiation.
- **Input handling** — debouncing rotary encoder or buttons, mapping to BPM changes.
- **LED/display driver** — beat position visualization.
- **BLE communication** — exposing tempo, time signature, accent pattern, and playback state to the companion app.
- **Power management** — sleep on inactivity, wake on input.

### Companion app responsibilities
- **Advanced configuration** — time signatures (3/4, 5/8, 7/8…), accent patterns, subdivision modes, tempo presets per song.
- **Practice session tracking** — log tempo, duration, and patterns over time.
- **Setlist / preset management** — ordered list of songs with tempo and time-signature presets that can be pushed to the device.
- **Visual display** — large BPM readout, beat visualization, optional notation-style display.
- **OTA firmware updates** — delivering new features (new click sounds, expanded time signatures).

### Cloud (minimal / optional)
- Firmware image hosting for OTA.
- Optional cloud backup of practice logs and presets (could also be app-local only for V1).

## Relevant Skill Areas

| # | Skill Area | Relevance | Why |
|---|-----------|-----------|-----|
| 1 | Systems Architecture | **High** | Defining the split between on-device timing engine and app-side configuration is the core architectural decision. |
| 5 | Embedded Software & Firmware | **High** | Sub-millisecond timing precision is the hardest firmware problem. RTOS or bare-metal timer ISR design is key. |
| 9 | Power Management | **High** | Battery-powered portable device; audio output and BLE are the main power consumers. |
| 10 | Sensors & Actuators | **High** | Speaker/buzzer selection, optional haptic motor — these define the product's primary output. |
| 3 | Electrical & Electronic HW | **High** | MCU selection (timer resolution, DAC/PWM quality), audio amplifier, power supply. |
| 6 | Connectivity & Protocols | **Medium** | BLE for app pairing. Simple GATT profile — not a complex networking problem. |
| 7 | Companion App Architecture | **Medium** | Straightforward app: BLE connection, config UI, practice logs. No real-time streaming. |
| 13 | User Interaction (Physical + Digital) | **Medium** | Physical controls must be intuitive for musicians mid-practice. LED beat pattern must be instantly readable. |
| 4 | Mechanical & Industrial Design | **Medium** | Small enclosure, stable base, speaker port acoustics, button/knob ergonomics. |
| 12 | Regulatory & Compliance | **Low-Med** | FCC/CE for BLE radio. No special safety concerns. |
| 15 | Cost & BOM Awareness | **Low-Med** | Simple BOM — MCU, speaker, LEDs, battery, encoder, BLE. Target < $15 BOM at volume. |
| 8 | Cloud & Backend | **Low** | Minimal cloud needs. OTA hosting and optional practice-log backup. |
| 11 | Security | **Low** | Low-value target. Signed OTA is the main security need. |
| 14 | Manufacturing & Provisioning | **Low** | Simple assembly. Flash firmware + basic HW test at factory. |
| 16 | Testing & Validation | **Medium** | Timing accuracy validation is critical. Need to measure actual jitter with an oscilloscope or audio capture. |
| 2 | Requirements Thinking | **High** | "Minimal" is itself a design constraint — every feature must justify its inclusion. |

## Key Unknowns and Questions

1. **Audio output type** — Piezo buzzer (cheap, loud, harsh) vs. small speaker with DAC (richer tone, higher power, more complex)? This drives MCU selection (DAC needed?), amplifier circuit, and power budget.
2. **Haptic feedback** — Is a vibration motor included for silent practice? Adds BOM cost (~$0.50–1.00) and power draw but enables a major use case (practicing without disturbing others).
3. **Display** — LEDs only, or a small OLED/segment display showing BPM? A display adds cost and power but reduces app dependency.
4. **Portability requirements** — Must it run on battery, or is USB-C–powered acceptable? Battery adds charging circuit, enclosure volume, and weight.
5. **Tempo range** — Standard 20–300 BPM, or wider for niche use cases?
6. **Target price point** — Under $30 retail suggests < $10 BOM. Under $50 retail opens up better audio and display options.
7. **"Minimal" scope** — Does minimal mean minimal features (just a click) or minimal physical size (pocket-sized)?

## Initial Risk Areas

| Risk | Severity | Notes |
|------|----------|-------|
| **Timing jitter** | High | The fundamental hardware problem. If beats drift or jitter by >0.5 ms, trained musicians will notice. MCU timer resolution, ISR latency, and audio output path all contribute. Must be validated early with a prototype. |
| **Audio quality** | Medium | Cheap piezo buzzers sound bad. Musicians are discerning listeners. The click tone must be clean, sharp, and non-fatiguing over long practice sessions. |
| **BLE latency for tempo changes** | Low | App-initiated tempo changes will have ~20–50 ms BLE latency. This is fine for configuration but means the app cannot be in the timing-critical path. All beat generation must be on-device. |
| **Market differentiation** | Medium | Phone metronome apps are free. The hardware must offer something apps cannot: physical controls during practice, superior timing (phones have audio latency issues), haptic feedback, and no screen distraction. |
| **Power budget for audio** | Medium | Driving a speaker at usable volume consumes 50–200 mW. Battery life target of 8+ hours of continuous use at moderate volume needs ~1500 mAh minimum with a speaker, or much less with a piezo. |

## Suggested Focus for High-Level Design

1. **Timing architecture** — Detail the firmware timing engine. This is the product's core value proposition and the hardest technical problem. Specify timer source, ISR structure, and measured jitter target.
2. **Audio output chain** — Select between piezo and speaker+amplifier. This cascades into MCU selection, power budget, and enclosure acoustics.
3. **Input/output hardware** — Nail down the physical interface: rotary encoder vs. buttons, LED count/arrangement, optional display.
4. **BLE GATT profile** — Define the characteristics: tempo, time signature, accent pattern, playback state, preset list.
5. **Power architecture** — Battery vs. USB-powered, and the resulting power budget.
