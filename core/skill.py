# -*- coding: utf-8 -*-
"""Skill六件套抽象：执行器/评价器/反思器/优化器/经验库/进化器。"""


class SkillUnit:
    def __init__(self, name, executor, evaluator=None, reflector=None, optimizer=None,
                 experience_ns=None, evolution_hook=None, memory=None):
        self.name = name
        self.executor = executor
        self.evaluator = evaluator
        self.reflector = reflector
        self.optimizer = optimizer
        self.experience_ns = experience_ns
        self.evolution_hook = evolution_hook
        self.memory = memory

    def run(self, payload, max_optimize=2):
        trace = [("EXEC", self.name)]
        out = self.executor(payload)
        eval_res = self.evaluator(out, payload) if self.evaluator else {"passed": True, "score": None}
        for i in range(max_optimize):
            if eval_res.get("passed", True):
                break
            if self.optimizer:
                out = self.optimizer(out, payload, eval_res)
                eval_res = self.evaluator(out, payload)
                trace.append(("OPT" + str(i + 1), self.name))
        if self.reflector:
            self.reflector(out, eval_res, payload)
        if self.experience_ns and self.memory:
            self.memory.add(self.experience_ns, {
                "skill": self.name,
                "passed": eval_res.get("passed"),
                "score": eval_res.get("score"),
            })
        if self.evolution_hook and not eval_res.get("passed", True):
            self.evolution_hook(self.name, eval_res)
        return {"output": out, "evaluation": eval_res, "trace": trace}


class SkillRegistry:
    def __init__(self, memory=None):
        self.skills = {}
        self.memory = memory

    def register(self, unit):
        unit.memory = unit.memory or self.memory
        self.skills[unit.name] = unit
        return unit

    def run(self, name, payload):
        return self.skills[name].run(payload)

    def list_skills(self):
        return sorted(self.skills)
