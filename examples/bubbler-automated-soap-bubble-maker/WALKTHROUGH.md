# Walkthrough: Bubbler — Automated Soap Bubble Machine

*A complete Electrum run, from one-line idea to gate review.*

This walkthrough shows what happened when we ran `/electrum automated soap bubble machine that optimizes for large bubbles using sensor feedback` through all eight phases. It took about 90 minutes of interactive dialogue. Here's what the process surfaced — and what we would have missed without it.

## The Starting Point

The idea seemed straightforward: a consumer device that dips a wand into soap solution, lifts it, and blows air through the film to make large bubbles. Battery-powered, sub-$50, outdoor use.

If you stopped here, you'd start shopping for motors and fans. That's where most teams go wrong.

## Phase 1: Explore — Finding the Real Product

The exploration phase classified Bubbler as **electromechanical** — it moves air, rotates a mechanical arm, and uses closed-loop sensor feedback. This classification matters because it determines what questions come next: structural loads, motion control, media handling (soap solution).

**What the process surfaced:** The central technical question isn't "how do we blow bubbles" — it's "how does the firmware know what's happening to the soap film?" The exploration mapped four sensing approaches:

| Approach | Cost | Signal Quality | Practicality |
|----------|------|---------------|--------------|
| IR break-beam | ~$1.50 | Binary only | Needs components spanning the 160mm loop |
| Duct pressure | ~$2.00 | Overwhelmed by outdoor wind | Poor outdoors |
| Motor current | ~$0.00 | Too small vs. baseline draw | Unreliable |
| **Strain gauge on pivot** | **~$0.80** | **Continuous inflation curve** | **Fully internal, compact** |

The strain gauge approach won on every dimension. A $0.30 strain gauge plus a $0.50 HX711 ADC gives firmware a real-time force curve: slope = inflation rate, peak = bubble size, sudden drop = pop vs. clean detach.

**What we would have missed:** Without structured exploration, most teams would reach for IR break-beam (the obvious choice) and discover its limitations during prototyping.

→ Output: [`explore_notes.md`](explore_notes.md)

## Phase 2: High-Level Design — The Block Diagram

The high-level design produced a block diagram and identified the three hardest unsolved problems:

1. **Film survival during wand rotation** — the soap film must survive a 175-degree rotation from horizontal (dip) to vertical (blow) without tearing
2. **Force-curve interpretation** — firmware must distinguish a healthy inflation from a failing one, in real time, using only the strain gauge signal
3. **Wind compensation** — outdoor use means variable airflow that the system can't control

These three problems shape every downstream decision: motor speed, fan ramp profile, control loop timing, even enclosure geometry (wind shielding).

→ Output: [`high_level_design.md`](high_level_design.md), [`block_diagram.png`](block_diagram.png)

## Phase 3: Component Arrangement — Spatial Reality

The arrangement phase inventoried every physical element and generated cross-section diagrams showing how they fit together. This is where "it should be compact" meets real dimensions:

- The vat needs to be 200×170mm to accommodate the 160mm loop
- The motor, PCB, battery, and fan all need to stack inside a tapered enclosure on one side
- The air duct needs an L-bend to redirect airflow from vertical (fan) to horizontal (toward the loop)

→ Output: [`component_arrangement.md`](component_arrangement.md), [`arrangement_options.png`](arrangement_options.png)

## Phase 4: System Description — Naming Real Parts

The system description forced specifics:

- **MCU:** nRF52840 (overkill for MVP, but supports BLE for optional app)
- **Motor driver:** H-bridge for bidirectional wand arm control
- **ADC:** HX711 for strain gauge (24-bit, 80 SPS — fast enough for inflation curves)
- **Power:** LiPo 3.7V, ~1.5W peak draw, estimated 2-hour runtime
- **Control loop:** 50ms sample period, adaptive fan PWM based on force-curve slope

The specifics exposed a firmware architecture question: does the optimization loop run as a state machine (simpler, deterministic) or as a PID controller (smoother, harder to tune)? The system description chose a hybrid — state machine for the dip/rotate/blow sequence, with PID control only during the blow phase for fan speed modulation.

→ Output: [`system_description.md`](system_description.md)

## Phase 5: Gate Checklist — What We're Still Assuming

The 90-item gate review is where the process earns its keep. Selected findings:

**PASS (examples):**
- Sensor sampling rate compatible with processing pipeline (80 SPS vs. 50ms control loop)
- Power budget accounts for peak motor + fan + MCU draw
- Firmware update strategy defined (USB-C DFU for this product tier)

**FAIL (examples):**
- No defined behavior for watchdog timer if firmware crashes mid-optimization
- No factory calibration procedure for the strain gauge (zero-offset varies per unit)
- No specification for soap solution viscosity range (affects film thickness and survival)
- Wind speed threshold for automatic shutdown not defined

Each FAIL is a conversation the team hasn't had yet. Some are simple to resolve (add a watchdog reset that returns the wand to home position). Others reshape the product (soap solution viscosity tolerance may require a specific formulation, which changes the BOM and supply chain).

→ Output: [`gate_checklist.md`](gate_checklist.md)

## Phases 6–8: Communication Materials

The remaining phases generated visual diagrams, a PPTX carousel, and a PDF — useful for sharing the concept with stakeholders or investors, but the engineering value is in phases 1–5.

→ Output: [`Bubbler_Carousel.pptx`](Bubbler_Carousel.pptx), [`Bubbler_Carousel.pdf`](Bubbler_Carousel.pdf)

## What We Learned

The structured process turned a "simple bubble machine" into a product with a clear technical identity: **a force-sensing feedback system that happens to make bubbles.** That reframing changes how you staff the project (you need someone who understands signal processing, not just mechanical design), how you prioritize the prototype (validate the strain gauge signal first, not the enclosure), and how you pitch it (the optimization loop is the differentiator, not the bubble size).

Without the process, the team would have built a motor-and-fan prototype, discovered the IR sensor doesn't work outdoors, pivoted to strain gauges at EVT, and lost two months.

## Try It Yourself

```bash
claude
> /electrum <your product idea>
```

The process works best with ideas you're uncertain about — the weirder, the better. The goal isn't to produce a final spec. It's to find out what you're still assuming.
