# -*- coding: utf-8 -*-
"""规则评分指标：不依赖LLM自评。"""


REQUIRED_KEYS = ["intent", "domains", "quality", "deliverables", "constraints", "compute_hint"]


def structure_score(spec):
    return 1.0 if all(k in spec for k in REQUIRED_KEYS) else 0.0


def content_score(spec, expected):
    parts = []
    parts.append(1.0 if spec.get("intent") == expected.get("intent") else 0.0)
    parts.append(1.0 if spec.get("quality") == expected.get("quality") else 0.0)
    exp_d = set(expected.get("domains", []))
    out_d = set(spec.get("domains", []))
    parts.append(len(exp_d & out_d) / len(exp_d) if exp_d else 1.0)
    exp_c = set(expected.get("constraints", []))
    out_c = set(spec.get("constraints", []))
    parts.append(len(exp_c & out_c) / len(exp_c) if exp_c else 1.0)
    exp_dl = set(expected.get("deliverables", []))
    out_dl = set(spec.get("deliverables", []))
    parts.append(len(exp_dl & out_dl) / len(exp_dl) if exp_dl else 1.0)
    return round(sum(parts) / len(parts), 4)


def task_match(spec, expected):
    ok_intent = spec.get("intent") == expected.get("intent")
    ok_domains = set(expected.get("domains", [])) <= set(spec.get("domains", []))
    return 1.0 if ok_intent and ok_domains else 0.0


def cost_estimate(input_text, output_text=None, price_per_1k=0.0):
    """token估算：中文按字符数/1.5 粗略估算；价格默认0（规则基线）。"""
    in_tokens = max(1, int(len(input_text or "") / 1.5))
    out_tokens = max(1, int(len(output_text or "") / 1.5))
    return {"input_tokens": in_tokens, "output_tokens": out_tokens,
            "cost": round((in_tokens + out_tokens) / 1000 * price_per_1k, 6)}


def evaluate(spec, expected, input_text="", output_text="", latency_ms=0.0):
    content = content_score(spec, expected)
    structure = structure_score(spec)
    match = task_match(spec, expected)
    cost = cost_estimate(input_text, output_text)
    return {
        "content": content,
        "structure": structure,
        "task_match": match,
        "cost": cost,
        "latency_ms": latency_ms,
        "pass": structure == 1.0 and content >= 0.8 and match == 1.0,
    }
