import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import sqlite3

from app.core.database import get_db
from app.core.config import settings
from app.core.security import get_current_user, require_admin
from app.schemas.schemas import ProductCreate, ProductResponse, ScrapeRequest
from app.rag.document_processor import process_document
from app.rag.web_scraper import scrape_website, process_scraped_pages
from app.rag.vector_store import vector_store

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.post("", response_model=ProductResponse)
def create_product(
    req: ProductCreate,
    conn: sqlite3.Connection = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    existing = conn.execute("SELECT id FROM products WHERE product_id = ?", (req.product_id,)).fetchone()
    if existing:
        raise HTTPException(status_code=400, detail="Product ID already exists")

    cursor = conn.execute(
        "INSERT INTO products (product_id, name, description) VALUES (?, ?, ?)",
        (req.product_id, req.name, req.description),
    )
    conn.commit()
    return ProductResponse(id=cursor.lastrowid, product_id=req.product_id, name=req.name, description=req.description)


@router.get("", response_model=list[ProductResponse])
def list_products(
    conn: sqlite3.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] == "admin":
        rows = conn.execute("SELECT id, product_id, name, description FROM products").fetchall()
    else:
        restricted = conn.execute(
            "SELECT product_id FROM user_products WHERE user_id = ?",
            (current_user["user_id"],)
        ).fetchall()

        if restricted:
            pids = [r["product_id"] for r in restricted]
            placeholders = ",".join("?" * len(pids))
            rows = conn.execute(
                f"SELECT id, product_id, name, description FROM products WHERE product_id IN ({placeholders})",
                pids,
            ).fetchall()
        else:
            rows = conn.execute("SELECT id, product_id, name, description FROM products").fetchall()

    return [ProductResponse(id=r["id"], product_id=r["product_id"], name=r["name"], description=r["description"]) for r in rows]


@router.post("/{product_id}/documents")
def upload_document(
    product_id: str,
    file: UploadFile = File(...),
    conn: sqlite3.Connection = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    product = conn.execute("SELECT id FROM products WHERE product_id = ?", (product_id,)).fetchone()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    allowed_extensions = {".pdf", ".docx", ".txt"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}")

    product_dir = os.path.join(settings.UPLOAD_DIR, product_id)
    os.makedirs(product_dir, exist_ok=True)

    document_id = str(uuid.uuid4())
    file_path = os.path.join(product_dir, f"{document_id}_{file.filename}")

    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)

    chunks = process_document(
        file_path, product_id, document_id,
        settings.CHUNK_SIZE, settings.CHUNK_OVERLAP
    )

    if not chunks:
        raise HTTPException(status_code=400, detail="No text content could be extracted from the document")

    # Store document record first (chunks have FK to documents)
    conn.execute(
        "INSERT INTO documents (document_id, product_id, filename, file_path, chunk_count, status) VALUES (?, ?, ?, ?, ?, ?)",
        (document_id, product_id, file.filename, file_path, len(chunks), "processed"),
    )

    for chunk in chunks:
        conn.execute(
            "INSERT INTO chunks (chunk_id, document_id, product_id, text_chunk, chunk_index, source_file) VALUES (?, ?, ?, ?, ?, ?)",
            (chunk["chunk_id"], chunk["document_id"], chunk["product_id"], chunk["text_chunk"], chunk["chunk_index"], chunk["source_file"]),
        )
    conn.commit()

    # Embeddings are local (sentence-transformers) — no API key needed
    vector_store.add_chunks(product_id, chunks)

    return {
        "message": "Document uploaded and processed",
        "document_id": document_id,
        "chunks_created": len(chunks),
        "filename": file.filename,
    }


@router.get("/{product_id}/documents")
def list_documents(
    product_id: str,
    conn: sqlite3.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if product_id == "_all":
        rows = conn.execute(
            "SELECT d.document_id, d.product_id, d.filename, d.chunk_count, d.status, d.created_at FROM documents d WHERE d.filename NOT LIKE 'web_%' ORDER BY d.created_at DESC"
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT document_id, product_id, filename, chunk_count, status, created_at FROM documents WHERE product_id = ? AND filename NOT LIKE 'web_%' ORDER BY created_at DESC",
            (product_id,),
        ).fetchall()
    return [dict(r) for r in rows]


@router.post("/preview-url")
def preview_url(
    req: dict,
    admin: dict = Depends(require_admin),
):
    from app.rag.web_scraper import scrape_url, extract_text_from_html
    import re

    url = req.get("url", "").strip()
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    if not url.startswith("http://") and not url.startswith("https://"):
        raise HTTPException(status_code=400, detail="URL must start with http:// or https://")

    try:
        page = scrape_url(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")

    # Rewrite relative URLs in HTML to absolute so preview renders correctly
    html = page["html"]
    base_tag = f'<base href="{url}">'
    if "<head>" in html.lower():
        html = re.sub(r'(<head[^>]*>)', r'\1' + base_tag, html, count=1, flags=re.IGNORECASE)
    else:
        html = base_tag + html

    return {
        "html": html,
        "text_preview": page["text"][:2000],
        "text_length": len(page["text"]),
        "url": url,
    }


@router.post("/scrape")
def scrape_and_ingest(
    req: ScrapeRequest,
    conn: sqlite3.Connection = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    product = conn.execute("SELECT id FROM products WHERE product_id = ?", (req.product_id,)).fetchone()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not req.url or not req.url.strip():
        raise HTTPException(status_code=400, detail="URL is required")

    if not req.url.startswith("http://") and not req.url.startswith("https://"):
        raise HTTPException(status_code=400, detail="URL must start with http:// or https://")

    max_pages = min(req.max_pages, 50)  # Cap at 50

    pages = scrape_website(req.url, max_pages=max_pages)
    if not pages:
        raise HTTPException(status_code=400, detail="Could not extract any content from the website")

    document_id = str(uuid.uuid4())
    domain = req.url.split("//")[-1].split("/")[0]
    filename = f"web_{domain}"

    chunks = process_scraped_pages(
        pages, req.product_id, document_id,
        settings.CHUNK_SIZE, settings.CHUNK_OVERLAP
    )

    if not chunks:
        raise HTTPException(status_code=400, detail="No text content could be extracted from the scraped pages")

    conn.execute(
        "INSERT INTO documents (document_id, product_id, filename, file_path, chunk_count, status) VALUES (?, ?, ?, ?, ?, ?)",
        (document_id, req.product_id, filename, req.url, len(chunks), "processed"),
    )

    for chunk in chunks:
        conn.execute(
            "INSERT INTO chunks (chunk_id, document_id, product_id, text_chunk, chunk_index, source_file) VALUES (?, ?, ?, ?, ?, ?)",
            (chunk["chunk_id"], chunk["document_id"], chunk["product_id"], chunk["text_chunk"], chunk["chunk_index"], chunk["source_file"]),
        )
    conn.commit()

    vector_store.add_chunks(req.product_id, chunks)

    return {
        "message": "Website scraped and processed",
        "document_id": document_id,
        "pages_scraped": len(pages),
        "chunks_created": len(chunks),
        "source": req.url,
    }


@router.get("/{product_id}/scraped")
def list_scraped_sources(
    product_id: str,
    conn: sqlite3.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if product_id == "_all":
        rows = conn.execute(
            "SELECT document_id, product_id, filename, file_path, chunk_count, status, created_at FROM documents WHERE filename LIKE 'web_%' ORDER BY created_at DESC"
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT document_id, product_id, filename, file_path, chunk_count, status, created_at FROM documents WHERE product_id = ? AND filename LIKE 'web_%' ORDER BY created_at DESC",
            (product_id,),
        ).fetchall()
    return [dict(r) for r in rows]


@router.post("/{product_id}/rebuild")
def rebuild_embeddings(
    product_id: str,
    conn: sqlite3.Connection = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    vector_store.delete_product_index(product_id)

    rows = conn.execute(
        "SELECT chunk_id, document_id, product_id, text_chunk, chunk_index, source_file FROM chunks WHERE product_id = ?",
        (product_id,),
    ).fetchall()

    if not rows:
        return {"message": "No chunks to rebuild"}

    chunks = [dict(r) for r in rows]
    vector_store.add_chunks(product_id, chunks)

    return {"message": f"Rebuilt embeddings for {len(chunks)} chunks"}
