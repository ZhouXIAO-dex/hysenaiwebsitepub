"""
Improved logo cutout: sample background color from corners, 
use color distance to separate text from background.
"""
from PIL import Image, ImageFilter
import os
import math

src = r"C:\Users\18747\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a7af05af72b40ccacc96f3a\hysenai-website\logo.png"
out_dir = r"C:\Users\18747\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a7af05af72b40ccacc96f3a\hysenai-website"

img = Image.open(src).convert("RGBA")
w, h = img.size
print(f"Original: {w}x{h}")

pixels = img.load()

# Step 1: Sample background color from 4 corners (50x50 area each)
corners = []
for cx, cy in [(0,0), (w-1,0), (0,h-1), (w-1,h-1)]:
    r_sum, g_sum, b_sum, count = 0, 0, 0, 0
    for dx in range(-25, 25):
        for dy in range(-25, 25):
            x = max(0, min(w-1, cx+dx))
            y = max(0, min(h-1, cy+dy))
            r, g, b, a = pixels[x, y]
            r_sum += r
            g_sum += g
            b_sum += b
            count += 1
    corners.append((r_sum//count, g_sum//count, b_sum//count))

# Average background color
bg_r = sum(c[0] for c in corners) // 4
bg_g = sum(c[1] for c in corners) // 4
bg_b = sum(c[2] for c in corners) // 4
print(f"Background color: ({bg_r}, {bg_g}, {bg_b})")

# Step 2: For each pixel, calculate color distance from background
# If distance is small -> background -> transparent
# If distance is large -> text -> keep
result = Image.new("RGBA", (w, h), (0, 0, 0, 0))
result_pixels = result.load()

# Threshold: pixels with color distance > this are text
DISTANCE_THRESHOLD = 60

for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        
        # Calculate Euclidean distance from background color
        dist = math.sqrt((r - bg_r)**2 + (g - bg_g)**2 + (b - bg_b)**2)
        
        if dist > DISTANCE_THRESHOLD:
            # This is text content - keep it fully opaque
            result_pixels[x, y] = (r, g, b, 255)
        elif dist > DISTANCE_THRESHOLD * 0.5:
            # Edge pixel - semi-transparent for smooth edges
            alpha = int((dist - DISTANCE_THRESHOLD * 0.5) / (DISTANCE_THRESHOLD * 0.5) * 255)
            result_pixels[x, y] = (r, g, b, alpha)
        # else: background -> stays transparent

# Step 3: Apply slight edge smoothing
result = result.filter(ImageFilter.ModeFilter(size=3))

# Save
result.save(os.path.join(out_dir, "logo_cutout.png"))
print("Saved logo_cutout.png (improved cutout)")

# Nav version (height 42px)
ratio_nav = 42 / h
new_w_nav = int(w * ratio_nav)
result.resize((new_w_nav, 42), Image.LANCZOS).save(os.path.join(out_dir, "logo_nav.png"))
print(f"Saved logo_nav.png ({new_w_nav}x42)")

# Footer version (height 50px)
ratio_ft = 50 / h
new_w_ft = int(w * ratio_ft)
result.resize((new_w_ft, 50), Image.LANCZOS).save(os.path.join(out_dir, "logo_footer.png"))
print(f"Saved logo_footer.png ({new_w_ft}x50)")

# Watermark (8% opacity)
wm = result.copy()
alpha_ch = wm.split()[3]
alpha_ch = alpha_ch.point(lambda v: int(v * 0.08))
wm.putalpha(alpha_ch)
wm.save(os.path.join(out_dir, "logo_watermark.png"))
print("Saved logo_watermark.png")

print("Done!")
