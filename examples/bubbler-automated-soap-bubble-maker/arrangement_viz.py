#!/usr/bin/env python3
"""Bubbler arrangement — shaft on right by protrusion, trapezoid protrusion tapers to duct exit."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Arc, Polygon
import numpy as np

fig, (ax_side, ax_front) = plt.subplots(1, 2, figsize=(18, 13),
                                         gridspec_kw={"width_ratios": [1.0, 1.0]})
fig.patch.set_facecolor("#F0F0F0")

MECH = "#1a5276"; ELEC = "#c0392b"; SENSE = "#7d3c98"; POWER = "#27ae60"
FLOW = "#2e86c1"; STRUCT = "#5d6d7e"; TEXT = "#1a1a1a"; DIM = "#d35400"
ACCENT = "#d35400"; AIR = "#0e6655"; WAND_C = "#2471a3"; LOOP_C = "#1a5276"
DUCT_C = "#1a5276"; WIRE_C = "#b9770e"

S = 1 / 12  # 1 unit = 12mm

def setup(ax, title, sub, xlim, ylim):
    ax.set_facecolor("#FFFFFF"); ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("equal"); ax.axis("off")
    ax.text((xlim[0]+xlim[1])/2, ylim[1]-0.3, title, color=ACCENT, fontsize=13,
            fontweight="bold", ha="center")
    ax.text((xlim[0]+xlim[1])/2, ylim[1]-0.9, sub, color="#555555", fontsize=8,
            ha="center", style="italic")

def rbox(ax, x, y, w, h, label, sub, fill, border=None, fs=7.5, alpha=0.85):
    r = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04",
                        facecolor=fill, edgecolor=border or "#667788", linewidth=1.2, alpha=alpha)
    ax.add_patch(r)
    ax.text(x+w/2, y+h/2+0.1, label, color=TEXT, fontsize=fs,
            fontweight="bold", ha="center", va="center")
    if sub:
        ax.text(x+w/2, y+h/2-0.2, sub, color="#666666", fontsize=5,
                ha="center", va="center")

def dimline(ax, x1, y1, x2, y2, label, off=0.2, side="auto"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="<->", color=DIM, lw=0.9))
    mx, my = (x1+x2)/2, (y1+y2)/2
    if side == "left":
        ax.text(mx-off-0.1, my, label, color=DIM, fontsize=6, ha="right", va="center")
    elif side == "right":
        ax.text(mx+off+0.1, my, label, color=DIM, fontsize=6, ha="left", va="center")
    else:
        if abs(x2-x1) > abs(y2-y1):
            ax.text(mx, my+off, label, color=DIM, fontsize=6, ha="center")
        else:
            ax.text(mx+off+0.1, my, label, color=DIM, fontsize=6, ha="left", va="center")

def farrow(ax, x1, y1, x2, y2, label="", col=AIR):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.8))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my+0.25, label, color=col, fontsize=5.5, ha="center")

# ── Dimensions (mm) ──
base_thick = 10 * S
vat_depth  = 20 * S
vat_wall   = 3 * S
vat_long   = 200 * S
vat_short  = 170 * S
clearance  = 5 * S
arm_len    = 30 * S
loop_diam  = 160 * S
loop_r     = 80 * S
duct_diam  = 40 * S
duct_r     = 20 * S
duct_clearance = 10 * S  # 10mm radial clearance around duct
sol_depth  = 12 * S
foot_h     = 5 * S
motor_depth = 15 * S

# Protrusion: base width = full motor bay width, top = duct_diam + 2*clearance
prot_base_w = 60 * S   # ~60mm at base (battery + motor + clearances)
prot_top_w  = (duct_diam + 2*duct_clearance)  # 60mm at top (40mm duct + 20mm clearance)

base_short = vat_short + 2*vat_wall + prot_base_w + 10*S  # base width
base_long  = 215 * S

# ══════════════════════════════════════════
#  SIDE CROSS-SECTION: looking along LONG axis (200mm)
#  X = short axis, Y = height
#  Shaft on RIGHT, next to protrusion. Arm extends LEFT.
# ══════════════════════════════════════════
setup(ax_side, "Side Cross-Section",
      "Looking along long axis — shaft on right, tapered protrusion with duct",
      (-3, 22), (-2, 22))

base_x = 0.5; base_y = foot_h

# Rubber feet
for fx in [base_x + 0.3, base_x + base_short - 0.3]:
    ax_side.add_patch(FancyBboxPatch((fx - 0.25, 0), 0.5, foot_h,
        boxstyle="round,pad=0.02", facecolor="#888888", edgecolor="#555555", linewidth=1))

# Base plate
ax_side.add_patch(FancyBboxPatch((base_x, base_y), base_short, base_thick,
    boxstyle="square,pad=0", facecolor=STRUCT, edgecolor="#444444", linewidth=1.2, alpha=0.85))
ax_side.text(base_x + base_short/2, base_y + base_thick/2, "BASE",
             color=TEXT, fontsize=6, ha="center")

# ── VAT (left portion) ──
vat_ext = vat_short + 2*vat_wall
vat_x = base_x + 3*S
vat_y = base_y + base_thick
vat_right = vat_x + vat_ext

ax_side.fill([vat_x, vat_right, vat_right, vat_right-vat_wall,
              vat_right-vat_wall, vat_x+vat_wall, vat_x+vat_wall, vat_x],
             [vat_y, vat_y, vat_y+vat_depth, vat_y+vat_depth,
              vat_y+vat_wall, vat_y+vat_wall, vat_y+vat_depth, vat_y+vat_depth],
             color=FLOW, alpha=0.6)
ax_side.fill_between([vat_x+vat_wall, vat_right-vat_wall],
                      vat_y+vat_wall, vat_y+vat_wall+sol_depth,
                      color="#85c1e9", alpha=0.3)
ax_side.text((vat_x+vat_right)/2, vat_y+vat_depth/2, "VAT (170mm)",
             color=TEXT, fontsize=6, ha="center", fontweight="bold")

# ── SHAFT on RIGHT side, next to protrusion ──
shaft_y = vat_y + vat_depth + clearance
shaft_x = vat_right - 5*S  # shaft near right vat wall, connecting to motor in protrusion

ax_side.plot(shaft_x, shaft_y, 'o', color=ACCENT, markersize=9, zorder=6)
ax_side.text(shaft_x + 0.4, shaft_y + 0.2, "shaft", color=ACCENT,
             fontsize=5.5, fontweight="bold")

# ── WAND ARM — extends LEFT from shaft ──
# Blow position: arm goes up-left (~90° = straight up)
blow_angle = np.radians(90)  # straight up
arm_tip_x = shaft_x - arm_len * np.cos(blow_angle)  # = shaft_x (straight up, no X change)
arm_tip_y = shaft_y + arm_len * np.sin(blow_angle)   # = shaft_y + arm_len

ax_side.plot([shaft_x, arm_tip_x], [shaft_y, arm_tip_y],
             color=WAND_C, linewidth=4, solid_capstyle="round", zorder=4)

# Loop edge-on (vertical line, 160mm tall, from arm tip upward)
loop_bot = arm_tip_y
loop_top = arm_tip_y + loop_diam
loop_center_y = (loop_bot + loop_top) / 2

ax_side.plot([shaft_x, shaft_x], [loop_bot, loop_top],
             color=LOOP_C, linewidth=3, solid_capstyle="round", zorder=4)
ax_side.text(shaft_x - 0.5, loop_center_y, "loop\n(edge-on)\n160mm", color=LOOP_C,
             fontsize=5.5, ha="right", fontweight="bold")
ax_side.plot(shaft_x, loop_center_y, '+', color=LOOP_C, markersize=8,
             markeredgewidth=1.5, zorder=5)

# Dip position: arm rotates from 90° to ~265° (175° sweep)
# At 265°: arm points down-left
dip_angle = np.radians(265)
dip_arm_x = shaft_x + arm_len * np.cos(dip_angle)
dip_arm_y = shaft_y + arm_len * np.sin(dip_angle)
ax_side.plot([shaft_x, dip_arm_x], [shaft_y, dip_arm_y],
             color=WAND_C, linewidth=2, linestyle="--", alpha=0.35)

# Loop flat in vat at dip position
loop_flat_y = vat_y + vat_wall + 0.02
ax_side.plot([dip_arm_x - loop_r, dip_arm_x + loop_r*0.5],
             [loop_flat_y, loop_flat_y],
             color=LOOP_C, linewidth=2.5, linestyle="--", alpha=0.35)
ax_side.text(dip_arm_x - loop_r*0.3, loop_flat_y + 0.2,
             "loop flat (dip)", color=LOOP_C, fontsize=5, alpha=0.5, ha="center")

# Rotation arc (from 90° to 265°)
arc_r_draw = arm_len * 1.5
arc = Arc((shaft_x, shaft_y), arc_r_draw*2, arc_r_draw*2,
          angle=0, theta1=90, theta2=265, color=ACCENT, linewidth=1.3, linestyle=":")
ax_side.add_patch(arc)
ax_side.text(shaft_x - arc_r_draw*0.9, shaft_y - arc_r_draw*0.3, "175°", color=ACCENT, fontsize=5.5)

# Strain gauge
ax_side.plot(shaft_x - 0.15, shaft_y + 0.2, 's', color=SENSE, markersize=5, zorder=6)
ax_side.text(shaft_x - 0.6, shaft_y + 0.25, "strain\ngauge", color=SENSE,
             fontsize=4.5, ha="right")

# ── TAPERED PROTRUSION (right side) ──
# Trapezoid: wide at base, narrows to duct exit + clearance at top
prot_base_left = vat_right + 2*S   # left edge at base
prot_base_right = base_x + base_short - 2*S  # right edge = near base edge
prot_top_half = (duct_diam + 2*duct_clearance) / 2  # half-width at top

# Protrusion center X at top = centered on duct exit
# Duct exit must be at loop center height and aligned with loop
# Since loop is at shaft_x, duct exits from protrusion toward the loop
prot_center_x = (prot_base_left + prot_base_right) / 2
prot_top_left = prot_center_x - prot_top_half
prot_top_right = prot_center_x + prot_top_half

prot_bot_y = vat_y  # starts at base top / vat bottom level
prot_top_y = loop_center_y + duct_r + 15*S  # extends above duct center

# Draw trapezoid
trap_x = [prot_base_left, prot_base_right, prot_top_right, prot_top_left]
trap_y = [prot_bot_y, prot_bot_y, prot_top_y, prot_top_y]
trap = Polygon(list(zip(trap_x, trap_y)), closed=True,
               facecolor="#E0E0E0", edgecolor=STRUCT, linewidth=2.5, alpha=0.5)
ax_side.add_patch(trap)
ax_side.text(prot_center_x, prot_top_y + 0.3, "TAPERED PROTRUSION",
             color=STRUCT, fontsize=6, fontweight="bold", ha="center")

# ── Components inside protrusion ──

# Battery — at bottom, near base
batt_w = (prot_base_right - prot_base_left) - 2*S
batt_h = 15*S
batt_x = prot_base_left + 1*S
batt_y = prot_bot_y + 2*S
rbox(ax_side, batt_x, batt_y, batt_w, batt_h, "Battery", "4×AA", POWER, fs=6)

# PCBA — above battery
pcba_w = batt_w - 2*S
pcba_h = 10*S
pcba_x = batt_x + 1*S
pcba_y = batt_y + batt_h + 2*S
rbox(ax_side, pcba_x, pcba_y, pcba_w, pcba_h, "PCBA", "MCU, HX711", ELEC, fs=6)

# Motor — near shaft height, mounted on rim
motor_w = motor_depth
motor_h = 12*S
motor_x = prot_base_left + 1*S
motor_y = shaft_y - motor_h/2
rbox(ax_side, motor_x, motor_y, motor_w, motor_h, "Motor", "on rim", MECH, fs=5)
ax_side.plot([motor_x, shaft_x], [shaft_y, shaft_y],
             color=MECH, linewidth=1.5, linestyle=":", alpha=0.6)

# Fan — upper portion of protrusion, mounted on rim
# Width narrows here due to taper
fan_y_pos = prot_top_y - 15*S
# Calculate protrusion width at fan height (linear interpolation)
t_fan = (fan_y_pos - prot_bot_y) / (prot_top_y - prot_bot_y)
fan_left = prot_base_left + t_fan * (prot_top_left - prot_base_left)
fan_right = prot_base_right + t_fan * (prot_top_right - prot_base_right)
fan_w = (fan_right - fan_left) - 2*S
fan_x = fan_left + 1*S
rbox(ax_side, fan_x, fan_y_pos, fan_w, 10*S, "Fan", "on rim", MECH, border="#5588cc", fs=5.5)

# ── AIR DUCT — horizontal from protrusion to loop ──
duct_y_center = loop_center_y
duct_left = shaft_x + 0.3  # just past the loop edge-on position
# Calculate protrusion left edge at duct height
t_duct = (duct_y_center - prot_bot_y) / (prot_top_y - prot_bot_y)
duct_prot_left = prot_base_left + t_duct * (prot_top_left - prot_base_left)
duct_right = duct_prot_left

ax_side.fill_between([duct_left, duct_right],
                      duct_y_center - duct_r, duct_y_center + duct_r,
                      color="#d5e8f0", alpha=0.3)
ax_side.plot([duct_left, duct_right], [duct_y_center + duct_r, duct_y_center + duct_r],
             color=DUCT_C, linewidth=2)
ax_side.plot([duct_left, duct_right], [duct_y_center - duct_r, duct_y_center - duct_r],
             color=DUCT_C, linewidth=2)
ax_side.text((duct_left + duct_right)/2, duct_y_center, "DUCT\nØ40", color=DUCT_C,
             fontsize=5.5, ha="center", va="center", fontweight="bold")

# Vertical duct segment inside protrusion (from fan down to duct exit level)
ax_side.plot([prot_center_x - duct_r, prot_center_x - duct_r],
             [fan_y_pos, duct_y_center + duct_r], color=DUCT_C, linewidth=1.5, alpha=0.4)
ax_side.plot([prot_center_x + duct_r, prot_center_x + duct_r],
             [fan_y_pos, duct_y_center + duct_r], color=DUCT_C, linewidth=1.5, alpha=0.4)

# Airflow
farrow(ax_side, duct_right - 0.5, duct_y_center, duct_left + 0.2, duct_y_center, "air →")
farrow(ax_side, prot_center_x, fan_y_pos - 0.1, prot_center_x, duct_y_center + duct_r + 0.5, "↓")

# Wire runs (motor + fan to PCBA)
ax_side.plot([pcba_x + pcba_w*0.3, motor_x + motor_w*0.5],
             [pcba_y + pcba_h, motor_y], color=WIRE_C, linewidth=1, linestyle="-.", alpha=0.6)
ax_side.plot([pcba_x + pcba_w*0.6, fan_x + fan_w*0.3],
             [pcba_y + pcba_h, fan_y_pos], color=WIRE_C, linewidth=1, linestyle="-.", alpha=0.6)

# ── U-rim minimal side (left wall) ──
rim_lx = vat_x - 3*S
rim_ltop = shaft_y + 10*S
ax_side.plot([rim_lx, rim_lx], [vat_y, rim_ltop], color=STRUCT, linewidth=2.5)
ax_side.plot([rim_lx, vat_right], [rim_ltop, rim_ltop], color=STRUCT, linewidth=2.5)
ax_side.text(rim_lx - 0.15, (vat_y + rim_ltop)/2, "rim\n(min)", color=STRUCT,
             fontsize=5, ha="right", va="center")

# ── Dimensions ──
dimline(ax_side, -2, 0, -2, prot_top_y, f"~{int(prot_top_y/S)}mm", side="left")
dimline(ax_side, -2, 0, -2, loop_top, f"~{int(loop_top/S)}mm\nloop top", side="left")
dimline(ax_side, vat_x + vat_wall, -1.2, vat_right - vat_wall, -1.2, "170mm (vat)")
dimline(ax_side, base_x, -0.5, base_x + base_short, -0.5,
        f"{int(base_short/S)}mm (base)")
dimline(ax_side, 20.5, vat_y, 20.5, vat_y + vat_depth, "20mm", side="right")

# Top width annotation
dimline(ax_side, prot_top_left, prot_top_y + 0.5, prot_top_right, prot_top_y + 0.5,
        f"{int(prot_top_half*2/S)}mm (duct+clr)")

ax_side.annotate("bubbles inflate\ninto page ⊗",
                 xy=(shaft_x - loop_r, loop_top + 0.3),
                 xytext=(shaft_x - loop_r - 2, loop_top + 1),
                 color=ACCENT, fontsize=7, fontweight="bold", ha="center",
                 arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.2))

# ══════════════════════════════════════════
#  FRONT VIEW: looking along airflow / SHORT axis
#  X = long axis (215mm), Y = height
#  Shows: full loop circle, concentric duct exit
# ══════════════════════════════════════════
setup(ax_front, "Front View",
      "Looking along airflow (short axis) — duct exit concentric with loop",
      (-3, 20), (-2, 22))

fb_w = base_long; fb_x = 0.5; fb_y = foot_h

# Rubber feet
for fx in [fb_x + 0.3, fb_x + fb_w - 0.3]:
    ax_front.add_patch(FancyBboxPatch((fx - 0.25, 0), 0.5, foot_h,
        boxstyle="round,pad=0.02", facecolor="#888888", edgecolor="#555555", linewidth=1))

# Base
ax_front.add_patch(FancyBboxPatch((fb_x, fb_y), fb_w, base_thick,
    boxstyle="square,pad=0", facecolor=STRUCT, edgecolor="#444444", linewidth=1.2, alpha=0.85))
ax_front.text(fb_x + fb_w/2, fb_y + base_thick/2, "BASE (215mm)",
              color=TEXT, fontsize=6, ha="center")

# Vat (200mm long axis)
fvt = vat_long + 2*vat_wall
fvx = fb_x + (fb_w - fvt)/2
fvy = fb_y + base_thick
ax_front.fill([fvx, fvx+fvt, fvx+fvt, fvx+fvt-vat_wall, fvx+fvt-vat_wall,
               fvx+vat_wall, fvx+vat_wall, fvx],
              [fvy, fvy, fvy+vat_depth, fvy+vat_depth, fvy+vat_wall,
               fvy+vat_wall, fvy+vat_depth, fvy+vat_depth],
              color=FLOW, alpha=0.6)
ax_front.fill_between([fvx+vat_wall, fvx+fvt-vat_wall],
                       fvy+vat_wall, fvy+vat_wall+sol_depth, color="#85c1e9", alpha=0.3)
ax_front.text(fvx+fvt/2, fvy+vat_depth/2, "VAT (200mm)",
              color=TEXT, fontsize=6, ha="center", fontweight="bold")

# Shaft (horizontal, spanning vat — on the far right end near protrusion)
fs_y = fvy + vat_depth + clearance
fs_x1 = fvx + 3*S
fs_x2 = fvx + fvt - 3*S
# Shaft position along long axis — near one end (where motor is)
fs_cx = fvx + fvt - 8*S  # shaft near right end of vat

ax_front.plot([fs_x1, fs_x2], [fs_y, fs_y], color=ACCENT, linewidth=3, zorder=4)
ax_front.text((fs_x1+fs_x2)/2, fs_y + 0.25, "SHAFT (~180mm)", color=ACCENT, fontsize=6,
              ha="center", fontweight="bold")
for bx in [fs_x1, fs_x2]:
    ax_front.plot(bx, fs_y, 's', color=STRUCT, markersize=6, zorder=5)

# Arm going UP from shaft center of vat (in front view, arm is into the page —
# but loop appears as full circle centered above shaft position)
# For front view, the loop center appears above the vat center
f_arm_top = fs_y + arm_len
floop_cx = (fs_x1 + fs_x2) / 2  # loop appears centered on vat in front view
ax_front.plot([floop_cx, floop_cx], [fs_y, f_arm_top],
              color=WAND_C, linewidth=3.5, zorder=4)

f_loop_cy = f_arm_top + loop_r
f_loop = plt.Circle((floop_cx, f_loop_cy), loop_r,
                     fill=False, edgecolor=LOOP_C, linewidth=3, zorder=4)
ax_front.add_patch(f_loop)
ax_front.text(floop_cx, f_loop_cy + loop_r*0.35, "160mm Ø loop", color=LOOP_C,
              fontsize=7, ha="center", fontweight="bold")

# Duct exit concentric
f_duct = plt.Circle((floop_cx, f_loop_cy), duct_r,
                     fill=True, facecolor="#d5e8f0", edgecolor=AIR,
                     linewidth=2.5, zorder=3, alpha=0.6)
ax_front.add_patch(f_duct)
ax_front.text(floop_cx, f_loop_cy, "DUCT\nØ40", color=AIR,
              fontsize=6.5, ha="center", va="center", fontweight="bold")

# Airflow arrows
for a_deg in range(0, 360, 45):
    a = np.radians(a_deg)
    ax_front.annotate("",
        xy=(floop_cx + loop_r*0.85*np.cos(a), f_loop_cy + loop_r*0.85*np.sin(a)),
        xytext=(floop_cx + duct_r*0.6*np.cos(a), f_loop_cy + duct_r*0.6*np.sin(a)),
        arrowprops=dict(arrowstyle="-|>", color=AIR, lw=0.8, alpha=0.5))
ax_front.text(floop_cx, f_loop_cy - loop_r - 0.5, "air disperses through film",
              color=AIR, fontsize=5.5, ha="center", style="italic")

# Tapered protrusion outline (behind loop, shown dashed)
fp_top = f_loop_cy + duct_r + 15*S
fp_top_half = (duct_diam + 2*duct_clearance) / 2
fp_left_bot = fvx + 2*S
fp_right_bot = fvx + fvt - 2*S
fp_left_top = floop_cx - fp_top_half
fp_right_top = floop_cx + fp_top_half
trap_fx = [fp_left_bot, fp_right_bot, fp_right_top, fp_left_top]
trap_fy = [fvy, fvy, fp_top, fp_top]
trap_f = Polygon(list(zip(trap_fx, trap_fy)), closed=True,
                 facecolor="none", edgecolor=STRUCT, linewidth=1.5, linestyle="--", alpha=0.4)
ax_front.add_patch(trap_f)
ax_front.text(fp_right_bot + 0.5, fp_top - 1, "protrusion\n(behind)", color=STRUCT,
              fontsize=5, alpha=0.5)

# Dimensions
dimline(ax_front, fvx+vat_wall, -1, fvx+fvt-vat_wall, -1, "200mm (vat long)")
dimline(ax_front, fb_x, -0.3, fb_x + fb_w, -0.3, "215mm (base)")
dimline(ax_front, -2, 0, -2, f_loop_cy + loop_r, f"~{int((f_loop_cy+loop_r)/S)}mm", side="left")

ax_front.annotate("bubbles toward viewer ⊙",
                  xy=(floop_cx + loop_r, f_loop_cy),
                  xytext=(floop_cx + loop_r + 2, f_loop_cy + loop_r*0.3),
                  color=ACCENT, fontsize=7, fontweight="bold", ha="center",
                  arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.2))

# ── LEGEND ──
legend_items = [
    (MECH, "Mechanical"), (ELEC, "Electronic"), (SENSE, "Sensing"),
    (POWER, "Power"), (FLOW, "Vat / Fluid"), (STRUCT, "Structure"),
    (AIR, "Airflow / Duct"), (WAND_C, "Wand Arm"), (LOOP_C, "Loop"),
]
for i, (color, label) in enumerate(legend_items):
    col = i % 5; row = i // 5
    fig.text(0.06 + col*0.19, 0.025 - row*0.018, f"■ {label}",
             color=color, fontsize=7.5, fontweight="bold", va="center")

fig.suptitle("Bubbler — Component Arrangement (Side + Front Views)",
             color=ACCENT, fontsize=15, fontweight="bold", y=0.98)

plt.tight_layout(rect=[0, 0.04, 1, 0.95])
out = "/Users/yoel/Desktop/product_ideas/output/bubbler-automated-soap-bubble-maker/arrangement_options.png"
fig.savefig(out, dpi=180, facecolor=fig.get_facecolor())
plt.close()
print(f"Saved: {out}")
