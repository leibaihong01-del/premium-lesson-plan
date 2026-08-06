# -*- coding: utf-8 -*-
"""自适应路由 Agent：指纹→决策缓存→规则分类→轻量判断→历史调整。"""
import os

from agents.light_judge import judge
from modules import decision_cache, escalation, fast_classifier


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY = os.path.join(ROOT, "memory")
PATTERNS = os.path.join(MEMORY, "task_patterns.json")
HISTORY = os.path.join(MEMORY, "compute_history.json")
RULES = os.path.join(MEMORY, "decision_rules.json")


def route(meta, request="", force_profile=None):
    fp = decision_cache.fingerprint(meta, request)
    cached = decision_cache.lookup(PATTERNS, fp)
    if cached and not force_profile:
        cached = dict(cached)
        cached["source"] = "decision_cache"
        return cached
    dec = fast_classifier.classify(meta, request)
    if dec["confidence"] < 0.9:
        dec = judge(meta, request, dec)
        dec["reason"].append("level2_light_judge")
    if force_profile and force_profile != "auto":
        dec["recommended_compute"] = force_profile
        dec["reason"].append("force_profile")
        dec["fingerprint"] = fp
        dec["source"] = "forced"
        return dec
    if force_profile == "auto":
        dec["reason"].append("profile_auto")
    history = decision_cache.load(HISTORY, [])
    adjusted, note = escalation.suggest(dec["recommended_compute"], meta.get("task_type", "docx"), history)
    if note:
        dec["recommended_compute"] = adjusted
        dec["reason"].append(note)
    dec["fingerprint"] = fp
    dec["source"] = "rule_classifier"
    decision_cache.store(PATTERNS, fp, dec)
    return dec


def record(meta, score, passed, loops, level):
    entry = {
        "task_type": meta.get("task_type", "docx"),
        "score": score,
        "passed": passed,
        "loops": loops,
        "level": level,
        "time": __import__("time").strftime("%Y-%m-%d %H:%M:%S"),
    }
    decision_cache.append_history(HISTORY, entry)
