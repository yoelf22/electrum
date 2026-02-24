"""Side-by-side cross-section visualization of two motor arrangement options."""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Arc
import numpy as np

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 20))
fig.patch.set_facecolor('#1a1a2e')

SHELL_COLOR = '#b0b0b0'
TPE_COLOR = '#5ca08e'
PP_COLOR = '#d4c896'
MOTOR_COLOR = '#c0392b'
BATTERY_COLOR = '#2980b9'
BRISTLE_COLOR = '#ecf0f1'
SWITCH_COLOR = '#e67e22'
ORING_COLOR = '#222222'
LINKAGE_COLOR = '#e74c3c'
BG = '#22223a'

def draw_option_a(ax):
    ax.set_facecolor(BG)
    ax.set_xlim(-12, 12)
    ax.set_ylim(-5, 105)
    ax.set_aspect('equal')
    ax.set_title('Option A — Axial Motor', color='white', fontsize=16, fontweight='bold', pad=15)
    ax.axis('off')

    # --- Battery cap + O-ring (bottom) ---
    cap = FancyBboxPatch((-6, 0), 12, 3, boxstyle="round,pad=0.3", fc='#888888', ec='#555555', lw=1.5)
    ax.add_patch(cap)
    ax.text(0, 1.5, 'Battery Cap\n(threaded PP)', ha='center', va='center', fontsize=6, color='white', fontweight='bold')
    # O-ring
    ax.add_patch(patches.Ellipse((0, 3.2), 10, 1.2, fc=ORING_COLOR, ec='#444', lw=1))
    ax.text(12, 3.2, '← O-ring', ha='left', va='center', fontsize=7, color=ORING_COLOR, fontstyle='italic')

    # --- Shell outline (main body) ---
    # Outer shell - TPE overmold
    shell = FancyBboxPatch((-7.5, 3.5), 15, 82, boxstyle="round,pad=0.8", fc=TPE_COLOR, ec='#3d7a6a', lw=2, alpha=0.35)
    ax.add_patch(shell)
    # Inner rigid PP body
    body = FancyBboxPatch((-6.5, 4), 13, 81, boxstyle="round,pad=0.5", fc=PP_COLOR, ec='#a8a060', lw=1.5, alpha=0.3)
    ax.add_patch(body)

    # --- Spring contact (negative) ---
    ax.add_patch(patches.FancyBboxPatch((-3, 4.5), 6, 1.5, boxstyle="round,pad=0.2", fc='#aaa', ec='#666', lw=1))
    ax.text(0, 5.2, '− spring', ha='center', va='center', fontsize=5.5, color='#333')

    # --- AAA Battery ---
    batt = FancyBboxPatch((-5, 6.5), 10, 36, boxstyle="round,pad=0.5", fc=BATTERY_COLOR, ec='#1a5276', lw=2)
    ax.add_patch(batt)
    ax.text(0, 24.5, 'AAA\nBattery\n⌀10.5×44.5\n1.5V', ha='center', va='center', fontsize=8, color='white', fontweight='bold')

    # --- + contact plate ---
    ax.add_patch(patches.FancyBboxPatch((-3, 43), 6, 1.5, boxstyle="round,pad=0.2", fc='#aaa', ec='#666', lw=1))
    ax.text(0, 43.7, '+ plate', ha='center', va='center', fontsize=5.5, color='#333')

    # --- Wire ---
    ax.plot([0, 0], [44.5, 48], color='#e74c3c', lw=1.5, ls='--')
    ax.text(2, 46, 'wire', ha='left', va='center', fontsize=5.5, color='#e74c3c', fontstyle='italic')

    # --- Switch ---
    sw = FancyBboxPatch((-4, 48), 8, 5, boxstyle="round,pad=0.3", fc=SWITCH_COLOR, ec='#c0571e', lw=1.5)
    ax.add_patch(sw)
    ax.text(0, 50.5, 'Latching\nSwitch', ha='center', va='center', fontsize=7, color='white', fontweight='bold')
    # Button indicator on shell
    ax.annotate('← user presses\n   (TPE membrane)', xy=(7.5, 50.5), fontsize=7, color=SWITCH_COLOR,
                ha='left', va='center', fontstyle='italic')

    # --- TPE grip zone label ---
    ax.text(-9, 38, 'TPE\ngrip\nzone', ha='center', va='center', fontsize=7, color=TPE_COLOR, fontweight='bold', rotation=90)

    # --- Wire to motor ---
    ax.plot([0, 0], [53, 58], color='#e74c3c', lw=1.5, ls='--')

    # --- ERM Motor (axial) ---
    motor = FancyBboxPatch((-3.5, 58), 7, 14, boxstyle="round,pad=0.4", fc=MOTOR_COLOR, ec='#922b21', lw=2)
    ax.add_patch(motor)
    ax.text(0, 65, 'ERM\nMotor\n⌀6×12', ha='center', va='center', fontsize=7.5, color='white', fontweight='bold')
    # shaft arrow
    ax.annotate('', xy=(0, 72.5), xytext=(0, 72), arrowprops=dict(arrowstyle='->', color='white', lw=1.5))

    # --- Eccentric mass ---
    ecc = patches.Ellipse((1.5, 73.5), 4, 2.5, fc='#ff6b6b', ec='#c0392b', lw=1.5)
    ax.add_patch(ecc)
    ax.text(1.5, 73.5, '●', ha='center', va='center', fontsize=8, color='#922b21')
    ax.text(8, 73.5, '← eccentric\n   mass', ha='left', va='center', fontsize=6.5, color='#ff6b6b', fontstyle='italic')

    # --- Linkage arm ---
    ax.add_patch(patches.FancyBboxPatch((-1, 75), 3, 8, boxstyle="round,pad=0.2", fc=LINKAGE_COLOR, ec='#c0392b', lw=1, alpha=0.7))
    ax.text(1, 79, 'linkage\n~15mm', ha='center', va='center', fontsize=6, color='white', rotation=90)

    # --- TPE boot ---
    boot = FancyBboxPatch((-7, 82.5), 14, 3, boxstyle="round,pad=0.5", fc=TPE_COLOR, ec='#3d7a6a', lw=2, alpha=0.6)
    ax.add_patch(boot)
    ax.text(0, 84, 'TPE boot (seal)', ha='center', va='center', fontsize=6.5, color='white', fontweight='bold')
    ax.text(10, 84, '← dynamic\n   seal', ha='left', va='center', fontsize=6.5, color=TPE_COLOR, fontstyle='italic')

    # --- Split head ---
    # Pivot line
    ax.plot([-5.5, 5.5], [86, 86], color='white', lw=1, ls=':')
    ax.text(8, 86, '← pivot', ha='left', va='center', fontsize=6, color='white', fontstyle='italic')

    # Fixed half
    fixed = FancyBboxPatch((-5.5, 86.5), 5, 8, boxstyle="round,pad=0.3", fc=PP_COLOR, ec='#a8a060', lw=1.5)
    ax.add_patch(fixed)
    ax.text(-3, 90.5, 'Fixed\nHalf', ha='center', va='center', fontsize=7, color='#333', fontweight='bold')

    # Moving half
    moving = FancyBboxPatch((0.5, 86.5), 5, 8, boxstyle="round,pad=0.3", fc='#f0e68c', ec='#b8a030', lw=1.5)
    ax.add_patch(moving)
    ax.text(3, 90.5, 'Moving\nHalf', ha='center', va='center', fontsize=7, color='#333', fontweight='bold')
    # oscillation arrow
    ax.annotate('', xy=(5.8, 90.5), xytext=(5.8, 88.5), arrowprops=dict(arrowstyle='<->', color='#b8a030', lw=1.5))
    ax.text(8, 89.5, '↕1-2mm', fontsize=6, color='#b8a030', ha='left')

    # Bristles
    for x in np.linspace(-4.5, 4.5, 10):
        color = BRISTLE_COLOR
        ax.plot([x, x], [94.5, 99], color=color, lw=2.5, solid_capstyle='round')
    ax.text(0, 101, 'bristle tips', ha='center', va='center', fontsize=7, color=BRISTLE_COLOR, fontstyle='italic')

    # Dimension annotations
    ax.annotate('', xy=(-8.5, 4), xytext=(-8.5, 85), arrowprops=dict(arrowstyle='<->', color='#888', lw=1))
    ax.text(-10.5, 44, '~160mm\ntotal', ha='center', va='center', fontsize=7, color='#888', rotation=90)

    ax.annotate('', xy=(-7.5, 58), xytext=(7.5, 58), arrowprops=dict(arrowstyle='<->', color='#888', lw=1))
    ax.text(0, 56, '~15mm neck', ha='center', va='top', fontsize=6.5, color='#888')


