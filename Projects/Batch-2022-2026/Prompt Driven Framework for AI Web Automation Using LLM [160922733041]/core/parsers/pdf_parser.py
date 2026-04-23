"""PDF resume parser: pymupdf4llm + LLM for structured extraction."""

import hashlib
import pymupdf4llm
from core.llm.client_factory import create_llm_client
from core.llm.tools import RESUME_PARSE_TOOL
from core.llm.prompts import RESUME_PARSE_PROMPT

# In-memory cache: file content hash -> parsed resume data
_resume_cache = {}


def parse_resume(filepath):
    """Parse a PDF resume into structured data.

    Two-stage process:
    1. Convert PDF to markdown using pymupdf4llm
    2. Send to LLM (Claude or Gemini) with tool calling to extract structured fields

    Results are cached by file content hash to avoid redundant LLM calls.

    Args:
        filepath: Path to the PDF file

    Returns:
        dict with structured resume data
    """
    # Stage 1: PDF -> markdown
    md_text = pymupdf4llm.to_markdown(filepath)

    if not md_text or len(md_text.strip()) < 20:
        raise ValueError("Could not extract text from PDF. The file may be image-only or corrupted.")

    # Check cache by content hash
    content_hash = hashlib.md5(md_text.encode()).hexdigest()
    if content_hash in _resume_cache:
        return _resume_cache[content_hash]

    # Truncate very long resumes to save tokens (keep first 3000 chars)
    truncated = md_text[:3000] if len(md_text) > 3000 else md_text

    # Stage 2: LLM extracts structured data
    client = create_llm_client()
    prompt = RESUME_PARSE_PROMPT.format(resume_text=truncated)

    resume_data = client.parse_resume(
        system_prompt="You are a resume parser. Extract all structured data from the resume.",
        resume_text=prompt,
        tool=RESUME_PARSE_TOOL,
    )

    if not resume_data:
        raise ValueError("Failed to extract structured data from resume.")

    # Cache the result
    _resume_cache[content_hash] = resume_data
    return resume_data
