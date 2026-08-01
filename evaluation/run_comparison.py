# -*- coding: utf-8 -*-
"""兼容入口：转发到 Mock LLM Evaluation Harness。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evaluation.runners.mock_llm_runner import prompt_version, run_mock_comparison as run_comparison, simulate_llm

__all__ = ["prompt_version", "run_comparison", "simulate_llm"]


if __name__ == "__main__":
    report, md, js = run_comparison()
    for mode, s in report["summary"].items():
        print(mode, s["passed"], "/", s["total"], "rate", s["pass_rate"])
    print("报告:", md)
