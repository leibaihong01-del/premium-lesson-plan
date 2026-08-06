# -*- coding: utf-8 -*-
"""Vision Provider 插件：统一视觉分析接口与 MiMo Provider。"""

from .analyzer import analyze_media, render_pdf_page
from .base import VisionProvider
from .mimo import MimoVisionProvider
from .registry import VisionProviderRegistry
from .schema import VISION_RESULT_SCHEMA, normalize_vision_result, validate_vision_result

__all__ = [
    "VisionProvider",
    "MimoVisionProvider",
    "VisionProviderRegistry",
    "analyze_media",
    "render_pdf_page",
    "VISION_RESULT_SCHEMA",
    "normalize_vision_result",
    "validate_vision_result",
]