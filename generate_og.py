"""Generate a 1200x630 Open Graph social-preview banner for the portfolio."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W, H = 1200, 630
BG = (12, 1, 24)
C1 = (255, 77, 141)    # pink
C2 = (155, 92, 255)    # purple
C3 = (0, 224, 208)     # teal
WHITE = (244, 236, 255)
DIM = (184, 169, 212)

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = r"C:\Windows\Fonts"


def font(name, size):
    for cand in (name, "segoeuib.ttf", "arialbd.ttf", "arial.ttf"):
        p = os.path.join(FONTS, cand)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def linear_gradient(size, colors):
    """Diagonal multi-stop gradient."""
    w, h = size
    base = Image.new("RGB", size, colors[0])
    px = base.load()
    n = len(colors) - 1
    for y in range(h):
        for x in range(w):
            t = (x / w + y / h) / 2  # diagonal 0..1
            seg = min(int(t * n), n - 1)
            lt = t * n - seg
            px[x, y] = lerp(colors[seg], colors[seg + 1], lt)
    return base


def radial_glow(center, radius, color, strength=1.0):
    """Return an RGBA glow layer."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = center
    d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
              fill=color + (int(180 * strength),))
    return layer.filter(ImageFilter.GaussianBlur(radius * 0.6))


# --- Background ---
img = Image.new("RGB", (W, H), BG)
img = Image.alpha_composite(img.convert("RGBA"), radial_glow((120, 90), 360, C2, 0.9))
img = Image.alpha_composite(img, radial_glow((1080, 560), 380, C3, 0.7))
img = Image.alpha_composite(img, radial_glow((760, 120), 300, C1, 0.6))
img = img.convert("RGB")
draw = ImageDraw.Draw(img)

# --- Circular profile photo with gradient ring (right side) ---
D = 340
ring = 12
cx, cy = 940, H // 2
# gradient ring
grad = linear_gradient((D + ring * 2, D + ring * 2), [C1, C2, C3])
ring_mask = Image.new("L", grad.size, 0)
ImageDraw.Draw(ring_mask).ellipse([0, 0, grad.size[0], grad.size[1]], fill=255)
img.paste(grad, (cx - D // 2 - ring, cy - D // 2 - ring), ring_mask)

photo_path = os.path.join(HERE, "profile.jpg")
if os.path.exists(photo_path):
    photo = Image.open(photo_path).convert("RGB")
    # cover-crop to square, biased toward top
    pw, ph = photo.size
    side = min(pw, ph)
    left = (pw - side) // 2
    photo = photo.crop((left, 0, left + side, side)).resize((D, D), Image.LANCZOS)
    pmask = Image.new("L", (D, D), 0)
    ImageDraw.Draw(pmask).ellipse([0, 0, D, D], fill=255)
    img.paste(photo, (cx - D // 2, cy - D // 2), pmask)

# --- Text (left side) ---
x = 80
f_eyebrow = font("segoeuib.ttf", 26)
f_name = font("segoeuib.ttf", 92)
f_title = font("segoeuib.ttf", 46)
f_tag = font("segoeui.ttf", 27)
f_meta = font("segoeui.ttf", 24)

draw.text((x, 150), "PORTFOLIO", font=f_eyebrow, fill=C3)
draw.text((x, 188), "Aastha", font=f_name, fill=WHITE)
draw.text((x, 280), "Ojha", font=f_name, fill=WHITE)
draw.text((x, 392), "Lead Software Engineer", font=f_title, fill=C1)

tagline = "AI-driven development &"
tagline2 = "cloud architecture - 8+ yrs"
draw.text((x, 458), tagline, font=f_tag, fill=DIM)
draw.text((x, 492), tagline2, font=f_tag, fill=DIM)

draw.text((x, 545), "Bengaluru, India", font=f_meta, fill=DIM)

# bottom gradient accent bar
bar = linear_gradient((W, 10), [C1, C2, C3])
img.paste(bar, (0, H - 10))

out = os.path.join(HERE, "og-image.png")
img.save(out, "PNG")
print("saved", out, img.size)
