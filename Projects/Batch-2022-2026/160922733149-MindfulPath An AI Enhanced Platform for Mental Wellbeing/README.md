# MindfulPath — AI Mental Wellbeing Platform

An AI-powered mental wellbeing platform that combines Natural Language Processing (NLP) sentiment analysis with Cognitive Behavioral Therapy (CBT) principles to provide accessible mental health support.

## Features

- **AI Chatbot** — Transformer-based NLP conversational companion using CBT techniques (validation, grounding, thought records, behavioral activation, psychoeducation, reinforcement)
- **Sentiment Analysis** — Real-time DistilBERT transformer model analysis on chat messages (handles negation, intensifiers, context)
- **Crisis Detection** — Automatic detection of crisis keywords with helpline information
- **Mood Tracker** — Daily mood logging (1-5 scale) with optional journaling and sentiment analysis
- **Meditation Library** — 10 guided meditation scripts across 6 categories (stress, anxiety, depression, sleep, focus, mindfulness)
- **Therapist Directory** — Professional profiles with specialties, education, pricing, and therapeutic approach
- **Session Booking** — Book video, audio, or chat therapy sessions with therapists
- **Role-Based Dashboards** — Separate dashboards for Users, Therapists, and Admins
- **Admin Chat History** — Admin can view all users' AI chatbot conversations with full message logs and sentiment data
- **Admin AI Settings** — Admin can switch between local model and external LLM API (Anthropic Claude, OpenAI, Google Gemini) without code changes
- **Smooth Scrolling Chat UI** — Chat window auto-scrolls to latest message; input box is always anchored at the bottom
- **Dark Theme UI** — Bootstrap 5 dark gradient theme with Chart.js mood trend visualizations

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Node.js + Express.js |
| Frontend | EJS Templates + Bootstrap 5 |
| Database | SQLite (better-sqlite3) |
| NLP Engine | @xenova/transformers — DistilBERT (distilbert-base-uncased-finetuned-sst-2-english) |
| Authentication | JWT + bcryptjs |
| Charts | Chart.js |
| Container | Docker |

|Name|      |Roll number|
|Syed Asim  ||160922733149|
|Syed Mazher||160922733143|
|Syed Rayyan||160922733156|
## Project Structure

```
MindfulPath/
├── server.js                  # Express entry point
├── package.json               # Dependencies
├── .env                       # Configuration
├── Dockerfile                 # Docker container
├── db/
│   └── database.js            # SQLite schema + seed data
├── nlp/
│   ├── sentiment.js           # DistilBERT transformer sentiment analysis
│   ├── responses.js           # CBT response templates
│   └── llm.js                 # LLM API integration (Claude, OpenAI, Gemini)
├── middleware/
│   └── auth.js                # JWT auth + role-based access
├── routes/
│   ├── auth.js                # Login, register, logout
│   ├── chat.js                # AI chatbot API + admin chat history routes
│   ├── admin.js               # Admin settings routes
│   ├── mood.js                # Mood tracker
│   ├── meditations.js         # Meditation library
│   ├── therapists.js          # Therapist directory
│   ├── sessions.js            # Session booking
│   └── dashboard.js           # Role-based dashboards
├── views/
│   ├── partials/
│   │   ├── header.ejs         # Shared header + navbar
│   │   └── footer.ejs         # Shared footer + scripts
│   ├── login.ejs              # Login page
│   ├── register.ejs           # Registration page
│   ├── dashboard.ejs          # Role-based dashboard
│   ├── chat.ejs               # AI chatbot interface
│   ├── admin-chats.ejs        # Admin: user chat history viewer
│   ├── admin-settings.ejs     # Admin: AI engine settings
│   ├── mood.ejs               # Mood tracker
│   ├── meditations.ejs        # Meditation library
│   ├── therapists.ejs         # Therapist directory
│   ├── sessions.ejs           # Session management
│   ├── about.ejs              # About page
│   └── 404.ejs                # Not found page
├── public/
│   ├── css/style.css          # Dark theme styles
│   └── js/
│       ├── chat.js            # Chat interface logic
│       └── charts.js          # Chart.js mood charts
├── README.md
└── PROJECT_EXPLANATION.md
```

## Installation (Windows / macOS / Linux)

### Prerequisites

