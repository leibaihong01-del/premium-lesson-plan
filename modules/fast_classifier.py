# -*- coding: utf-8 -*-
"""第一层规则快速判断器：零/低 Token，纯程序判断任务复杂度。"""


LEVELS = ["low", "medium", "high"]


def classify(file_meta, request=""):
    req = request or ""
    file_score = 0
    files = file_meta.get("file_count", 1)
    file_score += 5 if files == 1 else 15
    if file_meta.get("pages", 0) >= 60:
        file_score += 10
    if file_meta.get("tables", 0) >= 10:
        file_score += 10
    if file_meta.get("images", 0) >= 5:
        file_score += 5
    if file_meta.get("complex_layout"):
        file_score += 10

    content_score = 10
    if any(k in req for k in ("专家级", "专家评审", "重构")):
        content_score = 50
    elif any(k in req for k in ("专业课程优化", "精品课程", "教学设计")):
        content_score = 40
    elif any(k in req for k in ("结构调整", "内容重构")):
        content_score = 30
    elif any(k in req for k in ("润色", "调整")):
        content_score = 20

    quality_score = 10
    if any(k in req for k in ("精品课程申报", "专家评审", "excellent", "精品")):
        quality_score = 50
    elif any(k in req for k in ("正式文档", "formal", "官方")):
        quality_score = 30

    total = min(100, file_score + content_score + quality_score)
    if total <= 30:
        level = "low"
    elif total <= 70:
        level = "medium"
    else:
        level = "high"

    confidence = 0.95
    reason = []
    if file_meta.get("tables", 0) >= 10:
        reason.append("大量表格")
    if file_meta.get("pages", 0) >= 60:
        reason.append("页数较多")
    if content_score >= 40:
        reason.append("专业内容重构")
    if quality_score >= 50:
        reason.append("精品/申报级质量要求")
    if not reason:
        reason.append("常规任务")
        confidence = 0.85
    return {
        "complexity": total,
        "confidence": confidence,
        "reason": reason,
        "recommended_compute": level,
        "scores": {"file": file_score, "content": content_score, "quality": quality_score},
    }
