# Online Integrated Development Environment — Project Explanation

## What Does This Project Do?

Imagine you want to write and run code, but you don't want to install anything on your computer — no Python, no VS Code, no complicated setup. This project gives you a full code editor right in your web browser! Just open the website, type your code, and click Run.

It's like having VS Code in your browser, but simpler and with a built-in AI assistant that can help you understand code, find errors, and even write code for you.

## How Does It Work? (Step by Step)

### Step 1: The Code Editor

When you open the Editor page, you see a professional code editor called **Monaco Editor**. This is actually the same editor engine that powers Visual Studio Code (the most popular code editor in the world!). It gives you:

- **Syntax highlighting** — different parts of your code are colored (keywords in purple, strings in green, comments in gray, etc.)
- **Line numbers** — so you can easily reference specific lines
- **Auto-indent** — when you press Enter after a colon in Python, it automatically indents the next line
- **Bracket matching** — when you click on a bracket, it highlights the matching one

You can switch between 6 programming languages: Python, JavaScript, Java, C++, HTML, and CSS. The editor automatically adjusts its highlighting for each language.

### Step 2: Running Code

When you write Python code and click the **Run** button:

1. Your code is sent from the browser to the server (the Flask backend)
2. The server saves your code to a temporary file
3. It runs the file using Python's `subprocess` module (like running `python myfile.py` in the terminal)
4. Whatever the program prints (stdout) is captured
5. Any errors (stderr) are also captured
6. Both are sent back to your browser and displayed in the terminal panel at the bottom

There are safety measures in place:
- **Timeout:** Code stops after 10 seconds (so infinite loops don't crash the server)
- **Blocked imports:** Dangerous modules like `os`, `subprocess`, and `sys` are blocked so code can't harm the server
- **Temporary files:** Code files are deleted after execution

Only Python can be executed. For other languages, you can still write code and use the AI assistant to analyze it.

### Step 3: AI Code Assistant

The AI assistant can do 4 things with your code:

**Analyze** — The AI scans your code and reports:
- How many lines, functions, classes, loops, and imports it found
- Whether there are syntax errors
- Common issues (missing docstrings, single-character variable names, etc.)

**Explain** — The AI reads your code line by line and explains what each part does in plain English. Great for understanding someone else's code!

**Refactor** — The AI suggests improvements:
- Use `enumerate()` instead of `range(len())`
- Add docstrings to functions
- Use f-strings instead of string concatenation
- Use more descriptive variable names

**Generate** — You type a description (like "factorial" or "linked list") and the AI generates ready-to-use code for that task. It knows 15+ common programming tasks.

### Step 4: Dual AI Modes

The app works in two modes:

- **Mock AI (default):** The AI assistant uses pattern matching and templates — it's built right into the code, no internet needed. It detects real Python syntax errors using Python's `compile()` function and has pre-written code snippets for 15+ tasks. The navbar shows a yellow "Mock AI" badge.

- **Live AI (optional):** If you set up a Google Gemini API key (free!), the AI uses Google's actual AI model to analyze your code. This gives much more detailed and context-aware responses. The navbar shows a green "Live AI" badge.

### Step 5: Saving and History

- **Save Snippets:** Click the Save button to store your code with a title. You can load it later from the Snippets page.
- **Session History:** Every time you run code or ask the AI, it's logged. The History page shows all your past sessions with the code you wrote, the output, and any AI responses.

## What Does Each File Do?

| File | Purpose |
|------|---------|
| `app.py` | The main website — handles all routes, user login, code execution, AI requests |
| `code_runner.py` | Runs Python code safely using subprocess with timeout and security checks |
| `ai_assistant.py` | The AI brain — mock mode (pattern analysis) and real mode (Google Gemini API) |
| `templates/base.html` | Page layout with emerald green dark theme |
| `templates/login.html` | Login page |
| `templates/register.html` | Registration page |
| `templates/home.html` | Dashboard with stats and recent sessions |
| `templates/editor.html` | The main IDE — Monaco Editor + AI panel + output terminal |
| `templates/snippets.html` | Saved code snippets gallery |
| `templates/history.html` | Past coding sessions |
| `templates/about.html` | Project information and feature list |

## What Is Monaco Editor?

Monaco Editor is the code editing component that powers Visual Studio Code. Microsoft open-sourced it so anyone can use it in web applications. It provides:

- Syntax highlighting for 50+ programming languages
- IntelliSense (code completion)
- Code folding
- Find and replace
- Multiple cursors
- Minimap
- And much more!

In our project, we load it directly from a CDN (Content Delivery Network), so there's nothing to install. When the editor page loads, the browser downloads Monaco Editor's JavaScript files and creates the editor right in the page.

## What Is subprocess?

In Python, `subprocess` is a module that lets you run other programs from within your Python program. It's like opening a terminal and typing a command.

When a user submits code to run:
```python
result = subprocess.run(
    ['python', 'temp_file.py'],  # The command to run
    capture_output=True,          # Capture what the program prints
    text=True,                    # Return as text (not bytes)
    timeout=10                    # Stop after 10 seconds
)
```

This runs the user's code in a completely separate process, captures everything it prints, and returns it to our app.

## What Is an API Key?

An API key is like a password that lets your application use a service. Think of it like a library card — you need one to borrow books, but getting one is free and easy.

For Google Gemini:
1. You go to Google AI Studio (free)
2. You click "Create API Key"
3. You get a long string of characters (like `AIzaSyA123...`)
4. You put this in a `.env` file
5. Your app can now talk to Google's AI

Without the key, the app still works perfectly — it just uses the built-in mock AI instead.

## How to Run It Yourself

1. Install Python 3.8+
2. Run `pip install -r requirements.txt`
3. Run `python app.py` (starts the website)
4. Open http://localhost:5016 in your browser
5. Login with username: `admin`, password: `admin123`
6. Go to Editor and start coding!

## Optional: Live AI

To use real Google AI instead of mock AI:
1. Go to https://aistudio.google.com/apikey
2. Create an API key (free, takes 30 seconds)
3. Create a `.env` file with `GOOGLE_API_KEY=your_key`
4. Restart the app — the navbar will show "Live AI"

## Why Does This Matter?

- **Accessibility:** Not everyone can install development tools — this works in any browser
- **Education:** Students can start coding immediately without setup headaches
- **AI-Assisted Learning:** The AI explains code, which helps beginners understand what their code does
- **Portability:** Your code is available from any device with a browser
- **Safety:** Code runs in a sandboxed environment, so students can experiment without fear of breaking anything
- Professional IDEs like VS Code, Replit, and GitHub Codespaces all use similar web-based approaches
