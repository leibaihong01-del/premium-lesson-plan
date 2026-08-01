# -*- coding: utf-8 -*-
"""Mock LLM Evaluation Harness（模拟模型测试框架）。

用途：验证 Evaluation 框架能否比较不同输出，不证明“模拟LLM有效”。
未来：用 DeepSeekAdapter 替换 simulate_llm 即可。
"""
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.translator import parse
from evaluation.metrics import evaluate


PATCHES = [
    ("32学时", {"constraints": ["32学时"]}),
    ("教案封面", {"domains": ["教案封面"], "deliverables": ["教案封面"], "constraints": ["课程、专业信息"]}),
    ("评分≥95", {"quality": "formal", "constraints": ["评分≥95"]}),
    ("覆盖全部项目", {"constraints": ["覆盖全部项目"]}),
    ("安全交底、步骤、记录表", {"constraints": ["安全交底、步骤、记录表"]}),
    ("申报书结构", {"constraints": ["申报书结构"]}),
    ("与教案一致", {"constraints": ["与教案一致"]}),
]


def simulate_llm(input_text, base_spec, prompt_template=""):
    """确定性模拟LLM：基于规则补充转译缺口；真实LLM接入后替换本函数。"""
    spec = dict(base_spec)
    spec["domains"] = list(base_spec.get("domains", []))
    spec["deliverables"] = list(base_spec.get("deliverables", []))
    spec["constraints"] = list(base_spec.get("constraints", []))
    for kw, patch in PATCHES:
        if kw in input_text:
            for d in patch.get("domains", []):
                if d not in spec["domains"]:
                    spec["domains"].append(d)
            for d in patch.get("deliverables", []):
                if d not in spec["deliverables"]:
                    spec["deliverables"].append(d)
            if "quality" in patch:
                spec["quality"] = patch["quality"]
            for c in patch.get("constraints", []):
                if c not in spec["constraints"]:
                    spec["constraints"].append(c)
    spec["llm_source"] = "simulated"
    return spec


def prompt_version():
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                     "prompts", "manifest.yaml")
    text = ""
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            text = f.read()
    m = re.search(r"version:\s*[\"']?([0-9.]+)", text)
    return m.group(1) if m else "unknown"


def run_mock_comparison(cases_path=None, reports_dir=None):
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    cases_path = cases_path or os.path.join(root, "evaluation", "cases", "translator_cases.json")
    reports_dir = reports_dir or os.path.join(root, "evaluation", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    with open(cases_path, encoding="utf-8-sig") as f:
        data = json.load(f)
    version = data["version"]
    with open(os.path.join(root, "prompts", "translator", "user_template.json"), encoding="utf-8-sig") as f:
        template = json.load(f)["template"]
    modes = {"rule": [], "llm": [], "hybrid": []}
    for case in data["cases"]:
        inp = case["input"]
        rule = parse(inp, None)
        llm = simulate_llm(inp, rule, template)
        hybrid = llm if not evaluate(rule, case["expected"], inp, "", 0)["pass"] else rule
        modes["rule"].append({"id": case["id"], "metrics": evaluate(rule, case["expected"], inp, "", 0)})
        modes["llm"].append({"id": case["id"], "metrics": evaluate(llm, case["expected"], inp, "", 0)})
        modes["hybrid"].append({"id": case["id"], "metrics": evaluate(hybrid, case["expected"], inp, "", 0)})

    summary = {}
    failures = {}
    for mode, items in modes.items():
        passed = sum(1 for it in items if it["metrics"]["pass"])
        summary[mode] = {
            "total": len(items), "passed": passed,
            "pass_rate": round(passed / len(items), 4),
            "avg_content": round(sum(it["metrics"]["content"] for it in items) / len(items), 4),
            "avg_structure": round(sum(it["metrics"]["structure"] for it in items) / len(items), 4),
            "avg_task_match": round(sum(it["metrics"]["task_match"] for it in items) / len(items), 4),
        }
        failures[mode] = [it["id"] for it in items if not it["metrics"]["pass"]]

    report = {
        "version": version, "prompt_version": prompt_version(),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "note": "Mock LLM Evaluation Harness：仅验证Evaluation比较框架；真实DeepSeek接入后替换simulate_llm",
        "summary": summary, "failures": failures,
    }
    md = os.path.join(reports_dir, f"translator_mock_comparison_v{version}.md")
    js = os.path.join(reports_dir, f"translator_mock_comparison_v{version}.json")
    with open(md, "w", encoding="utf-8") as f:
        f.write("# Translator Mock 对比报告（Evaluation框架验证）\n\n")
        f.write(f"案例版本 v{version}    Prompt版本 v{report['prompt_version']}\n\n")
        f.write("| 模式 | 通过率 | 内容质量 | 结构完整 | 任务符合度 | 失败 |\n|---|---|---|---|---|---|\n")
        for mode, s in summary.items():
            f.write(f"| {mode} | {s['passed']}/{s['total']} | {s['avg_content']} | {s['avg_structure']} | {s['avg_task_match']} | {len(failures[mode])} |\n")
        f.write(f"\n说明：{report['note']}\n")
    with open(js, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return report, md, js


if __name__ == "__main__":
    report, md, js = run_mock_comparison()
    for mode, s in report["summary"].items():
        print(mode, s["passed"], "/", s["total"], "rate", s["pass_rate"])
    print("报告:", md)
