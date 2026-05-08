#!/usr/bin/env python3
"""
Generate Microsoft Store assets from the main NetGuard Pro icon.
Creates all required sizes for Store submission.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

OUT = os.path.dirname(os.path.abspath(__file__))
ICON_SRC = os.path.join(os.path.dirname(OUT), "netguard_icon.png")

def create_store_icon(size, name, bg_color=None):
    """Create a Store icon at given size with optional background."""
    src = Image.open(ICON_SRC).convert("RGBA")

    if bg_color:
        # Create background
        canvas = Image.new("RGBA", (size, size), bg_color)
        # Scale icon to 80% of canvas
        icon_size = int(size * 0.8)
        resized = src.resize((icon_size, icon_size), Image.LANCZOS)
        offset = (size - icon_size) // 2
        canvas.paste(resized, (offset, offset), resized)
        result = canvas
    else:
        result = src.resize((size, size), Image.LANCZOS)

    path = os.path.join(OUT, name)
    result.save(path, "PNG")
    print(f"  [OK] {name} ({size}x{size})")
    return path


def create_feature_graphic():
    """Create a 1920x1080 feature/hero graphic for the Store."""
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), "#0a0a12")
    draw = ImageDraw.Draw(img)

    # Dark cyber gradient background
    for y in range(H):
        r = int(10 + (y / H) * 12)
        g = int(10 + (y / H) * 10)
        b = int(18 + (y / H) * 20)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Grid pattern
    for x in range(0, W, 60):
        draw.line([(x, 0), (x, H)], fill=(255, 255, 255, 8), width=1)
    for y in range(0, H, 60):
        draw.line([(0, y), (W, y)], fill=(255, 255, 255, 8), width=1)

    # Central icon
    icon = Image.open(ICON_SRC).convert("RGBA").resize((300, 300), Image.LANCZOS)
    icon_x = (W - 300) // 2
    icon_y = 180
    img.paste(icon, (icon_x, icon_y), icon)

    # Glow behind icon
    glow = Image.new("RGBA", (500, 500), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([50, 50, 450, 450], fill=(61, 255, 180, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    img_rgba = img.convert("RGBA")
    img_rgba.paste(glow, (W//2 - 250, icon_y - 100), glow)
    img = img_rgba.convert("RGB")

    # Title text
    try:
        title_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 72)
        sub_font = ImageFont.truetype("C:/Windows/Fonts/segoeuil.ttf", 32)
        small_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        sub_font = title_font
        small_font = title_font

    # "NETGUARD PRO"
    title = "NETGUARD PRO"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 520), title, fill=(61, 255, 180), font=title_font)

    # Subtitle
    subtitle = "Suite de cybersecurite tout-en-un pour Windows"
    bbox2 = draw.textbbox((0, 0), subtitle, font=sub_font)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W - tw2) // 2, 610), subtitle, fill=(200, 200, 220), font=sub_font)

    # Feature bullets
    features = [
        "IDS/IPS en temps reel",
        "Pare-feu intelligent",
        "Carte mondiale des menaces",
        "VPN WireGuard integre",
        "Anti-malware & Honeypot",
        "14 modules de securite"
    ]
    start_y = 700
    cols = 3
    col_w = W // cols
    for i, feat in enumerate(features):
        col = i % cols
        row = i // cols
        x = col * col_w + col_w // 2
        y = start_y + row * 50
        # Green dot
        draw.ellipse([x - 120, y + 6, x - 108, y + 18], fill=(61, 255, 180))
        draw.text((x - 100, y), feat, fill=(220, 220, 230), font=small_font)

    # Version
    draw.text((W - 180, H - 40), "v3.0.0", fill=(100, 100, 120), font=small_font)

    path = os.path.join(OUT, "store_hero_1920x1080.png")
    img.save(path, "PNG", quality=95)
    print(f"  [OK] store_hero_1920x1080.png")


print("=== Generating Microsoft Store Assets ===\n")

# Required Store icons
print("[1] Store Icons:")
create_store_icon(300, "StoreLogo_300x300.png")
create_store_icon(150, "StoreLogo_150x150.png")
create_store_icon(50, "StoreLogo_50x50.png")
create_store_icon(44, "AppIcon_44x44.png")
create_store_icon(71, "SmallTile_71x71.png")
create_store_icon(150, "MediumTile_150x150.png")
create_store_icon(310, "WideTile_310x150.png", "#0a0a12")  # wide with bg
create_store_icon(310, "LargeTile_310x310.png", "#0a0a12")

print("\n[2] Hero/Feature Graphic:")
create_feature_graphic()

print(f"\n=== All assets saved to {OUT} ===")
