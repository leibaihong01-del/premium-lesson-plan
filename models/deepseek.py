# -*- coding: utf-8 -*-
"""DeepSeek 模型适配器（试点，默认关闭，密钥仅环境变量）。"""
import json
import os
import urllib.request

from .base import ModelAdapter


class DeepSeekAdapter(ModelAdapter):
    name = "deepseek"

    def __init__(self, config=None):
        super().__init__(config)
        self.api_key = os.getenv(self.config.get("api_key_env", ""), "")

    def health_check(self):
        base = super().health_check()
        if base["status"] != "enabled":
            return base
        if not self.api_key:
            base["status"] = "misconfigured"
            base["reason"] = "API key 未配置（环境变量）"
        return base

    def generate(self, prompt, system=None, **kwargs):
        if not self.config.get("enabled", False):
            raise RuntimeError("deepseek 未启用")
        if not self.api_key:
            raise RuntimeError("deepseek API key 未配置")
        base_url = self.config.get("base_url", "").rstrip("/")
        url = base_url + "/chat/completions"
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        payload = json.dumps({
            "model": self.config.get("model", "deepseek-chat"),
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.2),
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key,
        })
        timeout = self.config.get("timeout", 30)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]
