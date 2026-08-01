# -*- coding: utf-8 -*-
"""L3升级人工审批：列表、批准、驳回。"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.memory import Memory


def main():
    ap = argparse.ArgumentParser(description="L3升级审批")
    ap.add_argument("action", choices=["list", "approve", "reject"])
    ap.add_argument("--id", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--reason", default="人工审核通过")
    args = ap.parse_args()
    m = Memory()
    rules = m._load("rules")
    rules = rules if isinstance(rules, list) else []
    if args.action == "list":
        print("=== 规则审批状态 ===")
        for r in rules:
            rid = r.get("id", "")
            if r.get("approval") in ("pending_approval", "pending_verify", "verified"):
                print(f"{rid} | {r.get('level')} | {r.get('approval')} | {r.get('rule', '')[:60]}")
        return
    targets = rules if args.all else [r for r in rules if r.get("id") == args.id]
    for r in targets:
        if args.action == "approve":
            r["approval"] = "approved"
            r["approved_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            r["reason"] = args.reason
        else:
            r["approval"] = "rejected"
            r["rejected_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            r["reason"] = args.reason
    m._save("rules", rules)
    print("处理完成:", args.action, "数量:", len(targets))
    lines = ["# 升级审批记录", "", f"时间：{time.strftime('%Y-%m-%d %H:%M:%S')}", ""]
    lines.append("| 级别 | 规则 | 状态 |")
    lines.append("|---|---|---|")
    for r in rules:
        lines.append(f"| {r.get('level')} | {r.get('rule', '')[:60]} | {r.get('approval')} |")
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "升级审批记录.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("记录:", out)


if __name__ == "__main__":
    main()
