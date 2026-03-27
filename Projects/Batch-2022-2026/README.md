# RAG Knowledge Assistant

A multi-product knowledge assistant powered by Retrieval-Augmented Generation (RAG). Upload documents or scrape websites per product, then ask questions — the system retrieves relevant context and generates accurate answers using Claude AI.

---

## What is This Product?

Imagine you work at a company that sells multiple products — say, a **CRM tool**, a **billing platform**, and a **mobile app**. Each product has its own user manuals, FAQs, help articles, and website pages. When a customer or a support agent has a question like *"How do I reset my password in the billing platform?"*, someone has to dig through piles of documentation to find the answer.

**RAG Knowledge Assistant** does that work for you — instantly.

You feed it your product documentation (PDFs, Word files, text files, or even entire websites), and it reads, understands, and remembers all of it. Then, anyone on your team can simply **ask a question in plain English**, and the system finds the most relevant information from your documents and gives a clear, accurate answer — with references to where it found the information.

### How Does It Work? (In Simple Terms)

Think of it like a **super-smart search + answer engine** for your company's documents:

1. **You upload your documents** — Drop in your user guides, policy documents, FAQs, or paste a website URL. The system reads them and breaks them into small, searchable pieces.

2. **Someone asks a question** — A support agent types: *"What's the refund policy for the Enterprise plan?"*

3. **The system finds the right information** — It searches through all the document pieces to find the most relevant ones (like searching a library, but in milliseconds).

4. **AI writes a clear answer** — Using the found information, the AI (Claude by Anthropic) writes a natural, easy-to-read answer. It only uses facts from your documents — it never makes things up.

5. **Sources are shown** — The answer includes which documents the information came from, so you can verify it.

### What Makes It Special?

- **No hallucination** — Unlike general AI chatbots that might guess or make up answers, this system only answers from your actual documents. If the answer isn't in the docs, it says so.
- **Multi-product support** — Keep documentation for different products separate. A question about Product A won't pull answers from Product B's docs.
- **Always up to date** — Upload new documents or scrape updated websites anytime. The system learns the new content immediately.
- **Access control** — Admins manage everything. Regular users can only ask questions about products they're assigned to.

---

## Real-World Use Cases

### 1. Customer Support Team

**Scenario:** A software company has 5 products, each with 50+ pages of documentation.

**Problem:** Support agents spend 10-15 minutes per ticket searching through manuals, wikis, and old emails to find the right answer.

**Solution with RAG Knowledge Assistant:**
- Admin uploads all product manuals and scrapes the help center website
- Support agents log in, select the product the customer is asking about, and type the question
- They get an instant, accurate answer with the exact source document
- **Result:** Ticket resolution time drops from 15 minutes to 2 minutes

### 2. Employee Onboarding & Training

**Scenario:** A company has HR policies, IT setup guides, and compliance documents spread across multiple PDFs and internal wikis.

**Problem:** New employees ask the same questions repeatedly. HR and IT teams spend hours answering *"How do I set up VPN?"*, *"What's the leave policy?"*, *"How do I request a laptop?"*

**Solution with RAG Knowledge Assistant:**
- Admin uploads all HR policies, IT guides, and compliance docs
- New hires simply ask their questions and get instant answers
- **Result:** HR and IT teams save hours per week; new hires get self-service answers on day one

### 3. Legal & Compliance

**Scenario:** A law firm or compliance department has hundreds of contracts, regulations, and policy documents.

**Problem:** Finding a specific clause or regulation across hundreds of documents takes significant time.

**Solution with RAG Knowledge Assistant:**
- Upload all contracts and regulatory documents
- Ask questions like *"What are the termination clauses in the vendor agreement with Acme Corp?"*
- **Result:** Research that took hours now takes seconds, with exact source references

### 4. Product Knowledge Base for Sales Teams

**Scenario:** A company sells complex B2B products with detailed technical specifications.

**Problem:** Sales reps can't remember every feature, pricing detail, and competitive advantage across all products.

