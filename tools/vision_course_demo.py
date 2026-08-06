# -*- coding: utf-8 -*-
"""课程文档生成 Demo：课程模板截图 + 任务书 → 文档生成结果。"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from planner.vision_constraint_planner import VisionConstraintPlanner
from providers.vision import analyze_media
from validators.vision_consistency import validate

TEMPLATE_PROMPT = (
    "请分析该模板的版式结构，输出 layout_elements、page_size、sections、notes 的结构化JSON。"
)


class MockTemplateProvider:
    name = "mock"

    def analyze(self, image_path, prompt, **kwargs):
        return {
            "ok": True,
            "provider": "mock",
            "analysis": {
                "layout_elements": ["title", "sections", "footer"],
                "page_size": "A4",
                "sections": ["课程基本信息", "教学目标", "教学内容", "教学评价"],
                "notes": ["标题居中", "教学评价使用表格"],
            },
        }


def build_document(spec, sections):
    title = (spec.get("goal") or "课程文档")[:50]
    doc = {"title": title, "sections": []}
    for sec in sections:
        doc["sections"].append({
            "heading": sec,
            "content": "（依据任务规格生成：" + str(spec.get("intent", "")) + "）",
        })
    return doc


def render_markdown(doc):
    lines = ["# " + doc.get("title", "课程文档"), ""]
    for sec in doc.get("sections", []):
        lines.append("## " + sec["heading"])
        lines.append("")
        lines.append(sec["content"])
        lines.append("")
    return "\n".join(lines)


def run_demo(template_path, task, mock=True, enabled=False, course="", kind="course_document"):
    if mock:
        provider = MockTemplateProvider()
    elif enabled:
        from providers.vision.mimo import MimoVisionProvider
        provider = MimoVisionProvider({
            "enabled": True,
            "base_url": os.getenv("MIMO_BASE_URL", ""),
            "api_key_env": "MIMO_API_KEY",
            "model": os.getenv("MIMO_MODEL", "mimo-vision"),
        })
    else:
        provider = None
    vision_result = analyze_media(template_path, TEMPLATE_PROMPT, provider)
    planner = VisionConstraintPlanner(vision_result)
    spec = {
        "raw": task,
        "goal": task,
        "intent": "generate",
        "domains": ["教案"],
        "quality": "normal",
        "deliverables": ["课程文档"],
        "constraints": [],
        "compute_hint": [],
    }
    planned, plan = planner.plan(spec)
    sections = plan["required_sections"] or ["课程基本信息", "教学目标", "教学内容", "教学评价"]
    doc = build_document(planned, sections)
    markdown = render_markdown(doc)
    consistency = validate(markdown, planner.context.structure)
    return {
        "ok": consistency["ok"],
        "document": doc,
        "markdown": markdown,
        "plan": plan,
        "consistency": consistency,
    }


def main():
    parser = argparse.ArgumentParser(description="Vision 课程文档生成 Demo")
    parser.add_argument("template", help="课程模板截图或PDF路径")
    parser.add_argument("--task", default="生成课程文档")
    parser.add_argument("--mock", action="store_true", default=True, help="使用内置Mock模板结构（默认）")
    parser.add_argument("--enabled", action="store_true", help="启用MiMo真实API")
    parser.add_argument("--out-md", default="", help="输出Markdown路径")
    parser.add_argument("--out-json", default="", help="输出JSON路径")
    args = parser.parse_args()
    result = run_demo(args.template, args.task, mock=args.mock, enabled=args.enabled)
    summary = {k: v for k, v in result.items() if k != "markdown"}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.out_md:
        with open(args.out_md, "w", encoding="utf-8") as f:
            f.write(result["markdown"])
        print("Markdown:", args.out_md)
    if args.out_json:
        with open(args.out_json, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("JSON:", args.out_json)


if __name__ == "__main__":
    main()