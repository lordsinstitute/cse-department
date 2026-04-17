"""
Train CNN and ML models for brain stroke detection from CT images.
Saves trained models and performance metrics.
"""

import os
import json
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'Dataset')
IMG_SIZE = 128
BATCH_SIZE = 32
EPOCHS = 15
LR = 0.001

device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
print(f'Using device: {device}')


class StrokeCNN(nn.Module):
    """CNN for binary classification of brain CT images (Normal vs Stroke)."""

    def __init__(self):
        super(StrokeCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256 * 8 * 8, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


def get_transforms():
    """Image preprocessing transforms."""
    return transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
    ])


def load_data():
    """Load training and test datasets."""
    transform = get_transforms()

    train_dataset = datasets.ImageFolder(
        os.path.join(DATASET_DIR, 'train'), transform=transform
    )
    test_dataset = datasets.ImageFolder(
        os.path.join(DATASET_DIR, 'test'), transform=transform
    )

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

    print(f'Classes: {train_dataset.classes}')
    print(f'Class to idx: {train_dataset.class_to_idx}')
    print(f'Train samples: {len(train_dataset)}')
    print(f'Test samples: {len(test_dataset)}')

    return train_loader, test_loader, train_dataset, test_dataset


def train_cnn(train_loader, test_loader):
    """Train the CNN model."""
    print('\n' + '=' * 60)
    print('Training CNN Model')
    print('=' * 60)

    model = StrokeCNN().to(device)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=LR)

    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.float().to(device)

            optimizer.zero_grad()
            outputs = model(images).squeeze()
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            predicted = (outputs >= 0.5).float()
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        train_acc = 100 * correct / total
        avg_loss = running_loss / len(train_loader)

        # Validation
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for images, labels in test_loader:
                images = images.to(device)
                labels = labels.float().to(device)
                outputs = model(images).squeeze()
                predicted = (outputs >= 0.5).float()
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()

        val_acc = 100 * val_correct / val_total
        print(f'Epoch [{epoch+1}/{EPOCHS}] Loss: {avg_loss:.4f} '
              f'Train Acc: {train_acc:.1f}% Val Acc: {val_acc:.1f}%')

    # Save model
    model_path = os.path.join(BASE_DIR, 'stroke_cnn_model.pth')
    torch.save(model.state_dict(), model_path)
    print(f'\nCNN model saved to {model_path}')

    return model


def evaluate_cnn(model, test_loader):
    """Evaluate CNN on test set."""
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            outputs = model(images).squeeze()
            predicted = (outputs >= 0.5).float()
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.numpy())

    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)

    return {
        'accuracy': round(accuracy_score(all_labels, all_preds) * 100, 2),
        'precision': round(precision_score(all_labels, all_preds, zero_division=0) * 100, 2),
        'recall': round(recall_score(all_labels, all_preds, zero_division=0) * 100, 2),
        'f1': round(f1_score(all_labels, all_preds, zero_division=0) * 100, 2),
    }


def flatten_dataset(dataset):
    """Flatten image dataset for ML models."""
    X, y = [], []
    for img, label in dataset:
        X.append(img.numpy().flatten())
        y.append(label)
    return np.array(X), np.array(y)


def train_ml_models(train_dataset, test_dataset):
    """Train traditional ML models for comparison."""
    print('\n' + '=' * 60)
    print('Training ML Models (for comparison)')
    print('=' * 60)

    X_train, y_train = flatten_dataset(train_dataset)
    X_test, y_test = flatten_dataset(test_dataset)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    results = {}

    # Random Forest
    print('\nTraining Random Forest...')
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    rf_preds = rf.predict(X_test)
    results['Random Forest'] = {
        'accuracy': round(accuracy_score(y_test, rf_preds) * 100, 2),
        'precision': round(precision_score(y_test, rf_preds, zero_division=0) * 100, 2),
        'recall': round(recall_score(y_test, rf_preds, zero_division=0) * 100, 2),
        'f1': round(f1_score(y_test, rf_preds, zero_division=0) * 100, 2),
    }
    print(f'  Accuracy: {results["Random Forest"]["accuracy"]}%')

    # Save RF model
    rf_path = os.path.join(BASE_DIR, 'ml_model.pkl')
    joblib.dump(rf, rf_path)
    print(f'  Saved to {rf_path}')

    # SVM
    print('\nTraining SVM...')
    svm = SVC(kernel='rbf', random_state=42)
    svm.fit(X_train_scaled, y_train)
    svm_preds = svm.predict(X_test_scaled)
    results['SVM'] = {
        'accuracy': round(accuracy_score(y_test, svm_preds) * 100, 2),
        'precision': round(precision_score(y_test, svm_preds, zero_division=0) * 100, 2),
        'recall': round(recall_score(y_test, svm_preds, zero_division=0) * 100, 2),
        'f1': round(f1_score(y_test, svm_preds, zero_division=0) * 100, 2),
    }
    print(f'  Accuracy: {results["SVM"]["accuracy"]}%')

    # Logistic Regression
    print('\nTraining Logistic Regression...')
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train_scaled, y_train)
    lr_preds = lr.predict(X_test_scaled)
    results['Logistic Regression'] = {
        'accuracy': round(accuracy_score(y_test, lr_preds) * 100, 2),
        'precision': round(precision_score(y_test, lr_preds, zero_division=0) * 100, 2),
        'recall': round(recall_score(y_test, lr_preds, zero_division=0) * 100, 2),
        'f1': round(f1_score(y_test, lr_preds, zero_division=0) * 100, 2),
    }
    print(f'  Accuracy: {results["Logistic Regression"]["accuracy"]}%')

    return results


def main():
    print('=' * 60)
    print('Brain Stroke Detection — Model Training')
    print('=' * 60)

    # Load data
    train_loader, test_loader, train_dataset, test_dataset = load_data()

    # Train CNN
    cnn_model = train_cnn(train_loader, test_loader)
    cnn_metrics = evaluate_cnn(cnn_model, test_loader)
    print(f'\nCNN Results: {cnn_metrics}')

    # Train ML models
    ml_results = train_ml_models(train_dataset, test_dataset)

    # Combine all results
    all_results = {'CNN (Deep Learning)': cnn_metrics}
    all_results.update(ml_results)

    # Save metrics
    metrics_path = os.path.join(BASE_DIR, 'models_info.json')
    with open(metrics_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f'\nMetrics saved to {metrics_path}')

    # Print summary
    print('\n' + '=' * 60)
    print('Model Comparison Summary')
    print('=' * 60)
    print(f'{"Model":<25} {"Accuracy":>10} {"Precision":>10} {"Recall":>10} {"F1":>10}')
    print('-' * 65)
    for name, metrics in all_results.items():
        print(f'{name:<25} {metrics["accuracy"]:>9.2f}% {metrics["precision"]:>9.2f}% '
              f'{metrics["recall"]:>9.2f}% {metrics["f1"]:>9.2f}%')
    print('=' * 60)


if __name__ == '__main__':
    main()
