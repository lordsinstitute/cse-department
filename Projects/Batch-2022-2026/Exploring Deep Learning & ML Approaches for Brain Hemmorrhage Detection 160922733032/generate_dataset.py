"""
Generate synthetic brain CT scan dataset for hemorrhage detection.
Creates grayscale images simulating brain CT scans:
- Normal: Brain-like elliptical structure with tissue textures
- Hemorrhage: Same structure with bright hemorrhage regions (bleeds)
"""
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFilter
import random
import shutil

DATASET_DIR = 'dataset'
IMG_SIZE = 224
TRAIN_COUNT = 400  # per class
TEST_COUNT = 100   # per class

random.seed(42)
np.random.seed(42)


def create_brain_base(size=IMG_SIZE):
    """Create a base brain CT-like image."""
    img = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(img)

    # Skull outline (bright ellipse)
    skull_margin = random.randint(15, 25)
    draw.ellipse(
        [skull_margin, skull_margin + 5, size - skull_margin, size - skull_margin + 5],
        fill=random.randint(180, 220)
    )

    # Brain tissue (darker interior)
    tissue_margin = skull_margin + random.randint(8, 14)
    draw.ellipse(
        [tissue_margin, tissue_margin + 3, size - tissue_margin, size - tissue_margin + 3],
        fill=random.randint(90, 130)
    )

    # Midline (vertical line through center)
    mid_x = size // 2 + random.randint(-2, 2)
    draw.line([(mid_x, tissue_margin + 10), (mid_x, size - tissue_margin - 10)],
              fill=random.randint(140, 165), width=2)

    # Ventricles (symmetric dark regions near center)
    vent_y = size // 2 + random.randint(-10, 5)
    vent_w = random.randint(12, 20)
    vent_h = random.randint(18, 28)
    # Left ventricle
    draw.ellipse([mid_x - vent_w - 8, vent_y - vent_h // 2,
                  mid_x - 8, vent_y + vent_h // 2],
                 fill=random.randint(40, 65))
    # Right ventricle
    draw.ellipse([mid_x + 8, vent_y - vent_h // 2,
                  mid_x + vent_w + 8, vent_y + vent_h // 2],
                 fill=random.randint(40, 65))

    # Add subtle gray matter variations
    for _ in range(random.randint(6, 12)):
        cx = random.randint(tissue_margin + 15, size - tissue_margin - 15)
        cy = random.randint(tissue_margin + 15, size - tissue_margin - 15)
        r = random.randint(8, 20)
        brightness = random.randint(75, 145)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=brightness)

    # Apply slight blur for realism
    img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(1.0, 2.0)))

    # Add noise
    arr = np.array(img, dtype=np.float32)
    noise = np.random.normal(0, random.uniform(3, 8), arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)

    return Image.fromarray(arr)


def add_hemorrhage(img):
    """Add hemorrhage regions (bright spots) to a brain CT image."""
    draw = ImageDraw.Draw(img)
    arr = np.array(img)

    num_bleeds = random.randint(1, 3)
    size = img.size[0]
    margin = 40

    for _ in range(num_bleeds):
        # Hemorrhage position (within brain area)
        cx = random.randint(margin, size - margin)
        cy = random.randint(margin, size - margin)

        bleed_type = random.choice(['subdural', 'intracerebral', 'subarachnoid'])

        if bleed_type == 'subdural':
            # Crescent-shaped along skull edge
            angle_start = random.randint(0, 360)
            r_outer = random.randint(70, 90)
            r_inner = random.randint(55, 68)
            for angle in range(angle_start, angle_start + random.randint(60, 120)):
                rad = np.radians(angle)
                for r in range(r_inner, r_outer):
                    px = int(size // 2 + r * np.cos(rad))
                    py = int(size // 2 + r * np.sin(rad))
                    if 0 <= px < size and 0 <= py < size:
                        brightness = random.randint(190, 255)
                        arr[py, px] = min(255, max(arr[py, px], brightness))

        elif bleed_type == 'intracerebral':
            # Irregular bright blob within brain tissue
            rx = random.randint(12, 30)
            ry = random.randint(12, 30)
            brightness = random.randint(200, 255)
            draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=brightness)
            # Add irregular edges
            for _ in range(random.randint(3, 7)):
                ox = cx + random.randint(-rx, rx)
                oy = cy + random.randint(-ry, ry)
                sr = random.randint(4, 12)
                draw.ellipse([ox - sr, oy - sr, ox + sr, oy + sr],
                             fill=random.randint(180, 250))

        else:  # subarachnoid
            # Bright streaks in sulci
            for _ in range(random.randint(3, 6)):
                sx = cx + random.randint(-25, 25)
                sy = cy + random.randint(-25, 25)
                ex = sx + random.randint(-15, 15)
                ey = sy + random.randint(-15, 15)
                draw.line([(sx, sy), (ex, ey)],
                          fill=random.randint(200, 255),
                          width=random.randint(2, 5))

    # Merge drawn and array modifications
    img_arr = np.maximum(np.array(img), arr)
    result = Image.fromarray(img_arr)
    result = result.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.5, 1.2)))

    return result


def generate_dataset():
    """Generate full dataset with train/test split."""
    # Clean previous dataset
    if os.path.exists(DATASET_DIR):
        shutil.rmtree(DATASET_DIR)

    splits = {'train': TRAIN_COUNT, 'test': TEST_COUNT}
    classes = ['normal', 'hemorrhage']

    for split, count in splits.items():
        for cls in classes:
            dir_path = os.path.join(DATASET_DIR, split, cls)
            os.makedirs(dir_path, exist_ok=True)

    total = sum(splits.values()) * 2
    generated = 0

    for split, count in splits.items():
        for i in range(count):
            # Normal image
            normal_img = create_brain_base()
            normal_path = os.path.join(DATASET_DIR, split, 'normal', f'normal_{split}_{i:04d}.png')
            normal_img.save(normal_path)
            generated += 1

            # Hemorrhage image
            hemorrhage_img = create_brain_base()
            hemorrhage_img = add_hemorrhage(hemorrhage_img)
            hemorrhage_path = os.path.join(DATASET_DIR, split, 'hemorrhage', f'hemorrhage_{split}_{i:04d}.png')
            hemorrhage_img.save(hemorrhage_path)
            generated += 1

            if generated % 100 == 0:
                print(f'  Generated {generated}/{total} images...')

    # Also create a few test sample images for easy testing
    sample_dir = os.path.join('static', 'test_samples')
    os.makedirs(sample_dir, exist_ok=True)

    for i in range(3):
        normal = create_brain_base()
        normal.save(os.path.join(sample_dir, f'sample_normal_{i+1}.png'))
        hemorrhage = create_brain_base()
        hemorrhage = add_hemorrhage(hemorrhage)
        hemorrhage.save(os.path.join(sample_dir, f'sample_hemorrhage_{i+1}.png'))

    print(f'\nDataset generated successfully!')
    print(f'  Train: {TRAIN_COUNT} normal + {TRAIN_COUNT} hemorrhage = {TRAIN_COUNT*2}')
    print(f'  Test:  {TEST_COUNT} normal + {TEST_COUNT} hemorrhage = {TEST_COUNT*2}')
    print(f'  Test samples: 3 normal + 3 hemorrhage in static/test_samples/')


if __name__ == '__main__':
    print('Generating Brain CT Scan Dataset...')
    generate_dataset()
