# Social Media Hate Speech Analysis

A machine learning-powered web application that classifies social media text into Hate Speech, Offensive, or Clean categories using NLP and TF-IDF vectorization with multiple ML models.

## Features

- **Text Classification** — Analyze any social media text for hate speech, offensive language, or clean content
- **Multiple ML Models** — 6 models trained and compared (Logistic Regression, Naive Bayes, SVM, Random Forest, Gradient Boosting, KNN)
- **NLP Pipeline** — Text preprocessing with stopword removal, TF-IDF vectorization with bigrams
- **EDA Visualizations** — 8 data analysis charts (class distribution, word clouds, feature importance, model comparison)
- **Analysis History** — Per-user history of all analyses with confidence scores
- **Model Dashboard** — Side-by-side comparison of all models with Accuracy, Precision, Recall, F1 metrics
- **User Authentication** — Login/register with password hashing
- **Dark Theme UI** — Bootstrap 5 dark gradient design

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python + Flask |
| Frontend | Jinja2 Templates + Bootstrap 5 |
| Database | SQLite |
| ML Library | scikit-learn |
| NLP | NLTK + TF-IDF |
| Data Analysis | pandas + NumPy |
| Visualization | matplotlib + seaborn |
| Authentication | Werkzeug (PBKDF2-SHA256) |
| Container | Docker |

## Project Structure

```
code/
├── app.py                    # Flask application
├── generate_dataset.py       # Synthetic dataset generator
├── train_model.py            # Model training + EDA visualization
├── hate_speech_model.pkl     # Trained best model
├── tfidf_vectorizer.pkl      # TF-IDF vectorizer
├── models_info.json          # Model metrics and config
├── hate_speech_data.csv      # Training dataset (15,000 rows)
├── templates/
│   ├── base.html             # Dark theme layout + navbar
│   ├── login.html            # Login page
│   ├── register.html         # Registration page
│   ├── home.html             # Dashboard
│   ├── predict.html          # Text analysis form + results
│   ├── history.html          # Analysis history
│   ├── visualize.html        # EDA visualizations
│   ├── dashboard.html        # Model comparison
│   └── about.html            # Project info
├── static/vis/               # EDA chart images
├── Dockerfile
├── README.md
└── PROJECT_EXPLANATION.md
```

## Installation (Windows)

### Prerequisites

- **Python 3.8 or higher** — Download from [https://python.org](https://python.org)
- **Git** — Download from [https://git-scm.com](https://git-scm.com)

### Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd code
   ```

2. **Install dependencies:**
   ```bash
   pip install flask scikit-learn pandas numpy matplotlib seaborn joblib werkzeug nltk
   ```

3. **Download NLTK data:**
   ```bash
   python -c "import nltk; nltk.download('stopwords')"
   ```

4. **Generate dataset and train model:**
   ```bash
   python generate_dataset.py
   python train_model.py
   ```

5. **Start the application:**
   ```bash
   python app.py
   ```

6. **Open in browser:**
   ```
   http://127.0.0.1:5007
   ```

### Demo Login

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |

## Docker Setup

```bash
docker build -t hate-speech .
docker run -p 5007:5007 hate-speech
```

Open `http://127.0.0.1:5007` in your browser.

## Classification Categories

| Category | Description | Color |
|----------|-------------|-------|
| Hate Speech | Content targeting protected groups (race, religion, gender, nationality) | Red |
| Offensive | Rude, profane, insulting language not targeting specific groups | Orange |
| Clean | Normal, non-harmful social media content | Green |

## Model Performance

| Model | Accuracy | Precision | Recall | F1 Score |
|-------|----------|-----------|--------|----------|
| **Logistic Regression** | **94.83%** | **94.87%** | **94.83%** | **94.81%** |
| Naive Bayes | 94.83% | 94.87% | 94.83% | 94.81% |
| SVM | 94.83% | 94.87% | 94.83% | 94.81% |
| KNN | 94.73% | 94.77% | 94.73% | 94.71% |
| Gradient Boosting | 94.50% | 94.53% | 94.50% | 94.47% |
| Random Forest | 94.17% | 94.20% | 94.17% | 94.14% |

## Test Cases

### Test Case 1: User Registration
1. Go to `/register`, fill Name=Alice, Username=alice, Password=pass123
2. Click Register
- **Expected:** Redirect to login with success message

### Test Case 2: Login
1. Go to `/login`, enter admin / admin123
- **Expected:** Redirect to dashboard

### Test Case 3: Dashboard
1. Login → see dashboard with analysis count and recent analyses
- **Expected:** Stats cards and recent analyses table displayed

### Test Case 4: Analyze Clean Text
1. Go to `/predict`
2. Enter: "I love spending time with my family on weekends"
3. Click Analyze
- **Expected:** Classification = "Clean" with green badge and high confidence

### Test Case 5: Analyze Hate Speech
1. Enter: "All immigrants are disgusting and should be deported"
- **Expected:** Classification = "Hate Speech" with red badge

### Test Case 6: Analyze Offensive Text
1. Enter: "You're such a stupid idiot go away"
- **Expected:** Classification = "Offensive" with orange badge

### Test Case 7: Analysis History
1. After making several analyses, go to `/history`
- **Expected:** Table showing all past analyses with text, classification, confidence, date

### Test Case 8: EDA Visualizations
1. Go to `/visualize`
- **Expected:** 8 charts: class distribution, text length, word count, word clouds (hate + clean), top features, model comparison, confusion matrix

### Test Case 9: Model Dashboard
1. Go to `/dashboard`
- **Expected:** Cards and table showing all 6 models with Accuracy, Precision, Recall, F1. Best model marked.

### Test Case 10: About Page
1. Go to `/about`
- **Expected:** Project info, NLP pipeline, tech stack, ML models list

### Test Case 11: Invalid Login
1. Try logging in with wrong credentials
- **Expected:** Error message "Invalid username or password"

### Test Case 12: Duplicate Registration
1. Try registering with existing username "admin"
- **Expected:** Error message "Username already exists"

### Test Case 13: Access Control
1. Logout → try accessing `/predict` directly
- **Expected:** Redirect to login page

### Test Case 14: Admin Stats
1. Login as admin → dashboard shows total users and total analyses
- **Expected:** Admin section visible with system-wide statistics

### Test Case 15: Form Validation
1. Submit analysis form with empty text
- **Expected:** Browser validation prevents submission

### Test Case 16: Docker Deployment
1. `docker build -t hate-speech .`
2. `docker run -p 5007:5007 hate-speech`
- **Expected:** App accessible at http://127.0.0.1:5007

## Team

| Roll Number | Name |
|-------------|------|
| 160922733155 | Syed Muzammil Hussaini |
| 160922733136 | Omer Farooq |
| 160922733157 | S.S Quadri |
| 160922733134 | Mustafa Wasif Hussain |

## Notes

- The SQLite database (`hate_speech.db`) is auto-created on first run with an admin account
- Delete `hate_speech.db` and restart to reset all data
- The model is pre-trained and saved as `hate_speech_model.pkl` — no training needed at runtime
- Run `generate_dataset.py` and `train_model.py` to regenerate the dataset and retrain models
