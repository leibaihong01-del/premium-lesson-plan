# -*- coding: utf-8 -*-
import json, os, shutil, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
COURSEAGENT = r"D:\Users\leibaihong\Desktop\课程材料优化\CourseAgent"
PROJECT = r"D:\Users\leibaihong\Desktop\课程材料优化"
WS = os.path.join(PROJECT, "毕业设计智能制作工作区")
sys.path.insert(0, os.path.join(COURSEAGENT, "core"))
sys.path.insert(0, os.path.join(WS, "00_系统配置", "模块", "v03"))
sys.path.insert(0, os.path.join(WS, "00_系统配置", "模块", "v06"))
from docx import Document
from student_profile import StudentProfile
from graduation_skill_runners import EvaluationSkillRunner, DefenseSkillRunner
from render_docx import render_to_pdf
from result_document_parser import parse as parse_result
from document_structure_parser import parse as parse_structure

DIRECTION = "01_AFC自动售检票系统"
STUDENT = "王欢"
INFO = os.path.join(WS, "03_需要修改文件整理", DIRECTION, STUDENT, "学生信息.json")
STUDENT_DIR = os.path.join(WS, "03_需要修改文件整理", DIRECTION, STUDENT)
REGRESS = os.path.join(WS, "06_输出成果", DIRECTION, STUDENT + "_归档回归测试")
PROCESS = os.path.join(REGRESS, "_过程记录")
os.makedirs(PROCESS, exist_ok=True)
with open(INFO, encoding="utf-8") as f:
    info = json.load(f)
topic = info["课题名称"]

def profile_from_info(i):
    return StudentProfile.from_dict({
        "school": "长沙轨道交通职业学院", "college": "轨道车辆学院", "major": "城市轨道交通机电技术",
        "class": i["班级"], "student_name": i["姓名"], "student_id": i["学号"],
        "advisor": i["指导老师"], "topic": i["课题名称"], "direction": i["方向"]
    })

process_map = {
  "task_book": {"template": "01 杨振海 毕业设计任务书 ...docx", "input": os.path.join(STUDENT_DIR, "任务书.docx"), "generator": "v03/run_taskbook_case.py", "validator": "v03/internal_audit.py", "experience": ["task_book_tkm_001", "task_book_quality_memory_001"]},
  "grade_evaluation": {"template": "04 杨振海 毕业设计成绩评定表 ...docx", "input": INFO, "generator": "EvaluationSkillRunner", "validator": "TemplateComplianceSense", "experience": ["evaluation_form_tkm_001", "evaluation_form_quality_memory_001"]},
  "defense_record": {"template": "05 杨振海 毕业设计答辩记录表 ...docx", "input": os.path.join(STUDENT_DIR, "答辩记录表.docx"), "generator": "DefenseSkillRunner", "validator": "TemplateComplianceSense", "experience": ["defense_record_tkm_001", "defense_record_quality_memory_001"]}
}
with open(os.path.join(COURSEAGENT, "docs", "v0.7", "ResultAgent", "Graduation_Archive_Process_Map.json"), "w", encoding="utf-8") as f:
    json.dump(process_map, f, ensure_ascii=False, indent=2)

env = dict(os.environ, GRAD_STUDENT=STUDENT, GRAD_DIRECTION=DIRECTION, GRAD_SEQ="01")
subprocess.run([sys.executable, os.path.join(WS, "00_系统配置", "模块", "v03", "run_taskbook_case.py")], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, cwd=PROJECT, timeout=600)
task_src = os.path.join(WS, "06_输出成果", "V0.3_王欢任务书验证", "01 王欢 毕业设计任务书 %s.docx" % topic)
task_docx = os.path.join(REGRESS, "01 王欢 毕业设计任务书 %s_回归测试版.docx" % topic)
task_pdf = os.path.join(PROCESS, os.path.basename(task_docx).replace(".docx", ".pdf"))
shutil.copy2(task_src, task_docx)
render_to_pdf(task_docx, task_pdf)

eval_runner = EvaluationSkillRunner(profile_from_info(info), WS, COURSEAGENT, PROJECT)
def_runner = DefenseSkillRunner(profile_from_info(info), WS, COURSEAGENT, PROJECT)
eval_runner.run(STUDENT_DIR, REGRESS, PROCESS)
def_runner.run(STUDENT_DIR, REGRESS, PROCESS)

eval_docx = os.path.join(REGRESS, "03 王欢 毕业设计成绩评定表 %s.docx" % topic)
def_docx = os.path.join(REGRESS, "04 王欢 毕业设计答辩记录表 %s.docx" % topic)
eval_pdf = os.path.join(PROCESS, "03 王欢 毕业设计成绩评定表 %s.pdf" % topic)
def_pdf = os.path.join(PROCESS, "04 王欢 毕业设计答辩记录表 %s.pdf" % topic)

def check_doc(path, pdf_path=None):
    s = parse_structure(path, pdf_path, document_type="result")
    m = parse_result(path)
    text = s.get("full_text", "")
    pages = (s.get("pages") or {}).get("count")
    return {"tables": len(s.get("tables", [])), "pages": pages, "text_has": {k: (k in text) for k in ["王欢", "202421044615", topic, "瞿曌"]}, "sections": len(m.get("sections", [])), "refs": m.get("reference_count", 0)}

task_r = check_doc(task_docx, task_pdf)
eval_r = check_doc(eval_docx, eval_pdf)
def_r = check_doc(def_docx, def_pdf)

results = {
  "task_book": {"status": "PASS" if (task_r["tables"]==1 and task_r["text_has"]["王欢"] and task_r["text_has"][topic]) else "PARTIAL", "details": task_r},
  "grade_evaluation": {"status": "PASS" if (eval_r["tables"]==1 and eval_r["text_has"]["王欢"] and eval_r["text_has"][topic]) else "PARTIAL", "details": eval_r},
  "defense_record": {"status": "PASS" if (def_r["tables"]==1 and def_r["text_has"]["王欢"] and def_r["text_has"][topic]) else "PARTIAL", "details": def_r}
}
for name, data in results.items():
    with open(os.path.join(PROCESS, "%s_Regression_Result.json" % name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

all_pass = all(r["status"] == "PASS" for r in results.values())
lines = [
 "# Graduation Archive Regression Report", "",
 "- 学生：王欢", "",
 "| 文档 | 状态 | 表格 | 页数 | 姓名 | 学号 | 课题 |", "|---|---|---|---|---|---|---|",
]
for name, r in results.items():
    d = r["details"]
    lines.append("| %s | %s | %s | %s | %s | %s | %s |" % (name, r["status"], d["tables"], d["pages"], d["text_has"]["王欢"], d["text_has"]["202421044615"], d["text_has"][topic]))
lines.append("")
lines.append("## 结论")
lines.append("")
lines.append("- 综合状态：%s" % ("PASS" if all_pass else "PARTIAL"))
lines.append("- Skill 封装条件：%s" % ("可以封装" if all_pass else "需要修复后封装"))
report = os.path.join(COURSEAGENT, "docs", "v0.7", "ResultAgent", "Graduation_Archive_Regression_Report.md")
with open(report, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(json.dumps({"taskbook": task_docx, "task_pdf": task_pdf, "eval": eval_docx, "eval_pdf": eval_pdf, "defense": def_docx, "defense_pdf": def_pdf, "results": results, "report": report}, ensure_ascii=False, indent=2))