# -*- coding: utf-8 -*-
"""模板理解 Demo：用 Vision 分析模板图片/PDF，输出模板结构 JSON。"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflows.vision_ingestion import run_vision_ingestion

DEFAULT_PROMPT = (
    "请分析该模板的版式结构：标题位置、正文区域、表格/图片区域、页眉页脚，"
    "输出结构化JSON，字段：layout_elements、page_size、notes"
)


def main():
    parser = argparse.ArgumentParser(description="Vision 模板理解 Demo")
    parser.add_argument("path", help="模板图片或PDF路径")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--enabled", action="store_true", help="启用 MiMo（需 MIMO_API_KEY/MIMO_BASE_URL）")
    parser.add_argument("--page", type=int, default=0)
    parser.add_argument("--out", default="", help="JSON 输出路径")
    args = parser.parse_args()

    config = {
        "enabled": args.enabled,
        "base_url": os.getenv("MIMO_BASE_URL", ""),
        "api_key_env": "MIMO_API_KEY",
        "model": os.getenv("MIMO_MODEL", "mimo-vision"),
    }
    result = run_vision_ingestion(
        args.path, args.prompt, config=config, page_index=args.page,
        enabled=args.enabled, providers=["mimo"] if args.enabled else [],
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("已写入:", args.out)


if __name__ == "__main__":
    main()