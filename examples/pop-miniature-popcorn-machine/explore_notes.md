# Exploration Notes: Pop!

## Product Summary

A desktop gadget that pops popcorn one kernel at a time. A hopper holds unpopped kernels. A feeding mechanism drops a single kernel onto a hot spot. The kernel pops. It falls (or launches) into a collection bowl below. The next kernel feeds in. Repeat. The result is a mesmerizing, one-at-a-time popcorn machine — part desk toy, part snack maker, part conversation piece. The fun is watching it work.

## HW/SW Boundary Analysis

### Must be physical hardware
- **Kernel hopper** — a gravity-fed reservoir holding ~50-100 kernels. Funnel-shaped, tapering to a single-kernel outlet. Like a gumball machine throat.
- **Singulation mechanism** — the hardest mechanical problem. Must reliably isolate and release exactly one kernel at a time. Kernels are irregular in size and shape. Options: rotating disc with a pocket (like a pill dispenser), a gate/slider, or a vibrating channel. Must not jam.
- **Hot spot / popping chamber** — a small heated surface or cavity where the single kernel sits and receives enough heat to pop. Could be a heated cup, a focused hot-air jet, or a contact surface at ~200°C. Must be small enough to heat one kernel efficiently, not waste energy heating a large volume.
- **Popped kernel ejection** — when the kernel pops, it expands ~10-15x and needs to go somewhere. The pop itself provides kinetic energy (kernels jump when they pop). The geometry should channel the popped kernel into the collection bowl and clear the hot spot for the next one.
- **Collection bowl** — where finished popcorn accumulates. Could be a clear container so you can watch it fill up.
- **Temperature sensor** — thermistor at the hot spot for closed-loop temperature control.
- **Pop detection** — MEMS mic or mechanical switch/vibration sensor to detect when the kernel has popped (the pop is a sharp impulse). This triggers the feed-next-kernel cycle.
- **Motor(s)** — for the singulation mechanism (stepper or small DC motor with encoder).
- **Enclosure** — the whole thing should be visually delightful. Clear sections so you can see the kernel travel from hopper → hot spot → bowl. Think desk toy aesthetics, not kitchen appliance.

