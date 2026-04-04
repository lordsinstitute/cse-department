# Prompt-Driven AI Web Automation

Use natural language to automate browser tasks powered by **Claude AI** + **Playwright**.

## Modules

### 1. Web Data Extraction Agent
Type a natural language prompt (e.g., *"Scrape laptop prices from this page"*) → the AI agent navigates the page using Playwright → extracts structured data → exports to Excel/CSV.

### 2. AI Form Filler Bot
Upload a PDF resume → Claude extracts structured data → point to a web form → the AI agent fills it automatically.

Both modules share a **live browser view** with real-time screenshots and color-coded action logs streamed via SocketIO.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.12+ | Runtime |
| Flask | Web server and UI |
| Flask-SocketIO | Real-time screenshot streaming and action logs |
| Flask-Login | Session-based user authentication |
| Playwright | Browser automation (headless Chromium) |
| Claude API (Anthropic) | LLM reasoning via Tool Use |
| pymupdf4llm | PDF resume → markdown conversion |
| pandas + openpyxl | Excel/CSV data export |
| Bootstrap 5 | Chrome-style light theme UI |

---

## Prerequisites

- **Python 3.12** or later (3.13 also works; 3.14 may have compatibility issues with some packages)
- **Anthropic API Key** — Get one from [console.anthropic.com](https://console.anthropic.com/) (requires credits on your account)
- **pip** — Python package manager
- **Git** (optional) — For cloning the project

---

## Installation & Setup

### Step 1: Create a Virtual Environment

```bash
cd prompt-web-automation
python3.12 -m venv venv
```

### Step 2: Activate the Virtual Environment

**macOS / Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Playwright Chromium Browser

```bash
playwright install chromium
```

### Step 5: Configure API Key

```bash
cp .env.example .env
```

Open `.env` in a text editor and replace `your-api-key-here` with your actual Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
```

> **Note:** Your API key must start with `sk-ant-`. Keys starting with `sk-proj-` are OpenAI keys and will not work.

> **Note:** Your Anthropic account must have credits loaded. Purchase credits at [console.anthropic.com/settings/billing](https://console.anthropic.com/settings/billing).

### Step 6: Run the Application

```bash
python app.py
```

The server starts on **http://localhost:5050**. Open this URL in your browser.

You will be redirected to the **login page**. Sign in with the default credentials:

- **Username:** `admin`
- **Password:** `admin123`

After login, you'll see the dashboard with:
- A green **"API Key Configured"** badge (if your key is set correctly)
- Two module cards: **Web Data Extraction** and **AI Form Filler**

---

## Configuration (Optional)

All settings are in `.env`:

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | *(required)* | Your Anthropic API key |
| `CLAUDE_MODEL` | `claude-sonnet-4-20250514` | Claude model to use |
| `MAX_AGENT_STEPS` | `25` | Maximum steps per agent run |
| `STEP_DELAY` | `1.0` | Delay (seconds) between agent steps |

---

## Usage Guide

### Module 1: Web Data Extraction

1. Open **http://localhost:5050/scraper**
2. Enter the **Target URL** of the website to scrape
3. Describe what data you want in the **task description** field
4. Click **Start Extraction**
5. Watch the AI agent work in real-time:
   - **Left panel:** Live browser screenshot updates after each action
   - **Right panel:** Color-coded action log
6. When the agent finishes, click **Download Excel** to get the extracted data

**How it works:**
- The agent reads the page's DOM (interactive elements + visible text)
- Sends the page state to Claude, which decides what action to take
- Executes the action (click, scroll, navigate, extract data)
- Repeats until all data is collected, then exports to Excel

### Module 2: AI Form Filler

1. Open **http://localhost:5050/form-filler**
2. **Step 1 — Upload Resume:**
   - Click **Choose File** and select a PDF resume
   - Click **Upload & Parse Resume**
   - Wait for Claude to extract structured data (name, email, skills, etc.)
   - Review the parsed data in the preview panel
   - Optionally click **Edit Data** to modify any field as JSON
3. **Step 2 — Fill a Form:**
   - Enter the URL of the web form to fill, OR click **Use Demo Form** for the built-in demo
   - Click **Start Filling**
   - Watch the agent fill each field in real-time
4. The agent matches form fields to resume data, fills them, and submits

**How it works:**
- PDF → markdown conversion via pymupdf4llm
- Claude extracts structured fields (name, email, phone, education, experience, skills) using forced tool choice
- The form filler agent receives this data and intelligently matches it to form fields
- Fields are filled using Playwright automation (fill, select, click)

---

## Demo & Testing

### Test 1: Web Data Extraction (Scraper)

1. Go to **http://localhost:5050/scraper**
2. **URL:** `https://books.toscrape.com/`
3. **Task:** `Extract the title and price of all books on this page`
4. Click **Start Extraction**
5. Watch the agent:
   - Read book titles and prices from the page
   - Optionally navigate to the next page for more data
   - Call `done` when finished
6. Click **Download Excel** and verify the data in the spreadsheet

**Other scraping targets to try:**
- `https://books.toscrape.com/catalogue/category/books/science_22/index.html` → *"Get all science book titles and prices"*
- Any Wikipedia table page → *"Extract the data from the main table on this page"*

### Test 2: AI Form Filler

1. Go to **http://localhost:5050/form-filler**
2. Upload the sample resume at `demo/sample_resume.pdf` (included in the project)
3. Review the parsed data — it should show:
   - **Name:** Alex Johnson
   - **Email:** alex.johnson@email.com
   - **Phone:** +1 (555) 987-6543
   - **Skills:** Python, JavaScript, TypeScript, React, Node.js, etc.
4. Click **Use Demo Form** to pre-fill the URL with the built-in demo form
5. Click **Start Filling**
6. Watch the agent:
   - Fill Full Name, Email, Phone, Address fields
   - Select "Full Stack Developer" from the Position dropdown
   - Select "5-10 years" for experience
   - Select "Bachelor's Degree" for education
   - Fill in University, Skills, and Summary text areas
   - Click a radio button for availability
   - Click Submit
7. The demo form shows a success message with all filled data

### Test 3: Live Browser View

Both modules display:
- **Real-time browser screenshots** — updated after every agent action
- **Color-coded action logs:**
  - Gray — info messages (step count, navigation)
  - Blue — action messages (click, fill, select)
  - Purple — thinking messages (Claude's reasoning)
  - Green — success messages (data extracted, task done)
  - Red — error messages (action failures, API errors)

### Test 4: Error Handling

| Scenario | Expected Behavior |
|---|---|
| Not logged in | Redirected to `/auth/login` with flash message |
| Wrong username/password | Flash: "Invalid username or password" on login page |
| Missing API key | Yellow warning on dashboard, error message when starting agent |
| Invalid/expired API key | Error log: "authentication_error" after first step |
| No credits on account | Error log: "credit balance too low" |
| Invalid URL | Blocked with descriptive error (scheme/IP validation) |
| `file://` or `ftp://` URL | Blocked: "URL scheme not allowed" |
| Internal IP (192.168.x.x) | Blocked: "Access to internal/private IP addresses is blocked" |
| File > 10MB upload | Blocked: "File too large" |
| Path traversal on download | Blocked: filename sanitized + path verified |
| Too many requests (>5/min) | Rate limited: "Too many requests. Please wait X seconds" |
| Empty task/URL fields | Client-side alert preventing submission |
| No resume uploaded | Error message: "No resume data provided" |
| Non-PDF file upload | Error message: "Only PDF files are supported" |
| Agent stuck | Click **Stop** button to terminate |

### Test 5: Stop Functionality

1. Start either the scraper or form filler agent
2. While the agent is running, click the **Stop** button
3. The agent should stop within the current step and report "Agent was stopped by user"

### Test 6: Authentication

1. Open **http://localhost:5050** → should redirect to `/auth/login`
2. Enter wrong credentials → should show "Invalid username or password"
3. Login with `admin` / `admin123` → should redirect to dashboard
4. Verify navbar shows username and **Logout** link
5. Navigate to `/scraper`, `/form-filler`, `/history` → all accessible
6. Click **Logout** → should redirect to login page
7. Try accessing `/scraper` directly → should redirect to login

---

## Architecture

### Agent Loop (Observe → Think → Act)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   OBSERVE   │ ──► │    THINK    │ ──► │     ACT     │
│ Extract DOM │     │ Claude API  │     │  Playwright  │
│ state from  │     │ decides the │     │  executes   │
│ the page    │     │ next action │     │  the action │
└─────────────┘     └─────────────┘     └─────────────┘
       ▲                                       │
       │            ┌─────────────┐            │
       └────────────│    EMIT     │◄───────────┘
                    │ Screenshot  │
                    │ + log via   │
                    │  SocketIO   │
                    └─────────────┘
```

1. **OBSERVE:** Extract page state — URL, title, all interactive elements (links, buttons, inputs, dropdowns) with sequential IDs `[0], [1], [2]...`, and truncated visible text (~2000 chars)
2. **THINK:** Send state to Claude with tool definitions → Claude returns a `tool_use` response block
3. **ACT:** Execute the chosen tool via Playwright (click, fill, select, navigate, scroll, extract_data, done)
4. **EMIT:** Take a JPEG screenshot and emit it + action log to the frontend via SocketIO
5. **REPEAT** until Claude calls `done` or max 25 steps reached

### Why DOM-Based (Not Screenshot)?

| Approach | Cost | Speed | Success Rate |
|---|---|---|---|
| Screenshot-based | High (image tokens) | Slow | ~64% |
| **DOM/text-based** | **3x cheaper** | **3x faster** | **~89%** |

Text-based DOM extraction sends element metadata as text, not images. Element IDs provide precise targeting instead of coordinate guessing.

### Claude Tool Definitions (7 Tools)

| Tool | Parameters | Description |
|---|---|---|
| `click` | `element_id`, `reason` | Click an interactive element |
| `fill` | `element_id`, `value` | Fill a text input or textarea |
| `select_option` | `element_id`, `value` | Select a dropdown option |
| `navigate` | `url` | Navigate to a URL |
| `scroll` | `direction` (up/down) | Scroll the page |
| `extract_data` | `data` (array), `description` | Collect structured data (scraper only) |
| `done` | `summary`, `success` | Signal task completion |

### Flask ↔ Playwright Bridge

Playwright is async (`asyncio`), but Flask is synchronous. `BrowserManager` solves this by:
1. Running an `asyncio` event loop on a daemon thread
2. Using `run_coroutine_threadsafe()` to bridge sync calls to async Playwright operations

### PDF Parsing Pipeline

```
PDF File → pymupdf4llm → Markdown Text → Claude (forced tool_choice) → Structured JSON
```

Claude is forced to use the `save_resume_data` tool via `tool_choice={"type": "tool", "name": "save_resume_data"}`, guaranteeing structured output with fields: full_name, email, phone, address, summary, education[], experience[], skills[].

### SocketIO Room Isolation

Each browser tab generates a unique session ID (room). The server uses `join_room()` and emits screenshots/logs only to that specific room. Multiple users can run agents simultaneously without interference.

### Message Trimming

After many steps, the conversation grows large. The agent trims messages by:
- Always keeping the first message (task description + initial state)
- Keeping the last ~9 messages (recent context)
- Never breaking `tool_use` / `tool_result` pairs (cuts only at plain user messages)

---

## Authentication

The application requires login to access all features. Authentication uses Flask-Login with session-based cookies and a SQLite user database (`auth.db`).

- **Default credentials:** `admin` / `admin123`
- All routes are protected with `@login_required` (except the demo form and login page)
- Sessions persist across browser refreshes (remember me enabled)
- Passwords are hashed using Werkzeug's `generate_password_hash` (pbkdf2:sha256)
- The default admin user is auto-created on first startup

---

## Security Features

| Feature | Description |
|---|---|
| **Login Required** | All routes protected with Flask-Login `@login_required` decorator |
| **Password Hashing** | Passwords stored as pbkdf2:sha256 hashes via Werkzeug |
| **Session Cookies** | Secure session-based authentication with Flask secret key |
| **URL Validation** | Blocks `file://`, `ftp://`, `data://`, `javascript:` schemes. Only `http://` and `https://` allowed |
| **Internal IP Blocking** | Blocks `127.0.0.1`, `10.*`, `192.168.*`, `172.16-31.*`, cloud metadata IPs |
| **API Key Masking** | Any `sk-ant-*` patterns in logs are replaced with `sk-ant-***MASKED***` before display |
| **File Upload Limit** | Max 10MB for PDF uploads |
| **Path Traversal Protection** | Download filenames sanitized with `secure_filename()`, paths verified inside export directory |
| **Rate Limiting** | Max 5 agent starts per IP per minute (in-memory) |
| **Localhost Control** | Localhost blocked for scraper, allowed for form filler (demo form) |

---

## Task History

All agent runs are automatically saved to a local SQLite database (`history.db`).

- **Dashboard** shows the 5 most recent runs in a "Recent Activity" card
- **History page** (`/history`) shows all runs with: timestamp, module, URL, status, steps, items, duration, download link
- Click any row to see the full summary
- **Clear All** button to delete history
- **API endpoints:**
  - `GET /api/history` — JSON list of all runs
  - `POST /api/history/clear` — clear all history

---

## Project Structure

```
prompt-web-automation/
├── app.py                              # Entry point — runs server on port 5050
├── config.py                           # Settings, API key loading from .env
├── requirements.txt                    # Python dependencies
├── .env.example                        # API key template
├── .gitignore                          # Git ignore rules
├── core/
│   ├── browser/
│   │   ├── manager.py                  # BrowserManager: async bridge, lifecycle
│   │   ├── page_state.py              # DOM extraction, element indexing
│   │   └── actions.py                 # Action executor (click, fill, navigate, etc.)
│   ├── auth.py                        # User authentication (Flask-Login + SQLite)
│   ├── security.py                    # URL validation, API key masking, rate limiter
│   ├── history.py                     # Task history (SQLite storage)
│   ├── agents/
│   │   ├── base_agent.py             # Base observe-think-act loop
│   │   ├── scraper_agent.py          # Data extraction agent
│   │   └── form_filler_agent.py      # Form filling agent
│   ├── llm/
│   │   ├── claude_client.py          # Claude API wrapper with tool use
│   │   ├── prompts.py                # System prompts for each agent
│   │   └── tools.py                  # Tool definitions (7 tools)
│   ├── parsers/
│   │   └── pdf_parser.py            # Resume PDF → structured data
│   └── exporters/
│       └── excel_exporter.py         # Data → Excel/CSV export
├── web/
│   ├── __init__.py                   # Flask app factory + SocketIO init
│   ├── routes/
│   │   ├── auth.py                   # Login/logout routes
│   │   ├── main.py                   # Home dashboard + history routes
│   │   ├── scraper.py               # Scraper endpoints
│   │   └── form_filler.py           # Form filler endpoints
│   ├── templates/
│   │   ├── base.html                # Base template (Bootstrap 5, SocketIO)
│   │   ├── login.html               # Login page
│   │   ├── index.html               # Dashboard with module cards
│   │   ├── scraper.html             # Scraper UI (prompt + live view)
│   │   ├── form_filler.html         # Form filler UI (upload + live view)
│   │   └── history.html             # Task history page
│   └── static/
│       ├── css/style.css            # Chrome-style light theme
│       └── js/socket-handler.js     # SocketIO client for screenshots + logs
├── demo/
│   ├── sample_form.html             # Built-in demo job application form
│   └── sample_resume.pdf            # Sample PDF resume for testing
├── uploads/                          # PDF uploads directory (gitignored)
├── exports/                          # Excel/CSV output directory (gitignored)
├── README.md                         # This file
└── PROJECT_EXPLANATION.md            # Detailed architecture explanation + viva Q&A
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `pip install` fails with PEP 668 error | Use a virtual environment: `python3.12 -m venv venv && source venv/bin/activate` |
| `greenlet` build fails | Use Python 3.12 or 3.13 (not 3.14) |
| `playwright install` fails | Run `playwright install-deps` first (Linux only) |
| "authentication_error" / "invalid x-api-key" | Check your API key in `.env` — must start with `sk-ant-` |
| "credit balance too low" | Purchase credits at [console.anthropic.com/settings/billing](https://console.anthropic.com/settings/billing) |
| Port 5050 already in use | Kill the existing process: `lsof -ti:5050 \| xargs kill` |
| Can't login / forgot password | Default credentials are `admin` / `admin123`. Delete `auth.db` and restart to reset |
| Agent stuck or looping | Click the **Stop** button, then retry with a clearer task description |
| PDF parsing fails | Ensure the PDF has selectable text (not a scanned image) |
| No screenshots appearing | Check browser console for SocketIO connection errors |

---

## API Key Security

- Your API key is stored locally in `.env` (gitignored — never committed)
- The key is only used server-side to call the Anthropic API
- API keys in log messages are automatically masked (`sk-ant-***MASKED***`)
- Never share your API key or commit it to version control
