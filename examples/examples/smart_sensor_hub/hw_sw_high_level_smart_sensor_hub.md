### AirSense Indoor Environment Monitor — High-Level System Design

**Date:** 2026-02-20 | **Author:** [Example] | **Status:** Draft

#### What It Is

A wireless indoor environment monitor that tracks CO2, temperature, humidity, and particulate matter per room in commercial offices. Battery-powered sensor nodes communicate over BLE to per-floor Ethernet gateways, which forward data to a cloud backend serving a web dashboard for facility managers. The system replaces complaint-driven HVAC management with room-level data and historical trends.

#### Block Diagram

```
  ┌──────────────────────────────────────────────────┐
  │           AirSense Sensor Node (per room)        │
  │                                                  │
  │  ┌──────────────┐      ┌───────────────┐         │
  │  │ CO2 (SCD41)  │─I2C─→│  nRF52840     │         │
  │  │ T/H (SHT40)  │─I2C─→│  Firmware:    │         │
  │  │ PM (PMSA003I)│─I2C─→│  sensor mgr,  │         │
  │  └──────────────┘      │  BLE adv,     │         │
  │                        │  power mgr    │         │
  │  ┌──────────┐          └───────┬───────┘         │
  │  │ 2x AA    │─→ TPS62740      │ BLE 5.3         │
  │  └──────────┘                  │ advertising     │
  │                                │                 │
  │  ┌──────────┐    ┌────────┐   │                 │
  │  │ Button   │────│RGB LED │   │                 │
  │  └──────────┘    └────────┘   │                 │
  └────────────────────────────────┼─────────────────┘
                                   │ BLE
                                   ▼
  ┌──────────────────────────────────────────────────┐
  │       AirSense Gateway (per floor)               │
  │  ESP32-S3  ←─ BLE scan ─→  Ethernet             │
  │                    MQTT over TLS ────────────→   │
  └──────────────────────────────────────────────────┘
                                   │
                                   ▼
  ┌──────────────────────────────────────────────────┐
  │             Cloud Backend                        │
  │  MQTT Broker → TimescaleDB → REST API            │
  │  Alert Engine → Email/Webhook                    │
  │  Web Dashboard (facility manager)                │
  │  Mobile QR Page (occupant read-only)             │
  └──────────────────────────────────────────────────┘
```

#### Subsystems

| Subsystem | Purpose | Domain |
|-----------|---------|--------|
| Sensor array (SCD41, SHT40, PMSA003I) | Measure CO2, temperature, humidity, and particulate matter per room | HW |
| nRF52840 + firmware | Read sensors on schedule, format BLE advertisement payload, manage power states, handle OTA via gateway | FW |
| Power management (TPS62740 + 2x AA) | Regulate 6V input to 3.3V rail, enable >12 month battery life with deep sleep | HW |
| BLE gateway (ESP32-S3 + Ethernet) | Scan BLE advertisements, aggregate sensor data from all nodes on one floor, forward to cloud via MQTT | HW+FW |
| Cloud backend | Ingest MQTT telemetry, store time-series data, serve REST API, run alert engine, host dashboard | Cloud |
| Web dashboard + mobile QR page | Facility manager floor map with color-coded rooms; occupant-facing single-room view via QR scan | SW |

#### Key Interfaces

| From → To | What Crosses | Protocol / Medium |
|-----------|-------------|-------------------|
| Sensors → nRF52840 | Raw CO2 ppm, temperature, humidity, PM counts | I2C (100-400 kHz) |
| nRF52840 → Gateway | Sensor payload in BLE advertisement (encoded, ~20 bytes) | BLE 5.3 extended advertising, one-way |
| Gateway → Cloud | Aggregated sensor readings with device IDs and timestamps | MQTT over TLS 1.2, Ethernet |
| Cloud → Dashboard | Room-level current + historical data, alerts, device health | HTTPS REST API |
| Cloud → Gateway → Device | OTA firmware images, config updates | MQTT download → BLE DFU |

#### Constraints

| Constraint | Value | Why It Matters |
|-----------|-------|----------------|
| Battery life | >12 months on 2x AA | Self-install by facility staff, no wiring, no charging. Drives the BLE-not-WiFi architecture decision. |
| BOM cost (sensor node) | <$35 at 1k units | 50-200 nodes per building. Cost per node must stay under building-automation alternatives. |
| BOM cost (gateway) | <$40 at 1k units | 1 per floor. Must justify itself vs. direct WiFi (which it replaces for power reasons). |
| CO2 accuracy | ±50 ppm + 5% | Facility managers make HVAC decisions from this data. Inaccurate readings = wasted energy or complaints. |
| Certification | FCC, CE, IC (BLE radio) | BLE transmission requires intentional radiator certification in all target markets. |
| Deployment density | Up to 50 nodes per gateway | Gateway BLE scanning must handle 50 devices advertising every 5 minutes without packet loss. |

