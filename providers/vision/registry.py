# -*- coding: utf-8 -*-
"""Vision Provider 注册表：注册、获取、列表。"""


class VisionProviderRegistry:
    def __init__(self):
        self._providers = {}

    def register(self, name, provider):
        if not hasattr(provider, "analyze"):
            raise TypeError("provider 必须实现 analyze()")
        self._providers[name] = provider
        return provider

    def get(self, name):
        return self._providers.get(name)

    def list(self):
        return sorted(self._providers)

    def clear(self):
        self._providers.clear()