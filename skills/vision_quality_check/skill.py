# -*- coding: utf-8 -*-
"""Vision Quality Check Skill：模板结构一致性质量检查。"""
import json


def run_quality_check(generated_text, template_structure, provider=None, **kwargs):
    """检查生成文本是否包含模板必需段落，输出结构化JSON。"""
    required = (template_structure or {}).get("sections") or []
    text = generated_text or ""
    issues = []
    for sec in required:
        if sec and sec not in text:
            issues.append("缺少模板段落: " + sec)
    score = round(1 - len(issues) / max(1, len(required)), 2)
    return {
        "ok": not issues,
        "issues": issues,
        "score": score,
        "skill": "vision_quality_check",
        "checked_sections": required,
        "provider": getattr(provider, "name", None),
    }