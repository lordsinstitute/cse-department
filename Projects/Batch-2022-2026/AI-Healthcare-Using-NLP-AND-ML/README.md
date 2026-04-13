#  — AI Assistance for Healthcare (Medical Chatbot)

## Project Structure

```
AI MEDICAL CHATBOT -VBIT/
├── app.py                          # Main Flask application (chatbot logic)
├── DATA.json                       # Stores user diagnosis history
├── Dockerfile                      # Docker container configuration
├── .dockerignore                   # Docker ignore file
├── requierments.txt                # Original dependency list (conda)
├── model/
│   ├── knn.pkl                     # Pre-trained KNN classifier (~5 MB)
│   └── tfidfsymptoms.csv           # TF-IDF symptom features
├── Medical_dataset/
│   ├── Training.csv                # Training data (4920 rows, 132 symptoms, 41 diseases)
│   ├── Testing.csv                 # Testing data (41 rows)
│   ├── symptom_Description1.csv    # Disease descriptions
│   ├── symptom_severity.csv        # Symptom severity scores
│   ├── symptom_precaution1.csv     # Disease precautions & recommendations
│   ├── intents.json                # Chatbot intent patterns
│   └── ... (additional dataset files)
├── static/
│   └── styles/
│       ├── style.css               # Chat interface styles
│       ├── styles.css              # Landing page styles
│       └── DOCT.png                # Doctor illustration
├── templates/
│   ├── index.html                  # Landing page with "Chat Now" button
│   └── home.html                   # Chat interface (jQuery AJAX)
└── nltk_data/                      # NLTK downloaded data (auto-created)
```

## Prerequisites

- Python 3.8 to 3.13 (Python 3.14 has compatibility issues with spaCy)
- pip (Python package manager)

## Installation Steps (Windows)

**Step 1:** Open Command Prompt and navigate to project

```bash
cd "AI MEDICAL CHATBOT -VBIT"
```

**Step 2:** Install required packages

```bash
pip install flask spacy nltk pandas numpy scikit-learn joblib
```

**Step 3:** Download spaCy English model

```bash
python -m spacy download en_core_web_sm
```

**Step 4:** Download NLTK data

```bash
python -c "import nltk; nltk.download('wordnet'); nltk.download('punkt'); nltk.download('omw-1.4'); nltk.download('punkt_tab')"
```

**Step 5:** Run the application

```bash
python app.py
```

**Step 6:** Open in browser

```
http://127.0.0.1:5000
```

---

## Docker Setup (Windows)

### Prerequisites

- Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
- Make sure Docker Desktop is running

### Build and Run

**Step 1:** Open Command Prompt and navigate to project

```bash
cd "AI MEDICAL CHATBOT -VBIT"
```

**Step 2:** Build the Docker image

```bash
docker build -t medical-chatbot .
```

**Step 3:** Run the container

```bash
docker run -d -p 5000:5000 --name medical-chatbot-app medical-chatbot
```

**Step 4:** Open in browser

```
http://localhost:5000
```

### Docker Management Commands

```bash
# Stop the container
docker stop medical-chatbot-app

# Start the container again
docker start medical-chatbot-app

# Remove the container
docker rm -f medical-chatbot-app

# View logs
docker logs medical-chatbot-app

# Rebuild after code changes
docker rm -f medical-chatbot-app
docker build -t medical-chatbot .
docker run -d -p 5000:5000 --name medical-chatbot-app medical-chatbot
```

---

## How It Works

1. User visits the landing page and clicks **Chat Now**
2. The chatbot greets the user and asks for basic info (name, age, gender)
3. User describes their **first symptom** in natural language
4. The system uses **NLP** (spaCy lemmatization + stop word removal) to process the input
5. **Syntactic matching** (Jaccard similarity + permutations) finds matching symptoms in the database
6. If no syntactic match, **semantic matching** (WordNet WUP similarity) is used
7. User provides a **second symptom** — same matching process
8. The chatbot asks follow-up questions about related symptoms for possible diseases
9. A **KNN classifier** predicts the disease based on symptom one-hot vectors
10. The chatbot provides: disease name, description, severity assessment, and precautions

---

## Pages Overview

| Page | URL | Description |
|---|---|---|
| Landing Page | `/` | Welcome page with doctor image and "Chat Now" button |
| Chat Interface | `/home.html` | Interactive chat with the medical chatbot |
| Bot Response | `/get` | AJAX endpoint that returns bot responses |

---

## Test Cases

### Test Case 1: Landing Page

1. Open `http://127.0.0.1:5000`
2. See the landing page with doctor image and description

**Expected Result:** Landing page loads with "MEDICAL CHATBOT" heading, description text, and "Chat Now" button.

---

### Test Case 2: Start Chat

1. Click "Chat Now" on landing page
2. Chat interface opens with bot greeting
3. Type "OK" and send

**Expected Result:** Bot responds with "What is your name?"

---

### Test Case 3: Provide Basic Information

