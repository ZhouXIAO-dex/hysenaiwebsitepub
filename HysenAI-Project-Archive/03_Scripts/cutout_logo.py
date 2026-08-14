"""
Extract HysenAI logo from logo.png by removing the dark background.
Keep only the text/colored content (white, orange, blue).
"""
from PIL import Image
import os

src = r"C:\Users\18747\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a7af05af72b40ccacc96f3a\hysenai-website\logo.png"
out_dir = r"C:\Users\18747\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a7af05af72b40ccacc96f3a\hysenai-website"

img = Image.open(src).convert("RGBA")
w, h = img.size
print(f"Original: {w}x{h}")

# Create a new image with transparent background
result = Image.new("RGBA", (w, h), (0, 0, 0, 0))
pixels = img.load()
result_pixels = result.load()

# Threshold for detecting dark background pixels
# Background is roughly #1a1a1a to #0d0d0d (R,G,B all < 40)
# Text is white (R,G,B > 200), orange (#f26522), blue (#2e7de4)
threshold = 45

for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        # If pixel is bright enough (not background), keep it
        # Background has all RGB values very low (< ~40)
        max_rgb = max(r, g, b)
        if max_rgb > threshold:
            # This is content (text/logo), keep it
            # But also reduce any remaining background tint
            result_pixels[x, y] = (r, g, b, 255)
        else:
            # This is background, make transparent
            # But for edge pixels (semi-dark), give partial transparency for smooth edges
            if max_rgb > 20:
                alpha = int((max_rgb - 20) / (threshold - 20) * 255)
                result_pixels[x, y] = (r, g, b, alpha)
            # else: fully transparent (default)

# Save the cutout version
result.save(os.path.join(out_dir, "logo_cutout.png"))
print("Saved logo_cutout.png (transparent background)")

# Also create a resized version for nav (height 36px)
ratio_nav = 36 / h
new_w_nav = int(w * ratio_nav)
nav_version = result.resize((new_w_nav, 36), Image.LANCZOS)
nav_version.save(os.path.join(out_dir, "logo_nav.png"))
print(f"Saved logo_nav.png ({new_w_nav}x36)")

# Create watermark version from cutout (very faint)
wm = result.copy()
alpha = wm.split()[3]
alpha = alpha.point(lambda v: int(v * 0.08))
wm.putalpha(alpha)
wm.save(os.path.join(out_dir, "logo_watermark.png"))
print("Saved logo_watermark.png (from cutout)")

# Create footer version (height 50px)
ratio_footer = 50 / h
new_w_footer = int(w * ratio_footer)
footer_version = result.resize((new_w_footer, 50), Image.LANCZOS)
footer_version.save(os.path.join(out_dir, "logo_footer.png"))
print(f"Saved logo_footer.png ({new_w_footer}x50)")

print("All done!")
