"""
Process logo.png to create:
1. A semi-transparent watermark version for page background
2. A clean transparent-background version for partner section
"""
from PIL import Image, ImageEnhance
import os

src = r"C:\Users\18747\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a7af05af72b40ccacc96f3a\hysenai-website\logo.png"
out_dir = r"C:\Users\18747\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a7af05af72b40ccacc96f3a\hysenai-website"

# Open original
img = Image.open(src).convert("RGBA")
w, h = img.size
print(f"Original size: {w}x{h}")

# --- 1. Watermark version (very faint, for background) ---
wm = img.copy()
# Reduce opacity to ~8% for subtle watermark
alpha = wm.split()[3]
alpha = alpha.point(lambda v: int(v * 0.08))
wm.putalpha(alpha)
wm.save(os.path.join(out_dir, "logo_watermark.png"))
print("Saved logo_watermark.png")

# --- 2. Partner section version (moderate opacity, clean) ---
partner = img.copy()
# Slightly reduce opacity for subtle display
alpha2 = partner.split()[3]
alpha2 = alpha2.point(lambda v: int(v * 0.85))
partner.putalpha(alpha2)
# Resize to reasonable partner logo size (height ~80px)
ratio = 80 / h
new_w = int(w * ratio)
partner_resized = partner.resize((new_w, 80), Image.LANCZOS)
partner_resized.save(os.path.join(out_dir, "logo_partner.png"))
print(f"Saved logo_partner.png ({new_w}x80)")

# --- 3. Nav version (small, height 36px) ---
nav = img.copy()
ratio_nav = 36 / h
new_w_nav = int(w * ratio_nav)
nav_resized = nav.resize((new_w_nav, 36), Image.LANCZOS)
nav_resized.save(os.path.join(out_dir, "logo_nav.png"))
print(f"Saved logo_nav.png ({new_w_nav}x36)")

print("All done!")
