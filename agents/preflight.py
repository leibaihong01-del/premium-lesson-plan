# -*- coding: utf-8 -*-
"""Preflight Agent：任务执行前需求预审（行为规范层，5.2-E 小范围验证）。"""
import time


def preflight(request, spec=None, user_profile=None):
    """返回需求预审报告：复述、信息完整性、第一性审查、确认状态。"""
    req = request or ""
    spec = spec or {}
    restate = "目标：%s" % (spec.get("goal") or req[:120])
    checks = {
        "requirement_restated": bool(restate),
        "intent_known": spec.get("intent") not in (None, "unknown"),
        "domains_known": bool(spec.get("domains")) and "未知" not in spec.get("domains", []),
        "constraints_recorded": bool(spec.get("constraints")),
    }
    missing = [k for k, v in checks.items() if not v]
    first_principles = []
    if spec.get("intent") == "unknown":
        first_principles.append("意图不明确：需先确认真实目标")
    if not spec.get("domains") or "未知" in spec.get("domains", []):
        first_principles.append("领域不明确：需补充输入信息")
    if "精品" in req and spec.get("quality") != "excellent":
        first_principles.append("质量要求与输入不一致")
    return {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "restate": restate,
        "checks": checks,
        "missing": missing,
        "first_principles": first_principles,
        "needs_confirmation": bool(missing) or bool(first_principles),
        "confirmed": False,
    }