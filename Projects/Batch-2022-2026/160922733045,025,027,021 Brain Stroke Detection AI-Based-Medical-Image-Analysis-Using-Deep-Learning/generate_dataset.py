"""
Generate synthetic brain CT scan images for stroke detection training.
Creates normal brain CTs and stroke CTs (ischemic dark patches, midline shift).
"""

import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'Dataset')
SAMPLES_DIR = os.path.join(BASE_DIR, 'static', 'test_samples')
IMG_SIZE = 224


def create_brain_base(size=IMG_SIZE):
    """Create a realistic-looking normal brain CT base image."""
    img = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(img)

    cx, cy = size // 2, size // 2

    # Skull outline (bright ellipse)
    skull_brightness = random.randint(180, 220)
    skull_rx, skull_ry = size // 2 - 8, size // 2 - 6
    draw.ellipse(
        [cx - skull_rx, cy - skull_ry, cx + skull_rx, cy + skull_ry],
        fill=skull_brightness
    )

    # Brain tissue (gray fill inside skull)
    brain_brightness = random.randint(90, 130)
    brain_rx, brain_ry = skull_rx - 10, skull_ry - 10
    draw.ellipse(
        [cx - brain_rx, cy - brain_ry, cx + brain_rx, cy + brain_ry],
        fill=brain_brightness
    )

    # Midline (falx cerebri) - vertical line
    midline_brightness = random.randint(140, 165)
    midline_width = random.randint(2, 3)
    draw.line(
        [(cx, cy - brain_ry + 5), (cx, cy + brain_ry - 5)],
        fill=midline_brightness, width=midline_width
    )

    # Ventricles (dark CSF-filled cavities)
    vent_brightness = random.randint(40, 65)
    vent_w = random.randint(8, 14)
    vent_h = random.randint(18, 28)
    vent_offset = random.randint(12, 20)
    # Left ventricle
    draw.ellipse(
        [cx - vent_offset - vent_w, cy - vent_h // 2,
         cx - vent_offset + vent_w, cy + vent_h // 2],
        fill=vent_brightness
    )
    # Right ventricle
    draw.ellipse(
        [cx + vent_offset - vent_w, cy - vent_h // 2,
         cx + vent_offset + vent_w, cy + vent_h // 2],
        fill=vent_brightness
    )

    # Gray matter variations (random patches)
    num_patches = random.randint(6, 14)
    for _ in range(num_patches):
        px = cx + random.randint(-brain_rx + 15, brain_rx - 15)
        py = cy + random.randint(-brain_ry + 15, brain_ry - 15)
        pr = random.randint(5, 15)
        pb = random.randint(75, 145)
        draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=pb)

    # Apply gaussian blur for soft tissue appearance
    blur_radius = random.uniform(1.0, 2.0)
    img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    # Add noise
    arr = np.array(img, dtype=np.float32)
    noise = np.random.normal(0, random.uniform(3, 8), arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr)

    return img


def add_stroke(img):
    """Add stroke indicators to a brain CT image.

    Stroke appears as:
    1. Ischemic: dark hypodense patches (blocked blood flow -> tissue death)
    2. Midline shift: pressure pushes midline to opposite side
    3. Optional hemorrhagic transformation: small bright spots within dark zone
    """
    draw = ImageDraw.Draw(img)
    size = img.size[0]
    cx, cy = size // 2, size // 2

    # Choose which hemisphere is affected
    affected_side = random.choice(['left', 'right'])
    sign = -1 if affected_side == 'left' else 1

    # 1. Ischemic dark patch (main stroke indicator)
    # Large irregular dark region in one hemisphere
    num_patches = random.randint(2, 4)
    base_x = cx + sign * random.randint(25, 55)
    base_y = cy + random.randint(-30, 20)

    for _ in range(num_patches):
        px = base_x + random.randint(-20, 20)
        py = base_y + random.randint(-20, 20)
        rx = random.randint(12, 30)
        ry = random.randint(10, 25)
        # Dark patch (hypodense - dead tissue)
        darkness = random.randint(30, 60)
        draw.ellipse([px - rx, py - ry, px + rx, py + ry], fill=darkness)

    # 2. Subtle midline shift (pressure effect)
    if random.random() < 0.7:
        shift = sign * random.randint(3, 8)  # Shift away from affected side
        midline_brightness = random.randint(140, 165)
        brain_ry = size // 2 - 16
        draw.line(
            [(cx - shift, cy - brain_ry + 10), (cx - shift, cy + brain_ry - 10)],
            fill=midline_brightness, width=random.randint(2, 3)
        )

    # 3. Sulcal effacement - reduced contrast in affected area
    if random.random() < 0.5:
        for _ in range(random.randint(3, 6)):
            ex = base_x + random.randint(-25, 25)
            ey = base_y + random.randint(-25, 25)
            er = random.randint(5, 12)
            # Slightly darker than normal tissue
            draw.ellipse([ex - er, ey - er, ex + er, ey + er],
                         fill=random.randint(50, 75))

    # 4. Optional hemorrhagic transformation (bright spot within dark zone)
    if random.random() < 0.3:
        hx = base_x + random.randint(-10, 10)
        hy = base_y + random.randint(-10, 10)
        hr = random.randint(4, 8)
        draw.ellipse([hx - hr, hy - hr, hx + hr, hy + hr],
                     fill=random.randint(200, 255))

    # Re-blur to blend
    img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.8, 1.5)))

    return img