- **Node.js** 18 or higher — Download from [https://nodejs.org](https://nodejs.org)
- **Git** — Download from [https://git-scm.com](https://git-scm.com)
- Approximately **200MB free disk space** — the DistilBERT model (~67MB) is downloaded and cached on first run

### Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd MindfulPath
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the server:**
   ```bash
   node server.js
   ```

4. **Open in browser:**
   ```
   http://127.0.0.1:5006
   ```

The SQLite database is auto-created with sample data on first run.

> **First Run Note:** On first startup the server will download the DistilBERT sentiment model (~67MB) from HuggingFace and cache it in `node_modules/@xenova/transformers/.cache/`. This happens only once. Subsequent starts load the model from cache and are ready in seconds.

### Demo Login Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@mindfulpath.com | admin123 |
| Therapist | dr.sarah@mindfulpath.com | doctor123 |
| Therapist | dr.omar@mindfulpath.com | doctor123 |
| User | patient@mindfulpath.com | patient123 |

## Docker Setup

```bash
# Build the image
docker build -t mindfulpath .

# Run the container
docker run -p 5006:5006 mindfulpath
```

Open `http://127.0.0.1:5006` in your browser.

## How the NLP Chatbot Works

### Sentiment Analysis Pipeline

1. **Input** — User types a message
2. **Transformer Inference** — Text is passed to the locally-running DistilBERT model (`distilbert-base-uncased-finetuned-sst-2-english`)
3. **Confidence Scoring** — Model returns POSITIVE and NEGATIVE confidence scores (0.0–1.0)
4. **Classification** — Scores are mapped to a comparative value used for CBT response selection

The transformer model correctly handles:
- **Negation** — "I am not sad" → positive (old AFINN lexicon would score this as negative)
- **Intensifiers** — "I feel a little bad" vs "I feel absolutely terrible" → different severity levels
- **Context** — Full sentence understanding rather than word-by-word scoring

### Sentiment Score Mapping

| Model Output | Comparative Value | Classification |
|---|---|---|
| NEGATIVE confidence ≥ 0.85 | -0.6 | very_negative |
| NEGATIVE confidence ≥ 0.65 | -0.3 | negative |
| NEGATIVE confidence > 0.50 | -0.15 | mildly_negative |
| POSITIVE confidence ≥ 0.60 | +0.3 | positive |
| Otherwise | 0 | neutral |

### CBT Response Selection

| Sentiment Level | Technique | Purpose |
|----------------|-----------|---------|
| Very Negative (< -0.5) | Validation + Grounding | Acknowledge emotions, anchor to present moment |
| Negative (-0.5 to -0.2) | Thought Record | Challenge negative thought patterns |
| Mild Negative (-0.2 to -0.1) | Behavioral Activation | Encourage small positive activities |
| Neutral (-0.1 to 0.1) | Check-in + Psychoeducation | General wellness support and education |
| Positive (> 0.1) | Reinforcement | Strengthen positive feelings, gratitude practice |

### Crisis Detection

The system monitors for crisis keywords (e.g., "suicide", "self-harm", "hopeless", "end it all"). When detected, it immediately shows:
- Vandrevala Foundation: 1860-2662-345 (24/7)
- iCall: 9152987821
- AASRA: 9820466726

Crisis detection runs before the transformer model — it is a fast keyword check that cannot be delayed by model inference.

## Admin: AI Engine Settings

Admins can configure the chatbot response engine at `/admin/settings` without touching any code.

### Two Modes

| Mode | Description |
|------|-------------|
| **Local Model** | DistilBERT sentiment → pre-written CBT templates. No API key, no cost, no internet. |
| **LLM API** | DistilBERT sentiment → dynamic response from an external LLM. Requires API key. |

### Supported LLM Providers

| Provider | Models | API Key Source |
|----------|--------|----------------|
| **Anthropic Claude** | `claude-haiku-4-5-20251001`, `claude-sonnet-4-6` | console.anthropic.com |
| **OpenAI** | `gpt-4o-mini`, `gpt-4o` | platform.openai.com |
| **Google Gemini** | `gemini-2.0-flash`, `gemini-1.5-pro` | aistudio.google.com/app/apikey |

### How LLM Mode Works
- Sentiment analysis **always runs locally** — only the response generation is delegated to the LLM
- Crisis keyword detection **always runs locally** — the LLM is never called for crisis messages
- The last session messages are sent as **conversation context** so the LLM gives coherent follow-up replies
- If the API call fails for any reason, the chatbot **silently falls back** to local CBT responses
- Settings (mode, provider, key, model) are stored in the local SQLite `app_settings` table

### Test Connection
The settings page includes a **Test Connection** button that sends a test message to the configured provider and shows the reply — confirming the key and model are valid before saving.

## Admin: Chat History Feature

Admins can monitor all user AI chatbot conversations through a 3-level drill-down interface:

| URL | Description |
|-----|-------------|
| `/chat/admin/chats` | All users and therapists — session count, total messages, last chat time |
| `/chat/admin/chats/user/:id` | All chat sessions for a specific user with sentiment badges |
| `/chat/admin/chats/session/:id` | Full message log with chat bubbles, per-message sentiment labels, and CBT technique used |

Access via the **"Chat History"** link in the admin navbar, or the quick-access card on the admin dashboard. All routes are protected with `authorize('admin')` — any other role receives a 403 error.

## Database Schema

The application uses SQLite with 8 tables:

- **users** — User accounts with roles (user, therapist, admin)
- **therapists** — Professional profiles linked to user accounts
- **sessions** — Therapy session bookings
- **meditations** — Guided meditation library
- **mood_entries** — Daily mood logs with sentiment scores
- **chat_sessions** — AI chatbot conversation sessions
- **chat_messages** — Individual messages with sentiment analysis data
- **app_settings** — Admin-configurable settings (NLP mode, LLM provider, API key, model)

## Test Cases

### Test Case 1: User Registration
1. Go to `http://127.0.0.1:5006/register`
2. Fill in: Name = Alice, Email = alice@test.com, Password = pass123, Role = User
3. Click Register
- **Expected:** Redirect to login page with success message

### Test Case 2: Therapist Registration
1. Go to `/register`
2. Fill: Name = Dr. Priya, Email = priya@test.com, Password = doc123, Role = Therapist
3. Fill therapist fields: Specialties = Depression + Anxiety, Education = PhD Psychology, Experience = 5, License = MH12345, Price = 500
- **Expected:** Redirect to login with success message. Therapist profile created.

### Test Case 3: Login and Role-Based Dashboard
1. Login as `admin@mindfulpath.com` / `admin123` → See admin dashboard with system statistics and Chat History quick-access card
2. Login as `dr.sarah@mindfulpath.com` / `doctor123` → See therapist dashboard with sessions
3. Login as `patient@mindfulpath.com` / `patient123` → See user dashboard with mood chart and quick actions
- **Expected:** Each role sees its appropriate dashboard

### Test Case 4: AI Chatbot — Start Conversation
1. Login as user → Click "AI Chat" in navbar
2. Click "New Chat" → Bot sends a greeting
3. Type "I've been feeling really anxious lately" → Send
- **Expected:** Sentiment analyzed (negative), bot responds with a CBT technique (thought record)

### Test Case 5: AI Chatbot — Transformer Sentiment (Negation Handling)
1. Type "I am not sad" → Expected: positive sentiment (green dot)
2. Type "I am not happy at all" → Expected: negative sentiment (red dot)
3. Type "I feel absolutely terrible and overwhelmed" → Expected: very_negative (red dot, validation/grounding response)
4. Type "I'm so happy today, everything went perfectly!" → Expected: positive (green dot, reinforcement response)
- **Expected:** Each message shows correct sentiment badge. Negation handled correctly (unlike old AFINN lexicon).

### Test Case 6: AI Chatbot — Crisis Detection
1. Type a message with crisis keywords (e.g., "I feel like ending it all")
- **Expected:** Bot shows crisis helpline information prominently with supportive message

### Test Case 7: AI Chatbot — Continuous Conversation
1. Start a new chat and send multiple messages back and forth
- **Expected:** Send button remains enabled after every response. Chat continues indefinitely without locking up.

### Test Case 8: AI Chatbot — Conversation History
1. Have multiple chat sessions
2. Click on a previous session in the sidebar
- **Expected:** Previous messages load with sentiment badges and bot responses

### Test Case 9: Mood Tracker — Log Mood
1. Click "Mood Tracker" in navbar
2. Select mood (e.g., "Sad" face)
3. Write journal entry: "Had a tough day at work"
4. Click Submit
- **Expected:** Entry saved, sentiment analysis shown, mood chart updates

### Test Case 10: Mood Tracker — View Trends
1. After logging several mood entries
2. View the mood chart on the mood page
- **Expected:** Line chart shows mood scores over time with correct dates

### Test Case 11: Meditation Library
1. Click "Meditations" → See all meditations in card grid
2. Click a category filter (e.g., "Anxiety")
3. Click on a meditation card
- **Expected:** Filtered view shows only that category. Detail view shows full guided text.

### Test Case 12: Therapist Directory
1. Click "Therapists" → See therapist cards
2. Click on a therapist card
- **Expected:** Full profile with specialties, education, experience, pricing, therapeutic approach

### Test Case 13: Book Therapy Session
1. Login as user → Go to Sessions
2. Click "Book Session" → Select therapist, date, time, type
3. Submit
- **Expected:** Session created with "scheduled" status, appears in session list

### Test Case 14: Cancel Session
1. On sessions page, click "Cancel" on a scheduled session
- **Expected:** Status changes to "cancelled", shown with red badge

### Test Case 15: Admin — View Chat History
1. Login as `admin@mindfulpath.com` / `admin123`
2. Click "Chat History" in navbar (or the quick-access card on dashboard)
3. Click "View" on any user → See list of their chat sessions with sentiment badges
4. Click on a session → See full message log with chat bubbles, sentiment labels per message, and CBT technique labels
- **Expected:** 3-level drill-down works. Full conversation visible. Non-admin users cannot access these routes (403 error).

### Test Case 16: Dashboard Analytics
1. Login as admin → Dashboard shows: Total Users, Therapists, Sessions, Chat Messages, Mood Entries
2. Login as user → Dashboard shows: Mood trend chart (last 7 days), recent chats, upcoming sessions
- **Expected:** Correct counts and charts with seeded data

### Test Case 17: About Page
1. Click "About" in navbar
2. View: How NLP Works, How CBT Chatbot Works, Tech Stack, Features
- **Expected:** Complete project information with NLP explanation and CBT technique table

### Test Case 18: Admin — AI Engine Settings (Local Mode)
1. Login as admin → Click "AI Settings" in navbar
2. Verify "Local Model" is selected by default
3. Click Save
4. Open chat as a user and send a message
- **Expected:** Bot responds with a pre-written CBT template response

### Test Case 19: Admin — Switch to LLM API Mode
1. Login as admin → Go to `/admin/settings`
2. Select "LLM API" mode
3. Click the provider card (Anthropic / OpenAI / Gemini)
4. Enter a valid API key and model name
5. Click "Test Connection" — verify a reply is shown
6. Click Save Settings
7. Open chat as a user and send a message
- **Expected:** Bot responds with a dynamic, contextual response from the selected LLM

### Test Case 20: Admin — Switch LLM Provider
1. In AI Settings, switch from one provider to another (e.g., Claude → Gemini)
2. Enter the Gemini API key (`AIza...`) and model `gemini-2.0-flash`
3. Save and test chat
- **Expected:** Model field auto-fills with provider default. Chat responses come from Gemini.

### Test Case 21: Chat UI — Smooth Scroll
1. Start a new chat and send 6+ messages
2. Observe the chat window as messages arrive
- **Expected:** Chat window smoothly scrolls to the latest message. Input box stays anchored at the bottom. Older messages are accessible by scrolling up — not removed.

### Test Case 22: Access Control
1. Logout → Try to access `/dashboard` directly
2. Login as user → Try to access `/chat/admin/chats` directly
3. Login as admin → Access `/chat/admin/chats`
- **Expected:** Unauthenticated users redirected to login. Non-admin users get 403. Admin access granted.

## Notes

- The SQLite database file (`mindfulpath.db`) is auto-created on first run with sample data
- Delete `mindfulpath.db` and restart the server to reset all data
- The DistilBERT model is downloaded once and cached locally — no API key or internet needed after the first run
- Crisis detection is keyword-based and should not replace professional crisis intervention
- The `@xenova/transformers` package uses ES module syntax — it is loaded via dynamic `import()` inside the CommonJS `sentiment.js` module
- LLM API keys are stored in the local SQLite `app_settings` table — keep the server secure and do not expose the database publicly
- In LLM API mode, if the API call fails the chatbot automatically falls back to local CBT responses with no error shown to the user
