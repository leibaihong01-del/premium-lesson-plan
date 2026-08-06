# -*- coding: utf-8 -*-
"""汪子涵 ResultSkillRunner 单项验证（不运行四件套）。"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core"))

from graduation_skill_runners import ResultSkillRunner
from student_profile import StudentProfile

COURSEAGENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = os.path.dirname(COURSEAGENT)
WS = os.path.join(PROJECT, "毕业设计智能制作工作区")
DIRECTION = "02_屏蔽门系统"
STUDENT = "汪子涵"
INFO = os.path.join(WS, "03_需要修改文件整理", DIRECTION, STUDENT, "学生信息.json")
PACKAGE = os.path.join(WS, "06_输出成果", DIRECTION, STUDENT + "_毕业设计完整成果包")
PROCESS = os.path.join(PACKAGE, "_过程记录")
STUDENT_DIR = os.path.join(WS, "03_需要修改文件整理", DIRECTION, STUDENT)


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
    runner = ResultSkillRunner(profile, WS, COURSEAGENT, PROJECT)
    result = runner.run(STUDENT_DIR, PACKAGE, PROCESS)

    trace_path = os.path.join(PROCESS, "experience_trace_result.json")
    with open(trace_path, encoding="utf-8") as f:
        trace = json.load(f)

    print(json.dumps({
        "skill": "ResultSkillRunner",
        "new_result": result.get("output"),
        "pdf": result.get("pdf"),
        "quality_status": result.get("quality", {}).get("quality_status"),
        "experience_trace": trace,
        "call_chain": [
            "StudentProfile",
            "GraduationSkillOrchestrator",
            "ResultSkillRunner",
            "ResultExperienceConsumer",
            "ResultAnalyzer/DocumentStructure",
            "ResultQualityPipeline",
        ],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())