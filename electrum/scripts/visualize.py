import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Arc
import numpy as np

_DIR = os.path.dirname(os.path.abspath(__file__))

fig, axes = plt.subplots(1, 3, figsize=(16, 6))
fig.suptitle("Chair Balancing Act", fontsize=16, fontweight="bold", y=0.98)

# --- Panel 1: Device top view ---
ax = axes[0]
ax.set_xlim(-25, 25)
ax.set_ylim(-25, 25)
ax.set_aspect("equal")
ax.set_title("Device — Top View", fontsize=11, fontweight="bold")
ax.axis("off")

# Enclosure circle
enclosure = Circle((0, 0), 16, fill=True, facecolor="#2d2d2d", edgecolor="#1a1a1a", linewidth=2)
ax.add_patch(enclosure)

# Coin cell visible through top
cell = Circle((0, 2), 12.5, fill=True, facecolor="#b0b0b0", edgecolor="#888888", linewidth=1.5)
ax.add_patch(cell)
ax.text(0, 2, "CR2450", ha="center", va="center", fontsize=8, color="#444444", fontweight="bold")

# Button
button = Circle((0, -12), 3, fill=True, facecolor="#cc3333", edgecolor="#991111", linewidth=1.5)
ax.add_patch(button)
ax.text(0, -12, "BTN", ha="center", va="center", fontsize=5.5, color="white", fontweight="bold")

# Speaker slots (edge)
for angle_deg in [120, 150, 180, 210, 240]:
    angle = np.radians(angle_deg)
    x = 16 * np.cos(angle)
    y = 16 * np.sin(angle)
    dx = 2.5 * np.cos(angle)
    dy = 2.5 * np.sin(angle)
    ax.plot([x, x + dx], [y, y + dy], color="#666666", linewidth=2.5, solid_capstyle="round")

ax.text(-22, 14, "speaker\nslots", fontsize=7, color="#666666", ha="center", style="italic")
ax.annotate("", xy=(-17, 8), xytext=(-20, 12),
            arrowprops=dict(arrowstyle="->", color="#666666", lw=1))

# Dimensions
ax.annotate("", xy=(-16, -22), xytext=(16, -22),
            arrowprops=dict(arrowstyle="<->", color="#444444", lw=1))
ax.text(0, -24, "~32 mm", ha="center", va="center", fontsize=8, color="#444444")


# --- Panel 2: Device side view (cross section) ---
ax = axes[1]
ax.set_xlim(-25, 25)
ax.set_ylim(-10, 15)
ax.set_aspect("equal")
ax.set_title("Device — Side Cross Section", fontsize=11, fontweight="bold")
ax.axis("off")

# Enclosure outline
enclosure_side = FancyBboxPatch((-16, -3), 32, 10, boxstyle="round,pad=1",
                                 facecolor="#e8e8e8", edgecolor="#1a1a1a", linewidth=2)
ax.add_patch(enclosure_side)

# PCB
pcb = patches.Rectangle((-13, 1), 26, 1, facecolor="#1b7a1b", edgecolor="#0d5a0d", linewidth=1)
ax.add_patch(pcb)
ax.text(18, 1.5, "PCB", fontsize=7, color="#0d5a0d", va="center")

# Coin cell on top of PCB
cell_side = patches.Rectangle((-10, 2), 20, 4.5, facecolor="#b0b0b0", edgecolor="#888888",
                               linewidth=1, linestyle="-")
ax.add_patch(cell_side)
ax.text(0, 4.2, "CR2450", ha="center", va="center", fontsize=7, color="#444444")

# Components on bottom of PCB
for x_pos, label, w in [(-10, "MCU", 4), (-4, "Accel", 3), (3, "Audio\nIC", 5)]:
    comp = patches.Rectangle((x_pos, -1.5), w, 1.5, facecolor="#333333", edgecolor="#111111", linewidth=0.8)
    ax.add_patch(comp)
    ax.text(x_pos + w / 2, -3.5, label, ha="center", va="center", fontsize=5.5, color="#333333")

# Speaker (piezo disc on side)
speaker = patches.Rectangle((-14, -2.5), 2, 4, facecolor="#cc8833", edgecolor="#995511", linewidth=1)
ax.add_patch(speaker)
ax.text(-18, -0.5, "Piezo", fontsize=6, color="#995511", ha="center")

# Adhesive pad at bottom
adhesive = patches.Rectangle((-12, -3.5), 24, 0.8, facecolor="#ff6666", edgecolor="#cc3333",
                              linewidth=0.8)
ax.add_patch(adhesive)
ax.text(18, -3.1, "adhesive\npad", fontsize=6, color="#cc3333", va="center")

# Height dimension
ax.annotate("", xy=(21, -3.5), xytext=(21, 7.5),
            arrowprops=dict(arrowstyle="<->", color="#444444", lw=1))
ax.text(23.5, 2, "~10\nmm", ha="center", va="center", fontsize=8, color="#444444")


# --- Panel 3: Mounted under chair ---
ax = axes[2]
ax.set_xlim(-30, 30)
ax.set_ylim(-5, 55)
ax.set_aspect("equal")
ax.set_title("Mounted Under Chair", fontsize=11, fontweight="bold")
ax.axis("off")

# Chair legs
leg_color = "#8B6914"
leg_width = 2.5
# Back legs
ax.plot([-18, -12], [0, 42], color=leg_color, linewidth=leg_width, solid_capstyle="round")
ax.plot([18, 12], [0, 42], color=leg_color, linewidth=leg_width, solid_capstyle="round")
# Front legs
ax.plot([-20, -14], [0, 28], color=leg_color, linewidth=leg_width, solid_capstyle="round")
ax.plot([20, 14], [0, 28], color=leg_color, linewidth=leg_width, solid_capstyle="round")

# Seat
seat = FancyBboxPatch((-15, 27), 30, 2.5, boxstyle="round,pad=0.5",
                       facecolor="#A0722A", edgecolor="#8B6914", linewidth=2)
ax.add_patch(seat)

# Back rest
backrest = FancyBboxPatch((-11, 32), 22, 12, boxstyle="round,pad=1",
                           facecolor="#A0722A", edgecolor="#8B6914", linewidth=2)
ax.add_patch(backrest)

# Device under seat
device = Circle((0, 26.5), 2.5, fill=True, facecolor="#2d2d2d", edgecolor="#cc3333",
                linewidth=1.5, linestyle="--")
ax.add_patch(device)

# Arrow pointing to device
ax.annotate("Chair\nBalancing\nAct", xy=(1.5, 25), xytext=(18, 18),
            fontsize=8, color="#cc3333", fontweight="bold", ha="center",
            arrowprops=dict(arrowstyle="->", color="#cc3333", lw=1.5))

# Sound waves
for r in [5, 7.5, 10]:
    wave = Arc((-3, 26.5), r, r, angle=0, theta1=160, theta2=250,
               color="#cc8833", linewidth=1, linestyle="--", alpha=0.6)
    ax.add_patch(wave)
ax.text(-15, 22, "sound", fontsize=7, color="#cc8833", style="italic", ha="center")

plt.tight_layout()
plt.savefig(os.path.join(_DIR, "chair_balancing_act_visual.png"),
            dpi=180, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved.")
