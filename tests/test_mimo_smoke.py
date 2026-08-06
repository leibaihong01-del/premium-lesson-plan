# -*- coding: utf-8 -*-
"""真实 MiMo API 冒烟测试（未配置环境变量时跳过）。"""
import base64
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.vision_smoke import run_smoke

PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)


class TestMimoSmoke(unittest.TestCase):
    def test_skips_without_env(self):
        os.environ.pop("MIMO_API_KEY", None)
        os.environ.pop("MIMO_BASE_URL", None)
        result = run_smoke("x.png")
        self.assertTrue(result.get("skipped", False))

    @unittest.skipUnless(
        os.getenv("MIMO_API_KEY") and os.getenv("MIMO_BASE_URL"),
        "真实 MiMo API 未配置",
    )
    def test_real_api_smoke(self):
        tmp = tempfile.mkdtemp(prefix="mimo_smoke_")
        try:
            img = os.path.join(tmp, "pixel.png")
            with open(img, "wb") as f:
                f.write(PNG_1X1)
            result = run_smoke(img, "请用一句话描述图片内容")
            self.assertIn("ok", result)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()