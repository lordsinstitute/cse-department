from fastapi import APIRouter, Depends, HTTPException
import sqlite3

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.schemas import QueryRequest, QueryResponse
from app.rag.vector_store import vector_store
from app.rag.llm_client import generate_answer
from app.services.config_service import get_active_api_key, get_active_model, get_active_top_k, get_active_temperature

router = APIRouter(prefix="/api", tags=["Query"])


@router.post("/query", response_model=QueryResponse)
def query_product(
    req: QueryRequest,
    conn: sqlite3.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if not req.productId or not req.productId.strip():
        raise HTTPException(status_code=400, detail="Product ID is required")
    if not req.question or not req.question.strip():
        raise HTTPException(status_code=400, detail="Question is required")

    product = conn.execute("SELECT id FROM products WHERE product_id = ?", (req.productId,)).fetchone()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if current_user["role"] != "admin":
        restricted = conn.execute(
            "SELECT product_id FROM user_products WHERE user_id = ?",
            (current_user["user_id"],),
        ).fetchall()
        if restricted:
            allowed = [r["product_id"] for r in restricted]
            if req.productId not in allowed:
                raise HTTPException(status_code=403, detail="You do not have access to this product")

    # Using local Ollama model instead of Anthropic
    api_key = None

    top_k = get_active_top_k(conn)
    model = get_active_model(conn)
    temperature = get_active_temperature(conn)

    # Vector search (local embeddings, no API key needed)
    chunks = vector_store.search(req.productId, req.question, top_k=top_k)

    if not chunks:
        return QueryResponse(
            answer="I could not find the answer in the product documentation.",
            sources=[],
        )

    answer = generate_answer(
        question=req.question,
        chunks=chunks,
        api_key=api_key,
        model=model,
        temperature=temperature,
    )

    sources = list(set(c["source_file"] for c in chunks))
    return QueryResponse(answer=answer, sources=sources)
