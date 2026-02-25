#!/usr/bin/env python3
"""Block diagram for Bubbler — automated large-bubble machine with force-sensing optimization."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(14, 9))
fig.patch.set_facecolor("#1a1a2e")
ax.set_facecolor("#1a1a2e")
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis("off")

# Colors
CARD = "#22223a"
MECH_FILL = "#3a5ba0"      # mechanical — blue
ELEC_FILL = "#a05c3a"      # electronic — orange
SENSE_FILL = "#6b3a8a"     # sensing — purple
POWER_FILL = "#3a7a4a"     # power — green
UI_FILL = "#7a7a3a"        # user interface — olive
FLOW_FILL = "#2a6a7a"      # airflow/fluid — teal
TEXT = "#e8e8e8"
ACCENT = "#ff9f43"
SIGNAL_COLOR = "#ffdd57"    # signal/data arrows
POWER_COLOR = "#55efc4"     # power arrows
FORCE_COLOR = "#74b9ff"     # force/flow arrows
AIR_COLOR = "#81ecec"       # airflow arrows

def block(x, y, w, h, label, sublabel, fill, border=None):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                          facecolor=fill, edgecolor=border or "#555577", linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2 + 0.12, label, color=TEXT, fontsize=9,
            fontweight="bold", ha="center", va="center")
    ax.text(x + w/2, y + h/2 - 0.18, sublabel, color="#aaaacc", fontsize=6.5,
            ha="center", va="center", style="italic")

def arrow(x1, y1, x2, y2, color, label="", style="-|>", lw=1.5, curve=0):
    if curve:
        arrow_patch = FancyArrowPatch((x1, y1), (x2, y2),
            arrowstyle=style, color=color, lw=lw,
            connectionstyle=f"arc3,rad={curve}", mutation_scale=12)
    else:
        arrow_patch = FancyArrowPatch((x1, y1), (x2, y2),
            arrowstyle=style, color=color, lw=lw, mutation_scale=12)
    ax.add_patch(arrow_patch)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my + 0.18, label, color=color, fontsize=6, ha="center", va="bottom")

# ── Title ──
ax.text(7, 8.6, "Bubbler — System Block Diagram", color=ACCENT, fontsize=16,
        fontweight="bold", ha="center", va="center")
ax.text(7, 8.25, "Large-bubble machine with force-sensing auto-optimization",
        color="#aaaacc", fontsize=9, ha="center", va="center")

# ── Domain separator ──
ax.plot([0.3, 13.7], [4.3, 4.3], color="#444466", linewidth=1, linestyle="--")
ax.text(0.6, 4.45, "ELECTRONIC DOMAIN", color="#666688", fontsize=7, fontweight="bold")
ax.text(0.6, 4.1, "MECHANICAL DOMAIN", color="#666688", fontsize=7, fontweight="bold")

# ═══════════════════════════════════════════════
#  MECHANICAL DOMAIN (bottom half)
# ═══════════════════════════════════════════════

# Open vat
block(0.5, 0.5, 2.5, 1.2, "Open Vat", "soap solution reservoir", FLOW_FILL)

# Wand arm + loop
block(4.0, 0.5, 3.0, 1.2, "Wand Arm + Loop", "160mm loop, dip-rotate pivot", MECH_FILL)

# Fan / blower
block(8.2, 0.5, 2.8, 1.2, "Blower Fan", "60-80mm, gentle laminar flow", MECH_FILL)

# Bubble (output)
block(11.5, 0.5, 2.0, 1.2, "Bubble", "≤500mm, detach & float", "#3a3a5a", border=ACCENT)

# Pivot servo/motor
block(4.0, 2.3, 2.2, 1.0, "Pivot Motor", "geared DC / servo", MECH_FILL)

# Strain gauge
block(7.0, 2.3, 2.5, 1.0, "Strain Gauge", "on wand arm pivot", SENSE_FILL)

# Arrows in mechanical domain
# Vat → Wand (dip)
arrow(3.0, 1.1, 4.0, 1.1, FORCE_COLOR, "dip into\nsolution")

# Wand → Bubble (film presented)
arrow(7.0, 1.1, 8.2, 1.1, AIR_COLOR, "soap film")

# Fan → Bubble (airflow)
arrow(11.0, 1.1, 11.5, 1.1, AIR_COLOR, "inflate")

# Fan airflow → wand loop area
arrow(8.2, 1.5, 7.0, 1.5, AIR_COLOR, "airflow", curve=-0.15)

# Pivot motor → Wand arm (rotation)
arrow(5.1, 2.3, 5.5, 1.7, FORCE_COLOR, "rotate")

# Strain gauge ← Wand arm (force)
arrow(7.0, 1.7, 7.8, 2.3, SIGNAL_COLOR, "force signal")

# ═══════════════════════════════════════════════
#  ELECTRONIC DOMAIN (top half)
# ═══════════════════════════════════════════════

# MCU + Firmware (center)
block(4.5, 5.5, 3.5, 1.5, "MCU + Firmware", "control loop, optimization, state machine", ELEC_FILL, border=ACCENT)

# HX711 ADC (strain gauge interface)
block(9.0, 5.5, 2.5, 1.0, "HX711 ADC", "strain gauge amplifier", SENSE_FILL)

# Fan motor driver
block(9.0, 7.0, 2.5, 1.0, "Fan Motor Driver", "MOSFET + PWM", ELEC_FILL)

# Servo / H-bridge driver
block(1.0, 5.5, 2.5, 1.0, "Pivot Driver", "H-bridge / servo PWM", ELEC_FILL)

# Power system
block(1.0, 7.2, 2.5, 1.0, "Battery + Regulator", "4×AA or LiPo, 3.3V reg", POWER_FILL)

# User interface
block(4.5, 7.5, 3.0, 0.9, "User Controls", "power btn, mode dial, LEDs", UI_FILL)

# ── Electronic arrows ──

# MCU ↔ HX711
arrow(8.0, 6.0, 9.0, 6.0, SIGNAL_COLOR, "SPI/DOUT+SCK")

# MCU → Fan driver
arrow(8.0, 6.8, 9.0, 7.3, SIGNAL_COLOR, "PWM")

# MCU → Pivot driver
arrow(4.5, 6.0, 3.5, 6.0, SIGNAL_COLOR, "PWM / DIR")

# MCU ↔ UI
arrow(6.0, 7.0, 6.0, 7.5, SIGNAL_COLOR, "GPIO")

# Power → MCU
arrow(3.5, 7.5, 4.5, 7.0, POWER_COLOR, "3.3V")

# Power → Fan driver
arrow(3.5, 7.7, 9.0, 7.5, POWER_COLOR, "V_bat", curve=-0.1)

# Power → Pivot driver
arrow(2.25, 7.2, 2.25, 6.5, POWER_COLOR, "V_bat")

# ── Cross-domain arrows (electronic ↔ mechanical) ──

# Pivot driver → Pivot motor
arrow(2.25, 5.5, 4.5, 3.3, POWER_COLOR, "motor power", curve=0.2)

# Fan driver → Fan
arrow(10.25, 7.0, 9.6, 1.7, POWER_COLOR, "motor power", curve=-0.3)

# Strain gauge → HX711
arrow(8.5, 3.3, 10.0, 5.5, SIGNAL_COLOR, "analog mV", curve=-0.15)

# ── Legend ──
legend_y = 0.15
legend_items = [
    (SIGNAL_COLOR, "Signal / Data"),
    (POWER_COLOR, "Power"),
    (FORCE_COLOR, "Mechanical Force"),
    (AIR_COLOR, "Airflow / Fluid"),
]
for i, (color, label) in enumerate(legend_items):
    x = 1.5 + i * 3.2
    ax.plot([x - 0.3, x + 0.3], [legend_y, legend_y], color=color, lw=2)
    ax.text(x + 0.5, legend_y, label, color=color, fontsize=7, va="center")

plt.tight_layout(pad=0.5)
out = "/Users/yoel/Desktop/product_ideas/output/bubbler-automated-soap-bubble-maker/block_diagram.png"
fig.savefig(out, dpi=180, facecolor=fig.get_facecolor())
plt.close()
print(f"Saved: {out}")
