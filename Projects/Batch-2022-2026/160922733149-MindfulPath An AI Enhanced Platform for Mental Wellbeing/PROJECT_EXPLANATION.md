# MindfulPath — Project Explanation

This document explains the MindfulPath project in simple language that anyone can understand.

## What is MindfulPath?

MindfulPath is a website that helps people take care of their mental health. Think of it like a health app, but instead of tracking your steps or calories, it tracks your feelings and moods. It also has an AI chatbot that you can talk to when you're feeling stressed, anxious, or sad.

## Why Was This Project Built?

Mental health is just as important as physical health, but many people don't have easy access to support. Some people:
- Can't afford therapy
- Feel too shy to talk to someone face-to-face
- Don't know where to start

MindfulPath provides a safe, private space where anyone can:
- Talk to an AI companion about how they feel
- Track their moods over time to spot patterns
- Learn meditation and relaxation techniques
- Find and connect with real therapists when ready

## What Happens When You Use MindfulPath?

### 1. You Create an Account

You sign up with your name, email, and password. You can register as a regular user (someone looking for support) or as a therapist (a mental health professional).

### 2. You Talk to the AI Chatbot

This is the main feature. Here's how it works step by step:

**Step 1: You type a message**
For example: "I've been feeling really anxious lately and can't sleep"

**Step 2: The computer analyzes your words using a Transformer AI Model**

The system uses a pre-trained AI model called **DistilBERT** — a lightweight version of BERT (Bidirectional Encoder Representations from Transformers), developed by Google and HuggingFace. Unlike older dictionary-based methods, DistilBERT reads your entire sentence and understands context, including:

- **Negation** — "I am not sad" is correctly identified as positive (old systems would see "sad" and call it negative)
- **Intensity** — "I feel a little bad" is treated differently from "I feel absolutely terrible"
- **Context** — The model understands the full meaning of the sentence, not just individual words

The model runs entirely on your own computer — it does not send your messages to any external server or cloud service. No internet connection or API key is needed after the first setup.

**Step 3: The model gives confidence scores**

The model returns two scores:
- How confident it is that the message is POSITIVE (e.g., 0.95 = 95% positive)
- How confident it is that the message is NEGATIVE (e.g., 0.92 = 92% negative)

These are mapped to severity levels:

| Model Says | Severity |
|---|---|
| 85%+ negative | Very negative |
| 65–85% negative | Moderately negative |
| 50–65% negative | Mildly negative |
| 60%+ positive | Positive |
| Otherwise | Neutral |

**Step 4: The bot picks the right technique**
Based on the severity, the bot uses a specific technique from Cognitive Behavioral Therapy (CBT). CBT is a real type of therapy used by professionals. Here's what happens:

| How You're Feeling | What the Bot Does | Why It Helps |
|---|---|---|
| Very upset or distressed | Validates your feelings and does a grounding exercise | Makes you feel heard and brings you back to the present moment |
| Somewhat negative | Helps you examine your negative thoughts | Teaches you that thoughts aren't always facts |
| Mildly down | Suggests small positive activities | Even small actions can shift your mood |
| Neutral / okay | Checks in on you, shares helpful information | Keeps the conversation going, educates about mental health |
| Feeling good | Celebrates with you, suggests gratitude exercises | Builds on positive feelings to make them stronger |

**Step 5: Crisis detection**
Before analyzing sentiment, the system checks if your message contains words that suggest someone might be in serious danger (like "suicide" or "end it all"). If detected, it immediately shows crisis helpline phone numbers. These are real helplines staffed by trained counselors available 24/7:
- Vandrevala Foundation: 1860-2662-345 (24/7)
- iCall: 9152987821
- AASRA: 9820466726

### 3. You Track Your Mood

Every day, you can log how you're feeling using a simple 5-point scale:
- 😢 Very Sad (1)
- 😞 Sad (2)
- 😐 Neutral (3)
- 😊 Happy (4)
- 😄 Very Happy (5)

You can also write a journal entry about your day. The system analyzes the text of your journal using the same sentiment analysis as the chatbot.

Over time, MindfulPath shows your mood as a line chart so you can see patterns. For example, you might notice you feel worse on Mondays or better after exercise.

### 4. You Try Guided Meditations

