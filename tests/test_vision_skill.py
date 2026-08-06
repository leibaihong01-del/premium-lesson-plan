# -*- coding: utf-8 -*-
"""Vision Understanding Skill 测试。"""
import base64
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.vision_understanding import run_vision_analysis, summarize

PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)


class FakeProvider:
    name = "fake"

    def analyze(self, image_path, prompt, **kwargs):
        return {"ok": True, "analysis": "fake skill analysis", "provider": self.name}


class TestVisionSkill(unittest.TestCase):
    def test_run_skill_with_fake_provider(self):
        tmp = tempfile.mkdtemp(prefix="skill_")
        try:
            img = os.path.join(tmp, "a.png")
            with open(img, "wb") as f:
                f.write(PNG_1X1)
            result = run_vision_analysis(img, "分析", provider=FakeProvider())
            self.assertTrue(result["ok"])
            self.assertEqual(result["skill"], "vision_understanding")
            self.assertEqual(result["input"], img)
            self.assertEqual(result["prompt"], "分析")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_summarize_failure(self):
        text = summarize({"ok": False, "error": "文件不存在"})
        self.assertIn("未完成", text)


if __name__ == "__main__":
    unittest.main()