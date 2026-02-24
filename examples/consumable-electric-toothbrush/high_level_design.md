### Consumable Electric Toothbrush — High-Level System Design

**Date:** 2026-02-24 | **Author:** Electrum workflow | **Status:** Draft

#### What It Is

A battery-powered vibrating toothbrush designed as a consumable — use it until the battery dies, then discard. A single alkaline cell powers an ERM vibration motor through a latching push button. A split bristle head concentrates oscillation at the bristles (Oral-B Pulsar architecture). Dual-injection overmolding seals the internals. No circuit board, no microcontroller, no wireless. Target retail: $3–5 (undercutting Oral-B Pulsar at $8–12), with ~350 minutes of motor runtime covering ~90 days of twice-daily brushing. Single SKU, blister-packed.

#### Block Diagram

```
  ┌───────────────────────────────────────────────────────────────────┐
  │              Consumable Electric Toothbrush                        │
  │                                                                    │
  │  ┌────────────┐  spring   ┌──────────────┐  wire   ┌───────────┐ │
  │  │  Alkaline   │  contact  │  Latching     │────────→│ ERM Motor │ │
  │  │  Cell       │─────────→│  Push Button   │         │ (cylindr.)│ │
  │  │  AAA 1.5V   │          └──────────────┘         └─────┬─────┘ │
  │  └──────┬─────┘                                          │       │
  │         │                                                 │       │
  │    ┌────┴─────┐                                    ┌─────┴─────┐ │
  │    │ Battery   │                                    │ Eccentric  │ │
  │    │ Cap +     │                                    │ Mass →     │ │
  │    │ O-ring    │                                    │ Linkage    │ │
  │    └──────────┘                                    └─────┬─────┘ │
  │                                                          │       │
  │                                              ┌───────────┴──────┐│
  │                                              │  Split Bristle   ││
  │                                              │  Head            ││
  │                                              │ ┌──────┬──────┐ ││
  │                                              │ │ Fixed │Moving│ ││
  │                                              │ │ Half  │ Half │ ││
  │                                              │ └──────┴──────┘ ││
  │                                              └─────────────────┘│
  │                                                                    │
  │  ╔════════════════════════════════════════════════════════════╗   │
  │  ║  1st shot: Rigid PP body (bristles insert-molded)          ║   │
  │  ║  2nd shot: TPE overmold (seals, grip, button boot)         ║   │
  │  ╚════════════════════════════════════════════════════════════╝   │
  └───────────────────────────────────────────────────────────────────┘

Power path:     Battery ──→ Switch ──→ Motor
Mechanical path: Motor ──→ Eccentric ──→ Linkage ──→ Moving head half ──→ Bristles
Seal strategy:  Insert-molded bristles │ TPE overmold body │ O-ring battery cap
```

#### Subsystems

| Subsystem | Purpose | Domain |
|-----------|---------|--------|
| Power cell (AAA alkaline, 1.5V) | Store energy for ~350+ min motor runtime | Electrical |
| Latching push-button switch | User on/off control; push-on, push-off mechanical latch | Electromechanical |
| ERM vibration motor (cylindrical) | Convert electrical energy to rotary eccentric vibration | Electromechanical |
| Split bristle head | Concentrate oscillation at bristle tips; fixed half anchors, moving half vibrates | Mechanical |
| Motor-to-head linkage | Transmit eccentric motion from motor shaft to moving head half | Mechanical |
| Rigid body (1st injection, PP) | Structural handle, motor pocket, battery tube, bristle anchor (insert-molded) | Mechanical |
| TPE overmold (2nd injection) | Seal all penetrations, soft-touch grip, button membrane, head joint boot | Mechanical |
| Battery cap + O-ring | Seal battery compartment at handle base; factory-installed, not user-serviceable | Mechanical |

#### Key Interfaces

| From → To | What Crosses | Protocol / Medium |
|-----------|-------------|-------------------|
| Battery → Switch | DC current, 1.5V, up to ~100 mA | Spring contact (battery) → wire → switch terminal |
| Switch → Motor | DC current, 1.5V, ~60–100 mA | Soldered wire |
| Motor → Moving head half | Rotary eccentric force → oscillating linear motion | Rigid plastic linkage arm from eccentric mass to head pivot |
| Fixed head half ↔ Moving head half | Pivot joint, ~1–2mm oscillation amplitude | Molded-in living hinge or pin pivot, sealed by TPE boot |
| Rigid body ↔ TPE overmold | Mechanical bond + seal | Chemical/mechanical adhesion during 2nd injection shot |
| Battery cap ↔ Handle base | Compression seal | Threaded cap compresses O-ring against molded seat |

#### Constraints

