# PROJECT EXPLANATION — AI Assistance for Healthcare (Medical Chatbot)

This document explains the entire project in simple terms so that even a 7th-grader can understand how it works.

---

## What Does This Project Do?

Imagine you're feeling sick — maybe you have a headache and a fever. Normally, you would go to a doctor, describe your symptoms, and the doctor would figure out what's wrong with you. But what if you could talk to a **smart computer program** that does something similar?

That's exactly what this project is! It's a **Medical Chatbot** — a computer program that you can chat with, just like texting a friend. You tell it your symptoms, and it uses **Artificial Intelligence (AI)** to figure out what disease you might have and what you should do about it.

**Important:** This chatbot is NOT a replacement for a real doctor. It's a tool to help you understand your symptoms and get basic guidance.

---

## How Does the Chat Work? (Step by Step)

Here's what happens when you use the chatbot:

### Step 1: Say Hello
When you open the chat, the bot greets you and asks you to type "OK" to start.

### Step 2: Basic Information
The bot asks you three simple questions:
1. **What is your name?** (e.g., "Ahmed")
2. **How old are you?** (e.g., "25")
3. **What is your gender?** (e.g., "Male")

### Step 3: First Symptom
The bot asks: **"What is your main symptom?"**

You type something like "headache" or "stomach pain". The bot then tries to understand what you mean (more on this below!).

### Step 4: Second Symptom
The bot asks for another symptom. You might type "fever" or "nausea".

### Step 5: Follow-Up Questions
The bot thinks about which diseases could cause your symptoms, and asks you more questions like:
- "Are you experiencing chest pain?"
- "Are you experiencing fatigue?"

You answer "yes" or "no" to each one.

### Step 6: Diagnosis
Based on all your answers, the bot tells you:
- **What disease you might have** (e.g., "You may have Common Cold")
- **A description** of the disease
- **How serious it is** (should you see a doctor or just take precautions?)
- **Precautions** you can take (e.g., "Drink warm water", "Take rest")

### Step 7: Continue or Exit
The bot asks if you want another consultation. You can say "yes" to start over or "no" to end the chat.

---

## How Does the Bot Understand Your Symptoms?

This is the most interesting part! When you type a symptom like "my head hurts", the bot needs to figure out that you mean "headache". It does this in **three clever ways**:

### Method 1: Exact Matching (Syntactic Similarity)

The bot has a list of **132 known symptoms** (like headache, fever, cough, nausea, etc.). When you type something, it:

1. **Cleans up your text** — removes small words like "my", "the", "is" (these are called "stop words")
2. **Finds the root word** — turns "running" into "run", "headaches" into "headache" (this is called "lemmatization")
3. **Compares your words** with the known symptom list using something called **Jaccard Similarity**

#### What is Jaccard Similarity?

Imagine you have two sets of words:
- Your input: {stomach, pain}
- Known symptom: {stomach, pain}

Jaccard Similarity = (words in common) / (total unique words) = 2/2 = **1.0** (perfect match!)

Another example:
- Your input: {bad, stomach, pain}
- Known symptom: {stomach, pain}

Jaccard Similarity = 2/3 = **0.67** (still a good match!)

The bot picks the symptom with the highest similarity score.

### Method 2: Smart Matching (Semantic Similarity)

What if you type "throwing up" but the database has "vomiting"? The words are completely different, but they mean the same thing!

This is where **WordNet** comes in. WordNet is like a giant dictionary that knows which words have similar meanings. The bot uses something called **WUP Similarity** (Wu-Palmer Similarity) to measure how close two words are in meaning.

**How WUP Similarity works (simplified):**
- WordNet organizes words in a tree-like structure
- "Vomiting" and "throwing up" are close together in the tree → high similarity score
- "Vomiting" and "happiness" are far apart → low similarity score

If the score is above 0.25 (on a scale of 0 to 1), the bot considers it a match.

### Method 3: Synonym Suggestions

If neither method works, the bot tries one more thing — it looks up **synonyms** (words with similar meanings) of what you typed, and checks if any of those synonyms match a known symptom. It then asks you: "Are you experiencing [synonym]?" and you can say yes or no.

---

## How Does the Bot Predict the Disease?

