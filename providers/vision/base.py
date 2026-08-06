# -*- coding: utf-8 -*-
"""Vision Provider 抽象层：统一图片 / PDF 页面视觉分析接口。"""
import abc


class VisionProvider(abc.ABC):
    name = "base"

    def __init__(self, config=None):
        self.config = config or {}

    @abc.abstractmethod
    def health_check(self):
        """返回结构化状态：disabled / enabled / misconfigured。"""

    @abc.abstractmethod
    def analyze(self, image_path, prompt, **kwargs):
        """输入图片文件路径，输出结构化 dict。"""