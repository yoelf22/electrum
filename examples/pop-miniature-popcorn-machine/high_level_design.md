### Pop! — High-Level System Design

**Date:** 2026-02-24 | **Author:** | **Status:** Draft

#### What It Is

A desktop gadget that pops popcorn one kernel at a time using a gravity-fed chute and a slow double conveyor belt that moves kernels through a hot zone. If a kernel pops, it expands and escapes the belt into a "ready to eat" bowl. If it doesn't pop, the belt carries it to the end and dumps it into a dud bowl. No sensors needed for sorting — physics does it. USB-C PD powered. The whole mechanism is visible through a clear enclosure.

#### Block Diagram

```
  ┌──────────────────────────────────────────────────────────────┐
  │                          Pop!                                 │
  │                                                               │
  │  ┌───────────────┐                                            │
  │  │ Kernel Hopper │                                            │
  │  │ (~100 kernels)│                                            │
  │  └───────┬───────┘                                            │
  │          │ gravity chute (single-file slide)                  │
  │  ┌───────▼──────────────────────────────────┐                 │
  │  │ Double Conveyor Belt                      │                │
  │  │ (two belts grip kernel, move slowly       │                │
  │  │  through heated zone)                     │                │
  │  │                                           │                │
  │  │  ┌─────────┐                              │                │
  │  │  │ Hot Zone │  PTC heater under belt      │                │
  │  │  └─────────┘                              │                │
  │  │           │                               │                │
  │  │    kernel pops → escapes belt upward      ├──── dud exits  │
  │  └───────────┼───────────────────────────────┘     end of belt│
  │              │                                        │       │
  │     ┌────────▼────────┐                 ┌─────────────▼───┐   │
  │     │ Popcorn Bowl    │                 │ Dud Bowl        │   │
  │     │ (ready to eat)  │                 │ (unpopped)      │   │
  │     └─────────────────┘                 └─────────────────┘   │
  │                                                               │
  │  ┌─────────────────────┐         ┌─────────────────────┐     │
  │  │  MCU (ESP32-C3)     │         │ USB-C PD supply     │     │
  │  │  • Belt motor PWM   │         │ (20V, 1.5A = 30W)  │     │
  │  │  • Temp PID control │         └─────────────────────┘     │
  │  │  • LED effects      │                                      │
  │  │  • BLE (optional)   │                                      │
  │  └─────────────────────┘                                      │
  └───────────────────────────────────────────────────────────────┘
```

#### Subsystems

| Subsystem | Purpose | Domain |
|-----------|---------|--------|
| Kernel hopper + chute | Gravity-fed reservoir, angled chute narrows kernels into single-file and slides them onto the conveyor belt intake | HW |
| Double conveyor belt | Two parallel belts (silicone or PTFE) grip a kernel between them and move it slowly through the hot zone. Speed: ~5-10mm/s. Belt gap slightly less than kernel diameter for gentle grip. | HW |
| Hot zone (PTC heater) | Heats the belt path from below. Kernels passing through reach popping temperature. A popped kernel expands 10-15x, breaks free of the belt grip, and escapes upward/sideways into the popcorn bowl. | HW |
| Popcorn bowl | Catches popped kernels that escape the belt. Open top, positioned alongside the hot zone. Clear, removable. | HW |
| Dud bowl | Catches unpopped kernels that reach the end of the belt without popping. Small container at the belt exit. | HW |
| MCU + firmware (ESP32-C3) | Belt motor speed control, PID temperature control, LED effects, optional BLE | FW |
| LED ring | Visual effects — amber during preheat, animations during operation, idle glow | HW+FW |
| USB-C PD power supply | 20V @ 1.5A from USB-C PD for heater and motor | HW |
| Companion app (optional) | Stats, temperature/speed adjustment | SW |

#### Key Interfaces

| From → To | What Crosses | Protocol / Medium |
|-----------|-------------|-------------------|
| Hopper → Conveyor belt | Kernels under gravity via angled chute | Mechanical (chute angle and width sized for single-file kernel flow) |
| MCU → Belt motor | Speed control | PWM via motor driver IC |
| Thermistor → MCU | Hot zone temperature | ADC (12-bit, 10 Hz) |
| MCU → PTC heater | PWM power control | GPIO → MOSFET (20V rail) |
| MCU → LED ring | Color/brightness | SPI (WS2812B) |
| MCU ↔ App | Stats, config | BLE GATT (optional) |
| USB-C PD → Device | 20V @ 1.5A | USB-C PD negotiation |

#### Constraints

