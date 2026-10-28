# Electrum — Product Definition Toolkit for Software-Augmented Hardware

*Status: v0.4 — exercised on 7 worked examples (see [`examples/`](examples/)), MIT-licensed.*

## The Problem

Software PMs have established tools — user stories, PRDs, sprint planning. Pure hardware PMs have theirs — datasheets, BOMs, DFM checklists. But when the product is *both* — firmware-driven hardware with sensors, actuators, maybe an app, maybe cloud — most PMs either use a software PRD template that ignores physics, or a hardware spec that ignores the software.

The boundary between HW and SW is where the expensive mistakes happen, and it's usually the least documented part.

## Choose Your Route

You have a connected product idea and want to stress-test it before committing resources. The same
`/electrum` skill runs in three places. The phases, the questions and the output files are identical;
what differs is what you install and where the files live.

| Route | For | Needs | What you give up |
|-------|-----|-------|------------------|
| **1. Skill in Claude chat** | Trying it out, no installs | A claude.ai plan with code execution on | Files are downloads; you re-upload them to resume. A full run may need two conversations |
| **2. Claude Cowork** | Real work without a terminal | A paid plan and the Claude Desktop app | Nothing in the workflow; outputs persist in a folder you pick |
| **3. Claude Code** | Teams, git, long runs, extending the scripts | Claude Code, Python 3.11, this repo | Nothing |

Routes 1 and 2 use the same ZIP, so start with 1 and move to 2 when it earns a working folder.
Route 3 picks up where either left off: copy your phase files into `output/<slug>/` in a clone and
the skill resumes from the first missing phase.

### Route 1: Skill in Claude chat

