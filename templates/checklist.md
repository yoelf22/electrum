# System Description Completeness Checklist — Software-Augmented Hardware

Run through this checklist when you believe the system description is ready for review. Every unchecked box is either a gap to fill or a conscious scope decision to document.

This checklist is for products where physical hardware and software (firmware, companion apps, cloud services) are designed together. Items marked with **[HW↔SW]** specifically target the hardware/software boundary.

---

## Vision and Context
- [ ] Product statement is a single clear sentence
- [ ] Problem being solved is stated explicitly
- [ ] **[HW↔SW]** Which capabilities require physical hardware vs. software is stated
- [ ] **[HW↔SW]** What value the software adds on top of the hardware is clear (not just "it has an app")
- [ ] Deployment environment is defined (indoor/outdoor, setting, user type)
- [ ] Expected product lifespan is stated — for both hardware and software support

## User Scenarios
- [ ] At least 3 concrete scenarios with persona, situation, action, outcome
- [ ] **[HW↔SW]** Each scenario traces through the full stack: physical interaction → firmware → app/cloud → user feedback
- [ ] Includes at least 1 error/edge-case scenario (low battery, lost connection, firmware crash, app force-quit)
- [ ] **[HW↔SW]** First-time experience is described end-to-end: unboxing → charging → pairing → app setup → first value
- [ ] Most common interaction is identified
- [ ] **[HW↔SW]** Offline/degraded scenarios are covered: what works when the app is closed? When the cloud is unreachable? When Bluetooth disconnects mid-operation?

## System Architecture
- [ ] Block diagram covers all major subsystems — hardware, firmware, app, and cloud as distinct blocks
- [ ] Every subsystem in the diagram has a description in the subsystem section
- [ ] **[HW↔SW]** Every arrow between a hardware block and a software block specifies the protocol, data format, and direction
- [ ] Data flows between subsystems are identified (what data, what direction, what rate)
- [ ] Trust/security boundaries are marked — especially the boundary between device and cloud
- [ ] Architecture narrative explains the "why" of the structure
- [ ] **[HW↔SW]** The diagram makes clear where processing happens (on-device vs. on-phone vs. in-cloud) for each major feature
- [ ] Fundamental hardware problems are identified — the physics, geometry, or environment problems that must be solvable for the product to exist
- [ ] Each fundamental hardware problem has a stated resolution path or is flagged as requiring prototyping

## Subsystem Descriptions

### Hardware
- [ ] MCU/SoC selected with rationale — processing headroom for current firmware plus planned features
- [ ] For each major component, the dominant tradeoff axis is identified (physical constraint, performance, availability, cost, or firmware complexity)
- [ ] Component tradeoff conflicts are surfaced — where two axes pull in opposite directions, the chosen resolution is stated
- [ ] All sensors listed with interface, sample rate, and key specs
- [ ] Actuators and physical UI elements listed (LEDs, buttons, haptics, displays)
- [ ] PCB strategy described (single board, flex, modular)
- [ ] **[HW↔SW]** Hardware test points and debug interfaces documented (JTAG/SWD, UART console, test pads)

### Firmware
- [ ] OS/framework chosen with rationale (RTOS, bare-metal, Linux)
- [ ] Major modules listed with responsibilities
- [ ] **[HW↔SW]** Hardware abstraction layer (HAL) boundaries defined — what firmware exposes to higher layers vs. what talks directly to registers
- [ ] **[HW↔SW]** OTA update strategy defined: delivery mechanism (BLE DFU, Wi-Fi, app-mediated), image signing, rollback on failure, A/B partitioning
- [ ] **[HW↔SW]** On-device vs. cloud processing boundary is clear — what data is processed locally, what is sent raw, what triggers are evaluated on-device
- [ ] **[HW↔SW]** Firmware versioning scheme defined — how the app and cloud know which firmware version is running and what features it supports

### Companion App
- [ ] Platform and framework chosen (iOS, Android, cross-platform)
- [ ] Core screens and flows listed
- [ ] **[HW↔SW]** Device communication protocol defined: BLE service/characteristic UUIDs, GATT profile, or equivalent for Wi-Fi/other
- [ ] **[HW↔SW]** App behavior when device is disconnected is specified (cached data, reconnection strategy, user messaging)
- [ ] **[HW↔SW]** Pairing and authentication flow documented step-by-step from both the app and device perspective
- [ ] App store requirements and constraints noted (background BLE, permissions, review guidelines)

