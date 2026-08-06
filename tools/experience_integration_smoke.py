# -*- coding: utf-8 -*-
"""P1 验证工具：ExperienceLoader + StudentProfile + 双 Trace（默认关闭，仅显式开启时加载）。"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core"))

from core.experience_loader import ExperienceLoader
from core.experience_trace import build_experience_trace, write_experience_trace
from core.generation_trace import build_generation_trace, write_generation_trace
from core.student_profile import StudentProfile

COURSEAGENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = os.path.dirname(COURSEAGENT)
TRACE_DIR = os.path.join(COURSEAGENT, "output", "experience_traces")
TASK_ID = "p1_smoke_20260804"

DOC_TYPES = [
    ("task_book", "TaskBookSkill"),
    ("result", "ResultAgent"),
    ("evaluation_form", "EvaluationFormSkill"),
    ("defense_record", "DefenseRecordSkill"),
]


def main():
    # 默认配置应为关闭
    default_loader = ExperienceLoader()
    print("default_enabled=", default_loader.enabled)
    assert default_loader.enabled is False

    # 显式开启用于验证真实加载
    loader = ExperienceLoader(enabled=True)
    summary = {}
    audit_lines = ["# Experience Usage Report", "", "| 文档类型 | 经验 | 来源 | 状态 | 加载 | 缺失 |",
                   "|---|---|---|---|---|---|"]
    for doc_type, skill in DOC_TYPES:
        applicable = loader.load(doc_type, template="template://" + doc_type, task_context={"task_id": TASK_ID})
        applicable["task_id"] = TASK_ID
        exp_trace = build_experience_trace(applicable, skill, TASK_ID)
        gen_trace = build_generation_trace(applicable, skill, applicable.get("template"), final_validation="P1_trace_only")
        exp_path = os.path.join(TRACE_DIR, "experience_trace_%s.json" % doc_type)
        gen_path = os.path.join(TRACE_DIR, "generation_trace_%s.json" % doc_type)
        write_experience_trace(exp_path, exp_trace)
        write_generation_trace(gen_path, gen_trace)
        summary[doc_type] = {
            "enabled": applicable["enabled"],
            "loaded_count": applicable["loaded_count"],
            "missing_count": applicable["missing_count"],
            "experiences": [
                {"id": e["experience_id"], "loaded": e["loaded"], "missing": e["missing_files"]}
                for e in applicable["experiences"]
            ],
            "experience_trace": exp_path,
            "generation_trace": gen_path,
        }
        for e in applicable["experiences"]:
            status = e["status"]
            loaded = "是" if e["loaded"] else "否"
            missing = "、".join(e["missing_files"]) if e["missing_files"] else "无"
            audit_lines.append("| %s | %s | %s | %s | %s | %s |" % (
                doc_type, e["name"], (e["source_files"] or ["（未创建）"])[0], status, loaded, missing))

    # StudentProfile 验证
    profile = StudentProfile.from_dict({
        "school": "长沙轨道交通职业学院",
        "college": "轨道车辆学院",
        "major": "城市轨道交通机电技术",
        "class": "24级机电技术2班",
        "student_name": "陈家宝",
        "student_id": "202421044719",
        "advisor": "瞿曌",
        "topic": "橘子洲南站自动扶梯扶手带检修方案设计",
        "direction": "电梯系统",
    })
    missing = profile.validate()
    summary["student_profile"] = {"name": profile.student_name, "missing": missing}

    audit_lines.append("")
    audit_lines.append("## Student Profile")
    audit_lines.append("- 姓名：%s" % profile.student_name)
    audit_lines.append("- 缺失字段：%s" % ("、".join(missing) if missing else "无"))
    audit_path = os.path.join(TRACE_DIR, "experience_usage_report.md")
    with open(audit_path, "w", encoding="utf-8") as f:
        f.write("\n".join(audit_lines))

    with open(os.path.join(TRACE_DIR, "smoke_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("TRACE_DIR=", TRACE_DIR)
    return 0


if __name__ == "__main__":
    sys.exit(main())