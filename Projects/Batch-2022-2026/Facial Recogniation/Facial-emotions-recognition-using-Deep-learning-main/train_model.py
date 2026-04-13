"""
CNN Model Training for Facial Emotion Recognition
- Trains a 4-layer CNN on synthetic 48x48 grayscale face images
- Generates evaluation charts (dark theme)
- Trains ML baselines (Random Forest, SVM, Logistic Regression)
- Saves model and metrics
"""

import os
import json
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    precision_score, recall_score, f1_score
)
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'Dataset')
CHARTS_DIR = os.path.join(BASE_DIR, 'static', 'charts')
MODEL_PATH = os.path.join(BASE_DIR, 'emotion_cnn_model.pth')
METRICS_PATH = os.path.join(BASE_DIR, 'models_info.json')

EMOTIONS = ['Happy', 'Sad', 'Angry', 'Surprise', 'Fear', 'Disgust', 'Neutral']
IMG_SIZE = 48
BATCH_SIZE = 64
EPOCHS = 20
LEARNING_RATE = 0.001

# Dark theme for charts
plt.style.use('dark_background')
CHART_COLORS = {
    'primary': '#8b5cf6',
    'secondary': '#a78bfa',
    'accent': '#c4b5fd',
    'bg': '#1a1a2e',
    'grid': '#2d2d44',
    'text': '#e2e8f0'
}


def load_images(split='train'):
    """Load images from dataset directory."""
    images = []
    labels = []
    split_dir = os.path.join(DATASET_DIR, split)

    for idx, emotion in enumerate(EMOTIONS):
        emotion_dir = os.path.join(split_dir, emotion)
        if not os.path.exists(emotion_dir):
            print(f"  Warning: {emotion_dir} not found")
            continue
        files = sorted([f for f in os.listdir(emotion_dir) if f.endswith('.png')])
        for fname in files:
            img = Image.open(os.path.join(emotion_dir, fname)).convert('L')
            img = img.resize((IMG_SIZE, IMG_SIZE))
            img_array = np.array(img, dtype=np.float32) / 255.0
            images.append(img_array)
            labels.append(idx)

    return np.array(images), np.array(labels)


class EmotionCNN(nn.Module):
    """4-layer CNN for facial emotion classification."""

    def __init__(self, num_classes=7):
        super(EmotionCNN, self).__init__()

        self.features = nn.Sequential(
            # Block 1: Conv(1→32) + BN + ReLU + MaxPool → 24×24
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),

            # Block 2: Conv(32→64) + BN + ReLU + MaxPool → 12×12
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),

            # Block 3: Conv(64→128) + BN + ReLU + MaxPool → 6×6
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),

            # Block 4: Conv(128→256) + BN + ReLU + MaxPool → 3×3
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256 * 3 * 3, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


def get_device():
    """Get best available device."""
    if torch.backends.mps.is_available():
        return torch.device('mps')
    elif torch.cuda.is_available():
        return torch.device('cuda')
    return torch.device('cpu')


