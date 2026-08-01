# -*- coding: utf-8 -*-
"""DeepSeek 模型适配器（试点，默认关闭，密钥仅环境变量）。

5.2-E 小范围验证加固：
- retry：失败自动重试，带退避；
- timeout：可配置；
- cost 统计：记录 calls / input_tokens / output_tokens / cost；
- fallback：generate 失败抛异常，由 Translator 增强层回退规则。
"""
import json
import os
import time
import urllib.error
import urllib.request

from .base import ModelAdapter


class DeepSeekAdapter(ModelAdapter):
    name = "deepseek"

    def __init__(self, config=None):
        super().__init__(config)
        self.api_key = os.getenv(self.config.get("api_key_env", ""), "")
        self.timeout = float(self.config.get("timeout", 30) or 30)
        self.max_retries = int(self.config.get("max_retries", 2) or 2)
        self.retry_delay = float(self.config.get("retry_delay", 1.0) or 1.0)
        self.input_price = float(self.config.get("input_price_per_1k", 0.0) or 0.0)
        self.output_price = float(self.config.get("output_price_per_1k", 0.0) or 0.0)
        self.usage = {
            "calls": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "cost": 0.0,
            "failures": 0,
        }

    def reset_usage(self):
        self.usage = {
            "calls": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "cost": 0.0,
            "failures": 0,
        }
        return self.usage

    def _record_usage(self, data, payload_text):
        usage = data.get("usage") or {}
        in_tokens = int(usage.get("prompt_tokens") or 0) or max(1, int(len(payload_text) / 1.5))
        out_tokens = int(usage.get("completion_tokens") or 0)
        cost = (in_tokens / 1000.0 * self.input_price) + (out_tokens / 1000.0 * self.output_price)
        self.usage["calls"] += 1
        self.usage["input_tokens"] += in_tokens
        self.usage["output_tokens"] += out_tokens
        self.usage["cost"] += cost
        return {"input_tokens": in_tokens, "output_tokens": out_tokens, "cost": cost}

    def health_check(self):
        base = super().health_check()
        if base["status"] != "enabled":
            return base
        if not self.api_key:
            base["status"] = "misconfigured"
            base["reason"] = "API key 未配置（环境变量）"
        elif not self.config.get("base_url", ""):
            base["status"] = "misconfigured"
            base["reason"] = "base_url 未配置"
        return base

    def generate(self, prompt, system=None, **kwargs):
        if not self.config.get("enabled", False):
            raise RuntimeError("deepseek 未启用")
        if not self.api_key:
            raise RuntimeError("deepseek API key 未配置")
        base_url = self.config.get("base_url", "").rstrip("/")
        if not base_url:
            raise RuntimeError("deepseek base_url 未配置")
        url = base_url + "/chat/completions"
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        payload = json.dumps({
            "model": self.config.get("model", "deepseek-chat"),
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.2),
        }, ensure_ascii=False).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key,
        }
        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                req = urllib.request.Request(url, data=payload, headers=headers)
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                content = data["choices"][0]["message"]["content"]
                self._record_usage(data, payload.decode("utf-8"))
                return content
            except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError, KeyError) as exc:
                last_error = exc
                self.usage["failures"] += 1
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (attempt + 1))
        raise RuntimeError("deepseek generate failed after retries: %s" % last_error)