import tempfile
import unittest
from pathlib import Path

from aoi.storage import SQLiteStore


class SQLiteStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = SQLiteStore(Path(self.tmp.name) / "aoi.db")

    def tearDown(self):
        self.tmp.cleanup()

    def test_exchange_order_and_conversation_isolation(self):
        self.store.add_exchange("one", "Hello", "Hi")
        self.store.add_exchange("one", "Remember?", "Yes")
        self.store.add_exchange("two", "Private", "Different session")
        messages = self.store.recent_messages("one", limit=3)
        self.assertEqual([message.content for message in messages], ["Hi", "Remember?", "Yes"])
        self.assertEqual(len(self.store.recent_messages("two")), 2)

    def test_memories_are_persistent_and_removable(self):
        memory_id = self.store.add_memory("My test note", source="unit-test")
        reopened = SQLiteStore(self.store.path)
        self.assertEqual(reopened.list_memories()[0].content, "My test note")
        self.assertTrue(reopened.delete_memory(memory_id))
        self.assertFalse(reopened.delete_memory(memory_id))

    def test_no_empty_exchanges(self):
        with self.assertRaises(ValueError):
            self.store.add_exchange("main", "Hello", "")
        self.assertEqual(self.store.recent_messages("main"), [])