### Cloud / Backend
- [ ] Platform/infrastructure chosen
- [ ] **[HW↔SW]** Device provisioning approach defined — how a new device gets identity, certificates, and cloud registration
- [ ] Data model documented (types, rates, retention, privacy implications)
- [ ] **[HW↔SW]** Device management capabilities listed: remote configuration, firmware deployment, device health monitoring, fleet segmentation
- [ ] **[HW↔SW]** Device-to-cloud authentication method specified (certificates, tokens, pre-shared keys)

## Interfaces
- [ ] Every internal bus/connection listed (I2C, SPI, UART, GPIO, ADC)
- [ ] Every external interface listed (wireless, USB, debug)
- [ ] Physical connectors documented (charging, debug, expansion)
- [ ] No subsystem is an island — every block connects to something
- [ ] Protocol specified for each interface
- [ ] **[HW↔SW]** Every HW↔FW interface specifies: signal/register level details, interrupt behavior, DMA if applicable
- [ ] **[HW↔SW]** Every FW↔App interface specifies: protocol, message format, error codes, reconnection behavior
- [ ] **[HW↔SW]** Every App↔Cloud interface specifies: API endpoints or topics, authentication, payload schema, rate limits
- [ ] **[HW↔SW]** Data format transformations are documented — how raw sensor data becomes user-facing values at each layer

## Power Architecture
- [ ] Power source and capacity specified
- [ ] Power states defined with transition triggers
- [ ] Power budget table filled for at least the primary operating mode
- [ ] Target battery life stated
- [ ] Feasibility check: back-of-envelope calculation done
- [ ] Charging method specified (if applicable)
- [ ] **[HW↔SW]** Firmware's role in power management is defined — which power state transitions are firmware-controlled, which are hardware-controlled
- [ ] **[HW↔SW]** Radio duty cycle is specified and its impact on app responsiveness is noted (e.g., "BLE advertising interval of 1s means connection takes up to 1.5s")

## Connectivity
- [ ] Primary connectivity technology chosen with rationale
- [ ] Protocol stack documented (physical through application layer)
- [ ] Data transmission frequency, payload size, and daily volume estimated
- [ ] **[HW↔SW]** Provisioning/pairing flow described step-by-step — from both device side (firmware) and app side
- [ ] **[HW↔SW]** Offline behavior defined for every layer: what the device does, what the app does, what happens on reconnection (sync strategy)
- [ ] **[HW↔SW]** Connection recovery is specified — how firmware and app handle dropped connections, partial transfers, and out-of-order messages

## Key Decisions
- [ ] At least 3 non-obvious technical decisions documented
- [ ] Each decision lists options considered, chosen approach, and rationale
- [ ] Consequences and risks are stated for each decision
- [ ] The 3 decisions that would force a major redesign if reversed are identified
- [ ] **[HW↔SW]** HW/SW tradeoff decisions are explicit: what is done in hardware vs. firmware vs. app vs. cloud, and why

## Constraints
- [ ] Required certifications listed (FCC, CE, UL, etc.)
- [ ] Operating environment defined (temperature, IP rating, humidity, vibration)
- [ ] Target BOM cost or cost range stated
- [ ] Target production volume stated
- [ ] Key schedule milestones listed
- [ ] Third-party dependencies identified
- [ ] **[HW↔SW]** App store and platform constraints noted (iOS background execution limits, Android battery optimization, minimum OS versions)
- [ ] **[HW↔SW]** Manufacturing test requirements identified — what firmware/software is needed on the production line for device testing and provisioning

## Open Questions and Risks
- [ ] All open questions have an owner and target resolution date
- [ ] High-impact risks have mitigation plans or are flagged for prototyping
- [ ] No question has been open for more than 2 weeks without progress
- [ ] **[HW↔SW]** Cross-domain risks are flagged — risks where a hardware problem can only be mitigated by software (or vice versa)

## Overall Quality
- [ ] No section is still placeholder-only (every section has real content)
- [ ] Consistent terminology throughout (glossary updated)
- [ ] Diagrams match the text (no orphan blocks, no missing connections)
- [ ] **[HW↔SW]** Cross-domain consistency check: power budget matches connectivity choice, firmware features match MCU capabilities, app features match firmware API, cloud data model matches device telemetry
- [ ] **[HW↔SW]** A reviewer from hardware/EE has reviewed software assumptions; a reviewer from software has reviewed hardware assumptions
- [ ] Open questions are either resolved or explicitly carried into PRD as TBDs
