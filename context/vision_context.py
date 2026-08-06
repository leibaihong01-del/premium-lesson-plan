# -*- coding: utf-8 -*-
"""Vision Context 注入层：把视觉识别的模板结构转换为生成约束，外挂注入。"""
import copy

from providers.vision.schema import extract_json_text


def _first(analysis, *keys):
    for k in keys:
        v = analysis.get(k)
        if v:
            return v
    return None


def extract_structure(vision_result):
    analysis = vision_result.get("analysis") or vision_result.get("content") or {}
    analysis = extract_json_text(analysis)
    if not isinstance(analysis, dict):
        analysis = {}

    layout = _first(analysis, "layout_elements", "elements", "关键元素", "版面元素")
    page = _first(analysis, "page_size", "页面尺寸", "版式尺寸", "纸张大小")
    sections = _first(analysis, "sections", "章节", "板块", "结构单元", "页面结构")
    notes_raw = _first(analysis, "notes", "备注", "建议", "建议标签")

    if not isinstance(layout, list):
        layout = []
    if not isinstance(sections, list):
        sections = []
    layout = [str(x) for x in layout if x]
    sections = [str(x) for x in sections if isinstance(x, (str, int, float))]

    notes = []
    if isinstance(notes_raw, list):
        notes = [str(x) for x in notes_raw if x]
    elif isinstance(notes_raw, str):
        notes = [notes_raw]
    layout_desc = analysis.get("布局结构") or analysis.get("layout_description")
    if isinstance(layout_desc, str) and layout_desc and layout_desc not in notes:
        notes.append(layout_desc)

    return {
        "layout_elements": layout,
        "page_size": str(page or "A4"),
        "sections": sections,
        "notes": notes,
    }


class VisionContext:
    def __init__(self, vision_result=None):
        self.vision_result = vision_result or {}
        self.structure = extract_structure(self.vision_result)

    def to_context(self):
        return {
            "vision_result": self.vision_result,
            "structure": self.structure,
            "constraints": {
                "required_sections": list(self.structure["sections"]),
                "layout_elements": list(self.structure["layout_elements"]),
                "page_size": self.structure["page_size"],
                "notes": list(self.structure["notes"]),
            },
        }

    def inject(self, task_spec):
        out = copy.deepcopy(task_spec or {})
        out["vision_context"] = self.to_context()
        out["planning_injected"] = True
        return out