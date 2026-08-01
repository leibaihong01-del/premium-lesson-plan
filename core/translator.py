# -*- coding: utf-8 -*-
"""需求转译智能体：自然语言 → 结构化 TaskSpec。"""
import json
import re


INTENT_KEYWORDS = {
    "generate": ["生成", "创建", "新建", "制定", "制作"],
    "optimize": ["优化", "提升", "重构", "改进", "升级"],
    "audit": ["审核", "检查", "评估", "检测", "评分"],
    "convert": ["转换", "转成", "套用模板", "套模板"],
    "plan": ["规划", "方案", "设计", "建议", "路线"],
}

DOMAIN_KEYWORDS = {
    "课程标准": ["课程标准", "课标"],
    "教学进度计划": ["教学进度", "进度计划", "教学计划"],
    "教案": ["教案", "教学设计"],
    "实训": ["实训", "实操", "任务书", "任务工单", "评价标准"],
    "课件": ["课件", "PPT", "演示文稿"],
    "题库": ["题库", "试题", "试卷", "习题"],
    "竞赛": ["比赛", "竞赛", "说课", "课堂创新"],
    "教研": ["教改", "课题", "论文", "教研"],
    "成果": ["软著", "软件著作权", "专利", "申报", "成果"],
}

QUALITY_KEYWORDS = {
    "excellent": ["精品", "申报", "专家", "excellent", "优秀教师"],
    "formal": ["正式", "规范", "标准", "formal"],
}

FORBIDDEN_HINTS = ["禁止", "不要", "不允许", "避免"]


def parse(request, user_profile=None):
    req = request or ""
    intent = None
    for key, words in INTENT_KEYWORDS.items():
        if any(w in req for w in words):
            intent = key
            break
    domains = [d for d, words in DOMAIN_KEYWORDS.items() if any(w in req for w in words)]
    quality = "excellent" if any(w in req for w in QUALITY_KEYWORDS["excellent"]) else \
              "formal" if any(w in req for w in QUALITY_KEYWORDS["formal"]) else "normal"
    constraints = []
    if any(w in req for w in FORBIDDEN_HINTS):
        for term in ["设备维修", "联锁故障处理", "CBTC参数配置", "信号设备检修", "越界内容"]:
            if term in req:
                constraints.append("禁止：" + term)
    if "模板" in req:
        constraints.append("模板优先")
    if "报告" in req or "闭环" in req:
        constraints.append("输出审核报告并闭环")
    hints = []
    if any(w in req for w in ["大量", "多份", "多轮", "复杂", "专家"]):
        hints.append("高复杂度")
    if intent in ("generate", "plan") and quality == "excellent":
        hints.append("建议高算力")
    elif intent in ("audit", "convert") and quality != "excellent":
        hints.append("建议低/标准算力")
    spec = {
        "goal": req[:120],
        "intent": intent or "unknown",
        "domains": domains or ["未知"],
        "deliverables": domains or ["课程文档"],
        "quality": quality,
        "constraints": constraints,
        "compute_hint": hints,
        "confidence": 0.6,
        "raw": req,
    }
    if intent:
        spec["confidence"] += 0.15
    if domains:
        spec["confidence"] += 0.15
    if quality != "normal":
        spec["confidence"] += 0.1
    if user_profile:
        pref = user_profile.get("preferences", {})
        if pref.get("重视精品标准"):
            spec["quality"] = "excellent"
            spec["constraints"].append("用户偏好：精品标准")
        if pref.get("要求闭环报告"):
            spec["constraints"].append("用户偏好：闭环报告")
        spec["confidence"] = min(0.95, spec["confidence"] + 0.05)
    spec["confidence"] = min(0.95, round(spec["confidence"], 2))
    return spec


def enrich_spec_with_llm(spec, adapter, prompt=None):
    """可选LLM增强：细化需求转译结果；任何异常回退原spec（默认关闭）。"""
    if not adapter or not getattr(adapter, "health_check", None):
        return spec
    try:
        hc = adapter.health_check()
        if hc.get("status") != "enabled":
            return spec
        p = prompt or (
            "请基于以下需求输出JSON，字段：intent/domains/quality/constraints。"
            "只输出JSON，不要其他文字。\n需求：" + spec.get("raw", "")
        )
        text = adapter.generate(p)
        start = text.find("{")
        end = text.rfind("}") + 1
        if start < 0 or end <= start:
            return spec
        data = json.loads(text[start:end])
        if isinstance(data, dict):
            for key in ("intent", "quality"):
                if data.get(key):
                    spec[key] = data[key]
            if isinstance(data.get("domains"), list) and data["domains"]:
                spec["domains"] = data["domains"]
            if isinstance(data.get("constraints"), list):
                spec["constraints"] = list(spec.get("constraints", [])) + data["constraints"]
            spec["llm_enhanced"] = True
    except Exception:
        pass
    return spec
