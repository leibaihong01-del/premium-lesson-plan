# -*- coding: utf-8 -*-
"""质量审核 Agent：模板/内容/教学/格式评分并输出 JSON 报告。"""
import json
import os

from modules import content_checker, format_checker


def review(docx_path, template_path, reports_dir, weights=None):
    weights = weights or {"template": 30, "content": 25, "teaching": 25, "format": 20}
    fmt = format_checker.check_format(docx_path, template_path)
    content = content_checker.check_content(docx_path)
    teaching = content_checker.check_teaching(docx_path)
    style = content_checker.check_format_style(docx_path)
    total = round(
        fmt["score"] * weights["template"] / 20
        + content["score"] * weights["content"] / 25
        + teaching["score"] * weights["teaching"] / 25
        + style["score"] * weights["format"] / 20,
        1,
    )
    report = {
        "file": os.path.basename(docx_path),
        "template_score": round(fmt["score"] * weights["template"] / 20, 1),
        "content_score": round(content["score"] * weights["content"] / 25, 1),
        "teaching_score": round(teaching["score"] * weights["teaching"] / 25, 1),
        "format_score": round(style["score"] * weights["format"] / 20, 1),
        "total_score": total,
        "final": "PASS" if total >= 95 else "REPAIR_REQUIRED",
        "checks": {
            "template": fmt["checks"],
            "content": content["checks"],
            "teaching": teaching["checks"],
            "format": style["checks"],
        },
        "issues": {
            "template": fmt["issues"],
            "content": content["issues"],
            "teaching": teaching["issues"],
            "format": style["issues"],
        },
    }
    os.makedirs(reports_dir, exist_ok=True)
    with open(os.path.join(reports_dir, "quality_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    with open(os.path.join(reports_dir, "quality_report.md"), "w", encoding="utf-8") as f:
        f.write("# 质量评分报告\n\n")
        f.write("| 维度 | 得分 |\n|---|---|\n")
        f.write(f"| 模板符合度（30） | {report['template_score']} |\n")
        f.write(f"| 内容完整度（25） | {report['content_score']} |\n")
        f.write(f"| 教学专业度（25） | {report['teaching_score']} |\n")
        f.write(f"| 格式规范度（20） | {report['format_score']} |\n")
        f.write(f"| 综合质量 | **{total}** |\n\n")
        f.write(f"结论：{report['final']}\n")
    return report
