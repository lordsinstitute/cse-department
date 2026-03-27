# Project Explanation — Brain Stroke Detection Using Deep Learning

## What Does This Project Do?

Imagine you're a doctor looking at a brain scan (called a CT scan) of a patient who came to the hospital feeling dizzy or weak on one side of their body. You need to quickly figure out if they're having a brain stroke — a very serious medical emergency where part of the brain stops getting blood.

This project is like having a super-smart computer assistant that can look at brain scan pictures and instantly tell the doctor: "This brain looks normal" or "Warning! This brain shows signs of a stroke!" It does this using something called a **Convolutional Neural Network (CNN)** — a type of artificial intelligence that's really good at understanding images.

---

## What Is a Brain Stroke?

A brain stroke happens when blood stops flowing to part of the brain. Without blood, brain cells start dying within minutes. There are two main types:

1. **Ischemic Stroke (87% of cases):** A blood clot blocks an artery going to the brain. Like a clogged pipe — water can't flow through. On a CT scan, the affected area appears **darker** than normal because the tissue is dying.

2. **Hemorrhagic Stroke (13% of cases):** A blood vessel in the brain bursts and bleeds. Like a pipe breaking — blood leaks everywhere. On a CT scan, the blood appears as a **bright white spot** because blood is denser than brain tissue.

Both types are medical emergencies. The faster you detect a stroke, the more brain you can save. That's why AI detection is so important — it can spot patterns in seconds that might take a human minutes or longer.

---

## How Does the AI Actually Work?

### Step 1: Getting the Picture Ready

When a doctor uploads a CT scan image, the computer first needs to prepare it:
- **Convert to grayscale** — CT scans are already gray, but we make sure it's in the right format
- **Resize to 128x128 pixels** — The AI needs all images to be the same size, like making sure all puzzle pieces are the same shape
- **Normalize** — Convert pixel values to numbers between 0 and 1 (the computer works better with small numbers)

### Step 2: The CNN Looks at the Image (Feature Extraction)

Think of the CNN like a series of magnifying glasses, each looking at different things:

**Layer 1 (32 filters):** Looks for basic patterns — edges, lines, bright/dark spots. Like noticing "there's a bright edge here" or "there's a dark area there."

**Layer 2 (64 filters):** Combines basic patterns into more complex ones — like recognizing "this group of edges looks like the outline of a ventricle" (ventricles are fluid-filled spaces in the brain).

**Layer 3 (128 filters):** Starts recognizing larger structures — "this is the midline of the brain" or "this dark patch doesn't look like a normal ventricle."

**Layer 4 (256 filters):** Sees the big picture — "there's an unusual dark region in one hemisphere that looks like dead tissue" or "everything looks symmetrical and healthy."

After each layer, there's a **MaxPooling** step that shrinks the image to focus on the most important features (like zooming out to see the forest instead of individual trees).

### Step 3: Making the Decision (Classification)

After the four layers extract features, the CNN has 16,384 numbers describing what it "sees" in the image. These go through:

1. **Dense Layer** (256 neurons) — Weighs all the features and combines them
2. **Dropout** (50%) — During training, randomly ignores half the neurons to prevent the AI from "memorizing" instead of "learning"
3. **Final Neuron** (1 output + Sigmoid) — Outputs a single number between 0 and 1:
   - Close to 0 = Normal brain
   - Close to 1 = Stroke detected

### Step 4: Showing the Result

The system shows:
- **Prediction:** "Normal (No Stroke)" or "Stroke Detected"
- **Confidence:** How sure the AI is (e.g., 97.5%)
- **Color-coded badge:** Green for normal, red for stroke
- **Medical advice:** "Consult a doctor immediately" if stroke is detected

---

## What Are the Other Models?

We don't just use the CNN — we also train three simpler models to compare:

### Random Forest
Imagine 100 people each looking at the brain scan and voting "stroke" or "normal." Each person looks at random parts of the image. The majority vote wins. This is essentially what Random Forest does — it creates 100 "decision trees" that each vote.

### SVM (Support Vector Machine)
Imagine drawing a line on a piece of paper to separate two groups of dots (stroke scans vs normal scans). SVM finds the best possible line that separates them with the maximum gap between the groups.

### Logistic Regression
The simplest model — it multiplies each pixel value by a weight, adds them all up, and if the total is above a threshold, it says "stroke." Like a very simple scoring system.