1. Type your name (e.g., "Ahmed") → Bot asks for age
2. Type age (e.g., "25") → Bot asks for gender
3. Type gender (e.g., "Male") → Bot greets and asks to tap S

**Expected Result:** Bot collects name, age, gender and asks to start diagnostic.

---

### Test Case 4: First Symptom — Direct Match

1. After tapping "S", bot asks for main symptom
2. Type "headache"

**Expected Result:** Bot recognizes "headache" via syntactic matching and asks for a second symptom or shows related symptoms to choose from.

---

### Test Case 5: First Symptom — Multiple Matches

1. Type a broad symptom like "pain"

**Expected Result:** Bot shows numbered list of related symptoms (e.g., "0) chest pain", "1) back pain", etc.) and asks user to select one.

---

### Test Case 6: Second Symptom

1. After first symptom is confirmed, bot asks for another symptom
2. Type a second symptom (e.g., "fever")

**Expected Result:** Bot processes second symptom and begins disease analysis.

---

### Test Case 7: Follow-Up Questions

1. After both symptoms are entered, bot asks about related symptoms
2. Answer "yes" or "no" to each question

**Expected Result:** Bot narrows down possible diseases by asking about symptoms associated with candidate diseases.

---

### Test Case 8: Disease Prediction

1. After enough symptoms are collected, bot predicts the disease

**Expected Result:** Bot says "you may have [Disease Name]" and asks to tap D for description.

---

### Test Case 9: Disease Description

1. Type "D" or any text after prediction

**Expected Result:** Bot shows disease description from the medical dataset and mentions precautions.

---

### Test Case 10: Severity Assessment

1. Bot asks about duration (number of days)
2. Enter number of days (e.g., "5")

**Expected Result:** If severity is high, bot recommends consulting a doctor. If low, bot lists precautions.

---

### Test Case 11: Continue or Exit

1. After diagnosis, bot asks "Do you need another medical consultation (yes or no)?"
2. Type "yes" → Bot starts a new symptom collection
3. Type "no" → Bot says goodbye

**Expected Result:** "yes" restarts diagnosis with same user info. "no" ends the conversation.

---

### Test Case 12: Unrecognized Symptom

1. Type a symptom that doesn't match anything (e.g., "xyzabc")

**Expected Result:** Bot tries semantic similarity. If no match found, asks user to specify more details or offers to continue/quit.

---

### Test Case 13: Semantic Similarity Fallback

1. Type a synonym of a symptom (e.g., "throwing up" instead of "vomiting")

**Expected Result:** Bot uses WordNet semantic similarity to find "vomiting" and asks for confirmation.

---

### Test Case 14: Diagnosis History (DATA.json)

1. Complete a full diagnosis conversation
2. Open `DATA.json` in the project folder

**Expected Result:** JSON file contains the diagnosis record with name, age, gender, predicted disease, and symptoms list.

---

### Test Case 15: Restart Conversation

1. After completing a diagnosis, type "yes" when asked for another consultation
2. Bot should ask for main symptom again (skips name/age/gender since already collected)

**Expected Result:** New diagnosis begins with same user info. Bot asks for main symptom directly.

---

### Test Case 16: Page Refresh Reset

1. During an active conversation, refresh the browser page
2. The chat interface reloads with initial bot greeting

**Expected Result:** Session is cleared. User must start over from "OK" → name → age → gender.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| **Python** | Backend programming language |
| **Flask** | Web framework for routing and sessions |
| **spaCy** | NLP — tokenization, lemmatization, stop word removal |
| **NLTK** | WordNet for semantic similarity (WUP similarity) |
| **scikit-learn** | KNN classifier for disease prediction |
| **pandas / numpy** | Data processing and one-hot vector creation |
| **joblib** | Loading pre-trained KNN model |
| **jQuery** | AJAX requests for chat interaction |
| **HTML/CSS** | User interface |
| **Docker** | Containerized deployment |

---

## Team

| Roll Number | Name |
|-------------|------|
| 160922733160 | Syed Yousuf Pasha Quadri |
| 160922733128 | Mohd Amaanuddin |
| 160922733126 | Mohd Abdul Sameer |
| 160922733146 | Syed Abdul Jauvad |

## Notes

- The chatbot uses a **session-based** conversation flow — each user gets their own chat state
- The **KNN model** (`model/knn.pkl`) is pre-trained on 4920 medical records with 132 symptoms and 41 diseases
- Symptom matching uses a two-stage approach: **syntactic** (Jaccard similarity) first, then **semantic** (WordNet) as fallback
- User diagnosis history is saved to `DATA.json` (auto-created on startup)
- The app runs on default Flask port **5000**
- To reset chat state, refresh the page or restart the server
- Python 3.14 is **not supported** due to spaCy compatibility issues — use Python 3.8 to 3.13
- The KNN model was trained with scikit-learn 0.24.2 — a version warning may appear but the model loads and works correctly
- `DATA.json` is reset each time the server restarts (by design)

