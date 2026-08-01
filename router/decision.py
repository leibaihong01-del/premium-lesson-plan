# -*- coding: utf-8 -*-
"""路由决策：按任务类型/复杂度选择 规则 / LLM / 混合，并支持降级。"""


RULE_INTENTS = {"convert", "audit"}
LLM_INTENTS = {"optimize", "plan", "generate"}


def decide(spec, enabled_providers=(), compute_level=None):
    """返回 {strategy, provider, reason}。

    规则：文件/固定流程/简单校验；
    LLM：复杂理解与方案生成（有可用模型时）；
    混合：生成内容后仍需规则校验（当前建议以规则为准）。
    """
    intent = spec.get("intent", "unknown")
    quality = spec.get("quality", "normal")
    providers = list(enabled_providers or [])
    has_llm = bool(providers)
    if intent in RULE_INTENTS:
        return {"strategy": "rule", "provider": None, "reason": "固定流程/校验任务"}
    if intent in LLM_INTENTS:
        if has_llm and quality == "excellent":
            return {"strategy": "hybrid", "provider": providers[0],
                    "reason": "复杂任务：LLM生成+规则校验"}
        if has_llm:
            return {"strategy": "llm", "provider": providers[0],
                    "reason": "语义增强任务"}
        return {"strategy": "rule", "provider": None, "reason": "无可用模型，回退规则"}
    if compute_level == "high" and has_llm:
        return {"strategy": "llm", "provider": providers[0], "reason": "高算力档启用LLM"}
    return {"strategy": "rule", "provider": None, "reason": "默认规则路径"}


def fallback_strategy(route):
    """LLM不可用时统一回退规则。"""
    if route.get("strategy") in ("llm", "hybrid"):
        return {"strategy": "rule", "provider": None,
                "reason": route.get("reason", "") + "；LLM不可用回退规则"}
    return route
