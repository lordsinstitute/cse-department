import os
import uuid
from typing import List, Dict

from pypdf import PdfReader
from docx import Document


def parse_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def parse_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])


def parse_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def parse_document(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    parsers = {
        ".pdf": parse_pdf,
        ".docx": parse_docx,
        ".txt": parse_txt,
    }
    parser = parsers.get(ext)
    if not parser:
        raise ValueError(f"Unsupported file type: {ext}")
    return parser(file_path)


def split_text_into_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    if not text.strip():
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - chunk_overlap
    return chunks


def process_document(file_path: str, product_id: str, document_id: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Dict]:
    text = parse_document(file_path)
    chunks = split_text_into_chunks(text, chunk_size, chunk_overlap)
    filename = os.path.basename(file_path)

    chunk_records = []
    for i, chunk_text in enumerate(chunks):
        chunk_records.append({
            "chunk_id": str(uuid.uuid4()),
            "document_id": document_id,
            "product_id": product_id,
            "text_chunk": chunk_text,
            "chunk_index": i,
            "source_file": filename,
        })
    return chunk_records