#### Three Hardest Problems

1. **12-month battery life with a PM sensor on board:** The PMSA003I particulate matter sensor draws 25 mA during sampling — 50x more than all other components combined. At a 5-minute sample rate, it alone consumes ~417 µA average, exceeding the entire power budget. Either reduce PM sample rate dramatically (30-60 min), make the PM sensor a removable module, or accept shorter battery life for PM-equipped units.

2. **BLE range in concrete office buildings:** BLE advertising reach drops to 5-10m through concrete walls and metal partitions. A single gateway per floor assumes ~15m line-of-sight range. Dense offices with many walls may need 2-3 gateways per floor, increasing deployment cost and complexity.

3. **OTA firmware updates over BLE via gateway:** Updating sensor node firmware requires a reliable multi-hop path: cloud → gateway (MQTT) → sensor node (BLE DFU). BLE DFU to a battery-powered node that's asleep 99% of the time means coordinating wake windows, handling interrupted transfers, and validating images before committing — all without bricking deployed devices.

#### Fundamental Hardware Problems

| Problem | Why It's Fundamental |
|---------|---------------------|
| Powering a PM sensor from AA batteries for 12 months | The PM sensor's 25 mA draw during sampling defines the entire power architecture. If this can't be solved (by reduced sampling, modular PM, or larger batteries), the product either drops PM sensing or drops the 12-month battery target — both change what the product is. |
| Getting accurate CO2 readings with a 5-second sensing window | The SCD41 has a 15-second recommended warm-up for full accuracy. A 5-second window (to save power) may degrade accuracy below the ±50 ppm spec. If the sensor needs 15+ seconds per sample, the power budget roughly triples for the CO2 path. |
| BLE advertisement reliability at 50 nodes per gateway | 50 nodes advertising simultaneously on 3 BLE channels creates collision probability. Missed advertisements mean missed data points. If reliability drops below ~99%, the dashboard shows gaps that undermine facility manager trust. |

#### Component Choice Architecture

| Component | Dominant Axis | Key Tension | Resolution Direction |
|-----------|--------------|-------------|---------------------|
| MCU (nRF52840) | Performance | Best BLE power efficiency and mature SDK, but $4-5 at volume — more expensive than ESP32-C3 ($1-2) which has WiFi+BLE but worse sleep current | nRF52840 — the 12-month battery target is non-negotiable, and Nordic's BLE stack is proven for beacon-style advertising |
| CO2 sensor (SCD41) | Performance | Only photoacoustic CO2 sensor small enough for the enclosure with ±40 ppm accuracy. $8-12 at volume — dominates the BOM. No cheaper alternative meets the accuracy spec. | Accept the cost — CO2 is the core measurement. Accuracy is the product's credibility. |
| PM sensor (PMSA003I) | Cost vs. power | Adds ~$8 and dominates the power budget. Dropping it saves cost and battery but removes a differentiating measurement. | Make PM a removable module — offer two SKUs (with/without PM). Let the customer decide. |
| Power regulator (TPS62740) | Power efficiency | Ultra-low quiescent current (360 nA) justifies the $1.50 cost vs. a $0.30 LDO that wastes 10-50 µA quiescent — which would cut battery life by months | TPS62740 — quiescent current directly maps to battery life in a device that sleeps 99% of the time |
| Gateway MCU (ESP32-S3) | Cost + availability | ESP32-S3 ($3-4) with built-in BLE+WiFi+Ethernet MAC is the cheapest path to a mains-powered BLE scanner with Ethernet uplink. No real tension here — gateways are mains-powered, so power efficiency doesn't matter. | ESP32-S3 — clear winner on cost and integration |

#### Open Calls

| Decision | Options | Deadline |
|----------|---------|----------|
| PM sensor sampling strategy | Every 5 min (kills battery) vs. every 30-60 min (reduced resolution) vs. removable module (two SKUs) | Before power architecture finalized |
| SCD41 sensing window | 5s (power-optimized, accuracy risk) vs. 15s (spec-compliant, 3x power) vs. duty-cycled (10s on, accuracy TBD) | Before firmware sensor manager design |
| OTA update mechanism | BLE DFU via gateway (complex, reliable) vs. USB-C port on device (simple, requires physical access) | Before firmware partition layout |
| Gateway density model | 1 per floor (cheaper, range risk) vs. 1 per zone/wing (reliable, more hardware) | Before deployment guide |
