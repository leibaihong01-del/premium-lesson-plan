# -*- coding: utf-8 -*-
"""用户画像报告：从偏好、统计与反馈生成用户模型摘要。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.memory import Memory


def main():
    m = Memory()
    up = m._load("user_preferences")
    prefs = up.get("preferences", {})
    model = up.get("user_model", {})
    stats = model.get("stats", {})
    feedback = model.get("feedback", [])
    lines = ["# 用户画像报告", ""]
    lines.append("## 一、偏好")
    lines.append("")
    for k, v in prefs.items():
        lines.append(f"- {k}：{'是' if v is True else v}")
    lines.append("")
    lines.append("## 二、任务统计")
    lines.append("")
    for k, v in stats.items():
        lines.append(f"- {k}：{v}")
    lines.append("")
    lines.append(f"## 三、反馈记录（{len(feedback)}）")
    lines.append("")
    for f in feedback[-10:]:
        lines.append(f"- {f.get('text', '')[:80]}")
    lines.append("")
    lines.append("结论：用户模型已沉淀，需求转译与满意度预测将自动引用。")
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "用户画像报告.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("报告:", out)


if __name__ == "__main__":
    main()
