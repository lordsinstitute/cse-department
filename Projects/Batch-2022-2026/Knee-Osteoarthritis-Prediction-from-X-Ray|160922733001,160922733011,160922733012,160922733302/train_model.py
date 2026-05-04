"""
Train MobileNetV2, custom CNN, and ML models for knee osteoarthritis classification.
5-class KL grading: Normal, Doubtful, Mild, Moderate, Severe.
Designed for real knee X-ray images with data augmentation.
"""

import os
import json
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'Dataset')
BATCH_SIZE = 32
EPOCHS = 20
LR = 0.0001

CLASS_NAMES = ['Normal', 'Doubtful', 'Mild', 'Moderate', 'Severe']
NUM_CLASSES = 5

device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
print(f'Using device: {device}')


class KneeCNN(nn.Module):
    """Custom CNN for knee X-ray classification (comparison model)."""

    def __init__(self, num_classes=NUM_CLASSES):
        super(KneeCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256 * 8 * 8, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


def create_mobilenet(num_classes=NUM_CLASSES):
    """Create MobileNetV2 with transfer learning for 5-class classification."""
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)

    # Freeze early layers, unfreeze last 5 feature blocks for fine-tuning
    for i, child in enumerate(model.features):
        if i < 14:  # Freeze first 14 blocks (of 19)
            for param in child.parameters():
                param.requires_grad = False

    # Replace classifier for 5 classes
    model.classifier = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(1280, num_classes)
    )

    return model


def get_mobilenet_transforms(train=False):
    """Transforms for MobileNetV2 with augmentation for training."""
    if train:
        return transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.RandomCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])


def get_cnn_transforms(train=False):
    """Transforms for custom CNN with augmentation for training."""
    if train:
        return transforms.Compose([
            transforms.Grayscale(num_output_channels=1),
            transforms.Resize((140, 140)),
            transforms.RandomCrop(128),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ToTensor(),
        ])
    return transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
    ])


def load_data(train_transform, test_transform):
    """Load training and test datasets with separate transforms."""
    train_dataset = datasets.ImageFolder(
        os.path.join(DATASET_DIR, 'train'), transform=train_transform
    )
    test_dataset = datasets.ImageFolder(
        os.path.join(DATASET_DIR, 'test'), transform=test_transform
    )

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

    print(f'  Train: {len(train_dataset)} images, Test: {len(test_dataset)} images')
    print(f'  Classes: {train_dataset.classes}')

    return train_loader, test_loader, train_dataset, test_dataset


def train_model(model, train_loader, test_loader, model_name, epochs=EPOCHS, lr=LR,
                class_weights=None):
    """Train a PyTorch model and return metrics."""
    print(f'\n{"=" * 60}')
    print(f'Training {model_name}')
    print(f'{"=" * 60}')

    model = model.to(device)
    # Use class weights to address Doubtful under-representation
    if class_weights is not None:
        weights_tensor = torch.tensor(class_weights, dtype=torch.float).to(device)
        criterion = nn.CrossEntropyLoss(weight=weights_tensor)
        print(f'  Using weighted loss: {dict(zip(CLASS_NAMES, class_weights))}')
    else:
        criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=lr)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=3, factor=0.5)

    best_val_acc = 0
    best_state = None

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        train_acc = 100 * correct / total
        avg_loss = running_loss / len(train_loader)

        # Validation
        model.eval()
        val_correct = 0
        val_total = 0
        val_loss = 0.0
        with torch.no_grad():
            for images, labels in test_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                _, predicted = outputs.max(1)
                val_total += labels.size(0)
                val_correct += predicted.eq(labels).sum().item()

        val_acc = 100 * val_correct / val_total
        avg_val_loss = val_loss / len(test_loader)
        scheduler.step(avg_val_loss)

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_state = {k: v.clone() for k, v in model.state_dict().items()}

        print(f'Epoch [{epoch+1}/{epochs}] Loss: {avg_loss:.4f} '
              f'Train Acc: {train_acc:.1f}% Val Acc: {val_acc:.1f}%')

    # Restore best model
    if best_state:
        model.load_state_dict(best_state)
        print(f'Restored best model (Val Acc: {best_val_acc:.1f}%)')

    return model


def evaluate_model(model, test_loader):
    """Evaluate model and return per-class and overall metrics."""
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            outputs = model(images)
            _, predicted = outputs.max(1)
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.numpy())

    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)

    overall = {
        'accuracy': round(accuracy_score(all_labels, all_preds) * 100, 2),
        'precision': round(precision_score(all_labels, all_preds, average='weighted', zero_division=0) * 100, 2),
        'recall': round(recall_score(all_labels, all_preds, average='weighted', zero_division=0) * 100, 2),
        'f1': round(f1_score(all_labels, all_preds, average='weighted', zero_division=0) * 100, 2),
    }

    # Per-class accuracy
    per_class = {}
    for i, name in enumerate(CLASS_NAMES):
        mask = all_labels == i
        if mask.sum() > 0:
            class_acc = round((all_preds[mask] == i).mean() * 100, 2)
        else:
            class_acc = 0.0
        per_class[name] = class_acc

    overall['per_class'] = per_class
    return overall


