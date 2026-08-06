# -*- coding: utf-8 -*-
"""Vision 自动路由测试。"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from router.vision_router import decide_vision


class TestVisionRouter(unittest.TestCase):
    def test_text_task_no_vision(self):
        r = decide_vision({"request": "生成课程标准"}, providers=["mimo"], enabled=True)
        self.assertEqual(r["strategy"], "none")

    def test_vision_disabled_fallback_rule(self):
        r = decide_vision({"request": "分析课件PPT页面版式"}, providers=["mimo"], enabled=False)
        self.assertEqual(r["strategy"], "rule")

    def test_vision_enabled(self):
        r = decide_vision({"request": "请分析教材图片"}, providers=["mimo"], enabled=True)
        self.assertEqual(r["strategy"], "vision")
        self.assertEqual(r["provider"], "mimo")

    def test_spec_domain_triggers(self):
        spec = {"domains": ["PPT"], "raw": ""}
        r = decide_vision({}, spec=spec, providers=["mimo"], enabled=True)
        self.assertEqual(r["strategy"], "vision")


if __name__ == "__main__":
    unittest.main()