def train_cnn(X_train, y_train, X_test, y_test, device):
    """Train CNN model and return history."""
    print("\n" + "=" * 60)
    print("Training CNN Model")
    print("=" * 60)

    # Prepare tensors
    X_train_t = torch.FloatTensor(X_train).unsqueeze(1).to(device)
    y_train_t = torch.LongTensor(y_train).to(device)
    X_test_t = torch.FloatTensor(X_test).unsqueeze(1).to(device)
    y_test_t = torch.LongTensor(y_test).to(device)

    train_dataset = TensorDataset(X_train_t, y_train_t)
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

    test_dataset = TensorDataset(X_test_t, y_test_t)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

    model = EmotionCNN(num_classes=7).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    history = {
        'train_acc': [], 'val_acc': [],
        'train_loss': [], 'val_loss': []
    }

    for epoch in range(EPOCHS):
        # Training
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0

        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * batch_X.size(0)
            _, predicted = torch.max(outputs, 1)
            train_correct += (predicted == batch_y).sum().item()
            train_total += batch_y.size(0)

        # Validation
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0

        with torch.no_grad():
            for batch_X, batch_y in test_loader:
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                val_loss += loss.item() * batch_X.size(0)
                _, predicted = torch.max(outputs, 1)
                val_correct += (predicted == batch_y).sum().item()
                val_total += batch_y.size(0)

        train_acc = train_correct / train_total
        val_acc = val_correct / val_total
        train_loss_avg = train_loss / train_total
        val_loss_avg = val_loss / val_total

        history['train_acc'].append(train_acc)
        history['val_acc'].append(val_acc)
        history['train_loss'].append(train_loss_avg)
        history['val_loss'].append(val_loss_avg)

        print(f"  Epoch {epoch + 1:2d}/{EPOCHS} | "
              f"Train Loss: {train_loss_avg:.4f} | Train Acc: {train_acc:.4f} | "
              f"Val Loss: {val_loss_avg:.4f} | Val Acc: {val_acc:.4f}")

    # Save model
    torch.save(model.state_dict(), MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")

    # Get predictions for evaluation
    model.eval()
    all_preds = []
    with torch.no_grad():
        for batch_X, batch_y in test_loader:
            outputs = model(batch_X)
            _, predicted = torch.max(outputs, 1)
            all_preds.extend(predicted.cpu().numpy())

    return model, history, np.array(all_preds)


def generate_charts(history, y_test, y_pred):
    """Generate evaluation charts with dark theme."""
    os.makedirs(CHARTS_DIR, exist_ok=True)
    print("\nGenerating evaluation charts...")

    # 1. Training & Validation Accuracy
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(CHART_COLORS['bg'])
    ax.set_facecolor(CHART_COLORS['bg'])
    epochs = range(1, len(history['train_acc']) + 1)
    ax.plot(epochs, history['train_acc'], color=CHART_COLORS['primary'],
            linewidth=2, marker='o', markersize=4, label='Training Accuracy')
    ax.plot(epochs, history['val_acc'], color='#22d3ee',
            linewidth=2, marker='s', markersize=4, label='Validation Accuracy')
    ax.set_xlabel('Epoch', color=CHART_COLORS['text'], fontsize=12)
    ax.set_ylabel('Accuracy', color=CHART_COLORS['text'], fontsize=12)
    ax.set_title('Training & Validation Accuracy', color=CHART_COLORS['text'], fontsize=14, fontweight='bold')
    ax.legend(facecolor=CHART_COLORS['bg'], edgecolor=CHART_COLORS['grid'])
    ax.grid(True, alpha=0.3, color=CHART_COLORS['grid'])
    ax.tick_params(colors=CHART_COLORS['text'])
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, 'accuracy.png'), dpi=150,
                facecolor=CHART_COLORS['bg'], bbox_inches='tight')
    plt.close()
    print("  1/5 Accuracy chart saved")

    # 2. Training & Validation Loss
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(CHART_COLORS['bg'])
    ax.set_facecolor(CHART_COLORS['bg'])
    ax.plot(epochs, history['train_loss'], color=CHART_COLORS['primary'],
            linewidth=2, marker='o', markersize=4, label='Training Loss')
    ax.plot(epochs, history['val_loss'], color='#f97316',
            linewidth=2, marker='s', markersize=4, label='Validation Loss')
    ax.set_xlabel('Epoch', color=CHART_COLORS['text'], fontsize=12)
    ax.set_ylabel('Loss', color=CHART_COLORS['text'], fontsize=12)
    ax.set_title('Training & Validation Loss', color=CHART_COLORS['text'], fontsize=14, fontweight='bold')
    ax.legend(facecolor=CHART_COLORS['bg'], edgecolor=CHART_COLORS['grid'])
    ax.grid(True, alpha=0.3, color=CHART_COLORS['grid'])
    ax.tick_params(colors=CHART_COLORS['text'])
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, 'loss.png'), dpi=150,
                facecolor=CHART_COLORS['bg'], bbox_inches='tight')
    plt.close()
    print("  2/5 Loss chart saved")

    # 3. Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor(CHART_COLORS['bg'])
    ax.set_facecolor(CHART_COLORS['bg'])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Purples',
                xticklabels=EMOTIONS, yticklabels=EMOTIONS, ax=ax,
                linewidths=0.5, linecolor=CHART_COLORS['grid'])
    ax.set_xlabel('Predicted', color=CHART_COLORS['text'], fontsize=12)
    ax.set_ylabel('Actual', color=CHART_COLORS['text'], fontsize=12)
    ax.set_title('Confusion Matrix', color=CHART_COLORS['text'], fontsize=14, fontweight='bold')
    ax.tick_params(colors=CHART_COLORS['text'])
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, 'confusion_matrix.png'), dpi=150,
                facecolor=CHART_COLORS['bg'], bbox_inches='tight')
    plt.close()
    print("  3/5 Confusion matrix saved")

    # 4. Per-Class Accuracy Bar Chart
    per_class_acc = []
    for i, emotion in enumerate(EMOTIONS):
        mask = y_test == i
        if mask.sum() > 0:
            acc = (y_pred[mask] == i).sum() / mask.sum()
        else:
            acc = 0
        per_class_acc.append(acc)

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(CHART_COLORS['bg'])
    ax.set_facecolor(CHART_COLORS['bg'])
    colors = [CHART_COLORS['primary'] if a >= 0.7 else '#ef4444' for a in per_class_acc]
    bars = ax.bar(EMOTIONS, per_class_acc, color=colors, edgecolor=CHART_COLORS['accent'], linewidth=0.5)
    for bar, acc in zip(bars, per_class_acc):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f'{acc:.1%}', ha='center', va='bottom', color=CHART_COLORS['text'], fontsize=10)
    ax.set_xlabel('Emotion', color=CHART_COLORS['text'], fontsize=12)
    ax.set_ylabel('Accuracy', color=CHART_COLORS['text'], fontsize=12)
    ax.set_title('Per-Class Accuracy', color=CHART_COLORS['text'], fontsize=14, fontweight='bold')
    ax.set_ylim(0, 1.15)
    ax.grid(True, axis='y', alpha=0.3, color=CHART_COLORS['grid'])
    ax.tick_params(colors=CHART_COLORS['text'])
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, 'per_class_accuracy.png'), dpi=150,
                facecolor=CHART_COLORS['bg'], bbox_inches='tight')
    plt.close()
    print("  4/5 Per-class accuracy chart saved")

    # 5. Classification Report Heatmap
    report = classification_report(y_test, y_pred, target_names=EMOTIONS, output_dict=True)
    metrics_data = []
    for emotion in EMOTIONS:
        metrics_data.append([
            report[emotion]['precision'],
            report[emotion]['recall'],
            report[emotion]['f1-score']
        ])
    metrics_array = np.array(metrics_data)

    fig, ax = plt.subplots(figsize=(8, 7))
    fig.patch.set_facecolor(CHART_COLORS['bg'])
    ax.set_facecolor(CHART_COLORS['bg'])
    sns.heatmap(metrics_array, annot=True, fmt='.3f', cmap='Purples',
                xticklabels=['Precision', 'Recall', 'F1-Score'],
                yticklabels=EMOTIONS, ax=ax, vmin=0, vmax=1,
                linewidths=0.5, linecolor=CHART_COLORS['grid'])
    ax.set_title('Classification Report Heatmap', color=CHART_COLORS['text'], fontsize=14, fontweight='bold')
    ax.tick_params(colors=CHART_COLORS['text'])
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, 'classification_report.png'), dpi=150,
                facecolor=CHART_COLORS['bg'], bbox_inches='tight')
    plt.close()
    print("  5/5 Classification report heatmap saved")


