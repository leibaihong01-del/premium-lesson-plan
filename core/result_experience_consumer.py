# -*- coding: utf-8 -*-
"""Result Experience Consumer：旁路消费成果经验，不修改旧生成逻辑。"""
import hashlib
import json
import os
import time

from result_experience_context import ResultExperienceContext


class ResultExperienceConsumer:
    def __init__(self, registry_path=None, project_root=None, courseagent_root=None,
                 enabled=None, config_path=None):
        self.courseagent_root = courseagent_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.project_root = project_root or os.path.dirname(self.courseagent_root)
        self.registry_path = registry_path or os.path.join(self.courseagent_root, "data", "result_experience_registry.json")
        self.config_path = config_path or os.path.join(self.courseagent_root, "config", "experience_integration.yaml")
        self.enabled = self._read_enabled() if enabled is None else enabled

    def _read_enabled(self):
        try:
            with open(self.config_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("experience_integration_enabled:"):
                        return line.split(":", 1)[1].strip().lower() in ("true", "1", "yes")
        except Exception:
            pass
        return False

    @staticmethod
    def _file_hash(path):
        if not path or not os.path.isfile(path):
            return None
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()[:12]

    @staticmethod
    def _load_text(path):
        with open(path, encoding="utf-8") as f:
            return f.read()

    def build_context(self, student_name="", template_source="", generation_stage="planning"):
        context = ResultExperienceContext(
            student_name=student_name,
            template_source=template_source,
            generation_stage=generation_stage,
        )
        if not self.enabled:
            return context

        with open(self.registry_path, encoding="utf-8") as f:
            registry = json.load(f)

        for entry in registry.get("experiences", []):
            exp_id = entry.get("experience_id")
            rels = entry.get("source_files", []) or []
            if not rels:
                context.missing_experience.append({
                    "experience_id": exp_id,
                    "name": entry.get("name"),
                    "reason": entry.get("missing_note") or "未创建",
                })
                continue
            resolved = []
            for rel in rels:
                path = os.path.normpath(os.path.join(self.project_root, rel.replace("/", os.sep)))
                resolved.append({"path": path, "hash": self._file_hash(path)})
            if any(r["hash"] is None for r in resolved):
                context.missing_experience.append({
                    "experience_id": exp_id,
                    "name": entry.get("name"),
                    "reason": "来源文件缺失",
                    "source_files": rels,
                })
                continue
            name = entry.get("name", exp_id)
            context.loaded_experience.append({
                "experience_id": exp_id,
                "name": name,
                "phase": entry.get("phase"),
                "impact": entry.get("impact"),
                "source_files": rels,
                "hashes": [r["hash"] for r in resolved],
            })
            # 把真实内容放进上下文对应槽位
            if exp_id == "result_tkm_001":
                context.tkm = json.loads(self._load_text(resolved[0]["path"]))
            elif exp_id == "golden_case_wanghuan_001":
                context.golden_cases.append({"name": name, "content": self._load_text(resolved[0]["path"])})
            elif exp_id == "reference_quality_sense_001":
                context.reference_rules.append({"name": name, "content": self._load_text(resolved[0]["path"])})
            elif exp_id == "document_quality_sense_schema_001":
                context.quality_rules.append({"name": name, "content": self._load_text(resolved[0]["path"])})
            elif exp_id == "result_rules_set_001":
                for r in resolved:
                    context.quality_rules.append({"name": os.path.basename(r["path"]), "content": self._load_text(r["path"])})
        return context

    def trace(self, context, task_id):
        return {
            "trace_version": "0.7-result-experience-trace-v1",
            "student": context.student_name,
            "template": context.template_source,
            "task_id": task_id,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "generation_stage": context.generation_stage,
            "experience_integration_enabled": self.enabled,
            "loaded_experience": [e["name"] for e in context.loaded_experience],
            "missing_experience": [m["name"] for m in context.missing_experience],
            "context": context.to_dict(),
        }