# -*- coding: utf-8 -*-
"""P3-B 收尾验证：陈家宝成果质量流水线只读回归。"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core"))

from student_profile import StudentProfile
from result_experience_consumer import ResultExperienceConsumer
from document_router import DocumentRouter

COURSEAGENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = os.path.dirname(COURSEAGENT)
WS = os.path.join(PROJECT, "毕业设计智能制作工作区")
DIRECTION = "03_电梯系统"
TOPIC = "橘子洲南站自动扶梯扶手带检修方案设计"
PACKAGE = os.path.join(WS, "06_输出成果", DIRECTION, "陈家宝_毕业设计完整成果包")
PROCESS = os.path.join(PACKAGE, "_过程记录")
OUT_DIR = os.path.join(COURSEAGENT, "output", "p3b_chenjiabao")
TEMPLATE = os.path.join(WS, "02_模板文件", "02 杨振海 毕业设计成果 黄兴南路站AFC闸机设备检修方案设计.docx")
RESULT = os.path.join(PACKAGE, "02 陈家宝 毕业设计成果 %s.docx" % TOPIC)
RESULT_PDF = os.path.join(PROCESS, "02 陈家宝 毕业设计成果 %s.pdf" % TOPIC)
TASKBOK = os.path.join(PACKAGE, "01 陈家宝 毕业设计任务书 %s.docx" % TOPIC)
TEMPLATE_PDF = os.path.join(OUT_DIR, "template_render.pdf")
INFO = os.path.join(WS, "03_需要修改文件整理", DIRECTION, "陈家宝", "学生信息.json")


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(INFO, encoding="utf-8") as f:
        info = json.load(f)
    profile = StudentProfile.from_dict({
        "school": "长沙轨道交通职业学院",
        "college": "轨道车辆学院",
        "major": "城市轨道车辆应用技术",
        "class": info["班级"],
        "student_name": info["姓名"],
        "student_id": info["学号"],
        "advisor": info["指导老师"],
        "topic": info["课题名称"],
        "direction": info["方向"],
    })

    if not os.path.isfile(TEMPLATE_PDF):
        sys.path.insert(0, os.path.join(WS, "00_系统配置", "模块", "v06"))
        from render_docx import render_to_pdf
        ok = render_to_pdf(TEMPLATE, TEMPLATE_PDF)
        print("TEMPLATE_RENDER_OK=", ok)

    consumer = ResultExperienceConsumer(enabled=True)
    context = consumer.build_context(info["姓名"], "02 杨振海 毕业设计成果 黄兴南路站AFC闸机设备检修方案设计.docx")

    router = DocumentRouter()
    pipeline = router.build_result_pipeline(output_dir=OUT_DIR)
    before = sha256(RESULT)

    result = pipeline.run(
        profile=profile,
        document_path=RESULT,
        pdf_path=RESULT_PDF,
        template_path=TEMPLATE,
        
        taskbook_path=TASKBOK,
        experience_context=context,
    )

    after = sha256(RESULT)
    unchanged = before == after
    print("UNCHANGED=", unchanged)
    print("QUALITY_STATUS=", result["quality_status"])
    print("TRACE=", os.path.join(OUT_DIR, "quality_pipeline_trace.json"))
    print(json.dumps({
        "quality_status": result["quality_status"],
        "content": result["result_quality_report"]["reports"]["content"]["status"],
        "structure": result["result_quality_report"]["reports"]["structure"]["status"],
        "layout": result["result_quality_report"]["reports"]["layout"]["status"],
        "reference": result["reference_quality_report"]["status"],
        "academic": result["academic_requirement_report"]["status"],
        "revision_actions": len(result["revision_plan"]["actions"]),
        "checked_items": result["result_quality_report"]["checked_items"],
        "passed": result["result_quality_report"]["passed"],
        "failed": result["result_quality_report"]["failed"],
        "review": result["result_quality_report"]["review"],
        "unchanged": unchanged,
    }, ensure_ascii=False, indent=2))
    assert unchanged
    return 0


if __name__ == "__main__":
    sys.exit(main())