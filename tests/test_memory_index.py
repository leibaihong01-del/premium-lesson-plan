# -*- coding: utf-8 -*-
"""阶段4 Memory 结构化索引测试。"""
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.memory import Memory
from memory.index import MemoryIndex


class TestMemoryIndex(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="courseagent_mem_")
        self.m = Memory(root=os.path.join(self.tmp, "system"))
        self.m.add("successes", {"task": "测试任务", "score": 95})
        self.m.add("successes", {"task": "另一任务", "score": 100})

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_rebuild_and_get(self):
        idx = MemoryIndex(self.m)
        data = idx.rebuild(["successes"])
        self.assertEqual(data["successes"]["count"], 2)
        self.assertEqual(idx.get("successes")["count"], 2)

    def test_search_via_index(self):
        idx = MemoryIndex(self.m)
        idx.rebuild(["successes"])
        hits = idx.search("successes", "测试任务")
        self.assertEqual(len(hits), 1)

    def test_old_json_still_readable(self):
        MemoryIndex(self.m).rebuild(["successes"])
        entries = self.m._load("successes")
        self.assertEqual(len(entries), 2)

    def test_counts_and_query_alias(self):
        counts = self.m.counts()
        self.assertGreaterEqual(counts["successes"], 2)
        self.assertEqual(len(self.m.query("successes", "100")), 1)


if __name__ == "__main__":
    unittest.main()
