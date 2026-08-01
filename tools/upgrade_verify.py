# -*- coding: utf-8 -*-
"""L2规则验证自动化：按知识更新证据核验待验证规则。"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.memory import Memory


def main():
    m = Memory()
    rules = m._load("rules")
    rules = rules if isinstance(rules, list) else []
    updates = m._load("knowledge_updates")
    updates = updates if isinstance(updates, list) else []
    domains = {u.get("domain") for u in updates}
    lines = ["# 升级验证报告", "", f"时间：{time.strftime('%Y-%m-%d %H:%M:%S')}", ""]
    lines.append("| 规则 | 级别 | 验证前 | 验证后 | 证据 |")
    lines.append("|---|---|---|---|---|")
    for r in rules:
        if r.get("approval") != "pending_verify":
            continue
        rule_text = r.get("rule", "")
        evidence = next((u.get("title") for u in updates if u.get("domain") in rule_text), "")
        if evidence:
            r["approval"] = "verified"
            r["verified_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            status = "verified"
        else:
            status = "no_evidence"
        lines.append(f"| {rule_text} | {r.get('level')} | pending_verify | {status} | {evidence or '无'}")
    m._save("rules", rules)
    lines.append("")
    lines.append("结论：verified 规则可参与自动执行；no_evidence 规则保持待验证。")
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "升级验证报告.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("报告:", out)


if __name__ == "__main__":
    main()
