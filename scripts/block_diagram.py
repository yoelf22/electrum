#!/usr/bin/env python3
"""Generate AirSense block diagram — three-tier architecture illustration."""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

_DIR = os.path.dirname(os.path.abspath(__file__))

fig, ax = plt.subplots(figsize=(16, 9))
fig.set_facecolor("#0F172A")
ax.set_facecolor("#0F172A")
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis("off")

# -- Colors --
TEAL = "#00BFA5"
BLUE = "#009BF5"
PURPLE = "#9B6DFF"
ORANGE = "#FF8C00"
RED = "#FF4545"
CARD = "#18223A"
CARD_BORDER = "#2A3656"
WHITE = "#FFFFFF"
GRAY = "#8899AA"
SOFT = "#C8D0E0"


def block(x, y, w, h, label, sublabel=None, color=TEAL, fontsize=10, sublabel_size=7.5):
    """Draw a rounded block with label."""
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.12",
                          facecolor=CARD, edgecolor=color, linewidth=1.8)
    ax.add_patch(rect)
    # Color strip on top
    strip = FancyBboxPatch((x + 0.05, y + h - 0.22), w - 0.1, 0.18,
                           boxstyle="round,pad=0.04",
                           facecolor=color, edgecolor="none", alpha=0.9)
    ax.add_patch(strip)
    ax.text(x + w / 2, y + h - 0.13, label,
            ha="center", va="center", fontsize=fontsize, fontweight="bold",
            color=WHITE, family="sans-serif")
    if sublabel:
        ax.text(x + w / 2, y + h / 2 - 0.1, sublabel,
                ha="center", va="center", fontsize=sublabel_size,
                color=SOFT, family="sans-serif", linespacing=1.5)


def group_box(x, y, w, h, label, color=TEAL):
    """Draw a dashed group outline with label."""
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.2",
                          facecolor="none", edgecolor=color,
                          linewidth=1.5, linestyle="--", alpha=0.5)
    ax.add_patch(rect)
    ax.text(x + 0.25, y + h - 0.2, label,
            fontsize=11, fontweight="bold", color=color,
            family="sans-serif", alpha=0.8)


def arrow(x1, y1, x2, y2, label=None, color=GRAY, style="-|>", lw=1.5, label_offset=(0, 0.15)):
    """Draw an arrow with optional label."""
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                connectionstyle="arc3,rad=0"))
    if label:
        mx = (x1 + x2) / 2 + label_offset[0]
        my = (y1 + y2) / 2 + label_offset[1]
        ax.text(mx, my, label, ha="center", va="center",
                fontsize=7, color=color, family="sans-serif",
                fontstyle="italic",
                bbox=dict(boxstyle="round,pad=0.15", facecolor="#0F172A",
                          edgecolor="none", alpha=0.85))


def curved_arrow(x1, y1, x2, y2, label=None, color=GRAY, rad=0.3, label_offset=(0, 0)):
    """Draw a curved arrow."""
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5,
                                connectionstyle=f"arc3,rad={rad}"))
    if label:
        mx = (x1 + x2) / 2 + label_offset[0]
        my = (y1 + y2) / 2 + label_offset[1]
        ax.text(mx, my, label, ha="center", va="center",
                fontsize=7, color=color, family="sans-serif",
                fontstyle="italic",
                bbox=dict(boxstyle="round,pad=0.15", facecolor="#0F172A",
                          edgecolor="none", alpha=0.85))


# ================================================================
# TIER 1: Sensor Node (left)
# ================================================================
group_box(0.3, 0.5, 5.4, 8.0, "SENSOR NODE  (per room)", TEAL)

# Sensors
block(0.7, 6.6, 2.2, 1.4, "SCD41", "CO2 + Temp + RH\nI2C  |  +/-40 ppm", TEAL, 9, 7)
block(3.1, 6.6, 2.2, 1.4, "SHT40", "Temp + Humidity\nI2C  |  +/-0.2C", TEAL, 9, 7)
block(0.7, 4.8, 2.2, 1.4, "PMSA003I", "PM1.0 / PM2.5 / PM10\nI2C  |  25 mA active", ORANGE, 9, 7)

# MCU
block(0.7, 2.4, 4.6, 1.8, "nRF52840 + Firmware",
      "Zephyr RTOS  |  BLE 5.3\nSensor mgr, power mgr, OTA\nDeep sleep 99% of the time",
      BLUE, 10, 7.5)

# Power
block(3.1, 4.8, 2.2, 1.4, "Power", "2x AA Lithium\nTPS62740 reg\n6V -> 3.3V", ORANGE, 9, 7)

# LED + Button
block(0.7, 0.9, 2.2, 1.0, "RGB LED", "Status indicator", GRAY, 9, 7)
block(3.1, 0.9, 2.2, 1.0, "Button", "Reset / pairing", GRAY, 9, 7)

