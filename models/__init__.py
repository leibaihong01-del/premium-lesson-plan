# -*- coding: utf-8 -*-
"""模型适配层：统一模型接口与注册表（V1.0 基础层）。"""

from .base import ModelAdapter
from .deepseek import DeepSeekAdapter
from .registry import ModelRegistry

__all__ = ["ModelAdapter", "DeepSeekAdapter", "ModelRegistry"]