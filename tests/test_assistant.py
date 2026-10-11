import tempfile
import unittest
from pathlib import Path
from aoi.assistant import AoiAssistant
from aoi.retrieval import KeywordRetriever
from aoi.storage import SQLiteStore


class StubGenerator:
    def __init__(self, text="Hello from the test generator"):
        self.text = text
        self.last_messages = None

    def generate(self, messages):
        self.last_messages = messages
        if isinstance(self.text, Exception):
            raise self.text
        return self.text


class AoiAssistantTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = SQLiteStore(Path(self.tmp.name) / "test.db")

    def tearDown(self):
        self.tmp.cleanup()

    def test_relevant_memory_and_history_in_prompt(self):
        self.store.add_memory("The project uses SQLite for memory.")
        generator = StubGenerator()
        assistant = AoiAssistant(self.store, generator, KeywordRetriever())
        assistant.reply("Tell me about SQLite", "session-1")
        self.assertIn("SQLite", generator.last_messages[0]["content"])
        assistant.reply("And again", "session-1")
        self.assertEqual([m["role"] for m in generator.last_messages[-3:]],
                         ["user", "assistant", "user"])
        self.assertEqual(len(self.store.recent_messages("session-1")), 4)

    def test_failed_model_does_not_save_partial_exchange(self):
        assistant = AoiAssistant(self.store, StubGenerator(RuntimeError("no response")))
        with self.assertRaises(RuntimeError):
            assistant.reply("Hello", "session-1")
        self.assertEqual(self.store.recent_messages("session-1"), [])
