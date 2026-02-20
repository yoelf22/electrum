#!/usr/bin/env python3
"""ChillStream cross-section annotated visualization."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(20, 26))
fig.patch.set_facecolor('#0E0E1A')
ax.set_facecolor('#0E0E1A')
ax.set_xlim(-1, 21)
ax.set_ylim(-1, 33)
ax.set_aspect('equal')
ax.axis('off')

# ── Color palette ──
C_STEEL      = '#8899AA'
C_STEEL_DARK = '#556677'
C_INSULATION = '#FFD966'
C_WATER_COLD = '#4FC3F7'
C_WATER_WARM = '#FF8A65'
C_WATER_HOT  = '#FF5252'
C_PCM_FROZEN = '#00BCD4'
C_PCM_COAT   = '#00897B'
C_REFRIG     = '#E040FB'
C_COPPER     = '#D4874E'
C_PLASTIC    = '#78909C'
C_ELECTRONICS= '#66BB6A'
C_ACCENT     = '#00D4AA'
C_WHITE      = '#F0F0F5'
C_GRAY       = '#99AABB'
C_DARK_BOX   = '#1A1A2E'
C_ANNOT_BG   = '#1E2236'
C_FILTER     = '#AED581'
C_GASKET     = '#EF5350'
C_DRIP       = '#546E7A'

def draw_rect(x, y, w, h, fc, ec='none', lw=1, alpha=1, zorder=2):
    r = patches.Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec,
                           linewidth=lw, alpha=alpha, zorder=zorder)
    ax.add_patch(r)
    return r

def draw_rounded(x, y, w, h, fc, ec='none', lw=1, alpha=1, zorder=2, rad=0.3):
    r = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={rad}",
                        facecolor=fc, edgecolor=ec, linewidth=lw, alpha=alpha, zorder=zorder)
    ax.add_patch(r)
    return r

def annotate(text, xy, xytext, color=C_WHITE, fontsize=9, ha='left', arrow_color=None,
             bold=False, bg=True):
    if arrow_color is None:
        arrow_color = color
    weight = 'bold' if bold else 'normal'
    bbox_props = dict(boxstyle='round,pad=0.3', facecolor=C_ANNOT_BG, edgecolor=arrow_color,
                      linewidth=1, alpha=0.92) if bg else None
    ax.annotate(text, xy=xy, xytext=xytext,
                fontsize=fontsize, color=color, fontweight=weight, ha=ha, va='center',
                bbox=bbox_props,
                arrowprops=dict(arrowstyle='->', color=arrow_color, lw=1.3,
                                connectionstyle='arc3,rad=0.15'))

# ============================================================
# Title
# ============================================================
ax.text(10, 32.2, 'ChillStream', fontsize=28, color=C_WHITE, fontweight='bold',
        ha='center', va='center', fontfamily='sans-serif')
ax.text(10, 31.5, 'Cross-Section View \u2014 Component Layout', fontsize=14, color=C_GRAY,
        ha='center', va='center', fontfamily='sans-serif')
ax.plot([3, 17], [31.1, 31.1], color=C_ACCENT, lw=1.5, alpha=0.6)

# ============================================================
# OUTER ENCLOSURE (ABS/PC shell)
# ============================================================
enc_x, enc_y, enc_w, enc_h = 3, 2.5, 14, 25
draw_rounded(enc_x, enc_y, enc_w, enc_h, fc='none', ec=C_PLASTIC, lw=2.5, zorder=1, rad=0.8)
# Enclosure fill (very subtle)
draw_rounded(enc_x + 0.05, enc_y + 0.05, enc_w - 0.1, enc_h - 0.1,
             fc=C_PLASTIC, ec='none', alpha=0.06, zorder=0, rad=0.8)

# ============================================================
# COVER / MANIFOLD (top section)
# ============================================================
cover_y = 24
cover_h = 3.2

# Cover body
draw_rect(3.3, cover_y, 13.4, cover_h, fc='#2A3A4A', ec=C_STEEL, lw=2, zorder=5)

# Gasket line
draw_rect(3.3, cover_y - 0.15, 13.4, 0.15, fc=C_GASKET, ec='none', zorder=6)

# Cover internal channels (water routing)
# Mains water inlet channel (from right side, down into tank)
draw_rect(14, cover_y + 0.5, 2.2, 0.6, fc=C_WATER_WARM, ec=C_STEEL_DARK, lw=1, alpha=0.7, zorder=6)
draw_rect(14.5, cover_y - 0.15, 0.6, 0.65, fc=C_WATER_WARM, ec=C_STEEL_DARK, lw=1, alpha=0.7, zorder=6)

# Chilled water outlet channel (from HX up through cover to left/tap)
draw_rect(4, cover_y + 0.5, 2.5, 0.6, fc=C_WATER_COLD, ec=C_STEEL_DARK, lw=1, alpha=0.7, zorder=6)
draw_rect(5, cover_y - 0.15, 0.6, 0.65, fc=C_WATER_COLD, ec=C_STEEL_DARK, lw=1, alpha=0.7, zorder=6)

# Cold tap nozzle (extends left out of cover)
draw_rect(3, cover_y + 0.5, 0.8, 0.6, fc=C_STEEL, ec=C_STEEL_DARK, lw=1.5, zorder=7)
# Nozzle opening
draw_rect(2.5, cover_y + 0.55, 0.5, 0.5, fc=C_WATER_COLD, ec=C_STEEL_DARK, lw=1, alpha=0.8, zorder=7)

# Refrigerant lines through cover
draw_rect(9, cover_y + 1.8, 0.35, 1.4, fc=C_COPPER, ec='#8B5E3C', lw=1, zorder=6)  # liquid line
draw_rect(11, cover_y + 1.8, 0.35, 1.4, fc=C_COPPER, ec='#8B5E3C', lw=1, zorder=6)  # suction line
# Lines going down into tank
draw_rect(9, cover_y - 0.15, 0.35, 2.0, fc=C_COPPER, ec='#8B5E3C', lw=1, zorder=6)
draw_rect(11, cover_y - 0.15, 0.35, 2.0, fc=C_COPPER, ec='#8B5E3C', lw=1, zorder=6)

# Sensor wire pass-through
draw_rect(12.5, cover_y, 0.15, cover_h * 0.4, fc=C_ELECTRONICS, ec='none', alpha=0.8, zorder=6)

# Cover label
ax.text(10, cover_y + 2.5, 'COVER / MANIFOLD', fontsize=10, color=C_WHITE,
        fontweight='bold', ha='center', va='center', zorder=8,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#2A3A4A', edgecolor=C_ACCENT, lw=1))

# ============================================================
# INSULATED COLD WATER TANK
# ============================================================
tank_x, tank_y, tank_w, tank_h = 4, 10, 8.5, 13.8

# Insulation layer (PU foam)
draw_rect(tank_x - 0.6, tank_y - 0.6, tank_w + 1.2, tank_h + 1.2,
          fc=C_INSULATION, ec='none', alpha=0.25, zorder=2)
draw_rect(tank_x - 0.6, tank_y - 0.6, tank_w + 1.2, tank_h + 1.2,
          fc='none', ec=C_INSULATION, lw=1.5, alpha=0.6, zorder=3, )

# SS inner wall
draw_rect(tank_x, tank_y, tank_w, tank_h, fc='none', ec=C_STEEL, lw=2, zorder=4)

# Water fill (gradient effect - cold at bottom, warmer at top)
n_bands = 20
for i in range(n_bands):
    frac = i / n_bands
    r = int(0x4F + (0xFF - 0x4F) * frac * 0.3)
    g = int(0xC3 + (0x8A - 0xC3) * frac * 0.3)
    b = int(0xF7 + (0x65 - 0xF7) * frac * 0.3)
    band_color = f'#{r:02X}{g:02X}{b:02X}'
    band_y = tank_y + 0.1 + (tank_h - 0.2) * (1 - frac) - (tank_h - 0.2) / n_bands
    draw_rect(tank_x + 0.1, band_y, tank_w - 0.2, (tank_h - 0.2) / n_bands,
              fc=band_color, ec='none', alpha=0.3, zorder=3)

# ============================================================
# SUBMERGED PLATE HEAT EXCHANGER
# ============================================================
hx_x = tank_x + 1.5
hx_y = tank_y + 1.5
hx_w = 5.5
hx_h = 8
plate_count = 5
plate_spacing = hx_h / (plate_count + 1)

# HX outer frame
draw_rect(hx_x, hx_y, hx_w, hx_h, fc='none', ec=C_STEEL, lw=2, zorder=5)

for p in range(plate_count):
    py = hx_y + plate_spacing * (p + 0.5)
    plate_h = 0.35

    # Plate (stainless steel)
    draw_rect(hx_x + 0.2, py, hx_w - 0.4, plate_h, fc=C_STEEL_DARK, ec=C_STEEL, lw=1, zorder=6)

    # PCM coating on plate surfaces (top and bottom of each plate)
    draw_rect(hx_x + 0.3, py + plate_h, hx_w - 0.6, 0.18, fc=C_PCM_FROZEN, ec='none', alpha=0.8, zorder=6)
    draw_rect(hx_x + 0.3, py - 0.18, hx_w - 0.6, 0.18, fc=C_PCM_FROZEN, ec='none', alpha=0.8, zorder=6)

    # Channel labels (alternating)
    if p % 2 == 0:
        # Water channel
        channel_y = py + plate_h + 0.18
        channel_h = plate_spacing - plate_h - 0.36
        if channel_h > 0.1:
            draw_rect(hx_x + 0.3, channel_y, hx_w - 0.6, channel_h,
                      fc=C_WATER_COLD, ec='none', alpha=0.2, zorder=5)
            if p == 0:
                ax.text(hx_x + hx_w / 2, channel_y + channel_h / 2, 'water',
                        fontsize=7, color=C_WATER_COLD, ha='center', va='center',
                        alpha=0.8, zorder=7, style='italic')
    else:
        # Refrigerant channel
        channel_y = py + plate_h + 0.18
        channel_h = plate_spacing - plate_h - 0.36
        if channel_h > 0.1:
            draw_rect(hx_x + 0.3, channel_y, hx_w - 0.6, channel_h,
                      fc=C_REFRIG, ec='none', alpha=0.15, zorder=5)
            if p == 1:
                ax.text(hx_x + hx_w / 2, channel_y + channel_h / 2, 'refrigerant',
                        fontsize=7, color=C_REFRIG, ha='center', va='center',
                        alpha=0.8, zorder=7, style='italic')

# Refrigerant lines connecting to HX from above
draw_rect(9, hx_y + hx_h, 0.35, cover_y - (hx_y + hx_h), fc=C_COPPER, ec='#8B5E3C', lw=1, zorder=5)
draw_rect(11, hx_y + hx_h, 0.35, cover_y - (hx_y + hx_h), fc=C_COPPER, ec='#8B5E3C', lw=1, zorder=5)

# Water outlet from HX bottom going up through cover
draw_rect(5, hx_y - 0.5, 0.6, 0.5, fc=C_WATER_COLD, ec=C_STEEL_DARK, lw=1, alpha=0.7, zorder=5)
draw_rect(5, hx_y + hx_h, 0.6, cover_y - (hx_y + hx_h), fc=C_WATER_COLD, ec=C_STEEL_DARK, lw=1, alpha=0.5, zorder=5)

# ============================================================
# HOT WATER TANK (right side of enclosure)
# ============================================================
hot_x, hot_y, hot_w, hot_h = 13.5, 10, 3, 6

# Insulation
draw_rect(hot_x - 0.3, hot_y - 0.3, hot_w + 0.6, hot_h + 0.6,
          fc=C_INSULATION, ec=C_INSULATION, lw=1, alpha=0.2, zorder=2)

# Tank wall
draw_rect(hot_x, hot_y, hot_w, hot_h, fc='none', ec=C_STEEL, lw=2, zorder=4)

# Hot water fill
draw_rect(hot_x + 0.1, hot_y + 0.1, hot_w - 0.2, hot_h - 0.2,
          fc=C_WATER_HOT, ec='none', alpha=0.3, zorder=3)

# Heating element (coil at bottom)
for i in range(4):
    coil_y = hot_y + 0.5 + i * 0.6
    draw_rect(hot_x + 0.4, coil_y, hot_w - 0.8, 0.25,
              fc='#FF6D00', ec='#BF360C', lw=1, alpha=0.8, zorder=5)

ax.text(hot_x + hot_w / 2, hot_y + hot_h / 2 + 0.5, 'HOT\nTANK', fontsize=10, color=C_WATER_HOT,
        fontweight='bold', ha='center', va='center', zorder=6)
ax.text(hot_x + hot_w / 2, hot_y + hot_h / 2 - 0.8, '1.5L\n85-95°C', fontsize=8, color=C_GRAY,
        ha='center', va='center', zorder=6)

# Hot tap nozzle (extends right out of enclosure top)
draw_rect(hot_x + 1, cover_y + 1.5, 0.6, 0.6, fc=C_WATER_HOT, ec=C_STEEL_DARK, lw=1, alpha=0.7, zorder=6)
draw_rect(16.7, cover_y + 1.5, 0.8, 0.6, fc=C_STEEL, ec=C_STEEL_DARK, lw=1.5, zorder=7)
# Hot water line from tank up through cover
draw_rect(hot_x + 1, hot_y + hot_h, 0.6, cover_y - (hot_y + hot_h), fc=C_WATER_HOT, ec=C_STEEL_DARK, lw=1, alpha=0.5, zorder=5)

# ============================================================
# REFRIGERATION SYSTEM (bottom section)
# ============================================================
ref_y = 3

# Compressor
comp_x, comp_y, comp_r = 5.5, ref_y + 1.5, 1.2
circle = plt.Circle((comp_x, comp_y), comp_r, facecolor='#37474F', edgecolor=C_STEEL, lw=2, zorder=5)
ax.add_patch(circle)
inner = plt.Circle((comp_x, comp_y), 0.6, facecolor='#455A64', edgecolor=C_STEEL_DARK, lw=1, zorder=6)
ax.add_patch(inner)
ax.text(comp_x, comp_y, 'COMP', fontsize=8, color=C_WHITE, fontweight='bold',
        ha='center', va='center', zorder=7)

# Condenser (right side bottom)
cond_x, cond_y, cond_w, cond_h = 13, ref_y, 3.5, 3.5
draw_rect(cond_x, cond_y, cond_w, cond_h, fc='#37474F', ec=C_STEEL, lw=2, zorder=5)
# Condenser fins
for i in range(8):
    fy = cond_y + 0.3 + i * 0.35
    draw_rect(cond_x + 0.2, fy, cond_w - 0.4, 0.15, fc=C_STEEL, ec='none', alpha=0.5, zorder=6)
ax.text(cond_x + cond_w / 2, cond_y + cond_h / 2 + 0.5, 'CONDENSER', fontsize=8, color=C_WHITE,
        fontweight='bold', ha='center', va='center', zorder=7)
ax.text(cond_x + cond_w / 2, cond_y + cond_h / 2 - 0.3, '+ FAN', fontsize=8, color=C_GRAY,
        ha='center', va='center', zorder=7)

# Ventilation grilles (bottom of enclosure)
for i in range(6):
    gx = 13.2 + i * 0.55
    draw_rect(gx, 2.5, 0.3, 0.4, fc='#0E0E1A', ec=C_PLASTIC, lw=0.5, zorder=3)

# Capillary tube from condenser to HX
ax.plot([cond_x, cond_x - 1, 9.35], [cond_y + cond_h, ref_y + 4, hx_y],
        color=C_COPPER, lw=2, zorder=4, alpha=0.7)
ax.text(10.5, ref_y + 5, 'capillary\ntube', fontsize=7, color=C_COPPER, ha='center', va='center',
        alpha=0.7, style='italic', zorder=5)

# Suction line from HX back to compressor
ax.plot([11.35, 11.35, comp_x + comp_r], [hx_y, ref_y + 3, comp_y + 0.5],
        color=C_REFRIG, lw=2, zorder=4, alpha=0.5, linestyle='--')

# Discharge line from compressor to condenser
ax.plot([comp_x + comp_r, 8, cond_x], [comp_y, ref_y + 2.5, cond_y + 1],
        color=C_REFRIG, lw=2, zorder=4, alpha=0.5)

# ============================================================
# ELECTRONICS (behind cover / top of enclosure)
# ============================================================
pcb_x, pcb_y = 13.5, 18
draw_rect(pcb_x, pcb_y, 3, 5.5, fc='#1B5E20', ec=C_ELECTRONICS, lw=1.5, zorder=5, alpha=0.8)

# Components on PCB
# ESP32
draw_rect(pcb_x + 0.3, pcb_y + 3.5, 1.4, 0.8, fc='#333333', ec=C_ELECTRONICS, lw=1, zorder=6)
ax.text(pcb_x + 1, pcb_y + 3.9, 'ESP32-S3', fontsize=6, color=C_WHITE, ha='center', va='center', zorder=7)

# Relay/SSR
draw_rect(pcb_x + 0.3, pcb_y + 2.2, 1.0, 0.8, fc='#1A237E', ec=C_ELECTRONICS, lw=1, zorder=6)
ax.text(pcb_x + 0.8, pcb_y + 2.6, 'SSR', fontsize=6, color=C_WHITE, ha='center', va='center', zorder=7)

# Relay (compressor)
draw_rect(pcb_x + 1.5, pcb_y + 2.2, 1.0, 0.8, fc='#1A237E', ec=C_ELECTRONICS, lw=1, zorder=6)
ax.text(pcb_x + 2, pcb_y + 2.6, 'Relay', fontsize=6, color=C_WHITE, ha='center', va='center', zorder=7)

# PSU module
draw_rect(pcb_x + 0.3, pcb_y + 0.5, 2.4, 1.2, fc='#212121', ec='#616161', lw=1, zorder=6)
ax.text(pcb_x + 1.5, pcb_y + 1.1, 'AC-DC PSU', fontsize=7, color=C_WHITE, ha='center', va='center', zorder=7)

# Display (front panel - shown as side view)
draw_rect(pcb_x + 2.2, pcb_y + 3.5, 0.6, 2.0, fc='#0D47A1', ec='#1565C0', lw=1, zorder=6)
ax.text(pcb_x + 2.5, pcb_y + 4.5, 'LCD', fontsize=6, color=C_WHITE, ha='center', va='center',
        zorder=7, rotation=90)

ax.text(pcb_x + 1.5, pcb_y + 5.2, 'CONTROL\nBOARD', fontsize=8, color=C_ELECTRONICS,
        fontweight='bold', ha='center', va='center', zorder=7)

# ============================================================
# FILTER MODULE (inline, between inlet and tank)
# ============================================================
filter_x, filter_y = 14.5, 17
filter_w, filter_h = 1.5, 3.5

# Mains water line from back of enclosure to filter
draw_rect(16.5, filter_y + 1.5, 0.5, 0.4, fc=C_STEEL, ec=C_STEEL_DARK, lw=1.5, zorder=5)  # inlet fitting
ax.plot([16.5, filter_x + filter_w], [filter_y + 1.7, filter_y + 1.7],
        color=C_WATER_WARM, lw=2, zorder=4, alpha=0.7)

draw_rounded(filter_x, filter_y, filter_w, filter_h, fc=C_FILTER, ec='#558B2F',
             lw=2, alpha=0.4, zorder=5, rad=0.3)
draw_rounded(filter_x, filter_y, filter_w, filter_h, fc='none', ec='#558B2F',
             lw=2, zorder=6, rad=0.3)
ax.text(filter_x + filter_w / 2, filter_y + filter_h / 2 + 0.3, 'FILTER', fontsize=8,
        color='#33691E', fontweight='bold', ha='center', va='center', zorder=7)
ax.text(filter_x + filter_w / 2, filter_y + filter_h / 2 - 0.4, 'twist-\nlock', fontsize=7,
        color='#558B2F', ha='center', va='center', zorder=7)

# NFC tag on filter
draw_rect(filter_x + 0.3, filter_y + 0.3, 0.9, 0.5, fc='#E8F5E9', ec='#558B2F', lw=0.8, zorder=7)
ax.text(filter_x + 0.75, filter_y + 0.55, 'NFC', fontsize=6, color='#2E7D32',
        fontweight='bold', ha='center', va='center', zorder=8)

# ============================================================
# FLOW VALVE
# ============================================================
valve_x, valve_y = 13.8, 16
draw_rect(valve_x, valve_y, 1.2, 0.8, fc='#455A64', ec=C_STEEL, lw=1.5, zorder=5)
ax.text(valve_x + 0.6, valve_y + 0.4, 'VALVE', fontsize=6, color=C_WHITE,
        fontweight='bold', ha='center', va='center', zorder=7)

# Lines from filter down to valve, valve splits to cold tank and hot tank
ax.plot([filter_x + filter_w / 2, filter_x + filter_w / 2, valve_x + 0.6],
        [filter_y, valve_y + 0.8, valve_y + 0.8],
        color=C_WATER_WARM, lw=2, zorder=4, alpha=0.7)

# From valve to cold tank (cover inlet)
ax.plot([valve_x, 14.8, 14.8], [valve_y + 0.4, valve_y + 0.4, cover_y + 0.8],
        color=C_WATER_WARM, lw=2, zorder=4, alpha=0.5)

# From valve to hot tank
ax.plot([valve_x + 0.6, valve_x + 0.6, hot_x + 1.3],
        [valve_y, hot_y + hot_h, hot_y + hot_h],
        color=C_WATER_HOT, lw=2, zorder=4, alpha=0.5)

# ============================================================
# DRIP TRAY
# ============================================================
drip_y = 27.4
draw_rect(2.3, drip_y - 0.1, 3.5, 0.5, fc=C_DRIP, ec=C_STEEL_DARK, lw=1.5, zorder=8)
ax.text(4, drip_y + 0.15, 'DRIP TRAY', fontsize=7, color=C_WHITE,
        ha='center', va='center', zorder=9, fontweight='bold')

# ============================================================
# FLOW ARROWS
# ============================================================
arrow_style = dict(arrowstyle='->', color=C_WATER_COLD, lw=2, mutation_scale=15)

# Cold water flow: down through tank, through HX, up and out
ax.annotate('', xy=(7, hx_y + hx_h + 2), xytext=(7, cover_y - 0.5),
            arrowprops=dict(arrowstyle='->', color=C_WATER_WARM, lw=2.5, alpha=0.6))
ax.text(7.8, hx_y + hx_h + 1, 'mains\nwater\nin', fontsize=7, color=C_WATER_WARM,
        ha='center', va='center', alpha=0.7, style='italic')

ax.annotate('', xy=(5.3, hx_y + 0.5), xytext=(5.3, hx_y + hx_h - 0.5),
            arrowprops=dict(arrowstyle='->', color=C_WATER_COLD, lw=2.5, alpha=0.6))
ax.text(4.2, hx_y + hx_h / 2, 'water\nthrough\nHX', fontsize=7, color=C_WATER_COLD,
        ha='center', va='center', alpha=0.7, style='italic')

# ============================================================
# ANNOTATIONS (around the outside)
# ============================================================

# Cover manifold
annotate('COVER / MANIFOLD\nRoutes all fluid connections:\n\u2022 Mains water inlet\n\u2022 Chilled water outlet\n\u2022 Refrigerant lines to HX\n\u2022 Sensor wires\nLifts off for tank service',
         xy=(10, cover_y + 1.5), xytext=(-0.5, cover_y + 2), color=C_ACCENT, fontsize=8, bold=True,
         arrow_color=C_ACCENT)

# Gasket
annotate('Food-grade silicone gasket\nClamp or twist-lock seal',
         xy=(8, cover_y - 0.08), xytext=(-0.5, cover_y - 1.2), color=C_GASKET, fontsize=8,
         arrow_color=C_GASKET)

# Cold tap
annotate('COLD TAP\n4°C output',
         xy=(2.5, cover_y + 0.8), xytext=(-0.5, cover_y + 4), color=C_WATER_COLD, fontsize=9, bold=True,
         arrow_color=C_WATER_COLD)

# Hot tap
annotate('HOT TAP\n85-95°C',
         xy=(17.1, cover_y + 1.8), xytext=(18.5, cover_y + 4), color=C_WATER_HOT, fontsize=9, bold=True,
         arrow_color=C_WATER_HOT)

# Insulation
annotate('PU foam insulation',
         xy=(tank_x - 0.4, tank_y + tank_h / 2), xytext=(-0.5, tank_y + tank_h / 2 + 2),
         color=C_INSULATION, fontsize=8, arrow_color=C_INSULATION)

# Tank
annotate('INSULATED TANK\nFood-grade SS 304/316\n5L model: 15cm \u00d8 \u00d7 30cm\n10L model: 15cm \u00d8 \u00d7 50cm\nOpen top \u2014 no pressure rating',
         xy=(tank_x + tank_w, tank_y + tank_h / 2), xytext=(18, tank_y + tank_h / 2 + 3),
         color=C_STEEL, fontsize=8, bold=True, arrow_color=C_STEEL, ha='left')

# HX plates
annotate('SUBMERGED PLATE HX\nBrazed SS plates (Kaori/SWEP)\n4 plates (5L) or 8 plates (10L)\nAlternating channels:\n  \u2022 Water (to tap)\n  \u2022 Refrigerant (from compressor)',
         xy=(hx_x + hx_w, hx_y + hx_h / 2), xytext=(18, hx_y + hx_h / 2 - 2),
         color=C_STEEL, fontsize=8, bold=True, arrow_color=C_STEEL, ha='left')

# PCM coating
annotate('PCM COATING (-5 to -10°C)\nEncapsulated phase-change material\nbonded to plate surfaces\nFreezes during idle \u2192 stores cold energy\nMelts during pour \u2192 chills water',
         xy=(hx_x + 2, hx_y + 3.5), xytext=(-0.5, hx_y + 1),
         color=C_PCM_FROZEN, fontsize=8, bold=True, arrow_color=C_PCM_FROZEN)

# Refrigerant lines
annotate('Copper refrigerant lines\nLiquid + suction\nThrough cover to HX',
         xy=(9.17, cover_y - 0.5), xytext=(-0.5, 21.5), color=C_COPPER, fontsize=8,
         arrow_color=C_COPPER)

# Compressor
annotate('COMPRESSOR\n100-200W input\nR600a refrigerant\nSame class as mini-fridge',
         xy=(comp_x, comp_y), xytext=(-0.5, ref_y + 0.5), color=C_WHITE, fontsize=8, bold=True,
         arrow_color=C_STEEL)

# Condenser
annotate('CONDENSER + FAN\nFin-and-tube, air-cooled\nRear ventilation grilles',
         xy=(cond_x + cond_w / 2, cond_y + cond_h), xytext=(18, ref_y + 5.5),
         color=C_WHITE, fontsize=8, bold=True, arrow_color=C_STEEL, ha='left')

# Hot tank
annotate('HOT WATER TANK\n1.5L insulated SS\n1.5-2 kW heating element\nThermal fuse + overheat cutoff\nChild lock on dispense',
         xy=(hot_x + hot_w, hot_y + hot_h / 2), xytext=(18, hot_y + hot_h / 2),
         color=C_WATER_HOT, fontsize=8, bold=True, arrow_color=C_WATER_HOT, ha='left')

# Heating element
annotate('Heating element\n1.5 kW (office)\n2.0 kW (high-throughput)',
         xy=(hot_x + hot_w / 2, hot_y + 1.5), xytext=(18, hot_y - 1),
         color='#FF6D00', fontsize=8, arrow_color='#FF6D00', ha='left')

# Electronics / PCB
annotate('CONTROL BOARD\nESP32-S3 (WiFi built-in)\nSSR + Relay drivers\nAC-DC PSU module\n3.5" TFT LCD display\n100mm \u00d7 80mm, 2-layer FR4\nConformal coated',
         xy=(pcb_x + 1.5, pcb_y + 2.5), xytext=(18, pcb_y + 2),
         color=C_ELECTRONICS, fontsize=8, bold=True, arrow_color=C_ELECTRONICS, ha='left')

# Filter
annotate('FILTER MODULE\nTwist-lock bayonet (proprietary)\nNFC tag for lifecycle tracking\nCarbon / UV / RO options\nNo-tool replacement',
         xy=(filter_x, filter_y + filter_h / 2), xytext=(18, filter_y + filter_h / 2),
         color=C_FILTER, fontsize=8, bold=True, arrow_color='#558B2F', ha='left')

# Flow valve
annotate('Solenoid flow valve\nDiverts to cold or hot path',
         xy=(valve_x, valve_y + 0.4), xytext=(18, valve_y),
         color=C_GRAY, fontsize=8, arrow_color=C_GRAY, ha='left')

# Mains water inlet
annotate('MAINS WATER INLET\n3/8" BSP compression\n1-6 bar pressure',
         xy=(16.8, filter_y + 1.7), xytext=(18, filter_y + 4),
         color=C_WATER_WARM, fontsize=8, bold=True, arrow_color=C_WATER_WARM, ha='left')

# Drip tray
annotate('Drip tray\nRemovable, dishwasher-safe',
         xy=(3, drip_y + 0.15), xytext=(-0.5, drip_y + 1.5), color=C_DRIP, fontsize=8,
         arrow_color=C_DRIP)

# Power inlet
annotate('IEC C14 power inlet\n110-240V AC universal',
         xy=(16.5, 2.7), xytext=(18, 1.5), color=C_GRAY, fontsize=8, bold=True,
         arrow_color=C_GRAY, ha='left')

# Enclosure label
annotate('ENCLOSURE\nABS/PC outer shell\n~30cm W \u00d7 40cm D \u00d7 45cm H\nSS dispense area',
         xy=(3, enc_y + enc_h / 2), xytext=(-0.5, enc_y + enc_h / 2 - 3),
         color=C_PLASTIC, fontsize=8, bold=True, arrow_color=C_PLASTIC)

# ============================================================
# LEGEND
# ============================================================
legend_x, legend_y = 0.5, -0.5
legend_items = [
    (C_WATER_COLD, 'Cold water path'),
    (C_WATER_WARM, 'Mains / warm water'),
    (C_WATER_HOT, 'Hot water'),
    (C_REFRIG, 'Refrigerant'),
    (C_COPPER, 'Copper lines'),
    (C_PCM_FROZEN, 'PCM coating (frozen)'),
    (C_INSULATION, 'PU insulation'),
    (C_STEEL, 'Stainless steel'),
    (C_ELECTRONICS, 'Electronics'),
    (C_FILTER, 'Filter module'),
    (C_GASKET, 'Gasket / seal'),
]

for i, (color, label) in enumerate(legend_items):
    lx = legend_x + (i % 6) * 3.4
    ly = legend_y - (i // 6) * 0.5
    draw_rect(lx, ly, 0.4, 0.3, fc=color, ec='none', alpha=0.8, zorder=10)
    ax.text(lx + 0.55, ly + 0.15, label, fontsize=8, color=C_GRAY, va='center', zorder=10)

# ============================================================
# Save
# ============================================================
plt.tight_layout()
output_path = '/Users/yoel/Desktop/product_ideas/chillstream/ChillStream_Cross_Section.png'
fig.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor(),
            pad_inches=0.5)
print(f'Saved to {output_path}')
plt.close()
