# Changelog

All notable changes to Electrum are documented here.

## v0.2.0 — 2026-10-15

- **Word fill-in forms** — `scripts/build_word_forms.py` builds the High-Level Design, System Description and Gate Checklist as Word forms, plus a workbook holding all three. Template headings and questions are fixed text; every answer area is a content control pre-filled with the Bubbler example in grey, which disappears when you type. The checklist has tick boxes and a PASS / FAIL / N/A dropdown. Sections of the System Description that expand a High-Level Design section point back to it instead of repeating it. The forms are on the [Electrum Word Kit](https://claude.ai/artifact/TeQUJAtvwVfo2a8iTkUymx) page.
- **What each document is for** — the README gains "The Documents" section: what the High-Level Design, System Description and Gate Checklist each are, who writes and reads them, when, and how they feed each other. Each Word form opens with an "About this document" paragraph. The `/electrum` skill orients first-time users before Phase 1 and frames Phases 2, 4 and 5.
- **Lead time and MOQ on the BOM** — the BOM table gains Lead time, MOQ (minimum order quantity) and Buy / Make columns. The Cost guidance asks for the critical-path parts and alternate sources.
- **Manufactured part lead times** — a new §9 table for parts made to your design: tooling, first articles and approval, and production run, each a fill-in in weeks, with the basis (supplier quote or own estimate).
- **Assembly and inspection times** — a new §9 table with assembly and inspection minutes per unit for each subassembly and for final assembly, and the bottleneck stage.
- **Gantt schedule** — §9 Schedule is now a task table (duration, dependencies, owner). The new `scripts/gantt.py` draws it as a Gantt chart with the critical path highlighted; Phase 4 of the skill runs it.
- **"Anything else on your mind?"** — before each document is final, the `/electrum` skill asks whether the user has concerns, constraints or ideas not yet covered, and folds them in.
- **Gate checklist** — four new items: long-lead and high-MOQ parts, manufactured part lead times, assembly and inspection times, and the critical-path schedule (now 103).
- **Bubbler example** — filled in for all of the above with illustrative estimates: a 30-week schedule with enclosure tooling on the critical path. Its gate checklist rows and summary tallies are updated to match.
- **DfX coverage** — the system description's §9 Constraints gains a Design for X subsection (manufacturing/assembly, test, packaging and logistics, sustainability and end of life, service and repair). The gate checklist adds 8 matching items. Phase 4 of the skill fills the subsection, scaled to the manufacturing context.

## v0.1.0 — 2026-05-28

First tagged release. Bundles everything below and adds:

- **Bubbler walkthrough** — soup-to-nuts worked example (`examples/bubbler-automated-soap-bubble-maker/`) showing what each of the 8 phases surfaces, with a `WALKTHROUGH.md` narrative.
- **Pop miniature popcorn machine** — second full-coverage example added to `examples/`.
- **PM quickstart** — README opens with a 3-step quickstart aimed at hardware PMs and product strategists.
- **Project hygiene** — added `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` (Contributor Covenant v2.1), `SECURITY.md`, issue templates (bug, feature), and PR template under `.github/`.
- **Documentation alignment** — README workflow table now reflects the canonical 8 phases (Component Arrangement added, Phase 6 corrected to Product Visual). Removed stale references to ChatGPT/DALL-E image generation; Phase 6 picks an existing diagram, no 3rd-party image services.
- **Security cleanup** — removed `generate_nanobanana.py` (contained an exposed API key).

MIT-licensed. Python 3.11+. See [README](README.md) for setup.

## 2026-02-25

- **Use local visuals in carousel** — Phase 6 now uses existing arrangement/block diagrams instead of generating images via ChatGPT/DALL-E. No 3rd-party services needed.
- **Light color scheme for diagrams** — Arrangement visualizer switched from dark (#1a1a2e) background to white/light-grey for better contrast and print readability.
- **Carousel rebuilt** — PPTX and PDF carousels now feature the arrangement diagram on the title page.

## 2026-02-25 (earlier)

- **Visual-first diagrams** — All architecture and arrangement diagrams are now matplotlib-generated PNGs, no ASCII art. Includes dark-themed block diagrams and arrangement cross-sections.
- **Stop-and-wait gates** — Skill now pauses after every generated file so the user can review before proceeding. Prevents output from scrolling past.
- **Progressive disclosure** — System description (Phase 4) is written in two stages (architecture first, then power/constraints) with user checkpoints between them.
- **Electromechanical support** — Phase 1 classifies products as static electronic, electromechanical, or hybrid. Electromechanical products get dedicated questions about physical architecture, mechanical subsystems, and structural design.
- **User questions at every phase** — Each phase now asks targeted questions (market, deployment, connectivity, component preferences, etc.) before generating output.
- **Generic reference examples** — Replaced hardcoded chair example with reusable reference documents for high-level design, system description, and gate checklist.

## 2025 (initial releases)

- **8-phase workflow** — Explore, High-Level Design, Component Arrangement, System Description, Gate Checklist, Product Visual, PPTX Carousel, PDF Carousel.
- **Electrum skill** — Claude Code skill for running the full product definition workflow from a one-line product idea.
- **Templates and checklists** — System description template (10 sections), gate checklist, skills map covering 16 hardware/software disciplines.
- **Carousel generation** — LinkedIn-format 4:5 portrait carousels in both PPTX (python-pptx) and PDF (ReportLab).
- **Example products** — Shusher, Haptic Metronome Bracelet, Consumable Electric Toothbrush, AirSense.
