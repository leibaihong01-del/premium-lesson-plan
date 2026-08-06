# -*- coding: utf-8 -*-
"""Vision Consistency Validator：生成结果与模板结构一致性检查节点。"""
from skills.vision_quality_check import run_quality_check


def validate(generated_text, template_structure, provider=None, **kwargs):
    """一致性检查：必需段落缺失判失败，版式备注作为建议提示。"""
    base = run_quality_check(generated_text, template_structure, provider=provider)
    structure = template_structure or {}
    notes = structure.get("notes") or []
    warnings = ["建议体现版式备注: " + n for n in notes if n and n not in (generated_text or "")]
    return {
        "ok": base["ok"],
        "score": base["score"],
        "issues": base["issues"],
        "warnings": warnings,
        "checked_sections": base["checked_sections"],
        "validator": "vision_consistency",
    }