# -*- coding: utf-8 -*-
"""Vision 标准结果 Schema 与规范化。"""
import json
import re

VISION_RESULT_SCHEMA = {
    "type": "object",
    "required": ["ok", "provider", "prompt"],
    "properties": {
        "ok": {"type": "boolean"},
        "provider": {"type": "string"},
        "prompt": {"type": "string"},
        "analysis": {"type": ["string", "array", "object"]},
        "issues": {"type": "array", "items": {"type": "string"}},
        "confidence": {"type": "number"},
        "skill": {"type": "string"},
        "input": {"type": "string"},
        "media_type": {"type": "string"},
        "metadata": {"type": "object"},
    },
}


def extract_json_text(text):
    """从模型输出中提取 JSON：支持 Markdown 代码块包裹。"""
    if not isinstance(text, str):
        return text
    t = text.strip()
    if t.startswith("```"):
        m = re.match(r"^```(?:json)?\s*\n?(.*?)\n?```\s*$", t, re.S)
        if m:
            t = m.group(1).strip()
        else:
            parts = t.split("```", 2)
            if len(parts) >= 3:
                t = parts[1].strip()
                if t.startswith("json"):
                    t = t[4:].strip()
    try:
        return json.loads(t)
    except Exception:
        return text


def _merge_metadata(result):
    metadata = dict(result.get("metadata", {}) or {})
    for key in ("error", "path", "page_index"):
        if result.get(key) is not None:
            metadata[key] = result.get(key)
    return metadata


def normalize_vision_result(result, input_path="", prompt="", media_type="",
                            skill="vision_understanding"):
    """将任意 Provider 输出规范化为统一 Vision Result。"""
    raw_analysis = (result.get("analysis") or result.get("content")
                    or result.get("visual_analysis") or result.get("raw"))
    analysis = extract_json_text(raw_analysis)
    out = {
        "ok": bool(result.get("ok")),
        "provider": result.get("provider", "unknown"),
        "prompt": result.get("prompt", prompt),
        "analysis": analysis,
        "issues": list(result.get("issues", []) or []),
        "confidence": float(result.get("confidence", 0.0) or 0.0),
        "skill": result.get("skill", skill),
        "input": result.get("input", input_path),
        "media_type": result.get("media_type", media_type),
        "metadata": _merge_metadata(result),
    }
    return out


def validate_vision_result(result):
    """检查标准 Schema 必填字段，返回 {valid, errors}。"""
    errors = []
    for key in ("ok", "provider", "prompt"):
        if key not in result:
            errors.append("缺少字段: " + key)
    return {"valid": not errors, "errors": errors}