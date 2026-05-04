# Online Integrated Development Environment

A Flask web application providing a browser-based code editor with real Python execution and AI-powered code assistance. Write, run, and analyze code directly in your browser using Monaco Editor (the engine behind VS Code).

## Team Members

-Mohammed Abdul Waqeed
-Mohd Yaseen
-Fardeen Ahmed
-Wahaj Ather

## Features

- **Monaco Code Editor** — Professional-grade editor with syntax highlighting, auto-indent, bracket matching
- **Python Code Execution** — Run Python code with real-time output and error display
- **AI Code Assistant (Dual Mode)** — Analyze, explain, refactor, or generate code
- **6 Languages Supported** — Python, JavaScript, Java, C++, HTML, CSS
- **Code Snippets** — Save and reuse code snippets per user
- **Session History** — Track all past coding sessions with code and output
- **User Authentication** — Login/register with password hashing

## AI Assistant Modes

| Mode | Badge | How It Works |
|------|-------|-------------|
| **Mock AI** (default) | Yellow | Pattern-based code analysis — detects errors, explains structure, suggests improvements. No API key needed. |
| **Live AI** (optional) | Green | Google Gemini API — real AI-powered analysis, explanation, and code generation. |

## AI Actions

| Action | Description |
|--------|-------------|
| Analyze | Find errors, count functions/classes/loops, syntax check |
| Explain | Line-by-line explanation of what the code does |
| Refactor | Suggest improvements — better names, cleaner patterns |
| Generate | Create code from a text prompt (e.g., "factorial", "linked list") |

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation (Windows)

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

4. **Run the application:**
```bash
python app.py
```
Open http://localhost:5016 in your browser.

5. **Login:**
- Username: `admin`
- Password: `admin123`

## Google Gemini API Setup (Optional — for Live AI)

The app works in **two modes**:

### Mock AI Mode (Default)
No configuration needed. The AI assistant uses pattern-based analysis to detect errors, explain code, suggest refactoring, and generate common code snippets. All features work out of the box.

### Live AI Mode
To enable real AI-powered code assistance:

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Click **Create API Key**
3. Copy the generated key
4. Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_api_key_here
```
5. Restart the application
6. The navbar badge will change from "Mock AI" to "Live AI"

**Note:** The Gemini API free tier allows 60 requests per minute, which is sufficient for demo/testing.

## Docker Deployment

```bash
docker build -t online-ide .
docker run -p 5016:5016 online-ide
```

To use Live AI in Docker:
```bash
docker run -p 5016:5016 -e GOOGLE_API_KEY=your_key online-ide
```

## Project Structure

```
code/
├── app.py                     # Flask app with all routes
├── ai_assistant.py            # Dual-mode AI: mock engine + Gemini API
├── code_runner.py             # Safe Python execution via subprocess
├── .env.example               # Template for API key
├── templates/
│   ├── base.html              # Emerald green dark theme
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── home.html              # Dashboard with stats
│   ├── editor.html            # Main IDE: Monaco + AI + terminal
│   ├── snippets.html          # Saved code snippets
│   ├── history.html           # Past sessions
│   └── about.html             # Project info
├── Dockerfile
├── requirements.txt
└── .gitignore
```

## Supported Languages

| Language | Editor | Execution | AI Analysis |
|----------|--------|-----------|-------------|
| Python | Yes | Yes | Yes |
| JavaScript | Yes | — | Yes |
| Java | Yes | — | Yes |
| C++ | Yes | — | Yes |
| HTML | Yes | — | Yes |
| CSS | Yes | — | Yes |

## Test Cases

1. Login as admin/admin123 → dashboard with stat cards
2. Editor loads Monaco Editor with Python syntax highlighting
3. Switch language dropdown → editor mode changes (JS, Java, etc.)
4. Write `print("Hello World")` → Run → output shows "Hello World"
5. Write code with error → Run → stderr shows traceback
6. Run non-Python code → message "Execution available for Python only"
7. Run `import os` → blocked with security warning
8. AI Analyze → shows code statistics and issues
9. AI Explain → line-by-line explanation
10. AI Refactor → improvement suggestions
11. AI Generate "factorial" → factorial code generated
12. Save snippet → appears in Snippets page
13. Load snippet from Snippets → opens in editor
14. History shows past sessions with code and output
15. Register new user → redirect to login with success
16. Duplicate username → error message
17. Access /editor without login → redirect to login
18. Navbar shows "Mock AI" badge (no API key)
19. About page shows features, languages, tech stack

## Technology Stack

- **Backend:** Python, Flask
- **Code Editor:** Monaco Editor (VS Code engine, via CDN)
- **AI:** Google Gemini API (optional), Pattern-based mock engine
- **Frontend:** Bootstrap 5, Bootstrap Icons, JavaScript (Fetch API)
- **Database:** SQLite
- **Security:** Werkzeug password hashing, subprocess sandboxing
