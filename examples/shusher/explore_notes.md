# Exploration Notes: Shusher

## Product Summary

A compact, personal device that detects obnoxiously loud talkers and speakerphone abusers in public spaces (cafés, coworking spaces, libraries, trains) and delivers a directed "shush" signal toward the offender. Part noise monitor, part social enforcer, part passive-aggressive ally. You set it on your table, it listens for sustained loud speech or speakerphone audio signatures, determines the direction, and fires a targeted audible "shush" — so you don't have to.

## HW/SW Boundary Analysis

### Must be physical hardware
- **Microphone array** — at least 2 MEMS mics, probably 3–4, for direction-of-arrival (DOA) estimation. The device needs to know *where* the noise is coming from, not just that it's loud. Spacing between mics determines angular resolution.
- **Directional speaker or speaker array** — the "shush" delivery mechanism. Options range from a standard small speaker (less directional, more social chaos) to a parametric/ultrasonic speaker array (highly directional, the offender hears it but neighbors don't). Parametric speakers are more expensive and larger but dramatically more fun.
- **DSP-capable processor** — beamforming, sound classification, and DOA all need real-time audio processing. An ESP32-S3 or STM32 with DSP extensions, or possibly a dedicated audio codec IC.
- **Battery** — portable, sits on a café table. Needs to last a workday session (4–6 hours of listening, intermittent shushing).
- **Enclosure** — small enough to be unobtrusive on a café table. Should not look threatening or weird. Ideally looks like a coaster, a small speaker, or a desk ornament.
- **LED ring or indicator** — subtle feedback showing listening state, detected noise direction, and shush activation. Also doubles as "don't mess with me" social signaling.

### Firmware responsibilities
- **Audio capture and beamforming** — continuous multi-channel audio capture from the mic array, real-time beamforming to estimate direction of arrival of dominant sound sources.
- **Sound classification** — distinguish loud speech and speakerphone audio from acceptable café noise (music, espresso machine, cutlery). This is the hard problem. A speakerphone call has a distinctive spectral signature (compressed voice audio from a phone speaker at high volume). Loud face-to-face conversation is sustained speech above a threshold, from a consistent direction.
- **Threshold and trigger logic** — not every loud moment deserves a shush. The firmware needs a sustained-loudness trigger: X dB above ambient baseline for Y seconds from direction Z. Adjustable sensitivity.
- **Shush generation and delivery** — synthesize or play back the "shush" sound, route it to the speaker (or parametric array driver) aimed at the detected direction. If using a parametric speaker, firmware drives the ultrasonic carrier modulation.
- **Ambient baseline tracking** — continuously adapts to the environment's baseline noise level. A noisy café has a higher threshold than a library.
- **LED control** — directional indication (which segment of the LED ring lights up), state feedback.
- **BLE communication** — settings sync with companion app.
- **Power management** — mic array and DSP are always on while active; speaker only fires on shush events.

### Companion app responsibilities
- **Sensitivity configuration** — how loud is too loud, how long before triggering, how aggressive the shush response is.
- **Shush style selection** — choose the shush sound: classic librarian "shhhh," passive-aggressive throat clear, gentle "ahem," or the nuclear option (a full "EXCUSE ME").
- **Shush log** — history of shush events with timestamp, direction, estimated dB level, and duration of the offense. Gamification potential: "You shushed 7 loud talkers this week."
- **Noise environment display** — real-time ambient noise level, directional noise map.
- **Custom sound upload** — let users upload their own shush sounds. Community shush library.
- **Mode presets** — "Café," "Library," "Train," "Coworking" with different thresholds and response styles.
- **OTA firmware updates.**

### Cloud (light)
- Firmware hosting for OTA.
- Optional: anonymous noise level crowdsourcing ("loudest cafés in your city"). Privacy-sensitive — no audio leaves the device, only dB levels and metadata.
- Community shush sound library.

## Relevant Skill Areas

| # | Skill Area | Relevance | Why |
|---|-----------|-----------|-----|
| 1 | Systems Architecture | **High** | The mic array → DSP → classification → directional speaker chain is the entire product. Getting the pipeline right determines whether it works or is just a random noise maker. |
| 5 | Embedded Software & Firmware | **High** | Real-time audio processing, beamforming, sound classification — this is a firmware-heavy product. The DSP pipeline runs continuously. |
| 10 | Sensors & Actuators | **High** | MEMS microphone array selection (sensitivity, SNR, matched response), speaker/parametric array selection — these components ARE the product. |
| 3 | Electrical & Electronic HW | **High** | Multi-channel audio capture, audio codec, DSP processor selection, speaker driver (especially if parametric — needs ultrasonic amplifier). Analog audio path quality matters. |
| 9 | Power Management | **High** | Continuous multi-mic audio capture and DSP is power-hungry. Battery life in a portable form factor is a real constraint. |
| 4 | Mechanical & Industrial Design | **High** | Mic placement geometry determines beamforming performance. Speaker direction matters. Enclosure must be small, unobtrusive, and café-table-friendly. Acoustic design (mic ports, speaker ports) is critical. |
| 13 | User Interaction | **High** | The LED feedback, the shush sound selection, the "personality" of the device — this product lives or dies on whether using it feels satisfying or embarrassing. |
| 7 | Companion App | **Medium** | Configuration, shush log, sound selection. Not the primary interface (the device acts autonomously) but important for personalization and entertainment value. |
| 6 | Connectivity | **Medium** | BLE for app pairing and settings. Not mission-critical — the device works standalone. |
| 2 | Requirements Thinking | **High** | "Detect loud talkers" sounds simple but the classification problem is subtle. What counts as "too loud"? How do you avoid shushing someone who just laughed once? |
| 16 | Testing & Validation | **High** | Testing audio classification in real café environments with real background noise. Beamforming accuracy. False positive rate is the key metric — shushing the wrong person is worse than not shushing at all. |
| 15 | Cost & BOM | **Medium** | Parametric speaker is expensive ($15–30 for the transducer array alone). Mic array adds cost. Target price point determines whether this is a $40 fun gadget or a $150 niche tool. |
| 12 | Regulatory | **Medium** | No RF certification issues beyond BLE. But: is it legal to direct sound at someone in a public space? Probably yes (it's just a speaker), but worth checking local noise/harassment ordinances. Also audio recording concerns — the device listens continuously but should NOT store or transmit audio. |
| 8 | Cloud & Backend | **Low** | Optional crowdsourcing and sound library. Not core. |
| 11 | Security | **Low** | BLE bonding. Signed OTA. No sensitive data beyond noise levels. |
| 14 | Manufacturing | **Low** | Standard PCB assembly. Mic array geometry needs fixture precision. |

## Key Unknowns and Questions

1. **Sound classification accuracy** — Can firmware reliably distinguish "obnoxiously loud talker" from "normal café conversation that happens to be nearby"? Speakerphone audio has a distinctive compressed quality, but loud face-to-face speech is just... speech, but louder. The classifier needs to combine dB level, sustained duration, and direction consistency. False positives (shushing innocent people) will kill the product. False negatives (missing actual offenders) make it useless.

2. **Directional speaker technology** — A standard speaker broadcasts in all directions, which means the whole café hears the shush, which is embarrassing for the *user*, not the offender. A parametric (ultrasonic) speaker can beam sound directionally — the offender hears "shhh" and nobody else does. But parametric speakers need a transducer array (40kHz+), an ultrasonic amplifier, and they don't work well for low frequencies. A "shush" is mostly sibilant high-frequency content, which is actually ideal for parametric delivery. Cost and size are the tradeoffs.

3. **Direction-of-arrival resolution** — With 3–4 MEMS mics spaced ~4cm apart on a small device, angular resolution at speech frequencies (300 Hz – 4 kHz) is limited. At 3 kHz with 4cm spacing, you get maybe ±15° resolution. Good enough to aim a parametric speaker? Probably, if the beam is wide enough. Needs simulation and real-world testing.

4. **Social dynamics** — Is this product funny-satisfying or cringe-embarrassing? If the shush is too obvious, the user becomes the antisocial one. If it's too subtle, it's ineffective. The "personality" of the shush — volume, tone, timing, repetition — is a design problem as much as an engineering one. A single well-timed "shhh" that seems to come from nowhere is comedy. A repeated robotic shush every 30 seconds is harassment.

5. **Form factor and social acceptability** — A device sitting on your café table that visibly reacts to nearby noise could make *you* look like the problem. Needs to be discreet. Could it look like a wireless charger? A coaster? A small bluetooth speaker?

6. **Legal/ethical gray area** — Directing sound at a stranger in a public space. Not illegal (you can play music from a speaker), but could escalate a situation. The product needs a de-escalation philosophy: one polite shush, then nothing. Not a weapon, a nudge.

7. **Battery life with continuous DSP** — Multi-channel audio capture + real-time beamforming + classification burns power. An ESP32-S3 running audio DSP at 240 MHz draws ~100–150mA. With a 2000mAh battery, that's 13–20 hours before speaker activation. Probably workable, but needs a smart duty cycle — full DSP only when ambient noise exceeds a baseline threshold.

## Initial Risk Areas

| Risk | Severity | Notes |
|------|----------|-------|
| **False positive shushing** | Critical | Shushing the wrong person — a normal-volume conversation, a brief loud laugh, the barista calling an order — makes the product annoying and socially dangerous. Classification accuracy and trigger thresholds must be very conservative. Better to miss an offender than to shush an innocent bystander. |
| **Sound classification in noisy environments** | High | Cafés have espresso machines, background music, dish clatter, door chimes. Separating "loud talker" from "generally noisy environment" requires robust classification. A simple dB threshold won't work — it needs directional sustained-speech detection. |
| **Directional delivery** | High | If the shush goes everywhere, the product embarrasses the user. Parametric speaker solves this but adds cost, size, and complexity. Standard speaker fallback works but changes the product from "stealth enforcer" to "public spectacle." |
| **Social backlash** | Medium | The offender may not appreciate being shushed by a gadget. Could escalate to confrontation. Product positioning and shush "personality" must be carefully designed — gentle, humorous, plausibly deniable. |
| **Form factor vs. acoustic performance** | Medium | Mic array beamforming needs physical separation between mics. Speaker directivity needs aperture size. Both push toward a larger device. But café-table discretion pushes toward smaller. Tension between acoustic physics and social usability. |
| **Market positioning** | Medium | Is this a serious product ($100+ noise management tool for remote workers in cafés) or a fun gadget ($40 gag gift that actually works)? The answer changes the BOM budget, the classification accuracy requirement, and the speaker technology. |

## Suggested Focus for High-Level Design

1. **Audio pipeline architecture** — Mic array → ADC → beamforming → classification → trigger decision → shush synthesis → directional speaker. This is the product's spine. Every other decision follows from how this pipeline is designed.

2. **Speaker technology decision** — Parametric (directional, expensive, larger) vs. standard (omnidirectional, cheap, smaller). This is the make-or-break product decision. It determines the form factor, the BOM cost, the social dynamics, and whether the product is magical or merely loud.

3. **Classification algorithm** — What features distinguish "shush-worthy" noise from acceptable café ambiance? Sustained speech above ambient + consistent DOA + duration threshold is the starting model. May need on-device ML inference (keyword-free voice activity detection + level analysis).

4. **Form factor and enclosure** — Drives mic placement geometry, speaker aperture, battery size, and social acceptability. All interlinked.

5. **Trigger behavior and personality** — The firmware state machine for when and how to shush. Single shush then cooldown? Escalating responses? Back-off if noise stops? This is where the product's character lives.