Once the bot has identified your symptoms, it uses a **Machine Learning model** called **KNN (K-Nearest Neighbors)** to predict which disease you might have.

### What is KNN? (Simple Explanation)

Imagine you're in a classroom and you want to guess if a new student likes sports. You look at the **5 students sitting closest** to them (their "nearest neighbors"). If 4 out of 5 of those students like sports, you'd guess the new student probably likes sports too!

KNN works the same way but with diseases:

1. The bot has a database of **4,920 medical records** — each record says "a patient had these symptoms and was diagnosed with this disease"
2. Your symptoms are converted into a row of **132 numbers** (1 if you have the symptom, 0 if you don't) — this is called a **One-Hot Vector**
3. The KNN model finds the records in the database that are **most similar** to your symptom pattern
4. It looks at what diseases those similar records had
5. The most common disease among them becomes the **prediction**

### Example:

Let's say you have: headache = 1, fever = 1, cough = 0, nausea = 0, ... (132 values)

The KNN model finds the 5 most similar patients in the database:
- Patient A (headache, fever) → Common Cold
- Patient B (headache, fever, runny nose) → Common Cold
- Patient C (headache, fever, body ache) → Flu
- Patient D (headache, fever) → Common Cold
- Patient E (headache, high fever) → Common Cold

Result: 4 out of 5 had Common Cold → **Prediction: Common Cold**

---

## What is NLP? (Natural Language Processing)

NLP is a branch of AI that helps computers understand human language. In this project, NLP is used to:

1. **Tokenization** — Breaking a sentence into individual words
   - "I have a bad headache" → ["I", "have", "a", "bad", "headache"]

2. **Stop Word Removal** — Removing common words that don't carry meaning
   - ["I", "have", "a", "bad", "headache"] → ["bad", "headache"]

3. **Lemmatization** — Converting words to their base form
   - "headaches" → "headache"
   - "running" → "run"
   - "worse" → "bad"

The project uses a library called **spaCy** for NLP processing, specifically the `en_core_web_sm` model (a small English language model).

---

## What Data Does the Bot Use?

The chatbot relies on several data files:

### Training.csv (The Main Dataset)
- **4,920 rows** of patient data
- **132 columns** — each column is a symptom (like itching, skin rash, nodal skin eruptions, etc.)
- **1 target column** — the disease (called "prognosis")
- Each row has 1s and 0s: 1 means the patient had that symptom, 0 means they didn't
- Covers **41 different diseases**

### symptom_Description1.csv
Contains a description for each disease. For example:
- Common Cold → "Common cold is a viral infection of your nose and throat..."

### symptom_severity.csv
Contains a severity score for each symptom. For example:
- Headache → severity 3
- High fever → severity 7

The bot adds up the severity scores of all your symptoms and multiplies by the number of days you've been sick. If the total is high, it recommends seeing a doctor.

### symptom_precaution1.csv
Contains precautions for each disease. For example:
- Common Cold → ["drink warm water", "take rest", "take vitamin C", "avoid cold food", ...]

### knn.pkl (Pre-Trained Model)
This is the KNN classifier that was already trained on the Training.csv data. Instead of training every time the app starts, the model is saved as a file and loaded instantly.

---

## What Technologies Are Used?

| Technology | What It Does |
|---|---|
| **Python** | The programming language used to write the entire backend |
| **Flask** | A web framework that creates the website and handles chat messages |
| **spaCy** | NLP library for text processing (lemmatization, stop words) |
| **NLTK (WordNet)** | Dictionary of word meanings used for semantic similarity |
| **scikit-learn** | Machine learning library that provides the KNN classifier |
| **pandas** | Library for reading and processing CSV data files |
| **numpy** | Library for mathematical operations (creating one-hot vectors) |
| **joblib** | Library for loading the pre-trained KNN model from file |
| **jQuery** | JavaScript library for sending chat messages without reloading the page |
| **HTML/CSS** | Standard web technologies for the user interface |
| **Docker** | A tool to package the entire app into a container for easy deployment |

---

## How is Data Stored?

### Session Storage (Temporary)
While you're chatting, the bot remembers your conversation using **Flask sessions**. This stores:
- Your name, age, gender
- Which step of the conversation you're on
- Your symptoms so far
- Possible diseases being considered

This data disappears when you close your browser or the server restarts.

### DATA.json (Permanent)
After each completed diagnosis, the bot saves a record to `DATA.json`:
```json
{
    "Name": "Ahmed",
    "Age": 25,
    "Gender": "Male",
    "Disease": "Common Cold",
    "Sympts": ["headache", "fever"]
}
```

This creates a history of all diagnoses made by the chatbot.

---

## The Two Pages

### 1. Landing Page (`index.html`)
This is the first page you see. It has:
- A picture of a doctor
- The title "MEDICAL CHATBOT"
- A description of what the chatbot does
- A **"Chat Now"** button that takes you to the chat

### 2. Chat Page (`home.html`)
This is where the actual conversation happens. It looks like a messaging app:
- **Bot messages** appear on the left (with a robot icon)
- **Your messages** appear on the right
- There's a text box at the bottom where you type
- Messages are sent using **AJAX** — this means the page doesn't reload when you send a message

#### How AJAX Works (Simple Explanation)
Normally, when you click a button on a website, the entire page reloads. With AJAX, your browser sends a message to the server **in the background** and gets a response back — all without the page flickering or reloading. This is what makes the chat feel smooth and real-time.

---

## The Conversation Flow (Detailed)

```
User opens chat
    ↓
Bot: "Hello! Tap OK to continue"
    ↓
User: "OK"
    ↓
Bot: "What is your name?"
    ↓
User: "Ahmed"
    ↓
Bot: "How old are you?"
    ↓
User: "25"
    ↓
Bot: "Can you specify your gender?"
    ↓
User: "Male"
    ↓
Bot: "Hello Mr/Ms Ahmed! Tap S to start diagnostic!"
    ↓
User: "S"
    ↓
Bot: "What is your main symptom?"
    ↓
User: "headache"
    ↓
[Syntactic matching → finds "headache" in database]
    ↓
Bot: "You are probably facing another symptom, can you specify it?"
    ↓
User: "fever"
    ↓
[Syntactic matching → finds "high_fever" or related]
    ↓
Bot: "Are you experiencing [related symptom]?" (follow-up questions)
    ↓
User: "yes" / "no" (multiple rounds)
    ↓
[KNN prediction runs]
    ↓
Bot: "You may have Common Cold. Tap D for description."
    ↓
User: "D"
    ↓
Bot: [Disease description + precaution info]
    ↓
Bot: "Do you need another consultation? (yes/no)"
    ↓
User: "no"
    ↓
Bot: "THANKS Mr/Ms Ahmed"
```

---

## What Makes This Project Special?

1. **Natural Language Understanding** — You can type symptoms in everyday language, not medical terms
2. **Two-Stage Matching** — First tries exact word matching, then falls back to meaning-based matching
3. **Synonym Suggestions** — If neither matching works, the bot suggests similar symptoms
4. **Machine Learning Prediction** — Uses a trained KNN model on 4,920 real medical records
5. **Severity Assessment** — Tells you whether your condition needs a doctor visit
6. **Precaution Guidance** — Provides specific precautions for your predicted disease
7. **Conversation Memory** — Remembers your info throughout the chat session
8. **Diagnosis History** — Saves all diagnoses to a file for future reference

---

## Frequently Asked Questions

**Q: Can this chatbot replace a real doctor?**
A: No. This is an educational project that demonstrates how AI can assist in healthcare. Always consult a real doctor for medical decisions.

**Q: How many diseases can it detect?**
A: The model is trained on **41 different diseases** including common cold, flu, diabetes, hypertension, migraine, and more.

**Q: How many symptoms does it know?**
A: The system knows **132 different symptoms** ranging from headache and fever to more specific ones like yellowing of eyes or fluid overload.

**Q: What if the bot can't identify my symptom?**
A: The bot tries three approaches: exact matching, meaning-based matching, and synonym suggestions. If none work, it asks you to describe your symptom differently or offers to end the conversation.

**Q: Is my data stored permanently?**
A: Your conversation is temporary (stored in browser session). Only the final diagnosis result (name, age, gender, disease, symptoms) is saved to `DATA.json`.

**Q: What happens if I refresh the page during a chat?**
A: The conversation resets and you'll need to start over, because the session data is cleared.
