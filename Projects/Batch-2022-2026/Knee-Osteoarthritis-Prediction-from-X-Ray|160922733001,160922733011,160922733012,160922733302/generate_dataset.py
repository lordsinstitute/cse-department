"""
Generate synthetic knee X-ray images for osteoarthritis classification.
Creates 5 classes based on Kellgren-Lawrence (KL) grading scale:
  Grade 0 - Normal
  Grade 1 - Doubtful
  Grade 2 - Mild
  Grade 3 - Moderate
  Grade 4 - Severe
"""

import os
import random
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'Dataset')
SAMPLES_DIR = os.path.join(BASE_DIR, 'static', 'test_samples')
IMG_SIZE = 224

CLASS_NAMES = ['0_normal', '1_doubtful', '2_mild', '3_moderate', '4_severe']
GRADE_LABELS = ['normal', 'doubtful', 'mild', 'moderate', 'severe']


def create_knee_base(size=IMG_SIZE):
    """Create the base knee X-ray structure (bones + soft tissue)."""
    img = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(img)
    cx = size // 2

    # Soft tissue background (gray)
    tissue_brightness = random.randint(35, 55)
    draw.rectangle([0, 0, size, size], fill=tissue_brightness)

    # Skin/muscle outline (slightly brighter ellipse around knee)
    outline_b = tissue_brightness + random.randint(10, 20)
    draw.ellipse([cx - 80, 20, cx + 80, size - 20], fill=outline_b)

    return img, draw, cx


def draw_femur(draw, cx, size, bone_brightness, condyle_smoothness=1.0):
    """Draw the femur (upper bone) with condyles."""
    # Femur shaft (top portion)
    shaft_w = random.randint(28, 35)
    shaft_top = 10
    shaft_bottom = size // 2 - 30
    draw.rectangle([cx - shaft_w, shaft_top, cx + shaft_w, shaft_bottom],
                   fill=bone_brightness)

    # Femoral condyles (rounded bottom of femur) - two bumps
    condyle_y = shaft_bottom
    condyle_r = int(random.randint(30, 38) * condyle_smoothness)
    # Left condyle
    draw.ellipse([cx - 55, condyle_y - 10, cx - 5, condyle_y + condyle_r],
                 fill=bone_brightness)
    # Right condyle
    draw.ellipse([cx + 5, condyle_y - 10, cx + 55, condyle_y + condyle_r],
                 fill=bone_brightness)

    return condyle_y + condyle_r


def draw_tibia(draw, cx, size, bone_brightness, joint_y, plateau_flatness=1.0):
    """Draw the tibia (lower bone) with tibial plateau."""
    # Tibial plateau (flat top of tibia)
    plateau_w = int(random.randint(50, 58) * plateau_flatness)
    plateau_h = random.randint(15, 22)
    draw.rectangle([cx - plateau_w, joint_y, cx + plateau_w, joint_y + plateau_h],
                   fill=bone_brightness)

    # Tibia shaft (below plateau)
    shaft_w = random.randint(26, 33)
    shaft_top = joint_y + plateau_h
    shaft_bottom = size - 10
    draw.rectangle([cx - shaft_w, shaft_top, cx + shaft_w, shaft_bottom],
                   fill=bone_brightness)

    return joint_y


def add_osteophytes(draw, cx, joint_y, count, max_size):
    """Add osteophytes (bone spurs) at the joint margins."""
    for _ in range(count):
        side = random.choice([-1, 1])
        ox = cx + side * random.randint(45, 65)
        oy = joint_y + random.randint(-8, 8)
        ow = random.randint(3, max_size)
        oh = random.randint(3, max_size)
        brightness = random.randint(170, 220)
        draw.ellipse([ox - ow, oy - oh, ox + ow, oy + oh], fill=brightness)


def add_sclerosis(draw, cx, joint_y, intensity):
    """Add subchondral sclerosis (bright band at bone-joint interface)."""
    sclerosis_b = random.randint(200, 240) if intensity > 0.5 else random.randint(170, 200)
    band_h = int(random.randint(2, 5) * intensity)
    draw.rectangle([cx - 50, joint_y - band_h, cx + 50, joint_y + 1],
                   fill=sclerosis_b)


def add_bone_cysts(draw, cx, joint_y, count):
    """Add subchondral bone cysts (small dark spots near joint)."""
    for _ in range(count):
        bx = cx + random.randint(-40, 40)
        by = joint_y + random.choice([-1, 1]) * random.randint(10, 25)
        br = random.randint(3, 7)
        draw.ellipse([bx - br, by - br, bx + br, by + br],
                     fill=random.randint(20, 50))


