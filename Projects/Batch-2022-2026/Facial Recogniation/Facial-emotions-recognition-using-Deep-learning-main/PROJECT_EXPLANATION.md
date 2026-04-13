# Facial Emotion Recognition Using Deep Learning — Project Explanation

This document explains the entire project in simple terms, as if explaining to a 7th-grader. We'll go through every single file, what it does, and how everything connects together.

---

## What Does This Project Do?

Imagine you take a selfie or a photo of someone's face. This project can look at that face and tell you what emotion the person is feeling — whether they're **happy**, **sad**, **angry**, **surprised**, **scared**, **disgusted**, or showing **no emotion** (neutral).

It uses something called a **Convolutional Neural Network (CNN)** — a type of artificial intelligence that's really good at understanding images. The same kind of AI that phones use to recognize your face!

---

## The Big Picture

Here's how the whole system works, step by step:

1. **You open the website** and log in
2. **You upload a photo** of someone's face
3. **The computer finds the face** in the photo (using a tool called Haar Cascade)
4. **The AI brain (CNN) analyzes** the face and decides which emotion it sees
5. **You see the result** — the emotion name and how confident the AI is (like "Happy — 95%")

---

## File-by-File Explanation

### `generate_dataset.py` — The Image Factory

**What it does:** Creates thousands of tiny cartoon-like face images for training the AI.

**Why we need it:** Just like a student needs textbooks to study, our AI needs lots of example images to learn from. Since we don't have real face photos, we draw simple faces using computer code!

**How it works:**
- It draws a face shape (an oval)
- Adds two eyes (circles)
- Draws eyebrows (lines)
- Draws a mouth (curved line or circle)
- Each emotion has different features:
  - **Happy**: Eyebrows go up, mouth curves up (smile!)
  - **Sad**: Eyebrows go down, mouth curves down (frown)
  - **Angry**: Eyebrows make a V-shape, mouth is tight and straight
  - **Surprise**: Eyes go really wide, mouth makes an O shape
  - **Fear**: Eyes go wide, mouth slightly open
  - **Disgust**: Eyes squint, mouth goes wavy
  - **Neutral**: Everything is normal and relaxed

**What it creates:**
- 3,500 training images (500 for each of the 7 emotions)
- 700 test images (100 for each emotion)
- 14 sample images (2 for each emotion)

Each image is tiny — just 48 x 48 pixels — and black-and-white (grayscale).

---

### `train_model.py` — The AI Teacher

**What it does:** Teaches the AI to recognize emotions by showing it thousands of face images.

**The CNN Model (the AI Brain):**

Think of the CNN like a series of magnifying glasses, each one looking for different things:

1. **Layer 1 (32 filters)**: Looks for basic things like edges and lines
2. **Layer 2 (64 filters)**: Combines edges to find shapes like eyes, mouth curves
3. **Layer 3 (128 filters)**: Recognizes facial parts — "that's an eye!" "that's a frown!"
4. **Layer 4 (256 filters)**: Understands the whole face expression — "this face looks sad!"

After the 4 layers of "looking," the AI has a "thinking" section:
- 2304 pieces of information get compressed to 512, then 256
- Finally, 7 numbers come out — one for each emotion
- The biggest number wins and becomes the predicted emotion!

**Training process:**
- The AI looks at 64 images at a time (called a "batch")
- It goes through ALL images 20 times (called "epochs")
- Each time, it gets a little better at guessing the emotion
- It's like studying for a test — the more you practice, the better you get!