1. Download [`electrum-skill.zip`](https://github.com/yoelf22/electrum/releases/latest/download/electrum-skill.zip)
   (about 100 KB: the skill, templates, reference documents and scripts; no examples).
2. In claude.ai or the Claude Desktop app, open **Settings**, then **Customize**, then **Skills**.
   Click **Add** and choose **Upload skill**. Pick the ZIP.
3. Under **Settings**, **Capabilities**, make sure **Code execution and file creation** is on. The
   skill needs it to draw the diagrams and build the HTML page.
4. Start a new chat and type `/electrum <describe your product in one sentence>`.

Download each file as it is produced. To continue in a new conversation, upload the files you have
and run `/electrum` again; it resumes from the first missing phase.

### Route 2: Claude Cowork

1. Upload the same ZIP the same way (Cowork reads your uploaded skills).
2. Open Cowork in the Claude Desktop app, pick a working folder for the product, and type
   `/electrum <describe your product in one sentence>`.

Phase files land in `electrum-output/<slug>/` inside that folder and stay there between sessions.

### Route 3: Claude Code

```bash
# 1. Install Claude Code (https://docs.anthropic.com/en/docs/claude-code) and Python 3.11+
# 2. Clone this repo and open a terminal in it
git clone https://github.com/yoelf22/electrum.git
cd electrum
pip install -r requirements.txt

# 3. Start Claude Code and run the skill
claude
> /electrum <describe your product in one sentence>
```

On Windows, install Python from python.org with **Add python.exe to PATH** ticked, and use `python`
and `pip` where this README says `python3` and `pip3`. Git for Windows is recommended but optional:
the green **Code** button on GitHub also offers **Download ZIP**.

Whichever route you take, the process walks you through a structured dialogue: mapping the HW/SW
boundary, forcing specifics, and surfacing what you're still assuming. It pauses after every output
for your review. Budget 60–90 minutes for a full run.

**Don't want AI in the loop?** The templates work without it. Copy `templates/system_description_template.md` into your project folder, fill it in by hand, then run through `templates/checklist.md`. That's 80% of the value.

**Input language: English works best.** The templates, the 103 checklist items and the scripts are English, and the skill answers in whatever language you write in. Hebrew (or any right-to-left or non-Latin language) runs the dialog fine, but has known rough edges: a non-Latin product name gives an empty output-folder slug, so give the product an English working name; `scripts/gantt.py` looks for the English heading `### Schedule` and English column names, so keep template headings in English and translate only the content; `review.html` is laid out left to right; and text extracted from a Hebrew PDF by pypdf may come out reversed (`pdftotext` is more reliable). Part numbers, standards and protocol names should stay in Latin script so the gate review can find them.

**Want to see what a full run looks like?** Read the [Bubbler walkthrough](examples/bubbler-automated-soap-bubble-maker/WALKTHROUGH.md) — a soup-to-nuts example that turned "automated soap bubble machine" into a force-sensing feedback system with a 90-item gate review.

---

## What This Toolkit Does

A repeatable, AI-assisted process for defining hardware products that have software inside them — so the firmware team and the mechanical team aren't surprised by each other at EVT.

It takes a product idea from "I think this could work" through to a structured system description with its diagrams and a gate review, bundled into one HTML page. Five phases, driven by the `/electrum` Claude Code skill:

| Phase | Output | Description |
|-------|--------|-------------|
| 1. **Explore** | `explore_notes.md`, `team.md` | Map the HW/SW boundary, identify knowledge gaps, surface risks; propose the domain leads the product needs (mechanical, electrical, firmware, app, cloud, ML/data, UX…) for your approval |
| 2. **High-Level Design** | `high_level_design.md` | Single-page system overview: blocks, interfaces, constraints, hardest problems |
| 3. **Component Arrangement** | `component_arrangement.md`, `arrangement_options.png` | Spatial layout alternatives — where boards, batteries, sensors, and actuators sit relative to each other and the enclosure |
| 4. **System Description** | `system_description.md`, `schedule_gantt.png`, `executive_summary.md` | Full engineering-grade spec with real components, power budgets, firmware architecture; §4 has one subsection per approved lead, each a self-contained brief for that domain. Closes with the Executive Summary that heads the bundle |
| 5. **Gate Checklist** | `gate_checklist.md`, `review.html`, `<slug>.docx` | Validate completeness across both domains (103 items, PASS/FAIL/N/A), then the deliverables checklist and the Word export |

Every phase refreshes `review.html`: all the documents so far in one HTML page with the diagrams embedded, opening with the product name, an intro paragraph and a table of contents linked to every document and section, so the `.md` files can be reviewed in any browser without a markdown viewer. The run ends with `<slug>.docx`, the same documents as one Word file: cover page, table of contents, then each document (`scripts/build_docx.py`).

## The Documents: What Each One Is For

Three documents carry the product definition. Each one feeds the next:

```
High-Level Design  →  System Description  →  Gate Checklist
 (what and why)        (how, in detail)       (is it complete?)
       ↑                                             │
       └──── a FAIL sends you back to revise ←───────┘
```

| Document | What it is | Who writes it | Who reads it | When |
|----------|-----------|---------------|--------------|------|
| **Executive Summary** | One page, written last from the finished spec: the business rationale (need, competition, value proposition), the solution in plain words for the target audience, and one row per domain lead with that domain's hardest challenges and required deliverables | The product lead | Anyone who reads only the first page; each domain lead, to find their row before their §4 subsection | After the System Description is approved, before the gate review |
| **High-Level Design** | A one-to-two-page overview: what the product is, the main blocks and how they connect, the constraints that rule options out, the three hardest problems | The product manager, with one hardware lead and one software lead | Executives, partners, investors, new team members: anyone who needs to understand the product in five minutes | After the idea is explored, before anyone picks parts. Half a day to a day |
| **System Description** | The full engineering spec: real part numbers, interfaces, power budget, firmware architecture, connectivity, key decisions, and constraints (BOM cost with lead times and minimum order quantities, lead times for manufactured parts, assembly and inspection times, certification) and a Gantt schedule with the critical path | The technical lead or systems engineer, with the electrical, mechanical, firmware and app leads | Engineers design from it; suppliers and contract manufacturers quote from it | Once the High-Level Design is agreed, before schematics or tooling. Several days, then kept current through the first engineering prototype build (EVT) |
| **Gate Checklist** | 103 items, each marked PASS / FAIL / N/A, that test whether the System Description is complete enough to start detailed design. Items tagged **[HW↔SW]** target the hardware/software line | Preferably someone who did not write the System Description: a reviewer, the engineering manager, or the hardware and software leads together | The team deciding whether to commit to detailed design | When you believe the System Description is ready. Re-run after each revision until the FAILs left are ones you accept |

**The High-Level Design is also a gate.** If it doesn't hold together, the details won't either, so don't start the System Description until it does. The System Description builds on it rather than repeating it: its vision, architecture, subsystem, interface, constraint and open-question sections each expand the matching High-Level Design section.

### Word forms and the workbook

For people who'd rather fill in Word than markdown, the same three documents are available as fill-in forms on the [Electrum Word Kit](https://claude.ai/artifact/TeQUJAtvwVfo2a8iTkUymx) page, linked from [tangibles-book.com/tools/electrum](https://tangibles-book.com/tools/electrum). The grey text in each is the Bubbler worked example; it disappears when you type. `scripts/build_word_forms.py` builds them from `templates/` and the Bubbler example.

The **workbook** (`electrum-workbook.docx`) is all three forms in one file, in fill-in order. It is not a fourth step, and the other documents don't come from it: the three single files contain the same forms. Use the workbook when one person or team takes the product through all three. Use the single files when different people own each document or you share them at different times.

## Prerequisites (Route 3 only)

Routes 1 and 2 run the scripts in Claude's sandbox and need nothing installed. For Claude Code:

### Python dependencies

```bash
pip install -r requirements.txt
```

Required packages: `matplotlib`, `numpy`, `markdown`. `python-pptx`, `playwright` and `python-docx`
are only for the optional scripts below.

### Playwright browser (optional, for `scripts/generate_illustration.py`)

```bash
pip install playwright
python -m playwright install chromium
```

### Claude Code (for the `/electrum` skill)

Install [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and open a terminal in this repo. The `/electrum` skill is automatically available:

```bash
claude
> /electrum smart posture-correcting office chair
```

## Repository Structure

```
├── .claude/skills/   # The /electrum skill (one SKILL.md for all three routes)
├── .github/workflows/skill-zip.yml   # Builds electrum-skill.zip on each release tag
├── scripts/          # Python reference implementations (diagrams, HTML bundle, Word export, deck builders)
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
| `templates/hw_sw_product_initiation.md` | Workflow guide from concept to system description to PRD |
| `templates/hw_sw_high_level.md` | Single-page system overview template |
| `templates/system_description_template.md` | Full system description template with HW↔SW boundary items; §4 has one subsection per domain lead, each ending in a Handoff block |
| `templates/executive_summary.md` | One-page summary written last: business rationale, the solution in plain words, one row per domain lead with challenges and deliverables |
| `templates/checklist.md` | Gate checklist — 103 items, each tagged if it targets the HW/SW boundary |
| `templates/skills_map.md` | 16 competency areas a PM should understand or staff for |
| `.claude/skills/electrum/SKILL.md` | Claude Code skill definition (drives the 5-phase workflow) |

### Reference Scripts

| File | What it does |
|------|-------------|
| `scripts/generate_illustration.py` | DALL-E image generation via Playwright browser automation |
| `scripts/build_html.py` | Bundles a run's `.md` documents into one `review.html` with the PNGs embedded |
| `scripts/build_deck.py` | Executive product overview deck builder |
| `scripts/build_high_level_deck.py` | High-level design deck builder |
| `scripts/visualize.py` | Visualization utilities |
| `scripts/block_diagram.py` | Block diagram generator |
| `scripts/gantt.py` | Gantt chart of the §9 Schedule table, critical path highlighted |
| `scripts/ingest_spec.py` | Prints a spec document (txt, md, html, docx, rtf, pdf, doc) as plain text for Phase 0 |
| `scripts/build_word_forms.py` | Builds the Word fill-in forms from `templates/` and the Bubbler example |
| `scripts/build_docx.py` | Exports one run's documents as a single Word file with cover page and table of contents |
| `scripts/mdblocks.py` | Markdown block parser shared by the two Word builders |

### Worked Examples

| Project | What it is | Phases covered |
|---------|-----------|----------------|
| [`bubbler-automated-soap-bubble-maker/`](examples/bubbler-automated-soap-bubble-maker/) | Force-sensing automated bubble machine with adaptive optimization — **[full walkthrough](examples/bubbler-automated-soap-bubble-maker/WALKTHROUGH.md)** | All 5 phases including `team.md`, `executive_summary.md`, `decisions.md`, the §4 handoff split, `review.html` and the `.docx` export (re-run hands-free on the new flow, 2026-10-28); plus a carousel from an earlier version |
| `pop-miniature-popcorn-machine/` | Miniature countertop popcorn machine with heating and motor control | Explore, HLD, system description, gate checklist |
| `metronome/` | Wrist-worn haptic metronome bracelet for musicians — silent, precise beat pulses | All phases |
| `chair_balancing_act/` | Clip-on tilt sensor that plays an escalating tone when a chair leaves static balance | HLD, system description, gate checklist |
| `consumable-electric-toothbrush/` | Disposable electric toothbrush with wear tracking | Full |
| `shusher/` | Noise-aware mechanical mute device with sound detection | HLD, system description, gate checklist |
| `smart_sensor_hub/` | Wireless indoor environment monitor (CO2, temp, humidity, PM) with BLE mesh | HLD, system description |

The bubbler example includes a [step-by-step walkthrough](examples/bubbler-automated-soap-bubble-maker/WALKTHROUGH.md) showing what each phase surfaced and what the team would have missed without the process.

## How to Use

### With the `/electrum` skill

Pick a route from [Choose Your Route](#choose-your-route), then:

1. Type `/electrum <your product idea>`, or `/electrum <path to a spec>` if you already have a
   brief, PRD or proposal (txt, md, html, docx, rtf, pdf, doc; in chat, upload the file instead)
2. Walk through all 5 phases interactively. Claude drafts, you review and refine at each step
3. Final output: a complete product definition + diagrams, as `review.html` (any browser) and `<slug>.docx` (Word)

**The team comes first.** The product spans disciplines, so before anything is designed Phase 1
proposes the domain leads it needs: product, electrical, firmware, mechanical / industrial
design, app, cloud, ML / data, UX, security and compliance, manufacturing / NPI, each with why
and what it owns, marked required or recommended. You go through them role by role (keep,
remove, merge, change what it owns), add what is missing, then approve the final roster; nothing
is written to `team.md` until you do, even hands-free. Every later document is split along those
roles: §4 of the System Description has one subsection per lead, each ending in a Handoff block
(lead, deliverables at the gate, what it needs from the other domains), so each lead can take
their subsection away as the brief for their domain.

**The executive summary comes last.** Once the System Description is approved, the skill writes
`executive_summary.md` from it: the business rationale (the need, the competition and
alternatives, the value proposition), the solution in plain words for the target audience, and
one row per domain lead with that domain's hardest challenges and required deliverables. It heads
`review.html` and the Word file, and its Solution paragraph is the page intro.

**Starting from a document you already have.** Phase 0 reads it, scores every question the
five phases will ask as answered, implied or missing, lists the claims it makes without evidence
and the places it contradicts itself, and parks the open items in `open_questions.md` with the
phase that will resolve each. It then puts the three to five core premises to you with options.
Later phases do not re-ask what the document answers; they ask the parked questions when they
reach them, and whatever is still open at the end is listed, not dropped. At every question you
can ask Claude something first, or hold your choice against its recommendation; the decision is
recorded with your reason and not reopened.

**Running hands-free.** A `decisions.md` answer sheet in the output folder (or uploaded to the
chat) answers the questions before they are asked; `mode | hands-free` lets the run go through
every gate on its own. The skill writes one at the end of any run, so an interactive run can be
replayed, or handed to someone else, without the dialog. The keys are listed in SKILL.md under
"Question keys".

**Moving up a route.** The output files are the same everywhere. Chat downloads go into a Cowork
working folder, or into `output/<slug>/` in a Claude Code clone, and `/electrum` resumes from the
first missing phase. Nothing is redone.

### With the Word forms

Download the workbook or the three single forms from the [Electrum Word Kit](https://claude.ai/artifact/TeQUJAtvwVfo2a8iTkUymx) and fill them in order: High-Level Design, System Description, Gate Checklist. See [The Documents](#the-documents-what-each-one-is-for) for who owns each one and when.

### Without Claude Code

The core toolkit is markdown templates and checklists — no AI required:

1. **Understand the process** — Read `templates/hw_sw_product_initiation.md` for the workflow overview
2. **Assess your gaps** — Review `templates/skills_map.md` for team competency planning
3. **Create the high-level design** — Copy `templates/hw_sw_high_level.md` into your project folder and fill it in
4. **Write the system description** — Copy `templates/system_description_template.md` and work through each section
5. **Validate** — Run through `templates/checklist.md` to confirm nothing was missed

For diagrams and decks, adapt the scripts in `scripts/` to your product.

## Who This is For

Hardware product managers and technical leads building products where physical hardware and software must be designed together. The toolkit is most useful when:

- Your product has firmware, and maybe a companion app or cloud backend
- Your team spans EE/ME and software disciplines
- You need documents that both an executive and an engineer can use
- You want presentation-ready materials alongside the engineering spec
- You've been burned before by HW/SW integration surprises at EVT

---

## Part of *Tangibles*

Electrum is the open-source companion to **[Tangibles](https://tangibles-book.com)** — a book on building connected hardware your competitors can't copy. The book's companion site hosts an overview of Electrum plus a set of free, no-signup tools for connected-hardware teams:

Book: [tangibles-book.com](https://tangibles-book.com) · Available on Amazon: [https://a.co/d/00nTWJs0](https://a.co/d/00nTWJs0)

- **[Electrum overview](https://tangibles-book.com/tools/electrum)** — what this toolkit is, with worked examples
- **[IoT Security Scorecard](https://tangibles-book.com/tools/iot-security-scorecard)** — grade your device against ETSI EN 303 645 / EU CRA
- **[Security Requirements Generator](https://tangibles-book.com/tools/iot-security-requirements)** — a PRD-ready requirements list
- **[Regulatory Landscape](https://tangibles-book.com/tools/regulatory-landscape)** — which frameworks bind your product, by market and archetype

By [Yoel Frischoff](https://theroadtlv.com).
