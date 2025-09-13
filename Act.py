from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

# ---------- Config ----------
OUTFILE = "BSCS3B_FirstAidersGuild_Trophy.png"
W, H = 900, 1100
BG_CENTER = (W // 2, H // 3)  # center of radial background
MEDAL_BOX = (220, 160, 680, 560)  # left, top, right, bottom (medal ellipse)
INNER_MARGIN = 30  # inner margin inside medal
RIBBON_TOP = 560

# Colors
gold = (212, 175, 55)
dark_gold = (170, 130, 30)
black = (10, 10, 10)
white = (255, 255, 255)
red = (220, 20, 60)
teal = (12, 170, 160)
purple = (160, 80, 200)
blue = (30, 144, 255)
pink = (255, 100, 160)

# ---------- Helpers ----------
def radial_gradient(size, inner_color, outer_color):
    """Return an Image with radial gradient."""
    cx, cy = size[0] // 2, size[1] // 3
    max_r = math.hypot(cx, cy)
    base = Image.new("RGB", size, outer_color)
    pix = base.load()
    for y in range(size[1]):
        for x in range(size[0]):
            dx = x - cx
            dy = y - cy
            r = math.hypot(dx, dy) / max_r
            r = min(1.0, max(0.0, r))
            ir = int(inner_color[0] * (1 - r) + outer_color[0] * r)
            ig = int(inner_color[1] * (1 - r) + outer_color[1] * r)
            ib = int(inner_color[2] * (1 - r) + outer_color[2] * r)
            pix[x, y] = (ir, ig, ib)
    return base

def draw_text_with_outline(draw, position, text, font, fill, outline_fill, outline_width=2):
    x, y = position
    for ox in range(-outline_width, outline_width + 1):
        for oy in range(-outline_width, outline_width + 1):
            if ox == 0 and oy == 0:
                continue
            draw.text((x + ox, y + oy), text, font=font, fill=outline_fill)
    draw.text((x, y), text, font=font, fill=fill)

# ---------- Canvas & background ----------
canvas = Image.new("RGB", (W, H), (255, 255, 255))
bg = radial_gradient((W, H), inner_color=(240, 250, 255), outer_color=(200, 220, 255))
canvas.paste(bg, (0, 0))
draw = ImageDraw.Draw(canvas)

# ---------- Top banner ----------
banner_left, banner_top, banner_right, banner_bottom = 80, 20, W - 80, 90
draw.rounded_rectangle((banner_left, banner_top, banner_right, banner_bottom), radius=30, fill=(255, 255, 255, 230))

banner_text = "INTRAMURALS 2025 — RECOGNIZING OUR MEDICS"

# Auto resize font for banner
banner_font_size = 36
while banner_font_size > 10:
    try:
        banner_font = ImageFont.truetype("arialbd.ttf", banner_font_size)
    except:
        banner_font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), banner_text, font=banner_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    if tw <= (banner_right - banner_left - 20) and th <= (banner_bottom - banner_top - 10):
        break
    banner_font_size -= 2

bx = (banner_left + banner_right - tw) // 2
by = (banner_top + banner_bottom - th) // 2
draw_text_with_outline(draw, (bx, by), banner_text, banner_font, fill=black, outline_fill=white, outline_width=1)

# ---------- Medal ----------
left, top, right, bottom = MEDAL_BOX
draw.ellipse((left - 8, top - 8, right + 8, bottom + 8), fill=dark_gold)
draw.ellipse((left, top, right, bottom), fill=gold, outline=dark_gold, width=8)

# inner boundary for text
inner_left = left + INNER_MARGIN
inner_top = top + INNER_MARGIN
inner_right = right - INNER_MARGIN
inner_bottom = bottom - INNER_MARGIN

