"""Environment-driven settings with no third-party dependencies."""
from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    model_name: str = "Qwen/Qwen2.5-3B-Instruct"
    db_path: Path = Path("data/aoi.sqlite3")
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    max_new_tokens: int = 180
    temperature: float = 0.7
    memory_threshold: float = 0.30

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            model_name=os.getenv("AOI_MODEL_NAME", cls.model_name),
            db_path=Path(os.getenv("AOI_DB_PATH", str(cls.db_path))),
            embedding_model=os.getenv("AOI_EMBEDDING_MODEL", cls.embedding_model),
            max_new_tokens=int(os.getenv("AOI_MAX_NEW_TOKENS", str(cls.max_new_tokens))),
            temperature=float(os.getenv("AOI_TEMPERATURE", str(cls.temperature))),
            memory_threshold=float(os.getenv("AOI_MEMORY_THRESHOLD", str(cls.memory_threshold))),
        )