def train_ml_baselines(X_train, y_train, X_test, y_test):
    """Train ML baseline models and return metrics."""
    print("\n" + "=" * 60)
    print("Training ML Baseline Models")
    print("=" * 60)

    # Flatten images for ML models
    X_train_flat = X_train.reshape(X_train.shape[0], -1)
    X_test_flat = X_test.reshape(X_test.shape[0], -1)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_flat)
    X_test_scaled = scaler.transform(X_test_flat)

    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        'SVM': SVC(kernel='rbf', random_state=42),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1)
    }

    results = {}
    for name, model in models.items():
        print(f"\n  Training {name}...")
        if name == 'Random Forest':
            model.fit(X_train_flat, y_train)
            y_pred = model.predict(X_test_flat)
        else:
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted')
        rec = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')

        results[name] = {
            'accuracy': round(acc, 4),
            'precision': round(prec, 4),
            'recall': round(rec, 4),
            'f1_score': round(f1, 4)
        }
        print(f"    Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f} | F1: {f1:.4f}")

    return results


def main():
    print("=" * 60)
    print("Facial Emotion Recognition — Model Training Pipeline")
    print("=" * 60)

    # Load data
    print("\nLoading training data...")
    X_train, y_train = load_images('train')
    print(f"  Training set: {X_train.shape[0]} images")

    print("Loading test data...")
    X_test, y_test = load_images('test')
    print(f"  Test set: {X_test.shape[0]} images")

    # Device
    device = get_device()
    print(f"\nUsing device: {device}")

    # Train CNN
    model, history, y_pred_cnn = train_cnn(X_train, y_train, X_test, y_test, device)

    # CNN metrics
    cnn_acc = accuracy_score(y_test, y_pred_cnn)
    cnn_prec = precision_score(y_test, y_pred_cnn, average='weighted')
    cnn_rec = recall_score(y_test, y_pred_cnn, average='weighted')
    cnn_f1 = f1_score(y_test, y_pred_cnn, average='weighted')
    print(f"\nCNN Test Results:")
    print(f"  Accuracy: {cnn_acc:.4f} | Precision: {cnn_prec:.4f} | Recall: {cnn_rec:.4f} | F1: {cnn_f1:.4f}")

    # Generate charts
    generate_charts(history, y_test, y_pred_cnn)

    # Train ML baselines
    ml_results = train_ml_baselines(X_train, y_train, X_test, y_test)

    # Save all metrics
    all_metrics = {
        'CNN (Deep Learning)': {
            'accuracy': round(cnn_acc, 4),
            'precision': round(cnn_prec, 4),
            'recall': round(cnn_rec, 4),
            'f1_score': round(cnn_f1, 4),
            'epochs': EPOCHS,
            'batch_size': BATCH_SIZE,
            'learning_rate': LEARNING_RATE,
            'architecture': '4-layer CNN (32→64→128→256) + FC (512→256→7)',
            'training_history': history
        },
        **ml_results
    }

    with open(METRICS_PATH, 'w') as f:
        json.dump(all_metrics, f, indent=2)
    print(f"\nAll metrics saved to {METRICS_PATH}")

    print("\n" + "=" * 60)
    print("Training pipeline complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
