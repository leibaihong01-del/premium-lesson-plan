# -*- coding: utf-8 -*-
"""第二层轻量判断器：置信度不足时基于摘要信息补充判断。"""


def judge(meta, request, base):
    reason = list(base.get("reason", []))
    confidence = base.get("confidence", 0.85)
    complexity = base.get("complexity", 50)
    if meta.get("tables", 0) >= 20:
        complexity = max(complexity, 85)
        reason.append("表格数量大")
        confidence = max(confidence, 0.95)
    elif meta.get("pages", 0) >= 30:
        complexity = max(complexity, 60)
        reason.append("页数中等")
        confidence = max(confidence, 0.9)
    if "精品" in request or "专家" in request:
        complexity = max(complexity, 80)
        reason.append("要求高")
        confidence = max(confidence, 0.92)
    level = "low" if complexity <= 30 else "medium" if complexity <= 70 else "high"
    return {
        "complexity": complexity,
        "confidence": confidence,
        "reason": reason,
        "recommended_compute": level,
        "scores": base.get("scores", {}),
    }
