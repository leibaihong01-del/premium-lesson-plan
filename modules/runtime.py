# -*- coding: utf-8 -*-
"""运行时优化：文件哈希、结果缓存、增量跳过。"""
import hashlib
import json
import os


def file_hash(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_cache(path):
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_cache(path, cache):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def cached_review(docx_path, template_path, cache_path):
    """同文件+同模板且上次 PASS 时直接复用评分。"""
    cache = load_cache(cache_path)
    key = os.path.basename(docx_path)
    entry = cache.get(key)
    if entry:
        same_file = entry.get("doc_hash") == file_hash(docx_path)
        same_tpl = entry.get("tpl_hash") == file_hash(template_path)
        if same_file and same_tpl and entry.get("final") == "PASS":
            return entry, True
    return None, False


def put_cache(cache_path, docx_path, template_path, report):
    cache = load_cache(cache_path)
    key = os.path.basename(docx_path)
    cache[key] = {
        "doc_hash": file_hash(docx_path),
        "tpl_hash": file_hash(template_path),
        "total_score": report.get("total_score"),
        "final": report.get("final"),
        "scores": {
            "template": report.get("template_score"),
            "content": report.get("content_score"),
            "teaching": report.get("teaching_score"),
            "format": report.get("format_score"),
        },
    }
    save_cache(cache_path, cache)


def normalize_cached(entry):
    scores = entry.get("scores", {})
    return {
        "file": entry.get("file", ""),
        "template_score": scores.get("template", 0),
        "content_score": scores.get("content", 0),
        "teaching_score": scores.get("teaching", 0),
        "format_score": scores.get("format", 0),
        "total_score": entry.get("total_score", 0),
        "final": entry.get("final", "REPAIR_REQUIRED"),
        "loops": 0,
        "issues": {},
    }
