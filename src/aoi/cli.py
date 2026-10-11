"""Terminal entry points for a working storage demo and optional model chat."""
from __future__ import annotations
import argparse
import tempfile
from pathlib import Path
from .assistant import AoiAssistant
from .config import Settings
from .retrieval import KeywordRetriever, SemanticRetriever
from .storage import SQLiteStore


def demo() -> None:
    # Use a temporary database: demo data never enters the user's real memory.
    with tempfile.TemporaryDirectory(prefix="aoi-demo-") as workdir:
        store = SQLiteStore(Path(workdir) / "demo.sqlite3")
        store.add_exchange("demo", "What stores Aoi's chat history?", "SQLite stores the chat history.")
        store.add_memory("Project Aoi stores its conversation history in SQLite.", source="demo")
        store.add_memory("The memory retrieval prototype also explores semantic embeddings.", source="demo")
        print("Project Aoi | local storage demonstration")
        print("----------------------------------------")
        print(f"Chat messages saved: {len(store.recent_messages('demo'))}")
        print(f"Long-term notes saved: {len(store.list_memories())}")
        print("Search query: 'SQLite chat history'")
        results = KeywordRetriever().search("SQLite chat history", store.list_memories())
        for memory in results:
            print(f"Matched note #{memory.id}: {memory.content}")
        print("Demo complete. This mode does not load an AI model.")


def chat(settings: Settings, conversation_id: str, retrieval: str) -> None:
    from .model import LocalQwenGenerator

    store = SQLiteStore(settings.db_path)
    retriever = None
    if retrieval == "keyword":
        retriever = KeywordRetriever()
    elif retrieval == "semantic":
        retriever = SemanticRetriever(settings.embedding_model, settings.memory_threshold)
    generator = LocalQwenGenerator(settings.model_name, settings.max_new_tokens, settings.temperature)
    assistant = AoiAssistant(store, generator, retriever)
    print("Aoi prototype chat | /quit to exit | /remember TEXT to save a note")
    print("Use only non-sensitive demo content. The local SQLite file is not encrypted.")
    while True:
        try:
            line = input("You > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if line.lower() in ("/quit", "/exit"):
            break
        if line.startswith("/remember "):
            note = line[len("/remember "):].strip()
            if note:
                number = store.add_memory(note, source="terminal-command")
                print(f"Saved note #{number}")
            else:
                print("Usage: /remember your note")
            continue
        if not line:
            continue
        try:
            print("Aoi > " + assistant.reply(line, conversation_id))
        except (RuntimeError, ValueError) as exc:
            print("Aoi error: " + str(exc))


def main() -> None:
    parser = argparse.ArgumentParser(description="Project Aoi local AI prototype")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("demo", help="Run a storage and search demo without downloading models")
    chat_parser = sub.add_parser("chat", help="Chat with the local model (requires optional extras)")
    chat_parser.add_argument("--conversation", default="main", help="Conversation name")
    chat_parser.add_argument("--retrieval", choices=["none", "keyword", "semantic"], default="keyword")
    args = parser.parse_args()
    if args.command == "demo":
        demo()
    elif args.command == "chat":
        chat(Settings.from_env(), args.conversation, args.retrieval)


if __name__ == "__main__":
    main()
