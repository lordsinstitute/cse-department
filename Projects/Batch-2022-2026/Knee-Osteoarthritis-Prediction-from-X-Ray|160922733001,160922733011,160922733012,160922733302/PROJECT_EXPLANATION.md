# Project Explanation — Knee Osteoarthritis Classification Using Deep Learning

## What Does This Project Do?

Imagine you go to the doctor because your knee hurts. The doctor takes an X-ray picture of your knee and needs to figure out how bad the damage is. Is your knee perfectly healthy, or is there some wear and tear? If there is damage, is it just beginning, or is it really serious?

This project is like a smart computer assistant that looks at knee X-ray pictures and tells the doctor exactly how damaged the knee is, using a rating scale from 0 (perfectly normal) to 4 (very serious). It uses **ensemble learning** — combining three different AI models so they vote together, producing a more reliable answer than any single model alone.

But it doesn't just give a grade — it also:
- **Explains why** it made that decision (Grad-CAM heatmap + clinical findings)
- **Downloads a PDF report** with the X-ray, heatmap, prediction, and clinical notes
- **Tracks patient history** — so a doctor can compare a patient's X-rays from different visits and see whether their condition is improving, worsening, or staying the same

---

## What Is Knee Osteoarthritis?

**Osteoarthritis (OA)** is the most common type of arthritis — a disease that affects your joints (the places where two bones meet, like your knee). Think of your knee joint like a door hinge:

- In a healthy knee, the bones have a smooth, slippery coating called **cartilage** that lets them glide past each other easily (like butter on a pan)
- With osteoarthritis, this cartilage slowly wears away, like how the rubber on your shoes wears down over time
- Without cartilage, the bones rub directly against each other, causing pain, swelling, and stiffness
- Over time, the bones can change shape and develop sharp bumps called **osteophytes** (bone spurs)

**Who gets it?** Over 300 million people worldwide. It's more common in people over 50, but can happen earlier due to injuries or genetics.

---

## The Kellgren-Lawrence (KL) Grading Scale

Doctors use a standard rating system called the **KL scale** to measure how bad osteoarthritis is. Think of it like grades on a school report card:

### Grade 0 — Normal
- Your knee is perfectly healthy
- Wide space between the bones (lots of cartilage)
- Smooth, round bone edges
- No bone spurs

### Grade 1 — Doubtful
- Possibly very slightly narrower space between bones
- Maybe a tiny bump at the edge of the bone
- This is the hardest grade to detect — even doctors sometimes disagree
- *This is also the hardest grade for AI to classify due to subtle differences from Normal*

### Grade 2 — Mild
- The space between bones is noticeably narrower (cartilage is thinning)
- Small bone spurs visible at the joint edges
- The bone near the joint looks slightly brighter (called **sclerosis**)

### Grade 3 — Moderate
- The space between bones is much narrower
- Multiple bone spurs, some quite large
- Small dark holes might appear in the bone (**cysts** — filled with fluid)

### Grade 4 — Severe
- Almost no space left between bones (nearly bone-on-bone)
- Very large bone spurs
- The bone shape has changed (deformity)
- Surgery (knee replacement) might be needed

---

## How Does the AI Classify Knee X-Rays?

### The Approach: Ensemble Learning

Instead of relying on a single AI model (which can be wrong), this project combines **three different models** that each look at the X-ray in a different way. They each produce a set of probabilities (how confident they are about each grade), and those probabilities are combined using a weighted average — MobileNetV2 contributes 55%, Custom CNN 30%, and Random Forest 15%.

This is like asking three doctors to look at the same X-ray and vote. If two of them say "Moderate" and one says "Mild", the combined opinion is more trustworthy than any single diagnosis.

### Model 1: MobileNetV2 (Transfer Learning) — Weight 55%

Instead of building an AI brain from scratch, MobileNetV2 was already trained to recognize patterns in 1.4 million everyday photos (cats, cars, flowers, etc.). This pre-learned knowledge is then fine-tuned for knee X-rays:

1. **Start with a pre-trained brain:** MobileNetV2 already knows how to find edges, textures, shapes, and patterns in images
2. **Freeze the knowledge:** The AI keeps all this general image understanding
3. **Add a new decision layer:** A small new section learns specifically about knee X-rays — "these patterns mean Grade 2", "these patterns mean Grade 4"