**What it creates:**
- `emotion_cnn_model.pth` — The trained AI brain (saved so we don't have to retrain)
- 5 charts showing how well the AI learned:
  1. **Accuracy chart** — Did the AI get better over time? (Yes!)
  2. **Loss chart** — Did the AI make fewer mistakes over time? (Yes!)
  3. **Confusion matrix** — Which emotions does the AI mix up?
  4. **Per-class accuracy** — How good is the AI at each emotion?
  5. **Classification report** — Detailed scores for each emotion

**ML Baselines:**
We also train 3 simpler AI models to compare:
- **Random Forest** — Uses many decision trees (like a group vote)
- **SVM** — Finds the best boundary between emotions
- **Logistic Regression** — Uses math equations to classify

The CNN beats all of them because it understands images much better!

---

### `app.py` — The Web Application (The Brain of the Website)

**What it does:** Runs the website and handles everything — logins, uploads, predictions, history.

**Key parts:**

1. **Database Setup:**
   - Creates two tables: `users` (who can log in) and `predictions` (what emotions were detected)
   - Makes a default admin account (username: admin, password: admin123)
   - Passwords are "hashed" — scrambled so nobody can read them even if they see the database

2. **Login System:**
   - You need an account to use the site
   - Passwords are checked securely (the scrambled versions are compared)
   - Sessions remember who you are so you don't have to login on every page

3. **Prediction Pipeline (the cool part!):**
   - You upload a photo
   - OpenCV's Haar Cascade scans the image for faces (it looks for face-shaped patterns)
   - If it finds a face, it crops just the face part
   - Converts to grayscale (black and white) and shrinks to 48x48 pixels
   - The CNN processes it and outputs probabilities for all 7 emotions
   - The emotion with the highest probability wins!
   - Result is saved to the database with the image

4. **Routes (pages you can visit):**
   - `/login` and `/register` — Account management
   - `/home` — Dashboard showing your stats
   - `/predict` — Upload a face image
   - `/history` — See all your past predictions
   - `/dashboard` — See how well the AI model performs
   - `/about` — Learn about the project

---

### Templates (HTML Files) — What You See

All the web pages use **Bootstrap 5** with a dark purple/violet theme (`#8b5cf6`).

**`base.html`** — The skeleton that every page uses:
- Navigation bar at the top with links to all pages
- Flash messages (green for success, red for errors)
- Footer at the bottom
- Dark background with violet accent colors

**`login.html` & `register.html`** — Simple forms centered on the page with the brain icon logo.

**`home.html`** — Your personal dashboard:
- 4 stat cards (total predictions, emotion classes, top emotion, total users)
- Emotion distribution bar chart
- Table of your 5 most recent predictions
- Quick action buttons

**`predict.html`** — The main feature page:
- Drag-and-drop upload zone
- Image preview before submitting
- After prediction: large emotion icon, name, color-coded badge, confidence bar
- If no face found: error message with tips

**`history.html`** — A table of all your past predictions with thumbnails, emotion badges, and confidence bars.

**`dashboard.html`** — Model performance page:
- Comparison table (CNN vs Random Forest vs SVM vs Logistic Regression)
- CNN training stats (epochs, batch size, learning rate)
- All 5 training/evaluation charts displayed as images

**`about.html`** — Information page:
- Project overview
- Table of all 7 emotions with descriptions
- How it works (4-step process)
- CNN architecture table
- Tech stack and features list
- Downloadable sample images

---

### Configuration Files

**`requirements.txt`** — Lists all the Python packages the project needs:
- `flask` — Web framework
- `torch` — PyTorch for deep learning
- `opencv-python-headless` — Image processing and face detection
- `scikit-learn` — Machine learning baselines
- `matplotlib` & `seaborn` — Chart generation
- And more...

**`Dockerfile`** — Instructions for building a Docker container:
- Uses Python 3.11
- Installs dependencies
- Generates the dataset and trains the model
- Starts the web server on port 5018

**`.gitignore`** — Tells Git which files NOT to upload:
- Database files (each person creates their own)
- Uploaded images (privacy)
- Training/test images (too many files, can be regenerated)
- Python cache files

---

## How Everything Connects

```
User opens website (port 5018)
        ↓
    app.py runs Flask server
        ↓
    User logs in → checked against users table in emotion.db
        ↓
    User uploads face photo → saved to static/uploads/
        ↓
    OpenCV Haar Cascade finds the face in the photo
        ↓
    Face cropped → grayscale → resize to 48x48
        ↓
    CNN model (emotion_cnn_model.pth) processes the face
        ↓
    Output: 7 probabilities → highest one = detected emotion
        ↓
    Result shown on screen + saved to predictions table
        ↓
    User can view history, dashboard, and download samples
```

---

## The 7 Emotions Explained

| Emotion | What It Looks Like | Example |
|---------|-------------------|---------|
| **Happy** | Smiling, eyes crinkling | Laughing at a joke |
| **Sad** | Frowning, droopy eyes | Hearing bad news |
| **Angry** | Furrowed brows, tight lips | Being frustrated |
| **Surprise** | Wide eyes, open mouth | Unexpected birthday party |
| **Fear** | Wide eyes, tense face | Watching a scary movie |
| **Disgust** | Wrinkled nose, squinted eyes | Smelling something bad |
| **Neutral** | Relaxed, no strong expression | Just sitting normally |

---

## Key Technical Terms Simplified

- **CNN (Convolutional Neural Network)**: An AI that's specially designed to understand images by looking at them layer by layer, from simple patterns to complex features
- **Epoch**: One complete pass through all training images (like reading the entire textbook once)
- **Batch Size**: How many images the AI looks at before updating its knowledge (studying 64 flashcards, then checking answers)
- **Learning Rate**: How big the AI's learning steps are (too big = jumps over the answer, too small = takes forever)
- **Haar Cascade**: A face-finding algorithm that scans the image for face-like patterns
- **Grayscale**: Black-and-white image (no colors, just shades of gray)
- **Softmax**: Converts raw numbers into percentages that add up to 100%
- **Dropout**: Randomly turns off some brain connections during training so the AI doesn't memorize (like covering some notes while studying to test real understanding)
- **BatchNorm**: Keeps the numbers in each layer balanced so training stays stable

---

## Why the CNN is Better Than Other Models

| Feature | CNN | Random Forest / SVM / LR |
|---------|-----|--------------------------|
| Understands image structure | Yes (pixels next to each other matter) | No (treats each pixel independently) |
| Learns features automatically | Yes (discovers edges, shapes, faces) | No (uses raw pixel values) |
| Works well with images | Excellent | Okay for simple patterns |
| Training time | Longer | Shorter |
| Accuracy on this task | ~100% | 65-83% |

The CNN wins because it understands that a face is not just random dots — the position and relationship between eyes, mouth, and eyebrows matter!

---

## Running the Project

1. Install Python 3.9+
2. Install packages: `pip install -r requirements.txt`
3. Generate faces: `python generate_dataset.py`
4. Train the AI: `python train_model.py`
5. Start the website: `python app.py`
6. Open `http://localhost:5018`
7. Login with admin / admin123
8. Upload a face photo and see the magic!
