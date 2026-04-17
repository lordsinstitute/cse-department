# Brain Stroke Detection — AI-Based Medical Image Analysis Using Deep Learning

A web application that uses a Convolutional Neural Network (CNN) to detect brain strokes from CT scan images. Upload a brain CT image and the AI model will classify it as **Normal** or **Stroke Detected** with a confidence score.

## Features

- **CNN-Based Detection** — 4-layer CNN trained on brain CT images for binary classification
- **Image Upload** — Drag-and-drop or click to upload CT scan images (PNG, JPG, BMP, TIFF)
- **Real-Time Prediction** — Instant analysis with confidence percentage
- **Model Comparison** — CNN vs Random Forest vs SVM vs Logistic Regression performance charts
- **Scan History** — Track all past predictions with thumbnails and timestamps
- **Interactive Dashboard** — Chart.js visualizations for model metrics and prediction analytics
- **User Authentication** — Secure login/register with password hashing
- **Admin Panel** — System-wide statistics for administrators
- **Sample Images** — Pre-generated test images for quick testing
- **Docker Support** — Containerized deployment

## Tech Stack

- **Backend:** Python, Flask, SQLite, Werkzeug
- **Deep Learning:** PyTorch, TorchVision, CNN
- **Machine Learning:** Scikit-learn (Random Forest, SVM, Logistic Regression)
- **Image Processing:** Pillow (PIL), NumPy
- **Frontend:** Bootstrap 5, Chart.js, Jinja2, Bootstrap Icons

## Installation (Windows)

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository:**
```bash
git clone <repository-url>
cd code
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

For PyTorch on Windows (CPU only):
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

4. **Generate the dataset:**
```bash
python generate_dataset.py
```
This creates 1,000 synthetic CT brain images (800 train + 200 test) and 6 sample images.

5. **Train the models:**
```bash
python train_model.py
```
This trains the CNN and 3 ML models, saving weights and metrics.

6. **Run the application:**
```bash
python app.py
```
Open http://localhost:5010 in your browser.

7. **Login:**
- Username: `admin`
- Password: `admin123`

## Docker Deployment

```bash
docker build -t stroke-detection .
docker run -p 5010:5010 stroke-detection
```

## Project Structure

```
code/
├── app.py                  # Flask web application
├── train_model.py          # CNN + ML model training
├── generate_dataset.py     # Synthetic CT image generator
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker container config
├── .gitignore
├── .dockerignore
├── templates/
│   ├── base.html           # Dark theme layout
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── home.html           # Dashboard home with stats
│   ├── predict.html        # Image upload + prediction
│   ├── history.html        # Scan history table
│   ├── dashboard.html      # Model comparison charts
│   └── about.html          # Project info + architecture
├── static/
│   ├── uploads/            # User-uploaded images
│   └── test_samples/       # 6 sample test images
├── Dataset/                # Training/test images (generated)
├── stroke_cnn_model.pth    # Trained CNN weights (generated)
├── ml_model.pkl            # Trained Random Forest (generated)
└── models_info.json        # Model metrics (generated)
```

## CNN Architecture

```
Input: 1 x 128 x 128 (Grayscale CT Image)
    ↓
Conv2D(1→32, 3x3) + ReLU + MaxPool(2x2)
Conv2D(32→64, 3x3) + ReLU + MaxPool(2x2)
Conv2D(64→128, 3x3) + ReLU + MaxPool(2x2)
Conv2D(128→256, 3x3) + ReLU + MaxPool(2x2)
    ↓
Flatten (16,384) → Dense(256) + ReLU + Dropout(0.5)
    ↓
Dense(1) + Sigmoid → Normal / Stroke
```

## Model Performance

| Model | Accuracy | Precision | Recall | F1 Score |
|-------|----------|-----------|--------|----------|
| CNN (Deep Learning) | 100.0% | 100.0% | 100.0% | 100.0% |
| Random Forest | 99.0% | 100.0% | 98.0% | 99.0% |
| SVM | 97.0% | 97.0% | 97.0% | 97.0% |
| Logistic Regression | 95.5% | 98.9% | 92.0% | 95.3% |

## Test Cases

1. Register a new user → redirect to login page
2. Login as admin/admin123 → redirect to home page
3. Home page shows stats cards (total scans, stroke count, normal count)
4. Upload a normal CT sample → "Normal (No Stroke)" with high confidence
5. Upload a stroke CT sample → "Stroke Detected" with high confidence
6. Download sample images from home page
7. Result shows color-coded badge (red for stroke, green for normal)
8. History page shows all past predictions with thumbnails
9. Dashboard shows model accuracy bar chart
10. Dashboard shows F1 score comparison chart
11. Dashboard shows prediction distribution doughnut chart
12. Dashboard shows confidence distribution chart
13. About page shows stroke types and CNN architecture
14. Invalid login shows error message
15. Access /predict without login → redirect to login
16. Admin sees system-wide statistics on home page

## Default Credentials

- **Username:** admin
- **Password:** admin123
