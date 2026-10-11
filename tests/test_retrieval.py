import unittest
from aoi.retrieval import KeywordRetriever
from aoi.storage import Memory


class KeywordRetrieverTests(unittest.TestCase):
    def test_returns_highest_overlap_first(self):
        memories = [
            Memory(1, "Aoi uses SQLite for chat history", "test", "now"),
            Memory(2, "Python powers the tool", "test", "now"),
            Memory(3, "SQLite supports local storage", "test", "now"),
        ]
        found = KeywordRetriever().search("SQLite chat history", memories)
        self.assertEqual([m.id for m in found], [1, 3])

    def test_empty_or_unmatched_query(self):
        memories = [Memory(1, "One note", "test", "now")]
        self.assertEqual(KeywordRetriever().search("", memories), [])
        self.assertEqual(KeywordRetriever().search("blue", memories), [])