The app has a library of 10 guided meditation scripts organized by category:
- **Stress** — Breathing exercises and progressive muscle relaxation
- **Anxiety** — Grounding techniques and visualization
- **Depression** — Body scan meditation and self-compassion exercises
- **Sleep** — Relaxing bedtime meditation
- **Focus** — Concentration-building meditation
- **Mindfulness** — Gratitude and mindful walking exercises

Each meditation has step-by-step instructions written as text that you read and follow along with.

### 5. You Can Find a Therapist

MindfulPath has a directory of therapists. Each therapist profile shows:
- Their name and qualifications
- What they specialize in (anxiety, depression, stress, etc.)
- How many years of experience they have
- What languages they speak
- How much they charge per session
- Their therapeutic approach (how they help people)

You can book a session with any therapist, choosing:
- The date and time
- How long (30, 45, 60, or 90 minutes)
- The type (video call, audio call, or text chat)

### 6. Admin Can Configure the AI Engine

The administrator has a dedicated settings page (`/admin/settings`) to control how the chatbot generates responses — without touching any code.

**Two modes are available:**

- **Local Model Mode** — The chatbot uses pre-written CBT response templates selected by the DistilBERT sentiment score. No API key needed, no cost, works entirely offline. This is the default.
- **LLM API Mode** — The chatbot sends the conversation to a real AI language model (like ChatGPT or Gemini) and gets a dynamic, personalised response back.

**When LLM API Mode is selected, the admin chooses a provider:**

| Provider | What it is |
|---|---|
| **Anthropic Claude** | Claude AI models (Haiku is fast and cheap, Sonnet is smarter) |
| **OpenAI** | ChatGPT models (GPT-4o-mini is fast and cheap, GPT-4o is best quality) |
| **Google Gemini** | Google's AI models (Gemini 2.0 Flash is fast and cheap) |

The admin enters the API key for their chosen provider and clicks **Test Connection** to verify it works before saving. The key is stored securely in the local database on the server.

**Important safety rules that always apply regardless of mode:**
- Sentiment analysis always runs locally on the server
- Crisis keyword detection always runs locally — the LLM is never called if the message contains crisis words
- If the LLM API call fails, the chatbot quietly falls back to local responses

### 7. Admin Can Monitor All Conversations

The Administrator can view all users' AI chatbot conversations through a dedicated interface. This helps monitor user wellbeing across the platform.

The admin sees a 3-level view:
1. **All users** — how many sessions each has, total messages, and when they last chatted
2. **User's sessions** — list of all chat sessions for that user with overall sentiment (positive/negative/neutral)
3. **Session messages** — full conversation log with sentiment label on each message and which CBT technique the bot used

This feature is only accessible to administrators. Regular users and therapists cannot see other people's conversations.

## How Does the Technology Work?

### The Server (Backend)

The backend is built with **Node.js** and **Express.js**. Think of it like the brain of the website — it receives your requests, processes them, and sends back the right information.

When you click a link or submit a form, your browser sends a request to the server. The server:
1. Checks if you're logged in (using a JWT token — like a digital key)
2. Gets the data you need from the database
3. Puts it together into a web page
4. Sends it back to your browser

### The Database (SQLite)

All the information is stored in a SQLite database — a single file on the computer called `mindfulpath.db`. It has 7 tables:

| Table | What It Stores |
|-------|---------------|
| users | Everyone's accounts (name, email, password, role) |
| therapists | Professional details for therapist accounts |
| sessions | Therapy session bookings |
| meditations | The meditation library |
| mood_entries | Your daily mood logs and journal entries |
| chat_sessions | Your conversations with the AI chatbot |
| chat_messages | Each individual message in those conversations |

### The NLP Engine (Transformer-Based Sentiment Analysis)

NLP stands for **Natural Language Processing** — it's a branch of AI that helps computers understand human language.

MindfulPath uses **DistilBERT**, a transformer-based deep learning model fine-tuned on the SST-2 (Stanford Sentiment Treebank) dataset. It was developed by HuggingFace and runs locally using the `@xenova/transformers` library — no internet or API key needed after the first download.

**Why transformers are better than word dictionaries:**

The older approach (AFINN lexicon) assigned a score to each individual word, without understanding how words relate to each other. The famous problem:

