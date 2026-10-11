"""Local SQLite chat history and explicitly saved long-term memories."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import sqlite3


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class Message:
    conversation_id: str
    role: str
    content: str
    created_at: str


@dataclass(frozen=True)
class Memory:
    id: int
    content: str
    source: str
    created_at: str


class SQLiteStore:
    """Each operation uses its own short-lived connection."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(str(self.path), timeout=10)
        connection.row_factory = sqlite3.Row
        return connection

    def _init_schema(self) -> None:
        with self._connect() as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_messages_conversation
                    ON messages (conversation_id, id);
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    source TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
            """)

    def add_exchange(self, conversation_id: str, user_text: str, reply_text: str) -> None:
        """Commit both halves together so a failed response cannot leave a partial turn."""
        if not conversation_id.strip() or not user_text.strip() or not reply_text.strip():
            raise ValueError("Conversation ID and both messages must be non-empty.")
        with self._connect() as connection:
            timestamp = _utc_now()
            connection.executemany(
                "INSERT INTO messages (conversation_id, role, content, created_at) VALUES (?, ?, ?, ?)",
                [(conversation_id, "user", user_text, timestamp),
                 (conversation_id, "assistant", reply_text, timestamp)],
            )

    def recent_messages(self, conversation_id: str, limit: int = 10) -> list[Message]:
        if limit <= 0:
            return []
        with self._connect() as connection:
            rows = connection.execute(
                """SELECT conversation_id, role, content, created_at
                   FROM messages WHERE conversation_id = ?
                   ORDER BY id DESC LIMIT ?""",
                (conversation_id, limit),
            ).fetchall()
        return [Message(**dict(row)) for row in reversed(rows)]

    def add_memory(self, content: str, source: str = "manual") -> int:
        """Store an explicit memory; chat messages are not auto-promoted."""
        if not content.strip():
            raise ValueError("Memory must contain text.")
        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO memories (content, source, created_at) VALUES (?, ?, ?)",
                (content.strip(), source, _utc_now()),
            )
            return int(cursor.lastrowid)

    def list_memories(self, limit: int = 250) -> list[Memory]:
        if limit <= 0:
            return []
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT id, content, source, created_at FROM memories ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [Memory(**dict(row)) for row in rows]

    def delete_memory(self, memory_id: int) -> bool:
        with self._connect() as connection:
            cursor = connection.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            return cursor.rowcount > 0
