# -*- coding: utf-8 -*-
"""真实 MiMo API 冒烟测试入口。

仅在 MIMO_API_KEY 与 MIMO_BASE_URL 配置时执行真实调用；
未配置时返回 skipped 结构化结果。
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from providers.vision import analyze_media
from providers.vision.mimo import MimoVisionProvider
from providers.vision.schema import normalize_vision_result, validate_vision_result


def run_smoke(image_path, prompt="请用一句话描述图片内容"):
    api_key = os.getenv("MIMO_API_KEY", "")
    base_url = os.getenv("MIMO_BASE_URL", "")
    if not api_key or not base_url:
        print("SKIP: MIMO_API_KEY / MIMO_BASE_URL 未配置")
        return {"ok": False, "skipped": True, "reason": "环境变量未配置"}
    provider = MimoVisionProvider({
        "enabled": True,
        "base_url": base_url,
        "api_key_env": "MIMO_API_KEY",
        "model": os.getenv("MIMO_MODEL", "mimo-v2.5"),
    })
    result = analyze_media(image_path, prompt, provider)
    norm = normalize_vision_result(result)
    schema = validate_vision_result(norm)
    norm["schema_valid"] = schema["valid"]
    norm["schema_errors"] = schema["errors"]
    print(json.dumps(norm, ensure_ascii=False, indent=2))
    return norm


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MiMo 冒烟测试")
    parser.add_argument("path", help="图片或PDF路径")
    parser.add_argument("--prompt", default="请用一句话描述图片内容")
    args = parser.parse_args()
    run_smoke(args.path, args.prompt)