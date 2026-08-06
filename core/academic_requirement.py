# -*- coding: utf-8 -*-
"""Academic Requirement Knowledge Model：学院要求符合性判断。"""
import json
import os


class AcademicRequirementChecker:
    name = "Academic Requirement Compliance Sense"

    def __init__(self, arkm_path=None, courseagent_root=None):
        self.courseagent_root = courseagent_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.arkm_path = arkm_path or os.path.join(self.courseagent_root, "data", "academic_requirement_knowledge_model.json")

    def load(self):
        with open(self.arkm_path, encoding="utf-8") as f:
            return json.load(f)

    def check(self, model, content_report=None, reference_report=None):
        arkm = self.load()
        requirements = {r["id"]: r for r in arkm.get("requirements", [])}
        results = []

        # ARKM-CONTENT-001 必备内容完整
        req = requirements.get("ARKM-CONTENT-001")
        fixed = model.get("fixed_markers", {})
        titles = [s.get("title", "") for s in model.get("sections", [])]
        present = all(fixed.get(k, False) for k in ["摘要", "目录", "参考文献"]) and any(
            k in " ".join(titles) for k in ["总结", "结论"])
        results.append({"id": req["id"], "name": req["name"], "source": req["source"],
                        "status": "pass" if present else "fail", "detail": "必备内容"})

        # ARKM-CONTENT-002 禁用科研式表达
        req = requirements.get("ARKM-CONTENT-002")
        forbidden_hits = [c for c in (content_report or {}).get("checks", [])
                          if c.get("type") == "content_rule" and c.get("rule") == "forbidden_expression"]
        results.append({"id": req["id"], "name": req["name"], "source": req["source"],
                        "status": "fail" if forbidden_hits else "pass", "detail": "违规表达 %s 处" % len(forbidden_hits)})

        # ARKM-CONTENT-003 正文字数
        req = requirements.get("ARKM-CONTENT-003")
        chars = model.get("body_chars", 0)
        results.append({"id": req["id"], "name": req["name"], "source": req["source"],
                        "status": "pass" if chars >= 5000 else "fail",
                        "detail": "正文字数 %s" % chars})

        # ARKM-STRUCT-001 自动目录
        req = requirements.get("ARKM-STRUCT-001")
        toc_ok = model.get("toc_field_present", False)
        results.append({"id": req["id"], "name": req["name"], "source": req["source"],
                        "status": "pass" if toc_ok else "fail", "detail": "TOC域"})

        # ARKM-FORMAT-001 模板格式
        req = requirements.get("ARKM-FORMAT-001")
        format_ok = model.get("sections_count") == 4 and len(model.get("tables", [])) == 6 and 12.0 in model.get("body_font_sizes", [])
        results.append({"id": req["id"], "name": req["name"], "source": req["source"],
                        "status": "pass" if format_ok else "review",
                        "detail": "分节 %s / 表 %s / 字号 %s" % (
                            model.get("sections_count"), len(model.get("tables", [])), model.get("body_font_sizes"))})

        # ARKM-FORMAT-002 章节分页（无法从解析层直接证实，标记 review）
        req = requirements.get("ARKM-FORMAT-002")
        results.append({"id": req["id"], "name": req["name"], "source": req["source"],
                        "status": "review", "detail": "需渲染层复核章节分页"})

        # ARKM-REF-001 参考文献质量
        req = requirements.get("ARKM-REF-001")
        ref_status = (reference_report or {}).get("status", "unknown")
        results.append({"id": req["id"], "name": req["name"], "source": req["source"],
                        "status": "pass" if ref_status == "pass" else ("review" if ref_status == "review" else "fail"),
                        "detail": "Reference Quality Sense: %s" % ref_status})

        # ARKM-QUALITY-001 任务匹配
        req = requirements.get("ARKM-QUALITY-001")
        task_checks = [c for c in (content_report or {}).get("checks", []) if c.get("type") == "task_match"]
        task_status = "pass"
        for c in task_checks:
            if c.get("status") == "fail":
                task_status = "fail"
            elif c.get("status") == "review" and task_status == "pass":
                task_status = "review"
        results.append({"id": req["id"], "name": req["name"], "source": req["source"],
                        "status": task_status, "detail": "任务匹配"})

        status = "fail" if any(r["status"] == "fail" for r in results) else (
            "review" if any(r["status"] == "review" for r in results) else "pass")
        return {"sense": self.name, "status": status, "requirements": results, "model": arkm["organization"]}