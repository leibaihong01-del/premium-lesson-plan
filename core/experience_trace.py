# -*- coding: utf-8 -*-
"""experience_trace 写入：记录本次真实加载的经验与来源。"""
import json
import os


def build_experience_trace(applicable_set, skill, task_id):
    experiences = []
    for exp in applicable_set.get("experiences", []):
        experiences.append({
            "experience_id": exp.get("experience_id"),
            "name": exp.get("name"),
            "source_file": exp.get("source_files") or [],
            "loaded_at": applicable_set.get("loaded_at"),
            "applicable_scope": exp.get("applicable_scope") or [],
            "phase": exp.get("phase"),
            "loaded": exp.get("loaded", False),
            "missing_files": exp.get("missing_files") or [],
            "impact": exp.get("impact"),
        })
    return {
        "trace_version": "0.7-trace-v1",
        "document_type": applicable_set.get("document_type"),
        "skill": skill,
        "template_source": applicable_set.get("template"),
        "task_id": task_id,
        "generated_at": applicable_set.get("loaded_at"),
        "experience_integration_enabled": applicable_set.get("enabled", False),
        "experiences": experiences,
    }


def write_experience_trace(output_path, payload):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return output_path

def build_experience_effects(applicable_set, reports=None):
    """经验作用记录：loaded -> stage -> used_for -> effect。"""
    reports = reports or {}
    effects = []
    ref_report = reports.get("reference") or {}
    ref_issues = []
    for c in ref_report.get("checks", []):
        for item in c.get("items", []) or []:
            if item.get("status") == "review" and item.get("problem_type"):
                ref_issues.append(item["problem_type"])
    for exp in applicable_set.get("experiences", []):
        if not exp.get("loaded"):
            continue
        name = exp.get("name", "")
        stage = exp.get("phase", "")
        used_for = []
        if "Reference" in name:
            used_for = ["reference_layout_detection", "content_pollution_check"]
        elif "TKM" in name or "模板知识" in name:
            used_for = ["template_structure_check"]
        elif "Golden" in name or "黄金" in name:
            used_for = ["content_quality_check", "golden_case_reference"]
        elif "Document Quality" in name or "Document Quality Sense" in name:
            used_for = ["layout_quality_check"]
        elif "Output" in name:
            used_for = ["output_naming_check"]
        else:
            used_for = ["context_planning"]
        effect = {"detected": ref_issues or ["no_issue"], "decision": "revision_plan_generated" if ref_issues else "validation_report"}
        effects.append({
            "experience": name,
            "loaded": True,
            "stage": stage,
            "used_for": used_for,
            "effect": effect,
        })
    return effects