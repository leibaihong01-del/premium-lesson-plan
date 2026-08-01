# -*- coding: utf-8 -*-
"""阶段5.1-B 评测指标与基线评测测试。"""
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.translator import parse
from evaluation.metrics import content_score, cost_estimate, evaluate, structure_score, task_match
from evaluation.run_evaluation import run_baseline


class TestMetrics(unittest.TestCase):
    def test_exact_match(self):
        spec = {"intent": "optimize", "domains": ["课程标准"], "quality": "excellent",
                "deliverables": ["课程标准"], "constraints": ["禁止：设备维修"], "compute_hint": []}
        expected = {"intent": "optimize", "domains": ["课程标准"], "quality": "excellent",
                    "deliverables": ["课程标准"], "constraints": ["禁止：设备维修"]}
        self.assertEqual(content_score(spec, expected), 1.0)
        self.assertEqual(structure_score(spec), 1.0)
        self.assertEqual(task_match(spec, expected), 1.0)

    def test_structure_missing_key(self):
        self.assertEqual(structure_score({"intent": "x"}), 0.0)

    def test_task_match_fail(self):
        spec = {"intent": "generate", "domains": ["课程标准"], "quality": "excellent",
                "deliverables": [], "constraints": [], "compute_hint": []}
        expected = {"intent": "optimize", "domains": ["课程标准"], "quality": "excellent"}
        self.assertEqual(task_match(spec, expected), 0.0)

    def test_cost_estimate(self):
        c = cost_estimate("课程建设任务" * 10)
        self.assertGreater(c["input_tokens"], 0)

    def test_evaluate_rule_based_no_llm(self):
        spec = parse("请优化课程标准，按精品要求，禁止设备维修，输出审核报告", None)
        expected = {"intent": "optimize", "domains": ["课程标准"], "quality": "excellent",
                    "constraints": ["禁止：设备维修", "输出审核报告并闭环"], "deliverables": ["课程标准"]}
        score = evaluate(spec, expected, "输入", "输出")
        self.assertIn("pass", score)

    def test_run_baseline_writes_reports(self):
        tmp = tempfile.mkdtemp(prefix="eval_")
        try:
            report, jp, mp, fp = run_baseline(reports_dir=tmp)
            self.assertTrue(os.path.exists(jp))
            self.assertTrue(os.path.exists(mp))
            self.assertTrue(os.path.exists(fp))
            self.assertEqual(report["summary"]["total"], 10)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
