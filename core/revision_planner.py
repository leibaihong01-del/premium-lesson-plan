# -*- coding: utf-8 -*-
"""Revision Planner：只生成修订计划，不自动执行。"""
import time


class RevisionPlanner:
    name = "Revision Planner"

    def plan(self, reports):
        actions = []
        ref = reports.get("reference", {})
        if ref.get("status") in ("fail", "review"):
            for c in ref.get("checks", []):
                if c.get("type") == "content_pollution" and c.get("status") == "fail":
                    actions.append({
                        "issue": "参考文献内容污染",
                        "cause": "参考文献区域存在网页残留/特殊字符",
                        "strategy": "仅清理污染字符，保留编号/作者/题名/来源/年份/页码",
                        "priority": 1,
                        "risk": "low",
                    })
                if c.get("type") == "visual_hanging_indent" and c.get("status") == "review":
                    actions.append({
                        "issue": "参考文献续行未形成模板悬挂关系",
                        "cause": "悬挂缩进不符合模板黄金样本",
                        "strategy": "依据模板样式调整段落悬挂缩进，禁止固定数值",
                        "priority": 1,
                        "risk": "low",
                    })
        arkm = reports.get("academic", {})
        if arkm.get("status") in ("fail", "review"):
            for r in arkm.get("requirements", []):
                if r.get("status") == "fail":
                    actions.append({
                        "issue": r.get("name"),
                        "cause": "学院要求未满足",
                        "strategy": "按 ARKM 来源规则局部处理或人工确认",
                        "priority": 1 if r.get("id", "").endswith(("001",)) else 2,
                        "risk": "medium",
                    })
        content = reports.get("content", {})
        if content.get("status") in ("fail", "review"):
            for c in content.get("checks", []):
                if c.get("status") == "fail" and c.get("type") in ("student_identity", "task_match"):
                    actions.append({
                        "issue": "身份/任务信息不一致",
                        "cause": "成果内容与 StudentProfile 不一致",
                        "strategy": "以 StudentProfile 为唯一数据源修正",
                        "priority": 1,
                        "risk": "medium",
                    })
                if c.get("status") == "fail" and c.get("type") == "content_rule":
                    actions.append({
                        "issue": "禁用表达/占位符",
                        "cause": "成果正文存在违规表达或占位符",
                        "strategy": "人工复核改写，禁止自动改写正文",
                        "priority": 2,
                        "risk": "medium",
                    })
        return {
            "schema_version": "0.7-revision-plan-v1",
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "auto_apply": False,
            "actions": actions,
        }