It's like hiring an experienced art critic (who already understands colors, shapes, and composition) and just teaching them the differences between five types of knee X-rays.

**Architecture:** 19 convolutional blocks → 1,280 feature values → Dropout(0.5) → 5-class output

### Model 2: Custom CNN — Weight 30%

A simpler neural network built from scratch with 4 convolutional blocks:
- Each block: Conv2D → BatchNorm → ReLU → MaxPool
- Works on **grayscale** images (128×128 pixels)
- Final layers: Flatten → Dense(256) → Dropout(0.5) → 5-class output

Because it's trained from scratch without ImageNet pre-training, it learns knee-specific features directly from the X-ray data.

### Model 3: Random Forest — Weight 15%

Not a deep learning model at all. It creates 100 "decision trees" that each look at different pixel patterns and vote on the grade. It works on flattened grayscale pixel values (128×128 = 16,384 numbers per image) and provides a different perspective from the neural networks. Simple but important as a diverse ensemble member.

### Doubtful Class Calibration

The Doubtful grade (Grade 1) is historically very difficult to classify — the raw model achieves only 7.87% accuracy on it. This happens because:
- Doubtful images look very similar to Normal images
- The dataset has far fewer Doubtful images than Normal images, so the model becomes biased toward predicting Normal

Two fixes are applied:
1. **Calibration weights at prediction time:** After the ensemble combines probabilities, Doubtful's probability is multiplied by 2.8 and renormalized. This raises the effective detection rate to ~31%.
2. **Class-weighted training loss:** When retraining, Doubtful samples are given 3× the penalty weight in the loss function, forcing the model to pay more attention to Doubtful cases.

### Step-by-Step Prediction Process

**Step 1: Upload the X-Ray**
The doctor uploads a knee X-ray image through the web application (drag-and-drop or click). Optionally, the scan can be assigned to a patient for progression tracking.

**Step 2: Prepare the Image**
- For MobileNetV2: resize to 224×224 RGB, normalize with ImageNet mean/std
- For CNN + Random Forest: resize to 128×128 grayscale, convert to tensor

**Step 3: Run All Three Models**
Each model independently processes the image and produces 5 probabilities (one per grade).

**Step 4: Weighted Ensemble**
Combine probabilities: `final = (0.55 × mobilenet + 0.30 × cnn + 0.15 × rf)`

**Step 5: Calibration**
Multiply by calibration weights `[0.85, 2.8, 1.2, 1.3, 0.9]` and renormalize. The highest calibrated probability wins.

**Step 6: Grad-CAM Explainability**
A colored heatmap is generated from MobileNetV2's last convolutional layer, showing which areas of the X-ray influenced the prediction most.

**Step 7: Clinical Findings**
Based on the predicted grade, a list of clinical findings is displayed (e.g., "Definite osteophytes visible at joint margins", "Mild narrowing of the joint space").

**Step 8: Results Available**
- Prediction result with ensemble model label and confidence
- Side-by-side original X-ray and Grad-CAM heatmap
- All 5 class confidence bars
- Clinical findings card
- PDF download button
- Patient timeline link (if scan is linked to a patient)

---

## Grad-CAM Explainability — How It Works

Grad-CAM stands for **Gradient-weighted Class Activation Mapping**. It makes the AI's decision-making process visible — like a "spotlight" showing where the AI was looking.

### How It Works

1. **Forward Pass:** The X-ray passes through MobileNetV2, producing the classification prediction
2. **Backward Pass:** Gradients flow backward to identify which parts of the image mattered most
3. **Activation Maps:** The last convolutional layer contains feature maps — filtered versions of the image highlighting edges, textures, and bone structures
4. **Weighted Combination:** Gradients weight each feature map by importance, summed into a single heatmap
5. **Overlay:** The heatmap is colored (blue → green → yellow → red) and overlaid on the X-ray

### Color Meaning

- **Red/Yellow regions:** Strongest influence — typically the joint space between femur and tibia, bone edges where osteophytes form, areas of sclerosis
- **Blue/Green regions:** Less influence
- **Dark regions:** Largely ignored (background soft tissue, bony shaft away from joint)

