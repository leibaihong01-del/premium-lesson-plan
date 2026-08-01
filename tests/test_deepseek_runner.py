# -*- coding: utf-8 -*-
"""DeepSeek 独立评测 runner 测试（5.2-E）。"""
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evaluation.runners.deepseek_runner import run_verification


class FakeAdapter:
    name = "fake"

    def __init__(self, text):
        self._text = text

    def health_check(self):
        return {"status": "enabled"}

    def generate(self, prompt, system=None, **kwargs):
        return self._text


class TestDeepSeekRunner(unittest.TestCase):
    def test_run_without_llm(self):
        tmp = tempfile.mkdtemp(prefix="ds_runner_")
        try:
            report, md, js = run_verification(reports_dir=tmp)
            self.assertTrue(os.path.exists(md))
            self.assertTrue(os.path.exists(js))
            self.assertEqual(report["summary"]["rule"]["total"], 10)
            self.assertFalse(report["llm_enabled"])
            self.assertIn("deepseek", report["summary"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_run_with_mock_adapter(self):
        tmp = tempfile.mkdtemp(prefix="ds_runner_")
        try:
            payload = json.dumps({"intent": "generate", "domains": ["教案"],
                                  "quality": "excellent", "constraints": [],
                                  "deliverables": ["教案"]}, ensure_ascii=False)
            report, md, js = run_verification(reports_dir=tmp,
                                              adapter=FakeAdapter(payload),
                                              llm_enabled=True)
            self.assertTrue(report["llm_enabled"])
            self.assertEqual(report["summary"]["deepseek"]["total"], 10)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()