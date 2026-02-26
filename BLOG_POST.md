# Electrum — Open-Source Toolkit for Exploring Hardware Products with Software Inside

*A Claude Code skill that asks the questions you forgot to ask*

You have a product idea. It has a microcontroller, a couple of sensors, maybe an app. You can picture it working. You can almost feel the enclosure in your hand.

But can you describe the firmware update mechanism? The power budget under peak load? What happens when the BLE connection drops mid-transfer? Which side of the HW/SW boundary owns the calibration logic?

These questions don't come up when you're excited about an idea. They come up six months later, at EVT, when it's expensive.

## The Gap Between Two Toolkits

Software PMs have their tools — user stories, PRDs, sprint planning. Hardware PMs have theirs — datasheets, BOMs, DFM checklists. But products that are both — firmware-driven hardware with sensors, actuators, a companion app, maybe a cloud backend — fall between the two. Most teams reach for one template or the other and cover the rest in meetings and Slack threads.

The HW/SW boundary, the part where the most expensive integration surprises live, ends up as implicit knowledge in someone's head. It stays there until it becomes a problem.

## Eight Phases of Asking "What About...?"

Electrum is a structured way to interrogate a product idea before you commit to it. It's built as a Claude Code skill — type `/electrum <your idea>` and it starts a dialogue that walks through eight phases.

The key word is *dialogue*. This isn't a form to fill out. Each phase is a back-and-forth: the system drafts, you push back, it revises, you push back again. It's Socratic in character — the value isn't in the answers it generates, it's in the questions the process forces you to confront.

**Phase 1: Explore.** Where does the hardware end and the software begin? Which of 16 competency areas does this product touch — analog signal conditioning? RF design? Cloud infrastructure? Regulatory compliance? What don't you know yet? For electromechanical products, the process also asks about physical architecture: what moves, what bears load, what media flows through the system. The output is an exploration document that maps the terrain before you start designing.

**Phase 2: High-Level Design.** One page. Block diagram (generated as a matplotlib visualization, not ASCII art), subsystem boundaries, interface protocols, constraints. And the three hardest unsolved problems. This is where the idea starts meeting physics. "Runs on a coin cell" collides with "streams data over BLE at 100 Hz." Good — you want those collisions now, not later.

**Phase 3: Component Arrangement.** Every physical element inventoried and placed in space. Cross-section and plan-view diagrams showing how the PCB, battery, motors, sensors, and enclosure actually fit together. This is where "it should be compact" meets real millimeters. The process generates 2–3 arrangement alternatives as side-by-side panels for comparison.

**Phase 4: System Description.** Now push harder. Name specific components — not "an MCU" but "nRF52840." Not "a battery" but "3.7V 500mAh LiPo with 15-hour target runtime." Power budgets with real numbers. Interface specs with actual protocols. Firmware architecture with module breakdowns. The point isn't to write the final engineering spec. The point is to see where the idea breaks when you apply specifics.

**Phase 5: Gate Checklist.** 90 items. PASS, FAIL, or N/A. Many specifically target the HW/SW boundary: "Is the watchdog timer behavior defined for each failure mode?" "Are sensor sampling rates compatible with the processing pipeline?" "Is there a defined strategy for field firmware updates?" Every FAIL is a conversation you haven't had yet. The checklist doesn't tell you the product is ready. It tells you what you're still assuming.

If the FAIL count is high, the process sends you back to Phase 4 to revise. This loop — describe, validate, revise — is where most of the discovery happens.

**Phases 6–8** shift from thinking to communicating. Product visuals (using the diagrams generated in earlier phases), an 8-page slide deck, a PDF carousel. Useful for sharing the idea with others, but the real work is in Phases 1–5.

## What This Looks Like in Practice

To make this concrete: we ran Electrum on an automated soap bubble machine. The starting concept was simple — dip a wand, blow air, make large bubbles. Sub-$50, battery-powered, outdoor use.

The exploration phase classified it as electromechanical and immediately surfaced the central question: how does the firmware know what's happening to the soap film? Four sensing approaches were compared. IR break-beam (the obvious choice) failed on every practical dimension — it needs components spanning the 160mm loop opening and only gives binary "present/absent." A $0.80 strain gauge on the wand arm pivot turned out to give a continuous real-time inflation curve: slope tells you growth rate, peak tells you size, sudden drop tells you whether the bubble popped or detached cleanly.

The high-level design identified three hard problems: film survival during a 175-degree wand rotation, real-time force-curve interpretation, and outdoor wind compensation. These three problems shaped every downstream decision.

The gate checklist found the expected gaps: no watchdog behavior defined for mid-optimization crashes, no factory calibration procedure for the strain gauge (zero-offset varies per unit), no soap solution viscosity spec. Each one is a conversation the team hadn't had yet.

The structured process turned "simple bubble machine" into "force-sensing feedback system that happens to make bubbles." That reframing changes how you staff the project, what you prototype first, and how you pitch it.

The [full walkthrough](https://github.com/yoelf22/electrum/blob/master/examples/bubbler-automated-soap-bubble-maker/WALKTHROUGH.md) shows every phase with outputs.

## The Conversation Is the Product

What makes this different from a document generator is the rhythm. Each phase pauses. You read what was produced. You disagree with a component choice, or notice the power budget doesn't add up, or realize the firmware architecture assumes a feature the hardware can't support. You say so. The document gets revised. You move on.

The gate checklist is particularly good at provoking this. You'll read "FAIL: No defined behavior for loss of sensor calibration during power brownout" and think — right, we never talked about that. That one item might reshape the firmware architecture. Or it might be irrelevant for this product. Either way, you're making the decision consciously instead of discovering the gap in testing.

The process works because it's progressive. The exploration gives you vocabulary. The high-level design gives you structure. The component arrangement gives you spatial reality. The system description gives you specifics. The checklist gives you accountability. Each phase builds on the one before, and each one surfaces a different class of questions.

## Try It With a Bad Idea

Seriously. Pick a product concept you're not sure about — the weirder the better. An automated soap bubble machine with force feedback. A wrist-worn haptic metronome for drummers. A miniature countertop popcorn maker with temperature control.

Run it through the eight phases. The exploration will tell you which technical domains you'd need to staff. The high-level design will show you where the system complexity actually lives. The system description will force you to pick real parts and do real math. The gate checklist will tell you what you're still hand-waving about.

You'll know within 90 minutes whether the idea has legs — not because the tool told you, but because the process forced you to think it through.

## What's in the Repo

- **Templates** — the high-level design template, system description template, 90-item gate checklist, 16-area skills map, and the 8-phase workflow description
- **Reference scripts** — Python code for building PPTX carousels, block diagrams, and arrangement visualizations
- **Seven worked examples** — from a [force-sensing bubble machine](https://github.com/yoelf22/electrum/blob/master/examples/bubbler-automated-soap-bubble-maker/WALKTHROUGH.md) to a haptic metronome bracelet, at varying levels of completeness

The templates work without AI. Copy them, fill them in by hand, run the checklist yourself. The Claude Code skill just makes the conversation faster.

It's a research and exploration tool, not a production methodology. Take the parts that provoke useful thinking, skip the rest.

[github.com/yoelf22/electrum](https://github.com/yoelf22/electrum)
