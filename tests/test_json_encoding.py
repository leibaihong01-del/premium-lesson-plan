# -*- coding: utf-8 -*-
"""JSON 编码兼容测试：UTF-8 与 UTF-8 BOM 均可加载且结果一致。"""
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA = {"version": "1.0", "items": [{"id": "A"}]}


def load_json(path):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


class TestJsonEncoding(unittest.TestCase):
    def test_utf8_and_bom_load_identically(self):
        tmp = tempfile.mkdtemp(prefix="json_enc_")
        try:
            plain = os.path.join(tmp, "plain.json")
            bom = os.path.join(tmp, "bom.json")
            text = json.dumps(DATA, ensure_ascii=False)
            with open(plain, "w", encoding="utf-8") as f:
                f.write(text)
            with open(bom, "w", encoding="utf-8-sig") as f:
                f.write(text)
            self.assertEqual(load_json(plain), DATA)
            self.assertEqual(load_json(bom), DATA)
            self.assertEqual(load_json(plain), load_json(bom))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()