### Firmware responsibilities
- **Feed cycle state machine** — idle → feed kernel → heat → detect pop → eject → cooldown → feed next. Each step has specific timing and sensor-driven transitions.
- **Singulation control** — drive the feeding mechanism to release exactly one kernel. Detect jams (kernel didn't drop within expected time). Retry or alert.
- **Temperature control** — PID loop on the hot spot. Must reach popping temp (~180-200°C) quickly and hold it. Between kernels, maintain temp to minimize wait time.
- **Pop detection** — acoustic (MEMS mic) or vibration-based. Detect the pop event to trigger the next cycle step. Also detect "dud" kernels that don't pop within a timeout — eject or skip.
- **Dud handling** — if a kernel doesn't pop within N seconds at temperature, it's a dud. The system must clear it somehow and move on. Can't let a dud block the pipeline.
- **Cycle speed optimization** — minimize the time between pops for satisfying cadence. Target: one pop every 3-8 seconds (depending on preheat state).
- **Safety** — thermal cutoff, max-on timer, stall detection on the feed motor.
- **LED/sound feedback** — optional LED strip or underglow that pulses with each pop. Satisfying audible "pop" is natural (it's popcorn).
- **BLE** — optional companion app for cycle stats, speed adjustment, kernel count.

### Companion app (low priority)
- Kernel counter ("you've popped 847 kernels")
- Speed/temperature adjustment
- Pop efficiency stats (% duds)
- Fun — totally optional, the device is self-contained entertainment

### Cloud
- None needed. This is a standalone desk gadget.

## Relevant Skill Areas

| # | Skill Area | Relevance | Why |
|---|-----------|-----------|-----|
| 4 | Mechanical & Industrial Design | **Critical** | The singulation mechanism is the product. Reliably feeding irregular-shaped kernels one at a time without jamming is the dominant engineering challenge. Everything else is secondary. |
| 1 | Systems Architecture | **High** | Feed → heat → pop → eject → repeat cycle. Tight integration between mechanical feeding, thermal control, and pop detection. Timing between subsystems matters. |
| 10 | Sensors & Actuators | **High** | Hot spot (heating element), feed motor, pop detection sensor, temperature sensor. Small, precise actuators for single-kernel handling. |
| 3 | Electrical & Electronic HW | **High** | Heating element drive (lower power than a batch popper — heating one kernel vs. a chamber full), motor drive, thermal management in a compact form. |
| 5 | Embedded Software & Firmware | **High** | The cycle state machine with pop detection, jam detection, dud handling, and temperature control. Real-time coordination between mechanical and thermal subsystems. |
| 13 | User Interaction | **High** | This is a desk toy. The visual and auditory experience of watching kernels pop one by one IS the product. Clear enclosure, satisfying rhythm, maybe LED effects. |
| 9 | Power Management | **Medium** | Mains-powered (USB-C PD or wall adapter) or possibly battery with a small heater? Power for a single-kernel heater is much less than a batch popper — maybe 20-50W. Could work from USB-C PD (up to 100W). |
| 15 | Cost & BOM | **Medium** | Desk toy / gift price point: $30-60. The singulation mechanism and clear enclosure are the cost drivers. |
| 12 | Regulatory | **Medium** | Heating element means safety certification, but much lower power than a full kitchen appliance. If <60W, regulatory path is simpler. |
| 2 | Requirements Thinking | **Medium** | Define "miniature": desk-sized. Define throughput: one kernel every 5-8 seconds = ~8-12 kernels/minute = a bowl in ~10 minutes. Acceptable for a desk toy. |
| 16 | Testing & Validation | **Medium** | Singulation reliability across kernel sizes/brands. Jam rate. Dud rate. Pop consistency. |
| 7 | Companion App | **Low** | Nice-to-have, not core. |
| 6 | Connectivity | **Low** | BLE optional. |
| 8 | Cloud & Backend | **Low** | None. |
| 11 | Security | **Low** | None. |
| 14 | Manufacturing | **Low** | Custom singulation mechanism needs tooling, but otherwise standard. |

## Key Unknowns and Questions

1. **Single-kernel singulation reliability** — Popcorn kernels vary in size (4-8mm), shape (round to pointed), and moisture content. A mechanism must reliably pick/release exactly one at a time from a hopper of hundreds. Pill dispensers solve this for uniform pills; kernels are irregular. Rotating disc with a sized pocket? Vibrating track with a gate? Auger? This is the make-or-break mechanism. Jam rate must be <1% for the experience to feel smooth.

2. **Heating a single kernel efficiently** — A full popper heats a large air volume. Here we heat one kernel. Options: (A) Contact heating — kernel sits on a hot surface (~200°C). Simple, but the kernel must make good thermal contact despite its irregular shape. (B) Focused hot air — a small nozzle blows hot air onto the kernel in a tiny cup. Better heat transfer but needs a micro-blower. (C) Radiant/IR — a focused IR source heats the kernel. Even heating but slower. The question: how fast can a single kernel go from room temp to popping temp? Kernels pop when internal moisture reaches ~180°C and builds ~135 PSI pressure. Time to pop depends on heat transfer rate.

3. **What happens at the moment of pop?** — A kernel expands violently when it pops, jumping up to 30cm. The device geometry must contain and direct this. If the kernel is in a small cup, the pop launches it upward or outward — this needs to be channeled into the collection bowl, not across the desk. The pop event also clears the hot spot for the next kernel, which is good. But if the popped kernel gets stuck, it blocks the next cycle.

4. **Dud handling** — 5-10% of kernels don't pop (low moisture, cracked hull). If a dud sits on the hot spot and doesn't pop, the system must detect the timeout and either: (A) mechanically sweep/dump the dud, or (B) overheat it until it eventually pops or chars (bad — smell, smoke), or (C) accept the dud and feed the next kernel on top (messy). A mechanical clearing mechanism adds complexity but is probably necessary.

5. **Power source** — Heating one kernel to 200°C requires much less energy than a batch. A single kernel weighs ~0.15g. Heating it from 25°C to 180°C requires ~0.1J (specific heat) but the moisture conversion (steam pressure) requires ~0.3-0.5J total. The heater must deliver this energy in a reasonable time (3-8 seconds), so power = 0.5J / 5s = ~0.1W for the kernel itself. But the heater, cup, and air losses make the actual draw much higher — estimate 10-30W. This might work from USB-C PD (20V × 1.5A = 30W) which would be amazing — no wall brick, just a USB-C cable.

6. **Cycle cadence** — How fast is satisfying? One pop per second is frenetic. One pop per 15 seconds is boring. Target sweet spot: one pop every 4-8 seconds. That means the hot spot must recover temperature and the next kernel must be in position within a few seconds of the previous pop. Thermal mass of the hot spot matters — if it cools too much per cycle, reheat time dominates.

7. **Aesthetic and desk-toy quality** — This product's appeal is watching it work. Clear/transparent sections, visible kernel path, satisfying mechanical motion, the anticipation of each pop. Think marble run or Newton's cradle energy. The engineering must serve the visual/auditory experience, not the other way around.

## Initial Risk Areas

| Risk | Severity | Notes |
|------|----------|-------|
| **Kernel jamming** | Critical | If the singulation mechanism jams every 20 kernels, the product is broken. Irregular kernel geometry makes reliable feeding hard. Must prototype extensively with multiple kernel brands/sizes. |
| **Thermal safety in a desk form factor** | High | A 200°C hot spot on a desk next to a laptop. Must be enclosed, insulated, and fail-safe. Lower power than a kitchen appliance, but still a burn hazard if the user reaches in. |
| **Dud kernels blocking the cycle** | High | Duds must be detected (timeout) and cleared without manual intervention. Mechanical complexity vs. reliability tradeoff. |
| **Pop containment** | Medium | Popcorn kernels jump violently when they pop. The device must catch the popped kernel reliably, not launch it across the desk. Geometry and containment design. |
| **Cycle speed** | Medium | If the feed-heat-pop cycle takes >10 seconds, the cadence is boring. If the hot spot takes too long to recover between pops, throughput drops. Thermal design drives entertainment value. |
| **Market positioning** | Medium | This is a desk toy that makes snacks, not a serious kitchen appliance. Price sensitivity: $30-60. Must feel premium and delightful, not cheap and gimmicky. |

## Suggested Focus for High-Level Design

1. **Singulation mechanism** — The entire product depends on reliably feeding one kernel at a time. This deserves the most design attention. Research existing single-object dispensing mechanisms (pill dispensers, seed planters, coin sorters).

2. **Hot spot design** — Contact vs. hot-air vs. radiant heating for a single kernel. Optimize for speed (fast pop cycle) and containment (kernel pops in a controlled direction).

3. **Pop-and-eject geometry** — What happens in the 50ms when the kernel pops? Where does it go? How is the hot spot cleared? The physical geometry of the popping zone determines whether this works smoothly or creates a mess.

4. **Power strategy** — Can the whole thing run from USB-C PD? If yes, the form factor and desk-friendliness improve dramatically. If not, what's the minimum wall adapter wattage?

5. **Visual design language** — Clear enclosure, visible mechanism, desk-toy aesthetics. The engineering must be visible and beautiful, not hidden inside a plastic box.
