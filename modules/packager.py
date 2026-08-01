# -*- coding: utf-8 -*-
"""文件打包模块：企业级输出目录。"""
import json
import os
import shutil


def package(project_name, final_docx, reports_dir, memory_dir, output_root):
    base = os.path.join(output_root, project_name)
    dirs = {
        "final": os.path.join(base, "01_最终文件"),
        "reports": os.path.join(base, "02_检测报告"),
        "process": os.path.join(base, "03_过程记录"),
        "growth": os.path.join(base, "04_Agent成长记录"),
    }
    for d in dirs.values():
        os.makedirs(d, exist_ok=True)
    final_name = os.path.basename(final_docx)
    shutil.copy2(final_docx, os.path.join(dirs["final"], final_name))
    for f in os.listdir(reports_dir):
        shutil.copy2(os.path.join(reports_dir, f), os.path.join(dirs["reports"], f))
    for f in os.listdir(memory_dir):
        if f.endswith(".json"):
            shutil.copy2(os.path.join(memory_dir, f), os.path.join(dirs["growth"], f))
    return base, dirs
