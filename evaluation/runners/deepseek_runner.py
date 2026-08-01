# -*- coding: utf-8 -*-
"""DeepSeek 独立评测 runner（5.2-E 小范围验证）。

对比模式：
- rule：规则 Translator 输出；
- hybrid：规则通过则用规则，否则启用 LLM 增强；
- deepseek：强制 DeepSeek 增强，不可用时自动回退规则并标记。

不使用 DeepSeek 自评；统一用 evaluation.metrics 规则评分。
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.translator import parse, translate_with_enhancement
from evaluation.metrics import evaluate


def _load_cases(cases_path):
    with open(cases_path, encoding="utf-8-sig") as f:
        return json.load(f)


def run_verification(cases_path=None, reports_dir=None, adapter=None, llm_enabled=False):
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    cases_path = cases_path or os.path.join(root, "evaluation", "cases", "translator_external_v1.0.json")
    reports_dir = reports_dir or os.path.join(root, "evaluation", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    data = _load_cases(cases_path)
    version = data.get("version", "external-v1.0")
    modes = {"rule": [], "hybrid": [], "deepseek": []}
    for case in data["cases"]:
        inp = case["input"]
        expected = case["expected"]
        rule = parse(inp, None)
        rule_score = evaluate(rule, expected, inp, "", 0.0)
        modes["rule"].append({"id": case["id"], "metrics": rule_score})

        if rule_score["pass"]:
            hybrid = rule
        else:
            hybrid, _, _ = translate_with_enhancement(inp, None, adapter, enabled=llm_enabled)
        modes["hybrid"].append({"id": case["id"], "metrics": evaluate(hybrid, expected, inp, "", 0.0)})

        ds, route, enhanced = translate_with_enhancement(inp, None, adapter, enabled=llm_enabled)
        ds_score = evaluate(ds, expected, inp, "", 0.0)
        ds_score["enhanced"] = enhanced
        ds_score["route"] = route
        modes["deepseek"].append({"id": case["id"], "metrics": ds_score})

    summary = {}
    failures = {}
    for mode, items in modes.items():
        passed = sum(1 for it in items if it["metrics"]["pass"])
        summary[mode] = {
            "total": len(items),
            "passed": passed,
            "pass_rate": round(passed / len(items), 4),
            "avg_content": round(sum(it["metrics"]["content"] for it in items) / len(items), 4),
            "avg_structure": round(sum(it["metrics"]["structure"] for it in items) / len(items), 4),
            "avg_task_match": round(sum(it["metrics"]["task_match"] for it in items) / len(items), 4),
        }
        failures[mode] = [it["id"] for it in items if not it["metrics"]["pass"]]

    usage = getattr(adapter, "usage", None)
    report = {
        "version": version,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "note": "外部独立案例；规则指标评分，不依赖LLM自评；DeepSeek模式不可用时自动回退规则",
        "llm_enabled": llm_enabled,
        "summary": summary,
        "failures": failures,
        "adapter_usage": usage,
    }
    md = os.path.join(reports_dir, f"translator_external_verification_{version}.md")
    js = os.path.join(reports_dir, f"translator_external_verification_{version}.json")
    with open(md, "w", encoding="utf-8") as f:
        f.write("# Translator 外部独立案例评测报告\n\n")
        f.write(f"案例版本：{version}    时间：{report['timestamp']}\n\n")
        f.write("| 模式 | 通过率 | 内容质量 | 结构完整 | 任务符合度 | 失败 |\n|---|---|---|---|---|---|\n")
        for mode, s in summary.items():
            f.write(f"| {mode} | {s['passed']}/{s['total']} | {s['avg_content']} | {s['avg_structure']} | {s['avg_task_match']} | {len(failures[mode])} |\n")
        f.write(f"\n说明：{report['note']}\n")
        if usage:
            f.write(f"\nAdapter 用量：{json.dumps(usage, ensure_ascii=False)}\n")
    with open(js, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return report, md, js


if __name__ == "__main__":
    report, md, js = run_verification()
    for mode, s in report["summary"].items():
        print(mode, s["passed"], "/", s["total"], "rate", s["pass_rate"])
    print("报告:", md)