# ---------- Red Cross ----------
cross_w = int((inner_right - inner_left) * 0.28)
cross_h = cross_w
cx = (inner_left + inner_right) // 2
cy = (inner_top + inner_bottom) // 2 - 15
cw = cross_w // 3
draw.rectangle((cx - cw, cy - cross_h // 2, cx + cw, cy + cross_h // 2), fill=white)
draw.rectangle((cx - cross_w // 2, cy - cw, cx + cross_w // 2, cy + cw), fill=white)
draw.rectangle((cx - cw + 3, cy - cross_h // 2 + 3, cx + cw - 3, cy + cross_h // 2 - 3), fill=red)
draw.rectangle((cx - cross_w // 2 + 3, cy - cw + 3, cx + cross_w // 2 - 3, cy + cw - 3), fill=red)

# ---------- Medal text ----------
lines = ["FIRST AIDERS", "GUILD"]
fit_w = inner_right - inner_left
fit_h = inner_bottom - inner_top
font_size = 72
chosen_font = None
line_sizes = []
line_spacing = 6

while font_size > 10:
    try:
        font = ImageFont.truetype("arialbd.ttf", font_size)
    except:
        font = ImageFont.load_default()
    total_h = -line_spacing
    max_w = 0
    sizes = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w_line = bbox[2] - bbox[0]
        h_line = bbox[3] - bbox[1]
        sizes.append((w_line, h_line))
        total_h += h_line + line_spacing
        if w_line > max_w:
            max_w = w_line
    if max_w <= (fit_w - 40) and total_h <= (fit_h - 40):
        chosen_font = font
        line_sizes = sizes
        break
    font_size -= 2

if chosen_font is None:
    chosen_font = ImageFont.truetype("arialbd.ttf", 20)
    line_sizes = []
    total_h = -line_spacing
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=chosen_font)
        w_line = bbox[2] - bbox[0]
        h_line = bbox[3] - bbox[1]
        line_sizes.append((w_line, h_line))
        total_h += h_line + line_spacing

block_h = sum([h for _, h in line_sizes]) + line_spacing * (len(lines) - 1)
cx = (inner_left + inner_right) // 2
cy = (inner_top + inner_bottom) // 2 + 30
start_y = cy - block_h // 2

for i, line in enumerate(lines):
    w_line, h_line = line_sizes[i]
    x = cx - w_line // 2
    y = start_y
    draw_text_with_outline(draw, (x, y), line, chosen_font, fill=black, outline_fill=white, outline_width=2)
    start_y += h_line + line_spacing

# ---------- Ribbon ----------
ribbon_x_center = (left + right) // 2
ribbon_colors = [blue, teal, purple, pink, red]
for i, c in enumerate(ribbon_colors):
    offset = i * 10
    draw.polygon([(ribbon_x_center - 80 + offset, RIBBON_TOP + offset // 2),
                  (ribbon_x_center, RIBBON_TOP + offset // 2),
                  (ribbon_x_center - 20, H - 80),
                  (ribbon_x_center - 160, H - 240)], fill=c)
    draw.polygon([(ribbon_x_center, RIBBON_TOP + offset // 2),
                  (ribbon_x_center + 80 - offset, RIBBON_TOP + offset // 2),
                  (ribbon_x_center + 160, H - 240),
                  (ribbon_x_center + 20, H - 80)], fill=c)

# ---------- Base ----------
base_top = H - 220
draw.rectangle((320, base_top, 580, base_top + 70), fill=dark_gold, outline=black, width=4)
draw.rectangle((280, base_top + 70, 620, base_top + 120), fill=gold, outline=dark_gold, width=4)

# ---------- Plaque ----------
plaque_w, plaque_h = 180, 50
plaque_x = (W - plaque_w) // 2
plaque_y = base_top + 10
draw.rounded_rectangle((plaque_x, plaque_y, plaque_x + plaque_w, plaque_y + plaque_h), radius=8, fill=(30, 30, 30))

plaque_text = "FAG"

plaque_font_size = 28
while plaque_font_size > 10:
    try:
        plaque_font = ImageFont.truetype("arialbd.ttf", plaque_font_size)
    except:
        plaque_font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), plaque_text, font=plaque_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    if tw <= (plaque_w - 20) and th <= (plaque_h - 10):
        break
    plaque_font_size -= 2

px = plaque_x + (plaque_w - tw) // 2
py = plaque_y + (plaque_h - th) // 2
draw_text_with_outline(draw, (px, py), plaque_text, plaque_font, fill=white, outline_fill=black, outline_width=1)




# Save output
canvas.save("BSCS3_3B_Caslibhannahfaith_Activity1.png")
print("Saved as BSCS3_3B_Caslibhannahfaith_Activity1.png")