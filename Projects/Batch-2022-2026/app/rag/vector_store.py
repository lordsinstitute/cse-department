import os
import pickle
from typing import List, Dict

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from app.core.config import settings

# Load model once at module level
_model = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


class VectorStore:
    def __init__(self):
        self.indexes: Dict[str, faiss.IndexFlatL2] = {}
        self.chunk_mappings: Dict[str, List[Dict]] = {}
        self.dimension = 384  # all-MiniLM-L6-v2 dimension

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        model = _get_model()
        embeddings = model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()

    def _index_path(self, product_id: str) -> str:
        return os.path.join(settings.FAISS_INDEX_DIR, f"{product_id}.index")

    def _mapping_path(self, product_id: str) -> str:
        return os.path.join(settings.FAISS_INDEX_DIR, f"{product_id}.pkl")

    def add_chunks(self, product_id: str, chunks: List[Dict]):
        texts = [c["text_chunk"] for c in chunks]
        embeddings = self.generate_embeddings(texts)
        embeddings_np = np.array(embeddings, dtype=np.float32)

        if product_id in self.indexes:
            index = self.indexes[product_id]
            existing_mapping = self.chunk_mappings[product_id]
        else:
            index = faiss.IndexFlatL2(self.dimension)
            existing_mapping = []

        index.add(embeddings_np)
        existing_mapping.extend(chunks)

        self.indexes[product_id] = index
        self.chunk_mappings[product_id] = existing_mapping

        faiss.write_index(index, self._index_path(product_id))
        with open(self._mapping_path(product_id), "wb") as f:
            pickle.dump(existing_mapping, f)

    def search(self, product_id: str, query: str, top_k: int = 5) -> List[Dict]:
        if product_id not in self.indexes:
            self._load_index(product_id)

        if product_id not in self.indexes:
            return []

        query_embedding = self.generate_embeddings([query])
        query_np = np.array(query_embedding, dtype=np.float32)

        index = self.indexes[product_id]
        k = min(top_k, index.ntotal)
        if k == 0:
            return []

        distances, indices = index.search(query_np, k)

        results = []
        mapping = self.chunk_mappings[product_id]
        for idx in indices[0]:
            if 0 <= idx < len(mapping):
                results.append(mapping[idx])
        return results

    def _load_index(self, product_id: str):
        index_path = self._index_path(product_id)
        mapping_path = self._mapping_path(product_id)
        if os.path.exists(index_path) and os.path.exists(mapping_path):
            self.indexes[product_id] = faiss.read_index(index_path)
            with open(mapping_path, "rb") as f:
                self.chunk_mappings[product_id] = pickle.load(f)

    def delete_product_index(self, product_id: str):
        self.indexes.pop(product_id, None)
        self.chunk_mappings.pop(product_id, None)
        for path in [self._index_path(product_id), self._mapping_path(product_id)]:
            if os.path.exists(path):
                os.remove(path)

    def load_all_indexes(self):
        index_dir = settings.FAISS_INDEX_DIR
        if not os.path.exists(index_dir):
            return
        for filename in os.listdir(index_dir):
            if filename.endswith(".index"):
                product_id = filename.replace(".index", "")
                self._load_index(product_id)


vector_store = VectorStore()
