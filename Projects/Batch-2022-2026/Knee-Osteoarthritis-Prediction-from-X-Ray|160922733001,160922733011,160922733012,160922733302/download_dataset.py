"""
Download real knee X-ray dataset from Kaggle for osteoarthritis classification.
Uses the 'Knee Osteoarthritis Dataset with Severity Grading' dataset.

KL Grading: 0=Normal, 1=Doubtful, 2=Mild, 3=Moderate, 4=Severe

Setup: pip install kagglehub
       Configure Kaggle API credentials (kaggle.json) if prompted.
"""

import os
import shutil
import random
import kagglehub

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'Dataset')
SAMPLES_DIR = os.path.join(BASE_DIR, 'static', 'test_samples')

CLASS_MAP = {
    '0': '0_normal',
    '1': '1_doubtful',
    '2': '2_mild',
    '3': '3_moderate',
    '4': '4_severe',
    'Normal': '0_normal',
    'Doubtful': '1_doubtful',
    'Mild': '2_mild',
    'Moderate': '3_moderate',
    'Severe': '4_severe',
}

GRADE_LABELS = ['normal', 'doubtful', 'mild', 'moderate', 'severe']


def find_image_dirs(root):
    """Recursively find directories containing image files."""
    img_exts = {'.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff'}
    result = []
    for dirpath, dirnames, filenames in os.walk(root):
        images = [f for f in filenames if os.path.splitext(f)[1].lower() in img_exts]
        if images:
            result.append((dirpath, images))
    return result


def organize_dataset(download_path):
    """Organize downloaded dataset into Dataset/train and Dataset/test."""
    print(f'\nOrganizing dataset from: {download_path}')

    # Find all directories with images
    img_dirs = find_image_dirs(download_path)
    print(f'Found {len(img_dirs)} directories with images')

    # Check if already has train/test split
    has_train = any('train' in d[0].lower() for d in img_dirs)
    has_test = any('test' in d[0].lower() or 'val' in d[0].lower() for d in img_dirs)

    # Collect images by class
    class_images = {cls: {'train': [], 'test': []} for cls in CLASS_MAP.values()}

    for dirpath, images in img_dirs:
        # Determine class from directory name
        dirname = os.path.basename(dirpath)
        mapped_class = CLASS_MAP.get(dirname)

        if not mapped_class:
            # Try parent directory
            parent = os.path.basename(os.path.dirname(dirpath))
            mapped_class = CLASS_MAP.get(parent)

        if not mapped_class:
            print(f'  Skipping unknown class directory: {dirpath}')
            continue

        # Determine split
        path_lower = dirpath.lower()
        if has_train and has_test:
            if 'test' in path_lower or 'val' in path_lower:
                split = 'test'
            else:
                split = 'train'
        else:
            split = 'all'  # Will split manually

        full_paths = [os.path.join(dirpath, img) for img in images]

        if split == 'all':
            class_images[mapped_class]['train'].extend(full_paths)
        else:
            class_images[mapped_class][split].extend(full_paths)

    # If no train/test split, do 80/20
    if not has_train or not has_test:
        print('  No train/test split found, creating 80/20 split...')
        for cls in class_images:
            all_imgs = class_images[cls]['train']
            random.shuffle(all_imgs)
            split_idx = int(len(all_imgs) * 0.8)
            class_images[cls] = {
                'train': all_imgs[:split_idx],
                'test': all_imgs[split_idx:],
            }

    # Clear existing dataset
    for split in ['train', 'test']:
        split_dir = os.path.join(DATASET_DIR, split)
        if os.path.exists(split_dir):
            shutil.rmtree(split_dir)

    # Copy images to organized structure
    total = 0
    for cls, splits in class_images.items():
        for split, paths in splits.items():
            if not paths:
                continue
            out_dir = os.path.join(DATASET_DIR, split, cls)
            os.makedirs(out_dir, exist_ok=True)
            for i, src in enumerate(paths):
                ext = os.path.splitext(src)[1]
                dst = os.path.join(out_dir, f'{cls}_{i+1:04d}{ext}')
                shutil.copy2(src, dst)
                total += 1
            print(f'  {split}/{cls}: {len(paths)} images')

    print(f'\nTotal: {total} images organized')
    return total


def generate_samples():
    """Copy 2 sample images per class from test set for the web UI."""
    os.makedirs(SAMPLES_DIR, exist_ok=True)
    # Clear old samples
    for f in os.listdir(SAMPLES_DIR):
        os.remove(os.path.join(SAMPLES_DIR, f))

    test_dir = os.path.join(DATASET_DIR, 'test')
    for grade, label in enumerate(GRADE_LABELS):
        class_dir = os.path.join(test_dir, f'{grade}_{label}')
        if not os.path.exists(class_dir):
            continue
        images = sorted(os.listdir(class_dir))[:2]
        for i, img in enumerate(images):
            src = os.path.join(class_dir, img)
            dst = os.path.join(SAMPLES_DIR, f'sample_{grade}_{label}_{i+1}.png')
            shutil.copy2(src, dst)

    print(f'Generated sample images in {SAMPLES_DIR}')


def main():
    print('=' * 60)
    print('Knee Osteoarthritis — Real X-Ray Dataset Download')
    print('=' * 60)

    # Download from Kaggle
    print('\nDownloading dataset from Kaggle...')
    print('(You may be prompted for Kaggle credentials on first run)')
    download_path = kagglehub.dataset_download(
        'shashwatwork/knee-osteoarthritis-dataset-with-severity'
    )
    print(f'Downloaded to: {download_path}')

    # Organize into proper structure
    total = organize_dataset(download_path)

    if total == 0:
        print('\nERROR: No images were organized. Check the dataset structure.')
        print('Listing downloaded contents:')
        for root, dirs, files in os.walk(download_path):
            level = root.replace(download_path, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            if level < 3:
                for f in files[:5]:
                    print(f'{indent}  {f}')
                if len(files) > 5:
                    print(f'{indent}  ... and {len(files)-5} more')
        return

    # Generate sample images for web UI
    generate_samples()

    print('\n' + '=' * 60)
    print('Dataset ready! Run train_model.py to retrain on real X-rays.')
    print('=' * 60)


if __name__ == '__main__':
    main()
