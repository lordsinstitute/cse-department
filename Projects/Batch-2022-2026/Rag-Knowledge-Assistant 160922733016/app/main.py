from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.database import init_db
from app.rag.vector_store import vector_store
from app.api import auth, products, query, admin

app = FastAPI(
    title="RAG Knowledge Assistant",
    description="Multi-product knowledge assistant with RAG pipeline",
    version="1.0.0",
)

# Include routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(query.router)
app.include_router(admin.router)

# Serve static frontend
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def startup():
    init_db()
    vector_store.load_all_indexes()


@app.get("/")
def root():
    return FileResponse("static/index.html")
