# -*- coding: utf-8 -*-
"""Skill审计：列出已注册能力单元并运行抽样验证。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.memory import Memory
from core.skill_factory import build_defaults


def main():
    m = Memory()
    reg = build_defaults(m)
    lines = ["# Skill审计报告", "", f"已注册Skill：{len(reg.list_skills())}", ""]
    lines.append("| Skill | 状态 |")
    lines.append("|---|---|")
    for name in reg.list_skills():
        lines.append(f"| {name} | ✅ 已注册 |")
    lines.append("")
    sample = r"D:\Users\leibaihong\Desktop\课程材料优化\城市轨道交通概论智能课程建设\05_输出文件\《城市轨道交通概论》-教案（第1课）优化版.docx"
    tpl = r"D:\Users\leibaihong\Desktop\课程材料优化\城市轨道交通概论智能课程建设\01_模板文件\教案模板.docx"
    lines.append("## 抽样验证")
    lines.append("")
    r = reg.run("分析Skill", {"docx": sample})
    lines.append(f"- 分析Skill：{r['evaluation']['score']} PASS={r['evaluation']['passed']}")
    r = reg.run("知识Skill", {"domain": "AI技术", "title": "生成式AI应用", "summary": "新技术 用于教案生成"})
    lines.append(f"- 知识Skill：影响分析={r['output'].get('impact')}")
    r = reg.run("竞赛Skill", {"capability": "competition_plan", "request": "生成精品比赛方案",
                              "course": "城市轨道交通概论", "major": "城市轨道交通通信信号技术",
                              "topic": "轨道交通系统组成认知", "name": "审计"})
    lines.append(f"- 竞赛Skill：{r['evaluation']['score']} PASS={r['evaluation']['passed']}")
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "Skill审计报告.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Skills:", reg.list_skills())
    print("报告:", out)


if __name__ == "__main__":
    main()
