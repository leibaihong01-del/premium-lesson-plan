# -*- coding: utf-8 -*-
"""邱志豪四件套端到端生产：v1.5 唯一输出方式。"""
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys

ROOT = r"D:\Users\leibaihong\Desktop\课程材料优化"
WS = os.path.join(ROOT, "毕业设计智能制作工作区")
CA = os.path.join(ROOT, "CourseAgent")
DIRECTION_DIR = "03_电梯系统"
DIRECTION = "电梯系统"
NAME = "邱志豪"
TOPIC = "太平街口站电梯常见故障分析与检修方案设计"

STUDENT_DIR = os.path.join(WS, "03_需要修改文件整理", DIRECTION_DIR, NAME)
INFO_PATH = os.path.join(STUDENT_DIR, "学生信息.json")
PACKAGE_DIR = os.path.join(WS, "06_输出成果", DIRECTION_DIR, NAME + "_毕业设计完整成果包")
PROCESS_DIR = os.path.join(PACKAGE_DIR, "_过程记录")
GOLDEN_RESULT = os.path.join(WS, "02_模板文件", "02 杨振海 毕业设计成果 黄兴南路站AFC闸机设备检修方案设计.docx")
RENDER_MOD = os.path.join(WS, "00_系统配置", "模块", "v06", "render_docx.py")


def load_render():
    spec = importlib.util.spec_from_file_location("render_docx", RENDER_MOD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def render_pdf(docx, pdf):
    rd = load_render()
    import tempfile
    tmp = tempfile.mkdtemp(prefix="qz_full_")
    src = os.path.join(tmp, "src.docx")
    dst = os.path.join(tmp, "out.pdf")
    shutil.copy2(docx, src)
    ok = rd.render_to_pdf(src, dst)
    if ok and os.path.exists(dst):
        os.makedirs(os.path.dirname(pdf), exist_ok=True)
        shutil.copy2(dst, pdf)
    shutil.rmtree(tmp, ignore_errors=True)
    return ok


def main():
    os.makedirs(PROCESS_DIR, exist_ok=True)
    with io.open(INFO_PATH, encoding="utf-8") as f:
        info = json.load(f)

    # 01 任务书：唯一入口 v03/run_taskbook_case.py
    tb_runner = os.path.join(WS, "00_系统配置", "模块", "v03", "run_taskbook_case.py")
    env = dict(os.environ)
    env["GRAD_STUDENT"] = NAME
    env["GRAD_DIRECTION"] = DIRECTION_DIR
    env["GRAD_SEQ"] = "01"
    r = subprocess.run([sys.executable, tb_runner], env=env, capture_output=True, timeout=900)
    tb_src = os.path.join(WS, "06_输出成果", "V0.3_%s任务书验证" % NAME,
                          "01 %s 毕业设计任务书 %s.docx" % (NAME, TOPIC))
    tb_out = os.path.join(PACKAGE_DIR, "01 %s 毕业设计任务书 %s.docx" % (NAME, TOPIC))
    shutil.copy2(tb_src, tb_out)
    tb_pdf = os.path.join(PROCESS_DIR, "01 %s 毕业设计任务书 %s.pdf" % (NAME, TOPIC))
    tb_render = render_pdf(tb_out, tb_pdf)
    print("taskbook rc:", r.returncode, "render:", tb_render, "exists:", os.path.exists(tb_out))

    # 02 成果：v1.5 唯一输出方式 result_v1.4_pipeline.py
    res_out = os.path.join(PACKAGE_DIR, "02 %s 毕业设计成果 %s.docx" % (NAME, TOPIC))
    res_pdf = os.path.join(PROCESS_DIR, "02 %s 毕业设计成果 %s.pdf" % (NAME, TOPIC))
    pipeline = os.path.join(CA, "tools", "result_v1.4_pipeline.py")
    rr = subprocess.run([sys.executable, pipeline, INFO_PATH, DIRECTION, res_out, GOLDEN_RESULT, res_pdf],
                        capture_output=True, timeout=900)
    with open(os.path.join(PROCESS_DIR, "result_production_report.json"), "wb") as f:
        f.write(rr.stdout)
    print("result rc:", rr.returncode, "exists:", os.path.exists(res_out), os.path.exists(res_pdf))

    # 03/04：EvaluationSkillRunner + DefenseSkillRunner
    sys.path.insert(0, os.path.join(CA, "core"))
    from student_profile import StudentProfile
    from graduation_skill_runners import DefenseSkillRunner, EvaluationSkillRunner
    profile = StudentProfile(
        school="长沙轨道交通职业学院",
        college="轨道车辆学院",
        major="城市轨道交通机电技术",
        class_name=info["班级"],
        student_name=info["姓名"],
        student_id=info["学号"],
        advisor=info["指导老师"],
        topic=info["课题名称"],
        direction=info["方向"],
    )
    ev = EvaluationSkillRunner(profile, WS, CA, ROOT)
    ev_res = ev.run(STUDENT_DIR, PACKAGE_DIR, PROCESS_DIR)
    print("evaluation:", os.path.exists(ev_res["output"]), os.path.exists(ev_res["pdf"]))
    os.environ["DEFENSE_LAYOUT_NORMALIZE"] = "1"
    dv = DefenseSkillRunner(profile, WS, CA, ROOT)
    dv_res = dv.run(STUDENT_DIR, PACKAGE_DIR, PROCESS_DIR)
    print("defense:", os.path.exists(dv_res["output"]), os.path.exists(dv_res["pdf"]))

    # 校验
    checks = {
        "01_taskbook": os.path.exists(tb_out),
        "02_result": os.path.exists(res_out),
        "03_evaluation": os.path.exists(ev_res["output"]),
        "04_defense": os.path.exists(dv_res["output"]),
        "02_result_pdf": os.path.exists(res_pdf),
    }
    with io.open(os.path.join(PROCESS_DIR, "generation_checks.json"), "w", encoding="utf-8") as f:
        json.dump({"student": NAME, "topic": TOPIC, "checks": checks}, f, ensure_ascii=False, indent=2)
    print("checks:", checks)


if __name__ == "__main__":
    main()
