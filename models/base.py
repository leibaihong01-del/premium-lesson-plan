# -*- coding: utf-8 -*-
"""ModelAdapter 基础接口。

V1.0 仅实现 generate() 与 health_check()；
vision() / embed() 为预留能力，暂不实现（见设计文档）。
核心 Agent 只依赖本抽象，不依赖具体模型。
"""


class ModelAdapter:
    name = "base"

    def __init__(self, config=None):
        self.config = config or {}

    def health_check(self):
        """返回模型可用状态：disabled / enabled + latency。"""
        enabled = bool(self.config.get("enabled", False))
        return {
            "adapter": self.name,
            "status": "enabled" if enabled else "disabled",
            "latency_ms": None,
        }

    def generate(self, prompt, system=None, **kwargs):
        raise NotImplementedError("generate 由具体模型实现")

    def vision(self, image, prompt, **kwargs):
        # 预留：V1.0 不实现
        raise NotImplementedError("vision 为预留能力，V1.0 未实现")

    def embed(self, texts, **kwargs):
        # 预留：V1.0 不实现
        raise NotImplementedError("embed 为预留能力，V1.0 未实现")
