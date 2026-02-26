# Electrum — Product Definition Toolkit for Software-Augmented Hardware

## The Problem

Software PMs have established tools — user stories, PRDs, sprint planning. Pure hardware PMs have theirs — datasheets, BOMs, DFM checklists. But when the product is *both* — firmware-driven hardware with sensors, actuators, maybe an app, maybe cloud — most PMs either use a software PRD template that ignores physics, or a hardware spec that ignores the software.

The boundary between HW and SW is where the expensive mistakes happen, and it's usually the least documented part.

## Quickstart for PMs and Product Strategists

You have a connected product idea and want to stress-test it before committing resources. Here's the fastest path:

```bash
# 1. Install Claude Code (https://docs.anthropic.com/en/docs/claude-code)
# 2. Clone this repo and open a terminal in it
git clone https://github.com/yoelf22/electrum.git && cd electrum

# 3. Start Claude Code and run the skill
claude
> /electrum <describe your product in one sentence>
```

The process will walk you through a structured dialogue — mapping the HW/SW boundary, forcing specifics, and surfacing what you're still assuming. It pauses after every output for your review. Budget 60–90 minutes for a full run.

**Don't have Claude Code?** The templates work without AI. Copy `templates/system_description_template.md` into your project folder, fill it in by hand, then run through `templates/checklist.md`. That's 80% of the value.

**Want to see what a full run looks like?** Read the [Bubbler walkthrough](examples/bubbler-automated-soap-bubble-maker/WALKTHROUGH.md) — a soup-to-nuts example that turned "automated soap bubble machine" into a force-sensing feedback system with a 90-item gate review.

---

## What This Toolkit Does

A repeatable, AI-assisted process for defining hardware products that have software inside them — so the firmware team and the mechanical team aren't surprised by each other at EVT.

It takes a product idea from "I think this could work" through to a structured system description, product illustrations, and a presentation-ready carousel. Eight phases, driven by the `/electrum` Claude Code skill:

| Phase | Output | Description |
|-------|--------|-------------|
| 1. **Explore** | `explore_notes.md` | Map the HW/SW boundary, identify knowledge gaps, surface risks |
| 2. **High-Level Design** | `high_level_design.md` | Single-page system overview: blocks, interfaces, constraints, hardest problems |
| 3. **System Description** | `system_description.md` | Full engineering-grade spec with real components, power budgets, firmware architecture |
| 4. **Gate Checklist** | `gate_checklist.md` | Validate completeness across both domains (90 items, PASS/FAIL/N/A) |
| 5. **Image Generation** | `cross_section_illustration_*.png` | Product illustrations via ChatGPT DALL-E (browser automation) |
| 6. **PPTX Carousel** | `*_Carousel.pptx` | LinkedIn-format slide deck (4:5 portrait, dark theme, 8 pages) |
| 7. **PDF Carousel** | `*_Carousel.pdf` | Same carousel as multi-page PDF |

Phases 1-4 produce the engineering definition. Phases 5-7 turn it into visual presentation materials.

## Prerequisites

### Python dependencies

```bash
pip install -r requirements.txt
```

Required packages: `python-pptx`, `reportlab`, `playwright`, `matplotlib`, `numpy`.

### Playwright browser (for image generation)

```bash
pip install playwright
python -m playwright install chromium
```

### ChatGPT account (for image generation)

Phase 5 uses Playwright to automate ChatGPT's web UI for DALL-E image generation. **No API key needed** — authentication happens through ChatGPT's own login flow.

On the first run, the script opens a Chromium browser window and navigates to ChatGPT's login page. **You must log in manually** (Google, email, or any supported method). The session is saved to a persistent browser profile (`~/.chatgpt_playwright_profile/`), so subsequent runs skip login automatically.

**This means an active ChatGPT account with DALL-E access is required.** Free-tier accounts may have limited image generation. If your session expires, the script will prompt you to log in again.

### Claude Code (for the `/electrum` skill)