def generate_images(output_dir, label, count):
    """Generate a set of brain CT images."""
    os.makedirs(output_dir, exist_ok=True)
    for i in range(count):
        img = create_brain_base()
        if label == 'stroke':
            img = add_stroke(img)
        # Convert to RGB for consistency with upload handling
        img_rgb = Image.new('RGB', img.size)
        img_rgb.paste(img)
        img_rgb.save(os.path.join(output_dir, f'{label}_{i+1:04d}.png'))
    print(f'  Generated {count} {label} images in {output_dir}')


def generate_samples():
    """Generate 6 sample test images (3 stroke + 3 normal)."""
    os.makedirs(SAMPLES_DIR, exist_ok=True)
    for i in range(3):
        # Normal sample
        img = create_brain_base()
        img_rgb = Image.new('RGB', img.size)
        img_rgb.paste(img)
        img_rgb.save(os.path.join(SAMPLES_DIR, f'sample_normal_{i+1}.png'))

        # Stroke sample
        img = create_brain_base()
        img = add_stroke(img)
        img_rgb = Image.new('RGB', img.size)
        img_rgb.paste(img)
        img_rgb.save(os.path.join(SAMPLES_DIR, f'sample_stroke_{i+1}.png'))

    print(f'  Generated 6 sample images in {SAMPLES_DIR}')


def main():
    print('=' * 60)
    print('Brain Stroke CT Dataset Generator')
    print('=' * 60)

    # Training data
    print('\nGenerating training data...')
    generate_images(os.path.join(DATASET_DIR, 'train', 'stroke'), 'stroke', 400)
    generate_images(os.path.join(DATASET_DIR, 'train', 'normal'), 'normal', 400)

    # Test data
    print('\nGenerating test data...')
    generate_images(os.path.join(DATASET_DIR, 'test', 'stroke'), 'stroke', 100)
    generate_images(os.path.join(DATASET_DIR, 'test', 'normal'), 'normal', 100)

    # Sample images for quick testing
    print('\nGenerating sample images...')
    generate_samples()

    print('\n' + '=' * 60)
    print('Dataset generation complete!')
    print(f'  Train: 800 images (400 stroke + 400 normal)')
    print(f'  Test:  200 images (100 stroke + 100 normal)')
    print(f'  Samples: 6 images (3 stroke + 3 normal)')
    print('=' * 60)


if __name__ == '__main__':
    main()
