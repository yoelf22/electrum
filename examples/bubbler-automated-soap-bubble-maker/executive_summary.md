# Executive Summary: Bubbler

| Field | Value |
|-------|-------|
| Date | 2026-10-28 |
| Author | Product lead (Electrum workflow, hands-free run) |
| Status | Draft |

## 1. Business Rationale

**The need:** Large soap bubbles, half a metre across, hold a crowd in a way small ones never do, and families, street performers and event organisers want them without the skill it takes to make them by hand. Doing it by hand means getting film thickness, airflow and timing right every single time; most people cannot, and the ones who can get tired.

**Competition and alternatives:** Rotating-disk consumer bubble machines ($15–40) run a fixed fan over a spinning wheel of small loops and make 20–50mm bubbles with a high pop rate and no adaptation to wind or solution; they fill the air but never impress. Hand-held giant-bubble wands and tri-string kits make big bubbles but need a practised operator and stop when the operator does. Professional stage bubble equipment exists at prices and sizes no family buys. Nothing in the consumer range makes large bubbles unattended.

**Value proposition:** For under $50, Bubbler makes large, stable bubbles on its own, at a steady pace, and keeps making them as the wind picks up and the solution ages. The whole difference is one $0.80 sensor and the firmware behind it, on a bill of materials of about $12.80 at 10k units.

## 2. The Solution

Bubbler is a battery-powered outdoor machine the size of a cake tin. You fill its open tray with bubble solution, put in four AA batteries and press one button. A 160mm loop dips into the tray, lifts upright, and a slow, gentle fan inflates the film into a bubble up to half a metre across that releases on its own; then it dips again. A force sensor on the loop's arm feels each bubble growing and the machine adjusts its own fan speed and timing from one bubble to the next, so it gets better over the first few cycles and copes with a light breeze. It runs for at least two hours on a set of batteries. V1 is standalone: no app, no Wi-Fi, no account; two buttons and four lights are the whole interface. It is a toy-grade consumer product, not stage equipment.

## 3. Domains: Challenges and Deliverables

| Domain lead | Hardest challenges | Required deliverables at the gate |
|-------------|--------------------|-----------------------------------|
| Product | Prove the adaptive loop is worth its cost against fixed settings (risk: only a 20% gain); decide toy vs. general-product classification (open question #6); keep the holiday retail window with a 30-week critical path | Approved scenarios; decision log with explicit consequences (gate gap #70); classification decision |
| Electrical / electronics | Resolve 50–200 mN on a cheap foil gauge through an HX711 with the motor running and the product outdoors; meet FCC 15B / CE EMC with a 25 kHz PWM and a 48 MHz MCU on a 2-layer board | Released schematic and layout; gauge signal-chain bench results against the 5 mN target; measured EVT power budget; EMC pre-scan plan |
| Firmware | Classify every cycle from the force curve (success, pop, no-film, partial) and converge the five-parameter hill-climb in 5–10 cycles while telling "wind changed" from "solution degraded" | Nine module skeletons; classifier validated on recorded curves; convergence shown on the bench; FW version struct in flash (gate gap #34) |
| Mechanical / industrial design | Keep the film intact through the 175° rotation (no jerk, no flex); produce 0.5–2 m/s laminar flow across a 160mm opening from a 40mm blower through an L-bent duct; seal the shaft where it crosses from the wet tray to the dry electronics | Tooling-ready CAD for base, U-rim and vat; wand, shaft, bearing and seal drawings; duct airflow measurement; gauge location and loop material decided |
| Manufacturing / NPI | Hold BOM under $15 with a 5k-unit motor MOQ and three moulds; make strain-gauge bonding and factory tare a repeatable line step; fit EVT, DVT, PVT and certification into 30 weeks | Tooling quotes; gauge bonding and calibration work instruction; DVT and PVT build plans; production test spec |