def draw_option_b(ax):
    ax.set_facecolor(BG)
    ax.set_xlim(-12, 12)
    ax.set_ylim(-5, 105)
    ax.set_aspect('equal')
    ax.set_title('Option B — Transverse Motor', color='white', fontsize=16, fontweight='bold', pad=15)
    ax.axis('off')

    # --- Battery cap + O-ring (bottom) ---
    cap = FancyBboxPatch((-6, 0), 12, 3, boxstyle="round,pad=0.3", fc='#888888', ec='#555555', lw=1.5)
    ax.add_patch(cap)
    ax.text(0, 1.5, 'Battery Cap\n(threaded PP)', ha='center', va='center', fontsize=6, color='white', fontweight='bold')
    ax.add_patch(patches.Ellipse((0, 3.2), 10, 1.2, fc=ORING_COLOR, ec='#444', lw=1))

    # --- Shell outline (main body) ---
    shell = FancyBboxPatch((-7.5, 3.5), 15, 73, boxstyle="round,pad=0.8", fc=TPE_COLOR, ec='#3d7a6a', lw=2, alpha=0.35)
    ax.add_patch(shell)
    body = FancyBboxPatch((-6.5, 4), 13, 72, boxstyle="round,pad=0.5", fc=PP_COLOR, ec='#a8a060', lw=1.5, alpha=0.3)
    ax.add_patch(body)

    # Wider neck section
    neck = FancyBboxPatch((-9, 72), 18, 14, boxstyle="round,pad=0.8", fc=TPE_COLOR, ec='#3d7a6a', lw=2, alpha=0.35)
    ax.add_patch(neck)
    neck_inner = FancyBboxPatch((-8, 72.5), 16, 13, boxstyle="round,pad=0.5", fc=PP_COLOR, ec='#a8a060', lw=1.5, alpha=0.3)
    ax.add_patch(neck_inner)

    # --- Spring contact ---
    ax.add_patch(patches.FancyBboxPatch((-3, 4.5), 6, 1.5, boxstyle="round,pad=0.2", fc='#aaa', ec='#666', lw=1))
    ax.text(0, 5.2, '− spring', ha='center', va='center', fontsize=5.5, color='#333')

    # --- AAA Battery ---
    batt = FancyBboxPatch((-5, 6.5), 10, 36, boxstyle="round,pad=0.5", fc=BATTERY_COLOR, ec='#1a5276', lw=2)
    ax.add_patch(batt)
    ax.text(0, 24.5, 'AAA\nBattery\n⌀10.5×44.5\n1.5V', ha='center', va='center', fontsize=8, color='white', fontweight='bold')

    # --- + contact plate ---
    ax.add_patch(patches.FancyBboxPatch((-3, 43), 6, 1.5, boxstyle="round,pad=0.2", fc='#aaa', ec='#666', lw=1))
    ax.text(0, 43.7, '+ plate', ha='center', va='center', fontsize=5.5, color='#333')

    # --- Wire ---
    ax.plot([0, 0], [44.5, 48], color='#e74c3c', lw=1.5, ls='--')

    # --- Switch ---
    sw = FancyBboxPatch((-4, 48), 8, 5, boxstyle="round,pad=0.3", fc=SWITCH_COLOR, ec='#c0571e', lw=1.5)
    ax.add_patch(sw)
    ax.text(0, 50.5, 'Latching\nSwitch', ha='center', va='center', fontsize=7, color='white', fontweight='bold')
    ax.annotate('← user presses', xy=(7.5, 50.5), fontsize=7, color=SWITCH_COLOR,
                ha='left', va='center', fontstyle='italic')

    # --- TPE grip zone label ---
    ax.text(-9, 38, 'TPE\ngrip\nzone', ha='center', va='center', fontsize=7, color=TPE_COLOR, fontweight='bold', rotation=90)

    # --- Wire to motor ---
    ax.plot([0, 0], [53, 73], color='#e74c3c', lw=1.5, ls='--')

    # --- ERM Motor (transverse - horizontal) ---
    motor = FancyBboxPatch((-6.5, 74), 13, 6, boxstyle="round,pad=0.4", fc=MOTOR_COLOR, ec='#922b21', lw=2)
    ax.add_patch(motor)
    ax.text(0, 77, 'ERM Motor ⌀6×12\n(transverse)', ha='center', va='center', fontsize=7, color='white', fontweight='bold')
    # eccentric on right side
    ecc = patches.Ellipse((5, 81), 3, 2.5, fc='#ff6b6b', ec='#c0392b', lw=1.5)
    ax.add_patch(ecc)
    ax.text(5, 81, '●', ha='center', va='center', fontsize=7, color='#922b21')

    # --- Stub arm (very short) ---
    ax.add_patch(patches.FancyBboxPatch((4, 82.5), 2, 3, boxstyle="round,pad=0.2", fc=LINKAGE_COLOR, ec='#c0392b', lw=1, alpha=0.7))
    ax.text(10.5, 82, '← stub arm\n   (direct)', ha='left', va='center', fontsize=6, color='#ff6b6b', fontstyle='italic')

    # --- TPE boot ---
    boot = FancyBboxPatch((-8, 85), 16, 3, boxstyle="round,pad=0.5", fc=TPE_COLOR, ec='#3d7a6a', lw=2, alpha=0.6)
    ax.add_patch(boot)
    ax.text(0, 86.5, 'TPE boot (seal)', ha='center', va='center', fontsize=6.5, color='white', fontweight='bold')

    # --- Split head ---
    ax.plot([-5.5, 5.5], [88.5, 88.5], color='white', lw=1, ls=':')

    # Fixed half
    fixed = FancyBboxPatch((-5.5, 89), 5, 8, boxstyle="round,pad=0.3", fc=PP_COLOR, ec='#a8a060', lw=1.5)
    ax.add_patch(fixed)
    ax.text(-3, 93, 'Fixed\nHalf', ha='center', va='center', fontsize=7, color='#333', fontweight='bold')

    # Moving half
    moving = FancyBboxPatch((0.5, 89), 5, 8, boxstyle="round,pad=0.3", fc='#f0e68c', ec='#b8a030', lw=1.5)
    ax.add_patch(moving)
    ax.text(3, 93, 'Moving\nHalf', ha='center', va='center', fontsize=7, color='#333', fontweight='bold')
    ax.annotate('', xy=(5.8, 93), xytext=(5.8, 91), arrowprops=dict(arrowstyle='<->', color='#b8a030', lw=1.5))
    ax.text(8, 92, '↕1-2mm', fontsize=6, color='#b8a030', ha='left')

    # Bristles
    for x in np.linspace(-4.5, 4.5, 10):
        ax.plot([x, x], [97, 101.5], color=BRISTLE_COLOR, lw=2.5, solid_capstyle='round')
    ax.text(0, 103.5, 'bristle tips', ha='center', va='center', fontsize=7, color=BRISTLE_COLOR, fontstyle='italic')

    # Dimension annotations
    ax.annotate('', xy=(-10, 4), xytext=(-10, 88), arrowprops=dict(arrowstyle='<->', color='#888', lw=1))
    ax.text(-12, 46, '~165mm\ntotal', ha='center', va='center', fontsize=7, color='#888', rotation=90)

    ax.annotate('', xy=(-9, 74), xytext=(9, 74), arrowprops=dict(arrowstyle='<->', color='#888', lw=1))
    ax.text(0, 72, '~18mm neck (wider)', ha='center', va='top', fontsize=6.5, color='#f39c12')

    ax.annotate('', xy=(-7.5, 48), xytext=(7.5, 48), arrowprops=dict(arrowstyle='<->', color='#888', lw=1))
    ax.text(0, 46, '~15mm handle', ha='center', va='top', fontsize=6.5, color='#888')


draw_option_a(ax1)
draw_option_b(ax2)

# Legend at bottom
fig.text(0.5, 0.02,
    '■ Red = Motor/Eccentric    ■ Blue = Battery    ■ Orange = Switch    ■ Green = TPE overmold    ■ Tan = Rigid PP body    ■ White = Bristles',
    ha='center', va='center', fontsize=9, color='#aaa',
    bbox=dict(boxstyle='round,pad=0.5', fc='#22223a', ec='#444'))

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig('output/single-use-electric-toothbrush-nfc/arrangement_options.png', dpi=150, facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close()
print("Saved arrangement_options.png")