**Solution with RAG Knowledge Assistant:**
- Upload product spec sheets, pricing guides, competitive analysis docs, and case studies
- Sales reps ask *"What are the key differences between our Enterprise and Pro plans?"* or *"How does our API rate limiting compare to competitors?"*
- **Result:** Sales reps have instant access to accurate product knowledge during calls

### 5. Educational Institutions

**Scenario:** A university has course materials, research papers, and administrative policies.

**Problem:** Students and staff struggle to find specific information across multiple departments.

**Solution with RAG Knowledge Assistant:**
- Create products per department (Admissions, Academics, Finance, etc.)
- Upload syllabi, handbooks, fee structures, and policy documents
- Students ask questions like *"What are the prerequisites for Advanced Machine Learning?"*
- **Result:** Reduced load on administrative staff; students get instant answers 24/7

### 6. Healthcare Documentation

**Scenario:** A hospital or clinic has treatment protocols, drug interaction guides, and patient care procedures.

**Problem:** Medical staff need quick access to protocols during patient care.

**Solution with RAG Knowledge Assistant:**
- Upload clinical guidelines, drug databases, and standard operating procedures
- Medical staff ask *"What is the recommended dosage of Drug X for pediatric patients?"*
- **Result:** Faster, evidence-based clinical decisions with source references for accountability

---

## Who Uses This System?

| Role | What They Do |
|------|-------------|
| **Admin** | Sets up the system, creates products, uploads documents, scrapes websites, manages users |
| **Regular User** | Logs in, selects a product, and asks questions to get instant answers from the knowledge base |

---

## Features

- **Multi-product knowledge base** — Organize documents by product with isolated vector indexes
- **Document ingestion** — Upload PDF, DOCX, or TXT files; automatically parsed, chunked, and embedded
- **Web scraping** — Crawl websites with preview, follow same-domain links, ingest into knowledge base
- **RAG-powered Q&A** — Vector search + Claude LLM with hallucination prevention (answers only from provided context)
- **Role-based access control** — Admin and user roles with JWT authentication
- **Product-level permissions** — Assign specific products to users; unassigned users see all products
- **Local embeddings** — Uses `sentence-transformers` (all-MiniLM-L6-v2) — no API key needed for embeddings
- **Web UI** — Single-page application with chat interface, admin dashboard, and settings

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI (Python) |
| Database | SQLite |
| Vector Store | FAISS (faiss-cpu) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2, 384-dim) |
| LLM | Anthropic Claude (claude-sonnet-4-20250514) |
| Auth | JWT (python-jose) + bcrypt |
| Frontend | Vanilla HTML/CSS/JS (single-page app) |

## Architecture

```
User Query → Embed Query (local) → FAISS Vector Search → Top-K Chunks → Claude LLM → Answer

Document Upload → Parse (PDF/DOCX/TXT) → Chunk (1000 chars, 200 overlap)
               → Embed (local) → Store in FAISS + SQLite
```

## Installation

### Prerequisites

- Python 3.10+
- pip

### Setup

```bash
# Clone or navigate to project directory
cd rag-knowledge-assistant

# Create virtual environment
python3 -m venv venv
source venv/bin/activate    # macOS/Linux
# venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### First Run

```bash
python3 run.py
```

The application starts at **http://localhost:8000**

On first run, the system automatically:
- Creates the SQLite database (`data/app.db`)
- Creates required tables
- Creates a default admin user: **username:** `admin`, **password:** `admin123`

### Configure API Key

1. Log in as admin at http://localhost:8000
2. Click the gear icon (Settings) in the sidebar
3. Enter your Anthropic API key and save

Without an API key, document upload and embedding work fine, but Q&A queries will fail.

## Usage Guide

### Admin Operations

**Create a Product:**
1. Navigate to **Products** in the sidebar
2. Click **Create** tab
3. Enter Product ID (unique identifier), Name, and Description
4. Submit — the product appears in the list

**Upload Documents:**
1. Navigate to **Documents** in the sidebar
2. Select a product from the dropdown
3. Upload a PDF, DOCX, or TXT file
4. The system parses, chunks, and embeds the document automatically

**Scrape a Website:**
1. Navigate to **Web Scraper** in the sidebar
2. Select a product, enter a URL, set max pages (up to 50)
3. Click **Preview** to see the website content before ingesting
4. Click **Scrape & Ingest** to process

**Manage Users:**
1. Navigate to **Users** in the sidebar
2. Create users with `admin` or `user` role
3. Click **Assign Products** to restrict a user to specific products

### User Operations

**Ask Questions:**
1. Log in and navigate to **Query**
2. Select a product from the dropdown
3. Type your question and press Enter
4. The assistant retrieves relevant document chunks and generates an answer with source references

## API Access Guide

All API endpoints (except login) require a JWT Bearer token. Obtain a token by logging in, then pass it in the `Authorization` header.

### Step 1: Get a Token

```bash
BASE=http://localhost:8000

