# -*- coding: utf-8 -*-
"""阶段1 Model Adapter 基础层测试（标准库 unittest）。"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import ModelAdapter, ModelRegistry


class MockAdapter(ModelAdapter):
    name = "mock"

    def generate(self, prompt, system=None, **kwargs):
        return "mock:" + (system or "") + prompt


class TestModelAdapter(unittest.TestCase):
    def test_unconfigured_health_check_disabled(self):
        adapter = ModelAdapter({"enabled": False})
        result = adapter.health_check()
        self.assertEqual(result["status"], "disabled")

    def test_configured_health_check_enabled(self):
        adapter = MockAdapter({"enabled": True})
        result = adapter.health_check()
        self.assertEqual(result["status"], "enabled")
        self.assertEqual(result["adapter"], "mock")

    def test_mock_generate(self):
        adapter = MockAdapter({"enabled": True})
        self.assertEqual(adapter.generate("hello", system="s:"), "mock:s:hello")

    def test_registry_register_get_list(self):
        reg = ModelRegistry()
        reg.register("mock", MockAdapter({}))
        self.assertIs(reg.get("mock").__class__, MockAdapter)
        self.assertEqual(reg.list(), ["mock"])
        self.assertIsNone(reg.get("missing"))

    def test_registry_rejects_invalid(self):
        reg = ModelRegistry()
        with self.assertRaises(TypeError):
            reg.register("bad", object())


if __name__ == "__main__":
    unittest.main()
