# -*- coding: utf-8 -*-
"""L2/L3 可控升级审核：列出待验证/待审批规则并生成审核报告。"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.memory import Memory


def main():
    m = Memory()
    rules = m._load("rules")
    rules = rules if isinstance(rules, list) else []
    pending = [r for r in rules if r.get("approval") in ("pending_verify", "pending_approval")]
    lines = ["# 升级审核报告", "", f"时间：{time.strftime('%Y-%m-%d %H:%M:%S')}", ""]
    lines.append("## 待审核规则")
    lines.append("")
    lines.append("| 级别 | 规则 | 审批状态 |")
    lines.append("|---|---|---|")
    for r in pending:
        lines.append(f"| {r.get('level')} | {r.get('rule')} | {r.get('approval')} |")
    lines.append("")
    lines.append("## 处理建议")
    lines.append("")
    lines.append("1. L2 规则需在小样本任务中验证后再生效；")
    lines.append("2. L3 规则涉及架构/核心代码，必须人工确认；")
    lines.append("3. 未确认规则不参与自动执行。")
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "升级审核报告.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("待审核规则:", len(pending), "| 报告:", out)


if __name__ == "__main__":
    main()
