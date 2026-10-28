# Changelog

All notable changes to Electrum are documented here.

## v0.6.1 — 2026-10-28

- **The skill states its version** — SKILL.md opens with `Electrum vX.Y.Z` and the releases link, and the orientation repeats it at the start of every run, so a user of an uploaded copy can see it is stale. README gains "Which version do I have?". Release step: bump the two version strings in SKILL.md and the CHANGELOG before tagging.

## v0.6.0 — 2026-10-28

- **Team first** — Phase 1 proposes the domain leads the product needs (product, electrical, firmware, mechanical/industrial design, app, cloud, ML/data, UX, security and compliance, manufacturing/NPI), each with why and what it owns, marked required or recommended, and walks them through role by role (keep / remove / merge / change ownership), asks what is missing, then requires explicit approval of the final roster before anything is designed; nothing is written until approved, even hands-free. Written to `team.md`. New question keys `phase1.team.<role>`, `phase1.team.add`, `phase1.team` and `phase1.competition`.
- **Spec split by role** — §4 of the System Description has one subsection per approved lead, in the team's order (4.5 Mechanical and Structural, 4.6 ML / Data, 4.7 UX added to the template), each closing with a Handoff block: lead, deliverables at the gate, what it needs from the other domains. Each subsection is the brief that lead takes away.
- **Word export and a linked contents** — `scripts/build_docx.py` writes the run's documents as one Word file (`<slug>.docx`): cover page, a table of contents Word fills on open, then each document with its images; Phase 5 runs it after the final `review.html`. `review.html` now opens with the product name, an intro paragraph (the Solution section of the executive summary) and a table of contents with live links to every document and its sections. The markdown block parser moved to `scripts/mdblocks.py`, shared with `build_word_forms.py`.
- **Executive summary heads the bundle** — written last (Phase 4 Stage C) from the finished spec: business rationale (need, competition and alternatives, value proposition), the solution in plain words for the target audience, and one row per domain with its hardest challenges and required deliverables. New `templates/executive_summary.md`; `review.html` opens with it.

## v0.5.4 — 2026-10-25

- **Graphics are a source** — an uploaded or referenced image of any kind (sketch, block diagram, technical drawing, marketing render, prototype photo) starts Phase 0 like a document. The skill writes what the image shows into `source_spec.md`, fuses it with the text into one depiction of the product with `(from image)` marks and named conflicts, and loops present → correct → re-present until the user confirms it; only then does the gap analysis run. The confirmed image is treated the image as the given architecture or arrangement downstream. New question key `phase0.fused_depiction`.

## v0.5.3 — 2026-10-24

- **README reaches the uploader** — the release ZIP now carries `README.md` and `CHANGELOG.md`, so they show under the skill's Contents tab in claude.ai, and the Phase 1 orientation points to the README and its input-language note (English works best; Hebrew and other non-Latin input has listed rough edges).

## v0.5.2 — 2026-10-24

- `argument-hint` in SKILL.md is a YAML list, the form claude.ai normalizes to, so the release ZIP and the uploaded copy are byte-identical.

## v0.5.1 — 2026-10-24

- **Ask before proposing** — Phase 2 opens by asking whether the user already has a system architecture (none / partly / fixed), and Phase 4 by asking which critical components are already designated (MCU, key sensor, actuator, radio, battery, display). What is given is reproduced as given and marked **(given)**; the skill's own ideas become flagged alternatives, never substitutions. New question keys `phase2.known_architecture` and `phase4.critical_components`.

## v0.5.0 — 2026-10-23

- **Carousel removed** — Phases 6–8 (product visual, PPTX and PDF LinkedIn carousel) and `scripts/build_carousel.py` are gone; `reportlab` is no longer required. The workflow is five phases ending in the gate review; `review.html` is the final output. The Bubbler example keeps its carousel files as history.
- **Decisions go through dialogs** — Interaction Principle 7: any list of two or more items that need the user's decision (premises, parked questions, FAIL items, open rows at the end, design options) is walked through with `AskUserQuestion` one item at a time, never as a prose list to answer in prose.
- **Deliverables checklist** — the run ends with a tick list of every output file, its path, status and counts, and the items still floating.

## v0.4.2 — 2026-10-23

- **Hands-free runs from `decisions.md`** — an answer sheet (`Key | Answer | Note`) in the output folder, the working folder or uploaded to the chat. The skill reads it before asking: a question whose key has a row is not asked, its answer is applied and cited; `phaseN.instruction` rows are applied at the start of that phase as if typed; `mode | hands-free` skips the file gates; answers the run collects are appended at the end so the next run is fully covered. SKILL.md gains a "Question keys" table naming every question the skill asks. Written so a run completed interactively can be replayed in Claude chat without the person present.

## v0.4.1 — 2026-10-23

- **HTML output and review copy** — `scripts/build_html.py` bundles every `.md` document of a run into one `review.html` with the diagrams embedded, so the documents open in any browser on Mac or Windows with nothing installed. The skill refreshes it after every phase (reviewers without a markdown viewer read it there and edit the `.md` in TextEdit or Notepad) and lists it as a final output in Phase 8 next to the PPTX and PDF.

## v0.4.0 — 2026-10-23

- **Phase 0: Ingest and Challenge** — `/electrum <path>` (or an uploaded file in chat) starts from an existing spec, brief or PRD in txt, md, html, docx, rtf, pdf or doc. `scripts/ingest_spec.py` prints any of them as plain text (standard library; pypdf or `pdftotext` for PDF, macOS `textutil` for legacy .doc). The phase writes `gap_analysis.md` (every question the eight phases will ask, scored answered / implied / missing against the document; claims without evidence; contradictions; topics the document is silent on) and `open_questions.md` (parked items tagged with the phase that resolves them, or Floating), then puts the core premises to the user with options. Later phases skip what the document answers, ask parked questions when they reach them, and list what is still floating at the end of Phase 5 and Phase 8.
- **The user is a party to the dialog** — Interaction Principle 6: every options question carries "Ask me something first" and "Keep my choice as stated"; overruled recommendations are recorded with the user's reason and not reopened; nothing assumed is filled in silently.

## v0.3.1 — 2026-10-22

- **Skill output path** — in Claude chat and Cowork, outputs go to `electrum-output/<slug>/`; the chat sandbox has no "outputs directory". Found in the first Route 1 test run.

## v0.3.0 — 2026-10-22

- **Three routes, one skill** — `/electrum` now runs as an uploaded skill in Claude chat, in Claude Cowork, or in Claude Code. `SKILL.md` gains an Environment section: where the templates and outputs live in each place, plain-text questions where `AskUserQuestion` is not available, resume from existing phase files, and context economy for chat (edit sections instead of rewriting files, hand off Phases 6–8 to a fresh conversation). `.github/workflows/skill-zip.yml` builds `electrum-skill.zip` on each release tag; the README opens with "Choose Your Route".

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
