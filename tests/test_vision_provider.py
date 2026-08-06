# -*- coding: utf-8 -*-
"""Vision Provider 插件测试。"""
import base64
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from providers.vision import MimoVisionProvider, VisionProviderRegistry, analyze_media, render_pdf_page

PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)


def write_png(directory):
    p = os.path.join(directory, "pixel.png")
    with open(p, "wb") as f:
        f.write(PNG_1X1)
    return p


class FakeVisionProvider:
    name = "fake"

    def __init__(self):
        self.calls = []

    def health_check(self):
        return {"provider": self.name, "status": "enabled"}

    def analyze(self, image_path, prompt, **kwargs):
        self.calls.append((image_path, prompt))
        return {"ok": True, "analysis": "fake analysis", "provider": self.name}


class TestVisionProvider(unittest.TestCase):
    def test_registry(self):
        reg = VisionProviderRegistry()
        reg.register("fake", FakeVisionProvider())
        self.assertIsNotNone(reg.get("fake"))
        self.assertEqual(reg.list(), ["fake"])
        with self.assertRaises(TypeError):
            reg.register("bad", object())

    def test_mimo_disabled(self):
        p = MimoVisionProvider({"enabled": False, "api_key_env": "MIMO_API_KEY"})
        self.assertEqual(p.health_check()["status"], "disabled")
        result = p.analyze("x.png", "prompt")
        self.assertFalse(result["ok"])

    def test_mimo_misconfigured(self):
        p = MimoVisionProvider({"enabled": True, "api_key_env": "MIMO_API_KEY",
                                "base_url": "http://x"})
        self.assertEqual(p.health_check()["status"], "misconfigured")

    def test_analyze_missing_file(self):
        result = analyze_media("nope.png", "prompt", FakeVisionProvider())
        self.assertFalse(result["ok"])
        self.assertIn("不存在", result["error"])

    def test_analyze_image_with_fake_provider(self):
        tmp = tempfile.mkdtemp(prefix="vision_")
        try:
            img = write_png(tmp)
            provider = FakeVisionProvider()
            result = analyze_media(img, "分析图片", provider)
            self.assertTrue(result["ok"])
            self.assertEqual(provider.calls[0][0], img)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_render_pdf_missing(self):
        self.assertIsNone(render_pdf_page("missing.pdf"))

    def test_analyze_pdf_missing(self):
        result = analyze_media("missing.pdf", "分析", FakeVisionProvider(), page_index=0)
        self.assertFalse(result["ok"])


if __name__ == "__main__":
    unittest.main()