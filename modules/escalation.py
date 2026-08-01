# -*- coding: utf-8 -*-
"""渐进式算力升级：low → medium → high，结合历史成败调整。"""


LEVELS = ["low", "medium", "high"]


def upgrade(level):
    idx = LEVELS.index(level) if level in LEVELS else 0
    return LEVELS[min(idx + 1, len(LEVELS) - 1)]


def downgrade(level):
    idx = LEVELS.index(level) if level in LEVELS else 1
    return LEVELS[max(idx - 1, 0)]


def suggest(level, task_type, history):
    """历史 ≥2 次失败升一级；连续 ≥5 次达标尝试降一级。"""
    relevant = [h for h in history if h.get("task_type") == task_type]
    failures = [h for h in relevant if h.get("score", 0) < 95]
    successes = [h for h in relevant if h.get("score", 0) >= 95]
    if len(failures) >= 2:
        return upgrade(level), "历史失败≥2次，自动升级"
    if len(successes) >= 5:
        return downgrade(level), "连续5次达标，尝试降档"
    return level, ""