# Login (admin or regular user)
curl -s $BASE/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "role": "admin",
  "username": "admin"
}
```

Save the token for subsequent requests:
```bash
TOKEN=$(curl -s $BASE/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
```

### Step 2: Use the Token

Pass the token in the `Authorization` header for all authenticated requests:

```bash
curl -s $BASE/api/products \
  -H "Authorization: Bearer $TOKEN"
```

### Access Levels

The system has two roles with different API access:

**Admin** — Full access to all endpoints:

| Action | Method | Endpoint | Example |
|--------|--------|----------|---------|
| Create user | POST | `/api/auth/users` | `curl -s $BASE/api/auth/users -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"username":"john","password":"pass123","role":"user"}'` |
| List users | GET | `/api/auth/users` | `curl -s $BASE/api/auth/users -H "Authorization: Bearer $TOKEN"` |
| Assign products | POST | `/api/auth/users/{id}/products` | `curl -s $BASE/api/auth/users/2/products -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '["PROD01","PROD02"]'` |
| Create product | POST | `/api/products` | `curl -s $BASE/api/products -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"product_id":"PROD01","name":"My Product","description":"desc"}'` |
| Upload document | POST | `/api/products/{id}/documents` | `curl -s $BASE/api/products/PROD01/documents -H "Authorization: Bearer $TOKEN" -F "file=@doc.pdf"` |
| Scrape website | POST | `/api/products/scrape` | `curl -s $BASE/api/products/scrape -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"product_id":"PROD01","url":"https://example.com","max_pages":10}'` |
| Preview URL | POST | `/api/products/preview-url` | `curl -s $BASE/api/products/preview-url -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"url":"https://example.com"}'` |
| Rebuild embeddings | POST | `/api/products/{id}/rebuild` | `curl -s -X POST $BASE/api/products/PROD01/rebuild -H "Authorization: Bearer $TOKEN"` |
| Update config | PUT | `/api/admin/config` | `curl -s -X PUT $BASE/api/admin/config -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"anthropic_api_key":"sk-ant-..."}'` |
| Get config | GET | `/api/admin/config` | `curl -s $BASE/api/admin/config -H "Authorization: Bearer $TOKEN"` |

**Regular User** — Read-only access + querying:

| Action | Method | Endpoint | Example |
|--------|--------|----------|---------|
| Get my info | GET | `/api/auth/me` | `curl -s $BASE/api/auth/me -H "Authorization: Bearer $TOKEN"` |
| List products | GET | `/api/products` | `curl -s $BASE/api/products -H "Authorization: Bearer $TOKEN"` |
| List documents | GET | `/api/products/{id}/documents` | `curl -s $BASE/api/products/PROD01/documents -H "Authorization: Bearer $TOKEN"` |
| List scraped sources | GET | `/api/products/{id}/scraped` | `curl -s $BASE/api/products/PROD01/scraped -H "Authorization: Bearer $TOKEN"` |
| Ask a question | POST | `/api/query` | `curl -s $BASE/api/query -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"productId":"PROD01","question":"How does feature X work?"}'` |

> **Note:** Regular users only see products assigned to them. If no products are assigned, they see all products.

### Common Workflows via API

**Complete setup (admin):**

