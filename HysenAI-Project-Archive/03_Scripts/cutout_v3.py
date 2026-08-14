"""
HysenAI Logo Cutout v3 — Precise background removal using HSV brightness channel.
The original logo has: dark background (low brightness) + white/orange/blue text (high brightness).
Strategy: Use V (brightness) channel to cleanly separate text from background.
"""
from PIL import Image, ImageFilter
import colorsys
import math

INPUT = r"C:\Users\18747\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a7af05af72b40ccacc96f3a\hysenai-website\logo.png"
OUTPUT_CUTOUT = r"C:\Users\18747\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a7af05af72b40ccacc96f3a\hysenai-website\logo_cutout.png"
OUTPUT_WATERMARK = r"C:\Users\18747\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a7af05af72b40ccacc96f3a\hysenai-website\logo_watermark.png"

print("Loading original logo...")
img = Image.open(INPUT).convert("RGBA")
width, height = img.size
print(f"Image size: {width}x{height}")

pixels = img.load()
result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
result_pixels = result.load()

# Phase 1: HSV-based background removal
# Background is dark: V < 35
# Text is bright: V > 60 (white=255, orange=~200, blue=~140)
# Transition zone: 35-60 for smooth edges

LOW_THRESH = 30   # Below this V = fully transparent (background)
HIGH_THRESH = 65  # Above this V = fully opaque (text)

print("Phase 1: HSV brightness-based background removal...")
for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        
        # Convert to HSV
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        v_int = int(v * 255)
        
        if v_int >= HIGH_THRESH:
            # Definitely text — keep full opacity
            result_pixels[x, y] = (r, g, b, 255)
        elif v_int <= LOW_THRESH:
            # Definitely background — transparent
            result_pixels[x, y] = (r, g, b, 0)
        else:
            # Transition zone — smooth alpha based on brightness
            alpha = int((v_int - LOW_THRESH) / (HIGH_THRESH - LOW_THRESH) * 255)
            result_pixels[x, y] = (r, g, b, alpha)

# Phase 2: Edge cleanup — remove isolated dark pixels near edges
print("Phase 2: Edge cleanup and artifact removal...")
# Create an alpha-only image for morphology
alpha_img = result.split()[3]  # Alpha channel

# Dilate then erode to fill small holes in text
dilated = alpha_img.filter(ImageFilter.MaxFilter(3))
eroded = dilated.filter(ImageFilter.MinFilter(3))

# Get cleaned alpha
cleaned_alpha = eroded

# Rebuild result with cleaned alpha but original RGB
for y in range(height):
    for x in range(width):
        r, g, b, old_alpha = result_pixels[x, y]
        new_alpha = cleaned_alpha.getpixel((x, y))
        
        if new_alpha == 0:
            result_pixels[x, y] = (0, 0, 0, 0)
        elif old_alpha == 0 and new_alpha > 0:
            # This pixel was background but is now text (filled hole)
            # Use a neutral color based on neighbors
            result_pixels[x, y] = (r, g, b, new_alpha)
        else:
            result_pixels[x, y] = (r, g, b, new_alpha)

# Phase 3: Remove residual dark pixels that are semi-transparent
# (these are the corner artifacts the user complained about)
print("Phase 3: Removing residual dark artifacts...")
for y in range(height):
    for x in range(width):
        r, g, b, a = result_pixels[x, y]
        if a > 0:
            # If this pixel is dark (all channels low) and semi-transparent, kill it
            max_rgb = max(r, g, b)
            if max_rgb < 50 and a < 200:
                result_pixels[x, y] = (0, 0, 0, 0)
            # If pixel is dark and was kept, reduce its alpha significantly
            elif max_rgb < 50:
                result_pixels[x, y] = (r, g, b, int(a * 0.1))

# Phase 4: Slight blur on alpha for smoother edges
print("Phase 4: Edge smoothing...")
# Split channels
r_chan, g_chan, b_chan, a_chan = result.split()
# Light Gaussian blur on alpha only
a_blurred = a_chan.filter(ImageFilter.GaussianBlur(0.8))
result = Image.merge("RGBA", (r_chan, g_chan, b_chan, a_blurred))

# Trim transparent borders
print("Phase 5: Trimming transparent borders...")
bbox = result.getbbox()
if bbox:
    result = result.crop(bbox)
    print(f"Trimmed to: {result.size}")
else:
    print("WARNING: No content found after trimming!")

# Save cutout
result.save(OUTPUT_CUTOUT, "PNG")
print(f"Saved cutout: {OUTPUT_CUTOUT}")

# Create watermark version (same as cutout, just for reference)
result.save(OUTPUT_WATERMARK, "PNG")
print(f"Saved watermark: {OUTPUT_WATERMARK}")

# Stats
total_pixels = result.size[0] * result.size[1]
transparent = sum(1 for pixel in result.getdata() if pixel[3] == 0)
opaque = sum(1 for pixel in result.getdata() if pixel[3] > 200)
print(f"\nStats: {total_pixels} total pixels, {transparent} transparent ({100*transparent//total_pixels}%), {opaque} opaque ({100*opaque//total_pixels}%)")
print("Done!")
