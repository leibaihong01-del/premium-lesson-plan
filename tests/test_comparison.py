# -*- coding: utf-8 -*-
"""阶段5.2 对比评测测试。"""
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evaluation.run_comparison import run_comparison


class TestComparison(unittest.TestCase):
    def test_comparison_runs_and_reports(self):
        tmp = tempfile.mkdtemp(prefix="cmp_")
        try:
            report, md, js = run_comparison(reports_dir=tmp)
            self.assertTrue(os.path.exists(md))
            self.assertTrue(os.path.exists(js))
            self.assertEqual(report["summary"]["rule"]["total"], 10)
            self.assertGreaterEqual(report["summary"]["llm"]["pass_rate"],
                                    report["summary"]["rule"]["pass_rate"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