### Why Is CNN the Best?

The CNN achieves 100% accuracy while simpler models get 95-99%. That's because:
- **CNN understands spatial relationships** — it knows that a dark patch NEXT TO the midline is suspicious, while a dark ventricle IN THE CENTER is normal
- **Simpler models treat each pixel independently** — they don't understand that pixels near each other are related

---

## The Dataset

### How Were the Images Created?

Since we can't share real patient CT scans (privacy laws), we generate synthetic (computer-made) images that look like real CT scans:

**Normal Brain CT:**
- Black background (air around the skull)
- Bright oval (skull bone — appears white on CT)
- Gray oval inside (brain tissue)
- A vertical line down the middle (the falx cerebri — the membrane dividing left and right brain)
- Two small dark ovals (ventricles — fluid-filled spaces)
- Random gray patches (normal variations in gray/white matter)
- Blur and noise (to look realistic)

**Stroke Brain CT:**
Everything above, plus:
- **Dark patches on one side** — simulating ischemic stroke (dead tissue appears darker)
- **Shifted midline** — when one side of the brain swells, it pushes the midline to the other side
- **Optional bright spot** — simulating hemorrhagic transformation (bleeding within the stroke area)

### Dataset Numbers
- **Training set:** 800 images (400 stroke + 400 normal)
- **Test set:** 200 images (100 stroke + 100 normal)
- **Sample images:** 6 (3 stroke + 3 normal) for quick testing

---

## The Web Application

### Pages

1. **Login/Register** — Create an account or log in. Default admin: admin/admin123

2. **Home** — Shows your statistics (total scans, stroke count, normal count), quick action buttons, sample image downloads, and recent scan results

3. **Predict** — The main page! Upload a CT scan image by dragging it into the upload area or clicking to browse. The AI analyzes it instantly and shows the result with a confidence score and color-coded badge.

4. **History** — A table of all your past scans with thumbnails, predictions, confidence scores, and dates

5. **Dashboard** — Beautiful charts showing:
   - Model accuracy comparison (bar chart)
   - F1 score comparison (bar chart)
   - Your prediction distribution (doughnut chart — how many stroke vs normal)
   - Confidence distribution (how confident the AI was across all your scans)

6. **About** — Explains stroke types, shows the CNN architecture diagram, lists all technologies used

### How Data Is Stored

Everything is saved in an SQLite database:
- **Users table:** Your account info (username, hashed password, name, role)
- **Predictions table:** Every scan you've done (image path, prediction, confidence, date)

Your uploaded images are saved in the `static/uploads/` folder with unique filenames to prevent conflicts.

---

## How Training Works

### The Training Loop (15 Epochs)

An "epoch" is one complete pass through all training images. Think of it like studying for an exam:

1. **Show the AI a batch of 32 images** with their correct answers
2. **AI makes predictions** — at first, it's basically guessing
3. **Calculate the error** (Binary Cross-Entropy Loss) — how wrong was it?
4. **Adjust the weights** (Adam Optimizer) — slightly change the internal parameters to be more correct next time
5. **Repeat** for all batches in the training set
6. **Test on validation set** — check accuracy on images the AI hasn't seen during training

Over 15 epochs, the AI goes from ~50% accuracy (random guessing) to 100% accuracy.

### Why Dropout Matters

Without dropout, the AI might "memorize" the training images instead of learning general patterns. With 50% dropout, random neurons are turned off during training, forcing the network to learn redundant representations. It's like studying with a friend who randomly covers parts of your notes — you have to truly understand the material, not just memorize the exact words.

---

## Running the Project

### Quick Start

```
python generate_dataset.py    # Create 1000 CT images (takes ~30 seconds)
python train_model.py         # Train all models (takes ~2 minutes)
python app.py                 # Start the web server on port 5010
```

Then open http://localhost:5010, log in as admin/admin123, and upload a sample image to test!

### Docker

```
docker build -t stroke-detection .
docker run -p 5010:5010 stroke-detection
```

---

## Important Disclaimer

This is an educational project using synthetic data. It is NOT intended for real medical diagnosis. Always consult qualified medical professionals for actual brain stroke detection and treatment. Real stroke detection systems use much larger datasets of actual patient CT scans and undergo rigorous clinical validation.
