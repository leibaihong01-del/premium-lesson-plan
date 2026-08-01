# -*- coding: utf-8 -*-
"""评测入口：规则基线评测，产出报告与失败案例。"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.translator import parse
from evaluation.metrics import evaluate


def run_baseline(cases_path=None, reports_dir=None):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cases_path = cases_path or os.path.join(root, "evaluation", "cases", "translator_cases.json")
    reports_dir = reports_dir or os.path.join(root, "evaluation", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    with open(cases_path, encoding="utf-8") as f:
        data = json.load(f)
    version = data["version"]
    results, failures = [], []
    for case in data["cases"]:
        spec = parse(case["input"], None)
        score = evaluate(spec, case["expected"], case["input"],
                         output_text=json.dumps(spec, ensure_ascii=False),
                         latency_ms=0.0)
        results.append({"id": case["id"], "spec": spec, "metrics": score})
        if not score["pass"]:
            failures.append({"id": case["id"], "input": case["input"], "metrics": score,
                             "got": {k: spec.get(k) for k in ("intent", "domains", "quality", "constraints", "deliverables")}})
    passed = sum(1 for r in results if r["metrics"]["pass"])
    summary = {
        "version": version,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(results),
        "passed": passed,
        "pass_rate": round(passed / len(results), 4) if results else 0,
        "avg": {
            "content": round(sum(r["metrics"]["content"] for r in results) / len(results), 4) if results else 0,
            "structure": round(sum(r["metrics"]["structure"] for r in results) / len(results), 4) if results else 0,
            "task_match": round(sum(r["metrics"]["task_match"] for r in results) / len(results), 4) if results else 0,
            "cost": round(sum(r["metrics"]["cost"]["cost"] for r in results), 6) if results else 0,
        },
    }
    report = {"summary": summary, "results": results, "failures": failures}
    json_path = os.path.join(reports_dir, f"translator_rule_baseline_v{version}.json")
    md_path = os.path.join(reports_dir, f"translator_rule_baseline_v{version}.md")
    fail_path = os.path.join(reports_dir, f"failures_v{version}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    with open(fail_path, "w", encoding="utf-8") as f:
        json.dump(failures, f, ensure_ascii=False, indent=2)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Translator 规则基线评测报告\n\n")
        f.write(f"案例版本：v{version}    时间：{summary['timestamp']}\n\n")
        f.write(f"通过率：{summary['passed']}/{summary['total']}（{summary['pass_rate']}）\n\n")
        f.write("| 指标 | 值 |\n|---|---|\n")
        f.write(f"| 内容质量 | {summary['avg']['content']} |\n")
        f.write(f"| 结构完整 | {summary['avg']['structure']} |\n")
        f.write(f"| 任务符合度 | {summary['avg']['task_match']} |\n")
        f.write(f"| 成本估算 | {summary['avg']['cost']} |\n")
        f.write(f"| 失败案例 | {len(failures)} |\n")
    return report, json_path, md_path, fail_path


if __name__ == "__main__":
    report, jp, mp, fp = run_baseline()
    print("PASS", report["summary"]["passed"], "/", report["summary"]["total"],
          "| 报告:", mp, "| 失败:", fp)
