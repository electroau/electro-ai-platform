import os
import json
import numpy as np
from typing import List, Dict
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer


class SemanticRAG:
    """
    Production-ready Semantic RAG (Local)

    Features:
    - Works even if no docs exist
    - Persistent cache (no recompute)
    - Fast similarity search
    - Ready for future upload system
    """

    def __init__(self, docs_path="docs", cache_path="rag_cache.json"):
        self.docs_path = docs_path
        self.cache_path = cache_path

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.chunks = []
        self.embeddings = []

        self._load_or_build()

    # =========================
    # Load or Build Cache 🔥
    # =========================
    def _load_or_build(self):
        # Load existing cache
        if os.path.exists(self.cache_path):
            self._load_cache()
            return

        # No docs → safe exit
        if not os.path.exists(self.docs_path) or not os.listdir(self.docs_path):
            print("⚠️ No documents found. RAG is empty but system is OK.")
            return

        # Build new index
        self._build_index()
        self._save_cache()

    # =========================
    # Build Index
    # =========================
    def _build_index(self):
        for file in os.listdir(self.docs_path):
            if file.endswith(".pdf"):
                path = os.path.join(self.docs_path, file)
                text = self._read_pdf(path)

                chunks = self._chunk_text(text)

                for chunk in chunks:
                    emb = self.model.encode(chunk)

                    self.chunks.append({
                        "content": chunk,
                        "source": file
                    })

                    self.embeddings.append(emb.tolist())

    # =========================
    # Save Cache
    # =========================
    def _save_cache(self):
        data = {
            "chunks": self.chunks,
            "embeddings": self.embeddings
        }

        with open(self.cache_path, "w") as f:
            json.dump(data, f)

    # =========================
    # Load Cache
    # =========================
    def _load_cache(self):
        with open(self.cache_path, "r") as f:
            data = json.load(f)

        self.chunks = data.get("chunks", [])
        self.embeddings = data.get("embeddings", [])

    # =========================
    # Read PDF
    # =========================
    def _read_pdf(self, path: str) -> str:
        try:
            reader = PdfReader(path)
            text = ""

            for page in reader.pages:
                text += page.extract_text() or ""

            return text
        except Exception:
            return ""

    # =========================
    # Chunking
    # =========================
    def _chunk_text(self, text: str, size: int = 500) -> List[str]:
        return [text[i:i + size] for i in range(0, len(text), size)]

    # =========================
    # Search 🔥
    # =========================
    def search(self, query: str, top_k: int = 3) -> List[Dict]:

        if not self.embeddings:
            return []

        query_emb = self.model.encode(query)

        scores = []

        for i, emb in enumerate(self.embeddings):
            emb_np = np.array(emb)
            sim = self._cosine_similarity(query_emb, emb_np)
            scores.append((sim, i))

        scores.sort(reverse=True)

        results = []
        for score, idx in scores[:top_k]:
            results.append({
                "content": self.chunks[idx]["content"],
                "source": self.chunks[idx]["source"],
                "score": float(score)
            })

        return results

    def _cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
