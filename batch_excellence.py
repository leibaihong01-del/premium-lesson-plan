# -*- coding: utf-8 -*-
"""批量精品课程五维诊断。"""
import argparse
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.excellence_engine import analyze


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "精品提升建议报告.md"))
    args = ap.parse_args()
    files = [f for f in sorted(glob.glob(os.path.join(args.dir, "*.docx")))
             if ("教案（第" in os.path.basename(f) or "教案样板（第" in os.path.basename(f) or "实训教案" in os.path.basename(f)) and "优化版" in f]
    rows = [analyze(f) for f in files]
    lines = ["# 精品提升建议报告", "", f"文件数：{len(rows)}", ""]
    lines.append("| 文件 | 教学逻辑25 | 内容体系25 | 职业特色20 | 创新设计15 | 评价体系15 | 总分 | 等级 |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for r in rows:
        d = r["dimensions"]
        lines.append(f"| {os.path.basename(r['file'])} | {d['教学逻辑']} | {d['内容体系']} | {d['职业特色']} | {d['创新设计']} | {d['评价体系']} | {r['total']} | {r['level']} |")
    lines.append("")
    lines.append("## 主要提升建议")
    for r in rows:
        if r["suggestions"]:
            lines.append(f"- {os.path.basename(r['file'])}：")
            for dim, sug in r["suggestions"].items():
                lines.append(f"  - {dim}：{sug}")
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("报告:", args.out, "| 文件数:", len(rows))


if __name__ == "__main__":
    main()
