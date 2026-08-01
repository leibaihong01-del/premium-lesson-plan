# -*- coding: utf-8 -*-
"""任务指纹、决策缓存与历史记录。"""
import hashlib
import json
import os


def fingerprint(meta, request=""):
    raw = {
        "type": meta.get("task_type", "docx"),
        "domain": meta.get("domain", "education"),
        "pages": meta.get("pages", 0),
        "tables": meta.get("tables", 0),
        "quality": "expert" if ("精品" in request or "专家" in request) else "formal" if ("正式" in request) else "normal",
        "request": (request or "")[:80],
    }
    h = hashlib.sha1()
    h.update(json.dumps(raw, ensure_ascii=False, sort_keys=True).encode("utf-8"))
    return h.hexdigest()[:16]


def load(path, default):
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default


def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def lookup(patterns_path, fp):
    patterns = load(patterns_path, {})
    return patterns.get(fp)


def store(patterns_path, fp, decision):
    patterns = load(patterns_path, {})
    patterns[fp] = decision
    save(patterns_path, patterns)


def append_history(path, entry, limit=200):
    history = load(path, [])
    history.append(entry)
    save(path, history[-limit:])
