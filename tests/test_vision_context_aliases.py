# -*- coding: utf-8 -*-
"""Vision Context 中文字段映射测试。"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from context.vision_context import VisionContext


class TestVisionContextAliases(unittest.TestCase):
    def test_chinese_alias_mapping(self):
        result = {"ok": True, "analysis": {
            "关键元素": ["标题区", "内容区"],
            "页面尺寸": "A4",
            "章节": ["教学目标", "教学评价"],
            "建议标签": ["课程模板"],
            "布局结构": "自上而下分栏布局",
        }}
        ctx = VisionContext(result)
        self.assertEqual(ctx.structure["layout_elements"], ["标题区", "内容区"])
        self.assertEqual(ctx.structure["page_size"], "A4")
        self.assertEqual(ctx.structure["sections"], ["教学目标", "教学评价"])
        self.assertIn("课程模板", ctx.structure["notes"])
        self.assertIn("自上而下分栏布局", ctx.structure["notes"])


if __name__ == "__main__":
    unittest.main()