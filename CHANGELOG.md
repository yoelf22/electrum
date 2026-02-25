# Changelog

All notable changes to Electrum are documented here.

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
