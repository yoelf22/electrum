# AirSense — Image Generation Prompts

Use these with ChatGPT (DALL-E) or similar image generators.

---

## Prompt 1: Cross-Section / Exploded View — Sensor Node

```
Technical cross-section illustration of a small wireless indoor air quality sensor device, cutaway view showing internal components.

The device is a compact white rounded-rectangle enclosure, roughly the size of a deck of cards (65mm × 65mm × 25mm), wall-mounted with a magnetic plate.

Cross-section reveals these layers from top to bottom:
- Ventilation slots along the top edge where air enters the sensing chamber
- A small green PCB with clearly labeled components:
  - CO2 sensor module (SCD41) — a small square photoacoustic sensor, the largest component on the board
  - A tiny temperature/humidity sensor (SHT40) near the air inlet
  - A particulate matter sensor module (PMSA003I) — a rectangular metal-shielded box with a small fan and air inlet/outlet
  - A Bluetooth radio chip (nRF52840) — a QFN IC in the center of the board
  - A small RGB LED visible through a light pipe in the front face
  - A tiny push button recessed on the side
- Below the PCB, a battery compartment holding two AA lithium batteries side by side
- A snap-fit battery door on the bottom

The enclosure wall is thin white plastic (ABS). A small QR code sticker is visible on the front face. The magnetic mounting plate is shown separated slightly behind the device.

Style: Clean technical product illustration on a white background. Isometric cutaway with precise labeling lines pointing to each component. Muted colors — white enclosure, green PCB, silver battery casings, subtle blue accent for the Bluetooth antenna trace. Professional product engineering aesthetic, similar to iFixit teardown illustrations.
```

---

## Prompt 2: Artist Concept — Full System in Context

```
Photorealistic product concept rendering of a commercial office indoor air quality monitoring system called "AirSense."

The scene shows a modern open-plan office during daytime with natural light:

- In the foreground, mounted on a white wall near the ceiling of a glass-walled meeting room, a small white rounded-rectangle device (the AirSense sensor node, about the size of a deck of cards). A tiny RGB LED glows soft green on its front face. A small QR code is visible on the device.

- On the far wall of the same room, a second identical device is partially visible, confirming room-level coverage.

- In the hallway outside the meeting room, a slightly larger white device (the AirSense gateway) sits on a shelf near an Ethernet wall jack, with a single thin Ethernet cable plugged in. A subtle blue LED strip indicates it's active.

- In the background, a facility manager at a standing desk looks at a laptop screen showing a floor-plan dashboard with rooms color-coded green, yellow, and amber. The dashboard has a dark UI theme with teal and blue accents.

- An employee in the meeting room holds up a phone, scanning the QR code on the wall device. The phone screen shows a simple readout: "23.1°C · 48% RH · 620 ppm CO2" in clean sans-serif type.

Style: Photorealistic product concept visualization. Clean, bright office environment. The devices are subtle and blend into the architecture — not attention-grabbing, but clearly identifiable. Warm natural lighting. Shot composition emphasizes the system working together across the three tiers (sensor → gateway → dashboard). No visible branding except a small "AirSense" wordmark on each device.
```

---

## Prompt 3: Cross-Section — Gateway

```
Technical cross-section illustration of a small wireless gateway device for an indoor air quality system.

The device is a slim white rectangular enclosure, approximately 120mm × 80mm × 30mm, designed to sit on a desk or shelf.

Cross-section reveals:
- A green PCB with:
  - ESP32-S3 module — a metal-shielded rectangular module with an integrated PCB antenna
  - Ethernet PHY IC and RJ45 jack with integrated magnetics on one end
  - A status LED strip (3 small LEDs: power, BLE activity, cloud connection) behind a translucent diffuser strip on the front edge
  - A USB-C power input jack on one end
  - A small ceramic BLE antenna or the module's PCB antenna trace highlighted
- Below the PCB, a flat area — no battery (this device is mains-powered via USB-C adapter)
- A wall-mount keyhole slot on the bottom surface
- The Ethernet cable exits one side, the USB-C power cable exits the other

The enclosure is white plastic with subtle ventilation slots. The design is minimal and unobtrusive.

Style: Clean technical product illustration on a white background. Isometric cutaway matching the sensor node illustration style. Precise labeling lines pointing to each component. White enclosure, green PCB, blue accent for the Ethernet jack. Professional product engineering aesthetic.
```
