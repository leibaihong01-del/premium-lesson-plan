# -*- coding: utf-8 -*-
"""阶段1.5 Task State 持久化测试。"""
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state.store import TaskStore


class TestTaskStore(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="courseagent_state_")
        self.store = TaskStore(root=os.path.join(self.tmp, "tasks"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_save_load_roundtrip(self):
        rec = self.store.new({"goal": "test"})
        rec["state"] = "EXECUTING"
        self.store.save(rec)
        loaded = self.store.load(rec["task_id"])
        self.assertEqual(loaded["state"], "EXECUTING")
        self.assertEqual(loaded["spec"]["goal"], "test")

    def test_resume_returns_last_step(self):
        rec = self.store.new({})
        rec["steps"] = ["TRANSLATED", "PLANNED"]
        self.store.save(rec)
        resumed = self.store.resume(rec["task_id"])
        self.assertEqual(resumed["last_step"], "PLANNED")

    def test_list_and_missing(self):
        rec = self.store.new({})
        self.assertIn(rec["task_id"], self.store.list())
        self.assertIsNone(self.store.load("missing-id"))

    def test_delete(self):
        rec = self.store.new({})
        self.assertTrue(self.store.delete(rec["task_id"]))
        self.assertFalse(self.store.delete(rec["task_id"]))

    def test_append_log(self):
        rec = self.store.new({})
        self.store.append_log(rec["task_id"], "step done")
        log = os.path.join(self.store.log_root, rec["task_id"] + ".log")
        self.assertTrue(os.path.exists(log))


if __name__ == "__main__":
    unittest.main()
