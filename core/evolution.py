# -*- coding: utf-8 -*-
"""自我进化系统：问题发现→分类→方案→验证→经验→可控升级→成长评分。"""
import time


CATEGORIES = {
    "需求理解": ["需求", "理解", "意图", "用户"],
    "专业能力": ["专业", "课程", "岗位", "知识", "标准"],
    "输出质量": ["质量", "评分", "逻辑", "完整"],
    "格式": ["格式", "表格", "分页", "模板", "字体"],
    "创新": ["创新", "案例", "特色"],
    "外部变化": ["政策", "标准更新", "趋势", "新规"],
}


class Evolution:
    def __init__(self, memory):
        self.memory = memory

    def classify(self, text):
        for cat, keys in CATEGORIES.items():
            if any(k in text for k in keys):
                return cat
        return "其他"

    def propose_solution(self, category):
        return {
            "需求理解": "重新解析用户意图并核对任务基线",
            "专业能力": "补充专业标准与岗位能力分析",
            "输出质量": "进入修复循环并提高评分阈值",
            "格式": "执行模板符合度检查与格式修复",
            "创新": "增加案例与职教特色要素",
            "外部变化": "更新知识库并提示模板升级",
            "其他": "记录问题并人工复核",
        }.get(category, "记录并复核")

    def record_outcome(self, task, score, passed, issues, feedback=""):
        cat = self.classify(" ".join(issues or []) + " " + feedback)
        entry = {
            "task": task,
            "score": score,
            "passed": passed,
            "category": cat,
            "issues": issues or [],
            "feedback": feedback,
            "solution": self.propose_solution(cat),
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.memory.add("successes" if passed else "failures", entry)
        self.memory.add("problems", {"problem": str(issues or feedback)[:200], "category": cat})
        self.memory.add("solutions", {"category": cat, "solution": entry["solution"]})
        self.memory.add("lessons_learned", {"category": cat, "lesson": entry["solution"]})
        return entry

    def controlled_upgrade(self, level, rule_text):
        approval = {"L1": "auto", "L2": "pending_verify", "L3": "pending_approval"}.get(level, "auto")
        entry = {"level": level, "rule": rule_text, "approval": approval,
                 "time": time.strftime("%Y-%m-%d %H:%M:%S")}
        self.memory.add("rules", entry)
        if approval == "auto":
            self.memory.add("improvements", {"rule": rule_text, "source": "evolution.L1"})
        return entry

    def growth_score(self):
        s = self.memory._load("successes")
        f = self.memory._load("failures")
        r = self.memory._load("rules")
        p = self.memory._load("problems")
        base = 60
        base += min(20, len(s) * 2)
        base += min(10, len(r) * 2)
        base += min(10, len(p))
        if s or f:
            base += int(10 * len(s) / (len(s) + len(f)))
        return min(100, base)
