# -*- coding: utf-8 -*-
"""Vision 课程文档生成 Demo 测试。"""
import base64
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.vision_course_demo import run_demo

PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)


class TestVisionCourseDemo(unittest.TestCase):
    def test_mock_demo_generates_template_aware_doc(self):
        tmp = tempfile.mkdtemp(prefix="demo_")
        try:
            img = os.path.join(tmp, "template.png")
            with open(img, "wb") as f:
                f.write(PNG_1X1)
            result = run_demo(img, "生成课程文档", mock=True)
            self.assertTrue(result["ok"])
            self.assertIn("教学目标", result["markdown"])
            self.assertEqual(result["consistency"]["validator"], "vision_consistency")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()