# Sensor node internal arrows
arrow(1.8, 6.6, 2.2, 4.2, "I2C", TEAL, label_offset=(-0.7, 0))
arrow(4.2, 6.6, 3.6, 4.2, "I2C", TEAL, label_offset=(0.7, 0))
arrow(1.8, 4.8, 2.4, 4.2, "I2C", ORANGE, label_offset=(-0.7, 0))
arrow(4.2, 4.8, 3.6, 4.2, "3.3V", ORANGE, label_offset=(0.7, 0))
arrow(1.8, 2.4, 1.8, 1.9, "GPIO", GRAY, label_offset=(0.45, 0))
arrow(4.2, 2.4, 4.2, 1.9, "GPIO", GRAY, label_offset=(0.45, 0))

# ================================================================
# TIER 2: Gateway (center)
# ================================================================
group_box(6.2, 2.5, 3.6, 4.5, "GATEWAY  (per floor)", BLUE)

block(6.6, 4.8, 2.8, 1.7, "ESP32-S3",
      "BLE scanner\nEthernet uplink\nMQTT client\nMains-powered", BLUE, 10, 7.5)

block(6.6, 3.0, 2.8, 1.2, "Ethernet PHY",
      "RJ45 to LAN\n100 Mbps", BLUE, 9, 7)

arrow(7.9, 4.8, 7.9, 4.2, "", BLUE)

# Sensor → Gateway: BLE
arrow(5.3, 3.3, 6.6, 5.3, "BLE 5.3\nadvertising", TEAL,
      label_offset=(0.0, 0.5))

# ================================================================
# TIER 3: Cloud (right)
# ================================================================
group_box(10.3, 0.5, 5.4, 8.0, "CLOUD BACKEND", PURPLE)

block(10.7, 6.6, 2.2, 1.4, "MQTT Broker",
      "AWS IoT Core\nTLS 1.2", PURPLE, 9, 7)
block(13.1, 6.6, 2.2, 1.4, "TimescaleDB",
      "Time-series storage\n90-day full, 2-yr agg", PURPLE, 9, 7)

block(10.7, 4.6, 2.2, 1.4, "REST API",
      "Device data\nFleet management\nJWT auth", PURPLE, 9, 7)
block(13.1, 4.6, 2.2, 1.4, "Alert Engine",
      "CO2 > 1000 ppm\nDevice offline\nLow battery", RED, 9, 7)

block(10.7, 2.4, 2.2, 1.4, "Web Dashboard",
      "Floor map\nColor-coded rooms\nHistorical trends", BLUE, 9, 7)
block(13.1, 2.4, 2.2, 1.4, "Mobile QR Page",
      "Single-room view\nNo auth required\nOccupant-facing", BLUE, 9, 7)

block(10.7, 0.8, 4.6, 1.0, "OTA Firmware Deployment",
      "Fleet segmentation  |  MCUboot images  |  Rollback", ORANGE, 9, 7)

# Cloud internal arrows
arrow(11.8, 6.6, 11.8, 6.0, "", PURPLE)
arrow(12.9, 7.3, 13.1, 7.3, "", PURPLE)
arrow(14.2, 6.6, 14.2, 6.0, "", RED)
arrow(11.8, 4.6, 11.8, 3.8, "HTTPS", BLUE, label_offset=(0.5, 0))
arrow(14.2, 4.6, 14.2, 3.8, "", BLUE)

# Gateway → Cloud: MQTT
arrow(9.4, 4.2, 10.7, 7.0, "MQTT / TLS\nEthernet", BLUE,
      label_offset=(0.0, 0.45))

# OTA path (cloud → gateway → node)
curved_arrow(11.8, 0.8, 8.0, 3.0, "OTA images\nvia gateway", ORANGE,
             rad=-0.3, label_offset=(0, -0.4))

# ================================================================
# Title and legend
# ================================================================
ax.text(8, 8.7, "AirSense  --  System Architecture",
        ha="center", va="center", fontsize=18, fontweight="bold",
        color=WHITE, family="sans-serif")

# Legend
legend_items = [
    (TEAL, "Sensor / sensing"),
    (BLUE, "Connectivity / UI"),
    (PURPLE, "Cloud / storage"),
    (ORANGE, "Power / OTA"),
    (RED, "Alerting"),
    (GRAY, "Physical UI"),
]
for i, (color, label) in enumerate(legend_items):
    lx = 6.4 + i * 1.7
    ly = 0.15
    rect = FancyBboxPatch((lx, ly), 0.2, 0.15,
                           boxstyle="round,pad=0.02",
                           facecolor=color, edgecolor="none")
    ax.add_patch(rect)
    ax.text(lx + 0.3, ly + 0.07, label,
            fontsize=7, color=GRAY, va="center", family="sans-serif")

# ================================================================
# Save
# ================================================================
out = os.path.join(_DIR, "AirSense_Block_Diagram.png")
fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"Saved to {out}")
