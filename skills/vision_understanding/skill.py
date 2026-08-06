# -*- coding: utf-8 -*-
"""Vision Understanding Skill：调用 Vision Provider 输出结构化 JSON。"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from providers.vision import VisionProviderRegistry, analyze_media


def build_provider(config=None, registry=None):
    from providers.vision.mimo import MimoVisionProvider
    cfg = config or {}
    reg = registry or VisionProviderRegistry()
    provider = MimoVisionProvider(cfg)
    reg.register(provider.name, provider)
    return provider, reg


def run_vision_analysis(path, prompt, provider=None, config=None, page_index=0, **kwargs):
    """Skill 主函数：返回结构化 dict。"""
    if provider is None:
        cfg = config or {"enabled": False}
        provider, _ = build_provider(cfg)
    result = analyze_media(path, prompt, provider, page_index=page_index, **kwargs)
    result.setdefault("skill", "vision_understanding")
    result.setdefault("input", path)
    result.setdefault("prompt", prompt)
    return result


def summarize(result):
    """面向教师的摘要：直接可读文本。"""
    if not result.get("ok"):
        return "视觉分析未完成：" + str(result.get("error", "未知错误"))
    analysis = (result.get("analysis") or result.get("content")
                or result.get("visual_analysis") or "")
    return "视觉分析完成：" + str(analysis)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Vision Understanding Skill")
    parser.add_argument("path", help="图片或PDF路径")
    parser.add_argument("--prompt", default="请分析该视觉材料并输出结构化JSON")
    parser.add_argument("--page", type=int, default=0)
    args = parser.parse_args()
    out = run_vision_analysis(args.path, args.prompt, page_index=args.page)
    print(json.dumps(out, ensure_ascii=False, indent=2))