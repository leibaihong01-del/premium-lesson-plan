# -*- coding: utf-8 -*-
"""Vision 任务自动路由（独立新增，不影响现有 router/decision）。"""

VISION_KEYWORDS = [
    "PPT", "ppt", "演示文稿", "图片", "教材图", "案例图", "截图",
    "PDF页面", "页面分析", "版式", "视觉", "图",
]


def decide_vision(meta=None, spec=None, providers=(), enabled=False):
    """判断是否调用视觉能力。

    meta：任务元信息（request / modality / domains 等）；
    spec：TaskSpec（可选）；
    providers：已启用视觉 provider 列表；
    enabled：vision 总开关。
    """
    meta = meta or {}
    spec = spec or {}
    parts = [
        str(meta.get("request") or ""),
        str(meta.get("modality") or ""),
        str(spec.get("raw") or ""),
        " ".join(str(x) for x in (spec.get("domains") or [])),
        str(meta.get("domains") or ""),
    ]
    text = " ".join(parts)
    is_vision = any(kw in text for kw in VISION_KEYWORDS)
    if not is_vision:
        return {"strategy": "none", "provider": None, "reason": "非视觉任务"}
    provider_list = list(providers or [])
    if not enabled or not provider_list:
        return {"strategy": "rule", "provider": None,
                "reason": "视觉模型未启用，回退规则检测"}
    return {"strategy": "vision", "provider": provider_list[0],
            "reason": "视觉任务，调用 Vision Provider"}