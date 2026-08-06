# -*- coding: utf-8 -*-
"""Vision Ingestion Workflow：视觉材料 → 分析 → 标准Schema → Memory。"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from providers.vision import analyze_media
from providers.vision.schema import normalize_vision_result, validate_vision_result
from router.vision_router import decide_vision


def run_vision_ingestion(path, prompt, provider=None, config=None, memory=None,
                         page_index=0, enabled=False, providers=(), **kwargs):
    """图片 / PDF 视觉分析并写入 Memory。

    返回规范化后的 Vision Result，含 route 与 schema_valid。
    """
    meta = {"request": prompt, "modality": "vision", "path": path}
    route = decide_vision(meta, providers=providers, enabled=enabled)
    if provider is None and route.get("strategy") == "vision":
        from providers.vision.mimo import MimoVisionProvider
        provider = MimoVisionProvider(config or {})
    result = analyze_media(path, prompt, provider, page_index=page_index, **kwargs)
    media_type = "pdf" if str(path).lower().endswith(".pdf") else "image"
    norm = normalize_vision_result(result, input_path=path, prompt=prompt,
                                   media_type=media_type)
    schema = validate_vision_result(norm)
    norm["schema_valid"] = schema["valid"]
    norm["route"] = route
    norm["time"] = time.strftime("%Y-%m-%d %H:%M:%S")
    if memory is not None:
        memory.add("vision_results", norm)
    return norm