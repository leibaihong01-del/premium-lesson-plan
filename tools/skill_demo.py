# -*- coding: utf-8 -*-
"""Skill六件套冒烟：注册竞赛/分析/教案Skill并运行。"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from capabilities import generate as cap_generate
from core.excellence_engine import analyze
from core.intent_alignment import check as intent_check
from core.memory import Memory
from core.skill import SkillRegistry, SkillUnit
from core.translator import parse


def make_registry():
    m = Memory()
    reg = SkillRegistry(m)

    def cap_exec(p):
        return cap_generate(p["capability"], p)

    def cap_eval(out, p):
        spec = parse(p.get("request", "生成材料"), m.user_profile())
        al = intent_check(spec, {"total_score": 100}, out)
        return {"passed": al["aligned"], "score": al["alignment_score"], "issues": al["issues"]}

    reg.register(SkillUnit(
        "竞赛Skill", cap_exec, evaluator=cap_eval,
        reflector=lambda out, res, p: m.add("lessons_learned", {"skill": "竞赛Skill", "res": res}),
        experience_ns="successes", evolution_hook=lambda name, res: m.add("improvements", {"skill": name}),
    ))

    def ana_exec(p):
        return analyze(p["docx"])

    def ana_eval(out, p):
        return {"passed": out["total"] >= 90, "score": out["total"]}

    reg.register(SkillUnit(
        "分析Skill", ana_exec, evaluator=ana_eval,
        experience_ns="best_practices",
    ))

    def doc_exec(p):
        shutil.copy2(p["src"], p["out"])
        return p["out"]

    reg.register(SkillUnit(
        "教案Skill", doc_exec, evaluator=lambda out, p: {"passed": True, "score": 100},
        experience_ns="successes",
    ))
    return reg


def main():
    reg = make_registry()
    print("已注册Skill:", reg.list_skills())
    r1 = reg.run("竞赛Skill", {"capability": "competition_plan", "request": "生成精品比赛方案",
                                "course": "城市轨道交通概论", "major": "城市轨道交通通信信号技术",
                                "topic": "轨道交通系统组成认知", "name": "技能演示"})
    print("竞赛Skill:", r1["evaluation"])
    r2 = reg.run("分析Skill", {"docx": r"D:\Users\leibaihong\Desktop\课程材料优化\城市轨道交通概论智能课程建设\05_输出文件\《城市轨道交通概论》-教案（第1课）优化版.docx"})
    print("分析Skill:", r2["evaluation"])
    r3 = reg.run("教案Skill", {
        "src": r"D:\Users\leibaihong\Desktop\课程材料优化\城市轨道交通概论智能课程建设\05_输出文件\《城市轨道交通概论》-教案（第1课）优化版.docx",
        "out": os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "_skill_demo.docx")})
    print("教案Skill:", r3["evaluation"], "| traces:", [t[0] for t in r1["trace"]])


if __name__ == "__main__":
    main()
