# -*- coding: utf-8 -*-
"""Vision Context 注入层测试。"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from context.vision_context import VisionContext


class TestVisionContext(unittest.TestCase):
    def test_inject_constraints(self):
        result = {"ok": True, "analysis": {
            "layout_elements": ["title", "footer"],
            "page_size": "A4",
            "sections": ["课程基本信息", "教学目标", "教学内容", "教学评价"],
            "notes": ["标题居中"],
        }}
        ctx = VisionContext(result)
        spec = ctx.inject({"raw": "生成课程文档"})
        self.assertTrue(spec["planning_injected"])
        self.assertIn("教学目标", spec["vision_context"]["constraints"]["required_sections"])
        self.assertEqual(spec["vision_context"]["structure"]["page_size"], "A4")


if __name__ == "__main__":
    unittest.main()