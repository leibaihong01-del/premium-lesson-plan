# -*- coding: utf-8 -*-
"""问题解决Agent：原因分析→候选方案→择优→验证计划。"""


CANDIDATES = {
    "需求理解": ["重新解析用户意图并输出需求澄清问题", "核对任务基线表并重排交付物"],
    "专业能力": ["补充专业标准与岗位能力分析", "引用教材与行业案例增强专业度"],
    "输出质量": ["进入修复循环并按四维评分复检", "拆分长句、重构逻辑结构"],
    "格式": ["执行模板符合度检查", "按行高/分页规则自动修复"],
    "创新": ["增加职教特色案例与项目化设计", "引入课程思政映射"],
    "外部变化": ["更新知识库并提示模板升级", "等待人工确认新标准"],
    "其他": ["记录问题并提交人工复核"],
}


class ProblemSolver:
    def __init__(self, memory):
        self.memory = memory

    def solve(self, problem, category="其他", context=""):
        candidates = CANDIDATES.get(category, CANDIDATES["其他"])
        chosen = candidates[0]
        solution = {
            "problem": problem,
            "category": category,
            "candidates": candidates,
            "chosen": chosen,
            "reason": "符合成本-效果优先级：先规则修复，再专业增强",
            "verify_plan": "重新执行质量评分与需求匹配，达到≥95且通过Intent Alignment",
            "time": __import__("time").strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.memory.add("solutions", {"category": category, "solution": chosen, "problem": problem[:120]})
        return solution