### Why Explainability Matters in Medical AI

In medical applications, it's not enough to output a number. Doctors need to:
- **Verify** the AI's reasoning matches what they see in the X-ray
- **Trust** the prediction by seeing it focused on medically relevant areas
- **Catch errors** if the AI is looking at the wrong part of the image

---

## Patient Progression Tracking

This is one of the key new features. It allows tracking of a patient's knee condition over multiple visits.

### How It Works

1. **Create a patient record** (name, age, gender, clinical notes)
2. **Assign scans to a patient** — when uploading an X-ray, optionally select a patient from the dropdown
3. **View the patient's timeline** — all scans are shown chronologically with:
   - The predicted KL grade badge for each scan
   - **Trend indicator** between scans:
     - ↓ **Improved** — grade went down (e.g., Severe → Moderate)
     - ↑ **Worsened** — grade went up (e.g., Mild → Moderate)
     - — **Stable** — same grade as previous scan
   - **Overall progression summary** — compares the very first scan to the most recent one
   - X-ray and Grad-CAM thumbnails for each scan entry
   - PDF download button per scan

### Example

A patient named Ahmed comes in three times:
- **Visit 1 (Jan):** Severe → *Initial scan*
- **Visit 2 (Mar):** Moderate → *↓ Improved from Severe to Moderate*
- **Visit 3 (Jun):** Moderate → *— Stable*

Overall summary: "Improved — condition improved from Severe to Moderate"

---

## PDF Report Generation

Every prediction can be downloaded as a PDF report using the "Download PDF" button (on the predict page or in the history table). The PDF includes:

1. **Header** — App name and subtitle
2. **Report Details** — ID, date, doctor/user name, models used, patient info (if linked)
3. **Diagnosis Banner** — Grade + confidence, colored by severity
4. **Clinical Description** — Short summary of what the grade means
5. **X-Ray Images** — Original X-ray and Grad-CAM heatmap side by side
6. **Confidence Score Bars** — Visual bar for all 5 grades
7. **Clinical Findings** — Bullet list of medical observations for this grade
8. **Disclaimer** — "For educational use only, not for clinical diagnosis"

---

## The Web Application

### Pages

1. **Login/Register** — Create an account or log in (default: admin/admin123)

2. **Home** — Shows:
   - Active ensemble models banner (which models are loaded)
   - Statistics: total scans, total patients, count per grade
   - Recent scan results
   - Sample image downloads

3. **Predict** — Main page:
   - Upload X-ray (drag-and-drop or click)
   - Optional patient assignment dropdown
   - Ensemble prediction result with grade, confidence, and models used
   - Original X-ray + Grad-CAM heatmap side by side
   - All 5 class probability bars
   - Clinical findings explanation
   - PDF download button
   - "View Patient Timeline" link (if patient assigned)

4. **History** — Table of all past scans with thumbnails, grade badge, confidence, patient name (linked), date, and PDF download button

5. **Patients** — Cards showing each patient with their scan count, latest grade, and last scan date; links to progression timeline

6. **Dashboard** — Charts comparing model accuracy, F1 scores, per-class accuracy, and personal prediction distribution

7. **About** — KL grading scale explanation and project tech stack

---

## Running the Project

### Quick Start

```bash
python download_dataset.py   # Download 9,786 real knee X-ray images from Kaggle
python train_model.py        # Train all 3 models (saves knee_cnn_model.pth + ml_model.pkl)
python app.py                # Start web server on port 5011
```

Then open http://localhost:5011, log in as admin/admin123, and upload a sample image.

> **Note:** The app works without running `train_model.py` if `knee_mobilenet_model.pth` and `ml_model.pkl` already exist (2-model ensemble). Running `train_model.py` also generates `knee_cnn_model.pth` to activate the full 3-model ensemble.

### Docker

```bash
docker build -t knee-oa .
docker run -p 5011:5011 knee-oa
```

---

## Important Disclaimer

This is an educational project. While it is trained on real X-ray data, it is **NOT** intended for real medical diagnosis. Always consult qualified medical professionals for actual knee osteoarthritis assessment. Real clinical systems undergo rigorous validation, regulatory approval, and clinical trials before deployment.