```bash
BASE=http://localhost:8000

# 1. Login as admin
TOKEN=$(curl -s $BASE/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# 2. Set Anthropic API key
curl -s -X PUT $BASE/api/admin/config \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"anthropic_api_key":"sk-ant-api03-your-key-here"}'

# 3. Create a product
curl -s $BASE/api/products \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id":"acme-docs","name":"Acme Documentation","description":"Acme product docs"}'

# 4. Upload a document
curl -s $BASE/api/products/acme-docs/documents \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@user_guide.pdf"

# 5. Scrape additional content
curl -s $BASE/api/products/scrape \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id":"acme-docs","url":"https://docs.acme.com","max_pages":20}'

# 6. Create a regular user
curl -s $BASE/api/auth/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username":"support_agent","password":"secure123","role":"user"}'

# 7. Assign products to user (use the user ID from step 6 response)
curl -s $BASE/api/auth/users/2/products \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '["acme-docs"]'
```

**Query as a regular user:**

```bash
# Login as regular user
USER_TOKEN=$(curl -s $BASE/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"support_agent","password":"secure123"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# Ask a question
curl -s $BASE/api/query \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"productId":"acme-docs","question":"What is the return policy?"}'
```

Response:
```json
{
  "answer": "Based on the documentation, the return policy allows...",
  "sources": ["user_guide.pdf", "https://docs.acme.com/returns"]
}
```

### Error Responses

| Status | Meaning | Example |
|--------|---------|---------|
| 401 | Not authenticated (missing/invalid token) | `{"detail": "Not authenticated"}` |
| 401 | Invalid login credentials | `{"detail": "Invalid credentials"}` |
| 403 | Admin access required | `{"detail": "Admin access required"}` |
| 400 | Validation error | `{"detail": "Username already exists"}` |
| 404 | Resource not found | `{"detail": "Product not found"}` |

## API Reference

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/login` | Login, returns JWT token | None |
| POST | `/api/auth/users` | Create user | Admin |
| GET | `/api/auth/users` | List all users with assigned products | Admin |
| POST | `/api/auth/users/{user_id}/products` | Assign products to user | Admin |
| GET | `/api/auth/users/{user_id}/products` | Get user's assigned products | Admin |
| GET | `/api/auth/me` | Get current user info | Bearer |

### Products & Documents

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/products` | Create product | Admin |
| GET | `/api/products` | List products (filtered by user access) | Bearer |
| POST | `/api/products/{product_id}/documents` | Upload document (PDF/DOCX/TXT) | Admin |
| GET | `/api/products/{product_id}/documents` | List uploaded documents | Bearer |
| POST | `/api/products/preview-url` | Preview website before scraping | Admin |
| POST | `/api/products/scrape` | Scrape website and ingest | Admin |
| GET | `/api/products/{product_id}/scraped` | List scraped sources | Bearer |
| POST | `/api/products/{product_id}/rebuild` | Rebuild FAISS embeddings | Admin |

### Query

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/query` | Ask a question (RAG pipeline) | Bearer |

### Admin Config

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/admin/config` | Get current config (API key masked) | Admin |
| PUT | `/api/admin/config` | Update Anthropic API key | Admin |

## Test Cases

### 1. Authentication Tests

```bash
BASE=http://localhost:8000

# TC-1.1: Admin login (valid credentials)
curl -s $BASE/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
# Expected: 200 — {"access_token":"...","token_type":"bearer","role":"admin","username":"admin"}

# TC-1.2: Login with wrong password
curl -s $BASE/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"wrongpass"}'
# Expected: 401 — {"detail":"Invalid credentials"}

# TC-1.3: Access protected endpoint without token
curl -s $BASE/api/products
# Expected: 401 — {"detail":"Not authenticated"}

# TC-1.4: Get current user info
TOKEN=<your_token>
curl -s $BASE/api/auth/me -H "Authorization: Bearer $TOKEN"
# Expected: 200 — {"username":"admin","role":"admin","user_id":1}
```

### 2. User Management Tests

