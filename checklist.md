# System Description Completeness Checklist

Run through this checklist when you believe the system description is ready for review. Every unchecked box is either a gap to fill or a conscious scope decision to document.

---

## Vision and Context
- [ ] Product statement is a single clear sentence
- [ ] Problem being solved is stated explicitly
- [ ] Deployment environment is defined (indoor/outdoor, setting, user type)
- [ ] Expected product lifespan is stated

## User Scenarios
- [ ] At least 3 concrete scenarios with persona, situation, action, outcome
- [ ] Includes at least 1 error/edge-case scenario (low battery, lost connection, etc.)
- [ ] First-time experience (unboxing to first value) is described
- [ ] Most common interaction is identified

## System Architecture
- [ ] Block diagram covers all major subsystems
- [ ] Every subsystem in the diagram has a description in Section 4
- [ ] Data flows between subsystems are identified (what data, what direction, what rate)
- [ ] Trust/security boundaries are marked or noted
- [ ] Architecture narrative explains the "why" of the structure

## Subsystem Descriptions
- [ ] Hardware: MCU/SoC selected with rationale
- [ ] Hardware: All sensors listed with interface, sample rate, and key specs
- [ ] Hardware: Actuators and physical UI elements listed
- [ ] Hardware: PCB strategy described
- [ ] Firmware: OS/framework chosen with rationale
- [ ] Firmware: Major modules listed with responsibilities
- [ ] Firmware: OTA update strategy defined (method, rollback, signing)
- [ ] Firmware: On-device vs. cloud processing boundary is clear
- [ ] App: Platform and framework chosen
- [ ] App: Core screens and flows listed
- [ ] App: Device communication protocol defined
- [ ] Cloud: Platform/infrastructure chosen
- [ ] Cloud: Device provisioning approach defined
- [ ] Cloud: Data model documented (types, rates, retention)
- [ ] Cloud: Device management capabilities listed

## Interfaces
- [ ] Every internal bus/connection listed (I2C, SPI, UART, GPIO, ADC)
- [ ] Every external interface listed (wireless, USB, debug)
- [ ] Physical connectors documented (charging, debug, expansion)
- [ ] No subsystem is an island — every block connects to something
- [ ] Protocol specified for each interface

## Power Architecture
- [ ] Power source and capacity specified
- [ ] Power states defined with transition triggers
- [ ] Power budget table filled for at least the primary operating mode
- [ ] Target battery life stated
- [ ] Feasibility check: back-of-envelope calculation done
- [ ] Charging method specified (if applicable)

## Connectivity
- [ ] Primary connectivity technology chosen with rationale
- [ ] Protocol stack documented (physical through application layer)
- [ ] Data transmission frequency, payload size, and daily volume estimated
- [ ] Provisioning/pairing flow described step-by-step
- [ ] Offline behavior defined

## Key Decisions
- [ ] At least 3 non-obvious technical decisions documented
- [ ] Each decision lists options considered, chosen approach, and rationale
- [ ] Consequences and risks are stated for each decision
- [ ] The 3 decisions that would force a major redesign if reversed are identified

## Constraints
- [ ] Required certifications listed (FCC, CE, etc.)
- [ ] Operating environment defined (temperature, IP rating, etc.)
- [ ] Target BOM cost or cost range stated
- [ ] Target production volume stated
- [ ] Key schedule milestones listed
- [ ] Third-party dependencies identified

## Open Questions and Risks
- [ ] All open questions have an owner and target resolution date
- [ ] High-impact risks have mitigation plans or are flagged for prototyping
- [ ] No question has been open for more than 2 weeks without progress

## Overall Quality
- [ ] No section is still placeholder-only (every section has real content)
- [ ] Consistent terminology throughout (glossary updated)
- [ ] Diagrams match the text (no orphan blocks, no missing connections)
- [ ] A second person has reviewed the document
- [ ] Open questions are either resolved or explicitly carried into PRD as TBDs
