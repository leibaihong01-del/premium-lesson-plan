# -*- coding: utf-8 -*-
"""CourseAgent 文件输入/输出式自动工作系统入口。

用法：
1. 文件放入 input/templates、input/materials、input/requirements；
2. 运行：python run_agent.py；
3. 结果写入 output/documents、output/reports、output/json；
4. 中间过程与视觉缓存写入 workspace/intermediate、workspace/vision_cache。
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(ROOT, "input")
TEMPLATES = os.path.join(INPUT, "templates")
MATERIALS = os.path.join(INPUT, "materials")
REQUIREMENTS = os.path.join(INPUT, "requirements")
WORKSPACE = os.path.join(ROOT, "workspace")
VISION_CACHE = os.path.join(WORKSPACE, "vision_cache")
INTERMEDIATE = os.path.join(WORKSPACE, "intermediate")
OUTPUT = os.path.join(ROOT, "output")
DOCS = os.path.join(OUTPUT, "documents")
REPORTS = os.path.join(OUTPUT, "reports")
JSON_DIR = os.path.join(OUTPUT, "json")

DOC_EXTS = (".docx",)
MEDIA_EXTS = (".png", ".jpg", ".jpeg", ".pdf")
REQ_EXTS = (".json", ".md", ".txt")

TEMPLATE_PROMPT = (
    "请分析该模板的版式结构，输出 layout_elements、page_size、sections、notes 的结构化JSON。"
)


def ensure_dirs():
    for d in (TEMPLATES, MATERIALS, REQUIREMENTS, VISION_CACHE, INTERMEDIATE,
              DOCS, REPORTS, JSON_DIR):
        os.makedirs(d, exist_ok=True)


def find_files(directory, exts):
    if not os.path.isdir(directory):
        return []
    return sorted(
        os.path.join(directory, f) for f in os.listdir(directory)
        if f.lower().endswith(exts) and os.path.isfile(os.path.join(directory, f))
    )


def load_requirement(path):
    if not path:
        return {}
    with open(path, encoding="utf-8") as f:
        if path.lower().endswith(".json"):
            return json.load(f)
        return {"task": f.read().strip()}


def run_vision(template_media, project):
    """调用现有 Vision 模块做模板预分析；失败/未配置不阻断主流程。"""
    try:
        sys.path.insert(0, ROOT)
        from providers.vision import analyze_media
        from providers.vision.mimo import MimoVisionProvider
        from providers.vision.schema import normalize_vision_result, validate_vision_result
        from context.vision_context import VisionContext
        from validators.vision_consistency import validate

        enabled = bool(os.getenv("MIMO_API_KEY") and os.getenv("MIMO_BASE_URL"))
        provider = MimoVisionProvider({"enabled": enabled}) if enabled else None
        raw = analyze_media(template_media, TEMPLATE_PROMPT, provider)
        norm = normalize_vision_result(raw, input_path=template_media,
                                       prompt=TEMPLATE_PROMPT)
        schema = validate_vision_result(norm)
        ctx = VisionContext(norm)
        report = {
            "project": project,
            "template": template_media,
            "schema_valid": schema["valid"],
            "schema_errors": schema["errors"],
            "structure": ctx.structure,
            "constraints": ctx.to_context()["constraints"],
            "raw_ok": norm.get("ok"),
            "raw_error": norm.get("metadata", {}).get("error"),
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        path = os.path.join(VISION_CACHE, project + "_vision.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return report
    except Exception as exc:
        return {"project": project, "ok": False, "error": str(exc), "skipped": True}


def run_workflow(template, material, req, project):
    cmd = [
        sys.executable,
        os.path.join(ROOT, "main.py"),
        "--template", template,
        "--existing", material,
        "--project", project,
        "--kind", req.get("kind", "lesson"),
        "--title", req.get("title", project),
        "--task", req.get("task", "根据模板生成精品课程教案并完成质量闭环"),
        "--profile", req.get("profile", "auto"),
    ]
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(cmd, capture_output=True, env=env, timeout=900)
    out = proc.stdout.decode("utf-8", "replace")
    err = proc.stderr.decode("utf-8", "replace")
    return {"exit": proc.returncode, "stdout": out, "stderr": err}


def copy_tree_files(src_dir, dst_dir, exts=(".json", ".md")):
    copied = []
    if not os.path.isdir(src_dir):
        return copied
    for f in os.listdir(src_dir):
        if f.lower().endswith(exts):
            src = os.path.join(src_dir, f)
            dst = os.path.join(dst_dir, f)
            shutil.copy2(src, dst)
            copied.append(dst)
    return copied


def main():
    parser = argparse.ArgumentParser(description="CourseAgent 自动工作系统")
    parser.add_argument("--project", default="", help="覆盖项目名")
    args = parser.parse_args()
    ensure_dirs()

    templates = find_files(TEMPLATES, DOC_EXTS)
    materials = find_files(MATERIALS, DOC_EXTS)
    requirements = find_files(REQUIREMENTS, REQ_EXTS)
    template_media = find_files(TEMPLATES, MEDIA_EXTS)

    if not templates:
        print("缺少模板：请将 .docx 模板放入 input/templates")
        return 1
    if not materials:
        print("缺少素材：请将 .docx 原文件放入 input/materials")
        return 1

    req = load_requirement(requirements[0]) if requirements else {}
    template = templates[0]
    results = []

    for material in materials:
        name = os.path.splitext(os.path.basename(material))[0]
        project = args.project or req.get("project") or name
        title = req.get("title") or name

        vision = run_vision(template_media[0], project) if template_media else {
            "project": project, "ok": False, "skipped": True}

        proc = run_workflow(template, material, req, project)

        final_src = os.path.join(OUTPUT, project + "_优化后版本.docx")
        doc_dst = ""
        if os.path.exists(final_src):
            doc_dst = os.path.join(DOCS, os.path.basename(final_src))
            shutil.copy2(final_src, doc_dst)

        project_report_dir = os.path.join(OUTPUT, project, "02_检测报告")
        report_files = copy_tree_files(project_report_dir, REPORTS)
        intermediate_files = copy_tree_files(project_report_dir, INTERMEDIATE)

        summary = {
            "project": project,
            "title": title,
            "template": template,
            "material": material,
            "workflow_exit": proc["exit"],
            "document_output": doc_dst,
            "reports": report_files,
            "intermediate": intermediate_files,
            "vision": vision,
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        json_path = os.path.join(JSON_DIR, project + "_run_summary.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        results.append(summary)
        print("已处理:", project, "workflow_exit=", proc["exit"],
              "doc=", doc_dst, "json=", json_path)

    return 0 if all(r["workflow_exit"] == 0 for r in results) else 2


if __name__ == "__main__":
    sys.exit(main())