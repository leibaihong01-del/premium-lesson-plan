# -*- coding: utf-8 -*-
"""generation_trace 写入：记录模板、Skill、生成过程与最终状态。"""
import json
import os


def build_generation_trace(applicable_set, skill, template_source, quality_checks=None,
                           revision_actions=None, final_validation=""):
    experience_loaded = []
    for exp in applicable_set.get("experiences", []):
        if exp.get("loaded"):
            experience_loaded.append({
                "experience_id": exp.get("experience_id"),
                "source_file": exp.get("source_files") or [],
                "phase": exp.get("phase"),
            })
    return {
        "trace_version": "0.7-generation-trace-v1",
        "document_type": applicable_set.get("document_type"),
        "skill": skill,
        "template_source": template_source,
        "task_id": applicable_set.get("task_id", ""),
        "experience_integration_enabled": applicable_set.get("enabled", False),
        "experience_loaded": experience_loaded,
        "quality_checks": quality_checks or [],
        "revision_actions": revision_actions or [],
        "final_validation": final_validation,
    }


def write_generation_trace(output_path, payload):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return output_path