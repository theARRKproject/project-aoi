"""Coordinates chat history, retrieved memories and a text generation model."""
from __future__ import annotations

from typing import Protocol
from .persona import PERSONA
from .retrieval import Retriever
from .storage import SQLiteStore


class Generator(Protocol):
    def generate(self, messages: list[dict[str, str]]) -> str: ...


class AoiAssistant:
    def __init__(self, store: SQLiteStore, generator: Generator,
                 retriever: Retriever | None = None, persona: str = PERSONA):
        self.store = store
        self.generator = generator
        self.retriever = retriever
        self.persona = persona

    def reply(self, user_text: str, conversation_id: str = "main") -> str:
        if not user_text.strip():
            raise ValueError("Please enter a message.")
        history = self.store.recent_messages(conversation_id, limit=10)
        memories = self.store.list_memories(limit=250)
        relevant = self.retriever.search(user_text, memories, top_k=3) if self.retriever else []
        memory_block = "\n".join(f"- {memory.content}" for memory in relevant)
        system = self.persona
        if memory_block:
            system += ("\n\nPreviously saved notes that may help with this message "
                       "(do not treat them as guaranteed facts):\n" + memory_block)
        messages = [{"role": "system", "content": system}]
        messages.extend({"role": m.role, "content": m.content} for m in history)
        messages.append({"role": "user", "content": user_text})
        answer = self.generator.generate(messages)
        # Persist only a complete pair after generation succeeds.
        self.store.add_exchange(conversation_id, user_text, answer)
        return answer