```bash
# TC-2.1: Create a new user
curl -s $BASE/api/auth/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test123","role":"user"}'
# Expected: 200 — {"id":...,"username":"testuser","role":"user"}

# TC-2.2: Create duplicate user
curl -s $BASE/api/auth/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test123","role":"user"}'
# Expected: 400 — {"detail":"Username already exists"}

# TC-2.3: List all users
curl -s $BASE/api/auth/users -H "Authorization: Bearer $TOKEN"
# Expected: 200 — Array of users with assigned_products field

# TC-2.4: Non-admin trying to create user
USER_TOKEN=<regular_user_token>
curl -s $BASE/api/auth/users \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username":"hacker","password":"hack","role":"admin"}'
# Expected: 403 — {"detail":"Admin access required"}
```

### 3. Product Tests

```bash
# TC-3.1: Create product
curl -s $BASE/api/products \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id":"PROD01","name":"My Product","description":"Test product"}'
# Expected: 200 — {"id":...,"product_id":"PROD01","name":"My Product","description":"Test product"}

# TC-3.2: Duplicate product ID
curl -s $BASE/api/products \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id":"PROD01","name":"Another","description":"dup"}'
# Expected: 400 — {"detail":"Product ID already exists"}

# TC-3.3: List products (admin sees all)
curl -s $BASE/api/products -H "Authorization: Bearer $TOKEN"
# Expected: 200 — Array of all products

# TC-3.4: List products (user sees only assigned)
curl -s $BASE/api/products -H "Authorization: Bearer $USER_TOKEN"
# Expected: 200 — Only products assigned to this user (or all if none assigned)
```

### 4. Product Assignment Tests

```bash
# TC-4.1: Assign products to user
curl -s $BASE/api/auth/users/2/products \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '["PROD01"]'
# Expected: 200 — {"message":"Assigned 1 products to user 2"}

# TC-4.2: Get user's assigned products
curl -s $BASE/api/auth/users/2/products \
  -H "Authorization: Bearer $TOKEN"
# Expected: 200 — ["PROD01"]

# TC-4.3: Verify user only sees assigned products
curl -s $BASE/api/products -H "Authorization: Bearer $USER_TOKEN"
# Expected: 200 — Only PROD01 in the list
```

### 5. Document Upload Tests

```bash
# TC-5.1: Upload TXT file
echo "Product documentation content here." > /tmp/test.txt
curl -s $BASE/api/products/PROD01/documents \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/test.txt"
# Expected: 200 — {"message":"Document uploaded and processed","document_id":"...","chunks_created":1,...}

# TC-5.2: Upload unsupported file type
echo "data" > /tmp/test.csv
curl -s $BASE/api/products/PROD01/documents \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/test.csv"
# Expected: 400 — {"detail":"Unsupported file type. Allowed: .docx, .txt, .pdf"}

# TC-5.3: Upload to non-existent product
curl -s $BASE/api/products/NONEXIST/documents \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/test.txt"
# Expected: 404 — {"detail":"Product not found"}

# TC-5.4: List documents for a product
curl -s $BASE/api/products/PROD01/documents \
  -H "Authorization: Bearer $TOKEN"
# Expected: 200 — Array of document records with chunk_count and status

# TC-5.5: List all documents across products
curl -s $BASE/api/products/_all/documents \
  -H "Authorization: Bearer $TOKEN"
# Expected: 200 — All documents from all products
```

### 6. Web Scraper Tests

```bash
# TC-6.1: Preview URL before scraping
curl -s $BASE/api/products/preview-url \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
# Expected: 200 — {"html":"...","text_preview":"...","text_length":...,"url":"..."}

# TC-6.2: Preview with empty URL
curl -s $BASE/api/products/preview-url \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":""}'
# Expected: 400 — {"detail":"URL is required"}

# TC-6.3: Preview with invalid URL
curl -s $BASE/api/products/preview-url \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"not-a-url"}'
# Expected: 400 — {"detail":"URL must start with http:// or https://"}

# TC-6.4: Scrape and ingest
curl -s $BASE/api/products/scrape \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id":"PROD01","url":"https://example.com","max_pages":5}'
# Expected: 200 — {"message":"Website scraped and processed","pages_scraped":...,"chunks_created":...}

# TC-6.5: Scrape for non-existent product
curl -s $BASE/api/products/scrape \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id":"NONEXIST","url":"https://example.com","max_pages":5}'
# Expected: 404 — {"detail":"Product not found"}

# TC-6.6: List scraped sources
curl -s $BASE/api/products/PROD01/scraped \
  -H "Authorization: Bearer $TOKEN"
# Expected: 200 — Array of scraped document records
```

