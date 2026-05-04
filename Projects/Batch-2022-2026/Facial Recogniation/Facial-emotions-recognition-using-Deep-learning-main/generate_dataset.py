"""
Synthetic Facial Emotion Dataset Generator
Generates 48x48 grayscale face images for 7 emotions using OpenCV drawing primitives.
"""

import cv2
import numpy as np
import os
import random

EMOTIONS = ['Happy', 'Sad', 'Angry', 'Surprise', 'Fear', 'Disgust', 'Neutral']
IMG_SIZE = 48
TRAIN_PER_CLASS = 500
TEST_PER_CLASS = 100
SAMPLE_PER_CLASS = 2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'Dataset')


def rand_offset(base, max_off=2):
    """Add small random offset for variation."""
    return base + random.randint(-max_off, max_off)


def draw_face(emotion, variation_seed=None):
    """Draw a synthetic face with emotion-specific features on a 48x48 grayscale image."""
    if variation_seed is not None:
        random.seed(variation_seed)

    img = np.zeros((IMG_SIZE, IMG_SIZE), dtype=np.uint8)

    # Random background brightness
    bg = random.randint(10, 40)
    img[:] = bg

    # Face ellipse (centered, with slight random offset)
    cx = rand_offset(24, 2)
    cy = rand_offset(25, 2)
    face_w = rand_offset(18, 2)
    face_h = rand_offset(22, 2)
    face_color = random.randint(160, 220)
    cv2.ellipse(img, (cx, cy), (face_w, face_h), 0, 0, 360, face_color, -1)

    # Eye positions
    left_eye_x = rand_offset(cx - 7, 1)
    right_eye_x = rand_offset(cx + 7, 1)
    eye_y = rand_offset(cy - 5, 1)

    # Nose
    nose_x = rand_offset(cx, 1)
    nose_top = rand_offset(cy - 1, 1)
    nose_bot = rand_offset(cy + 4, 1)
    cv2.line(img, (nose_x, nose_top), (nose_x, nose_bot), face_color - 40, 1)

    # Mouth position
    mouth_y = rand_offset(cy + 10, 1)

    # Draw emotion-specific features
    if emotion == 'Happy':
        _draw_happy(img, cx, cy, left_eye_x, right_eye_x, eye_y, mouth_y, face_color)
    elif emotion == 'Sad':
        _draw_sad(img, cx, cy, left_eye_x, right_eye_x, eye_y, mouth_y, face_color)
    elif emotion == 'Angry':
        _draw_angry(img, cx, cy, left_eye_x, right_eye_x, eye_y, mouth_y, face_color)
    elif emotion == 'Surprise':
        _draw_surprise(img, cx, cy, left_eye_x, right_eye_x, eye_y, mouth_y, face_color)
    elif emotion == 'Fear':
        _draw_fear(img, cx, cy, left_eye_x, right_eye_x, eye_y, mouth_y, face_color)
    elif emotion == 'Disgust':
        _draw_disgust(img, cx, cy, left_eye_x, right_eye_x, eye_y, mouth_y, face_color)
    elif emotion == 'Neutral':
        _draw_neutral(img, cx, cy, left_eye_x, right_eye_x, eye_y, mouth_y, face_color)

    # Add Gaussian noise for diversity
    noise = np.random.normal(0, random.uniform(3, 8), img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Random slight blur
    if random.random() > 0.5:
        img = cv2.GaussianBlur(img, (3, 3), 0)

    return img


def _draw_happy(img, cx, cy, lex, rex, ey, my, fc):
    """Happy: raised eyebrows, wide eyes, upward mouth curve."""
    eye_r = rand_offset(3, 1)
    # Wide eyes
    cv2.circle(img, (lex, ey), eye_r, fc - 80, -1)
    cv2.circle(img, (rex, ey), eye_r, fc - 80, -1)
    # Pupils
    cv2.circle(img, (lex, ey), 1, 20, -1)
    cv2.circle(img, (rex, ey), 1, 20, -1)
    # Raised eyebrows
    brow_y = ey - rand_offset(5, 1)
    cv2.line(img, (lex - 4, brow_y), (lex + 4, brow_y - 1), fc - 60, 1)
    cv2.line(img, (rex - 4, brow_y - 1), (rex + 4, brow_y), fc - 60, 1)
    # Upward mouth curve (smile)
    cv2.ellipse(img, (cx, my - 2), (rand_offset(7, 1), rand_offset(4, 1)), 0, 10, 170, fc - 80, 1)


def _draw_sad(img, cx, cy, lex, rex, ey, my, fc):
    """Sad: lowered eyebrows, smaller eyes, downward mouth curve."""
    eye_r = rand_offset(2, 1)
    # Smaller eyes
    cv2.circle(img, (lex, ey), max(eye_r, 1), fc - 80, -1)
    cv2.circle(img, (rex, ey), max(eye_r, 1), fc - 80, -1)
    cv2.circle(img, (lex, ey), 1, 20, -1)
    cv2.circle(img, (rex, ey), 1, 20, -1)
    # Lowered / slanted eyebrows (inner higher)
    brow_y = ey - rand_offset(4, 1)
    cv2.line(img, (lex - 4, brow_y - 2), (lex + 4, brow_y + 1), fc - 60, 1)
    cv2.line(img, (rex - 4, brow_y + 1), (rex + 4, brow_y - 2), fc - 60, 1)
    # Downward mouth curve (frown)
    cv2.ellipse(img, (cx, my + 3), (rand_offset(6, 1), rand_offset(3, 1)), 0, 190, 350, fc - 80, 1)


def _draw_angry(img, cx, cy, lex, rex, ey, my, fc):
    """Angry: V-shaped eyebrows, narrow eyes, tight straight mouth."""
    # Narrow eyes (horizontal ellipses)
    cv2.ellipse(img, (lex, ey), (3, rand_offset(2, 0)), 0, 0, 360, fc - 80, -1)
    cv2.ellipse(img, (rex, ey), (3, rand_offset(2, 0)), 0, 0, 360, fc - 80, -1)
    cv2.circle(img, (lex, ey), 1, 20, -1)
    cv2.circle(img, (rex, ey), 1, 20, -1)
    # V-shaped eyebrows (inner low, outer high)
    brow_y = ey - rand_offset(4, 1)
    cv2.line(img, (lex - 5, brow_y - 3), (lex + 3, brow_y + 1), fc - 60, 2)
    cv2.line(img, (rex - 3, brow_y + 1), (rex + 5, brow_y - 3), fc - 60, 2)
    # Tight straight mouth
    mouth_w = rand_offset(5, 1)
    cv2.line(img, (cx - mouth_w, my), (cx + mouth_w, my), fc - 80, 2)


def _draw_surprise(img, cx, cy, lex, rex, ey, my, fc):
    """Surprise: high eyebrows, very wide circular eyes, O-shaped mouth."""
    eye_r = rand_offset(4, 1)
    # Very wide eyes
    cv2.circle(img, (lex, ey), eye_r, fc - 80, -1)
    cv2.circle(img, (rex, ey), eye_r, fc - 80, -1)
    cv2.circle(img, (lex, ey), 2, 20, -1)
    cv2.circle(img, (rex, ey), 2, 20, -1)
    # High eyebrows
    brow_y = ey - rand_offset(7, 1)
    cv2.line(img, (lex - 4, brow_y), (lex + 4, brow_y), fc - 60, 1)
    cv2.line(img, (rex - 4, brow_y), (rex + 4, brow_y), fc - 60, 1)
    # O-shaped mouth
    mouth_r = rand_offset(4, 1)
    cv2.circle(img, (cx, my), mouth_r, fc - 80, 1)


def _draw_fear(img, cx, cy, lex, rex, ey, my, fc):
    """Fear: raised eyebrows, wide eyes, slightly open mouth."""
    eye_r = rand_offset(3, 1)
    # Wide eyes
    cv2.circle(img, (lex, ey), eye_r + 1, fc - 80, -1)
    cv2.circle(img, (rex, ey), eye_r + 1, fc - 80, -1)
    cv2.circle(img, (lex, ey), 1, 20, -1)
    cv2.circle(img, (rex, ey), 1, 20, -1)
    # Raised inner eyebrows (curved upward in the middle)
    brow_y = ey - rand_offset(6, 1)
    cv2.line(img, (lex - 4, brow_y + 1), (lex + 2, brow_y - 2), fc - 60, 1)
    cv2.line(img, (rex - 2, brow_y - 2), (rex + 4, brow_y + 1), fc - 60, 1)
    # Slightly open mouth (small ellipse)
    cv2.ellipse(img, (cx, my), (rand_offset(4, 1), rand_offset(2, 1)), 0, 0, 360, fc - 80, 1)


def _draw_disgust(img, cx, cy, lex, rex, ey, my, fc):
    """Disgust: lowered uneven eyebrows, squinted eyes, wavy mouth."""
    # Squinted eyes
    cv2.ellipse(img, (lex, ey), (3, 1), 0, 0, 360, fc - 80, -1)
    cv2.ellipse(img, (rex, ey), (3, 1), 0, 0, 360, fc - 80, -1)
    cv2.circle(img, (lex, ey), 1, 20, -1)
    cv2.circle(img, (rex, ey), 1, 20, -1)
    # Uneven lowered eyebrows
    brow_y = ey - rand_offset(3, 1)
    cv2.line(img, (lex - 4, brow_y - 1), (lex + 4, brow_y + 2), fc - 60, 2)
    cv2.line(img, (rex - 4, brow_y), (rex + 4, brow_y - 1), fc - 60, 1)
    # Wavy mouth (two small arcs)
    cv2.ellipse(img, (cx - 3, my), (3, 2), 0, 190, 350, fc - 80, 1)
    cv2.ellipse(img, (cx + 3, my), (3, 2), 0, 10, 170, fc - 80, 1)


def _draw_neutral(img, cx, cy, lex, rex, ey, my, fc):
    """Neutral: normal eyebrows, normal eyes, straight mouth."""
    eye_r = rand_offset(3, 0)
    # Normal eyes
    cv2.circle(img, (lex, ey), eye_r, fc - 80, -1)
    cv2.circle(img, (rex, ey), eye_r, fc - 80, -1)
    cv2.circle(img, (lex, ey), 1, 20, -1)
    cv2.circle(img, (rex, ey), 1, 20, -1)
    # Normal straight eyebrows
    brow_y = ey - rand_offset(4, 1)
    cv2.line(img, (lex - 4, brow_y), (lex + 4, brow_y), fc - 60, 1)
    cv2.line(img, (rex - 4, brow_y), (rex + 4, brow_y), fc - 60, 1)
    # Straight mouth
    mouth_w = rand_offset(6, 1)
    cv2.line(img, (cx - mouth_w, my), (cx + mouth_w, my), fc - 70, 1)


def generate_dataset():
    """Generate the complete synthetic dataset."""
    print("=" * 60)
    print("Synthetic Facial Emotion Dataset Generator")
    print("=" * 60)

    total_images = 0

    for emotion in EMOTIONS:
        print(f"\nGenerating {emotion} images...")

        # Training images
        train_dir = os.path.join(DATASET_DIR, 'train', emotion)
        os.makedirs(train_dir, exist_ok=True)
        for i in range(TRAIN_PER_CLASS):
            img = draw_face(emotion, variation_seed=None)
            cv2.imwrite(os.path.join(train_dir, f'{emotion.lower()}_{i:04d}.png'), img)
        print(f"  Train: {TRAIN_PER_CLASS} images saved to {train_dir}")
        total_images += TRAIN_PER_CLASS

        # Test images
        test_dir = os.path.join(DATASET_DIR, 'test', emotion)
        os.makedirs(test_dir, exist_ok=True)
        for i in range(TEST_PER_CLASS):
            img = draw_face(emotion, variation_seed=None)
            cv2.imwrite(os.path.join(test_dir, f'{emotion.lower()}_{i:04d}.png'), img)
        print(f"  Test:  {TEST_PER_CLASS} images saved to {test_dir}")
        total_images += TEST_PER_CLASS

        # Sample images for download
        sample_dir = os.path.join(DATASET_DIR, 'samples')
        os.makedirs(sample_dir, exist_ok=True)
        for i in range(SAMPLE_PER_CLASS):
            img = draw_face(emotion, variation_seed=None)
            # Save larger version (96x96) for better visibility
            img_large = cv2.resize(img, (96, 96), interpolation=cv2.INTER_NEAREST)
            cv2.imwrite(os.path.join(sample_dir, f'{emotion.lower()}_sample_{i + 1}.png'), img_large)
        print(f"  Samples: {SAMPLE_PER_CLASS} images saved to {sample_dir}")
        total_images += SAMPLE_PER_CLASS

    print(f"\n{'=' * 60}")
    print(f"Dataset generation complete!")
    print(f"Total images generated: {total_images}")
    print(f"  Training: {TRAIN_PER_CLASS * len(EMOTIONS)} images")
    print(f"  Testing:  {TEST_PER_CLASS * len(EMOTIONS)} images")
    print(f"  Samples:  {SAMPLE_PER_CLASS * len(EMOTIONS)} images")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    generate_dataset()
