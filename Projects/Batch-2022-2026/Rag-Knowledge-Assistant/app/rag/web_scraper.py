import re
import uuid
import requests
from typing import List, Dict
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser


class _TextExtractor(HTMLParser):
    """Extract visible text from HTML, skipping script/style tags."""

    def __init__(self):
        super().__init__()
        self._texts = []
        self._skip = False
        self._skip_tags = {"script", "style", "noscript", "svg", "head"}

    def handle_starttag(self, tag, attrs):
        if tag in self._skip_tags:
            self._skip = True

    def handle_endtag(self, tag):
        if tag in self._skip_tags:
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            text = data.strip()
            if text:
                self._texts.append(text)

    def get_text(self) -> str:
        return "\n".join(self._texts)


def extract_text_from_html(html: str) -> str:
    extractor = _TextExtractor()
    extractor.feed(html)
    text = extractor.get_text()
    # Collapse excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_links(html: str, base_url: str) -> List[str]:
    """Extract same-domain links from HTML."""
    base_domain = urlparse(base_url).netloc
    links = set()
    # Simple regex to find href values
    for match in re.finditer(r'href=["\']([^"\']+)["\']', html):
        href = match.group(1)
        if href.startswith('#') or href.startswith('mailto:') or href.startswith('javascript:'):
            continue
        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)
        # Same domain only, strip fragments
        if parsed.netloc == base_domain:
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if clean_url.rstrip('/') != base_url.rstrip('/'):
                links.add(clean_url)
    return list(links)


def scrape_url(url: str) -> Dict[str, str]:
    """Scrape a single URL and return its text content."""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; RAGBot/1.0)"
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    text = extract_text_from_html(response.text)
    return {"url": url, "text": text, "html": response.text}


def scrape_website(url: str, max_pages: int = 10) -> List[Dict[str, str]]:
    """Scrape a website starting from the given URL, following same-domain links."""
    visited = set()
    to_visit = [url]
    results = []

    while to_visit and len(results) < max_pages:
        current_url = to_visit.pop(0)
        normalized = current_url.rstrip('/')
        if normalized in visited:
            continue
        visited.add(normalized)

        try:
            page = scrape_url(current_url)
            if page["text"]:
                results.append({"url": current_url, "text": page["text"]})
                # Find more links
                new_links = extract_links(page["html"], current_url)
                for link in new_links:
                    if link.rstrip('/') not in visited:
                        to_visit.append(link)
        except Exception:
            continue

    return results


def process_scraped_pages(
    pages: List[Dict[str, str]],
    product_id: str,
    document_id: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List[Dict]:
    """Convert scraped pages into chunk records."""
    from app.rag.document_processor import split_text_into_chunks

    chunk_records = []
    for page in pages:
        url = page["url"]
        text = page["text"]
        chunks = split_text_into_chunks(text, chunk_size, chunk_overlap)

        for i, chunk_text in enumerate(chunks):
            chunk_records.append({
                "chunk_id": str(uuid.uuid4()),
                "document_id": document_id,
                "product_id": product_id,
                "text_chunk": chunk_text,
                "chunk_index": i,
                "source_file": url,
            })

    return chunk_records
