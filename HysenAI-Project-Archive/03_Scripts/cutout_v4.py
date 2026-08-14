"""
HysenAI Logo Cutout v4 — Color-distance matching approach.
Instead of brightness thresholding, directly match the three known text colors:
  - White:  (255, 255, 255)  for "Hysen" and "海森"
  - Orange: (242, 101, 34)   for "AI"
  - Blue:   (0, 120, 215)    for "智源"
Any pixel close to one of these colors = text (opaque).
Everything else = background (transparent).
This completely eliminates gradient background artifacts.
"""
from PIL import Image, ImageFilter
import math

INPUT = r"C:\Users\18747\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a7af05af72b40ccacc96f3a\hysenai-website\logo.png"
OUTPUT_CUTOUT = r"C:\Users\18747\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a7af05af72b40ccacc96f3a\hysenai-website\logo_cutout.png"
OUTPUT_WATERMARK = r"C:\Users\18747\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a7af05af72b40ccacc96f3a\hysenai-website\logo_watermark.png"

# Target text colors (sampled from logo description)
TARGET_COLORS = [
    (255, 255, 255),   # White text
    (242, 101, 34),    # Orange "AI"
    (0, 120, 215),     # Blue "智源"
    (230, 230, 230),   # Off-white (anti-aliased white edges)
    (220, 90, 30),     # Darker orange edges
    (0, 100, 190),     # Darker blue edges
]

# Distance threshold: pixels within this distance to any target color = text
# White text on dark bg has huge contrast, so threshold can be generous
OPAQUE_DIST = 80       # Within this distance = fully opaque
TRANSPARENT_DIST = 120 # Beyond this distance = fully transparent

print("Loading original logo...")
img = Image.open(INPUT).convert("RGBA")
width, height = img.size
print(f"Image size: {width}x{height}")

pixels = img.load()
result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
result_pixels = result.load()

print("Phase 1: Color-distance matching...")
for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        
        # Calculate minimum distance to any target color
        min_dist = float('inf')
        for tr, tg, tb in TARGET_COLORS:
            dist = math.sqrt((r - tr) ** 2 + (g - tg) ** 2 + (b - tb) ** 2)
            if dist < min_dist:
                min_dist = dist
        
        if min_dist <= OPAQUE_DIST:
            # Definitely text
            result_pixels[x, y] = (r, g, b, 255)
        elif min_dist >= TRANSPARENT_DIST:
            # Definitely background
            result_pixels[x, y] = (0, 0, 0, 0)
        else:
            # Transition zone — smooth alpha
            alpha = int((TRANSPARENT_DIST - min_dist) / (TRANSPARENT_DIST - OPAQUE_DIST) * 255)
            result_pixels[x, y] = (r, g, b, alpha)

print("Phase 2: Filling holes inside text (e.g., inside 'A', 'O', 'e')...")
# After removing background, there may be holes inside letters that were background-colored
# We need to fill these. Use a flood-fill from outside the text bbox to identify "true" background,
# then everything not reached by flood fill = text (including holes)

# Create a binary mask: 1 = transparent (background), 0 = non-transparent (text)
# We'll use a simple approach: dilate the text mask to fill small holes

r_chan, g_chan, b_chan, a_chan = result.split()

# Convert alpha to binary: text=255, bg=0
# Dilate to fill holes, then erode back
from PIL import ImageOps

# Create binary mask (text = white, bg = black)
binary = a_chan.point(lambda v: 255 if v > 50 else 0)

# Dilate (grow text) to fill holes
dilated = binary.filter(ImageFilter.MaxFilter(5))
# Erode back
eroded = dilated.filter(ImageFilter.MinFilter(5))
# One more dilate-erode cycle for thorough hole filling
dilated2 = eroded.filter(ImageFilter.MaxFilter(3))
filled = dilated2.filter(ImageFilter.MinFilter(3))

# Use filled mask as new alpha
for y in range(height):
    for x in range(width):
        old_alpha = result_pixels[x, y][3]
        new_mask = filled.getpixel((x, y))
        
        if new_mask > 0 and old_alpha == 0:
            # This was a hole inside text — fill with nearest text color
            # Just use white as it's inside letters
            result_pixels[x, y] = (255, 255, 255, 200)
        elif new_mask == 0 and old_alpha > 0:
            # This was removed by erosion — set to semi-transparent
            r, g, b = result_pixels[x, y][0], result_pixels[x, y][1], result_pixels[x, y][2]
            result_pixels[x, y] = (r, g, b, min(old_alpha, 128))

print("Phase 3: Removing any remaining dark semi-transparent pixels...")
for y in range(height):
    for x in range(width):
        r, g, b, a = result_pixels[x, y]
        if a > 0:
            max_rgb = max(r, g, b)
            # Kill any dark pixels that aren't part of the blue text
            # Blue text: B is high but R and G are low
            is_blue = (b > 100 and b > r + 50 and b > g + 30)
            if max_rgb < 60 and not is_blue:
                result_pixels[x, y] = (0, 0, 0, 0)

print("Phase 4: Edge smoothing...")
r_chan, g_chan, b_chan, a_chan = result.split()
a_blurred = a_chan.filter(ImageFilter.GaussianBlur(0.6))
result = Image.merge("RGBA", (r_chan, g_chan, b_chan, a_blurred))

print("Phase 5: Trimming transparent borders...")
bbox = result.getbbox()
if bbox:
    result = result.crop(bbox)
    print(f"Trimmed to: {result.size}")

# Save
result.save(OUTPUT_CUTOUT, "PNG")
print(f"Saved cutout: {OUTPUT_CUTOUT}")

# Watermark version (same image)
result.save(OUTPUT_WATERMARK, "PNG")
print(f"Saved watermark: {OUTPUT_WATERMARK}")

# Stats
total = result.size[0] * result.size[1]
transparent = 0
opaque = 0
for pixel in result.getdata():
    if pixel[3] == 0:
        transparent += 1
    elif pixel[3] > 200:
        opaque += 1
print(f"\nStats: {total} total, {transparent} transparent ({100*transparent//total}%), {opaque} opaque ({100*opaque//total}%)")
print("Done!")
