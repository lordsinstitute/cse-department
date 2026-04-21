"""
Train deep learning (CNN) and ML models for brain hemorrhage detection.
Compares: CNN (PyTorch), Random Forest, SVM, Logistic Regression.
Saves the best model and performance metrics.
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pickle
import json
import os
from PIL import Image

IMG_SIZE = 128
BATCH_SIZE = 32
EPOCHS = 15
DATASET_DIR = 'dataset'


# ---- CNN Model ----

class BrainCNN(nn.Module):
    def __init__(self):
        super(BrainCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256 * (IMG_SIZE // 16) * (IMG_SIZE // 16), 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


def get_data_loaders():
    """Create PyTorch data loaders."""
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
    ])

    train_dataset = datasets.ImageFolder(os.path.join(DATASET_DIR, 'train'), transform=transform)
    test_dataset = datasets.ImageFolder(os.path.join(DATASET_DIR, 'test'), transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

    return train_loader, test_loader, train_dataset.class_to_idx


def get_flat_data():
    """Load images as flattened arrays for ML models."""
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
    ])

    train_dataset = datasets.ImageFolder(os.path.join(DATASET_DIR, 'train'), transform=transform)
    test_dataset = datasets.ImageFolder(os.path.join(DATASET_DIR, 'test'), transform=transform)

    X_train = np.array([img.numpy().flatten() for img, _ in train_dataset])
    y_train = np.array([label for _, label in train_dataset])
    X_test = np.array([img.numpy().flatten() for img, _ in test_dataset])
    y_test = np.array([label for _, label in test_dataset])

    return X_train, y_train, X_test, y_test


def train_cnn(train_loader, test_loader):
    """Train the CNN model."""
    device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
    print(f'  Device: {device}')

    model = BrainCNN().to(device)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Training
    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.float().unsqueeze(1).to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            predicted = (outputs > 0.5).float()
            correct += (predicted == labels).sum().item()
            total += labels.size(0)

        train_acc = correct / total * 100
        avg_loss = running_loss / len(train_loader)
        print(f'  Epoch [{epoch+1}/{EPOCHS}] Loss: {avg_loss:.4f} Train Acc: {train_acc:.1f}%')

    # Evaluation
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            outputs = model(images)
            predicted = (outputs > 0.5).float().cpu()
            all_preds.extend(predicted.squeeze().numpy())
            all_labels.extend(labels.numpy())

    all_preds = np.array(all_preds).astype(int)
    all_labels = np.array(all_labels)

    # Save model (CPU version for portability)
    model_cpu = model.to('cpu')
    torch.save(model_cpu.state_dict(), 'brain_cnn_model.pth')

    return all_labels, all_preds


def train_ml_models(X_train, y_train, X_test, y_test):
    """Train ML models and return metrics."""
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'SVM': SVC(kernel='rbf', random_state=42),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    }

    results = {}
    for name, model in models.items():
        print(f'  Training {name}...')
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        results[name] = {
            'accuracy': round(accuracy_score(y_test, y_pred) * 100, 2),
            'precision': round(precision_score(y_test, y_pred) * 100, 2),
            'recall': round(recall_score(y_test, y_pred) * 100, 2),
            'f1': round(f1_score(y_test, y_pred) * 100, 2),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        print(f'    Accuracy: {results[name]["accuracy"]}%')

    # Save best ML model (Random Forest typically best)
    best_name = max(results, key=lambda k: results[k]['accuracy'])
    best_model = models[best_name]
    with open('ml_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)

    return results


def compute_metrics(y_true, y_pred, name):
    """Compute classification metrics."""
    return {
        'accuracy': round(accuracy_score(y_true, y_pred) * 100, 2),
        'precision': round(precision_score(y_true, y_pred) * 100, 2),
        'recall': round(recall_score(y_true, y_pred) * 100, 2),
        'f1': round(f1_score(y_true, y_pred) * 100, 2),
        'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
    }


if __name__ == '__main__':
    print('=' * 50)
    print('Brain Hemorrhage Detection - Model Training')
    print('=' * 50)

    # Get data loaders
    print('\n[1/3] Loading dataset...')
    train_loader, test_loader, class_to_idx = get_data_loaders()
    print(f'  Classes: {class_to_idx}')
    print(f'  Train batches: {len(train_loader)}, Test batches: {len(test_loader)}')

    # Train CNN
    print(f'\n[2/3] Training CNN ({EPOCHS} epochs)...')
    y_true, y_pred_cnn = train_cnn(train_loader, test_loader)
    cnn_metrics = compute_metrics(y_true, y_pred_cnn, 'CNN')
    print(f'  CNN Test Accuracy: {cnn_metrics["accuracy"]}%')

    # Train ML models
    print('\n[3/3] Training ML models...')
    X_train, y_train, X_test, y_test = get_flat_data()
    ml_results = train_ml_models(X_train, y_train, X_test, y_test)

    # Combine all results
    all_results = {'CNN (Deep Learning)': cnn_metrics}
    all_results.update(ml_results)

    # Save metrics and class mapping
    with open('models_info.json', 'w') as f:
        json.dump({
            'models': all_results,
            'class_to_idx': class_to_idx,
            'img_size': IMG_SIZE
        }, f, indent=2)

    print('\n' + '=' * 50)
    print('Results Summary:')
    print('=' * 50)
    for name, metrics in all_results.items():
        print(f'  {name}: Accuracy={metrics["accuracy"]}% F1={metrics["f1"]}%')

    print(f'\nFiles saved:')
    print(f'  brain_cnn_model.pth  (CNN model weights)')
    print(f'  ml_model.pkl         (Best ML model)')
    print(f'  models_info.json     (All metrics)')
    print('Done!')