def generate_knee_xray(grade, size=IMG_SIZE):
    """Generate a single knee X-ray image for a given KL grade."""
    img, draw, cx = create_knee_base(size)

    bone_brightness = random.randint(150, 185)

    # Joint space gap varies by grade
    if grade == 0:      # Normal - wide gap
        gap = random.randint(25, 32)
    elif grade == 1:    # Doubtful - slightly narrowed
        gap = random.randint(20, 26)
    elif grade == 2:    # Mild - definite narrowing
        gap = random.randint(14, 20)
    elif grade == 3:    # Moderate - significant narrowing
        gap = random.randint(8, 15)
    else:               # Severe - near-complete loss
        gap = random.randint(2, 7)

    # Draw femur
    femur_bottom = draw_femur(draw, cx, size, bone_brightness,
                              condyle_smoothness=1.0 if grade < 3 else random.uniform(0.8, 0.95))

    # Joint space (dark gap)
    joint_y = femur_bottom + gap

    # Draw tibia
    draw_tibia(draw, cx, size, bone_brightness, joint_y,
               plateau_flatness=1.0 if grade < 4 else random.uniform(0.9, 1.1))

    # Grade-specific features
    if grade >= 1:
        # Doubtful+ : possible tiny osteophytes
        osteophyte_count = random.randint(0, 2) if grade == 1 else \
                          random.randint(1, 3) if grade == 2 else \
                          random.randint(2, 5) if grade == 3 else \
                          random.randint(4, 8)
        osteophyte_size = 4 if grade <= 2 else 7 if grade == 3 else 12
        add_osteophytes(draw, cx, joint_y, osteophyte_count, osteophyte_size)

    if grade >= 2:
        # Mild+ : sclerosis at joint line
        sclerosis_intensity = 0.3 if grade == 2 else 0.7 if grade == 3 else 1.0
        add_sclerosis(draw, cx, joint_y, sclerosis_intensity)

    if grade >= 3:
        # Moderate+ : possible bone cysts
        cyst_count = random.randint(0, 2) if grade == 3 else random.randint(1, 4)
        add_bone_cysts(draw, cx, joint_y, cyst_count)

    if grade == 4:
        # Severe: bone deformity — angular irregularities
        for _ in range(random.randint(2, 4)):
            dx = cx + random.randint(-45, 45)
            dy = joint_y + random.randint(-15, 15)
            dr = random.randint(3, 8)
            draw.polygon([
                (dx, dy - dr),
                (dx + dr, dy + dr),
                (dx - dr, dy + dr)
            ], fill=random.randint(160, 210))

    # Apply blur for realistic appearance
    blur_radius = random.uniform(1.0, 1.8)
    img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    # Add noise
    arr = np.array(img, dtype=np.float32)
    noise = np.random.normal(0, random.uniform(2, 6), arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr)

    # Convert to RGB for model compatibility
    img_rgb = Image.new('RGB', img.size)
    img_rgb.paste(img)

    return img_rgb


def generate_images(output_dir, grade, count):
    """Generate a set of knee X-ray images for a given grade."""
    os.makedirs(output_dir, exist_ok=True)
    label = GRADE_LABELS[grade]
    for i in range(count):
        img = generate_knee_xray(grade)
        img.save(os.path.join(output_dir, f'{label}_{i+1:04d}.png'))
    print(f'  Generated {count} grade {grade} ({label}) images in {output_dir}')


def generate_samples():
    """Generate 10 sample test images (2 per class)."""
    os.makedirs(SAMPLES_DIR, exist_ok=True)
    for grade in range(5):
        label = GRADE_LABELS[grade]
        for i in range(2):
            img = generate_knee_xray(grade)
            img.save(os.path.join(SAMPLES_DIR, f'sample_{grade}_{label}_{i+1}.png'))
    print(f'  Generated 10 sample images in {SAMPLES_DIR}')


def main():
    print('=' * 60)
    print('Knee Osteoarthritis X-Ray Dataset Generator')
    print('KL Grading: Normal | Doubtful | Mild | Moderate | Severe')
    print('=' * 60)

    # Training data: 250 per class = 1250 total
    print('\nGenerating training data...')
    for grade, class_name in enumerate(CLASS_NAMES):
        generate_images(
            os.path.join(DATASET_DIR, 'train', class_name),
            grade, 250
        )

    # Test data: 50 per class = 250 total
    print('\nGenerating test data...')
    for grade, class_name in enumerate(CLASS_NAMES):
        generate_images(
            os.path.join(DATASET_DIR, 'test', class_name),
            grade, 50
        )

    # Sample images
    print('\nGenerating sample images...')
    generate_samples()

    print('\n' + '=' * 60)
    print('Dataset generation complete!')
    print(f'  Train: 1250 images (250 per class x 5 classes)')
    print(f'  Test:  250 images (50 per class x 5 classes)')
    print(f'  Samples: 10 images (2 per class)')
    print('=' * 60)


if __name__ == '__main__':
    main()
