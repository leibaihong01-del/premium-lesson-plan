# -*- coding: utf-8 -*-
"""P2 验证：Document Package Intelligence Layer 全生命周期档案对象。"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core"))

from student_profile import StudentProfile
from document_package_manager import DocumentPackageManager

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WS = os.path.join(os.path.dirname(PROJECT), "毕业设计智能制作工作区")
BASE_OUTPUT = os.path.join(WS, "06_输出成果")
DIRECTION = "03_电梯系统"
TOPIC = "橘子洲南站自动扶梯扶手带检修方案设计"
TRACE_DIR = os.path.join(PROJECT, "output", "experience_traces")

INFO_PATH = os.path.join(WS, "03_需要修改文件整理", DIRECTION, "陈家宝", "学生信息.json")
with open(INFO_PATH, encoding="utf-8") as f:
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
assert not profile.validate(), profile.validate()

PACKAGE_DIR = os.path.join(BASE_OUTPUT, DIRECTION, "陈家宝_毕业设计完整成果包")
PROCESS = os.path.join(PACKAGE_DIR, "_过程记录")
DOCS = {
    "01": ("毕业设计任务书", "01 杨振海 毕业设计任务书 黄兴南路站AFC闸机设备检修方案设计.docx"),
    "02": ("毕业设计成果", "02 杨振海 毕业设计成果 黄兴南路站AFC闸机设备检修方案设计.docx"),
    "03": ("毕业设计成绩评定表", "04 杨振海 毕业设计成绩评定表 黄兴南路站AFC闸机设备检修方案设计.docx"),
    "04": ("毕业设计答辩记录表", "05 杨振海 毕业设计答辩记录表 黄兴南路站AFC闸机设备检修方案设计.docx"),
}

manager = DocumentPackageManager(BASE_OUTPUT, profile, DIRECTION, archive_id="dpil-20260804-chenjiabao")
for code, (doc_type, template_name) in DOCS.items():
    docx = os.path.join(PACKAGE_DIR, "%s 陈家宝 %s %s.docx" % (code, doc_type, TOPIC))
    pdf = os.path.join(PROCESS, "%s 陈家宝 %s %s.pdf" % (code, doc_type, TOPIC))
    manager.register_document(code, doc_type, docx, pdf, template_source=template_name)

lifecycle_path = manager.write_lifecycle_state()
report = manager.validate(trace_dir=TRACE_DIR)

print("LIFECYCLE=", lifecycle_path)
print(json.dumps(report, ensure_ascii=False, indent=2))
print("PACKAGE_STATUS=", report["package_status"])