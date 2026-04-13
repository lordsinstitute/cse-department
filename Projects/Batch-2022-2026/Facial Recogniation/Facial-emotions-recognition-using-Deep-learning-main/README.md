# Facial Emotion Recognition Using Deep Learning

A web-based facial emotion recognition system that uses a Convolutional Neural Network (CNN) to detect and classify 7 human emotions from facial images. Built with PyTorch for deep learning and Flask for the web interface.

## Features

- **Real-time Emotion Detection** — Upload a face image and get instant emotion classification with confidence score
- **7 Emotion Classes** — Happy, Sad, Angry, Surprise, Fear, Disgust, Neutral
- **Deep Learning CNN** — 4-layer convolutional neural network with BatchNorm and Dropout
- **Face Detection** — OpenCV Haar Cascade for automatic face localization
- **User Authentication** — Secure login/register with password hashing
- **Prediction History** — Track all past predictions with images and results
- **Model Dashboard** — Training charts, confusion matrix, and model comparison
- **ML Baselines** — Compare CNN with Random Forest, SVM, and Logistic Regression
- **Responsive Dark UI** — Violet-themed Bootstrap 5 dark mode interface

## Screenshots

### Prediction Page
Upload a face image → detect face → classify emotion with confidence percentage.

### Model Dashboard
Training accuracy/loss charts, confusion matrix, per-class accuracy, and classification report heatmap.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python, Flask |
| Deep Learning | PyTorch (CNN) |
| Face Detection | OpenCV (Haar Cascade) |
| ML Models | scikit-learn (RF, SVM, LR) |
| Database | SQLite |
| Frontend | Bootstrap 5, Font Awesome |
| Charts | Matplotlib, Seaborn |

## CNN Architecture

```
Input: 1 x 48 x 48 (Grayscale)
├── Conv Block 1: Conv2d(1→32) + BatchNorm + ReLU + MaxPool → 32 x 24 x 24
├── Conv Block 2: Conv2d(32→64) + BatchNorm + ReLU + MaxPool → 64 x 12 x 12
├── Conv Block 3: Conv2d(64→128) + BatchNorm + ReLU + MaxPool → 128 x 6 x 6
├── Conv Block 4: Conv2d(128→256) + BatchNorm + ReLU + MaxPool → 256 x 3 x 3
├── Flatten → 2304
├── FC: Linear(2304→512) + ReLU + Dropout(0.5)
├── FC: Linear(512→256) + ReLU + Dropout(0.3)
└── Output: Linear(256→7) → 7 emotion classes
```

## Installation (Windows)

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Eng-Proj-Col/Facial-emotions-recognition-using-Deep-learning.git
   cd Facial-emotions-recognition-using-Deep-learning
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate the synthetic dataset**
   ```bash
   python generate_dataset.py
   ```
   This creates 4,214 images (3,500 training + 700 testing + 14 samples) across 7 emotion categories.

5. **Train the CNN model**
   ```bash
   python train_model.py
   ```
   This trains the CNN, generates 5 evaluation charts, trains ML baselines, and saves all metrics.

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open in browser**
   ```
   http://localhost:5018
   ```

8. **Login with default credentials**
   ```
   Username: admin
   Password: admin123
   ```

## Docker Installation

```bash
docker build -t facial-emotion-recognition .
docker run -p 5018:5018 facial-emotion-recognition
```

## Project Structure

```
├── generate_dataset.py          # Synthetic face image generator (7 emotions)
├── train_model.py               # CNN training + charts + ML baselines
├── app.py                       # Flask web application
├── emotion_cnn_model.pth        # Trained PyTorch model
├── models_info.json             # Model comparison metrics
├── Dataset/
│   ├── train/{7 emotions}/      # 3,500 training images
│   ├── test/{7 emotions}/       # 700 test images
│   └── samples/                 # 14 downloadable sample images
├── static/
│   ├── charts/                  # 5 evaluation charts
│   └── uploads/                 # User-uploaded images
├── templates/
│   ├── base.html                # Violet dark theme layout
│   ├── login.html               # Login page
│   ├── register.html            # Registration page
│   ├── home.html                # Dashboard with stats
│   ├── predict.html             # Image upload + emotion result
│   ├── history.html             # Past predictions
│   ├── dashboard.html           # Model metrics & charts
│   └── about.html               # Project information
├── requirements.txt
├── Dockerfile
└── README.md
```

## How It Works

1. **Upload** — User uploads a face image (JPG, PNG, etc.)
2. **Face Detection** — OpenCV Haar Cascade locates the face in the image
3. **Preprocessing** — Face is cropped, converted to grayscale, resized to 48x48
4. **CNN Classification** — 4-layer CNN processes the face and outputs emotion probabilities
5. **Result** — Detected emotion and confidence percentage are displayed

## API Routes

| Route | Method | Auth | Description |
|-------|--------|------|-------------|
| `/` | GET | No | Redirect to home or login |
| `/login` | GET/POST | No | User login |
| `/register` | GET/POST | No | User registration |
| `/logout` | GET | Yes | Logout and clear session |
| `/home` | GET | Yes | Dashboard with stats and recent predictions |
| `/predict` | GET/POST | Yes | Upload image and detect emotion |
| `/history` | GET | Yes | View past predictions |
| `/dashboard` | GET | Yes | Model metrics and charts |
| `/about` | GET | Yes | Project info and emotions table |
| `/download_sample/<file>` | GET | Yes | Download sample test image |

## Model Performance

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| **CNN (Deep Learning)** | **100.00%** | **100.00%** | **100.00%** | **100.00%** |
| Logistic Regression | 83.29% | 83.27% | 83.29% | 83.24% |
| Random Forest | 77.43% | 77.01% | 77.43% | 77.08% |
| SVM | 65.00% | 66.38% | 65.00% | 65.12% |
