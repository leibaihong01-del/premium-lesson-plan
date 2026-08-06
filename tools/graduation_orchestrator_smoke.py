# -*- coding: utf-8 -*-
"""汪子涵四件套统一链路验证：调用 Skill Orchestrator 并输出三份报告。"""
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core"))

from student_profile import StudentProfile
from graduation_skill_orchestrator import GraduationSkillOrchestrator

COURSEAGENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = os.path.dirname(COURSEAGENT)
WS = os.path.join(PROJECT, "毕业设计智能制作工作区")
DIRECTION = "02_屏蔽门系统"
STUDENT = "汪子涵"
INFO = os.path.join(WS, "03_需要修改文件整理", DIRECTION, STUDENT, "学生信息.json")
DOCS_DIR = os.path.join(COURSEAGENT, "docs", "v0.7", "SkillOrchestrator")
PACKAGE = os.path.join(WS, "06_输出成果", DIRECTION, STUDENT + "_毕业设计完整成果包")
PROCESS = os.path.join(PACKAGE, "_过程记录")


def main():
    with open(INFO, encoding="utf-8") as f:
        info = json.load(f)
    profile = StudentProfile.from_dict({
        "school": "长沙轨道交通职业学院",
        "college": "轨道车辆学院",
        "major": "城市轨道交通机电技术",
        "class": info["班级"],
        "student_name": info["姓名"],
        "student_id": info["学号"],
        "advisor": info["指导老师"],
        "topic": info["课题名称"],
        "direction": info["方向"],
    })
    orchestrator = GraduationSkillOrchestrator(profile, PROJECT, WS, direction=DIRECTION, regenerate=True)
    orchestrator.run()
    trace_path = orchestrator.write_skill_execution_trace()

    package_report = orchestrator.trace.get("package_validation", {})
    docs = [d for d in orchestrator.trace.get("skills", [])]

    # Skill Integration Report
    lines = []
    lines.append("# Skill Integration Report")
    lines.append("")
    lines.append("- 学生：汪子涵")
    lines.append("- 调度层：GraduationSkillOrchestrator")
    lines.append("- 旧 Skill：未修改")
    lines.append("")
    lines.append("## Skill 执行状态")
    lines.append("")
    lines.append("| Skill | 状态 |")
    lines.append("|---|---|")
    for d in docs:
        lines.append("| %s | %s |" % (d["name"], d["status"]))
    lines.append("")
    lines.append("## 包级验证")
    lines.append("")
    lines.append("- package_status：%s" % package_report.get("package_status"))
    lines.append("- consistency：%s" % package_report.get("checks", {}).get("consistency"))
    lines.append("- template：%s" % package_report.get("checks", {}).get("template"))
    lines.append("- experience_trace：%s" % package_report.get("checks", {}).get("experience_trace"))
    lines.append("- file_integrity：%s" % package_report.get("checks", {}).get("file_integrity"))
    integration_path = os.path.join(DOCS_DIR, "Skill Integration Report.md")
    with open(integration_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # Graduation Pipeline Trace
    plines = []
    plines.append("# Graduation Pipeline Trace")
    plines.append("")
    plines.append("```text")
    plines.append("学生输入（汪子涵）")
    plines.append("↓")
    plines.append("GraduationSkillOrchestrator")
    plines.append("↓")
    for d in docs:
        plines.append("%s（%s）" % (d["name"], d["status"]))
    plines.append("↓")
    plines.append("Document Package Manager")
    plines.append("↓")
    plines.append("Package Validator")
    plines.append("↓")
    plines.append("Experience Trace")
    plines.append("```")
    plines.append("")
    plines.append("执行文件：%s" % trace_path)
    pipeline_path = os.path.join(DOCS_DIR, "Graduation Pipeline Trace.md")
    with open(pipeline_path, "w", encoding="utf-8") as f:
        f.write("\n".join(plines))

    # V0.7.1 closed loop report
    rlines = []
    rlines.append("# V0.7.1 闭环验证报告")
    rlines.append("")
    rlines.append("- 学生：汪子涵")
    rlines.append("- 目标：验证已有 Skill 是否进入统一生产链路")
    rlines.append("")
    rlines.append("## 结果")
    rlines.append("")
    rlines.append("- Skill 执行：%s" % ("全部执行" if all(d["status"] == "executed" for d in docs) else "存在未执行"))
    rlines.append("- 包级状态：%s" % package_report.get("package_status"))
    rlines.append("- 经验 Trace：%s" % package_report.get("checks", {}).get("experience_trace"))
    rlines.append("")
    rlines.append("## 可生产 Skill")
    rlines.append("")
    for d in docs:
        if d["status"] == "executed":
            rlines.append("- %s：生产可用" % d["name"])
    rlines.append("")
    rlines.append("## 半成品")
    rlines.append("")
    rlines.append("- 结果 Skill 的正式重构器 result_reference_builder 仍未作为唯一入口，本次由调度层组装固定页；")
    rlines.append("- ARKM 与 Result Quality Memory 仍为 missing 状态。")
    rlines.append("")
    rlines.append("## 下一步")
    rlines.append("")
    rlines.append("- 收敛：将本次链路固化为生产模板；")
    rlines.append("- 课程建设方向：复用同一 StudentProfile + Orchestrator + Package Validator。")
    closed_path = os.path.join(DOCS_DIR, "V0.7.1闭环验证报告.md")
    with open(closed_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rlines))

    for src in (integration_path, pipeline_path, closed_path):
        shutil.copy2(src, os.path.join(PROCESS, os.path.basename(src)))

    print(json.dumps({
        "skills": docs,
        "package_status": package_report.get("package_status"),
        "trace": trace_path,
        "reports": [integration_path, pipeline_path, closed_path],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())