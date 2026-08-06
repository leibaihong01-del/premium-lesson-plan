# -*- coding: utf-8 -*-
"""MiMo Vision Provider：OpenAI Compatible Vision API 适配。

配置优先级：环境变量 > 配置文件默认值。
- MIMO_API_KEY：密钥（只从环境变量读取）
- MIMO_BASE_URL：服务地址（含 /v1）
- MIMO_MODEL：模型名
- MIMO_ENDPOINT：接口路径（默认 /chat/completions）

默认 disabled；支持 retry / timeout / cost 统计。
"""
import base64
import json
import os
import time
import urllib.error
import urllib.request

from .base import VisionProvider
from .schema import extract_json_text


class MimoVisionProvider(VisionProvider):
    name = "mimo"

    def __init__(self, config=None):
        super().__init__(config)
        self.api_key = os.getenv(self.config.get("api_key_env", ""), "") or os.getenv("MIMO_API_KEY", "")
        self.base_url = (self.config.get("base_url") or os.getenv("MIMO_BASE_URL", "") or "").rstrip("/")
        self.model = self.config.get("model") or os.getenv("MIMO_MODEL", "mimo-v2.5")
        self.endpoint = self.config.get("endpoint") or os.getenv("MIMO_ENDPOINT", "/chat/completions")
        self.timeout = float(self.config.get("timeout", 60) or 60)
        self.max_retries = int(self.config.get("max_retries", 2) or 2)
        self.retry_delay = float(self.config.get("retry_delay", 1.0) or 1.0)
        self.usage = {
            "calls": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "cost": 0.0,
            "failures": 0,
        }

    def health_check(self):
        enabled = bool(self.config.get("enabled", False))
        result = {"provider": self.name, "status": "enabled" if enabled else "disabled",
                  "latency_ms": None}
        if result["status"] != "enabled":
            return result
        if not self.api_key:
            result["status"] = "misconfigured"
            result["reason"] = "MIMO_API_KEY 未配置"
        elif not self.base_url:
            result["status"] = "misconfigured"
            result["reason"] = "MIMO_BASE_URL 未配置"
        return result

    def analyze(self, image_path, prompt, **kwargs):
        if not self.config.get("enabled", False):
            return {"ok": False, "error": "mimo vision 未启用", "provider": self.name}
        if not self.api_key:
            return {"ok": False, "error": "MIMO_API_KEY 未配置", "provider": self.name}
        if not os.path.exists(image_path):
            return {"ok": False, "error": "图片不存在", "path": image_path, "provider": self.name}
        if not self.base_url:
            return {"ok": False, "error": "MIMO_BASE_URL 未配置", "provider": self.name}
        url = self.base_url + self.endpoint
        mime = kwargs.get("mime", "image/png")
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        payload = json.dumps({
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url",
                         "image_url": {"url": "data:%s;base64,%s" % (mime, b64)}},
                    ],
                }
            ],
            "temperature": kwargs.get("temperature", 0.1),
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
                result = self._normalize(data, prompt)
                self._record_usage(data, payload.decode("utf-8"))
                return result
            except urllib.error.HTTPError as exc:
                last_error = exc
                self.usage["failures"] += 1
                body = ""
                try:
                    body = exc.read().decode("utf-8", "replace")[:500]
                except Exception:
                    pass
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                return {"ok": False, "error": "MiMo HTTP %s: %s" % (exc.code, body),
                        "provider": self.name, "http_status": exc.code}
            except (urllib.error.URLError, OSError, ValueError, KeyError) as exc:
                last_error = exc
                self.usage["failures"] += 1
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (attempt + 1))
        return {"ok": False, "error": "MiMo vision 调用失败: %s" % last_error,
                "provider": self.name}

    def _normalize(self, data, prompt):
        content = None
        try:
            content = data["choices"][0]["message"]["content"]
        except Exception:
            content = (data.get("content") or data.get("analysis")
                       or data.get("result") or data)
        if isinstance(content, list):
            texts = [c.get("text") for c in content if isinstance(c, dict) and c.get("text")]
            content = "\n".join(texts) if texts else json.dumps(content, ensure_ascii=False)
        parsed = extract_json_text(content)
        if isinstance(parsed, (dict, list)):
            return {"ok": True, "provider": self.name, "prompt": prompt,
                    "content": content, "analysis": parsed}
        if isinstance(parsed, dict):
            out = dict(parsed)
            out.setdefault("ok", True)
            out.setdefault("provider", self.name)
            out.setdefault("prompt", prompt)
            return out
        return {"ok": True, "provider": self.name, "prompt": prompt,
                "content": content, "analysis": content}

    def _record_usage(self, data, payload_text):
        usage = data.get("usage") or {}
        in_tokens = int(usage.get("prompt_tokens") or 0) or max(1, int(len(payload_text) / 1.5))
        out_tokens = int(usage.get("completion_tokens") or 0)
        self.usage["calls"] += 1
        self.usage["input_tokens"] += in_tokens
        self.usage["output_tokens"] += out_tokens
        return self.usage