def flatten_dataset(dataset):
    """Flatten image dataset for ML models."""
    X, y = [], []
    for img, label in dataset:
        X.append(img.numpy().flatten())
        y.append(label)
    return np.array(X), np.array(y)


def train_rf(train_dataset, test_dataset):
    """Train Random Forest for comparison."""
    print(f'\n{"=" * 60}')
    print('Training Random Forest')
    print(f'{"=" * 60}')

    X_train, y_train = flatten_dataset(train_dataset)
    X_test, y_test = flatten_dataset(test_dataset)

    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    rf_preds = rf.predict(X_test)

    # Save model
    rf_path = os.path.join(BASE_DIR, 'ml_model.pkl')
    joblib.dump(rf, rf_path)
    print(f'Saved to {rf_path}')

    overall = {
        'accuracy': round(accuracy_score(y_test, rf_preds) * 100, 2),
        'precision': round(precision_score(y_test, rf_preds, average='weighted', zero_division=0) * 100, 2),
        'recall': round(recall_score(y_test, rf_preds, average='weighted', zero_division=0) * 100, 2),
        'f1': round(f1_score(y_test, rf_preds, average='weighted', zero_division=0) * 100, 2),
    }

    per_class = {}
    for i, name in enumerate(CLASS_NAMES):
        mask = y_test == i
        if mask.sum() > 0:
            class_acc = round((rf_preds[mask] == i).mean() * 100, 2)
        else:
            class_acc = 0.0
        per_class[name] = class_acc

    overall['per_class'] = per_class
    print(f'Accuracy: {overall["accuracy"]}%')
    return overall


def main():
    print('=' * 60)
    print('Knee Osteoarthritis — Model Training (Real X-Ray Data)')
    print(f'Classes: {CLASS_NAMES}')
    print('=' * 60)

    all_results = {}

    # Class weights to improve Doubtful accuracy (inverse-frequency style)
    # Doubtful gets 3x weight since it has the lowest per-class accuracy (~7%)
    doubtful_boost_weights = [1.0, 3.0, 1.5, 1.5, 1.0]  # Normal/Doubtful/Mild/Moderate/Severe

    # 1. MobileNetV2 (Transfer Learning)
    mob_train_transform = get_mobilenet_transforms(train=True)
    mob_test_transform = get_mobilenet_transforms(train=False)
    mob_train_loader, mob_test_loader, _, _ = load_data(mob_train_transform, mob_test_transform)

    mobilenet = create_mobilenet()
    mobilenet = train_model(mobilenet, mob_train_loader, mob_test_loader,
                            'MobileNetV2 (Transfer Learning)', epochs=EPOCHS, lr=LR,
                            class_weights=doubtful_boost_weights)
    mob_metrics = evaluate_model(mobilenet, mob_test_loader)

    # Save MobileNetV2
    mob_path = os.path.join(BASE_DIR, 'knee_mobilenet_model.pth')
    torch.save(mobilenet.state_dict(), mob_path)
    print(f'\nMobileNetV2 saved to {mob_path}')
    print(f'Results: {mob_metrics}')
    all_results['MobileNetV2'] = mob_metrics

    # 2. Custom CNN
    cnn_train_transform = get_cnn_transforms(train=True)
    cnn_test_transform = get_cnn_transforms(train=False)
    cnn_train_loader, cnn_test_loader, _, _ = load_data(cnn_train_transform, cnn_test_transform)

    cnn = KneeCNN()
    cnn = train_model(cnn, cnn_train_loader, cnn_test_loader,
                      'Custom CNN', epochs=EPOCHS, lr=0.001,
                      class_weights=doubtful_boost_weights)
    cnn_metrics = evaluate_model(cnn, cnn_test_loader)

    # Save Custom CNN
    cnn_path = os.path.join(BASE_DIR, 'knee_cnn_model.pth')
    torch.save(cnn.state_dict(), cnn_path)
    print(f'Custom CNN saved to {cnn_path}')
    print(f'Results: {cnn_metrics}')
    all_results['Custom CNN'] = cnn_metrics

    # 3. Random Forest (using grayscale flattened images)
    _, _, cnn_train_dataset, cnn_test_dataset = load_data(cnn_test_transform, cnn_test_transform)
    rf_metrics = train_rf(cnn_train_dataset, cnn_test_dataset)
    all_results['Random Forest'] = rf_metrics

    # Save all metrics
    metrics_path = os.path.join(BASE_DIR, 'models_info.json')
    with open(metrics_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f'\nMetrics saved to {metrics_path}')

    # Print summary
    print(f'\n{"=" * 60}')
    print('Model Comparison Summary')
    print(f'{"=" * 60}')
    print(f'{"Model":<25} {"Accuracy":>10} {"Precision":>10} {"Recall":>10} {"F1":>10}')
    print('-' * 65)
    for name, metrics in all_results.items():
        print(f'{name:<25} {metrics["accuracy"]:>9.2f}% {metrics["precision"]:>9.2f}% '
              f'{metrics["recall"]:>9.2f}% {metrics["f1"]:>9.2f}%')

    print(f'\nPer-Class Accuracy (MobileNetV2):')
    for cls, acc in all_results['MobileNetV2']['per_class'].items():
        print(f'  {cls:<12} {acc:.2f}%')
    print('=' * 60)


if __name__ == '__main__':
    main()
