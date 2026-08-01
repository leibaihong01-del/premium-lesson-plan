# -*- coding: utf-8 -*-
"""阶段3 Router 路由决策测试。"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from router import decide, fallback_strategy


class TestRouter(unittest.TestCase):
    def test_rule_intent(self):
        route = decide({"intent": "convert", "quality": "normal"})
        self.assertEqual(route["strategy"], "rule")

    def test_audit_intent_rule(self):
        route = decide({"intent": "audit", "quality": "excellent"}, enabled_providers=["deepseek"])
        self.assertEqual(route["strategy"], "rule")

    def test_excellent_with_provider_hybrid(self):
        route = decide({"intent": "optimize", "quality": "excellent"}, enabled_providers=["deepseek"])
        self.assertEqual(route["strategy"], "hybrid")
        self.assertEqual(route["provider"], "deepseek")

    def test_llm_without_provider_fallback(self):
        route = decide({"intent": "generate", "quality": "excellent"}, enabled_providers=[])
        self.assertEqual(route["strategy"], "rule")

    def test_high_compute_with_provider(self):
        route = decide({"intent": "unknown", "quality": "normal"},
                       enabled_providers=["deepseek"], compute_level="high")
        self.assertEqual(route["strategy"], "llm")

    def test_fallback_strategy(self):
        route = {"strategy": "llm", "provider": "deepseek", "reason": "x"}
        self.assertEqual(fallback_strategy(route)["strategy"], "rule")
        self.assertEqual(fallback_strategy({"strategy": "rule"})["strategy"], "rule")


if __name__ == "__main__":
    unittest.main()
