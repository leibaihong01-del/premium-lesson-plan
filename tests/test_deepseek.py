# -*- coding: utf-8 -*-
"""阶段2/5.2-E DeepSeek Adapter 与 LLM增强测试（mock，不真实调用API）。"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.translator import enrich_spec_with_llm, parse, translate_with_enhancement
from models.deepseek import DeepSeekAdapter


class FakeAdapter:
    def __init__(self, text, status="enabled"):
        self._text = text
        self._status = status
        self.name = "fake"

    def health_check(self):
        return {"status": self._status}

    def generate(self, prompt, system=None, **kwargs):
        if self._status != "enabled":
            raise RuntimeError("disabled")
        return self._text


class TestDeepSeek(unittest.TestCase):
    def test_disabled(self):
        a = DeepSeekAdapter({"enabled": False, "api_key_env": "DS_KEY"})
        self.assertEqual(a.health_check()["status"], "disabled")
        with self.assertRaises(RuntimeError):
            a.generate("hi")

    def test_enabled_no_key(self):
        os.environ.pop("DS_KEY", None)
        a = DeepSeekAdapter({"enabled": True, "api_key_env": "DS_KEY"})
        self.assertEqual(a.health_check()["status"], "misconfigured")

    def test_enabled_no_base_url(self):
        os.environ["DS_KEY"] = "test-key"
        a = DeepSeekAdapter({"enabled": True, "api_key_env": "DS_KEY", "base_url": ""})
        self.assertEqual(a.health_check()["status"], "misconfigured")
        os.environ.pop("DS_KEY", None)

    def test_enabled_with_key(self):
        os.environ["DS_KEY"] = "test-key"
        a = DeepSeekAdapter({"enabled": True, "api_key_env": "DS_KEY", "base_url": "http://x"})
        self.assertEqual(a.health_check()["status"], "enabled")
        os.environ.pop("DS_KEY", None)

    def test_usage_initialized(self):
        a = DeepSeekAdapter({"enabled": True, "api_key_env": "DS_KEY", "base_url": "http://x"})
        self.assertEqual(a.usage["calls"], 0)
        self.assertEqual(a.max_retries, 2)

    def test_enrich_merges(self):
        spec = parse("请优化课程标准，按精品要求")
        payload = json.dumps({"intent": "optimize", "domains": ["课程标准"],
                              "quality": "excellent", "constraints": ["闭环报告"]}, ensure_ascii=False)
        out = enrich_spec_with_llm(spec, FakeAdapter(payload))
        self.assertTrue(out.get("llm_enhanced"))
        self.assertEqual(out["quality"], "excellent")
        self.assertIn("闭环报告", out["constraints"])

    def test_enrich_fallback_on_error(self):
        spec = parse("请生成教案")
        out = enrich_spec_with_llm(spec, FakeAdapter("", status="disabled"))
        self.assertFalse(out.get("llm_enhanced", False))
        self.assertEqual(out["domains"], ["教案"])

    def test_translate_with_enhancement_disabled(self):
        spec, route, enhanced = translate_with_enhancement(
            "请优化课程标准", None, FakeAdapter("{}"), enabled=False)
        self.assertFalse(enhanced)
        self.assertEqual(route["strategy"], "rule")

    def test_translate_with_enhancement_enabled(self):
        payload = json.dumps({"intent": "optimize", "domains": ["课程标准"],
                              "quality": "excellent", "constraints": ["闭环报告"]},
                             ensure_ascii=False)
        spec, route, enhanced = translate_with_enhancement(
            "请优化课程标准", None, FakeAdapter(payload), enabled=True)
        self.assertTrue(enhanced)
        self.assertEqual(route["strategy"], "llm")

    def test_translate_with_enhancement_invalid_fallback(self):
        spec, route, enhanced = translate_with_enhancement(
            "请生成教案", None, FakeAdapter("not json", status="disabled"), enabled=True)
        self.assertFalse(enhanced)
        self.assertEqual(route["strategy"], "rule")
        self.assertEqual(spec["domains"], ["教案"])


if __name__ == "__main__":
    unittest.main()