```
Old method: "I am not sad"
→ sees "sad" = -2 → scores as NEGATIVE ❌

DistilBERT: "I am not sad"
→ reads the full sentence → scores as POSITIVE ✅
```

DistilBERT reads the entire sentence at once and understands that "not" changes the meaning of "sad." This is called **contextual understanding** and is the core advantage of transformer models.

**How the model is loaded:**

The model (~67MB) is downloaded from HuggingFace on first startup and cached locally in `node_modules/@xenova/transformers/.cache/`. All future runs use the cached version — no internet needed.

Because `@xenova/transformers` is an ES Module, it is loaded using dynamic `import()` inside the otherwise CommonJS-based Node.js project. The model is pre-warmed at server startup so the first user request is not slow.

### The Web Pages (Frontend)

The pages are built using **EJS templates** — these are like fill-in-the-blank HTML pages. The server fills in the blanks with your data (your name, your mood entries, the chatbot's responses) and sends the completed page to your browser.

The pages use **Bootstrap 5** for styling, which is a popular library that makes websites look clean and professional. We use a dark theme with a purple accent color because:
- Dark themes are easier on the eyes
- Purple is associated with mindfulness and wellness
- It creates a calm, comfortable atmosphere

### The Chat Interface (Frontend Fix)

The chat send button uses a `finally` block to ensure it is always re-enabled after each message — whether the server responded successfully or returned an error. Before this fix, certain server errors could permanently lock the send button, requiring a page refresh to continue chatting.

### The Charts (Chart.js)

Chart.js is a library that draws charts in the browser. MindfulPath uses it to show:
- Your mood trend over time (a line chart showing if your mood is going up or down)
- Dashboard statistics for admins

### Authentication (Login System)

When you log in:
1. The server checks your email and password against the database
2. Your password is compared using **bcrypt** — a special algorithm that hashes (scrambles) passwords so even if someone sees the database, they can't read the passwords
3. If your login is correct, the server creates a **JWT token** (JSON Web Token) — think of it as a digital VIP pass
4. This token is stored in a **cookie** on your browser
5. Every time you visit a page, the server checks your token to confirm who you are

### Three User Roles

| Role | What They Can Do |
|------|-----------------|
| **User** | Chat with AI, log moods, browse meditations, book therapy sessions |
| **Therapist** | View patient sessions, manage bookings, professional profile |
| **Admin** | See system-wide statistics, view all users' chat history, configure AI engine (local vs LLM API) |

## What is CBT (Cognitive Behavioral Therapy)?

CBT is one of the most researched and effective forms of therapy. The basic idea is:

**Our thoughts affect our feelings, and our feelings affect our behavior.**

For example:
- **Thought:** "I'm going to fail this exam"
- **Feeling:** Anxiety, dread
- **Behavior:** Avoiding studying, which makes failure more likely

CBT teaches people to:
1. **Notice** their negative thoughts
2. **Question** whether those thoughts are accurate
3. **Replace** them with more balanced thinking
4. **Practice** healthier behaviors

MindfulPath's chatbot uses simplified versions of these CBT techniques in its conversations.

## Important Note

MindfulPath is a student project designed for educational purposes. While it uses real CBT principles and state-of-the-art NLP techniques:
- It is **not a substitute** for professional mental health treatment
- The crisis detection is basic keyword matching, not a comprehensive clinical assessment
- If you or someone you know is in crisis, please call a helpline or visit a hospital

## Summary

MindfulPath brings together:
1. **Transformer NLP (DistilBERT)** to accurately understand how users feel from their text — handling negation, context, and intensity
2. **CBT (Cognitive Behavioral Therapy)** principles to provide helpful, evidence-based responses
3. **Multi-Provider LLM Support** — admin can upgrade the chatbot to use Anthropic Claude, OpenAI, or Google Gemini for dynamic AI responses, all configurable from a settings page with no code changes
4. **Mood Tracking** to help users see patterns in their emotional health
5. **Meditation** to provide practical relaxation techniques
6. **Therapist Directory** to connect users with professional help
7. **Admin Monitoring** to let administrators view all chatbot conversations for platform oversight
8. **Modern Web Technology** (Node.js, SQLite, Bootstrap) to make it all work together

It demonstrates how modern AI (transformer models and large language models) and web technology can be used to make mental health support more accessible, accurate, and configurable for everyone.