### 7. RAG Query Tests

```bash
# TC-7.1: Ask a question (with documents ingested)
curl -s $BASE/api/query \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"productId":"PROD01","question":"What is this product about?"}'
# Expected: 200 — {"answer":"...","sources":["filename.txt"]}

# TC-7.2: Empty question
curl -s $BASE/api/query \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"productId":"PROD01","question":""}'
# Expected: 400 — {"detail":"Question is required"}

# TC-7.3: Empty product ID
curl -s $BASE/api/query \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"productId":"","question":"test"}'
# Expected: 400 — {"detail":"Product ID is required"}
```

### 8. Admin Config Tests

```bash
# TC-8.1: Get config
curl -s $BASE/api/admin/config \
  -H "Authorization: Bearer $TOKEN"
# Expected: 200 — {"anthropic_api_key":"***configured***"} (masked) or empty if not set

# TC-8.2: Update API key
curl -s -X PUT $BASE/api/admin/config \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"anthropic_api_key":"sk-ant-api03-xxxxx"}'
# Expected: 200 — {"message":"Configuration updated"}

# TC-8.3: Non-admin access to config
curl -s $BASE/api/admin/config \
  -H "Authorization: Bearer $USER_TOKEN"
# Expected: 403 — {"detail":"Admin access required"}
```

### 9. Rebuild Embeddings Test

```bash
# TC-9.1: Rebuild embeddings for a product
curl -s -X POST $BASE/api/products/PROD01/rebuild \
  -H "Authorization: Bearer $TOKEN"
# Expected: 200 — {"message":"Rebuilt embeddings for N chunks"}
```

## Project Structure

```
rag-knowledge-assistant/
├── app/
│   ├── main.py                    # FastAPI app, routers, startup
│   ├── api/
│   │   ├── auth.py                # Login, user CRUD, product assignment
│   │   ├── products.py            # Product CRUD, doc upload, scraping
│   │   ├── query.py               # RAG query endpoint
│   │   └── admin.py               # Config management
│   ├── core/
│   │   ├── config.py              # App settings (Pydantic)
│   │   ├── database.py            # SQLite schema & connection
│   │   └── security.py            # JWT, bcrypt, auth dependencies
│   ├── rag/
│   │   ├── vector_store.py        # FAISS indexing & search
│   │   ├── llm_client.py          # Claude API integration
│   │   ├── document_processor.py  # PDF/DOCX/TXT parsing & chunking
│   │   └── web_scraper.py         # Website crawling & text extraction
│   ├── schemas/
│   │   └── schemas.py             # Pydantic request/response models
│   └── services/
│       └── config_service.py      # DB config read/write
├── static/
│   └── index.html                 # Single-page web UI
├── data/                          # SQLite DB + FAISS indexes (auto-created)
├── uploads/                       # Uploaded documents (auto-created)
├── run.py                         # Entry point
└── requirements.txt               # Python dependencies
```

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `SECRET_KEY` | `change-this-...` | JWT signing key (change in production) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` (24h) | Token expiry |
| `CLAUDE_MODEL` | `claude-sonnet-4-20250514` | Claude model for Q&A |
| `RETRIEVAL_TOP_K` | `5` | Number of chunks retrieved per query |
| `LLM_TEMPERATURE` | `0.0` | LLM temperature (0 = deterministic) |
| `CHUNK_SIZE` | `1000` | Characters per chunk |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |

## Default Credentials

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | Admin |

> Change the admin password after first login in production.

## License

MIT
