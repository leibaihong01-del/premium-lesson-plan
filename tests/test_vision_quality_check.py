# -*- coding: utf-8 -*-
"""Vision Quality Check Skill 测试。"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.vision_quality_check import run_quality_check


class TestVisionQualityCheck(unittest.TestCase):
    def test_missing_section(self):
        result = run_quality_check("只有标题", {"sections": ["教学目标", "教学内容"]})
        self.assertFalse(result["ok"])
        self.assertEqual(len(result["issues"]), 2)

    def test_all_sections_present(self):
        result = run_quality_check("教学目标\n教学内容", {"sections": ["教学目标", "教学内容"]})
        self.assertTrue(result["ok"])
        self.assertEqual(result["score"], 1.0)


if __name__ == "__main__":
    unittest.main()