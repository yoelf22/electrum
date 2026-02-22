# Product Definition Toolkit for Software-Augmented Hardware

## The Problem

Software PMs have established tools — user stories, PRDs, sprint planning. Pure hardware PMs have theirs — datasheets, BOMs, DFM checklists. But when the product is *both* — firmware-driven hardware with sensors, actuators, maybe an app, maybe cloud — most PMs either use a software PRD template that ignores physics, or a hardware spec that ignores the software.

The boundary between HW and SW is where the expensive mistakes happen, and it's usually the least documented part.

## What This Toolkit Does

A repeatable process for defining hardware products that have software inside them — so the firmware team and the mechanical team aren't surprised by each other at EVT.

It takes a product idea from "I think this could work" through to a structured system description that engineering can build from. Four phases:

1. **Explore** — Map the HW/SW boundary, identify knowledge gaps
2. **High-Level Design** — Produce a single-page system overview: blocks, interfaces, constraints, fundamental hardware problems, and component tradeoffs
3. **Describe** — Write the full system description with HW and SW in lockstep
4. **Gate** — Validate completeness across both domains, then feed into PRD

The toolkit forces the HW↔SW boundary into the open from day one. Every template, every checklist item tagged `[HW↔SW]`, and every worked example traces decisions across that boundary.

## What's in the Box

| File | What it does |
|------|-------------|
| `hw_sw_product_initiation.md` | 4-phase workflow from concept to PRD |
| `hw_sw_high_level.md` | Single-page system overview template — enough for an executive or a first architecture review. Includes fundamental hardware problems and component choice architecture. |
| `templates/system_description_template.md` | Full system description template with HW↔SW boundary items built in |
| `checklist.md` | Gate checklist — 90 items, each tagged if it targets the HW/SW boundary |
| `skills_map.md` | 16 competency areas a PM should understand or staff for |

## Worked Examples

Two products, same process, very different complexity:

| Project | What it is | Complexity |
|---------|-----------|-----------|
| `examples/chair_balancing_act/` | Clip-on tilt sensor that plays a continuously escalating tone when a chair leaves static balance | Bare-metal standalone — no app, no cloud, no connectivity. MCU-generated audio, coin cell power. |
| `examples/smart_sensor_hub/` | Wireless indoor environment monitor (CO2, temp, humidity, PM) with BLE sensor nodes, per-floor gateways, and cloud dashboard | Multi-tier — battery nodes + gateways + cloud. BLE architecture, power-constrained sensing, fleet OTA. |

Each project folder contains a high-level design and system description. The Chair Balancing Act example also includes a gate checklist, PRD, and generated presentation deck.

## How to Use

The core toolkit is markdown templates and checklists — no installation required. The worked examples also include Python scripts for generating presentation decks and diagrams. To run those:

```
pip install -r requirements.txt
```

To apply the toolkit to your product:

1. **Understand the process** — Read [`hw_sw_product_initiation.md`](hw_sw_product_initiation.md) to see how the four phases fit together. Skim a worked example in `examples/` to see what finished output looks like.
2. **Assess your gaps** — Review [`skills_map.md`](skills_map.md) to figure out where you (or your team) need help.
3. **Create the high-level design** — Copy [`hw_sw_high_level.md`](hw_sw_high_level.md) into your project folder and fill it in. This produces the single-page system overview.
4. **Write the full system description** — Copy [`templates/system_description_template.md`](templates/system_description_template.md) into your project folder and work through each section.
5. **Validate** — Run through [`checklist.md`](checklist.md) to confirm nothing was missed, especially at the HW↔SW boundary.

## Who This is For

Hardware product managers and technical leads building products where physical hardware and software must be designed together. The toolkit is most useful when:

- Your product has firmware, and maybe a companion app or cloud backend
- Your team spans EE/ME and software disciplines
- You need documents that both an executive and an engineer can use
- You've been burned before by HW/SW integration surprises at EVT (Engineering Validation Test)
