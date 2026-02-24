### AquaChill — High-Level System Design

**Date:** 2026-02-24 | **Author:** (example) | **Status:** Draft

#### What It Is

A countertop appliance that chills tap water from ~20°C to 4°C in under 90 seconds using a miniature vapor-compression loop, stores 1.5L in an insulated stainless-steel tank, and connects via BLE to a companion app for temperature presets, filter life tracking, and energy usage stats. Fills the gap between bulky water coolers and slow pitcher filters for apartment kitchens and small offices.

#### Block Diagram

```
  ┌────────────────────────────────────────────────────────────┐
  │                       AquaChill                            │
  │                                                            │
  │  ┌────────────┐  I2C   ┌──────────────────┐  BLE   ┌────────────┐
  │  │ Temp Sensor │──────→│  MCU + Firmware   │←──────→│ Companion  │
  │  │ (NTC×2)     │       │  nRF52832         │        │ App (BLE)  │
  │  └────────────┘       │                    │        └────────────┘
  │                        │  PID control,      │
  │  ┌────────────┐  GPIO  │  state machine,    │
  │  │ Flow Sensor │──────→│  BLE GATT server   │
  │  └────────────┘       └────────┬───────────┘
  │                                │ GPIO + PWM
  │  ┌────────────┐         ┌──────┴───────┐
  │  │ 24V PSU    │         │ Compressor   │
  │  │ (mains)    │────────→│ driver +     │
  │  └────────────┘         │ fan + LEDs   │
  │                         └──────────────┘
  │                                                            │
  │  ┌──────────────────────┐                                  │
  │  │ Insulated 1.5L tank  │                                  │
  │  │ + dispense valve     │                                  │
  │  └──────────────────────┘                                  │
  └────────────────────────────────────────────────────────────┘
```

#### Subsystems

| Subsystem | Purpose | Domain |
|-----------|---------|--------|
| Temperature sensing (2× NTC thermistors) | Measure tank water temp and condenser temp for PID loop and safety cutoff | HW |
| Flow sensor | Detect dispense events, track cumulative volume for filter life | HW |
| MCU + firmware (nRF52832) | Run PID compressor control, manage power states, serve BLE GATT for app communication, track filter usage | FW |
| Compressor + driver (miniature R134a vapor-compression) | Reject heat from tank water to ambient air via condenser + fan | HW |
| Companion app (iOS + Android) | Set target temperature, view filter life, see energy stats, receive filter replacement alerts | SW |
| Power supply (external 24V/3A brick) | Convert mains AC to 24V DC for compressor; 3.3V rail derived on-board for MCU and sensors | HW |
| Insulated tank + dispense valve | Store 1.5L chilled water, manual push-lever dispense | HW |

#### Key Interfaces

| From → To | What Crosses | Protocol / Medium |
|-----------|-------------|-------------------|
| NTC thermistors → MCU | Analog voltage proportional to temperature | ADC (2 channels, 10-bit, sampled at 1 Hz) |
| Flow sensor → MCU | Pulse train (pulses per mL) | GPIO interrupt, counted in firmware |
| MCU → Compressor driver | On/off + speed (variable-speed compressor) | GPIO enable + PWM (25 kHz) |
| MCU → Fan | Speed control | PWM (25 kHz) |
| MCU → Status LEDs | Cooling active, ready, error | 3× GPIO |
| MCU ↔ App | Temperature data, target setpoint, filter life, energy log | BLE 5.0 GATT (custom service, 4 characteristics) |

#### Constraints

| Constraint | Value | Why It Matters |
|-----------|-------|----------------|
| Chill time | 20°C → 4°C in <90 seconds (1.5L full tank) | Core promise — if it's slow, users keep a pitcher in the fridge instead |
| Footprint | ≤ 20 cm × 25 cm base, ≤ 35 cm tall | Must fit under upper kitchen cabinets, next to a kettle |
| Noise | < 45 dBA at 1m during active cooling | Kitchen/office use — compressor + fan noise is the primary complaint with existing chillers |
| BOM cost | < $65 at 5k units | Retail target $149–179; needs 55%+ gross margin |
| Safety | UL/CE approval for mains-powered appliance with refrigerant | Non-negotiable for retail — drives enclosure, wiring, and refrigerant choices |

