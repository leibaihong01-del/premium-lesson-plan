# -*- coding: utf-8 -*-
"""Vision Template Index 测试。"""
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.vision_index import VisionTemplateIndex


class TestVisionIndex(unittest.TestCase):
    def test_index_get_search(self):
        tmp = tempfile.mkdtemp(prefix="vindex_")
        try:
            idx = VisionTemplateIndex(path=os.path.join(tmp, "vt.json"))
            structure = {"sections": ["教学目标"], "page_size": "A4"}
            idx.index("tpl-1", structure, course="城市轨道交通", kind="教案")
            self.assertEqual(idx.get("tpl-1")["structure"]["page_size"], "A4")
            self.assertEqual(len(idx.search(course="城市轨道交通")), 1)
            self.assertEqual(len(idx.search(kind="教案")), 1)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()