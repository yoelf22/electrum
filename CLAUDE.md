# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Electrum is a product definition toolkit for software-augmented hardware. It provides a 5-phase AI-assisted workflow (via the `/electrum` Claude Code skill) that takes a one-sentence product idea through exploration, design, specification and validation, bundled into one HTML page. The toolkit also works without AI — the markdown templates in `templates/` can be filled in manually.

## Key Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browser (needed for image generation)
python -m playwright install chromium

# Run the main workflow (inside Claude Code)
/electrum <product idea in one sentence>

# Run scripts directly
python3.11 scripts/build_html.py output/<slug>
python3.11 scripts/build_docx.py output/<slug>     # Word export: cover, contents, documents
python3.11 scripts/block_diagram.py
python3.11 scripts/generate_illustration.py
```

There is no build system, test suite, or linter. The project is markdown templates + Python scripts.

## Architecture

### The `/electrum` Skill (`.claude/skills/electrum/SKILL.md`)

The core of the project. Defines a 5-phase sequential workflow:

1. **Explore** — Map HW/SW boundary, classify product (static electronic / electromechanical / hybrid), identify risks; propose the domain leads for user approval (`team.md`)
2. **High-Level Design** — Block diagram (matplotlib PNG) + one-page system overview
3. **Component Arrangement** — Spatial layout diagrams (matplotlib PNG, 2-3 alternatives side-by-side)
4. **System Description** — Full engineering spec (10 sections; §4 one subsection per approved lead, each with a Handoff block), written in two stages, then `executive_summary.md` written last from it and placed first in the bundle
5. **Gate Checklist** — 103-item PASS/FAIL/N/A validation against `templates/checklist.md`

Each phase writes files to `output/<slugified-idea>/` and stops for user review before advancing.

### Interaction Principles (enforced by the skill)

- **Visual-first**: All diagrams are matplotlib PNGs, never ASCII art (ASCII doesn't display in the CLI)
- **Stop-and-wait**: Pause after every output file for user acknowledgment
- **Progressive disclosure**: Break large documents into reviewable stages
- **Decisions before design**: Present visual alternatives before committing

### Python Scripts (`scripts/`)

Self-contained reference implementations. Each can be run independently with `python3.11`. They share a visual style:
- Dark theme: `#1A1A2E` background, `#22223A` cards
- 6-color accent palette: orange (`#FF8C00`), green (`#4EC978`), red, blue, purple
- Helper functions: `bg()`, `accent_strip()`, `card()`, `txt()`, `txt_wrap()`, `bar()`, `circle_num()`, `footer()`

### Templates (`templates/`)

Markdown directives that define the workflow structure, not filled-in examples. Key files:
- `hw_sw_product_initiation.md` — Workflow overview
- `hw_sw_high_level.md` — Phase 2 template
- `system_description_template.md` — Phase 4 template (10 sections)
- `executive_summary.md` — Phase 4 Stage C template (business rationale, solution, domain rows)
- `checklist.md` — 103-item gate checklist
- `skills_map.md` — 16 competency areas for HW/SW products

### Examples (`examples/`)

Seven worked examples with complete output artifacts. The `bubbler-automated-soap-bubble-maker/` example is the most complete and includes `WALKTHROUGH.md`.

### Reference (`reference/`)

Worked reference documents (high-level design, system description, gate checklist) used by the skill as examples when generating output.

## Releasing

Bump the two `Electrum vX.Y.Z` strings in `.claude/skills/electrum/SKILL.md` (title line and orientation) and add the CHANGELOG entry, commit, then tag `vX.Y.Z` and push the tag; the workflow builds the ZIP. `grep -n 'Electrum v' .claude/skills/electrum/SKILL.md` must show the tag's version.

## Conventions

- **Commit messages**: `type(scope): short description` — types: `feat`, `fix`, `docs`, `refactor`, `chore`
- **Markdown**: ATX-style headings (`##`), ~100 char line wrap
- **Component specificity**: Always use real component names (nRF52840, BMI270), real protocols (BLE 5.0 GATT, MQTT over TLS), and real numbers (3.7V 500mAh LiPo) — no placeholders or TODOs in output
- **New examples**: Place under `examples/` with a descriptive hyphenated folder name
- **Output directories**: `output/<slugified-idea>/` — lowercase, hyphens, no special chars, max ~50 chars

## Dependencies

Python 3.11+. Key packages: `matplotlib`, `numpy`, `markdown`, `python-pptx`, `playwright`, `anthropic>=0.42.0`, `openai>=1.0.0`.
