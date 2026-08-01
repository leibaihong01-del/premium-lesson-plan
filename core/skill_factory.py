# -*- coding: utf-8 -*-
"""默认Skill工厂：注册教学/文件/分析/竞赛/科研/成果/知识等能力单元。"""
import os
import shutil

from capabilities import generate as cap_generate
from core.excellence_engine import analyze
from core.intent_alignment import check as intent_check
from core.skill import SkillRegistry, SkillUnit
from core.translator import parse
from modules import content_checker, document_writer, format_checker


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, "reports")


def _intent_eval(memory):
    def _eval(out, p):
        spec = parse(p.get("request", "生成材料"), memory.user_profile())
        al = intent_check(spec, {"total_score": 100}, out)
        return {"passed": al["aligned"], "score": al["alignment_score"], "issues": al["issues"]}
    return _eval


def _doc_eval():
    weights = {"template": 30, "content": 25, "teaching": 25, "format": 20}
    from agents.reviewer import review

    def _eval(out, p):
        rep = review(out, p["template"], REPORTS, weights)
        return {"passed": rep["final"] == "PASS", "score": rep["total_score"], "issues": []}
    return _eval


def _file_exec(p):
    shutil.copy2(p["src"], p["out"])
    return p["out"]


def _file_eval(out, p):
    fmt = format_checker.check_format(out, p["template"])
    content = content_checker.check_content(out)
    passed = all(fmt["checks"].values()) and all(content["checks"].values())
    score = round((fmt["score"] + content["score"]) / 2, 1)
    return {"passed": passed, "score": score, "issues": fmt["issues"] + content["issues"]}


def build_defaults(memory):
    reg = SkillRegistry(memory)
    intent_eval = _intent_eval(memory)
    doc_eval = _doc_eval()

    def teach_exec(p):
        if p.get("fills"):
            return document_writer.generate_document(p["template"], p["out"], p["fills"], project_kind=p.get("kind", "lesson"))
        shutil.copy2(p["src"], p["out"])
        return p["out"]

    reg.register(SkillUnit("教学资源Skill", teach_exec, evaluator=doc_eval,
                           experience_ns="successes",
                           evolution_hook=lambda name, res: memory.add("improvements", {"skill": name})))
    reg.register(SkillUnit("文件Skill", _file_exec, evaluator=_file_eval,
                           experience_ns="successes"))
    reg.register(SkillUnit("分析Skill", lambda p: analyze(p["docx"]),
                           evaluator=lambda out, p: {"passed": out["total"] >= 90, "score": out["total"]},
                           experience_ns="best_practices"))
    for name, cap in (("竞赛Skill", "competition_plan"), ("科研Skill", "project_application"),
                      ("成果Skill", "software_copyright")):
        reg.register(SkillUnit(name, lambda p, c=cap: cap_generate(c, p),
                               evaluator=intent_eval, experience_ns="successes"))

    def know_exec(p):
        from core.knowledge_update import KnowledgeUpdateAgent
        ku = KnowledgeUpdateAgent(memory)
        return ku.ingest_update(p["domain"], p["title"], p["summary"])

    reg.register(SkillUnit("知识Skill", know_exec,
                           evaluator=lambda out, p: {"passed": True, "score": 100},
                           experience_ns="knowledge_updates"))
    return reg
