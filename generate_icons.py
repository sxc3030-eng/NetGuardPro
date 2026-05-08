#!/usr/bin/env python3
"""
Generate NetGuard Pro suite icons — same style (green shield, orange border, dark bg)
with module-specific symbols. Outputs .ico + .png for each module.
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ICON_SIZE = 256
OUT_DIR = "sentinel/icons"

# Module definitions: (filename, symbol_lines, label)
# symbol_lines = list of drawing commands for the center symbol
MODULES = {
    "netguard":    {"label": "NetGuard Pro",   "symbol": "shield_lock"},
    "cleanguard":  {"label": "CleanGuard",     "symbol": "shield_scan"},
    "mailshield":  {"label": "MailShield",     "symbol": "shield_mail"},
    "vpnguard":    {"label": "VPN Guard",      "symbol": "shield_vpn"},
    "sentinel":    {"label": "SentinelOS",     "symbol": "shield_radar"},
    "mapper":      {"label": "Net Mapper",     "symbol": "shield_globe"},
    "fim":         {"label": "File Monitor",   "symbol": "shield_file"},
    "honeypot":    {"label": "HoneyPot",       "symbol": "shield_trap"},
    "strikeback":  {"label": "StrikeBack",     "symbol": "shield_sword"},
    "recorder":    {"label": "Recorder",       "symbol": "shield_rec"},
    "redteam":     {"label": "RedTeam",        "symbol": "shield_target"},
    "sandbox":     {"label": "Sandbox",        "symbol": "shield_box"},
    "mobile":      {"label": "Mobile GW",      "symbol": "shield_phone"},
    "help":        {"label": "Help Agent",     "symbol": "shield_help"},
}

# Colors matching the original icon
BG_DARK    = (15, 17, 23)
SHIELD_GREEN = (34, 139, 70)
SHIELD_GREEN_LIGHT = (46, 170, 90)
SHIELD_GREEN_DARK = (20, 100, 50)
BORDER_ORANGE = (230, 155, 30)
BORDER_RED    = (200, 60, 40)
GOLD       = (240, 180, 50)
WHITE      = (255, 255, 255)
CYAN_GLOW  = (0, 200, 220, 40)

def draw_rounded_rect(draw, xy, radius, fill):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0+radius, y0, x1-radius, y1], fill=fill)
    draw.rectangle([x0, y0+radius, x1, y1-radius], fill=fill)
    draw.pieslice([x0, y0, x0+2*radius, y0+2*radius], 180, 270, fill=fill)
    draw.pieslice([x1-2*radius, y0, x1, y0+2*radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1-2*radius, x0+2*radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1-2*radius, y1-2*radius, x1, y1], 0, 90, fill=fill)

def draw_shield(draw, cx, cy, w, h, fill_color, border_color, border_width=4):
    """Draw a shield shape centered at cx, cy with width w and height h"""
    # Shield as polygon
    hw, hh = w//2, h//2
    points = [
        (cx - hw, cy - hh + 20),      # top left
        (cx, cy - hh),                  # top center (peak)
        (cx + hw, cy - hh + 20),       # top right
        (cx + hw, cy + 10),            # right side
        (cx + hw - 10, cy + hh - 30),  # right lower
        (cx, cy + hh),                  # bottom point
        (cx - hw + 10, cy + hh - 30),  # left lower
        (cx - hw, cy + 10),            # left side
    ]
    # Border (larger)
    bw = border_width
    border_points = [
        (cx - hw - bw, cy - hh + 20 - bw),
        (cx, cy - hh - bw),
        (cx + hw + bw, cy - hh + 20 - bw),
        (cx + hw + bw, cy + 10 + bw),
        (cx + hw - 10 + bw, cy + hh - 30 + bw),
        (cx, cy + hh + bw),
        (cx - hw + 10 - bw, cy + hh - 30 + bw),
        (cx - hw - bw, cy + 10 + bw),
    ]
    draw.polygon(border_points, fill=border_color)
    draw.polygon(points, fill=fill_color)
    # Gradient effect — lighter top half
    for i in range(hh):
        alpha = max(0, 60 - i)
        if alpha > 0:
            y = cy - hh + 20 + i
            lx = cx - hw + (i * 10 // hh)
            rx = cx + hw - (i * 10 // hh)
            draw.line([(lx, y), (rx, y)], fill=(255, 255, 255, alpha))

def draw_cyber_bg(img, draw):
    """Draw dark cyber background with grid and glow dots"""
    # Dark gradient background
    for y in range(ICON_SIZE):
        r = int(10 + 8 * (y / ICON_SIZE))
        g = int(12 + 8 * (y / ICON_SIZE))
        b = int(20 + 10 * (y / ICON_SIZE))
        draw.line([(0, y), (ICON_SIZE, y)], fill=(r, g, b))

    # Subtle grid
    for x in range(0, ICON_SIZE, 20):
        draw.line([(x, 0), (x, ICON_SIZE)], fill=(255, 255, 255, 8), width=1)
    for y in range(0, ICON_SIZE, 20):
        draw.line([(0, y), (ICON_SIZE, y)], fill=(255, 255, 255, 8), width=1)

    # Glow dots at intersections
    import random
    random.seed(42)
    for _ in range(8):
        x = random.randint(10, ICON_SIZE-10)
        y = random.randint(10, ICON_SIZE-10)
        for r in range(6, 0, -1):
            alpha = int(15 * (6 - r))
            color_choice = random.choice([(0, 200, 180, alpha), (200, 150, 30, alpha), (0, 150, 255, alpha)])
            draw.ellipse([x-r, y-r, x+r, y+r], fill=color_choice)

def get_font(size):
    """Try to load a good font, fall back to default"""
    font_paths = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
    ]
    for fp in font_paths:
        try:
            return ImageFont.truetype(fp, size)
        except (IOError, OSError):
            pass
    return ImageFont.load_default()

def get_bold_font(size):
    font_paths = [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
    ]
    for fp in font_paths:
        try:
            return ImageFont.truetype(fp, size)
        except (IOError, OSError):
            pass
    return get_font(size)

# ── Symbol drawing functions ──────────────────────────────────────────────

def draw_lock(draw, cx, cy):
    """Lock icon (main NetGuard)"""
    # Lock body
    draw.rounded_rectangle([cx-18, cy-5, cx+18, cy+22], radius=4, fill=GOLD)
    draw.rounded_rectangle([cx-14, cy-1, cx+14, cy+18], radius=3, fill=(200, 140, 20))
    # Keyhole
    draw.ellipse([cx-5, cy+3, cx+5, cy+13], fill=SHIELD_GREEN_DARK)
    draw.polygon([(cx-3, cy+10), (cx+3, cy+10), (cx+1, cy+17), (cx-1, cy+17)], fill=SHIELD_GREEN_DARK)
    # Shackle
    draw.arc([cx-14, cy-30, cx+14, cy], 180, 360, fill=WHITE, width=5)
    # WiFi waves above
    for i, r in enumerate([35, 28, 20]):
        draw.arc([cx-r, cy-55-i*2, cx+r, cy-55+r-i*2], 220, 320, fill=WHITE, width=3)

def draw_scan(draw, cx, cy):
    """Scanner/virus scan icon (CleanGuard)"""
    # Magnifying glass
    draw.ellipse([cx-20, cy-22, cx+12, cy+10], outline=WHITE, width=4)
    draw.line([(cx+8, cy+6), (cx+24, cy+22)], fill=WHITE, width=5)
    # Checkmark inside
    draw.line([(cx-12, cy-6), (cx-4, cy+2), (cx+6, cy-14)], fill=(100, 255, 150), width=3)

def draw_mail(draw, cx, cy):
    """Email icon (MailShield)"""
    # Envelope body
    draw.rectangle([cx-24, cy-14, cx+24, cy+14], outline=WHITE, width=3, fill=(255,255,255,30))
    # Envelope flap (V shape)
    draw.line([(cx-24, cy-14), (cx, cy+4), (cx+24, cy-14)], fill=WHITE, width=3)
    # Lock on envelope
    draw.ellipse([cx-6, cy+2, cx+6, cy+14], fill=GOLD)
    draw.rectangle([cx-4, cy+6, cx+4, cy+14], fill=GOLD)

def draw_vpn(draw, cx, cy):
    """VPN tunnel icon"""
    # Tunnel shape
    draw.arc([cx-28, cy-18, cx+28, cy+18], 0, 180, fill=WHITE, width=3)
    draw.arc([cx-20, cy-12, cx+20, cy+12], 0, 180, fill=(200,200,200), width=2)
    # Key
    draw.ellipse([cx-8, cy-8, cx+8, cy+8], outline=GOLD, width=3)
    draw.line([(cx+8, cy), (cx+24, cy)], fill=GOLD, width=3)
    draw.line([(cx+20, cy), (cx+20, cy+6)], fill=GOLD, width=2)
    draw.line([(cx+16, cy), (cx+16, cy+5)], fill=GOLD, width=2)

def draw_radar(draw, cx, cy):
    """Radar/brain icon (Sentinel)"""
    # Radar circles
    for r in [24, 17, 10]:
        draw.arc([cx-r, cy-r, cx+r, cy+r], 0, 360, fill=WHITE, width=2)
    # Radar sweep line
    draw.line([(cx, cy), (cx+20, cy-16)], fill=(100, 255, 150), width=3)
    # Center dot
    draw.ellipse([cx-4, cy-4, cx+4, cy+4], fill=(100, 255, 150))
    # Blips
    draw.ellipse([cx+12, cy-14, cx+16, cy-10], fill=(255, 200, 50))
    draw.ellipse([cx-18, cy+6, cx-14, cy+10], fill=(255, 100, 100))

def draw_globe(draw, cx, cy):
    """Globe/network icon (Mapper)"""
    r = 22
    # Globe circle
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=WHITE, width=2)
    # Meridians
    draw.arc([cx-12, cy-r, cx+12, cy+r], 0, 360, fill=WHITE, width=1)
    draw.arc([cx-6, cy-r, cx+6, cy+r], 0, 360, fill=WHITE, width=1)
    # Equator + tropic
    draw.line([(cx-r, cy), (cx+r, cy)], fill=WHITE, width=1)
    draw.arc([cx-r, cy-8, cx+r, cy+8], 0, 360, fill=WHITE, width=1)
    # Network nodes
    for nx, ny in [(cx-16, cy-10), (cx+14, cy+8), (cx+8, cy-18)]:
        draw.ellipse([nx-3, ny-3, nx+3, ny+3], fill=(100, 255, 180))

def draw_file(draw, cx, cy):
    """File with checkmark (FIM)"""
    # File shape
    draw.polygon([(cx-16, cy-24), (cx+8, cy-24), (cx+18, cy-14), (cx+18, cy+24), (cx-16, cy+24)], outline=WHITE, width=2, fill=(255,255,255,20))
    # Fold corner
    draw.polygon([(cx+8, cy-24), (cx+18, cy-14), (cx+8, cy-14)], fill=(200,200,200,60))
    draw.line([(cx+8, cy-24), (cx+8, cy-14), (cx+18, cy-14)], fill=WHITE, width=2)
    # Checkmark
    draw.line([(cx-8, cy+4), (cx-2, cy+12), (cx+12, cy-4)], fill=(100, 255, 150), width=4)

def draw_trap(draw, cx, cy):
    """Honeypot trap icon"""
    # Pot shape
    draw.arc([cx-20, cy-8, cx+20, cy+8], 0, 180, fill=GOLD, width=3)
    draw.rectangle([cx-16, cy, cx+16, cy+18], fill=GOLD)
    draw.arc([cx-16, cy+12, cx+16, cy+24], 0, 180, fill=(200, 140, 20), width=0)
    draw.ellipse([cx-16, cy+12, cx+16, cy+24], fill=(200, 140, 20))
    # Honey drip
    draw.ellipse([cx-4, cy-14, cx+4, cy-6], fill=GOLD)
    draw.rectangle([cx-2, cy-10, cx+2, cy-2], fill=GOLD)
    # Spider web lines
    draw.line([(cx-24, cy-20), (cx-8, cy-8)], fill=(255,255,255,100), width=1)
    draw.line([(cx+24, cy-20), (cx+8, cy-8)], fill=(255,255,255,100), width=1)

def draw_sword(draw, cx, cy):
    """Sword/counter-attack (StrikeBack)"""
    # Sword blade
    draw.polygon([(cx-2, cy-28), (cx+2, cy-28), (cx+3, cy+4), (cx-3, cy+4)], fill=WHITE)
    draw.polygon([(cx, cy-28), (cx+2, cy-26), (cx, cy-24)], fill=(200,200,200))
    # Crossguard
    draw.rectangle([cx-14, cy+2, cx+14, cy+8], fill=GOLD)
    # Handle
    draw.rectangle([cx-4, cy+8, cx+4, cy+22], fill=(160, 100, 30))
    # Pommel
    draw.ellipse([cx-5, cy+20, cx+5, cy+28], fill=GOLD)
    # Lightning effect
    draw.line([(cx+10, cy-16), (cx+16, cy-6), (cx+12, cy-6), (cx+20, cy+6)], fill=(255, 220, 80), width=2)

def draw_rec(draw, cx, cy):
    """Recording dot (Recorder)"""
    # Outer ring
    draw.ellipse([cx-22, cy-22, cx+22, cy+22], outline=WHITE, width=3)
    # Inner red dot
    draw.ellipse([cx-12, cy-12, cx+12, cy+12], fill=(220, 40, 40))
    # Shine
    draw.ellipse([cx-6, cy-8, cx-2, cy-4], fill=(255, 100, 100))
    # Waveform lines
    for dx in [-28, -24, 28, 24]:
        h = 8 if abs(dx) == 24 else 14
        draw.line([(cx+dx, cy-h), (cx+dx, cy+h)], fill=WHITE, width=2)

def draw_target(draw, cx, cy):
    """Target/crosshair (RedTeam)"""
    # Concentric circles
    for r in [22, 15, 8]:
        color = (220, 50, 50) if r == 8 else WHITE
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=2)
    # Center dot
    draw.ellipse([cx-3, cy-3, cx+3, cy+3], fill=(220, 50, 50))
    # Crosshair lines
    draw.line([(cx, cy-28), (cx, cy-24)], fill=WHITE, width=2)
    draw.line([(cx, cy+24), (cx, cy+28)], fill=WHITE, width=2)
    draw.line([(cx-28, cy), (cx-24, cy)], fill=WHITE, width=2)
    draw.line([(cx+24, cy), (cx+28, cy)], fill=WHITE, width=2)

def draw_box(draw, cx, cy):
    """Sandbox box/cube"""
    # 3D cube - top face
    draw.polygon([(cx, cy-20), (cx+22, cy-8), (cx, cy+4), (cx-22, cy-8)], fill=(60, 160, 90), outline=WHITE, width=2)
    # Front-right face
    draw.polygon([(cx, cy+4), (cx+22, cy-8), (cx+22, cy+12), (cx, cy+24)], fill=(30, 120, 60), outline=WHITE, width=2)
    # Front-left face
    draw.polygon([(cx, cy+4), (cx-22, cy-8), (cx-22, cy+12), (cx, cy+24)], fill=(40, 140, 70), outline=WHITE, width=2)

def draw_phone(draw, cx, cy):
    """Mobile phone (Mobile Gateway)"""
    # Phone body
    draw.rounded_rectangle([cx-12, cy-24, cx+12, cy+24], radius=4, outline=WHITE, width=2, fill=(40,40,60))
    # Screen
    draw.rectangle([cx-9, cy-18, cx+9, cy+14], fill=(20, 80, 50))
    # Home button
    draw.ellipse([cx-4, cy+17, cx+4, cy+22], outline=WHITE, width=1)
    # WiFi on screen
    for i, r in enumerate([12, 8, 4]):
        draw.arc([cx-r, cy-12-i, cx+r, cy-12+r-i], 220, 320, fill=(100, 255, 150), width=2)
    # Shield mini on screen
    draw.ellipse([cx-3, cy+2, cx+3, cy+8], fill=(100, 255, 150))

def draw_help(draw, cx, cy):
    """Question mark (Help Agent)"""
    # Circle background
    draw.ellipse([cx-22, cy-22, cx+22, cy+22], outline=WHITE, width=3)
    # Question mark
    draw.arc([cx-12, cy-18, cx+12, cy+2], 180, 0, fill=WHITE, width=5)
    draw.line([(cx+12, cy-8), (cx+4, cy+2), (cx+4, cy+6)], fill=WHITE, width=5)
    # Dot
    draw.ellipse([cx-3, cy+12, cx+5, cy+18], fill=WHITE)

SYMBOL_FUNCS = {
    "shield_lock":   draw_lock,
    "shield_scan":   draw_scan,
    "shield_mail":   draw_mail,
    "shield_vpn":    draw_vpn,
    "shield_radar":  draw_radar,
    "shield_globe":  draw_globe,
    "shield_file":   draw_file,
    "shield_trap":   draw_trap,
    "shield_sword":  draw_sword,
    "shield_rec":    draw_rec,
    "shield_target": draw_target,
    "shield_box":    draw_box,
    "shield_phone":  draw_phone,
    "shield_help":   draw_help,
}


def generate_icon(name, module_info):
    """Generate a single module icon"""
    # Create RGBA image
    img = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")

    # Rounded rectangle background
    draw_rounded_rect(draw, (4, 4, ICON_SIZE-4, ICON_SIZE-4), 32, BG_DARK)

    # Cyber grid background
    for x in range(20, ICON_SIZE-4, 24):
        draw.line([(x, 8), (x, ICON_SIZE-8)], fill=(255, 255, 255, 6), width=1)
    for y in range(20, ICON_SIZE-4, 24):
        draw.line([(8, y), (ICON_SIZE-8, y)], fill=(255, 255, 255, 6), width=1)

    # Glow dots
    import random
    random.seed(hash(name) % 10000)
    for _ in range(6):
        gx = random.randint(20, ICON_SIZE-20)
        gy = random.randint(20, ICON_SIZE-50)
        gcolor = random.choice([
            (0, 180, 160), (200, 150, 30), (0, 140, 220), (50, 200, 100)
        ])
        for gr in range(8, 0, -1):
            alpha = int(10 * (8 - gr))
            draw.ellipse([gx-gr, gy-gr, gx+gr, gy+gr], fill=(*gcolor, alpha))

    cx, cy = ICON_SIZE // 2, ICON_SIZE // 2 - 16

    # Shield shadow
    shield_w, shield_h = 140, 150
    for si in range(6, 0, -1):
        alpha = int(20 * (6 - si))
        shadow_points = [
            (cx - shield_w//2 - si + 4, cy - shield_h//2 + 20 + si + 4),
            (cx + 4, cy - shield_h//2 + si + 4),
            (cx + shield_w//2 + si + 4, cy - shield_h//2 + 20 + si + 4),
            (cx + shield_w//2 + si + 4, cy + 10 + si + 4),
            (cx + shield_w//2 - 10 + si + 4, cy + shield_h//2 - 30 + si + 4),
            (cx + 4, cy + shield_h//2 + si + 4),
            (cx - shield_w//2 + 10 - si + 4, cy + shield_h//2 - 30 + si + 4),
            (cx - shield_w//2 - si + 4, cy + 10 + si + 4),
        ]
        draw.polygon(shadow_points, fill=(0, 0, 0, alpha))

    # Shield border (orange-red gradient effect)
    hw, hh = shield_w//2, shield_h//2
    border = 6
    border_points = [
        (cx - hw - border, cy - hh + 20 - border),
        (cx, cy - hh - border),
        (cx + hw + border, cy - hh + 20 - border),
        (cx + hw + border, cy + 10 + border),
        (cx + hw - 10 + border, cy + hh - 30 + border),
        (cx, cy + hh + border),
        (cx - hw + 10 - border, cy + hh - 30 + border),
        (cx - hw - border, cy + 10 + border),
    ]
    draw.polygon(border_points, fill=BORDER_ORANGE)

    # Inner orange border
    border2 = 3
    border2_points = [
        (cx - hw - border2, cy - hh + 20 - border2),
        (cx, cy - hh - border2),
        (cx + hw + border2, cy - hh + 20 - border2),
        (cx + hw + border2, cy + 10 + border2),
        (cx + hw - 10 + border2, cy + hh - 30 + border2),
        (cx, cy + hh + border2),
        (cx - hw + 10 - border2, cy + hh - 30 + border2),
        (cx - hw - border2, cy + 10 + border2),
    ]
    draw.polygon(border2_points, fill=(200, 80, 30))

    # Shield body (green)
    shield_points = [
        (cx - hw, cy - hh + 20),
        (cx, cy - hh),
        (cx + hw, cy - hh + 20),
        (cx + hw, cy + 10),
        (cx + hw - 10, cy + hh - 30),
        (cx, cy + hh),
        (cx - hw + 10, cy + hh - 30),
        (cx - hw, cy + 10),
    ]
    draw.polygon(shield_points, fill=SHIELD_GREEN)

    # Shield gradient — lighter green top
    for i in range(hh):
        alpha = max(0, 40 - i // 2)
        if alpha > 0:
            y = cy - hh + 20 + i
            progress = i / hh
            lx = int(cx - hw + progress * 12)
            rx = int(cx + hw - progress * 12)
            if y < cy + hh - 30:
                draw.line([(lx, y), (rx, y)], fill=(255, 255, 255, alpha))

    # Dark lower half of shield
    lower_points = [
        (cx - hw + 2, cy + 5),
        (cx + hw - 2, cy + 5),
        (cx + hw - 12, cy + hh - 32),
        (cx, cy + hh - 2),
        (cx - hw + 12, cy + hh - 32),
    ]
    draw.polygon(lower_points, fill=(20, 100, 50, 80))

    # Draw module-specific symbol
    sym_func = SYMBOL_FUNCS.get(module_info["symbol"])
    if sym_func:
        sym_func(draw, cx, cy)

    # Bottom label bar
    bar_y = ICON_SIZE - 48
    draw.rounded_rectangle([16, bar_y, ICON_SIZE-16, ICON_SIZE-12], radius=8, fill=BORDER_ORANGE)
    # Darker right half for "PRO" effect
    draw.rounded_rectangle([ICON_SIZE//2 + 10, bar_y, ICON_SIZE-16, ICON_SIZE-12], radius=8, fill=(40, 40, 50))

    # Label text
    label = module_info["label"]
    font = get_bold_font(20)
    font_small = get_bold_font(18)
    # Split into name + "Pro" or just name
    bbox = draw.textbbox((0, 0), label, font=font)
    tw = bbox[2] - bbox[0]
    tx = (ICON_SIZE - tw) // 2
    ty = bar_y + 6
    # Shadow
    draw.text((tx+1, ty+1), label, font=font, fill=(0, 0, 0, 180))
    draw.text((tx, ty), label, font=font, fill=WHITE)

    return img


def main():
    import os
    os.makedirs(OUT_DIR, exist_ok=True)

    for name, info in MODULES.items():
        print(f"[+] Generating {name}...")
        img = generate_icon(name, info)

        # Save PNG
        png_path = os.path.join(OUT_DIR, f"{name}.png")
        img.save(png_path, "PNG")

        # Save ICO (multiple sizes)
        ico_path = os.path.join(OUT_DIR, f"{name}.ico")
        sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        ico_images = []
        for sz in sizes:
            resized = img.resize(sz, Image.LANCZOS)
            ico_images.append(resized)
        ico_images[0].save(ico_path, format="ICO", sizes=[s for s in sizes], append_images=ico_images[1:])

        print(f"    -> {png_path}")
        print(f"    -> {ico_path}")

    # Also copy the main netguard icon to root
    import shutil
    main_ico = os.path.join(OUT_DIR, "netguard.ico")
    root_ico = "netguard_icon.ico"
    if os.path.exists(main_ico):
        shutil.copy2(main_ico, root_ico)
        print(f"\n[+] Main icon copied to {root_ico}")

    print(f"\n[OK] {len(MODULES)} icons generated in {OUT_DIR}/")


if __name__ == "__main__":
    main()