#### Fundamental Hardware Problems

| Problem | Why It's Fundamental |
|---------|---------------------|
| Rejecting 20°C water down to 4°C in a countertop form factor in <90 seconds | Defines the thermal system — compressor capacity, condenser area, fan airflow, and tank insulation. Every mechanical dimension follows from this. |
| Keeping compressor + fan noise below 45 dBA | The vapor-compression loop and fan are the only significant noise sources. If the compressor is too loud for a kitchen counter, the product fails regardless of how well it chills. |
| Managing refrigerant safely in a consumer countertop device | R134a (or R600a) under pressure in a sealed loop inside a kitchen appliance. Leak detection, pressure relief, and UL/CE compliance set hard requirements on the mechanical design. |

#### Component Choice Architecture

| Component | Dominant Axis | Key Tension | Resolution Direction |
|-----------|--------------|-------------|---------------------|
| MCU (nRF52832) | Firmware complexity | ESP32 is cheaper but BLE stack is less mature; nRF52 has a proven BLE SoftDevice but costs ~$1.50 more | Pay the premium — BLE reliability matters for app experience, and nRF SDK reduces firmware effort. |
| Compressor | Performance vs. noise | Higher-capacity compressor chills faster but is louder. Variable-speed helps but adds driver cost (~$3). | Variable-speed — allows PID to throttle down as water approaches setpoint, reducing noise during the last 30% of the chill cycle. |
| Thermistor vs. digital temp sensor | Cost vs. firmware complexity | NTC thermistors are $0.10 each but need ADC + Steinhart-Hart conversion in firmware. Digital sensors (TMP117) are $1.50 but give calibrated I2C output. | NTC — save $2.80 on two sensors. The Steinhart-Hart math is trivial firmware work. |
| Tank insulation | Physical constraint | Thicker vacuum insulation keeps water cold longer but increases diameter by 15mm. Foam insulation is thinner but water warms faster. | Foam + active re-chill. The MCU monitors temp and kicks the compressor on when water warms past setpoint + 2°C. Avoids the size penalty of vacuum. |

#### Three Hardest Problems

1. **Thermal design — fitting a 90-second chill cycle into a countertop form factor:** The compressor, condenser, fan, and insulated tank must all fit within a 20×25×35 cm envelope while moving ~125 W of heat. Condenser surface area and airflow path are the binding constraints — too small and the refrigerant can't reject heat fast enough.

2. **Noise management at <45 dBA:** The compressor and condenser fan together typically produce 50–55 dBA in comparable systems. Getting below 45 dBA requires vibration isolation mounts, a slow-start ramp via variable-speed drive, optimized fan blade geometry, and possibly acoustic dampening foam — all within the size and cost envelope.

3. **BLE reliability for a mains-powered appliance near a metal tank and compressor:** The nRF52 antenna is inside a metal-and-plastic enclosure next to a steel water tank and a compressor motor. RF shielding and multipath will degrade BLE range. Antenna placement and ground plane design need careful attention to maintain a reliable 5m connection to the user's phone.

#### Open Calls

| Decision | Options | Deadline |
|----------|---------|----------|
| Refrigerant choice | R134a (proven, higher GWP) vs. R600a (lower GWP, flammable — tighter safety requirements) | Before mechanical design |
| Variable-speed vs. on/off compressor | Variable-speed (quieter, better PID, +$3 BOM) vs. on/off (simpler, cheaper, louder) | Before schematic |
| App framework | React Native (cross-platform, faster V1) vs. native Swift/Kotlin (better BLE handling) | Before app development |
