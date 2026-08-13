#!/usr/bin/env python3
"""Generate OG image for qm.diazites.online landing (1200x630, dark premium)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random

W, H = 1200, 630
BG = (8, 11, 18)
ACC = (79, 140, 255)
ACC2 = (110, 231, 183)
MUT = (139, 150, 171)
TXT = (238, 242, 249)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ambient orbs (radial gradients)
def radial(center, radius, color, alpha):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    steps = 60
    for i in range(steps, 0, -1):
        r = radius * i / steps
        a = int(alpha * (1 - i / steps) ** 2)
        d.ellipse([center[0]-r, center[1]-r, center[0]+r, center[1]+r], fill=(*color, a))
    return layer

img = Image.alpha_composite(img.convert("RGBA"), radial((-150, -200), 700, (79, 140, 255), 130))
img = Image.alpha_composite(img, radial((1150, 150), 650, (110, 231, 183), 90))
img = Image.alpha_composite(img, radial((600, 750), 600, (124, 92, 255), 70))
img = img.convert("RGB")
draw = ImageDraw.Draw(img)

# subtle grid
grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grid)
for x in range(0, W, 52):
    gd.line([(x, 0), (x, H)], fill=(148, 163, 184, 12))
for y in range(0, H, 52):
    gd.line([(0, y), (W, y)], fill=(148, 163, 184, 12))
img = Image.alpha_composite(img.convert("RGBA"), grid).convert("RGB")
draw = ImageDraw.Draw(img)

def font(path, size):
    return ImageFont.truetype(path, size)

F_REG = "/tmp/Inter-Regular.ttf"
F_BOLD = "/tmp/Inter-Bold.ttf"
F_XB = "/tmp/Inter-ExtraBold.ttf"

# ---- logo mark (gradient rounded square + chat bubble) ----
lm = 84
lms = Image.new("RGBA", (lm, lm), (0, 0, 0, 0))
ld = ImageDraw.Draw(lms)
# gradient fill (vertical blue->green)
for y in range(lm):
    t = y / lm
    col = tuple(int(ACC[i] + (ACC2[i] - ACC[i]) * t) for i in range(3))
    ld.line([(0, y), (lm, y)], fill=(*col, 255))
mask = Image.new("L", (lm, lm), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([0, 0, lm-1, lm-1], radius=22, fill=255)
lms.putalpha(mask)
img.paste(lms, (70, 56), lms)
# chat bubble stroke
bd = ImageDraw.Draw(img)
def bubble(d, cx, cy, s, color, width=5):
    r = s
    d.arc([cx-r, cy-r, cx+r, cy+r], 150, 330, fill=color, width=width)
    d.arc([cx-r, cy-r, cx+r, cy+r], -30, 90, fill=color, width=width)
    # tail
    d.line([(cx + r*math.cos(math.radians(45)), cy + r*math.sin(math.radians(45))),
            (cx + r*math.cos(math.radians(45)) + 14, cy + r*math.sin(math.radians(45)) + 14)], fill=color, width=width)
bubble(bd, 70+42, 56+42, 19, (255, 255, 255, 255))

# ---- "Diazites." wordmark ----
draw.text((180, 66), "Diazites", font=font(F_XB, 40), fill=TXT)
draw.text((335, 66), ".", font=font(F_XB, 40), fill=ACC)

# ---- headline ----
draw.text((70, 230), "Your voice agent takes the call.", font=font(F_XB, 62), fill=TXT)
draw.text((70, 310), "This employee closes the loop.", font=font(F_XB, 62), fill=ACC)

# ---- subline ----
draw.text((70, 420), "Answers every call  ·  Follows up every lead  ·  Remembers every customer", font=font(F_REG, 28), fill=MUT)

# ---- CTA pill ----
px, py, pw, ph = 70, 500, 300, 62
draw.rounded_rectangle([px, py, px+pw, py+ph], radius=16, fill=(79, 140, 255, 255))
# subtle gradient on pill
pill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pd = ImageDraw.Draw(pill)
for y in range(ph):
    t = y / ph
    col = tuple(int(ACC[i] + (ACC2[i] - ACC[i]) * t) for i in range(3))
    pd.line([(px, py+y), (px+pw, py+y)], fill=(*col, 255))
pm = Image.new("L", (W, H), 0)
pmd = ImageDraw.Draw(pm)
pmd.rounded_rectangle([px, py, px+pw, py+ph], radius=16, fill=255)
img = Image.alpha_composite(img.convert("RGBA"), Image.composite(pill, Image.new("RGBA", (W, H), (0,0,0,0)), pm)).convert("RGB")
draw = ImageDraw.Draw(img)
draw.text((px+24, py+16), "Hire your AI employee", font=font(F_BOLD, 24), fill=(255, 255, 255))

# price chip
draw.rounded_rectangle([px+330, py, px+330+190, py+ph], radius=16, outline=(148, 163, 184, 120), width=2)
draw.text((px+330+24, py+16), "From $97/mo", font=font(F_BOLD, 24), fill=TXT)

img.save("/root/qm-landing-v2/og-image.png", "PNG")
print("OG image saved:", img.size)