Install [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and open a terminal in this repo. The `/electrum` skill is automatically available:

```bash
claude
> /electrum smart posture-correcting office chair
```

## Repository Structure

```
├── scripts/          # Python reference implementations (carousel, diagrams, deck builders)
├── templates/        # Directive markdown files (workflow, checklists, templates)
├── examples/         # Worked examples with full output artifacts
│   ├── bubbler-automated-soap-bubble-maker/   ← start here (has WALKTHROUGH.md)
│   ├── pop-miniature-popcorn-machine/
│   ├── metronome/
│   ├── chair_balancing_act/
│   ├── consumable-electric-toothbrush/
│   ├── shusher/
│   └── smart_sensor_hub/
└── output/           # Raw output from recent runs
```

## What's in the Box

### Templates and Checklists

| File | What it does |
|------|-------------|
| `electrum/templates/hw_sw_product_initiation.md` | 7-phase workflow from concept to presentation |
| `electrum/templates/hw_sw_high_level.md` | Single-page system overview template |
| `electrum/templates/system_description_template.md` | Full system description template with HW↔SW boundary items |
| `electrum/templates/checklist.md` | Gate checklist — 90 items, each tagged if it targets the HW/SW boundary |
| `electrum/templates/skills_map.md` | 16 competency areas a PM should understand or staff for |
| `.claude/skills/electrum/SKILL.md` | Claude Code skill definition (drives the 7-phase workflow) |

### Reference Scripts

| File | What it does |
|------|-------------|
| `electrum/scripts/generate_illustration.py` | DALL-E image generation via Playwright browser automation |
| `electrum/scripts/build_carousel.py` | PPTX + PDF carousel builder (LinkedIn-format, 4:5 portrait) |
| `electrum/scripts/build_deck.py` | Executive product overview deck builder |
| `electrum/scripts/build_high_level_deck.py` | High-level design deck builder |
| `electrum/scripts/visualize.py` | Visualization utilities |
| `electrum/scripts/block_diagram.py` | Block diagram generator |

### Worked Examples

| Project | What it is | Phases covered |
|---------|-----------|----------------|
| [`bubbler-automated-soap-bubble-maker/`](examples/bubbler-automated-soap-bubble-maker/) | Force-sensing automated bubble machine with adaptive optimization — **[full walkthrough](examples/bubbler-automated-soap-bubble-maker/WALKTHROUGH.md)** | All 8 phases |
| `pop-miniature-popcorn-machine/` | Miniature countertop popcorn machine with heating and motor control | Explore, HLD, system description, gate checklist, carousel |
| `metronome/` | Wrist-worn haptic metronome bracelet for musicians — silent, precise beat pulses | All phases |
| `chair_balancing_act/` | Clip-on tilt sensor that plays an escalating tone when a chair leaves static balance | HLD, system description, gate checklist |
| `consumable-electric-toothbrush/` | Disposable electric toothbrush with wear tracking | Full |
| `shusher/` | Noise-aware mechanical mute device with sound detection | HLD, system description, gate checklist |
| `smart_sensor_hub/` | Wireless indoor environment monitor (CO2, temp, humidity, PM) with BLE mesh | HLD, system description |

The bubbler example includes a [step-by-step walkthrough](examples/bubbler-automated-soap-bubble-maker/WALKTHROUGH.md) showing what each phase surfaced and what the team would have missed without the process.

## How to Use

### With Claude Code (recommended)

1. Open a terminal in this repo
2. Run `claude` to start Claude Code
3. Type `/electrum <your product idea>`
4. Walk through all 8 phases interactively — Claude drafts, you review and refine at each step
5. Final output: a complete product definition + diagrams + presentation deck

### Without Claude Code

The core toolkit is markdown templates and checklists — no AI required:

1. **Understand the process** — Read `electrum/templates/hw_sw_product_initiation.md` for the workflow overview
2. **Assess your gaps** — Review `electrum/templates/skills_map.md` for team competency planning
3. **Create the high-level design** — Copy `electrum/templates/hw_sw_high_level.md` into your project folder and fill it in
4. **Write the system description** — Copy `electrum/templates/system_description_template.md` and work through each section
5. **Validate** — Run through `electrum/templates/checklist.md` to confirm nothing was missed

For image generation and carousel building, adapt the scripts in `electrum/scripts/` to your product.

## Who This is For

Hardware product managers and technical leads building products where physical hardware and software must be designed together. The toolkit is most useful when:

- Your product has firmware, and maybe a companion app or cloud backend
- Your team spans EE/ME and software disciplines
- You need documents that both an executive and an engineer can use
- You want presentation-ready materials alongside the engineering spec
- You've been burned before by HW/SW integration surprises at EVT
