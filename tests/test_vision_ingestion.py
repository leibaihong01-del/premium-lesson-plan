# -*- coding: utf-8 -*-
"""Vision Ingestion Workflow 测试。"""
import base64
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflows.vision_ingestion import run_vision_ingestion

PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)


class FakeProvider:
    name = "fake"

    def analyze(self, image_path, prompt, **kwargs):
        return {"ok": True, "analysis": "template structure", "provider": self.name}


class TestVisionIngestion(unittest.TestCase):
    def test_run_with_fake_provider(self):
        tmp = tempfile.mkdtemp(prefix="ingest_")
        try:
            img = os.path.join(tmp, "template.png")
            with open(img, "wb") as f:
                f.write(PNG_1X1)
            result = run_vision_ingestion(
                img, "请分析模板版式", provider=FakeProvider(),
                enabled=True, providers=["fake"],
            )
            self.assertTrue(result["ok"])
            self.assertTrue(result["schema_valid"])
            self.assertEqual(result["route"]["strategy"], "vision")
            self.assertEqual(result["media_type"], "image")
            self.assertEqual(result["skill"], "vision_understanding")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_missing_file_normalized(self):
        result = run_vision_ingestion(
            "missing.png", "分析", provider=FakeProvider(),
            enabled=True, providers=["fake"],
        )
        self.assertFalse(result["ok"])
        self.assertTrue(result["schema_valid"])
        self.assertIn("error", result["metadata"] if "metadata" in result else {})


if __name__ == "__main__":
    unittest.main()