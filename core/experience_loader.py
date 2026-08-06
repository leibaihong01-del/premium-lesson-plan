# -*- coding: utf-8 -*-
"""ExperienceLoader：按文档类型真实加载经验，输出 Applicable Experience Set。"""
import hashlib
import os
import time

from experience_registry import ExperienceRegistry


class ExperienceLoader:
    def __init__(self, registry_path=None, config_path=None, enabled=None,
                 project_root=None, courseagent_root=None):
        self.courseagent_root = courseagent_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.project_root = project_root or os.path.dirname(self.courseagent_root)
        self.config_path = config_path or os.path.join(self.courseagent_root, "config", "experience_integration.yaml")
        self.registry_path = registry_path or os.path.join(self.courseagent_root, "data", "experience_registry.json")
        self.enabled = self._read_enabled() if enabled is None else enabled
        self.registry = ExperienceRegistry(self.registry_path, project_root=self.project_root)

    def _read_enabled(self):
        try:
            with open(self.config_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("experience_integration_enabled:"):
                        value = line.split(":", 1)[1].strip().lower()
                        return value in ("true", "1", "yes")
        except Exception:
            pass
        return False

    @staticmethod
    def _file_hash(path):
        if not path or not os.path.isfile(path):
            return None
        try:
            with open(path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()[:12]
        except Exception:
            return None

    def _load_entry(self, entry):
        source_files = []
        missing_files = []
        hashes = []
        rels = entry.get("source_files", []) or []
        if not rels:
            missing_files.append(entry.get("missing_note") or entry.get("experience_id"))
        for rel in rels:
            resolved = self.registry.resolve(rel)
            source_files.append(resolved)
            h = self._file_hash(resolved)
            if h is None:
                missing_files.append(rel)
            hashes.append(h)
        loaded = self.enabled and bool(source_files) and not missing_files
        return {
            "experience_id": entry.get("experience_id"),
            "name": entry.get("name"),
            "status": entry.get("status"),
            "phase": entry.get("phase"),
            "judgment": entry.get("judgment"),
            "strategy": entry.get("strategy"),
            "applicable_scope": entry.get("applicable_scope", []),
            "impact": entry.get("impact"),
            "source_files": source_files,
            "file_hashes": hashes,
            "loaded": loaded,
            "missing_files": missing_files,
            "missing_note": entry.get("missing_note"),
        }

    def load(self, document_type, template=None, task_context=None):
        loaded_at = time.strftime("%Y-%m-%dT%H:%M:%S")
        experiences = []
        if self.enabled:
            for entry in self.registry.for_document_type(document_type):
                experiences.append(self._load_entry(entry))
        loaded_count = sum(1 for e in experiences if e["loaded"])
        missing_count = sum(1 for e in experiences if not e["loaded"])
        return {
            "document_type": document_type,
            "template": template,
            "task_context": task_context or {},
            "enabled": self.enabled,
            "loaded_at": loaded_at,
            "experiences": experiences,
            "loaded_count": loaded_count,
            "missing_count": missing_count,
            "applicable_experience_set": True,
        }