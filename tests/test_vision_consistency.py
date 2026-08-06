# -*- coding: utf-8 -*-
"""Vision Consistency Validator 测试。"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from validators.vision_consistency import validate


class TestVisionConsistency(unittest.TestCase):
    def test_pass_when_sections_present(self):
        structure = {"sections": ["教学目标", "教学内容"], "notes": []}
        result = validate("教学目标\n教学内容", structure)
        self.assertTrue(result["ok"])
        self.assertEqual(result["validator"], "vision_consistency")

    def test_fail_when_missing(self):
        structure = {"sections": ["教学目标", "教学评价"], "notes": []}
        result = validate("只有标题", structure)
        self.assertFalse(result["ok"])
        self.assertGreaterEqual(len(result["issues"]), 2)


if __name__ == "__main__":
    unittest.main()