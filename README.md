# System Description Toolkit for Software-Augmented Hardware

A structured approach to writing architecture-level system descriptions for hardware products whose value depends on software — firmware, companion apps, cloud services, or all three.

## What This Is

Templates and guidance for the documents that sit between a product concept and a formal PRD. The toolkit produces two artifacts:
1. A **single-page high-level system design** — blocks, interfaces, constraints, fundamental hardware problems, and component tradeoff analysis. Enough for executive alignment or partner discussions.
2. A **detailed system description** — subsystem specs, interface contracts, power architecture, and connectivity design

## Quick Start

1. Read `hw_sw_product_initiation.md` for the full process
2. Review `skills_map.md` to identify your knowledge gaps
3. Fill in `hw_sw_high_level.md` to produce the single-page system overview
4. Copy `templates/system_description_template.md` to your project folder and write the full description
5. Validate with `checklist.md`

## Files

| File | Purpose |
|------|---------|
| `hw_sw_product_initiation.md` | Process guide: idea → high-level design → system description → PRD |
| `hw_sw_high_level.md` | Single-page high-level system design — template and process, includes fundamental hardware problems and component choice architecture |
| `skills_map.md` | 16 competency areas for SW-augmented HW system description writing |
| `templates/system_description_template.md` | Guided template with sections, prompts, and diagram placeholders |
| `checklist.md` | Completeness checklist — run before converting to PRD |
| `examples/smart_sensor_hub.md` | Partially worked example |
| `chillstream/` | Worked example: plumbed-in water dispenser with PCM thermal battery |
| `chair_balancing_act/` | Worked example: tilt-sensing audio feedback clip-on for fixed-leg chairs |

## Target Audience

Product managers and technical leads working on software-augmented hardware who need to bridge the gap between product concept and engineering requirements — for both hardware and software teams.
