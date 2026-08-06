# -*- coding: utf-8 -*-
"""Artifact Delivery Protocol helper.

Classifies generated outputs, builds a delivery manifest, and reports the
delivery status (chat_attachment when the runtime supports file mounting,
otherwise local_artifact).
"""
import argparse
import json
import os
import sys
import time


ARTIFACT_EXTS = {
    ".docx", ".pdf", ".xlsx", ".xls", ".pptx", ".ppt",
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".md", ".json",
}
LOG_EXTS = {".log", ".err", ".trace"}

PRIORITY = {
    ".docx": 1, ".pdf": 1,
    ".md": 2, ".json": 2,
    ".xlsx": 2, ".xls": 2, ".pptx": 2, ".ppt": 2,
    ".png": 2, ".jpg": 2, ".jpeg": 2, ".gif": 2, ".bmp": 2, ".webp": 2,
}

PURPOSE = {
    ".docx": "\u6b63\u5f0f\u6587\u6863",
    ".pdf": "\u9884\u89c8\u7248",
    ".xlsx": "\u8868\u683c\u6570\u636e",
    ".pptx": "\u6f14\u793a\u6587\u6863",
    ".md": "\u6587\u672c\u62a5\u544a",
    ".json": "\u7ed3\u6784\u5316\u6570\u636e",
    ".png": "\u56fe\u7247",
    ".jpg": "\u56fe\u7247",
    ".jpeg": "\u56fe\u7247",
}

OPEN_METHOD = {
    ".docx": "Word/WPS \u6253\u5f00",
    ".pdf": "PDF \u9605\u8bfb\u5668\u6253\u5f00",
    ".xlsx": "Excel/WPS \u6253\u5f00",
    ".pptx": "PowerPoint/WPS \u6253\u5f00",
    ".md": "Markdown \u9605\u8bfb\u5668\u6216\u8bb0\u4e8b\u672c\u6253\u5f00",
    ".json": "\u6587\u672c\u7f16\u8f91\u5668\u6253\u5f00",
    ".png": "\u56fe\u7247\u67e5\u770b\u5668\u6253\u5f00",
    ".jpg": "\u56fe\u7247\u67e5\u770b\u5668\u6253\u5f00",
    ".jpeg": "\u56fe\u7247\u67e5\u770b\u5668\u6253\u5f00",
}

NOTICE = "\u5f53\u524d\u73af\u5883\u4ec5\u751f\u6210\u672c\u5730\u6587\u4ef6\uff0c\u65e0\u6cd5\u8f6c\u6362\u4e3a\u804a\u5929\u9644\u4ef6\u3002"


def classify(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in LOG_EXTS:
        return "log"
    if ext in ARTIFACT_EXTS:
        return "artifact"
    return "other"


def group_name(ext, category):
    if category == "log":
        return "\u65e5\u5fd7"
    if ext in (".docx", ".pdf"):
        return "primary"
    return "analysis"


def collect(delivery_dir):
    files = []
    for root, _, names in os.walk(delivery_dir):
        for name in names:
            full = os.path.join(root, name)
            if name.startswith("delivery_manifest"):
                continue
            ext = os.path.splitext(name)[1].lower()
            category = classify(name)
            files.append({
                "name": name,
                "path": os.path.abspath(full),
                "category": category,
                "priority": PRIORITY.get(ext, 3),
                "delivery_group": group_name(ext, category),
                "purpose": PURPOSE.get(ext, ""),
                "open_method": OPEN_METHOD.get(ext, ""),
                "size": os.path.getsize(full),
            })
    files.sort(key=lambda f: (f["priority"], f["name"]))
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("delivery_dir")
    parser.add_argument("--label", default="experiment")
    args = parser.parse_args()
    if not os.path.isdir(args.delivery_dir):
        print("delivery dir not found:", args.delivery_dir)
        return 1
    supported = os.environ.get("ARTIFACT_MOUNT_SUPPORTED", "0") == "1"
    status = "chat_attachment" if supported else "local_artifact"
    files = collect(args.delivery_dir)
    manifest = {
        "protocol": "artifact_delivery",
        "label": args.label,
        "delivery_status": status,
        "environment_notice": "" if supported else NOTICE,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "files": files,
    }
    manifest_path = os.path.join(args.delivery_dir, "delivery_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    artifacts = [f for f in files if f["category"] == "artifact"]
    print("status:", status)
    print("artifacts:", len(artifacts))
    print("manifest:", manifest_path)
    if not supported:
        print(NOTICE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