| Constraint | Value | Why It Matters |
|-----------|-------|----------------|
| Power input | USB-C PD, max 30W | No wall brick. Limits heater power — single-kernel heating makes this feasible. |
| Footprint | ~15 cm wide × 20 cm deep × 15 cm tall | Must fit on a desk. Wider than tall (belt runs horizontally). |
| Belt speed | ~5-10 mm/s | Kernel must spend 5-10 seconds in the hot zone to pop. Too fast = all duds. Too slow = boring. |
| Hot zone temp | ~200°C | Popping temperature. Belt material must tolerate continuous 200°C contact. |
| BOM cost | <$25 at 1k units | Desk toy / gift: retail $50-80. |
| Food safety | FDA 21 CFR / EU 1935/2004 | Belt, bowls, and any food-contact surface must be food-safe. |

#### Three Hardest Problems

1. **Belt material and grip at 200°C:** The conveyor belts must grip a kernel firmly enough to move it, yet release it when it pops and expands. The belt material must survive continuous 200°C in the hot zone without degrading, must be food-safe, and must not stick to kernels or popped corn. Silicone and PTFE are candidates — both heat-tolerant and food-safe, but grip characteristics differ.

2. **Gravity chute single-filing:** The chute must naturally organize bulk kernels into a single-file stream feeding the belt at a steady rate. Kernels are irregular and tend to bridge. The chute angle, width, and surface texture determine whether kernels flow smoothly or jam. No active mechanism — pure geometry and gravity.

3. **Pop escape geometry:** When a kernel pops between the belts, the expansion force must be enough to break free of the belt grip and escape into the popcorn bowl — not get crushed between the belts, not shoot backward into the hopper, and not fall into the dud bowl. The belt gap, grip force, and pop chamber geometry must be tuned so that popped kernels reliably exit sideways/upward.

#### Fundamental Hardware Problems

| Problem | Why It's Fundamental |
|---------|---------------------|
| Conveyor belt material surviving continuous 200°C while gripping food-safe | Defines the belt choice, which defines the mechanism. If no food-safe belt material works at 200°C with appropriate grip, the conveyor concept doesn't work. |
| Kernel flow through a passive gravity chute without jamming | If the chute jams, the machine stops. There's no active singulation — the geometry must work passively. If passive flow is unreliable, an active feed mechanism must be added, changing the design. |
| Popped kernel escaping the belt grip reliably | The core sorting mechanism: pop = escape, no pop = continue. If popped kernels get stuck between the belts, the product fails. Belt gap and compliance must be tuned. |

#### Component Choice Architecture

| Component | Dominant Axis | Key Tension | Resolution Direction |
|-----------|--------------|-------------|---------------------|
| MCU (ESP32-C3) | Cost | Cheapest ESP32 with ADC for thermistor + PWM for motor/heater. BLE if wanted. | ESP32-C3 — ~$1.50, sufficient for simple PID + motor PWM. |
| Belt material | Performance + food safety | Silicone: good grip, food-safe, but softens at 200°C. PTFE: heat-tolerant to 260°C, food-safe, but low friction (poor grip). Fiberglass-reinforced PTFE mesh: best of both. | Prototype with PTFE-coated fiberglass mesh. Grip comes from belt tension, not surface friction. |
| PTC heater | Performance + power | Must heat a narrow zone to 200°C at ≤25W. Element shape must match the belt path. | Standard flat PTC element (~20W), mounted under the belt path. Custom shape may be needed. |
| Motor | Cost + reliability | Small DC gearmotor is cheapest and simplest for constant belt speed. Stepper offers precision but costs more. | DC gearmotor with encoder feedback — ~$2, constant speed is sufficient. |
| Enclosure | Aesthetics + food safety | Must be transparent (desk-toy appeal) and food-safe near bowls. Clear PC or Tritan. | Tritan for food-contact areas, PC or ABS for structural frame. |

#### Open Calls

| Decision | Options | Deadline |
|----------|---------|----------|
| Belt material and construction | Silicone belt vs. PTFE-coated fiberglass mesh vs. stainless steel mesh | Before mechanism prototype — defines the entire conveyor design |
| Belt configuration | Horizontal belt with top/bottom grip vs. angled belt vs. belt + heated slide | Before mechanism prototype |
| Hot zone geometry | Heater under belt vs. heater on both sides vs. radiant heater above | Before thermal prototype |
| Chute design | Straight slide vs. spiral/helical chute vs. stepped chute | Before mechanism prototype — determines feed rate and jam behavior |
