# Project Explanation: Prompt-Driven AI Web Automation

## What Does This Project Do?

This project lets users automate web browser tasks using **natural language**. Instead of writing code to scrape websites or fill forms, you simply describe what you want in plain English, and an AI agent does it for you.

**Two modules:**
1. **Web Data Extraction** — Tell the AI "Get all product prices from this page" → it navigates the site, collects data, exports to Excel
2. **AI Form Filler** — Upload your resume PDF → point to any web form → the AI reads your data and fills every field automatically

Both modules share a **Flask + SocketIO** web UI with a Chrome-style light theme, showing live browser screenshots and color-coded action logs in real time.

---

## How Does the AI Agent Work?

### The Core Loop: Observe → Think → Act

The agent operates in a cycle of 3 steps, repeated up to 25 times:

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

**Step 1 — OBSERVE:** We extract the current state of the web page:
- Page URL and title
- All interactive elements (buttons, links, inputs, dropdowns) with sequential IDs like [0], [1], [2]
- Visible text content (truncated to ~2000 characters)

**Step 2 — THINK:** We send this state to Claude (Anthropic's AI) along with the user's task. Claude analyzes the page and decides which action to take, returning a **tool_use** response.

**Step 3 — ACT:** We execute Claude's chosen action using Playwright (a browser automation library). After execution, we take a screenshot and send it to the frontend via SocketIO.

**Step 4 — EMIT:** The screenshot (base64-encoded JPEG) and a log entry are emitted to the specific browser tab via SocketIO rooms.

The cycle repeats until Claude calls the `done` tool or the maximum step limit (25) is reached.

### Why DOM-Based Instead of Screenshots?

We send the page's **text content** to Claude, not screenshots. This approach is:
- **3x cheaper** — text tokens cost much less than image tokens
- **3x faster** — smaller payloads, faster API responses
- **More accurate** — ~89% success rate vs ~64% for screenshot-based methods
- **More reliable** — element IDs give precise targeting (no coordinate guessing)

---

## How Does Claude Tool Use Work?

Claude's **Tool Use** feature lets the AI call predefined functions instead of just generating text. We define 7 tools:

| Tool | What It Does | Example |
|---|---|---|
| `click` | Click a button or link | `click(element_id=3, reason="Click the Next page button")` |
| `fill` | Type text into an input field | `fill(element_id=5, value="john@email.com")` |
| `select_option` | Choose from a dropdown | `select_option(element_id=7, value="frontend")` |
| `navigate` | Go to a URL | `navigate(url="https://example.com")` |
| `scroll` | Scroll the page | `scroll(direction="down")` |
| `extract_data` | Collect structured data | `extract_data(data=[{title: "Book1", price: "$10"}])` |
| `done` | Signal task completion | `done(summary="Extracted 20 items", success=true)` |

### The API Call Flow:

```python
# 1. We send the page state + tools to Claude
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    system="You are a web scraping agent...",
    messages=[{"role": "user", "content": page_state_text}],
    tools=tool_definitions,  # Our 7 tools
)

# 2. Claude responds with a tool_use block
# Example response:
# {
#   "type": "tool_use",
#   "name": "click",
#   "input": {"element_id": 5, "reason": "Click the search button"}
# }

# 3. We execute the action, then send the result back
# This creates a multi-turn conversation:
# User → "Here's the page state" → Claude → "click element 5"
# User → "Clicked! Here's the new state" → Claude → "fill element 3"
# ...and so on
```

### Tool Use vs Regular Chat

In regular chat, Claude returns plain text. With Tool Use:
- We define **tool schemas** (name, description, input parameters with types)
- Claude returns a `tool_use` content block instead of text
- We **execute** the tool and send back a `tool_result` message
- This continues as a multi-turn conversation until Claude calls `done`

### Forced Tool Choice (Resume Parsing)

For resume parsing, we use `tool_choice={"type": "tool", "name": "save_resume_data"}` which **forces** Claude to use that specific tool. This guarantees structured JSON output matching our schema, every time.

---

## How Does the Browser Engine Work?

### Playwright + Asyncio Bridge

**Problem:** Playwright is async (uses `asyncio`), but Flask is synchronous.

**Solution:** `BrowserManager` runs an `asyncio` event loop on a separate daemon thread. A `run_async()` method bridges sync Flask code to async Playwright:

```python
class BrowserManager:
    def start(self):
        # Create asyncio loop on a background thread
        self._loop = asyncio.new_event_loop()
        self._thread = Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        # Launch headless Chromium browser
        self.run_async(self._launch_browser())

    def run_async(self, coro):
        # Bridge: sync code calls this, it runs the coroutine on the async loop
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result(timeout=60)
```

This pattern allows synchronous Flask route handlers and SocketIO background tasks to call async Playwright methods seamlessly.

### DOM Extraction (`page_state.py`)

We use Playwright's `page.evaluate()` to run JavaScript in the browser that:
1. Queries all interactive elements using CSS selectors: `a, button, input, select, textarea, [role="button"]`
2. Filters out hidden/invisible elements (checks `offsetParent` and bounding rect)
3. Assigns sequential IDs: [0], [1], [2], ...
4. Extracts metadata per element: tag, type, name, placeholder, text, href, value, options, aria-label

The formatted output sent to Claude looks like:
```
Page: Books to Scrape - Sandbox
URL: https://books.toscrape.com/

Interactive Elements:
[0] link "Home" -> /index.html
[1] link "Books" -> /catalogue/category/books_1/index.html
[2] link "A Light in the Attic" -> /catalogue/a-light-in-the-attic_1000/index.html
[3] link "next" -> /catalogue/page-2.html

Visible Text (truncated):
Books to Scrape  We love being scraped!  Home  Books  ...
```

### Action Execution (`actions.py`)

When Claude decides on an action, the executor:
1. Resolves the element by its sequential ID (re-queries the DOM to find the nth visible interactive element)
2. Performs the action using Playwright methods (`click()`, `fill()`, `select_option()`)
3. Returns a success/failure result with a descriptive message
4. Handles errors like stale elements, timeouts, or element-not-found

---

## How Does PDF Resume Parsing Work?

Two-stage pipeline:

```
PDF File ──► pymupdf4llm ──► Markdown Text ──► Claude API ──► Structured JSON
              (Stage 1)                          (Stage 2)
```

### Stage 1: PDF → Markdown
We use `pymupdf4llm` to convert the PDF to clean markdown text. This handles:
- Multi-column layouts
- Headers and sections
- Tables
- Bold/italic formatting
- Preserves document structure

### Stage 2: Markdown → Structured Data
We send the markdown to Claude with **forced tool choice**:
```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    system="You are a resume parser...",
    messages=[{"role": "user", "content": resume_markdown}],
    tools=[resume_parse_tool],
    tool_choice={"type": "tool", "name": "save_resume_data"},  # Force this tool
)
```

This guarantees Claude returns a structured dictionary with fields:
- `full_name`, `email`, `phone`, `address`
- `summary` — professional summary/objective
- `education[]` — array of {degree, institution, year}
- `experience[]` — array of {title, company, duration, description}
- `skills[]` — array of skill strings

The parsed data is shown to the user in an editable preview before form filling begins.

---

## How Does Real-Time Streaming Work?

### Flask-SocketIO

SocketIO provides real-time bidirectional communication between the server and browser:

```
Browser (JavaScript)                    Server (Python)
─────────────────────                   ────────────────
const socket = io()         ◄──────►    socketio = SocketIO()
socket.emit('join', room)              @socketio.on('join') → join_room()
socket.on('screenshot')    ◄──────     socketio.emit('screenshot', data, room=room)
socket.on('agent_log')     ◄──────     socketio.emit('agent_log', data, room=room)
socket.on('agent_complete') ◄─────     socketio.emit('agent_complete', data, room=room)
```

### Room Isolation

Each browser tab generates a unique session ID (room) using:
```javascript
this.room = 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
```

The server uses `join_room()` and emits only to that specific room, so multiple users can run agents simultaneously without interference.

### Screenshot Streaming

After every action, the agent:
1. Takes a JPEG screenshot (quality=50 for small file size)
2. Base64-encodes the image bytes
3. Emits via SocketIO to the frontend: `socketio.emit('screenshot', {'image': base64_str}, room=room)`
4. The JavaScript client updates an `<img>` tag's `src` attribute: `img.src = 'data:image/jpeg;base64,' + data`

### Action Log

The `AgentUI` JavaScript class handles three event types:
- `screenshot` — updates the live browser view image
- `agent_log` — appends a color-coded entry to the log panel
- `agent_complete` — shows the final result and enables download/reset

Log colors (Chrome-style light theme):
- **Gray** — info messages (step count, navigation status)
- **Blue** — action messages (click, fill, select operations)
- **Purple** — thinking messages (Claude's reasoning)
- **Green** — success messages (data extracted, task completed)
- **Red** — error messages (action failures, API errors)

---

## How Does the Scraper Export to Excel?

We use **pandas** to convert the collected data (list of dicts) to a DataFrame, then save with **openpyxl**:

```python
import pandas as pd

# data = [{"title": "Book1", "price": "$10"}, {"title": "Book2", "price": "$15"}, ...]
df = pd.DataFrame(data)
df.to_excel("scraped_data_20260306_143000.xlsx", index=False, engine="openpyxl")
```

The file is saved to the `exports/` directory with a timestamp in the filename. The download link appears automatically in the UI when the agent finishes. CSV export is also supported.

---

## How Does the Form Filler Agent Work?

The `FormFillerAgent` extends `BaseAgent` with:

1. **Resume data injection:** The parsed resume data is formatted as JSON and injected into the system prompt, so Claude knows all the candidate's information.

2. **Field matching:** Claude reads the form's interactive elements (input names, placeholders, labels) and matches them to the resume data. For example:
   - `name="email"` → uses `resume_data.email`
   - `name="skills"` → joins `resume_data.skills` into a comma-separated string
   - A dropdown with education options → selects the closest match to `resume_data.education[0].degree`

3. **Reduced tool set:** The form filler uses 6 tools (excludes `extract_data` which is only needed for scraping).

4. **Submit handling:** After filling all fields, the agent looks for a Submit button and clicks it.

---

## What's the Message Trimming Strategy?

After many steps, the conversation grows large (each step adds ~3 messages: assistant tool_use, user tool_result, user page state). To prevent context overflow while maintaining conversation integrity:

```python
def _trim_messages(self):
    if len(self.messages) <= 12:
        return  # No trimming needed

    # Keep first message (task description + initial page state)
    # Keep last ~9 messages (recent context)
    # CRITICAL: Only cut at plain user messages (page state),
    # never between tool_use and tool_result pairs

    rest = self.messages[1:]
    target_keep = min(9, len(rest))
    cut = len(rest) - target_keep

    # Scan forward to find a safe cut point (plain user message)
    while cut < len(rest):
        msg = rest[cut]
        if msg.get("role") == "user" and isinstance(msg.get("content"), str):
            break  # Safe to cut here
        cut += 1

    self.messages = self.messages[:1] + rest[cut:]
```

**Key rules:**
- Always keep the **first message** (original task + initial page state) so Claude remembers what it's doing
- Keep the **last ~9 messages** for recent context
- **Never break** a `tool_use`/`tool_result` pair — the Claude API requires every `tool_use` block to have a corresponding `tool_result` immediately after
- Only cut at **plain user messages** (page state updates), which are safe boundaries between action groups

---

## Error Handling Strategy

### Agent-Level Errors
- **Max 3 consecutive errors:** If 3 actions fail in a row, the agent stops with an error summary
- **Max 25 steps:** Prevents infinite loops; the agent reports "Reached max steps"
- **Stop button:** Sets a `_stopped` flag checked at the start of each step

### API-Level Errors
- **Rate limiting:** Exponential backoff — wait 2s, then 4s, then 8s before retrying
- **Authentication errors:** Immediately reported to the user (invalid key, no credits)
- **Overloaded API:** Retried with backoff, same as rate limits

### Browser-Level Errors
- **Navigation timeout:** 30-second timeout on page loads
- **Stale elements:** After each action, the entire page state is re-extracted with fresh element IDs
- **Element not found:** Returns a descriptive error message with the valid element range

### User-Facing Errors
- **Missing API key:** Warning badge on dashboard + flash messages on module pages
- **Invalid URL:** Client-side validation + server-side error handling
- **Empty fields:** JavaScript alerts prevent form submission
- **PDF parsing failure:** Descriptive error message (e.g., "image-only PDF")

---

## Design Patterns Used

1. **Observe-Think-Act Loop** — The core agent cycle, inspired by reinforcement learning agent architectures
2. **Template Method Pattern** — `BaseAgent` defines the loop skeleton; `ScraperAgent` and `FormFillerAgent` override `get_system_prompt()`, `get_tools()`, and `handle_extract_data()`
3. **Factory Pattern** — Flask's `create_app()` app factory for clean initialization
4. **Blueprint Pattern** — Flask Blueprints for modular route organization (`auth`, `main`, `scraper`, `form_filler`)
5. **Decorator Pattern** — `@login_required` wraps route handlers to enforce authentication before execution
6. **Bridge Pattern** — `BrowserManager.run_async()` bridges synchronous Flask to asynchronous Playwright
7. **Room-based Pub/Sub** — SocketIO rooms for isolated real-time event delivery

---

## How Does Authentication Work?

### Flask-Login Integration (`core/auth.py`)
The application uses **Flask-Login** for session-based authentication. All routes (except the login page and demo form) require the user to be logged in.

**Components:**
- **User model** — A simple `User` class implementing Flask-Login's `UserMixin` (provides `is_authenticated`, `get_id()`, etc.)
- **SQLite database** — Users stored in `auth.db` with hashed passwords (separate from `history.db`)
- **Password hashing** — Uses Werkzeug's `generate_password_hash()` / `check_password_hash()` with pbkdf2:sha256
- **Default admin** — On first startup, `seed_default_user()` creates an `admin` / `admin123` account if no users exist

### Authentication Flow
```
Browser → GET /scraper → @login_required → Not authenticated?
    → 302 Redirect to /auth/login?next=/scraper
    → User submits username + password
    → POST /auth/login → verify_password() → login_user()
    → 302 Redirect to /scraper (original destination)
```

### Session Management
- Flask-Login stores the user ID in a signed session cookie (using `SECRET_KEY`)
- `remember=True` keeps the session alive across browser restarts
- `@login_manager.user_loader` callback loads the user from SQLite on each request
- Logout clears the session and redirects to the login page

### Route Protection
Every route uses the `@login_required` decorator from Flask-Login:
```python
@scraper_bp.route("/start", methods=["POST"])
@login_required  # Redirects to login if not authenticated
def start_scraping():
    ...
```

The only unprotected routes are:
- `/auth/login` — The login page itself
- `/form-filler/demo-form` — The built-in demo form (needs to be accessible by the agent's browser)

---

## How Does Security Work?

The application implements multiple security layers:

### URL Validation (`core/security.py`)
Before any agent navigates to a URL, the `validate_url()` function checks:
- **Scheme whitelisting:** Only `http://` and `https://` are allowed. `file://`, `ftp://`, `data://`, `javascript:` are blocked.
- **Internal IP blocking:** Private/internal IPs are blocked to prevent SSRF attacks: `127.0.0.1`, `10.*`, `192.168.*`, `172.16-31.*`, cloud metadata IPs (`169.254.169.254`).
- **Localhost control:** Blocked for scraper (no reason to scrape localhost), allowed for form filler (to use the demo form).

### API Key Masking
The `mask_sensitive()` function uses a regex to find API key patterns (`sk-ant-*`) in any text and replaces them with `sk-ant-***MASKED***`. This is applied in `BaseAgent.emit_log()` so keys never appear in browser logs or the terminal.

### File Upload Security
- Only `.pdf` files are accepted (extension check)
- Maximum 10MB file size enforced before saving to disk
- Uploaded files are deleted immediately after parsing

### Download Path Traversal Protection
The download route uses `secure_filename()` from Werkzeug and verifies the resolved filepath stays inside the `exports/` directory using `os.path.realpath()`. Prevents `../../etc/passwd` style attacks.

### Rate Limiting
A simple in-memory `RateLimiter` class limits each IP to 5 agent starts per minute. Returns a `429 Too Many Requests` response with a `retry_after` value.

```python
class RateLimiter:
    def __init__(self, max_requests=5, window_seconds=60):
        self._requests = defaultdict(list)  # IP -> [timestamps]

    def is_allowed(self, ip):
        # Clean old entries, check count, add new timestamp
        # Returns (allowed: bool, retry_after: int or None)
```

---

## How Does Task History Work?

### SQLite Storage (`core/history.py`)
All agent runs are automatically saved to a local SQLite database (`history.db`). Each record contains:

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Auto-incrementing primary key |
| `timestamp` | TEXT | ISO format datetime |
| `module` | TEXT | "scraper" or "form_filler" |
| `url` | TEXT | Target URL |
| `task_description` | TEXT | User's prompt |
| `status` | TEXT | "success", "failed", or "stopped" |
| `summary` | TEXT | Agent's completion summary |
| `steps` | INTEGER | Number of steps taken |
| `items_collected` | INTEGER | Items extracted (scraper only) |
| `download_filename` | TEXT | Excel file (nullable) |
| `duration_seconds` | REAL | Run duration |

### How Runs Are Saved
In the background task functions (`_run_scraper_agent`, `_run_form_filler_agent`), we:
1. Record `start_time = time.time()` before the agent starts
2. After the agent completes, compute `duration = time.time() - start_time`
3. Determine status: "success" if `result["success"]`, "stopped" if `agent._stopped`, otherwise "failed"
4. Call `save_run(...)` with all the metadata

### UI Integration
- **Dashboard:** Shows last 5 runs in a "Recent Activity" table
- **History page** (`/history`): Full table with all runs, clickable rows to see summary, clear button
- **API:** `GET /api/history` returns JSON, `POST /api/history/clear` deletes all records

---

## Viva Questions & Answers

### General Architecture

**Q1: What is the purpose of this project?**
A: To automate web browser tasks using natural language prompts. Users describe what they want (scrape data, fill a form), and an AI agent does it by controlling a real browser via Playwright.

**Q2: Why use DOM-based extraction instead of screenshots?**
A: DOM/text-based is 3x cheaper (fewer tokens), 3x faster (smaller payloads), and more accurate (~89% vs ~64% success rate). Element IDs also provide precise targeting instead of guessing pixel coordinates.

**Q3: How does the agent decide what action to take?**
A: The agent sends the current page state (interactive elements + visible text) to Claude with tool definitions. Claude analyzes the state relative to the task and returns a tool_use response indicating which action to perform and with what parameters.

**Q4: What happens if the agent makes a mistake?**
A: The agent has multi-level error handling: after 3 consecutive errors it stops, the page state is re-extracted after every action (fixing stale elements), and rate limit errors trigger exponential backoff (2s, 4s, 8s).

**Q5: How many steps can the agent take?**
A: Maximum 25 steps by default (configurable via `MAX_AGENT_STEPS` in `.env`). Each step is one complete observe→think→act cycle.

### Claude API & Tool Use

**Q6: What is Claude Tool Use?**
A: It's a feature where Claude can call predefined functions instead of just generating text. We define 7 tools (click, fill, navigate, etc.) with JSON schemas, and Claude decides which one to use based on the current page state and task.

**Q7: How does forced tool choice work in resume parsing?**
A: We set `tool_choice={"type": "tool", "name": "save_resume_data"}` which forces Claude to use that specific tool, guaranteeing structured output matching our schema every time. Without this, Claude might return plain text instead.

**Q8: How is conversation continuity maintained?**
A: Each Claude response (with tool_use) is added to the messages list as an `assistant` message, followed by a `user` message containing the `tool_result`. This creates a multi-turn conversation where Claude has context of all previous actions.

**Q9: What model do you use?**
A: Claude Sonnet (`claude-sonnet-4-20250514`) by default. It provides a good balance of capability, speed, and cost for browser automation tasks.

**Q10: How do you handle rate limits?**
A: Exponential backoff: wait 2 seconds, then 4, then 8. If all retries fail, the error propagates up and the agent stops with a descriptive error message shown to the user.

### Browser Automation

**Q11: Why Playwright instead of Selenium?**
A: Playwright is faster, has native async support, auto-waits for elements, provides better cross-browser consistency, and has a smaller, more modern API surface. It also has built-in support for headless mode and screenshots.

**Q12: How do you bridge Flask (sync) with Playwright (async)?**
A: `BrowserManager` creates a dedicated `asyncio` event loop running on a daemon thread. The `run_async()` method uses `asyncio.run_coroutine_threadsafe()` to schedule async Playwright coroutines from synchronous Flask code, then waits for the result with a 60-second timeout.

**Q13: How do you identify elements on the page?**
A: We run JavaScript via `page.evaluate()` that queries all interactive elements using CSS selectors, filters out hidden/invisible ones (checking `offsetParent` and bounding rectangles), assigns sequential IDs [0], [1], [2]..., and extracts metadata (tag, type, name, placeholder, text, options, value, aria-label).

**Q14: How do you handle dynamic pages (JavaScript-rendered content)?**
A: Playwright runs a real Chromium browser that fully executes JavaScript. We use `wait_until="domcontentloaded"` for navigation and add configurable delays (`STEP_DELAY`) between actions to let dynamic content render before re-extracting the page state.

**Q15: What is the viewport size?**
A: 1280x800 pixels, matching a standard laptop screen. This ensures most websites render their desktop layout normally, and screenshots are a reasonable size for streaming.

### Real-Time Features

**Q16: How do screenshots stream to the browser?**
A: After each action, the agent takes a JPEG screenshot (quality=50 for small size), base64-encodes it, and emits it via SocketIO to the client's room. The JavaScript `AgentUI` class updates an `<img>` tag's `src` attribute with the base64 data URI.

**Q17: How do you prevent cross-session interference?**
A: Each browser tab generates a unique room ID (combining random string + timestamp). The server uses `join_room()` to add the client to its room, and all `emit()` calls specify `room=room`. Multiple users see only their own agent's output.

**Q18: Why SocketIO instead of plain WebSockets?**
A: SocketIO adds essential features: automatic reconnection, room management for session isolation, fallback transports (long-polling if WebSocket fails), event-based messaging with named events, and built-in Flask integration via Flask-SocketIO.

**Q19: What are the log levels and their colors?**
A: In the Chrome-style light theme: info (gray `#5f6368`), action (blue `#1a73e8`), thinking (purple `#9334e6`), success (green `#1e8e3e`), error (red `#d93025`).

### PDF Parsing

**Q20: How is a PDF resume parsed?**
A: Two stages: (1) `pymupdf4llm` converts the PDF to clean markdown text, preserving structure and formatting, (2) The markdown is sent to Claude with forced tool choice (`save_resume_data`), which extracts structured fields into a JSON dictionary.

**Q21: What if the PDF is image-only (scanned)?**
A: `pymupdf4llm` can handle some scanned PDFs with embedded text layers, but pure image-only PDFs will produce empty or minimal text. The system checks if extracted text is less than 20 characters and returns an error telling the user the file may be image-only or corrupted.

**Q22: What fields are extracted from a resume?**
A: `full_name`, `email`, `phone`, `address`, `summary`, `education[]` (each with degree/institution/year), `experience[]` (each with title/company/duration/description), and `skills[]` (array of strings). Only `full_name` and `email` are required.

### Data Export

**Q23: How is scraped data exported?**
A: Collected data (list of dicts) is converted to a pandas DataFrame, then saved as Excel (`.xlsx`) using the openpyxl engine. The file is saved to the `exports/` directory with a timestamp in the filename (e.g., `scraped_data_20260306_143000.xlsx`). CSV export is also supported.

**Q24: Can the user edit extracted data before using it?**
A: Yes, in the form filler module, parsed resume data is shown in a preview panel. An "Edit Data" button reveals a JSON text editor where the user can modify any field, then click "Save Changes" to apply.

### Error Handling & Safety

**Q25: What if the target URL is invalid?**
A: The browser navigation times out after 30 seconds (`NAVIGATION_TIMEOUT = 30000`ms), and the agent reports the error through SocketIO as an error-level log, then stops gracefully.

**Q26: What prevents infinite loops?**
A: Three safeguards: (1) Maximum 25 steps limit, (2) Maximum 3 consecutive errors triggers auto-stop, (3) A Stop button in the UI sets a `_stopped` flag checked at the start of each iteration.

**Q27: What if Claude's API key is missing?**
A: The dashboard shows a yellow warning badge instead of the green "API Key Configured" badge. Starting any agent returns a 400 HTTP error with the message "ANTHROPIC_API_KEY not configured." Flash messages also appear on module pages.

**Q28: How do you handle stale elements?**
A: After each action, the entire page state is re-extracted from the DOM. Element IDs are reassigned fresh each time based on currently visible elements, so stale references from previous steps are automatically replaced with current ones.

**Q29: What design pattern does the agent use?**
A: The **Observe-Think-Act** loop (from reinforcement learning), implemented using the **Template Method** pattern. `BaseAgent` defines the loop skeleton and common behavior; subclasses `ScraperAgent` and `FormFillerAgent` override `get_system_prompt()`, `get_tools()`, and `handle_extract_data()`.

**Q30: How does message trimming prevent context overflow?**
A: After the conversation exceeds 12 messages, we keep the first message (original task + initial state) and the last ~9 messages (recent context), dropping intermediate steps. Critically, we only cut at **plain user messages** (page state updates), never between `tool_use`/`tool_result` pairs, which would cause an API error.

### Security

**Q31: How do you prevent SSRF (Server-Side Request Forgery)?**
A: The `validate_url()` function blocks dangerous URL schemes (`file://`, `ftp://`), internal/private IP addresses (`127.0.0.1`, `10.*`, `192.168.*`, `172.16-31.*`), and cloud metadata endpoints (`169.254.169.254`). Only `http://` and `https://` URLs to external hosts are allowed.

**Q32: How are API keys protected from leaking in logs?**
A: The `mask_sensitive()` function uses a regex pattern (`sk-ant-[a-zA-Z0-9_\-]{10,}`) to detect API keys in any log message and replaces them with `sk-ant-***MASKED***`. This is applied in `BaseAgent.emit_log()` before printing to terminal or emitting via SocketIO.

**Q33: How do you prevent path traversal attacks on file downloads?**
A: Two checks: (1) `secure_filename()` from Werkzeug strips directory separators and special characters, (2) `os.path.realpath()` resolves the full path and verifies it starts with the `EXPORT_DIR` prefix. This prevents `../../etc/passwd` style attacks.

**Q34: How does rate limiting work?**
A: An in-memory `RateLimiter` class tracks request timestamps per IP using a `defaultdict(list)`. Each request cleans entries older than the 60-second window, then checks if the count exceeds 5. If exceeded, it returns the number of seconds until the oldest entry expires.

**Q35: What file upload security measures are in place?**
A: Three checks: (1) Only `.pdf` extension is accepted, (2) File size is checked before saving (max 10MB), (3) Uploaded files are deleted immediately after parsing, never left on disk.

### Task History

**Q36: How is task history stored?**
A: In a local SQLite database (`history.db`) with a `task_runs` table. Each completed agent run is saved with metadata: timestamp, module, URL, task description, status, summary, steps, items collected, download filename, and duration.

**Q37: When is a history record created?**
A: After every agent run completes — whether it succeeds, fails, or is stopped. The background task functions (`_run_scraper_agent`, `_run_form_filler_agent`) call `save_run()` with the result data and computed duration.

**Q38: How is the history displayed in the UI?**
A: The dashboard shows the last 5 runs in a "Recent Activity" table. A dedicated `/history` page shows all runs in a full table with color-coded status badges (green=success, red=failed, gray=stopped). Clicking a row shows the full summary.

**Q39: Can history be exported or cleared?**
A: History can be cleared via the "Clear All" button on the history page (calls `POST /api/history/clear`). The `GET /api/history` endpoint returns all runs as JSON, which can be used for programmatic access.

**Q40: Why SQLite instead of a full database?**
A: SQLite is serverless, requires no setup, and stores everything in a single file. For a local development tool like this, it's the simplest choice. The database is automatically created on first import of `core/history.py`.

### Authentication

**Q41: How does user authentication work?**
A: Flask-Login provides session-based authentication. On login, the user ID is stored in a signed cookie. On each request, `@login_required` checks the session — if missing or invalid, it redirects to `/auth/login`. The `user_loader` callback loads the user from SQLite by ID.

**Q42: How are passwords stored securely?**
A: Passwords are never stored in plaintext. We use Werkzeug's `generate_password_hash()` which produces a pbkdf2:sha256 hash with a random salt. During login, `check_password_hash()` compares the submitted password against the stored hash.

**Q43: Why use a separate `auth.db` instead of adding users to `history.db`?**
A: Separation of concerns — authentication data and task history serve different purposes. If history is cleared, user accounts should not be affected. It also allows different backup/migration strategies for each database.

**Q44: How does the `@login_required` decorator work?**
A: Flask-Login's `@login_required` checks `current_user.is_authenticated` before each request. If `False`, it redirects to `login_manager.login_view` (configured as `auth.login_page`) with a `next` parameter so the user returns to their original destination after login.

**Q45: Why is the demo form route not protected?**
A: The demo form (`/form-filler/demo-form`) is accessed by the Playwright browser during agent automation, not by the user's browser. Since the headless browser doesn't share the user's session cookies, protecting this route would block the agent from accessing the form it needs to fill.
