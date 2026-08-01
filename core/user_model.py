# -*- coding: utf-8 -*-
"""用户理解模型：从任务、反馈与历史沉淀用户工作模型。"""
import time


class UserModel:
    def __init__(self, memory):
        self.memory = memory

    def ingest_task(self, spec):
        prefs = self.memory._load("user_preferences")
        stats = prefs.setdefault("user_model", {}).setdefault("stats", {})
        for d in spec.get("domains", []):
            stats[d] = stats.get(d, 0) + 1
        quality = spec.get("quality", "normal")
        stats["quality_" + quality] = stats.get("quality_" + quality, 0) + 1
        prefs["user_model"]["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.memory._save("user_preferences", prefs)

    def ingest_feedback(self, feedback, outcome=None):
        prefs = self.memory._load("user_preferences")
        preferences = prefs.setdefault("preferences", {})
        if any(k in feedback for k in ("不满意", "不够好", "不符合")):
            preferences["不接受简单修改"] = True
        if any(k in feedback for k in ("精品", "标准", "申报")):
            preferences["重视精品标准"] = True
        if any(k in feedback for k in ("报告", "闭环", "流程")):
            preferences["要求闭环报告"] = True
        if "岗位" in feedback:
            preferences["重视岗位能力"] = True
        history = prefs.setdefault("user_model", {}).setdefault("feedback", [])
        history.append({"text": feedback[:200], "outcome": outcome,
                        "time": time.strftime("%Y-%m-%d %H:%M:%S")})
        prefs["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.memory._save("user_preferences", prefs)
        return preferences

    def profile(self):
        return self.memory._load("user_preferences")
