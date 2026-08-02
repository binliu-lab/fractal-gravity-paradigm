# -*- coding: utf-8 -*-
"""
Generate a golden-ratio themed image for the Fractal Gravity Paradigm project.
Enhanced version: more luminous, more cosmic, more depth.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, FancyBboxPatch
import matplotlib.patheffects as pe
from PIL import Image, ImageDraw, ImageFilter
import io
import math

PHI = (1 + np.sqrt(5)) / 2  # 1.618...

# ========== Canvas: 16:9 ==========
fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('#000814')

# ========== Cosmic Background: deep gradient + nebula + stars ==========
bg_width, bg_height = 1600, 900
bg = Image.new('RGB', (bg_width, bg_height), '#000814')
bg_draw = ImageDraw.Draw(bg)
cx, cy = bg_width // 2, bg_height // 2

# Step 1: Radial gradient from center
max_r = int(math.sqrt(cx**2 + cy**2))
for r in range(max_r, 0, -2):
    ratio = r / max_r
    # Deep purple-blue center, near-black edges
    if ratio < 0.3:
        # Central glow area: purple/violet
        red = int(20 + 40 * (1 - ratio/0.3))
        green = int(5 + 15 * (1 - ratio/0.3))
        blue = int(40 + 60 * (1 - ratio/0.3))
    else:
        # Outer: deep blue-purple
        t = (ratio - 0.3) / 0.7
        red = int(20 * (1 - t) + 5 * t)
        green = int(5 * (1 - t) + 5 * t)
        blue = int(40 * (1 - t) + 20 * t)
    bg_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(red, green, blue))

bg = bg.filter(ImageFilter.GaussianBlur(radius=50))

# Step 2: Add nebula clouds (small purple/violet blobs)
np.random.seed(7)
for _ in range(15):
    nx = np.random.randint(100, bg_width - 100)
    ny = np.random.randint(100, bg_height - 100)
    nr = np.random.randint(60, 150)
    # Color: purple, violet, blue
    color_choice = np.random.choice(['purple', 'violet', 'blue', 'magenta'])
    if color_choice == 'purple':
        c = (60, 20, 100)
    elif color_choice == 'violet':
        c = (80, 30, 120)
    elif color_choice == 'blue':
        c = (30, 40, 100)
    else:
        c = (90, 30, 90)
    blob = Image.new('RGB', (nr*2, nr*2), c)
    # Make it blob-shaped with random mask
    mask = Image.new('L', (nr*2, nr*2), 0)
    mask_draw = ImageDraw.Draw(mask)
    for i in range(nr, 0, -5):
        alpha = int(60 * (1 - i/nr))
        mask_draw.ellipse([nr-i, nr-i, nr+i, nr+i], fill=alpha)
    blob.putalpha(mask)
    bg.paste(blob, (nx-nr, ny-nr), blob)

bg = bg.filter(ImageFilter.GaussianBlur(radius=20))

# Step 3: Add stars (3 layers: small, medium, large with glow)
np.random.seed(42)
# Small dim stars
for _ in range(500):
    sx = np.random.randint(0, bg_width)
    sy = np.random.randint(0, bg_height)
    brightness = np.random.randint(80, 180)
    size = 1
    bg_draw.ellipse([sx - size, sy - size, sx + size, sy + size],
                     fill=(brightness, brightness, min(255, brightness + 30)))

# Medium bright stars
for _ in range(100):
    sx = np.random.randint(0, bg_width)
    sy = np.random.randint(0, bg_height)
    brightness = np.random.randint(180, 240)
    size = 2
    bg_draw.ellipse([sx - size, sy - size, sx + size, sy + size],
                     fill=(brightness, brightness, brightness))
    # Add subtle glow
    bg_draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4],
                     fill=(brightness//3, brightness//3, brightness//3))

# Large bright stars with cross flare
for _ in range(15):
    sx = np.random.randint(100, bg_width - 100)
    sy = np.random.randint(100, bg_height - 100)
    brightness = np.random.randint(220, 255)
    # Center
    bg_draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(brightness, brightness, brightness))
    # Glow
    bg_draw.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill=(brightness//4, brightness//4, brightness//4))
    # Cross flare (vertical and horizontal)
    bg_draw.line([sx, sy - 12, sx, sy + 12], fill=(brightness, brightness, brightness), width=1)
    bg_draw.line([sx - 12, sy, sx + 12, sy], fill=(brightness, brightness, brightness), width=1)

# Paste background onto figure
buf = io.BytesIO()
bg.save(buf, format='PNG')
buf.seek(0)
bg_img = plt.imread(buf)
ax.imshow(bg_img, extent=[0, 16, 0, 9], aspect='auto', zorder=0, alpha=1.0)

# ========== Central golden aura ==========
center_x, center_y = 8.0, 4.5
# Outer warm glow
for i in range(40, 0, -1):
    r = 0.08 * i
    alpha = 0.015 * (41 - i) / 40
    glow = Circle((center_x, center_y), r, color='#FFB347', alpha=alpha, zorder=1)
    ax.add_patch(glow)

# Inner golden glow
for i in range(20, 0, -1):
    r = 0.06 * i
    alpha = 0.04 * (21 - i) / 20
    glow = Circle((center_x, center_y), r, color='#FFD700', alpha=alpha, zorder=2)
    ax.add_patch(glow)

# ========== Background Pentagon Mesh (subtle, large) ==========
def draw_pentagon(cx, cy, radius, angle_offset=0, color='#FFD700', alpha=0.4, lw=1.5, zorder=3):
    angles = np.linspace(0, 2*np.pi, 6)[:-1] + angle_offset - np.pi/2
    pts = np.column_stack([cx + radius * np.cos(angles), cy + radius * np.sin(angles)])
    polygon = Polygon(pts, closed=True, fill=False, edgecolor=color, alpha=alpha,
                      linewidth=lw, zorder=zorder)
    ax.add_patch(polygon)
    return pts

# Large outer pentagons (background)
for i in range(1, 5):
    r = 4.5 * (PHI ** (i * 0.25))
    if r > 12:
        continue
    angle = -i * np.pi / 5
    draw_pentagon(center_x, center_y, r, angle, '#DAA520', 0.08, 0.8, zorder=2)

# ========== Golden Ratio Connection Lines ==========
for angle_deg in range(0, 360, 36):
    angle_rad = np.radians(angle_deg)
    end_x = center_x + 5.5 * np.cos(angle_rad - np.pi/2)
    end_y = center_y + 5.5 * np.sin(angle_rad - np.pi/2)
    ax.plot([center_x, end_x], [center_y, end_y], color='#DAA520',
            alpha=0.06, linewidth=0.5, zorder=2, linestyle=':')

# ========== Nested Pentagons (main feature) ==========
pentagon_radius = 3.5
for i in range(15):
    scale = PHI ** (-i * 0.4)
    r = pentagon_radius * scale
    if r < 0.12:
        break
    angle = i * np.pi / 5
    alpha = max(0.15, 0.7 - i * 0.04)
    lw = max(0.4, 2.5 - i * 0.15)
    # Glow effect: draw twice, once thick faint, once thin bright
    if i < 5:
        draw_pentagon(center_x, center_y, r, angle, '#FFA500', alpha*0.5, lw*2.5, zorder=5)
    draw_pentagon(center_x, center_y, r, angle, '#FFD700', alpha, lw, zorder=6)

# ========== Golden Spiral (logarithmic) ==========
# Use golden spiral: r = a * phi^(2*theta/pi)
theta_main = np.linspace(0, 5 * np.pi, 2000)
r_main = 0.08 * np.exp(0.18 * theta_main)
x_main = center_x + r_main * np.cos(theta_main)
y_main = center_y + r_main * np.sin(theta_main)
mask = (x_main > 0.5) & (x_main < 15.5) & (y_main > 0.5) & (y_main < 8.5)

# Glow trail
spiral_glow, = ax.plot(x_main[mask], y_main[mask], color='#FFA500', alpha=0.4,
                        linewidth=4.0, zorder=4, solid_capstyle='round')
spiral_main, = ax.plot(x_main[mask], y_main[mask], color='#FFFFE0', alpha=0.95,
                        linewidth=1.8, zorder=5, solid_capstyle='round')
spiral_main.set_path_effects([pe.Stroke(linewidth=3, foreground='#FFD700', alpha=0.6), pe.Normal()])

# Second arm (rotated 180°)
x2 = center_x + r_main * np.cos(theta_main + np.pi)
y2 = center_y + r_main * np.sin(theta_main + np.pi)
mask2 = (x2 > 0.5) & (x2 < 15.5) & (y2 > 0.5) & (y2 < 8.5)
ax.plot(x2[mask2], y2[mask2], color='#FFB347', alpha=0.5, linewidth=1.0,
        zorder=3, solid_capstyle='round')

# ========== Mark Golden Ratio Points on spiral ==========
# At each phi ratio (1/phi, 1/phi², 1/phi³...), mark a small dot
for i in range(1, 8):
    theta_mark = i * np.pi / PHI
    if theta_mark > 5 * np.pi:
        break
    r_mark = 0.08 * np.exp(0.18 * theta_mark)
    x_mark = center_x + r_mark * np.cos(theta_mark)
    y_mark = center_y + r_mark * np.sin(theta_mark)
    if 0.5 < x_mark < 15.5 and 0.5 < y_mark < 8.5:
        ax.plot(x_mark, y_mark, 'o', color='#FFFFFF', markersize=4,
                markeredgecolor='#FFD700', markeredgewidth=1, zorder=8)

# ========== Central Bright Core ==========
for i in range(15, 0, -1):
    r = 0.04 * i
    alpha = 0.05 * (16 - i) / 15
    glow = Circle((center_x, center_y), r, color='#FFFFFF', alpha=alpha, zorder=9)
    ax.add_patch(glow)
ax.plot(center_x, center_y, 'o', color='#FFFFFF', markersize=10, zorder=11,
        markeredgecolor='#FFD700', markeredgewidth=2.5)

# ========== Title text - main formula ==========
# Top center: golden ratio
ax.text(8.0, 8.4, r'$\varphi = \frac{1+\sqrt{5}}{2} \approx 1.618$',
        fontsize=30, color='#FFD700', ha='center', va='center',
        fontweight='bold', zorder=20,
        path_effects=[pe.withStroke(linewidth=4, foreground='#000000', alpha=0.8)])

# Sub-formulas line
ax.text(8.0, 7.75, r'$S = 0.618$  |  $\eta = \cos(\pi/5) = \varphi/2$  |  $\Omega = \frac{4}{5\varphi}$',
        fontsize=13, color='#FFB347', ha='center', va='center',
        style='italic', zorder=20,
        path_effects=[pe.withStroke(linewidth=2, foreground='#000000', alpha=0.7)])

# Bottom: project name
ax.text(8.0, 0.55, 'QI  ·  Qi-Field Fractal Gravity Framework',
        fontsize=18, color='#DAA520', ha='center', va='center',
        fontweight='bold', zorder=20, alpha=0.95,
        path_effects=[pe.withStroke(linewidth=2.5, foreground='#000000', alpha=0.8)])

# Bottom decoration line
ax.text(8.0, 0.18, r'$\diamond$   $\varphi$-cascade   $\diamond$   $D_5$ symmetry   $\diamond$   fractal spacetime   $\diamond$',
        fontsize=11, color='#B8860B', ha='center', va='center',
        alpha=0.7, zorder=20, style='italic',
        path_effects=[pe.withStroke(linewidth=1.5, foreground='#000000', alpha=0.5)])

# ========== Corner mini-pentagons (decorative) ==========
for corner_x, corner_y in [(1.2, 7.7), (14.8, 7.7), (1.2, 1.3), (14.8, 1.3)]:
    for i in range(5):
        r = 0.55 * PHI ** (-i * 0.5)
        if r < 0.06:
            break
        draw_pentagon(corner_x, corner_y, r, i * np.pi/5,
                     '#B8860B', 0.18 - i*0.025, 0.7, zorder=4)
    # Center bright dot
    ax.plot(corner_x, corner_y, 'o', color='#FFD700', markersize=3,
            markeredgecolor='#B8860B', markeredgewidth=0.5, zorder=10)

# ========== Save ==========
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
output_path = r'c:\Users\win10\WorkBuddy\Claw\fractal-gravity-paradigm\golden_ratio_cover.png'
fig.savefig(output_path, dpi=150, facecolor='#000814', bbox_inches=None,
            pad_inches=0)
plt.close()

# Convert to JPG for WeChat compatibility
img = Image.open(output_path).convert('RGB')
# Resize to recommended 900x383 (WeChat small image standard)
target_w, target_h = 900, 383
img_resized = img.resize((target_w, target_h), Image.LANCZOS)
jpg_path = r'c:\Users\win10\WorkBuddy\Claw\fractal-gravity-paradigm\golden_ratio_cover.jpg'
img_resized.save(jpg_path, 'JPEG', quality=92)

# Also keep a larger 1200x675 version for other platforms
target_w2, target_h2 = 1200, 675
img_resized2 = img.resize((target_w2, target_h2), Image.LANCZOS)
jpg_path2 = r'c:\Users\win10\WorkBuddy\Claw\fractal-gravity-paradigm\golden_ratio_cover_large.jpg'
img_resized2.save(jpg_path2, 'JPEG', quality=92)

print(f"PNG saved: {output_path}")
print(f"JPG (900x383): {jpg_path}")
print(f"JPG (1200x675): {jpg_path2}")
print(f"Original size: {img.size}")