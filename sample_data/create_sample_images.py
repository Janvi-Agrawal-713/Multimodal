"""
Generates high-contrast sample test images for Safety/PPE audit and Concrete Crack diagnostics.
Ensures the app has ready-to-test demonstration assets out of the box.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def generate_sample_assets(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Sample Construction Site PPE Image
    img_site = Image.new("RGB", (900, 600), color=(140, 150, 160)) # Concrete backdrop
    draw = ImageDraw.Draw(img_site)
    
    # Draw scaffolding steel beams
    for x in range(50, 850, 150):
        draw.line([(x, 50), (x, 550)], fill=(70, 75, 80), width=8)
    for y in range(150, 550, 120):
        draw.line([(50, y), (850, y)], fill=(70, 75, 80), width=6)
        # diagonal cross bracing
        draw.line([(50, y), (200, y + 120)], fill=(100, 105, 110), width=4)
        draw.line([(200, y), (50, y + 120)], fill=(100, 105, 110), width=4)
        draw.line([(200, y), (350, y + 120)], fill=(100, 105, 110), width=4)
        draw.line([(350, y), (200, y + 120)], fill=(100, 105, 110), width=4)
        draw.line([(350, y), (500, y + 120)], fill=(100, 105, 110), width=4)
        draw.line([(500, y), (350, y + 120)], fill=(100, 105, 110), width=4)

    # Ground slab
    draw.rectangle([(0, 480), (900, 600)], fill=(110, 115, 120))
    
    # Worker 1 (Ground level - fully compliant)
    # Head & Yellow Safety Helmet
    draw.ellipse([(220, 260), (280, 320)], fill=(220, 180, 150))
    draw.pieslice([(210, 240), (290, 310)], 180, 360, fill=(255, 215, 0), outline=(200, 160, 0), width=3) # Yellow helmet
    # High-vis fluorescent orange/neon vest
    draw.rectangle([(215, 320), (285, 430)], fill=(255, 102, 0)) # Orange vest
    # Silver reflective stripes
    draw.rectangle([(220, 340), (280, 355)], fill=(230, 240, 250))
    draw.rectangle([(220, 385), (280, 400)], fill=(230, 240, 250))
    # Work pants & heavy safety boots
    draw.rectangle([(220, 430), (245, 510)], fill=(40, 60, 90))
    draw.rectangle([(255, 430), (280, 510)], fill=(40, 60, 90))
    draw.rectangle([(215, 510), (248, 530)], fill=(30, 30, 30)) # Boots
    draw.rectangle([(252, 510), (285, 530)], fill=(30, 30, 30))
    
    # Worker 2 (Scaffolding level - with white helmet & high-vis vest)
    draw.ellipse([(520, 160), (570, 210)], fill=(210, 175, 145))
    draw.pieslice([(515, 145), (575, 205)], 180, 360, fill=(245, 245, 250), outline=(180, 180, 180), width=2) # White helmet
    draw.rectangle([(515, 210), (575, 300)], fill=(50, 205, 50)) # Neon green vest
    draw.rectangle([(520, 230), (570, 245)], fill=(230, 240, 250))
    draw.rectangle([(520, 300), (542, 380)], fill=(50, 50, 60))
    draw.rectangle([(548, 300), (570, 380)], fill=(50, 50, 60))
    draw.rectangle([(516, 380), (545, 395)], fill=(30, 30, 30))
    draw.rectangle([(546, 380), (574, 395)], fill=(30, 30, 30))
    
    # Caution Signboard & Banner
    draw.rectangle([(680, 420), (840, 520)], fill=(255, 220, 0), outline=(30, 30, 30), width=3)
    draw.text((700, 440), "SAFETY FIRST", fill=(0, 0, 0))
    draw.text((695, 470), "HARD HAT AREA", fill=(0, 0, 0))
    
    site_path = os.path.join(output_dir, "sample_construction_site.jpg")
    img_site.save(site_path, "JPEG", quality=92)

    # 2. Sample Concrete Surface with Diagonal Shear Crack
    img_crack = Image.new("RGB", (800, 600), color=(185, 185, 185))
    draw_c = ImageDraw.Draw(img_crack)
    
    # Draw subtle concrete texture mottling
    import random
    random.seed(42)
    for _ in range(3000):
        rx = random.randint(0, 799)
        ry = random.randint(0, 599)
        shade = random.randint(160, 210)
        draw_c.point((rx, ry), fill=(shade, shade, shade))
        
    # Draw primary diagonal shear crack line (meandering from top-left to mid-right)
    crack_points = [
        (120, 60), (145, 95), (170, 130), (200, 180), (240, 225),
        (280, 260), (320, 305), (370, 340), (410, 380), (460, 430),
        (510, 470), (560, 510), (620, 555)
    ]
    # Primary fissure
    draw_c.line(crack_points, fill=(45, 45, 45), width=5)
    # Secondary shadow edge
    shadow_points = [(x + 2, y + 1) for x, y in crack_points]
    draw_c.line(shadow_points, fill=(90, 90, 90), width=2)
    
    # Branching secondary micro-cracks
    draw_c.line([(280, 260), (310, 230), (345, 215)], fill=(65, 65, 65), width=2)
    draw_c.line([(410, 380), (440, 360), (480, 350)], fill=(65, 65, 65), width=2)
    draw_c.line([(370, 340), (390, 385), (405, 420)], fill=(70, 70, 70), width=2)
    
    # Efflorescence (calcium deposit stain) around crack zone
    for _ in range(800):
        ex = random.randint(250, 450)
        ey = random.randint(280, 410)
        draw_c.point((ex, ey), fill=(235, 235, 240))
        
    draw_c.text((20, 565), "SURFACE: Reinforced Concrete Shear Wall (Grid C-3)", fill=(80, 80, 80))
    
    crack_path = os.path.join(output_dir, "sample_concrete_crack.jpg")
    img_crack.save(crack_path, "JPEG", quality=92)
    
    return site_path, crack_path

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    generate_sample_assets(current_dir)
    print("Sample assets successfully generated.")
