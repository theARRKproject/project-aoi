"""Two small memory ranking options: keyword demo and semantic embeddings.

Neither method is a production retrieval service. Semantic ranking loads a
SentenceTransformer model on demand and scores the current memory list.
"""
from __future__ import annotations

import re
from typing import Protocol
from .storage import Memory


class Retriever(Protocol):
    def search(self, query: str, memories: list[Memory], top_k: int = 3) -> list[Memory]: ...


class KeywordRetriever:
    """Dependency-free demo. Not a substitute for semantic search."""
    @staticmethod
    def _terms(value: str) -> set[str]:
        return set(re.findall(r"[a-z0-9]+", value.lower()))

    def search(self, query: str, memories: list[Memory], top_k: int = 3) -> list[Memory]:
        if top_k <= 0 or not query.strip():
            return []
        query_terms = self._terms(query)
        ranked = [(len(query_terms & self._terms(m.content)), m) for m in memories]
        ranked.sort(key=lambda item: (-item[0], -item[1].id))
        return [m for score, m in ranked if score > 0][:top_k]


class SemanticRetriever:
    def __init__(self, model_name: str, threshold: float = 0.30):
        self.model_name = model_name
        self.threshold = threshold
        self._model = None

    def _load(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as exc:
                raise RuntimeError("Install semantic search: pip install -e '.[semantic]'") from exc
            self._model = SentenceTransformer(self.model_name, device="cpu")
        return self._model

    def search(self, query: str, memories: list[Memory], top_k: int = 3) -> list[Memory]:
        if not query.strip() or not memories or top_k <= 0:
            return []
        model = self._load()
        # The model returns normalized vectors; cosine score is their dot product.
        embeddings = model.encode(
            [query] + [memory.content for memory in memories],
            normalize_embeddings=True,
        )
        query_vector = embeddings[0]
        scored = [(float(query_vector @ vector), memory)
                  for memory, vector in zip(memories, embeddings[1:])]
        scored.sort(key=lambda item: (-item[0], -item[1].id))
        return [memory for score, memory in scored if score >= self.threshold][:top_k]
