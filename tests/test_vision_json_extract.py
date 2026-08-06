# -*- coding: utf-8 -*-
"""Vision JSON 提取解析测试。"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from providers.vision.schema import extract_json_text


class TestJsonExtract(unittest.TestCase):
    def test_fenced_json(self):
        text = '```json\n{"a": 1}\n```'
        self.assertEqual(extract_json_text(text), {"a": 1})

    def test_plain_json(self):
        self.assertEqual(extract_json_text('{"a": 1}'), {"a": 1})

    def test_non_json_returns_text(self):
        self.assertEqual(extract_json_text("hello"), "hello")


if __name__ == "__main__":
    unittest.main()