| Constraint | Value | Why It Matters |
|-----------|-------|----------------|
| BOM cost | < $1.50 at 100k units | Retail target $3–5 through distribution. Overmolding + insert-molded bristles add process cost vs. simpler designs. |
| Motor runtime | ≥ 350 minutes total | ~90 days at 2×/day, 2-min sessions. The battery capacity floor. |
| Battery shelf life | ≥ 2 years sealed in packaging | Retail channel shelf time. Alkaline meets this. |
| Water resistance | IPX5 (splashing from all directions) | Daily wet use for ~90 days. Three seal zones must hold: overmold, head joint, battery cap. |
| Material safety | Non-toxic, oral-contact safe (FDA food-contact grade) | PP body, TPE grip, nylon bristles, alkaline cell — all standard oral-care materials. |
| Handle diameter | ≤ 18mm at grip | AAA cell is 10.5mm dia → ~15–16mm handle OD with wall + TPE. Must feel like a toothbrush. |
| Tooling amortization | Dual-injection mold $15k–25k | Must produce ≥50k units to bring tooling cost below $0.50/unit. |

#### Fundamental Hardware Problems

| Problem | Why It's Fundamental |
|---------|---------------------|
| Sealing the split head pivot joint for 90 days of wet use | The moving bristle half must oscillate freely while the TPE boot keeps water out of the motor cavity. If this joint leaks, the motor corrodes and the product dies early. This is the hardest seal in the design because it's dynamic, not static. |
| Insert-molding bristles with a watertight seal at the base | Each bristle tuft penetrates the head surface. The first injection must flow completely around the bristle bases to form a seal. Any gap between nylon and PP is a capillary ingress path. Process control (injection pressure, temperature, bristle positioning) is critical. |
| Keeping BOM under $1.50 with dual-injection manufacturing | Overmolding is more expensive per-unit than single-shot molding. The O-ring cap adds a discrete part and assembly step. At $3–5 retail, margins are thin. The design must minimize part count and assembly steps. |

#### Component Choice Architecture

| Component | Dominant Axis | Key Tension | Resolution Direction |
|-----------|--------------|-------------|---------------------|
| Motor (cylindrical ERM) | Cost | Cheapest motors ($0.08) may have inconsistent eccentric balance at volume. Slightly better motors ($0.12–0.18) with tighter QC reduce field failures. | Budget $0.12–0.15. Vibration at 1.5V is proven (Oral-B Pulsar reference). Focus on QC consistency, not performance. |
| Battery (AAA alkaline) | Availability + cost | AAA is universally sourced at $0.05–0.08. AAAA would be slimmer but costs more and is harder to source. | AAA. Accept the ~15–16mm handle diameter. Universally available, cheapest option, runtime overshoots target (1000+ min) which just means longer product life. |
| Enclosure (dual-injection PP + TPE) | Cost vs. sealing | Single-shot + ultrasonic weld is cheaper per-unit but produces inferior seals. Dual-injection costs more upfront (tooling) but seals better and enables the TPE grip and head boot in one step. | Dual-injection. The sealing quality justifies the tooling investment at ≥100k volume. |
| Battery cap (threaded + O-ring) | Cost vs. reliability | Press-fit cap is cheaper ($0.01) but less reliable seal. Threaded cap + O-ring ($0.03–0.05 total) is proven. | Threaded + O-ring. The $0.03 premium buys reliable sealing for the product's entire life. |
| Bristle material (PA-612 nylon) | Performance | Standard nylon-612 is the industry default. Softer grades (for sensitive teeth) or harder grades (for deep cleaning) are the same cost. | Standard medium-stiffness PA-612. Single SKU, middle of the market. |

#### Three Hardest Problems

1. **Dynamic seal at the split head joint:** The moving bristle half oscillates ~1–2mm at 150+ Hz while the TPE boot must keep water out of the motor cavity below. This is a fatigue + sealing problem — the boot material must survive millions of flex cycles over 90 days in a wet, toothpaste-laden environment without cracking or delaminating from the rigid PP substrate.

2. **Insert-molding bristle seal quality at production speed:** Each brush head has ~30–40 bristle tufts, each penetrating the PP surface. At production volumes (seconds per unit), the injection process must consistently seal every tuft base. A single unsealed tuft is a water ingress path. This is a process control challenge, not a design challenge — the design is proven, but the manufacturing tolerance window is narrow.

3. **BOM cost discipline with dual-injection process:** The overmolding process adds ~$0.10–0.20 per unit vs. single-shot molding, and the tooling investment is 2–3× higher. With a retail target of $3–5 and distribution margins to cover, every component and assembly step must be ruthlessly cost-optimized. There is no room for "nice to have" features.

#### Open Calls

| Decision | Options | Deadline |
|----------|---------|----------|
| Battery format | AAA (recommended — cheap, universal, thick handle) vs. AAAA (slim handle, scarce supply) | Before component arrangement |
| Head pivot mechanism | Living hinge (one-piece, no assembly) vs. pin pivot (stronger, adds a part) | Before mold design |
| TPE hardness for head boot | Shore A 40 (very flexible, better seal, wears faster) vs. Shore A 60 (stiffer, more durable, tighter fit) | Before material spec |
