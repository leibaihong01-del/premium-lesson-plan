# -*- coding: utf-8 -*-
"""Preflight Agent 测试（5.2-E 小范围验证）。"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.preflight import preflight
from core.translator import parse


class TestPreflight(unittest.TestCase):
    def test_clear_request(self):
        spec = parse("请优化课程标准，按精品要求，禁止设备维修，输出审核报告")
        r = preflight("请优化课程标准，按精品要求，禁止设备维修，输出审核报告", spec)
        self.assertFalse(r["needs_confirmation"])
        self.assertTrue(r["checks"]["intent_known"])
        self.assertTrue(r["checks"]["domains_known"])

    def test_missing_context(self):
        spec = parse("帮我弄一下")
        r = preflight("帮我弄一下", spec)
        self.assertTrue(r["needs_confirmation"])
        self.assertIn("intent_known", r["missing"])


if __name__ == "__main__":
    unittest.main()