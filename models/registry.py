# -*- coding: utf-8 -*-
"""模型注册表：注册、获取、列表。"""


class ModelRegistry:
    def __init__(self):
        self._adapters = {}

    def register(self, name, adapter):
        if not hasattr(adapter, "generate"):
            raise TypeError("adapter 必须实现 generate()")
        self._adapters[name] = adapter
        return adapter

    def get(self, name):
        return self._adapters.get(name)

    def list(self):
        return sorted(self._adapters)

    def clear(self):
        self._adapters.clear()
